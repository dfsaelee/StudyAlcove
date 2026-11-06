"""Draw the 24 x 32 base, with per-cell joints for optional overlay artwork."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE.parent.parent / "references"
COLORS = dict(k='#463138', s='#ae6952', b='#e09d6f', l='#f8c793',
              e='#49363b', w='#ffdfac', t='#ac6a61', d='#52505e',
              p='#797286', h='#b3a4a1', f='#69505a', g='#9b7972')

# Each row is an individually drawn scanline. Empty cells keep their alpha.
FRONT = """
....kkkkkk....
..kkbllllbkk..
.kbllllllllbk.
.kblllllllllk.
kbllllllllllbk
kbllllllllllbk
kbllllllllllbk
ksblllllllllbk
ksblllllllllbk
ksbeelllleebbk
ksbekllllekbbk
.ksblllbllbbk.
..ksbllllbbk..
...kssbbsbk...
.....kkkk.....
"""
PROFILE = """
....kkkkkk....
..kkbllllbkk..
.kbllllllllbk.
.kblllllllllk.
kbllllllllllbk
kbllllllllllbk
kbllllllllllbk
ksblllllllbblk
ksbbllllllbek.
ksbssbllllbek.
.ksbblblllllbk
.ksbbsbllllbk.
..kssbbllbbk..
....kssbbkk...
......kkk.....
"""
BACK = """
....kkkkkk....
..kkbllllbkk..
.kbllllllllbk.
.kblllllllllk.
kbllllllllllbk
kbllllllllllbk
kbllllllllllbk
ksblllllllllbk
ksbllllllllbbk
ksbbllllllbbsk
ksbbsllbbbsssk
.kssbbbbbbssk.
..kssbbbbssk..
...kksssskk...
.....kkkk.....
"""
TRUNK = """
...kkkkkk...
..ksbbllbk..
.ksblllllbk.
.ksblllllbk.
.ksblllllbk.
..ksblllbk..
..kkssbbkk..
..kppppppk..
..kddppddk..
...kkkkkk...
"""
SIDE = """
...kkkkk..
..ksbbblk.
.ksbbbllbk
.ksbblllbk
.ksbblllbk
..ksblllbk
..kssbbbk.
..kpppppk.
..kddpddk.
...kkkkk..
"""

def stamp(im, pattern, xy):
    ox, oy = xy
    for y, row in enumerate(pattern.strip().splitlines()):
        for x, char in enumerate(row):
            if char != '.':
                im.putpixel((ox+x, oy+y), tuple(bytes.fromhex(COLORS[char][1:]))+(255,))

def limb(im, joints, base, light=None):
    draw = ImageDraw.Draw(im)
    for (x0,y0),(x1,y1) in zip(joints,joints[1:]):
        # Rounded 4-connected outer contour, continuous two-pixel interior.
        for offset in [(-1,0),(1,0),(0,-1),(0,1)]:
            dx,dy = offset
            draw.line((x0+dx,y0+dy,x1+dx,y1+dy),fill=COLORS['k'],width=3)
        draw.line((x0,y0,x1,y1),fill=COLORS[base],width=3)
    if light:
        draw.point(joints[-1],fill=COLORS[light])

def shoe(im, tip, facing, far):
    x,y=tip
    stamp(im, (".kkk.\nkddgk\n.kkk." if far else ".kkk.\nkfggk\n.kkk.") if facing else
          (".kk.\nkddk\nkkkk" if far else ".kk.\nkggk\nkkkk"), (x-2,y-2))

def pose(i):
    side=i in (1,2,4,5,6,7)
    sit=i>=8
    bob=-int(i in (5,7))
    h=(12,10+bob+int(sit))
    shoulders=[(8,18),(15,18)]
    elbows=[(7,20),(16,20)]
    wrists=[(6,22),(17,22)]
    waist=(12,23)
    knees=[(9,26),(14,26)]
    feet=[(9,29),(15,29)]
    hips=[(10,24),(14,24)]
    if side:
        shoulders=[(13,18+bob),(10,18+bob)]
        elbows=[(15,20+bob),(10,20+bob)]
        wrists=[(15,22+bob),(10,22+bob)]
        knees=[(14,26),(11,26)]
        feet=[(15,28),(11,29)]
        hips=[(14,24+bob),(11,24+bob)]
        waist=(12,23+bob)
    if 4<=i<=7:
        j=i-4
        knees=[[(15,25),(10,26)],[(13,25),(13,26)],[(10,26),(15,25)],[(13,26),(13,25)]][j]
        feet=[[(16,28),(8,29)],[(12,27),(14,29)],[(8,28),(17,29)],[(14,29),(11,27)]][j]
        elbows=[[(12,20),(12,20)],[(14,19),(10,19)],[(15,20),(9,20)],[(14,19),(10,19)]][j]
        wrists=[[(11,22),(14,22)],[(14,21),(11,21)],[(16,22),(8,22)],[(14,21),(10,21)]][j]
    if sit:
        hips=[(10,23),(14,23)]
        knees=[(8,24),(16,24)]
        feet=[(8,27),(15,27)]
        elbows=[(6,21),(17,21)]
        wrists=[(5,18),(18,17-(i-8))]
    im=Image.new('RGBA',(24,32))
    for n in range(2):
        limb(im,[hips[n],knees[n],(feet[n][0],feet[n][1]-2)],'d' if n==0 and side else 'p')
        shoe(im,feet[n],side,n==0 and side)
    if side:
        limb(im,[shoulders[0],elbows[0],wrists[0]],'s','b')
    stamp(im,SIDE if side else TRUNK,(7 if side else 6,16+bob))
    for n in ([1] if side else [0,1]):
        limb(im,[shoulders[n],elbows[n],wrists[n]],'b','l')
    stamp(im,PROFILE if side else BACK if i==3 or sit else FRONT,(6 if side else 5,3+bob+int(sit)))
    guide=dict(head=h,shoulders=shoulders,elbows=elbows,wrists=wrists,waist=waist,knees=knees,feet=feet)
    if i==1:
        im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        for k,v in list(guide.items()):
            guide[k]=[(23-x,y) for x,y in v] if isinstance(v,list) else (23-v[0],v[1])
    return im, guide

def main():
    layers=BASE/'layers'; layers.mkdir(exist_ok=True)
    author=BASE/'authoring'; author.mkdir(exist_ok=True)
    proof=BASE/'previews'; proof.mkdir(exist_ok=True)
    sheet=Image.new('RGBA',(240,32)); frames=[]
    names=['stand_south','stand_west','stand_east','stand_north','walk_east_0','walk_east_1','walk_east_2','walk_east_3','study_north_0','study_north_1']
    for i,name in enumerate(names):
        frame,guide=pose(i)
        sheet.paste(frame,(24*i,0))
        frames.append(dict(index=i,name=name,**guide))
    sheet.save(layers/'body.png')
    contract=dict(cell=[24,32],pivot=[12,29],origin='top-left; coordinates are inclusive pixel centers',
                  pairs='South, north and seated: screen-left then screen-right. Profiles: far then near.',
                  skin={k:list(bytes.fromhex(COLORS[c][1:])) for k,c in [('outline','k'),('shadow','s'),('base','b'),('light','l')]},frames=frames)
    (author/'landmarks.json').write_text(json.dumps(contract,indent=2)+'\n')
    compare(sheet, proof)

def compare(sheet, proof):
    chart=Image.new('RGB',(260,196),'#e8dfd3')
    draw=ImageDraw.Draw(chart); font=ImageFont.load_default(size=10)
    def title(y,t): draw.text((5,y),t,font=font,fill='#392e38')
    def cell(im,x,y):
        im=im.convert('RGBA'); chart.paste(im,(x,y),im)
    title(2,'Original base  /  24 x 32')
    cell(sheet,6,13)
    title(48,'MP5Mfe  /  native pixels (source 3x)')
    src=Image.open(SOURCE/'MP5Mfe.gif').convert('RGB').resize((128,80),0)
    chart.paste(src.crop((8,10,120,34)),(8,62))
    chart.paste(src.crop((8,42,120,66)),(128,62))
    title(90,'char free  /  global.png body frames')
    src=Image.open(SOURCE/'char free/global.png')
    cell(src.crop((0,0,256,32)),2,101)
    title(136,'Left gait                          Right gait')
    for n,side in enumerate(['left','right']):
        src=Image.open(SOURCE/f'char free/char_walk_{side}.gif')
        for j in range(4):
            src.seek(j*2); cell(src,2+128*n+32*j,148)
    chart.save(proof/'base-reference-native.png')
    chart.resize((chart.width*4,chart.height*4),0).save(proof/'base-reference-4x.png')

if __name__=='__main__':
    main()
