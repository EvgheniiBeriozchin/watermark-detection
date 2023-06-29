"""
This script builds on train.py from https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.
"""
import time
import importlib
from functools import partial

from options.train_options import TrainOptions
from data import create_dataset
from models import create_model

from ray import tune
from ray.air import Checkpoint, session
from ray.tune.schedulers import ASHAScheduler

def train(config, *, dataset, opt):
    opt.batch_size = config["batch_size"]
    opt.lr = config["lr"]
    opt.num_epochs = 25

    model = create_model(opt)      # create a model given opt.model and other options
    model.setup(opt)               # regular setup: load and print networks; create schedulers
    total_iters = 0                # the total number of training iterations

    for epoch in range(opt.epoch_count, opt.n_epochs + opt.n_epochs_decay + 1):    # outer loop for different epochs; we save the model by <epoch_count>, <epoch_count>+<save_latest_freq>
        epoch_start_time = time.time()  # timer for entire epoch
        epoch_iter = 0                  # the number of training iterations in current epoch, reset to 0 every epoch
        model.update_learning_rate()    # update learning rates in the beginning of every epoch.
        for i, data in enumerate(dataset):  # inner loop within one epoch

            total_iters += opt.batch_size
            epoch_iter += opt.batch_size
            model.set_input(data)         # unpack data from dataset and apply preprocessing
            model.optimize_parameters()   # calculate loss functions, get gradients, update network weights
        print('End of epoch %d / %d \t Time Taken: %d sec' % (epoch, opt.n_epochs + opt.n_epochs_decay, time.time() - epoch_start_time))

    losses = model.get_current_losses()
    session.report(
        {"loss": losses["G_GAN"] + losses["G_L1"], "accuracy": -(losses["D_real"] + losses["D_fake"])},
        checkpoint=None,
    )

if __name__ == '__main__':
    num_samples = 12
    max_num_epochs = 25

    config = {
        "lr": tune.loguniform(2e-8, 2e-4),
        "batch_size": tune.choice([2, 4, 8])
    }

    scheduler = ASHAScheduler(
        metric="loss",
        mode="min",
        max_t=max_num_epochs,
        grace_period=1,
        reduction_factor=2,
    )

    opt = TrainOptions().parse()
    dataset = create_dataset(opt)
    dataset_size = len(dataset)
    print('The number of training images = %d' % dataset_size)
    
    result = tune.run(
        partial(train, dataset=dataset, opt=opt),
        resources_per_trial={"cpu": 24, "gpu": 1},
        config=config,
        num_samples=num_samples,
        scheduler=scheduler,
    )

    best_trial = result.get_best_trial("loss", "min", "last")
    print(f"Best trial config: {best_trial.config}")
    print(f"Best trial final validation loss: {best_trial.last_result['loss']}")
    print(f"Best trial final validation accuracy: {best_trial.last_result['accuracy']}")
