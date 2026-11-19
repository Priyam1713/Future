"""Deterministic delivery conversion of approved artwork; no artistic edits."""
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parent
SPECS=[
 ('card-back-v1.png','art/deck/fate-back-v1/card-back.webp',768,1152,90),
 ('card-back-v1.png','art/deck/fate-back-v1/card-back-360.webp',360,540,88),
 ('nebula-v1.png','art/nebula-v1.webp',768,768,90),
 ('orb-poster-v2.png','art/orb-poster-v2.webp',960,960,92),
 ('number-dial-v1.png','art/number-dial-v1.webp',960,960,90),
 ('number-dial-v1.png','art/number-dial-480.webp',480,480,88),
 ('gallery-hall-v1.png','art/gallery-hall-v1.webp',1536,1024,88),
 ('gallery-hall-v1.png','art/gallery-hall-768.webp',768,512,85),
 ('codex-cover-v1.png','art/codex-cover-v1.webp',768,1152,90),
 ('codex-cover-v1.png','art/codex-cover-400.webp',400,600,88),
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
