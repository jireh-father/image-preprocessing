import argparse

import json
import os
import glob
import sys
from pycocotools import mask
from PIL import Image
from label_data import *
import shutil
import random


def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate metric of the ''results saved in pkl format')
    parser.add_argument('--root_dir', type=str, default='D:\dataset\seed\disease')
    # fruit_burn_disease, field_crop_disease, field_crop_pest, greenhouse_crop_disease
    parser.add_argument('--output_path', type=str, default='D:\dataset\seed\disease\\total_coco.json')
    parser.add_argument('--output_image_dir', type=str, default='D:\dataset\seed\disease\\total_images')
    parser.add_argument('--max_normal_cate', type=int, default=2700)
    parser.add_argument('--seed', type=int, default=1)

    args = parser.parse_args()
    return args


def get_coco_template():
    template = {
        "info": {'year': 2021, 'version': '1.0',
                 'description': 'VIA project exported to COCO format using VGG Image Annotator (http://www.robots.ox.ac.uk/~vgg/software/via/)',
                 'contributor': '', 'url': 'http://www.robots.ox.ac.uk/~vgg/software/via/',
                 'date_created': 'Wed May 05 2021 14:18:44 GMT+0900 (한국 표준시)'}
        ,
        "licenses":
            [{'id': 0, 'name': 'Unknown License', 'url': ''}],
        "images": [
            # {
            #     "id": 1,
            #     "width": 400,
            #     "height": 400,
            #     'file_name': '1.jpg'
            # }
        ],
        "annotations": [
            # {
            #     "segmentation": [[2, 442, 996, 442, 996, 597, 2, 597]],
            #     "area": 11111,
            #     "bbox": [2, 4, 2, 4],
            #     "iscrowd": 0,
            #     "id": 21,
            #     "image_id": 4,
            #     "category_id": 1
            # }
        ],
        "categories": [{'supercategory': 'foot', 'id': 1, 'name': 'foot'},
                       {'supercategory': 'triangle', 'id': 2, 'name': 'left_triangle'},
                       {'supercategory': 'triangle', 'id': 3, 'name': 'right_triangle'}],
    }

    return template


def get_dataset_path(root_dir, dataset_type, phase):
    if dataset_type == "greenhouse_crop_disease":
        dataset_folder = "시설 작물 질병 진단 이미지"
    elif dataset_type == "fruit_burn_disease":
        dataset_folder = "과수화상병 촬영 이미지"
    elif dataset_type == "field_crop_disease":
        dataset_folder = "노지 작물 질병 진단 이미지"
    elif dataset_type == "field_crop_pest":
        dataset_folder = "노지 작물 해충 진단 이미지"
    else:
        raise Exception("unknown data type", dataset_type)
    phase_folder = "Training" if phase == "train" else "Validation"
    new_root_dir = os.path.join(root_dir, dataset_folder, phase_folder)

    return new_root_dir


def get_path(root_dir, dataset_type, phase):
    if dataset_type == "greenhouse_crop_disease":
        dataset_folder = "시설 작물 질병 진단 이미지"
    elif dataset_type == "fruit_burn_disease":
        dataset_folder = "과수화상병 촬영 이미지"
    elif dataset_type == "field_crop_disease":
        dataset_folder = "노지 작물 질병 진단 이미지"
    elif dataset_type == "field_crop_pest":
        dataset_folder = "노지 작물 해충 진단 이미지"
    else:
        raise Exception("unknown data type", dataset_type)
    output_path = os.path.join(root_dir, dataset_folder, "{}_coco.json".format(phase))

    return output_path


DATASET_TYPE = ['fruit_burn_disease', 'field_crop_disease', 'field_crop_pest', 'greenhouse_crop_disease']


def main():
    args = parse_args()

    coco_json_dict = {}
    for dataset_type in DATASET_TYPE:
        coco_json_dict[dataset_type] = {
            'train': get_path(args.root_dir, dataset_type, 'train'),
            'val': get_path(args.root_dir, dataset_type, 'val'),
        }

    categories = []

    for dataset_type in coco_json_dict:
        # for phase in coco_json_dict[dataset_type]:
        coco_json_path = coco_json_dict[dataset_type]['val']
        coco_data = json.load(open(coco_json_path, encoding='utf-8'))
        categories += coco_data['categories']

    merged_category_dict = {}
    for cate_item in categories:
        cate_name = cate_item['name']
        if cate_name not in merged_category_dict:
            merged_category_dict[cate_name] = {}
    category_list = list(merged_category_dict.keys())
    category_list.sort()

    image_dict = {}

    for i, dataset_type in enumerate(coco_json_dict):
        image_dict[dataset_type] = {}
        for phase in coco_json_dict[dataset_type]:
            coco_json_path = coco_json_dict[dataset_type][phase]
            print(coco_json_path)
            coco_data = json.load(open(coco_json_path, encoding='utf-8'))
            image_dict[dataset_type][phase] = {}
            for j, image_item in enumerate(coco_data['images']):
                image_dict[dataset_type][phase][image_item['id']] = image_item
            for anno_idx, anno in enumerate(coco_data['annotations']):
                # if i % 50 == 0:
                #     print(i, len(coco_json_dict), anno_idx, len(coco_data['annotations']))
                label_name = get_label_name_by_id(dataset_type, anno['category_id'])
                im_id = anno['image_id']
                key = "{}-{}-{}".format(dataset_type, phase, im_id)
                if key not in merged_category_dict[label_name]:
                    merged_category_dict[label_name][key] = []
                merged_category_dict[label_name][key].append(anno)
    os.makedirs(args.output_image_dir, exist_ok=True)
    random.seed(args.seed)
    coco_cates = []
    images = []
    annotations = []
    anno_id = 1
    for i, cate_name in enumerate(category_list):
        print(i, len(category_list))
        cate_id = i + 1
        coco_cates.append(
            {'supercategory': cate_name, 'id': cate_id, 'name': cate_name}
        )
        key_list = list(merged_category_dict[cate_name].keys())
        if len(merged_category_dict[cate_name]) > args.max_normal_cate:
            random.shuffle(key_list)
            key_list = key_list[:args.max_normal_cate]
        for j, key in enumerate(key_list):
            if j % 50 == 0:
                print(i, len(category_list), j, len(key_list))
            dname, phase, im_id = key.split("-")
            im_id = int(im_id)
            image_item = image_dict[dname][phase][im_id]
            new_im_id = len(images) + 1
            image_item['id'] = new_im_id

            dataset_path = get_dataset_path(args.root_dir, dname, phase)
            image_full_path = os.path.join(dataset_path, image_item['file_name'])
            shutil.copy(image_full_path, args.output_image_dir)
            images.append(image_item)
            for anno_item in merged_category_dict[cate_name][key]:
                anno_item['image_id'] = new_im_id
                anno_item['id'] = anno_id
                anno_id += 1
                anno_item['category_id'] = cate_id
                annotations.append(anno_item)
    coco_dataset = get_coco_template()
    coco_dataset['categories'] = coco_cates
    coco_dataset['annotations'] = annotations
    coco_dataset['images'] = images

    os.makedirs(os.path.dirname(args.output_path), exist_ok=True)
    json.dump(coco_dataset, open(args.output_path, "w+"))
    print("done")


if __name__ == '__main__':
    main()
