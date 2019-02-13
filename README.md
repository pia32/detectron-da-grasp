# Domain Adaptive Faster R-CNN in Detectron 

Forked from [Krumo's modification of Detectron](https://github.com/krumo/Detectron-DA-Faster-RCNN) to implement the techniques in this paper.

[Domain Adaptive Faster R-CNN for Object Detection in the Wild](https://arxiv.org/abs/1803.03243)

To train deepgrasp on the Jacquard dataset, run the following command


```Shell
cd $DETECTRON
python tools/train_net.py --cfg configs/deepgrasp/deepgrasp_faster_rcnn.yaml OUTPUT_DIR /tmp/detectron-output



To initially setup the datasets:

Download the Jacquard dataset into a datasets folder of your choosing using this shell script. [download_jacquard.sh](detectron/datasets/grasping/download_jacquard.sh)

Resize the dataset to be smaller using this matlab script. [generate_resized_Jacquard.m](detectron/datasets/grasping/generate_resized_Jacquard.m). Edit the paths at the top of the file as needed. This takes a long time. Note that this file expects to find the actual grasping files TWO directories down, not one.

Run prepare_coco_for_jacquard.py

Run grasps_to_coco.py

Add symlinks to the test and train folders in /detectron/datasets/data folder.

ln -s /local/patrick/datasets/jac_processed/test/ jacquard_test
ln -s /local/patrick/datasets/jac_processed/train/ jacquard_train
