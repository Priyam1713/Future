"""Draw five original metadata-free geometric targets for the pinned blind study."""

import math
import struct
import zlib
from pathlib import Path

from PIL import Image, ImageDraw


def chunk(kind, body):
    return struct.pack('>I',len(body))+kind+body+struct.pack('>I',zlib.crc32(kind+body))


def build(root):
    root.mkdir(parents=True,exist_ok=True)
    size = 192
    for i, (paper, ink, accent) in enumerate([
        ('#192e37','#d6b989','#4c948d'),('#302138','#df9d84','#945278'),
        ('#18263c','#9eb7d5','#a36d4c'),('#332822','#e0ca93','#a36954'),
        ('#233025','#a9c79b','#9877a8'),
    ],1):
        img = Image.new('RGB',(size,size),paper)
        draw = ImageDraw.Draw(img)
        for margin in (7,14,19):
            draw.rectangle((margin,margin,size-margin-1,size-margin-1),outline=accent,width=1)
        if i == 1:
            for x in (40,75,110,145):
                draw.rounded_rectangle((x,38,x+19,154),radius=9,outline=ink,width=3)
        elif i == 2:
            for d in (32,49,65):
                draw.ellipse((96-d,96-d,96+d,96+d),outline=ink,width=3)
            draw.ellipse((77,77,115,115),fill=accent)
        elif i == 3:
            for y in (38,68,98,128):
                draw.line([(x,y+12*math.sin(x/14)) for x in range(31,162)],fill=ink,width=4)
        elif i == 4:
            for n in range(4):
                top=30+n*26
                draw.polygon([(96,top),(149-n*11,145),(43+n*11,145)],outline=ink,width=3)
        else:
            for y in (52,96,140):
                for x in (52,96,140):
                    d=12 if x==y else 9
                    draw.polygon([(x,y-d),(x+d,y),(x,y+d),(x-d,y)],fill=ink if x==y else accent)
        raw = img.tobytes()
        pixels = b''.join(b'\x00'+raw[y*size*3:(y+1)*size*3] for y in range(size))
        header = struct.pack('>IIBBBBB',size,size,8,2,0,0,0)
        (root / f'plate-{i}.png').write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR',header) +
                                             chunk(b'IDAT',zlib.compress(pixels)) + chunk(b'IEND',b''))


if __name__ == '__main__':
    build(Path(__file__).parent/'data/sealed-targets-v1')
