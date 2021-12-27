import argparse

import json
import os
import glob
import shutil
from label_data import *


def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate metric of the '
                                                 'results saved in pkl format')
    parser.add_argument('--root_dir', type=str, default='E:\dataset\plant_disease\시설 작물 질병 진단 이미지\Validation')
    parser.add_argument('--output_path', type=str, default='E:\dataset\plant_disease\시설 작물 질병 진단 이미지\\stats_clean_val.json')
    parser.add_argument('--output_dir', type=str, default='E:\dataset\plant_disease\시설 작물 질병 진단 이미지\\stats_images_clean_val')
    # parser.add_argument('--output_dir', type=str, default=None)

    parser.add_argument('--dataset_type', type=str, default='greenhouse_crop_disease')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    label_files = glob.glob(os.path.join(args.root_dir, "*.json"))

    if args.dataset_type == "greenhouse_crop_disease":
        diseases = greenhouse_crop_disease
        crops = greenhouse_crops
        areas = greenhouse_areas
    else:
        diseases = greenhouse_crop_disease
        crops = greenhouse_crops
        areas = greenhouse_areas

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
    stats = {}
    for i, label_file in enumerate(label_files):
        # if i < 172760:
        #     continue
        if i % 10 == 0:
            print(i, len(label_files))
        label_data = json.load(open(label_file))

        disease = label_data["annotations"]["disease"]
        crop = label_data["annotations"]["crop"]
        area = label_data["annotations"]["area"]
        risk = str(label_data["annotations"]["risk"])

        if crop == 0 or area == 0 or (disease != 0 and risk == 0) or (disease == 0 and risk != 0):
            continue

        class_idx = get_label_name(args.dataset_type, disease, crop, area)
        if class_idx is None:
            continue

        disease_name = diseases[disease]
        crop_name = crops[crop]
        area_name = areas[area]

        if crop_name not in stats:
            stats[crop_name] = {}

        if area_name not in stats[crop_name]:
            stats[crop_name][area_name] = {}

        if disease_name not in stats[crop_name][area_name]:
            stats[crop_name][area_name][disease_name] = {}

        if risk not in stats[crop_name][area_name][disease_name]:
            stats[crop_name][area_name][disease_name][risk] = 0
        stats[crop_name][area_name][disease_name][risk] += 1
        if args.output_dir is not None:
            copy_dir = os.path.join(args.output_dir, crop_name, area_name, disease_name, risk)

            image_path = os.path.join(args.root_dir, label_data["description"]["image"])
            if not os.path.isfile(image_path):
                image_path = os.path.splitext(os.path.splitext(label_file)[0])[0] + ".jpg"
            os.makedirs(copy_dir, exist_ok=True)
            shutil.copy(image_path, copy_dir)
    json.dump(stats, open(args.output_path, "w+"))
    print(stats)
    print("done")


if __name__ == '__main__':
    main()
