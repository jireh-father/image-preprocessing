import argparse

import json
import os
import glob
import sys
from pycocotools import mask
from PIL import Image


def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate metric of the '
                                                 'results saved in pkl format')
    parser.add_argument('--root_dir', type=str, default='E:\dataset\plant_disease\시설 작물 질병 진단 이미지\Training')
    parser.add_argument('--output_path', type=str, default='E:\dataset\plant_disease\시설 작물 질병 진단 이미지\\train_coco.json')
    args = parser.parse_args()
    return args


greenhouse_crop_disease = [
    '정상',
    '가지잎곰팡이병',
    '가지흰가루병',
    '고추마일드모틀바이러스',
    '고추점무늬병',
    '단호박점무늬병',
    '단호박흰가루병',
    '딸기잿빛곰팡이병',
    '딸기흰가루병',
    '상추균핵병',
    '상추노균병',
    '수박탄저병',
    '수박흰가루병',
    '애호박점무늬병',
    '오이녹반모자이크바이러스',
    '오이모자이크바이러스',
    '참외노균병',
    '참외흰가루병',
    '토마토잎곰팡이병',
    '토마토황화잎말이바이러스',
    '포도노균병',
]


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
        template["categories"] = [{'supercategory': v, 'id': i + 1, 'name': v} for i, v in
                                  enumerate(greenhouse_crop_disease)]
    else:
        pass
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
    images = []
    for i, label_file in enumerate(label_files):
        if i % 10 == 0:
            print(i, len(label_files))
        label_data = json.load(open(label_file))
        im_path = os.path.join(args.root_dir, label_data["description"]["image"])
        resized_width, resized_height = Image.open(im_path).size
        w = label_data["description"]["width"]
        h = label_data["description"]["height"]

        bboxes = label_data["annotations"]["points"]
        if len(bboxes) > 1:
            raise Exception("over one bbox")

        disease = label_data["annotations"]["disease"]

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
        anno["category_id"] = disease + 1
        annotations.append(anno)

        image_info = {}
        image_info['width'] = resized_width
        image_info['height'] = resized_height
        image_info['id'] = im_id
        image_info['file_name'] = os.path.basename(im_path)
        images.append(image_info)
        anno_id += 1
        im_id += 1

    coco = get_coco_template()
    coco["annotations"] = annotations
    coco["images"] = images
    json.dump(coco, open(args.output_path, "w+"))

    print("done")


if __name__ == '__main__':
    main()
