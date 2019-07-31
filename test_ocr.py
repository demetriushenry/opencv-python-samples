"""Test ocr script."""
import cv2

import pytesseract

image = cv2.imread('/home/demetrius/Pictures/procel_tag.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

tessdata_dir = '"/home/demetrius/Comp/tesseract"'
tessdata_config = f'--tessdata-dir {tessdata_dir} --oem 1 --psm 3'
text = pytesseract.image_to_string(gray, lang='por', config=tessdata_config)
file = open('/home/demetrius/Documents/saida.txt', 'w+')
file.write(text.strip('\n'))
file.close()

cv2.imshow('Original', image)
cv2.imshow('Original gray', gray)
cv2.waitKey(0)
