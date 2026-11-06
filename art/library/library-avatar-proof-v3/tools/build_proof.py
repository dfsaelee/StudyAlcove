"""Rebuild the offline review page and rendered proof directly from PNG layers."""
import base64
import io
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT.parent / "library-sprites-v2"
PRE = ROOT / "previews"
NN = Image.Resampling.NEAREST
ORIGIN = (27,61)
RAIL = (31,86)

def read(path):
    with Image.open(path) as im:
        return im.convert("RGBA")

def upscale(im, factor):
    return im.resize((im.width*factor, im.height*factor), NN)

def room_layers():
    room = read(V2/"previews/library-native.png")
    props = {p.stem: read(p) for p in (V2/"cleaned/props").glob("*.png")}
    tiles = {p.stem: read(p) for p in (V2/"cleaned/tiles").glob("*.png")}
    for row in range(3,12):
        for col in range(20):
            tile = "oak_a" if (col+row//2)%3 else "oak_b"
            if row==3 and col in [9,10]:
                tile="threshold"
            room.paste(tiles[tile], (col*16,row*16))
    room.alpha_composite(props["rug"],(136,135))
    for row in range(2):
        for col,x in enumerate([23,84,204,265]):
            y=65+61*row
            desk=["writing_desk","reading_desk"][(col+row)%2]
            chair=["slat_chair","padded_chair"][col%2]
            room.alpha_composite(props[desk],(x,y))
            room.alpha_composite(props[["brass_lamp","banker_lamp"][col%2]],(x+1,y-8))
            tuck=4 if (col,row)==(0,0) else 0
            room.alpha_composite(props[chair],(x+8,y+13-tuck))
    for x in [0,298]:
        for y in [43,160]:
            room.alpha_composite(props["fern" if x else "autumn_plant"],(x,y))
    return room,props["slat_chair"].crop((0,12,16,18))

def encoded(im):
    out=io.BytesIO()
    im.save(out,format="PNG")
    return "data:image/png;base64,"+base64.b64encode(out.getvalue()).decode()

def cell(im,i):
    return im.crop((24*i,0,24*i+24,32))

def compose(images,hair,clothes):
    im=Image.new("RGBA",(240,32))
    for name in [hair+"Back","body",clothes,hair+"Front"]:
        im.alpha_composite(images[name])
    return im

def seated(room,rail,avatar):
    result=room.copy()
    result.alpha_composite(avatar,ORIGIN)
    result.alpha_composite(rail,RAIL)
    return result

def main():
    PRE.mkdir(exist_ok=True)
    room,rail=room_layers()
    paths={"body":"body", "cropBack":"crop-back","cropFront":"crop-front",
           "bobBack":"bob-back","bobFront":"bob-front","tee":"tee","cardigan":"cardigan"}
    images={key:read(ROOT/"layers"/(name+".png")) for key,name in paths.items()}
    palette=json.loads((ROOT/"authoring/palette.json").read_text(encoding="utf-8-sig"))
    data={"images":{key:encoded(im) for key,im in {**images,"room":room,"rail":rail}.items()},
          "ramps":palette["ramps"]}
    html=(ROOT/"tools/studio.template.html").read_text(encoding="utf-8-sig")
    (ROOT/"START-HERE.html").write_text(html.replace("__DATA__",json.dumps(data)),encoding="utf-8")
    board=Image.new("RGB",(1040,688),"#f6f2e8")
    d=ImageDraw.Draw(board)
    font_root=Path("C:/Windows/Fonts")
    title=ImageFont.truetype(str(font_root/"georgia.ttf"),32)
    normal=ImageFont.truetype(str(font_root/"segoeui.ttf"),15)
    d.text((28,12),"One base, four looks",font=title,fill="#293d35")
    for index,(label,x) in enumerate([("TURNAROUND",34),("EAST WALK",475),("SEATED STUDY",845)]):
        d.text((x,70),label,font=normal,fill="#46624f")
    for i,(hair,clothes) in enumerate([(h,c) for h in ["crop","bob"] for c in ["tee","cardigan"]]):
        strip=compose(images,hair,clothes)
        y=104+146*i
        d.text((28,y),f"{hair.title()}  /  {clothes.title()}",font=normal,fill="#293d35")
        for j in range(10):
            x=(32+j*86) if j<4 else (465+(j-4)*86 if j<8 else 842+(j-8)*86)
            avatar=upscale(cell(strip,j),3)
            board.paste(avatar,(x,y+28),avatar)
        for label,cols,ms in [("walk",range(4,8),125),("study",[8,9],333)]:
            frames=[upscale(cell(strip,j),4) for j in cols]
            frames[0].save(PRE/f"{hair}-{clothes}-{label}.png",save_all=True,append_images=frames[1:],duration=ms,loop=0,blend=0,disposal=0)
        if (hair,clothes) in [("crop","tee"),("bob","cardigan")]:
            native=seated(room,rail,cell(strip,8))
            native.save(PRE/f"library-{hair}.png")
            upscale(native,3).save(PRE/f"library-{hair}-3x.png")
    board.save(PRE/"four-looks.png")

if __name__=="__main__":
    main()

