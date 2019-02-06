import sys

import cv2 as cv


def get_sub_images_6(original_img_path: str):
    img = cv.imread(original_img_path)

    shape = img.shape
    rows = shape[0]
    columns = shape[1]

    num_col = 3
    num_row = 2
    roi_list = []
    roi_width = columns // 3
    roi_height = rows // 2

    for i in range(num_row):
        for j in range(num_col):
            x = j * roi_width
            y = i * roi_height
            w = roi_width
            h = roi_height
            roi_list.append((x, y, w, h))

    list_coords = [roi for roi in roi_list]

    list_imgs = [img[c[1]:c[1]+c[3], c[0]:c[0]+c[2]] for c in list_coords]

    return list_imgs


def main():
    imgs = get_sub_images_6('resized_image.jpg')
    print(len(imgs))

    for id, img in enumerate(imgs):
        cv.imshow('{}'.format(id), img)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == "__main__":
    sys.exit(main())
