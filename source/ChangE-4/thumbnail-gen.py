from PIL import Image
import glob
import os 

def make_dir_if_n_exist(d):
    if not os.path.exists(d):
        os.makedirs(d)
    return d

SIZE = (256, 256)

dirs = sorted(glob.glob('/Volumes/PowerBar/exp/TCAM/*'))
print(dirs)

for d in dirs:
    imgs = glob.glob(f'{d}/*.png')
    make_dir_if_n_exist(f"{d}/thumbnails")
    try:
        for p in imgs:
            im = Image.open(p)
            im.thumbnail(SIZE, Image.ANTIALIAS)
            im.save(f"{d}/thumbnails/tn_{p.split('/')[-1].split('.')[0]}.jpg", 'JPEG', quality=80)
    except:
        print(p)

