#!/usr/bin/env python3
"""Copy the bundled 25 November front page out to the output location.

The picture lives in this directory as ``entry.png``.  This script
confirms it is a whole PNG or JPEG within the size limits, then writes
an exact copy to ``/output/entry.png`` (or to the directory named by
``MAKEFUN_OUTPUT_DIR``, or to a path given with ``--output``).  It does
no decoding, no re-encoding and no renaming of anything: the bytes that
come out are the bytes that went in.

Everything here is standard library.  No network, no clock, no random
numbers are involved.
"""

import argparse
import hashlib
import os
import sys
from pathlib import Path

LIMIT_BYTES = 1048576
LIMIT_SIDE = 1024
NAME = "entry.png"


def fail(message):
    """Print an error and stop with a non-zero status."""
    print("error:", message, file=sys.stderr)
    return 1


def png_dims(blob):
    """Width and height from the IHDR chunk of a PNG byte string."""
    if len(blob) < 24 or blob[12:16] != b"IHDR":
        raise ValueError("PNG has no usable IHDR chunk")
    wide = int.from_bytes(blob[16:20], "big")
    tall = int.from_bytes(blob[20:24], "big")
    return wide, tall


def jpg_dims(blob):
    """Width and height from the first frame segment of a JPEG."""
    pos = 2
    frames = (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
              0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF)
    while pos + 3 < len(blob):
        if blob[pos] != 0xFF:
            raise ValueError("JPEG marker stream is broken")
        while blob[pos + 1] == 0xFF:
            pos += 1
        marker = blob[pos + 1]
        if marker == 0xD8:
            pos += 2
            continue
        if marker in (0xD9, 0xDA):
            break
        size = int.from_bytes(blob[pos + 2:pos + 4], "big")
        if size < 2 or pos + 2 + size > len(blob):
            raise ValueError("JPEG segment runs past the end")
        if marker in frames:
            tall = int.from_bytes(blob[pos + 5:pos + 7], "big")
            wide = int.from_bytes(blob[pos + 7:pos + 9], "big")
            return wide, tall
        pos += 2 + size
    raise ValueError("JPEG has no frame segment")


def check(blob):
    """Validate the bundled bytes; return (format, width, height)."""
    if len(blob) == 0:
        raise ValueError("bundled picture is empty")
    if len(blob) > LIMIT_BYTES:
        raise ValueError(f"picture is {len(blob)} bytes, over the limit")
    if blob[:8] == b"\x89PNG\r\n\x1a\n":
        kind = "PNG"
        wide, tall = png_dims(blob)
        tail_ok = blob[-12:-8] == b"\x00\x00\x00\x00" and blob[-8:-4] == b"IEND"
        if not tail_ok:
            raise ValueError("PNG lacks its IEND chunk")
    elif blob[:3] == b"\xff\xd8\xff":
        kind = "JPEG"
        wide, tall = jpg_dims(blob)
        if blob[-2:] != b"\xff\xd9":
            raise ValueError("JPEG lacks its end marker")
    else:
        raise ValueError("picture is neither PNG nor JPEG")
    if wide < 1 or tall < 1:
        raise ValueError(f"picture dimensions {wide}x{tall} are invalid")
    if wide > LIMIT_SIDE or tall > LIMIT_SIDE:
        raise ValueError(f"picture is {wide}x{tall}, over the side limit")
    return kind, wide, tall


def options():
    """Parse the command line."""
    parser = argparse.ArgumentParser(
        description="Check the bundled front page and copy it out.")
    parser.add_argument("--verify-only", action="store_true",
                        help="check the picture and write nothing")
    parser.add_argument("--output", metavar="PATH", default=None,
                        help="write the copy here instead of the default")
    parser.add_argument("--digest", action="store_true",
                        help="print the SHA-256 of the bundled picture")
    return parser.parse_args()


def destination(explicit):
    """Where the published copy belongs."""
    if explicit:
        return Path(explicit)
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if folder:
        return Path(folder) / "entry.png"
    return Path("/output/entry.png")


def main():
    """Verify the bundled picture, then publish it."""
    args = options()
    here = Path(__file__).resolve().parent
    try:
        blob = (here / NAME).read_bytes()
    except OSError as err:
        return fail(f"cannot read {NAME}: {err}")
    try:
        kind, wide, tall = check(blob)
    except ValueError as err:
        return fail(str(err))
    print(f"verified: {kind} {wide}x{tall}, {len(blob)} bytes")
    if args.digest:
        print("sha256:", hashlib.sha256(blob).hexdigest())
        return 0
    if args.verify_only:
        return 0
    target = destination(args.output)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blob)
        again = target.read_bytes()
    except OSError as err:
        return fail(f"cannot write {target}: {err}")
    if hashlib.sha256(again).digest() != hashlib.sha256(blob).digest():
        return fail("output does not match the bundled picture")
    print(f"wrote: {target} ({len(blob)} bytes, byte-identical)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
