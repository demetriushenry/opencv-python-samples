import os
import shutil
import sys
import time

import cv2


def copy_all_folder_content(path_dir, new_path_dir):
    if not os.path.exists(path_dir):
        print('path not found')
        exit(0)
    if not os.path.isdir(path_dir):
        print('path is not a directory')
        exit(0)

    dir_content = os.listdir(path_dir)

    if not dir_content:
        print('image path folder is empty')
        exit(0)

    for image in dir_content:
        new_name = _date_name(image)
        shutil.copy(
            os.path.join(path_dir, image),
            os.path.join(new_path_dir, new_name)
        )
        print('copying file: {}'.format(image), end='\r')


def cut_all_images(img_path_dir, geometry):
    if not os.path.exists(img_path_dir):
        print('path not found')
        exit(0)
    if not os.path.isdir(img_path_dir):
        print('path is not a directory')
        exit(0)
    if len(geometry) != 4:
        print('geometry not correct')
        exit(0)

    dir_content = os.listdir(img_path_dir)

    if not dir_content:
        print('image path folder is empty')
        exit(0)

    new_frame_list = []
    for image in dir_content:
        img_path = os.path.join(img_path_dir, image)
        frame = cv2.imread(img_path)
        x, y, w, h = geometry
        new_frame = frame[y:y+h, x:x+w]
        new_img_name = _date_name(image)
        new_frame_list.append((new_img_name, new_frame))

    print('all images cutted!')
    return new_frame_list


def _date_name(path_file):
    ts = time.time()
    filename, ext = os.path.splitext(path_file)
    return '{}_{}{}'.format(filename, ts, ext)


def cut_one_image(path, geometry):
    pass


def save_images(save_path, image_list):
    if not os.path.exists(save_path):
        print('path not found')
        exit(0)
    if not os.path.isdir(save_path):
        print('path is not a directory')
        exit(0)

    for img_name, frame in image_list:
        cv2.imwrite(os.path.join(save_path, img_name), frame)

    print('all images saved on:', save_path)


def main():
    img_path_dir = '/media/demetrius/LEANDROPAES/Frames/kr3/pos/'
    save_dir = '/media/demetrius/LEANDROPAES/AutoZoom/p1/'
    geometry = (1544, 679, 267, 309)
    img_list = cut_all_images(img_path_dir, geometry)
    save_images(save_dir, img_list)

    print('all process finished!')


if __name__ == "__main__":
    sys.exit(main())
