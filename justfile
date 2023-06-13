


setup-model-training:
  cd ..
  mkdir data
  git clone https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.git
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

train-sketch-model:
  @echo 'The sketch dataset training needs to be implemented.'

train-dnb-model:
  @echo 'The dnb dataset training needs to be implemented.'

