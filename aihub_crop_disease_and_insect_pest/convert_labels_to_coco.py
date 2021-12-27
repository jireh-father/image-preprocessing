import argparse

import json
import os
import glob
import sys
from pycocotools import mask
from PIL import Image
from label_data import *


def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate metric of the '
                                                 'results saved in pkl format')
    parser.add_argument('--root_dir', type=str, default='E:\dataset\plant_disease\시설 작물 질병 진단 이미지\Validation')
    parser.add_argument('--output_path', type=str, default='E:\dataset\plant_disease\시설 작물 질병 진단 이미지\\val_coco.json')
    parser.add_argument('--dataset_type', type=str, default='greenhouse_crop_disease')
    args = parser.parse_args()
    return args


def get_coco_template(dataset_type):
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

    if dataset_type == "greenhouse_crop_disease":
        labels = greenhouse_labels
    else:
        pass
    template["categories"] = [{'supercategory': k, 'id': i + 1, 'name': k} for i, k in
                              enumerate(labels)]
    print(template["categories"])
    return template


def make_anno(bbox, width, height):
    seg = []

    x2 = bbox[0] + bbox[2]
    y2 = bbox[1] + bbox[3]
    seg.append(bbox[0])
    seg.append(bbox[1])
    seg.append(x2)
    seg.append(bbox[1])
    seg.append(x2)
    seg.append(y2)
    seg.append(bbox[0])
    seg.append(y2)

    rles = mask.frPyObjects([seg], height, width)
    rle = mask.merge(rles)
    # bbox = mask.toBbox(rle)
    area = int(mask.area(rle))
    annotation = {
        "segmentation": [seg],
        "area": float(area),
        "bbox": bbox,
        "iscrowd": 0,
    }

    return annotation


def main():
    args = parse_args()

    label_files = glob.glob(os.path.join(args.root_dir, "*.json"))

    anno_id = 1
    im_id = 1
    annotations = []
    stat_category = {}
    images = []
    for i, label_file in enumerate(label_files):
        # if i < 172760:
        #     continue
        if i % 10 == 0:
            print(i, len(label_files))
        label_data = json.load(open(label_file))
        im_path = os.path.join(args.root_dir, label_data["description"]["image"])
        try:
            resized_width, resized_height = Image.open(im_path).size
        except:
            im_path = os.path.splitext(os.path.splitext(label_file)[0])[0] + ".jpg"
            resized_width, resized_height = Image.open(im_path).size
        w = label_data["description"]["width"]
        h = label_data["description"]["height"]

        bboxes = label_data["annotations"]["points"]
        if len(bboxes) > 1:
            raise Exception("over one bbox")

        disease = label_data["annotations"]["disease"]
        crop = label_data["annotations"]["crop"]
        area = label_data["annotations"]["area"]
        risk = label_data["annotations"]["risk"]
        if crop == 0 or area == 0 or (disease != 0 and risk == 0) or (disease == 0 and risk != 0):
            continue

        class_idx = get_label_name(args.dataset_type, disease, crop, area)
        if class_idx is None:
            continue

        if resized_height == h:
            x1 = bboxes[0]["xtl"]
            y1 = bboxes[0]["ytl"]
            x2 = bboxes[0]["xbr"]
            y2 = bboxes[0]["ybr"]

            bbox_w = x2 - x1
            bbox_h = y2 - y1

        else:

            short_size = min(w, h)
            ratio = min(resized_height, resized_width) / short_size

            x1 = bboxes[0]["xtl"] * ratio
            y1 = bboxes[0]["ytl"] * ratio
            x2 = bboxes[0]["xbr"] * ratio
            y2 = bboxes[0]["ybr"] * ratio

            bbox_w = x2 - x1
            bbox_h = y2 - y1
        bbox = [x1, y1, bbox_w, bbox_h]
        anno = make_anno(bbox, resized_width, resized_height)

        anno["image_id"] = im_id
        anno["id"] = anno_id
        anno["category_id"] = class_idx
        if class_idx not in stat_category:
            stat_category[class_idx] = 0
        stat_category[class_idx] += 1
        annotations.append(anno)

        image_info = {}
        image_info['width'] = resized_width
        image_info['height'] = resized_height
        image_info['id'] = im_id
        image_info['file_name'] = os.path.basename(im_path)
        images.append(image_info)
        anno_id += 1
        im_id += 1

    coco = get_coco_template(args.dataset_type)
    coco["annotations"] = annotations
    coco["images"] = images
    json.dump(coco, open(args.output_path, "w+"))
    json.dump(stat_category, open(args.output_path + "_category_stat.json", "w+"))
    print(stat_category)
    print("done")


if __name__ == '__main__':
    main()
