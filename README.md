# The World in One Picture — Wednesday 25 November 2026

A single 1024×1024 front page that tries to hold a whole morning of
news in one image, made for the make.fun `news-image-20261125` bounty
(Round 1, $100, entries close 2026-11-27T00:00:00Z).

## What the image shows

The page is laid out like a broadsheet front page, drawn entirely
with flat coloured blocks and simple shapes — there are no
photographs in it, and nothing was fetched from the internet while
it was drawn.

Across the top, a navy masthead carries the paper's name and the
date line: Wednesday 25 November 2026, morning edition. Under it,
the lead story takes the full width of the page in a deep red block
with a small drawn skyline: the investigation into Shanghai's party
chief Chen Jining, a Politburo member — the fourth Politburo member
to be probed since 2025.

Below the lead, twelve pictured stories sit in a four-by-three grid.
Each panel has its own coloured scene strip with a simple mark, a
category label, and a short headline. At the foot of the page, an
"ALSO TODAY" ticker in two columns carries eighteen one-line briefs
from the rest of the morning's news.

## How to run it

`main.py` uses only the Python standard library. It first checks the
bundled `entry.png` — that it really is a PNG or JPEG, that it is no
larger than 1 MiB, and that it is no bigger than 1024×1024 pixels —
and refuses with a plain error and a non-zero exit if anything is
wrong. Then it copies the file byte for byte to the output location.

```sh
python3 main.py                      # verify, then copy to /output/entry.png
python3 main.py --output out/entry.png
python3 main.py --verify-only        # check the bundle, write nothing
python3 main.py --digest             # also print the SHA-256 digest
```

`MAKEFUN_OUTPUT_DIR` can be set instead of passing `--output`; the
copy lands in `$MAKEFUN_OUTPUT_DIR/entry.png` in that case.

## Determinism check

The program makes no network calls, reads no clock, and uses no
randomness, so every run over the same bundled file produces the
same bytes. This was checked by running it twice into two different
output folders and comparing all three digests:

```text
17524a9de71ab6f8676dedb7d6b4c9f796eac281ba588f8bc3c9c1c320df590b  entry.png
17524a9de71ab6f8676dedb7d6b4c9f796eac281ba588f8bc3c9c1c320df590b  out1/entry.png
17524a9de71ab6f8676dedb7d6b4c9f796eac281ba588f8bc3c9c1c320df590b  out2/entry.png
```

All three SHA-256 digests match, and both copies are byte-identical
to the bundled file. The image itself is 1024×1024 pixels and
127,363 bytes — well under the 1 MiB limit.

## The stories on the page

**Lead story — China.** Shanghai party chief Chen Jining, a
Politburo member, is under investigation; he is the fourth
Politburo member to be probed since 2025.

**The twelve pictured stories:**

1. Courts — Huawei is convicted in the United States on 10 of
   12 counts.
2. Markets — the Nvidia rally fades as Huang returns.
3. White House — Trump pardons the turkeys Freedom and Feathers.
4. Washington — Giuliani is awarded the Medal of Freedom.
5. Gaza — a Hamas security chief is killed in a Gaza City strike.
6. Riyadh — a tower is hit for a second time in a week.
7. Climate — COP31 collapses with no deal.
8. Football — Senegal win the AFCON title back after a CAS ruling.
9. Football — Real Madrid beat PSV 5–1.
10. Colombia — 25 hostages are taken at a Cartagena supermarket.
11. Security — the CIA and the ODNI are hit by a cybersecurity breach.
12. United Nations — five women are killed each hour by relatives
    in 2025, according to the UN.

**Also today — the eighteen ticker briefs:**

- Iraq's Kurdish oilfields in focus
- Russia calls ship drones "terrorism"
- The Gaza toll reaches 74,746
- The WFP counts 266 million people as food-insecure
- Landmine deaths hit a five-year high of 7,000
- Shein agrees a $100m FTC settlement
- California hit by flooding
- Russian planes enter South Korea's air zone
- Democrats look ahead to 2028
- A Fort Hood execution bid advances
- A US soldier is accused of selling secrets
- Malaysia steps up repatriations
- North Korea opens a Swiss office
- China in the race for cobalt
- Denmark orders "ghetto" evictions
- Nigeria suspends an emir
- DR Congo rebels pull back
- Britain sanctions the Houthis

## Sources

The stories were gathered from reporting by Reuters, AP, the BBC,
SCMP, The Hindu, and The Guardian, as reported by about 02:00 UTC
on 25 November 2026. This is Round 1, filed early in the day; an
improvement round is expected later, when the day's later
developments can be folded in.

## Repo contents

- `entry.png` — the finished 1024×1024 front page (127,363 bytes).
- `main.py` — the stdlib-only verifier and delivery script.
- `build_entry_image.py` — the Pillow script that draws `entry.png`
  (build-time only; run it again with `python3 build_entry_image.py`
  to regenerate the image).
- `LICENSE` — MIT.

## Referral

Made with make.fun — referral link
<https://make.fun/r/q5gfrt9g> (code `q5gfrt9g`).
