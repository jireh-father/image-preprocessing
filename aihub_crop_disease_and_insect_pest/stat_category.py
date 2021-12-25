import argparse

import json
import os
import glob


def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate metric of the '
                                                 'results saved in pkl format')
    parser.add_argument('--root_dir', type=str, default='E:\dataset\plant_disease\시설 작물 질병 진단 이미지\Training')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    label_files = glob.glob(os.path.join(args.root_dir, "*.json"))

    cates = {}
    for i, label_file in enumerate(label_files):
        if i % 10 == 0:
            print(i, len(label_files))
        label_data = json.load(open(label_file))
        disease = label_data["annotations"]["disease"]
        if disease not in cates:
            cates[disease] = 0
        cates[disease] += 1
    print(cates)
    print("done")


if __name__ == '__main__':
    main()