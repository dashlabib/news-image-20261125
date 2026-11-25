#!/usr/bin/env python3
"""Deliver the bundled front-page image for 25 November 2026.

The image itself lives next to this file as entry.png. This program
does only three things, all offline and deterministic:

* check that the bundled file really is a PNG or JPEG image, is no
  larger than 1 MiB, and is no bigger than 1024 by 1024 pixels;
* copy it byte for byte to the output location;
* optionally report its SHA-256 digest, or only verify it.

It uses nothing but the Python standard library. It makes no network
calls, reads no clock, and uses no randomness, so repeated runs over
the same bundled file always produce identical output.
"""

import argparse
import hashlib
import os
import struct
import sys
from pathlib import Path

MAX_BYTES = 1_048_576
MAX_WIDTH = 1024
MAX_HEIGHT = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"

HERE = Path(__file__).resolve().parent
BUNDLED = HERE / "entry.png"
DEFAULT_OUTPUT_DIR = Path("/output")


def fail(message):
    """Print a plain error to stderr and exit non-zero."""
    print(f"error: {message}", file=sys.stderr)
    return 1


def sha256_of(path):
    """Return the hex SHA-256 digest of a file's bytes."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(65536)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(data):
    """Read width and height from a PNG's IHDR chunk, or None."""
    if len(data) < 33:
        return None
    if data[:8] != PNG_MAGIC:
        return None
    if data[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def jpeg_dimensions(data):
    """Scan JPEG markers for the first frame segment and read its size."""
    if len(data) < 4 or data[:3] != JPEG_MAGIC:
        return None
    pos = 2
    while pos + 9 < len(data):
        if data[pos] != 0xFF:
            return None
        marker = data[pos + 1]
        # Standalone markers carry no length field; skip them.
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        length = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if length < 2 or pos + length > len(data):
            return None
        # Start-of-frame markers (except the lossless/arithmetic ones
        # this simple reader does not need) hold height then width.
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            height, width = struct.unpack(
                ">HH", data[pos + 5:pos + 9])
            return width, height
        pos += 2 + length
    return None


def verify_image(path):
    """Check the bundled file; return (width, height) or an error string."""
    try:
        data = path.read_bytes()
    except OSError as exc:
        return None, f"cannot read bundled image {path}: {exc}"
    if len(data) == 0:
        return None, "bundled image is empty"
    if len(data) > MAX_BYTES:
        return None, (
            f"bundled image is {len(data)} bytes, over the "
            f"{MAX_BYTES} byte limit")
    if data[:8] == PNG_MAGIC:
        dimensions = png_dimensions(data)
        if dimensions is None:
            return None, "bundled PNG has no readable IHDR chunk"
        if not data.rstrip(b"\x00").endswith(b"IEND\xaeB`\x82"):
            return None, "bundled PNG looks truncated: no IEND trailer"
    elif data[:3] == JPEG_MAGIC:
        dimensions = jpeg_dimensions(data)
        if dimensions is None:
            return None, "bundled JPEG has no readable frame segment"
        if not data.rstrip(b"\x00").endswith(b"\xff\xd9"):
            return None, "bundled JPEG looks truncated: no end marker"
    else:
        return None, (
            "bundled file is not a PNG or JPEG image "
            "(bad magic bytes)")
    width, height = dimensions
    if width <= 0 or height <= 0:
        return None, f"bundled image has invalid size {width}x{height}"
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        return None, (
            f"bundled image is {width}x{height}, over the "
            f"{MAX_WIDTH}x{MAX_HEIGHT} limit")
    return (width, height), None


def resolve_output(args):
    """Work out where the copy goes: --output, env var, or /output."""
    if args.output:
        return Path(args.output)
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return Path(env_dir) / "entry.png"
    return DEFAULT_OUTPUT_DIR / "entry.png"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Verify and deliver the bundled front-page image.")
    parser.add_argument(
        "--output", default=None,
        help="write the copy to this path instead of /output/entry.png")
    parser.add_argument(
        "--verify-only", action="store_true",
        help="only check the bundled image; write nothing")
    parser.add_argument(
        "--digest", action="store_true",
        help="print the SHA-256 digest of the bundled image")
    args = parser.parse_args(argv)

    if not BUNDLED.exists():
        return fail(f"bundled image not found: {BUNDLED}")

    dimensions, error = verify_image(BUNDLED)
    if error is not None:
        return fail(error)
    width, height = dimensions

    digest = sha256_of(BUNDLED)
    print(f"verified: {BUNDLED.name} {width}x{height} "
          f"{BUNDLED.stat().st_size} bytes sha256={digest}")
    if args.digest:
        print(digest)
    if args.verify_only:
        return 0

    target = resolve_output(args)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(BUNDLED.read_bytes())
    except OSError as exc:
        return fail(f"cannot write output {target}: {exc}")

    # Read the copy back and confirm it is byte-identical.
    if sha256_of(target) != digest:
        return fail(f"output copy at {target} does not match the bundle")
    print(f"wrote {target} ({width}x{height})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
