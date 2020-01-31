import jinja2
import glob
from datetime import datetime


# [{ ob: 0004; date:xxx; imgs: [{tn: thumbnail, org: orginal, name: name}] }]
tcam = []
dirs = sorted(glob.glob('TCAM/*'))
print(dirs)
for d in dirs:
    ob, date = d.split('/')[-1].split('_')
    orgs = sorted(glob.glob(f'{d}/*.png'))
    tns = sorted(glob.glob(f'{d}/thumbnails/*.jpg'))
    imgs = []
    print(len(orgs))
    print(d)

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
print(tcam)

env = jinja2.Environment(loader=jinja2.FileSystemLoader(
    searchpath='')
)
template = env.get_template('page-template.html')

# display_dictionary = {}
# code that fills in display_dictionary with the values to send to the template

output = template.render(tcam=tcam)
with open('index.html', 'w') as f:
    f.write(output)

