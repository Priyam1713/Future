"""Deterministic delivery conversion of approved artwork; no artistic edits."""
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parent
SPECS=[
 ('card-back-v1.png','art/deck/fate-back-v1/card-back.webp',768,1152,90),
 ('card-back-v1.png','art/deck/fate-back-v1/card-back-360.webp',360,540,88),
 ('nebula-v1.png','art/nebula-v1.webp',768,768,90),
 ('orb-poster-v2.png','art/orb-poster-v2.webp',960,960,92),
]

def main():
    for source,target,width,height,quality in SPECS:
        with Image.open(ROOT/'design/sources'/source) as original:
            image=original.copy()
            image.thumbnail((width,height),Image.Resampling.LANCZOS)
            path=ROOT/'web/public'/target
            path.parent.mkdir(parents=True,exist_ok=True)
            image.save(path,'WEBP',quality=quality,method=6)
            print(target,image.size,path.stat().st_size)

if __name__=='__main__':main()
