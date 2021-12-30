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
    # fruit_burn_disease, field_crop_disease, field_crop_pest, greenhouse_crop_disease
    parser.add_argument('--dataset_type', type=str, default='field_crop_pest')
    parser.add_argument('--phase', type=str, default='val')
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

    # fruit_burn_disease, field_crop_disease, field_crop_pest
    if dataset_type == "greenhouse_crop_disease":
        labels = greenhouse_crop_disease_labels
    elif dataset_type == "fruit_burn_disease":
        labels = fruit_burn_disease_labels
    elif dataset_type == "field_crop_disease":
        labels = field_crop_disease_labels
    elif dataset_type == "field_crop_pest":
        labels = field_crop_pest_labels
    else:
        raise Exception("unknown data type", dataset_type)
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


def get_anno(disease, crop, area, risk, dataset_type, ori_width, ori_height, image_path, label_file, bbox, im_id,
             anno_id, stat_category, resized_width=None, resized_height=None):
    if crop == 0 or area == 0 or (disease != 0 and risk == 0) or (disease == 0 and risk != 0):
        return None

    class_idx = get_label_name(dataset_type, disease, crop, area)
    if class_idx is None:
        return None

    if resized_width is None:
        try:
            resized_width, resized_height = Image.open(image_path).size
        except:
            image_path = os.path.splitext(os.path.splitext(label_file)[0])[0] + ".jpg"
            try:
                resized_width, resized_height = Image.open(image_path).size
            except:
                return None

    if resized_height == ori_height:
        x1 = bbox["xtl"]
        y1 = bbox["ytl"]
        x2 = bbox["xbr"]
        y2 = bbox["ybr"]

        bbox_w = x2 - x1
        bbox_h = y2 - y1
    else:
        if ori_width < 1 or ori_height < 1:
            return None
        short_size = min(ori_width, ori_height)
        ratio = min(resized_height, resized_width) / short_size

        x1 = bbox["xtl"] * ratio
        y1 = bbox["ytl"] * ratio
        x2 = bbox["xbr"] * ratio
        y2 = bbox["ybr"] * ratio

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

    return anno, resized_width, resized_height, image_path


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
    phase_folder = "Training" if phase == "train" else "Validation"
    new_root_dir = os.path.join(root_dir, dataset_folder, phase_folder)
    output_path = os.path.join(root_dir, dataset_folder, "{}_coco.json".format(phase))
    stat_output_path = os.path.join(root_dir, dataset_folder, "{}_cate_stat.json".format(phase))

    return new_root_dir, output_path, stat_output_path


def main():
    args = parse_args()
    root_dir, output_path, stat_output_path = get_path(args.root_dir, args.dataset_type, args.phase)
    label_files = glob.glob(os.path.join(root_dir, "*.json"))

    anno_id = 1
    im_id = 1
    annotations = []
    stat_category = {}
    images = []
    for i, label_file in enumerate(label_files):
        # if i < 76910:
        #     continue
        if i % 10 == 0:
            print(i, len(label_files))
        label_data = json.load(open(label_file))
        im_path = os.path.join(root_dir, label_data["description"]["image"])

        w = label_data["description"]["width"]
        h = label_data["description"]["height"]

        crop = label_data["annotations"]["crop"]
        area = label_data["annotations"]["area"]
        risk = label_data["annotations"]["risk"]

        has_anno = False
        if args.dataset_type == "field_crop_pest":
            objects = label_data["annotations"]["object"]
            resized_width, resized_height = None, None
            for obj in objects:
                if len(obj["points"]) > 1:
                    raise Exception("over 1 points")
                disease = obj["class"]
                tmp_anno = get_anno(disease, crop, area, risk, args.dataset_type, w, h, im_path, label_file,
                                    obj["points"][0], im_id, anno_id, stat_category, resized_width, resized_height)
                if tmp_anno is None:
                    continue
                tmp_anno, resized_width, resized_height, image_path = tmp_anno
                im_path = image_path
                annotations.append(tmp_anno)
                has_anno = True
        else:
            bboxes = label_data["annotations"]["points"]
            if len(bboxes) > 1:
                raise Exception("over one bbox")

            disease = label_data["annotations"]["disease"]

            tmp_anno = get_anno(disease, crop, area, risk, args.dataset_type, w, h, im_path, label_file,
                                bboxes[0], im_id, anno_id, stat_category)
            if tmp_anno is None:
                continue
            tmp_anno, resized_width, resized_height, image_path = tmp_anno
            annotations.append(tmp_anno)

            anno_id += 1
            has_anno = True

        if has_anno:
            image_info = {}
            image_info['width'] = resized_width
            image_info['height'] = resized_height
            image_info['id'] = im_id
            if not os.path.isfile(image_path):
                print("no", image_path)
                sys.exit()
            image_info['file_name'] = os.path.basename(image_path)
            images.append(image_info)
            im_id += 1

    coco = get_coco_template(args.dataset_type)
    coco["annotations"] = annotations
    coco["images"] = images
    json.dump(coco, open(output_path, "w+"))
    json.dump(stat_category, open(stat_output_path, "w+"))
    print(stat_category)
    print("done")


if __name__ == '__main__':
    main()
