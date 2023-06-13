SKETCH_DATASET_PATH:="sketch_dataset"
DNB_DATASET_PATH:="dnb/processed/"

setup-model-training:
  cd ..
  mkdir data
  git clone https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.git gan-training
  pip install -r requirements.txt

setup-python:
  pip install -r requirements.txt

# TODO: Add scripts for setting up db
setup-db:
  @echo 'The db setup needs to be implemented.'

setup:
  just setup-python
  just setup-db
  just setup-model-training

prepare-dnb-dataset:
  @echo 'The dnb dataset preparation needs to be implemented.'

prepare-sketch-dataset:
  @echo 'The sketch dataset preparation needs to be implemented.'

prepare-datasets:
  just prepare-sketch-dataset
  just prepare-dnb-dataset

train-sketch-model modelname:
  cd ../gan-training/
  python train.py --dataroot ../data/{{SKETCH_DATASET_PATH}}/AB/ --name modelname --model pix2pix --direction BtoA

train-dnb-model modelname:
  cd ../gan-training/
  python train.py --dataroot ../data/{{DNB_DATASET_PATH}} --name modelname --model cycle_gan --batch_size=1 

