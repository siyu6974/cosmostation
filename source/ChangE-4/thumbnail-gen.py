from PIL import Image
import glob
import os 

def make_dir_if_n_exist(d):
    if not os.path.exists(d):
        os.makedirs(d)
    return d

SIZE = (512, 512)

# dirs = sorted(glob.glob('TCAM/*/'))
# print(dirs)

# for d in dirs:
#     imgs = glob.glob(f'{d}/*.png')
#     make_dir_if_n_exist(f"{d}/thumbnails")
#     try:
#         for p in imgs:
#             im = Image.open(p)
#             im.thumbnail(SIZE, Image.ANTIALIAS)
#             im.save(f"{d}/thumbnails/tn_{p.split('/')[-1].split('.')[0]}.jpg", 'JPEG', quality=70)
#     except:
#         print(p)


dirs = sorted(glob.glob('PCAM/*/'))
print(dirs)

for d in dirs:
    for cam in ['PCAML', 'PCAMR']:
        dd = f'{d}/{cam}'
        imgs = glob.glob(f'{dd}/*.png')
        make_dir_if_n_exist(f"{dd}/thumbnails")
        
        for p in imgs:
            im = Image.open(p)
            im.thumbnail(SIZE, Image.ANTIALIAS)
            im.save(f"{dd}/thumbnails/tn_{p.split('/')[-1].split('.')[0]}.jpg", 'JPEG', quality=70)

