[English](README.md) | [Português (BR)](README.pt-BR.md) | [Español](README.es.md)

# phomemo-t02-linux

## What is this

A driver for the Phomemo T02 thermal printer on Linux, over Bluetooth LE (BLE). Includes a standalone CLI (`t02`) and a CUPS backend for printing from any application.

## Requirements

- Python 3
- `uv` (recommended, runs the script with inline dependencies) **or** `bleak` + `pillow` installed manually (`pip install -r requirements.txt`)
- BlueZ (Linux Bluetooth stack)

## Installation

Copy `t02` to `~/.local/bin` and make it executable:

```sh
cp t02 ~/.local/bin/t02
chmod +x ~/.local/bin/t02
```

## First use

Run the setup wizard, which scans for the printer over BLE and saves its address:

```sh
t02 --setup
```

Config is saved at `~/.config/t02.conf`.

## Usage

```sh
t02 "some text"          # print text
t02 image.png            # print an image
t02 --font FONT.ttf ...  # custom font
t02 --size 32 ...        # font size
t02 --feed 8 ...         # extra feed in mm after printing
t02 --info               # query printer status
```

## Markdown

`t02 file.md` prints Markdown with bold, italic, underline (`++text++` or `<u>`), headings, lists, blockquotes, code, tables (equal-width columns at 48mm), horizontal rules, and local images. Requires Google Chrome or Chromium installed as a `.deb` (the snap build of Chromium is not supported), plus the `markdown` pip package or `python3-markdown` apt package. Limit: about 2m of height per print.

## CUPS/KDE integration

The `cups/t02-backend` script converts a print job (PDF) to PNG at 203dpi and sends it to the printer.

1. Install the backend as root:

   ```sh
   sudo install -o root -g root -m 0700 cups/t02-backend /usr/lib/cups/backend/t02
   ```

2. Register the printer:

   ```sh
   sudo lpadmin -p T02 -E -v t02:/ -m raw
   ```

3. Set the paper size to 48mm in the printer's options.

CUPS runs the backend as root, so the **system** Python needs `python3-bleak` and `python3-pil` installed (not just a user venv/uv environment). The backend reads the `t02` binary path from the `T02_BIN` env var (default `/usr/local/bin/t02`) — install a copy of `t02` there, or set `T02_BIN` accordingly.

## Troubleshooting

- **`ProfileUnavailable` error**: remove the stale BLE bond and rescan:

  ```sh
  bluetoothctl remove <MAC>
  bluetoothctl scan transport le
  ```

- The T02 only accepts **one BLE connection at a time** — disconnect any other client (app, another `t02` instance) before printing.
- Classic Bluetooth / RFCOMM does **not** work with this printer; it must be BLE.

## Protocol notes

- BLE GATT service `ff00`, write characteristic `ff02`, notify characteristics `ff01`/`ff03`.
- Images are sent as ESC/POS `GS v 0` raster commands.
- Status replies of the form `1f 11 xx` are acknowledged by sending `1a xx`.

## `--raw` mode

`--raw` sends printer commands directly over a low-level BLE write, bypassing the asyncio/bleak client loop. This is **experimental** and less tested than the default path — expect rough edges.

## Credits

Based on protocol reverse-engineering from [vivier/phomemo-tools](https://github.com/vivier/phomemo-tools) and [transcriptionstream/phomymo](https://github.com/transcriptionstream/phomymo).
