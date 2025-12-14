# N64 SRAM Save Converter

This takes the SRAM save files dumped from original carts by DreamDumper64 and converts them to .sav used by SummerCart 64.

To date I have only tested with two SRAM games I own.  Tested on Analogue3D.

I couldn't find another option online that worked correctly for me, so hopefully someone else may find this useful.

## ⚠️ AI Generated

This script was created with Claude (Anthropic) based on reverse-engineering DreamDumper64 save file formats and testing with actual N64 cartridges.

## What it does

Converts 32KB SRAM save files from the DreamDumper64 cart reader (which creates 128KB files) to the format needed for SummerCart 64 flashcarts.

The DreamDumper64 stores SRAM data in the first 32KB of a 128KB file. This script extracts that data and saves it in the raw cartridge format that SummerCart 64 expects.

## Supported Games

It should work with any N64 game that uses **256 Kilobits (32KB) SRAM** for saves, but I have only tested two that I currently own:

- 1080 Snowboarding
- F-Zero X
- Harvest Moon 64
- Legend of Zelda: Ocarina of Time (PAL) ✓ *tested*
- Major League Baseball featuring Ken Griffey Jr.
- Mario Golf (JP) ✓ *tested*
- New Tetris, The
- Ogre Battle 64: Person of Lordly Caliber
- Resident Evil 2
- Super Smash Bros.
- WCW/NWO Revenge
- WWF: Wrestlemania 2000

## NOT Supported

I intended to extend this script to all save types but my DreamDumper64 atleast does not show other save types.  I've tried updating the firmware with no change, so perhaps I have a hardware problem.  So...:
- ✗ EEPROM games (Super Mario 64, Mario Kart 64, etc.)
- ✗ FlashRAM games (Paper Mario, Majora's Mask, etc.)

## Requirements

- Python 3
- A DreamDumper64 cart reader
- A SummerCart 64 flashcart
- N64 cartridges with SRAM saves

## Usage

```bash
python3 n64_sram_converter.py <input.ram|input.fla> [output.sav]
```

### Examples

```bash
# Basic usage - auto-generates output filename
python3 n64_sram_converter.py ROMF.ram

# Specify output filename
python3 n64_sram_converter.py ROM.fla "Ocarina of Time.sav"
```

## Step-by-Step Guide

1. **Dump your cartridge save with DreamDumper64:**
   - Insert cartridge into DreamDumper64
   - Plug into computer - it mounts as "DreamDump64" drive
   - Copy `ROMF.ram` or `ROM.fla` file to your computer

2. **Convert the save:**
   ```bash
   python3 n64_sram_converter_universal.py ROMF.ram
   ```

3. **Rename the output file:**
   - The output `.sav` file MUST match your ROM filename exactly
   - Example: If ROM is `Legend of Zelda, The - Ocarina of Time (USA).n64`
   - Save must be: `Legend of Zelda, The - Ocarina of Time (USA).sav`

4. **Copy to SummerCart 64:**
   - Place the `.sav` file in the `/saves` folder on your SD card
   - Or place it in the same directory as the ROM

5. **Load the game on your SummerCart 64 - your save should work!**

## How It Works

The DreamDumper64 creates 128KB (131,072 byte) files for all save types. For SRAM games:
- The actual 32KB save data is in bytes 0-32,767 (the first 32KB)
- The script extracts this data without modification
- No byte swapping is performed (SummerCart 64 uses raw cartridge format)

## Tested Hardware

- **Cart Reader:** DreamDumper64 (AliExpress version, firmware unknown but attempted to flash to drmdmp64_mass_110224... unsure if successful)
- **Flashcart:** SummerCart 64
- **Tested Games:** 
  - The Legend of Zelda: Ocarina of Time (Europe)
  - Mario Golf 64 (Japan)

## Known Issues

- Game detection only works for Ocarina of Time and Mario Golf - the games I own (others should convert fine but aren't identified by name)


## License

MIT License - feel free to use, modify, and distribute.

## Credits

- Script created by Claude (Anthropic AI)
- DreamDumper64 firmware by [nopjne](https://github.com/nopjne/drmdmp64_mass)
- SummerCart 64 by [Polprzewodnikowy](https://github.com/Polprzewodnikowy/SummerCart64)
