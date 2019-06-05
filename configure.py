import os
from PIL import Image

print(
    'To proceed with the training setup you must have the main folder created'
    ' and inside the folders pos, neg and date.\n'
    'It is also necessary that in the pos and neg folders are already the '
    'images to be used for the training.\n'
)

print('Enter the parent path where the pos and neg folders are.\n')
parent_path = input()

# check if parent folder exists
folder_exists = os.path.exists(parent_path)

if not folder_exists:
    print('parent path not found.')
    exit(0)

# check if parent is a folder
parent_is_folder = os.path.isdir(parent_path)

if not parent_is_folder:
    print('parent path is not a folder.')
    exit(0)

# check if exists pos, neg and data folders
pos_path = parent_path + '/pos'
neg_path = parent_path + '/neg'
dat_path = parent_path + '/data'

if not os.path.exists(pos_path) and not os.path.exists(neg_path) and not \
        os.path.exists(dat_path):
    print('pos, neg or data folders do not exists')
    exit(0)

    if not os.path.isdir(pos_path) and not os.path.isdir(neg_path) and not \
            os.path.isdir(dat_path):
        print('pos, neg and data must be folder')
        exit(0)

# get object name
print('\nEnter the name for object to detect.\n')
obj_name = input()

# check pos and neg content
pos_content = os.listdir(pos_path)
neg_content = os.listdir(neg_path)

if not pos_content:
    print('pos folder is empty')
    exit(0)

if not neg_content:
    print('neg folder is empty')
    exit(0)

# remove empty files
for file in pos_content:
    file_path = pos_path + '/{}'.format(file)

    if not os.path.getsize(file_path):
        os.remove(file_path)

# update pos_content
pos_content = os.listdir(pos_path)

# create obj info and bg files
# obj info
file = open(parent_path + '/{}.info'.format(obj_name), 'w')

for f in pos_content:
    # get resolution of samples
    image_path = pos_path + '/{}'.format(f)
    image = Image.open(image_path)
    image_resolution = image.size
    image.close()

    file.write('pos/{} {}\n'.format(
        f,
        '1 0 0 {} {}'.format(image_resolution[0], image_resolution[1])
        )
    )

file.close()

# bg
file = open(parent_path + '/bg.txt', 'w')

for f in neg_content:
    file.write('neg/{}\n'.format(f))

file.close()

print('\nEnter the width for object to detect.\n')
obj_w = input()

print('\nEnter the height for object to detect.\n')
obj_h = input()

# create samples tools from opencv
cmd = 'opencv_createsamples -info {}.info -num {} -w {} -h {} -vec {}.vec'.format(
    obj_name,
    len(pos_content),
    obj_w,
    obj_h,
    obj_name
)

# run command
os.system(cmd)

# check if vec file has been created
if not os.path.exists(parent_path + '/{}.vec'.format(obj_name)):
    print('somethint went wrong')
    exit(0)

# create traincascade xml
print('\nEnter the number of samples for training.\n')
number_samples = input()

print('\nEnter the number of stages for training.\n')
number_stages = input()

print('\nEnter the train type for training - HAAR, LBP or HOG.\n')
train_type = input()

cmd = 'opencv_traincascade -data data -vec {}.vec -bg bg.txt -numPos {} -numNeg {} -numStages {}' \
      ' -numThreads 4 -w {} -h {} -featureType {}'.format(
          obj_name,
          number_samples,
          number_samples,
          number_stages,
          obj_w,
          obj_h,
          train_type
      )

# if train_type == 'LBP':
#     cmd += ' -weightTrimRate 0.95'

# run command
os.system(cmd)

# check if traincascade xml exists
if not os.path.exists(parent_path + '/data/cascade.xml'):
    print('something went wrong with xml file')

# finish
print('\nFinishing process...\n')
