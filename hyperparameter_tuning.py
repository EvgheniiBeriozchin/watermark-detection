"""
This script builds on train.py from https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.
"""
import time
from functools import partial

from options.train_options import TrainOptions
from data import create_dataset
from models import create_model

from ray import tune
from ray.air import session
from ray.tune.schedulers import ASHAScheduler
from util.visualizer import Visualizer

def train(config, *, dataset, opt):
    opt.batch_size = config["batch_size"]
    opt.lr = config["lr"]
    print("Config: {}".format(config))
    opt.n_epochs = 10
    opt.n_epochs_decay = 0
    print("Options in train: {}".format(opt))
    model = create_model(opt)      # create a model given opt.model and other options
    model.setup(opt)               # regular setup: load and print networks; create schedulers
    visualizer = Visualizer(opt)   # create a visualizer that display/save images and plots
    total_iters = 0                # the total number of training iterations

    for epoch in range(opt.epoch_count, opt.n_epochs + opt.n_epochs_decay + 1):    # outer loop for different epochs; we save the model by <epoch_count>, <epoch_count>+<save_latest_freq>
        epoch_start_time = time.time()  # timer for entire epoch
        iter_data_time = time.time()    # timer for data loading per iteration
        epoch_iter = 0                  # the number of training iterations in current epoch, reset to 0 every epoch
        visualizer.reset()
        model.update_learning_rate()    # update learning rates in the beginning of every epoch.
        for i, data in enumerate(dataset):  # inner loop within one epoch
            iter_start_time = time.time()  # timer for computation per iteration
            if total_iters % opt.print_freq == 0:
                t_data = iter_start_time - iter_data_time

            total_iters += opt.batch_size
            epoch_iter += opt.batch_size
            model.set_input(data)         # unpack data from dataset and apply preprocessing
            model.optimize_parameters()   # calculate loss functions, get gradients, update network weights

            if total_iters % opt.display_freq == 0:   # display images on visdom and save images to a HTML file
                save_result = total_iters % opt.update_html_freq == 0
                model.compute_visuals()
                visualizer.display_current_results(model.get_current_visuals(), epoch, save_result)

            if total_iters % opt.print_freq == 0:    # print training losses and save logging information to the disk
                losses = model.get_current_losses()
                t_comp = (time.time() - iter_start_time) / opt.batch_size
                visualizer.print_current_losses(epoch, epoch_iter, losses, t_comp, t_data)
                if opt.display_id > 0:
                    visualizer.plot_current_losses(epoch, float(epoch_iter) / dataset_size, losses)
        print('End of epoch %d / %d \t Time Taken: %d sec' % (epoch, opt.n_epochs + opt.n_epochs_decay, time.time() - epoch_start_time))

    losses = model.get_current_losses()
    session.report(
        {"loss": losses["G_GAN"] + losses["G_L1"], "accuracy": -(losses["D_real"] + losses["D_fake"])}
        if opt.model == "pix2pix"  else 
        {"loss": losses["G_A"] + losses["cycle_A"] + losses['D_B'], "accuracy": -(losses["G_B"] + losses["cycle_B"] + losses['D_A'])},
        checkpoint=None,
    )

if __name__ == '__main__':
    num_samples = 20
    max_num_epochs = 10

    config = {
        "lr": tune.loguniform(2e-8, 1e-4),
        "batch_size": tune.choice([2, 4])
    }

    scheduler = ASHAScheduler(
        metric="loss",
        mode="min",
        max_t=max_num_epochs,
        grace_period=1,
        reduction_factor=2,
    )

    opt = TrainOptions().parse()
    print("Options: {}".format(opt))
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
