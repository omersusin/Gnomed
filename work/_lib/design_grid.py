import sys, io, cairosvg
from pathlib import Path
from PIL import Image, ImageDraw
work=Path(sys.argv[1]); out=sys.argv[2]; slugs=sys.argv[3].split(','); alts=sys.argv[4].split(',') if len(sys.argv)>4 else ['faithful','disc','rimmed','symbol']
S=150; cols=1+len(alts)
W=Image.new('RGBA',(cols*S*2,len(slugs)*(S+14)),(255,255,255,255)); d=ImageDraw.Draw(W)
for r,s in enumerate(slugs):
    y=r*(S+14)
    for half,bg in enumerate([(246,245,244,255),(36,31,49,255)]):
        x0=half*cols*S
        d.rectangle([x0,y,x0+cols*S,y+S+13],fill=bg)
        src=Image.open(work/s/'source.png').convert('RGBA').resize((S-20,S-20))
        W.alpha_composite(src,(x0+10,y+10))
        for c,a in enumerate(alts):
            f=work/s/f'{s}-{a}.svg'
            if f.exists():
                im=Image.open(io.BytesIO(cairosvg.svg2png(url=str(f),output_width=S-10,output_height=S-10))).convert('RGBA')
                W.alpha_composite(im,(x0+(c+1)*S+5,y+5))
        d.text((x0+4,y+S),s,fill=(255,0,0,255))
W.save(out)
