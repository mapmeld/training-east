# image-slicer.py
from random import randint
from lxml import etree

# pip3 install Pillow
from PIL import Image

scans = ['Or 8349_0020', 'Delhi Arabic 1901_0155', 'Add MS 7474_0043']
ns = '{http://schema.primaresearch.org/PAGE/gts/pagecontent/2018-07-15}'

for scan in scans:
    im = Image.open(scan + '.tif')
    width, height = im.size
    # print(str(width) + 'x' + str(height))

    # generate random blocks
    for block in range(0, 120):
        blockx0 = randint(0, width - 100)
        blockx1 = randint(blockx0 + 100, min(width, blockx0 + int(width / 4)))
        blocky0 = randint(0, height - 100)
        blocky1 = randint(blocky0 + 100, min(height, blocky0 + int(height / 4)))

        rectangles = []
        tree = etree.parse(scan + '.xml')
        root = tree.getroot()
        for line in root.iter(ns + 'TextLine'):
            coords = line.find(ns + 'Coords')
            points = coords.attrib['points'].split(' ')

            xmin = width
            xmax = 0
            ymin = height
            ymax = 0
            for point in points:
                x, y = point.split(',')
                x = int(x)
                y = int(y)
                if x > blockx0 and x < blockx1 and y > blocky0 and y < blocky1:
                    xmin = min(xmin, int(x))
                    xmax = max(xmax, int(x))
                    ymin = min(ymin, int(y))
                    ymax = max(ymax, int(y))
            if (xmax > 0 and xmin != xmax and ymin != ymax):
                rectangles.append([str(xmin), str(ymin), str(xmax), str(ymax)])
        if (len(rectangles) > 0):
            # useful image
            print('block' + str(block))
            cropped = im.crop((blockx0, blocky0, blockx1, blocky1))
            cropname = scan.replace(' ', '') + '_' + str(block)
            cropped.save(cropname + '.png', 'PNG')

            sample = open(cropname + '.txt', 'w')
            for rectangle in rectangles:
                # use ### for non Latin text?
                sample.write(','.join([
                    rectangle[0], rectangle[1],
                    rectangle[2], rectangle[1],
                    rectangle[2], rectangle[3],
                    rectangle[0], rectangle[3]
                ]) + ",###\n")
