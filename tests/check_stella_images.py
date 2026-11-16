"""P01 diagnostic screenshots from actual Stella TIA rendering.

Checks sprite dimensions and one joystick motion. This is automated smoke
coverage, not independent verification of the entire Atari 2600 game.
"""
from pathlib import Path
from PIL import Image

root = Path('build')

def sprite(path: Path):
    im = Image.open(path).convert('RGB')
    data = im.load()
    xs = []
    ys = []
    for y in range(im.height):
        for x in range(im.width):
            r, g, b = data[x, y]
            if g > 80 and g > r * 1.25 and g > b * 1.25:
                xs.append(x)
                ys.append(y)
    if len(xs) < 16:
        raise AssertionError(f'No sufficient green troll pixels in {path}')
    box = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
    return box, len(xs), im.size

boxes = []
for i, expected in enumerate(((16, 12), (32, 24), (64, 36)), start=1):
    box, n, canvas = sprite(root / f'p01_level{i}.png')
    size = (box[2] - box[0], box[3] - box[1])
    print(f'level {i}: canvas={canvas}, bounding_box={box}, green_pixels={n}')
    assert size == expected, f'Level {i}: expected {expected}, got {size}'
    boxes.append(box)

moved, n, canvas = sprite(root / 'p01_level3_right.png')
print(f'movement: from={boxes[2]} to={moved}, green_pixels={n}')
assert moved[0] >= boxes[2][0] + 8, 'Right input did not move sprite far enough'
assert moved[1] == boxes[2][1], 'Right input unexpectedly changed vertical position'
assert moved[2] - moved[0] == 64 and moved[3] - moved[1] == 36
print('PASS: Stella P01 actual TIA frames show three sprite sizes and rightward motion.')
