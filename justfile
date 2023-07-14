SKETCH_DATASET_PATH:="sketch_dataset"
DNB_DATASET_PATH:="dnb/processed"

run imagepath modelname:
  rm -r outputs && mkdir outputs
  python3 -m pipeline.prepare_watermark --input_path {{imagepath}}
  cd ../gan-training && mkdir testA && mkdir testB && cp ../watermark-detection/outputs/tmp.jpg testA/ && cp ../watermark-detection/outputs/tmp.jpg testB/
  cd ../gan-training && python3 test.py --dataroot ./ --name {{modelname}} --model cycle_gan --no_dropout --results_dir ../watermark-detection/outputs/ && rm -r testA && rm -r testB
  rm outputs/tmp.jpg
  mv outputs/{{modelname}}/test_latest/images/tmp_fake_B.png outputs/tmp.jpg
  rm -r outputs/{{modelname}}
  python3 -m pipeline.get_nearest_neighbors                                                                  

setup-model-training:
  cd .. && mkdir data                            
  cd .. && git clone https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix.git gan-training                             
  cd ../gan-training && pip install -r requirements.txt

setup-python:
  pip install -r requirements.txt

setup-db:
  python data/create_table.py

setup:
  just setup-python
  just setup-db
  just setup-model-training

download-sketch-dataset:
  wget http://cybertron.cg.tu-berlin.de/eitz/projects/classifysketch/sketches_png.zip

download-dnb-dataset:
 @echo "Assuming dataset exists"

download-datasets:
  just download-sketch-dataset
  just download-dnb-dataset

[private]
transform-drawings path modelname:
  cp ../data/{{DNB_DATASET_PATH}}/{{path}}/* ../data/{{DNB_DATASET_PATH}}/tmp_src/test/
  python3 ../gan-training/datasets/combine_A_and_B.py --fold_A ../data/{{DNB_DATASET_PATH}}/tmp_src --fold_B ../data/{{DNB_DATASET_PATH}}/tmp_src  --fold_AB ../data/{{DNB_DATASET_PATH}}/tmp
  cd ../gan-training && python3 test.py --dataroot ../data/{{DNB_DATASET_PATH}}/tmp/ --name {{modelname}} --model pix2pix --direction BtoA --num_test 3000000
  rm -r ../data/{{DNB_DATASET_PATH}}/{{path}}/*
  mv ../gan-training/results/{{modelname}}/test_latest/images/*_fake_B.png ../data/{{DNB_DATASET_PATH}}/{{path}}
  python3 make_drawings_grayscale.py --path ../data/{{DNB_DATASET_PATH}}/{{path}}
  rm -r ../data/{{DNB_DATASET_PATH}}/tmp/*
  rm ../data/{{DNB_DATASET_PATH}}/tmp_src/test/*
  rm -r ../gan-training/results/{{modelname}}/test_latest


prepare-dnb-dataset modelname:
  python3 main.py
  cd ../data/{{DNB_DATASET_PATH}} && mkdir tmp && mkdir tmp_src && mkdir tmp2
  cd ../data/{{DNB_DATASET_PATH}}/tmp_src && mkdir test
  cd ../data/{{DNB_DATASET_PATH}}/tmp2 && mkdir trainB && mkdir testB
  just transform-drawings trainB {{modelname}}
  just transform-drawings testB {{modelname}}

  rm -r ../data/{{DNB_DATASET_PATH}}/tmp
  rm -r ../data/{{DNB_DATASET_PATH}}/tmp_src


prepare-sketch-dataset:
  python drawing-processing/sketch-dataset-preparation/transform_sketch_dataset.py
  python drawing-processing/sketch-dataset-preparation/image_noising.py

prepare-datasets modelname:
  just prepare-sketch-dataset {{modelname}}
  just prepare-dnb-dataset

train-sketch-model modelname:
  cd ../gan-training/ && python train.py --dataroot ../data/{{SKETCH_DATASET_PATH}}/AB/ --name {{modelname}} --model pix2pix --direction BtoA

train-dnb-model modelname:
  cd ../gan-training/ && python train.py --dataroot ../data/{{DNB_DATASET_PATH}} --name {{modelname}} --model cycle_gan --batch_size=1 
  cd ../gan-training/ && cp ./checkpoints/{{modelname}}/latest_net_G_A.pth ./checkpoints/{{modelname}}/latest_net_G.pth 

watermarks-to-outlines modelname sourcepath targetpath:
  mkdir {{targetpath}}/testA && mkdir {{targetpath}}/testB && cp {{sourcepath}}/* {{targetpath}}/testA && cp {{sourcepath}}/* {{targetpath}}/testB
  cd ../gan-training && python3 test.py --dataroot {{targetpath}} --name {{modelname}} --model cycle_gan --no_dropout --num_test 3000000
  rm -r {{targetpath}}/testA && rm -r {{targetpath}}/testB
  mv ../gan-training/results/{{modelname}}/test_latest/images/*_fake_B.png {{targetpath}}
  python3 make_drawings_grayscale.py --path {{targetpath}}

drawings-to-outlines modelname sourcepath targetpath:
  cd ../gan-training && python3 test.py --dataroot {{sourcepath}} --name {{modelname}} --model pix2pix --direction BtoA --num_test 3000000
  mv ../gan-training/results/{{modelname}}/test_latest/images/*_fake_B.png targetpath
  python3 make_drawings_grayscale.py --path targetpath