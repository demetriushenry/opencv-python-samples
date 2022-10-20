import os
from zxing import BarCodeReader


reader = BarCodeReader()

rootpath = '/home/demetriusv/Documents/Missing Label Mobile/codigos'

for entry in os.listdir(rootpath):
    if os.path.isfile(os.path.join(rootpath, entry)):
        barcode = reader.decode(os.path.join(rootpath, entry))
        print(f'{entry} - {barcode}')

