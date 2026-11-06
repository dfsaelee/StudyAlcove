"""Rebuild the review pack, or align a full-canvas sprite to its native grid.

python align_sprites.py
python align_sprites.py enlarged.png aligned.png --size 24 32
Requires Pillow. Keep the original canvas origin and padding when using --size.
"""
import argparse
import json
import shutil
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageColor, ImageDraw

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent / "library-sprites-v1"
HEX = """66535e 795f64 936d68 a37a70 b88e76 c89e80 deb698 edcfb1 f7e3c3 fff2d9
547574 679087 88afa0 a6c4aa c9dcaf 9e716f c48379 dc9a88 e7ab88 f2c879
76849a a3b1bf b79284 d8a891 eec2a8 ffdbc1 785851 986e5b b58a71 9a7d95 b996ae eddcc5""".split()
PALETTE = [ImageColor.getrgb("#" + value) for value in HEX]
CLEAR = (0, 0, 0, 0)
NEAREST = Image.Resampling.NEAREST


def snap(image, size, source_palette):
    """Area-sample each logical cell, restore hard alpha, and index its color."""
    if image.width * size[1] != image.height * size[0]:
        raise ValueError("Input and logical canvas must have the same aspect ratio")
    rgba = image.convert("RGBA")
    if rgba.size != size:
        rgba = rgba.resize(size, Image.Resampling.BOX)
    exact = dict(zip(source_palette, PALETTE))

    @lru_cache(None)
    def match(pixel):
        if pixel[3] < 128:
            return CLEAR
        rgb = pixel[:3]
        if rgb in exact:
            return (*exact[rgb], 255)
        nearest = min(range(len(source_palette)), key=lambda i: sum(
            (a - b) ** 2 for a, b in zip(rgb, source_palette[i])))
        return (*PALETTE[nearest], 255)

    result = Image.new("RGBA", size)
    result.putdata([match(pixel) for pixel in rgba.getdata()])
    return result


def enlarge(im, zoom):
    return im.resize((im.width * zoom, im.height * zoom), NEAREST)


def sheet(size):
    return Image.new("RGBA", size, CLEAR)


def label(im, xy, text):
    pen = ImageDraw.Draw(im)
    pen.fontmode = "1"
    x, y = xy
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        pen.text((x + dx, y + dy), text, fill=(*PALETTE[9], 255))
    pen.text(xy, text, fill=(*PALETTE[0], 255))


def build():
    for folder in ["cleaned/avatars", "cleaned/props", "cleaned/tiles", "previews", "metadata"]:
        (ROOT / folder).mkdir(parents=True, exist_ok=True)
    source = [ImageColor.getrgb(c) for c in json.loads((OLD / "metadata/palette.json").read_text())]
    for path in (OLD / "metadata").glob("*.json"):
        if path.stem != "palette":
            shutil.copyfile(path, ROOT / "metadata" / path.name)
    (ROOT / "metadata/palette.json").write_text(json.dumps(["#" + v for v in HEX], indent=2))
    art = {}
    for path in sorted((OLD / "cleaned").rglob("*.png")):
        with Image.open(path) as original:
            im = snap(original, original.size, source)
        art[path.stem] = im
        im.save(ROOT / path.relative_to(OLD))

    # Build the inspection sheet in logical pixels, then magnify the entire canvas.
    board = sheet((320, 247))
    label(board, (8, 3), "StudyAlcove  /  Library")
    groups = [
        ["tall_shelf", "low_shelf", "writing_desk", "reading_desk", "slat_chair", "padded_chair"],
        ["fern", "autumn_plant", "banker_lamp", "brass_lamp", "clock", "rug"],
    ]
    for row, names in enumerate(groups):
        for col, name in enumerate(names):
            im = art[name]
            x = 27 + col * 53
            y = 65 + row * 58
            board.alpha_composite(im, (x - im.width // 2, y - im.height))
    avatar = art["composed"]

    def frame(row, column):
        return avatar.crop((column*24, row*32, column*24+24, row*32+32))

    samples = [
        ("Idle", [(0, 0), (0, 1)]),
        ("Walk", [(2, 2), (2, 3)]),
        ("Sit", [(1, 6), (3, 6)]),
        ("Focus", [(3, 7), (3, 8)]),
    ]
    for i, (name, poses) in enumerate(samples):
        label(board, (12 + i*78, 138), name)
        for j, (direction, column) in enumerate(poses):
            board.alpha_composite(frame(direction, column), (9 + i*78 + j*27, 153))
    label(board, (8, 202), "Interior tiles")
    board.alpha_composite(art["interior_atlas"], (10, 222))
    enlarge(board, 3).save(ROOT / "START-HERE.png")

    for name in ["library-native", "seated-detail"]:
        if name == "library-native":
            with Image.open(OLD / "previews/library-native.png") as original:
                room = snap(original, original.size, source)
            room.save(ROOT / "previews/library-native.png")
            enlarge(room, 3).save(ROOT / "previews/library-3x.png")
        else:
            detail = sheet((112, 56))
            for i,x in enumerate([15,257]):
                detail.alpha_composite(room.crop((x,56,x+48,112)), (i*64,0))
            enlarge(detail, 6).save(ROOT / "previews/seated-detail.png")

    contact = sheet((262, 156))
    for row, direction in enumerate(["South","West","East","North"]):
        label(contact, (3, row*37 + 15), direction)
        for col in range(9):
            contact.alpha_composite(frame(row,col), (43+col*24,row*37))
    enlarge(contact, 4).save(ROOT / "previews/animation-frames.png")
    for name, color in [("light", "#fff4e0"), ("dark", "#443847")]:
        backdrop = Image.new("RGBA", avatar.size, color)
        backdrop.alpha_composite(avatar)
        enlarge(backdrop, 4).save(ROOT / ("previews/contrast-" + name + ".png"))

    for name, cols, ms in [("idle",[0,1],500),("walk",[2,3,4,5],125),("focus",[7,8],333)]:
        frames = []
        for col in cols:
            strip = sheet((96,32))
            for row in range(4):
                strip.alpha_composite(frame(row,col), (row*24,0))
            frames.append(enlarge(strip,4))
        frames[0].save(ROOT / ("previews/"+name+"-4x.png"), save_all=True,
                       append_images=frames[1:], duration=ms, loop=0, disposal=0, blend=0)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("paths", nargs="*", type=Path)
    cli.add_argument("--size", nargs=2, type=int, metavar=("WIDTH","HEIGHT"))
    args = cli.parse_args()
    if not args.paths and not args.size:
        build()
    elif len(args.paths) == 2 and args.size and min(args.size) > 0:
        if args.paths[0].resolve() == args.paths[1].resolve():
            cli.error("Use a separate output file")
        with Image.open(args.paths[0]) as im:
            snap(im, tuple(args.size), PALETTE).save(args.paths[1], format="PNG")
    else:
        cli.error("Supply input.png output.png --size WIDTH HEIGHT, or omit all arguments")




