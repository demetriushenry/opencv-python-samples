import concurrent.futures
import glob
import os
import time

import pytesseract

os.environ['OMP_THREAD_LIMIT'] = '1'


def ocr(path):
    tess_config = ("-l eng --oem 1 --psm 6")
    text = pytesseract.image_to_string(path, config=tess_config)
    text = text.replace('\t', '').replace('\n', ' ')
    return text


def main():
    path = "/home/demetrius/Pictures/roi"
    if os.path.isdir(path) == 1:
        # out_dir = "ocr_results//"
        # if not os.path.exists(out_dir):
        #     os.makedirs(out_dir)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            image_list = glob.glob(path + "/*.jpg")
            for img_path, out_file in zip(image_list, executor.map(ocr, image_list)):
                print(img_path.split("/")[-1], ',', out_file, ', processed')


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(end - start)
