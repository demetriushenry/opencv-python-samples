import cv2

import dlib

img_full_path = 'images/tv_procel.jpg'
img_template_path = 'images/procel.jpg'

tracker = dlib.correlation_tracker()
win = dlib.image_window()

img = dlib.load_rgb_image(img_template_path)

rect = dlib.rectangle(10, 0, img.shape[1], img.shape[0])
print(rect)
tracker.start_track(img, rect)

win.clear_overlay()
win.set_image(img)
win.add_overlay(rect)
dlib.hit_enter_to_continue()

img = dlib.load_rgb_image(img_full_path)
tracker.update(img)

win.clear_overlay()
win.set_image(img)
print(tracker.get_position())
win.add_overlay(tracker.get_position())
dlib.hit_enter_to_continue()
