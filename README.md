# Domain Adaptive Faster R-CNN in Detectron 

Forked from [Krumo's modification of Detectron](https://github.com/krumo/Detectron-DA-Faster-RCNN) to implement the techniques in this paper.

[Domain Adaptive Faster R-CNN for Object Detection in the Wild](https://arxiv.org/abs/1803.03243)

To train deepgrasp on the Jacquard dataset, run the following command


```Shell
cd $DETECTRON
python tools/train_net.py --cfg configs/deepgrasp/deepgrasp_faster_rcnn.yaml OUTPUT_DIR /tmp/detectron-output
