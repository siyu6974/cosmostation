import jinja2
import glob
from datetime import datetime


# [{ ob: 0004; date:xxx; imgs: [{tn: thumbnail, org: orginal, name: name}] }]
pcam = []
dirs = sorted(glob.glob('*/'))
# print(dirs)
for d in dirs:
    # print(d)
    ob, date = d.split('_')
    date = date.split('/')[0]
    lcam = sorted(glob.glob(f'{d}PCAML/*.png'))
    rcam = sorted(glob.glob(f'{d}PCAMR/*.png'))
    
    if len(lcam) != len(rcam):
        print(d)
        continue

    lrimgs = [''] * len(lcam) * 2
    for i in range(len(lrimgs)):
        if i % 2:
            lrimgs[i] = lcam[i//2]
        else:
            lrimgs[i] = rcam[i//2]
    
    imgs = []
    for i, org in enumerate(lrimgs):
        s = org.split('/')  # ['0001_2019-01-04', 'PCAMR', '000-20190104041502-PCAMR.png']
        tn = f"{s[0]}/{s[1]}/thumbnails/tn_{s[2].split('.')[0]}.jpg"
        imgs.append({
            'tn': tn,
            'org': org,
            'name': datetime.strptime(org.split('/')[-1].split('-')[1], '%Y%m%d%H%M%S').strftime('%m-%d %H:%M:%S')
        })

    pcam.append({
        'ob': ob,
        'date': date,
        'imgs': imgs
    })

env = jinja2.Environment(loader=jinja2.FileSystemLoader(
    searchpath='')
)
template = env.get_template('page-template.html')

output = template.render(pcam=pcam)
with open('index.html', 'w') as f:
    f.write(output)

