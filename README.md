# Wednesday 25 November 2026 — The World in One Picture

One newspaper front page for the morning of Wednesday 25 November 2026.
The lead story is China's shock corruption probe into Politburo member
and Shanghai party chief Chen Jining; below it, twelve more stories get
a picture each, and eighteen further items run in the "ALSO TODAY"
ticker. The entry itself is a single 1024×1024 image. The program
shipped with it does nothing but check that image and copy it to the
output path, byte for byte — nothing is downloaded, generated or
altered while it runs.

## Running it

```sh
python3 main.py
```

That checks `entry.png` and writes the copy to `/output/entry.png`.
Other ways to run it:

```sh
python3 main.py --verify-only          # check only, write nothing
python3 main.py --digest               # print the picture's SHA-256
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

`main.py` uses only the Python standard library. After writing, it
reads the output back and compares SHA-256 digests with the bundled
file, so two runs always agree:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out1 python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/out2 python3 main.py
sha256sum /tmp/out1/entry.png /tmp/out2/entry.png entry.png
```

All three digests must match. A truncated or non-image file is refused
with a plain error message and a non-zero exit.

Rebuilding the picture itself is a build-time job only (Pillow needed):

```sh
python3 build_entry_image.py
```


## The day's stories

**Lead — China:** Shanghai party chief Chen Jining, a Politburo
member, is under investigation for "suspected severe violations of
discipline and laws" — the fourth member of the top leadership body to
be probed since 2025.

**Twelve pictured stories, in reading order:**

1. Huawei convicted in US — guilty on 10 of 12 counts, trade secrets and Iran business
2. Nvidia rally fades — Huang back as CEO, shares drop again, board under scrutiny
3. Trump pardons turkeys — Freedom & Feathers spared at the White House
4. Giuliani gets Medal of Freedom — the highest US civilian honour
5. Hamas security chief killed — an Israeli strike on Gaza City
6. Riyadh tower hit again — Saudi condemns a "terrorist attack", second in a week
7. COP31 collapses — no deal as oil and gas producers block phaseout language
8. Senegal win AFCON back — CAS overturns the ruling that handed the title to Morocco
9. Real Madrid 5-1 PSV — Bellingham stunner, Mbappe brace
10. 25 hostages in Colombia — gunmen seize a Cartagena supermarket
11. CIA, ODNI breached — unclassified data exposed, NYT reports
12. Five women killed each hour — by relatives in 2025, UN says

**Also today, eighteen one-liners:** Iraq orders seizure of Kurdish
oilfields; Russia cries "terrorism" over ship drones; Gaza death toll
74,746, WAFA says; 266m face acute food insecurity (WFP); landmine
deaths hit a 5-year high of 7,000; Shein to pay $100m in an FTC
settlement; extreme flooding threatens California; Seoul says Russian
planes entered its air zone; Democrats turn sights to 2028; Fort Hood:
last bid on the execution fails; US soldier admits selling secrets;
Malaysia to repatriate migrants; North Korea threatens to shut its
Swiss office; China cobalt race beats the Congo ban; Denmark upholds
"ghetto" evictions; Nigeria emir suspended over a claim; rebels pull
back in DR Congo; Britain sanctions the Houthis and four officials.

Sources: Reuters, AP, BBC, SCMP, The Hindu, The Guardian — as reported
by 02:00 UTC, 25 November 2026. This is round 1, filed early in the
day; more of 25 November's news will follow in a later round.


## What is in the repository

- `main.py` — the entry program: check the bundled picture, copy it out.
- `entry.png` — the front page, 1024×1024 JPEG, under 1 MiB.
- `build_entry_image.py` — the build-time composer that made `entry.png`.
- `LICENSE` — MIT.

## Referral

Made for the make.fun bounty by @dashlabib — referral link:
https://make.fun/r/q5gfrt9g
