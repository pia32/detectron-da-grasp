#!/usr/bin/env python3

import datetime
import json
import os
import re
import fnmatch
from PIL import Image
import numpy as np
import pycococreatortools

ROOT_DIR = '/local/patrick/datasets/jac_processed/train'
IMAGE_DIR = os.path.join(ROOT_DIR, "grasps_train2018")
ANNOTATION_DIR = os.path.join(ROOT_DIR, "annotations")

INFO = {
    "description": "Example Dataset",
    "url": "https://github.com/waspinator/pycococreator",
    "version": "0.1.0",
    "year": 2018,
    "contributor": "waspinator",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

CATEGORIES = [
    {
        'id': 1,
        'name': 'orient01',
        'supercategory': 'grasps',
    },
    {
        'id': 2,
        'name': 'orient02',
        'supercategory': 'grasps',
    },
    {
        'id': 3,
        'name': 'orient03',
        'supercategory': 'grasps',
    },
    {
        'id': 4,
        'name': 'orient04',
        'supercategory': 'grasps',
    },
    {
        'id': 5,
        'name': 'orient05',
        'supercategory': 'grasps',
    },
    {
        'id': 6,
        'name': 'orient06',
        'supercategory': 'grasps',
    },
    {
        'id': 7,
        'name': 'orient07',
        'supercategory': 'grasps',
    },
    {
        'id': 8,
        'name': 'orient08',
        'supercategory': 'grasps',
    },
    {
        'id': 9,
        'name': 'orient09',
        'supercategory': 'grasps',
    },
    {
        'id': 10,
        'name': 'orient10',
        'supercategory': 'grasps',
    },
    {
        'id': 11,
        'name': 'orient11',
        'supercategory': 'grasps',
    },
    {
        'id': 12,
        'name': 'orient12',
        'supercategory': 'grasps',
    },
    {
        'id': 13,
        'name': 'orient13',
        'supercategory': 'grasps',
    },
    {
        'id': 14,
        'name': 'orient14',
        'supercategory': 'grasps',
    },
    {
        'id': 15,
        'name': 'orient15',
        'supercategory': 'grasps',
    },
    {
        'id': 16,
        'name': 'orient16',
        'supercategory': 'grasps',
    },
    {
        'id': 17,
        'name': 'orient17',
        'supercategory': 'grasps',
    },
    {
        'id': 18,
        'name': 'orient18',
        'supercategory': 'grasps',
    },
    {
        'id': 19,
        'name': 'orient19',
        'supercategory': 'grasps',
    },
    {
        'id': 20,
        'name': 'orient20',
        'supercategory': 'grasps',
    },
    {
        'id': 21,
        'name': 'orient21',
        'supercategory': 'grasps',
    },
    {
        'id': 22,
        'name': 'orient22',
        'supercategory': 'grasps',
    },
    {
        'id': 23,
        'name': 'orient23',
        'supercategory': 'grasps',
    },
    {
        'id': 24,
        'name': 'orient24',
        'supercategory': 'grasps',
    },
    {
        'id': 25,
        'name': 'orient25',
        'supercategory': 'grasps',
    },
    {
        'id': 26,
        'name': 'orient26',
        'supercategory': 'grasps',
    },
    {
        'id': 27,
        'name': 'orient27',
        'supercategory': 'grasps',
    },
    {
        'id': 28,
        'name': 'orient28',
        'supercategory': 'grasps',
    },
    {
        'id': 29,
        'name': 'orient29',
        'supercategory': 'grasps',
    },
    {
        'id': 30,
        'name': 'orient30',
        'supercategory': 'grasps',
    },
    {
        'id': 31,
        'name': 'orient31',
        'supercategory': 'grasps',
    },
    {
        'id': 32,
        'name': 'orient32',
        'supercategory': 'grasps',
    },
    {
        'id': 33,
        'name': 'orient33',
        'supercategory': 'grasps',
    },
    {
        'id': 34,
        'name': 'orient34',
        'supercategory': 'grasps',
    },
    {
        'id': 35,
        'name': 'orient35',
        'supercategory': 'grasps',
    },
    {
        'id': 36,
        'name': 'orient36',
        'supercategory': 'grasps',
    },
]

def filter_for_jpeg(root, files):
    file_types = ['*.jpeg', '*.jpg']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    
    return files


def filter_for_png(root, files):
    file_types = ['*.png']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]

    return files

def filter_for_annotations(root, files, image_filename):
    file_types = ['*.png']
    file_types = r'|'.join([fnmatch.translate(x) for x in file_types])
    basename_no_extension = os.path.splitext(os.path.basename(image_filename))[0]
    file_name_prefix = basename_no_extension + '.*'
    files = [os.path.join(root, f) for f in files]
    files = [f for f in files if re.match(file_types, f)]
    files = [f for f in files if re.match(file_name_prefix, os.path.splitext(os.path.basename(f))[0])]

    return files

def main():

    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }

    image_id = 1
    segmentation_id = 1
    
    # filter for jpeg images
    for root, _, files in os.walk(IMAGE_DIR):
        path = root.split(os.sep)
        image_files = filter_for_png(root, files)

        # go through each image
        for image_filename in image_files:
            image = Image.open(image_filename)
            image_filename_w_folder = os.path.join(path[-2], path[-1], os.path.basename(image_filename))

            image_info = pycococreatortools.create_image_info(
                image_id, image_filename_w_folder, image.size)
            coco_output["images"].append(image_info)

            # filter for associated png annotations
            annotation_dir_w_folder = os.path.join(ANNOTATION_DIR, path[-2], path[-1])
            for root, _, files in os.walk(annotation_dir_w_folder):
                annotation_files = filter_for_annotations(root, files, image_filename)

                # go through each associated annotation
                for annotation_filename in annotation_files:
                    
                    print(annotation_filename)
                    class_id = [x['id'] for x in CATEGORIES if x['name'] in annotation_filename][0]

                    category_info = {'id': class_id, 'is_crowd': 'crowd' in image_filename}
                    binary_mask = np.asarray(Image.open(annotation_filename)
                        .convert('L')).astype(np.uint8)

                    annotation_filename_Parse = annotation_filename.split('_')
                    x = float(annotation_filename_Parse[-4])/100
                    y = float(annotation_filename_Parse[-3])/100
                    width = float(annotation_filename_Parse[-2])/100
                    height = float(annotation_filename_Parse[-1].split('.')[0])/100
                    bbox = np.asarray([x,y,width,height])
                    
                    annotation_info = pycococreatortools.create_annotation_info(
                        segmentation_id, image_id, category_info, binary_mask,
                        image.size, tolerance=2, bounding_box=bbox)

                    if annotation_info is not None:
                        coco_output["annotations"].append(annotation_info)

                    segmentation_id = segmentation_id + 1

            image_id = image_id + 1

    with open('{}/instances_grasps_train2018.json'.format(ROOT_DIR), 'w') as output_json_file:
        json.dump(coco_output, output_json_file)


if __name__ == "__main__":
    main()
