#!/usr/bin/env python3
"""
N64 SRAM Save Converter - DreamDumper64 to SummerCart 64
Converter for 256 Kilobits (32,768 bytes) SRAM games
"""

import sys
from pathlib import Path


def detect_game_from_save(data):
    """Try to identify the game from save data markers."""
    # Only include markers that have been confirmed through testing
    markers = {
        b'ZELDAZ': 'The Legend of Zelda: Ocarina of Time',
        b'\x12\x34\x56\x78': 'Mario Golf 64',  # Confirmed: starts with these bytes
    }
    
    for marker, game_name in markers.items():
        if marker in data[:1024]:  # Check first 1KB
            return game_name
    return None


def convert_sram_save(input_file, output_file=None):
    """
    Convert a DreamDumper64 SRAM dump to SummerCart 64 format.
    
    The DreamDumper64 creates 128KB files. For SRAM games (32KB saves),
    the save data is in the FIRST 32KB of the file.
    SummerCart 64 uses the raw cartridge format.
    
    Supports all N64 games that use SRAM but only tested on two cartridges so far.
    
    Args:
        input_file: Path to input .ram or .fla file (128KB)
        output_file: Path to output .sav file (optional, will auto-generate if not provided)
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"Error: Input file '{input_file}' not found!")
        return False
    
    print(f"Reading: {input_path.name}")
    with open(input_path, 'rb') as f:
        data = f.read()
    
    file_size = len(data)
    print(f"File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
    
    # DreamDumper64 creates 128KB files (131,072 bytes)
    if file_size != 131072:
        print(f"⚠ Warning: Expected 128 KB (131,072 bytes), but got {file_size:,} bytes")
        print("This may not be a DreamDumper64 SRAM dump.")
        # Ask if user wants to continue
        response = input("Continue anyway? (y/n): ").lower()
        if response != 'y':
            return False
    
    # Extract FIRST 32KB (SRAM size)
    sram_size = 0x8000  # 32KB
    
    print(f"\nExtracting first {sram_size:,} bytes (32 KB SRAM data)...")
    save_data = data[0:sram_size]
    
    if len(save_data) != sram_size:
        print(f"Error: Could not extract {sram_size} bytes from file")
        return False
    
    print(f"Extracted: {len(save_data):,} bytes ({len(save_data) / 1024:.1f} KB)")
    
    # Check if data looks valid (not all zeros)
    non_zero = sum(1 for b in save_data if b != 0)
    data_percentage = (non_zero / len(save_data)) * 100
    
    if non_zero == 0:
        print("⚠ Warning: Save data appears to be empty (all zeros)")
        print("This might be a blank/new save file.")
    else:
        print(f"✓ Save data contains {data_percentage:.1f}% non-zero bytes")
    
    # Try to detect the game
    detected_game = detect_game_from_save(save_data)
    if detected_game:
        print(f"✓ Detected: {detected_game}")
    
    # Determine output filename
    if output_file is None:
        output_file = input_path.with_suffix('.sav')
    else:
        output_file = Path(output_file)
    
    # Write output file
    print(f"\nWriting: {output_file.name}")
    with open(output_file, 'wb') as f:
        f.write(save_data)
    
    print(f"\n{'='*60}")
    print(f"✓ Conversion complete!")
    print(f"{'='*60}")
    print(f"Output file: {output_file}")
    print(f"Size: {len(save_data):,} bytes ({len(save_data) / 1024:.1f} KB)")
    print(f"\n{'='*60}")
    print("NEXT STEPS:")
    print(f"{'='*60}")
    print("1. Rename the .sav file to EXACTLY match your ROM filename:")
    print("   - If ROM is: 'Mario Golf 64 (Japan).n64'")
    print("   - Save must be: 'Mario Golf 64 (Japan).sav'")
    print("   - Case, spaces, and special characters must match exactly!")
    print()
    print("2. Place the .sav file on your SD card:")
    print("   - In /saves folder (recommended)")
    print("   - OR in the same directory as the ROM")
    print()
    print("3. Insert SD card into SummerCart 64 and load the game")
    print()
    print("NOTE: DreamDumper64 can only dump SRAM games (32KB saves).")
    print("It cannot dump EEPROM or FlashRAM games.")
    print(f"{'='*60}")
    
    return True


def main():
    print("=" * 60)
    print("N64 SRAM Save Converter")
    print("DreamDumper64 → SummerCart 64 format")
    print("=" * 60)
    print()
    
    if len(sys.argv) < 2:
        print("Converts N64 SRAM save files from DreamDumper64 to SummerCart 64")
        print()
        print("Usage: python3 n64_sram_converter.py <input.ram|input.fla> [output.sav]")
        print()
        print("Examples:")
        print("  python3 n64_sram_converter.py ROMF.ram")
        print("  python3 n64_sram_converter.py ROM.fla 'Mario Golf 64.sav'")
        print()
        print("Probably supported games (SRAM 32KB saves only):")
        print("  ✓ 1080 Snowboarding")
        print("  ✓ F-Zero X")
        print("  ✓ Harvest Moon 64")
        print("  ✓ Legend of Zelda: Ocarina of Time, The - tested")
        print("  ✓ Major League Baseball featuring Ken Griffey Jr.")
        print("  ✓ Mario Golf - tested")
        print("  ✓ New Tetris, The")
        print("  ✓ Ogre Battle 64: Person of Lordly Caliber")
        print("  ✓ Pocket Monsters Stadium (JPN)")
        print("  ✓ Resident Evil 2")
        print("  ✓ Super Smash Bros.")
        print("  ✓ WCW/NWO Revenge")
        print("  ✓ WWF: Wrestlemania 2000")
        print()
        print("NOT supported... my DreamDumper64 bought from AliExpress does not see other save types... hardware problem?:")
        print("  ✗ EEPROM games (Super Mario 64, Mario Kart 64, etc.)")
        print("  ✗ FlashRAM games (Paper Mario, Majora's Mask, etc.)")
        print()
        print("What this script does:")
        print("  1. Extracts first 32KB from 128KB DreamDumper64 file")
        print("  2. Preserves raw cartridge format (no byte swapping)")
        print("  3. Creates a .sav file ready for SummerCart 64")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = convert_sram_save(input_file, output_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
