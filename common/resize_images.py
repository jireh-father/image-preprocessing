import glob
import argparse
import os
import shutil
from multiprocessing import Pool
import tqdm
import traceback
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
from PIL import Image, ExifTags


def recursive_files(image_dir, image_files):
    files = glob.glob(os.path.join(image_dir, "*"))
    for file in files:
        if os.path.isdir(file):
            recursive_files(file, image_files)
        else:
            image_files.append(file)


def resize(feed):
    file = feed[0]
    limit = feed[1]
    orientation = feed[2]
    output_dir = feed[3]
    only_save_modified = feed[4]
    remove_no_image_file = feed[5]
    print(file)

    try:
        im = Image.open(file)
    except:
        if remove_no_image_file:
            os.unlink(file)
        traceback.print_exc()
        return

    try:
        is_rotate = False
        exif = im._getexif()
        if exif is not None and orientation in exif:
            if exif[orientation] == 3:
                im = im.rotate(180, expand=True)
                is_rotate = True
            elif exif[orientation] == 6:
                im = im.rotate(270, expand=True)
                is_rotate = True
            elif exif[orientation] == 8:
                im = im.rotate(90, expand=True)
                is_rotate = True
    except (AttributeError, KeyError, IndexError):
        traceback.print_exc()
        is_rotate = False

    try:
        was_rgb = True
        if im.mode != "RGB":
            im = im.convert("RGB")
            was_rgb = False
        if im.format != "JPEG":
            was_rgb = False
    except:
        traceback.print_exc()
        was_rgb = True

    try:
        w, h = im.size
        is_big = False
        if w > limit and h > limit:
            is_big = True
            shorter_size = min(w, h)
            ratio = float(limit) / shorter_size
            im = im.resize((round(w * ratio), round(h * ratio)), Image.ANTIALIAS)
    except:
        traceback.print_exc()
        is_big = False

    if not was_rgb or is_big or is_rotate:
        if output_dir is None:
            if im.format != "JPEG":
                os.unlink(file)
                im.save(os.path.splitext(file)[0] + ".jpg")
            else:
                im.save(file)
        else:
            class_dir_name = os.path.basename(os.path.dirname(file))
            output_dir = os.path.join(output_dir, class_dir_name)
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.basename(file)
            if im.format != "JPEG":
                im.save(os.path.join(output_dir, os.path.splitext(output_file)[0] + ".jpg"))
            else:
                im.save(os.path.join(output_dir, output_file))
    elif output_dir is not None and not only_save_modified:
        class_dir_name = os.path.basename(os.path.dirname(file))
        output_dir = os.path.join(output_dir, class_dir_name)
        os.makedirs(output_dir, exist_ok=True)
        shutil.copy(file, output_dir)


def main(args):
    image_dirs = args.img_dirs.split(",")

    image_files = []
    for image_dir in image_dirs:
        recursive_files(image_dir, image_files)

    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break

    print("image files", len(image_files))

    with Pool(args.num_processes) as pool:
        print("start multi processing")
        tqdm.tqdm(pool.map(resize, zip(image_files, [args.max_shortest_edge_size] * len(image_files),
                                       [orientation] * len(image_files), [args.output_dir] * len(image_files),
                                       [args.only_save_modified] * len(image_files),[args.remove_no_image_file] * len(image_files))), total=len(image_files))

    print("done")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--img_dirs', type=str, default='E:\dataset\\food\상품 이미지')
    parser.add_argument('--output_dir', type=str, default=None)
    parser.add_argument('--max_shortest_edge_size', type=int, default=700)
    parser.add_argument('--num_processes', type=int, default=4)
    parser.add_argument('--remove_no_image_file', action="store_true", default=False)
    parser.add_argument('--only_save_modified', action="store_true", default=False)

    main(parser.parse_args())
