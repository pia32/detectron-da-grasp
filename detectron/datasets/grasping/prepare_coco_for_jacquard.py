import numpy as np
from PIL import Image, ImageDraw
import math
import numpy.matlib as npm
import os
import cv2
import matplotlib.pyplot as plt
import random


DATA_DIR = '/local/patrick/datasets/jac_resized'
ANNOTATION_OUT_TRAIN = '/local/patrick/datasets/jac_processed/train/annotations'
IMAGE_OUT_TRAIN = '/local/patrick/datasets/jac_processed/train/grasps_train2018'

ANNOTATION_OUT_TEST = '/local/patrick/datasets/jac_processed/train/annotations'
IMAGE_OUT_TEST = '/local/patrick/datasets/jac_processed/test/grasps_train2018'

VISUALIZE_UNROTATED = True
SHAPE = (512,512)

def convert5Pointto8Point(cx_, cy_, w_, h_, a_):

    theta = math.radians(a_)
    bbox = npm.repmat([[cx_], [cy_]], 1, 5) + \
       np.matmul([[math.cos(theta), math.sin(theta)],
                  [-math.sin(theta), math.cos(theta)]],
                 [[-w_ / 2, w_/ 2, w_ / 2, -w_ / 2, w_ / 2 + 8],
                  [-h_ / 2, -h_ / 2, h_ / 2, h_ / 2, 0]])
    # add first point
    x1, y1 = bbox[0][0], bbox[1][0]
    # add second point
    x2, y2 = bbox[0][1], bbox[1][1]
    # add third point
    #x3, y3 = bbox[0][4], bbox[1][4]
    # add forth point
    x3, y3 = bbox[0][2], bbox[1][2]
    # add fifth point
    x4, y4 = bbox[0][3], bbox[1][3]

    return [x1, y1, x2, y2, x3, y3, x4, y4]

for root, dirs, files in os.walk(DATA_DIR):
    path = root.split(os.sep)
    for file in files:
        # find RGB images
        if file[-7:] == 'RGD.png':
            # decide if train or test
            if random.random() > 0.2:
                ANNOTATION_OUT = ANNOTATION_OUT_TRAIN
                IMAGE_OUT = IMAGE_OUT_TRAIN
            else:
                ANNOTATION_OUT = ANNOTATION_OUT_TEST
                IMAGE_OUT = IMAGE_OUT_TEST

            # change the saving structure to grasp_train2018/Jacquard_Dataset_0/1a1ec1cfe633adcdebbf11b1629fc16a/
            # change the saving structure to     annotations/Jacquard_Dataset_0/1a1ec1cfe633adcdebbf11b1629fc16a/
            ANNOTATION_OUT = ANNOTATION_OUT + '/' + path[-2] + '/' + path[-1]
            IMAGE_OUT = IMAGE_OUT + '/' + path[-2] + '/' + path[-1]
            if not os.path.exists(ANNOTATION_OUT):
                os.makedirs(ANNOTATION_OUT)
            if not os.path.exists(IMAGE_OUT):
                os.makedirs(IMAGE_OUT)


            tmpPath = ("/").join(path) + '/' + file
            print ("processing image file: " + tmpPath)
            img = Image.open(tmpPath)

            maskPath = tmpPath.replace('_RGD.png', '_mask.png')
            imgMask = Image.open(maskPath)

            gtFile = tmpPath.replace('_RGD.png', '_grasps.txt')
            f = open(gtFile)
            line = f.readline()

            count = 0
            while line:
                parameters = line.split(';')
                parameters = [float(x) for x in parameters]

                # get overlap mask
                polygon_np = convert5Pointto8Point(parameters[0], parameters[1], parameters[3], parameters[4], -parameters[2])
                polygonMask = Image.new('L', SHAPE, 0)
                ImageDraw.Draw(polygonMask).polygon(polygon_np, outline=1, fill=1)
                #polygonMask.show()
                polygonMask_np = np.array(polygonMask)

                imgMask_np = np.array(imgMask)/255
                overlapingMask = (imgMask_np.astype('uint8') & polygonMask_np)*255
                overlapingMask = Image.fromarray(overlapingMask)
                #overlapingMask.show()

                #ImageDraw.Draw(img).polygon(polygon_np, outline=(255,255,255))
                #img.show()

                x = int(round(parameters[6],2)*100)
                y = int(round(parameters[7],2)*100)
                width = int(round(parameters[3],2)*100)
                height = int(round(parameters[4],2)*100)
                cls = int(parameters[5])

                maskSaveName = file[:-4] + '_orient' + str(cls).zfill(2) + '_' + str(count) + '_' + str(x) + '_' + str(y) + '_' + str(width) + '_' + str(height) + '.png'
                overlapingMask.save(ANNOTATION_OUT + '/' + maskSaveName)
                count += 1
                line = f.readline()

            f.close()

            img.save(IMAGE_OUT + '/' + file)



