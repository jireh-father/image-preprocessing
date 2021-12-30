import argparse

import json
import os
import glob
import sys
from pycocotools import mask
from PIL import Image
from label_data import *


def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate metric of the ''results saved in pkl format')
    parser.add_argument('--root_dir', type=str, default='D:\dataset\seed\disease')
    parser.add_argument('--output_path', type=str, default='D:\dataset\seed\disease\\total_cate_stat.json')
    args = parser.parse_args()
    return args


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

    merged_categories = {}
    for cate_item in categories:
        cate_name = cate_item['name']
        if cate_name not in merged_categories:
            merged_categories[cate_name] = 0

    for i, dataset_type in enumerate(coco_json_dict):
        for phase in coco_json_dict[dataset_type]:
            coco_json_path = coco_json_dict[dataset_type][phase]
            print(coco_json_path)
            coco_data = json.load(open(coco_json_path, encoding='utf-8'))
            for anno_idx, anno in enumerate(coco_data['annotations']):
                # if i % 50 == 0:
                #     print(i, len(coco_json_dict), anno_idx, len(coco_data['annotations']))
                label_name = get_label_name_by_id(dataset_type, anno['category_id'])
                merged_categories[label_name] += 1
    os.makedirs(os.path.dirname(args.output_path), exist_ok=True)
    json.dump(merged_categories, open(args.output_path, "w+"))
    print(merged_categories)
    print("done")


if __name__ == '__main__':
    main()
