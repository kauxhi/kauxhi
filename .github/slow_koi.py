"""Slow the koi GIF by raising every frame delay. git-koi renders at 2cs per frame."""
import sys

DELAY_CS = 8  # 8 = quarter speed (12.5 fps). 4 = half speed, 2 = original.

path = sys.argv[1]
d = bytearray(open(path, "rb").read())
n, i = 0, 0
while True:
    i = d.find(b"\x21\xf9\x04", i)  # graphic control extension
    if i < 0:
        break
    if d[i + 7] == 0:  # block terminator: a real extension, not pixel data that looks like one
        d[i + 4:i + 6] = DELAY_CS.to_bytes(2, "little")
        n += 1
    i += 8
assert n > 1, f"expected an animated GIF, found {n} frame headers"
open(path, "wb").write(d)
print(f"{n} frames set to {DELAY_CS}cs")
