import jinja2
import glob
from datetime import datetime


# [{ ob: 0004; date:xxx; imgs: [{tn: thumbnail, org: orginal, name: name}] }]
tcam = []
dirs = sorted(glob.glob('*/'))
print(dirs)
for d in dirs:
    print(d)
    ob, date = d.split('_')
    date = date.split('/')[0]
    orgs = sorted(glob.glob(f'{d}*.png'))
    tns = sorted(glob.glob(f'{d}thumbnails/*.jpg'))
    imgs = []
    print(len(orgs))

    for i, org in enumerate(orgs):
        imgs.append({
            'tn': tns[i],
            'org': org,
            'name': datetime.strptime(org.split('/')[-1].split('-')[1], '%Y%m%d%H%M%S').strftime('%m-%d %H:%M:%S')
        })

    tcam.append({
        'ob': ob,
        'date': date,
        'imgs': imgs
    })

env = jinja2.Environment(loader=jinja2.FileSystemLoader(
    searchpath='')
)
template = env.get_template('page-template.html')

# display_dictionary = {}
# code that fills in display_dictionary with the values to send to the template

output = template.render(tcam=tcam)
with open('index.html', 'w') as f:
    f.write(output)

