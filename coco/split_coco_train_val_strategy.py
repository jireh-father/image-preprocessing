import argparse

import random
import json
import os
import shutil
import copy


def parse_args():
    parser = argparse.ArgumentParser(description='Evaluate metric of the '
                                                 'results saved in pkl format')
    parser.add_argument('--annotation_file', type=str, default='D:\dataset\seed\disease/total_coco.json')
    parser.add_argument('--output_dir', type=str, default='D:\dataset\seed\disease/split')
    parser.add_argument('--image_dir', type=str, default='D:\dataset\seed\disease/total_images')
    parser.add_argument('--train_ratio', type=float, default=0.9)
    parser.add_argument('--random_seed', type=int, default=1)
    parser.add_argument('--check_image_size', action="store_true", default=False)
    args = parser.parse_args()
    return args


def add_anno_and_image(tmp_annos, im_id_to_image_dict, images, anno_id, annos, image_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for tmp_anno in tmp_annos:
        im_id = tmp_anno['image_id']
        im_item = copy.deepcopy(im_id_to_image_dict[im_id])
        if im_id in images:
            new_im_id = images[im_id]['id']
        else:
            new_im_id = len(images) + 1
            im_item['id'] = new_im_id
            images[im_id] = im_item
            shutil.copy(os.path.join(image_dir, im_item['file_name']), output_dir)

        tmp_anno['image_id'] = new_im_id
        tmp_anno['id'] = anno_id
        anno_id += 1
        annos.append(tmp_anno)
    return anno_id


def main():
    args = parse_args()

    random.seed(args.random_seed)

    coco_data = json.load(open(args.annotation_file))

    cate_id_to_annos_dict = {}
    im_id_to_image_dict = {}
    for anno_item in coco_data["annotations"]:
        if anno_item['category_id'] not in cate_id_to_annos_dict:
            cate_id_to_annos_dict[anno_item['category_id']] = []
        cate_id_to_annos_dict[anno_item['category_id']].append(anno_item)
    for image_item in coco_data["images"]:
        im_id_to_image_dict[image_item['id']] = image_item

    random.seed(args.random_seed)
    os.makedirs(args.output_dir, exist_ok=True)

    train_annos = []
    val_annos = []
    train_images = {}
    val_images = {}
    train_anno_id = 1
    val_anno_id = 1
    for cate_id in cate_id_to_annos_dict:
        print(cate_id, len(cate_id_to_annos_dict))
        anno_items = cate_id_to_annos_dict[cate_id]
        random.shuffle(anno_items)
        train_cnt = round(args.train_ratio * len(anno_items))
        tmp_train_annos = anno_items[:train_cnt]
        tmp_val_annos = anno_items[train_cnt:]

        train_anno_id = add_anno_and_image(tmp_train_annos, im_id_to_image_dict, train_images, train_anno_id,
                                           train_annos, args.image_dir, os.path.join(args.output_dir, "train_images"))

        val_anno_id = add_anno_and_image(tmp_val_annos, im_id_to_image_dict, val_images, val_anno_id, val_annos,
                                         args.image_dir, os.path.join(args.output_dir, "val_images"))

    coco_data['images'] = list(train_images.values())
    coco_data['annotations'] = train_annos
    json.dump(coco_data, open(os.path.join(args.output_dir, "train.json"), "w+"))

    coco_data['images'] = list(val_images.values())
    coco_data['annotations'] = val_annos
    json.dump(coco_data, open(os.path.join(args.output_dir, "val.json"), "w+"))

    print("done")


if __name__ == '__main__':
    main()
