#!/usr/bin/env python3
"""Extract .NET-related registry keys from system.reg, convert to REGEDIT4, merge with dotnet48.reg"""

import re
import os

WORKDIR = "/home/cas/Documentos/working-dotnet48-pfx"
OUTPUT = "/home/cas/Documentos/dotnet48-installer/package/dotnet48-full.reg"

def is_dotnet_key(key_name):
    """Check if a registry key is .NET related"""
    k = key_name.lower()
    # Direct .NET framework keys
    if re.search(r'microsoft\\\.net', k): return True
    if re.search(r'microsoft\\net\s', k): return True
    # CLR/mscoree COM class registrations
    if re.search(r'classes\\clr', k): return True
    if re.search(r'classes\\clsid\{', k):
        # Only include CLSID entries related to .NET
        return True  # We'll include all CLSIDs since the working prefix has them
    # Fusion,ngen
    if re.search(r'fusion', k): return True
    if re.search(r'ngen', k): return True
    return False

def read_system_reg(path):
    sections = []
    current_section = []
    in_dotnet = False
    
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    
    for line in lines:
        section_match = re.match(r'^\[(.+)\]\s+\d+$', line)
        if section_match:
            if in_dotnet and current_section:
                sections.append(current_section)
            key_name = section_match.group(1)
            in_dotnet = is_dotnet_key(key_name)
            if in_dotnet:
                current_section = [key_name]
            else:
                current_section = []
        elif in_dotnet:
            stripped = line.rstrip('\n\r')
            if stripped:
                current_section.append(stripped)
    
    if in_dotnet and current_section:
        sections.append(current_section)
    return sections

def convert_to_regedit4(sections):
    output = ["REGEDIT4", ""]
    
    for section in sections:
        if not section:
            continue
        key_name = section[0]
        output.append(f"[{key_name}]")
        for entry in section[1:]:
            if entry.startswith('#time='): continue
            if re.match(r'^\d+$', entry): continue
            output.append(entry)
        output.append("")
    
    return output

def merge_reg_files(regedit4_lines, dotnet48_path):
    with open(dotnet48_path, 'r', encoding='utf-8', errors='replace') as f:
        dotnet48 = f.read()
    dotnet48 = re.sub(r'^REGEDIT4\r?\n\r?\n', '', dotnet48)
    
    seen_keys = set()
    result = []
    in_header = True
    
    for line in regedit4_lines:
        if in_header:
            result.append(line)
            if line == '':
                in_header = False
            continue
        key_match = re.match(r'^\[(.+)\]$', line)
        if key_match:
            seen_keys.add(key_match.group(1))
        result.append(line)
    
    current_key = None
    skip_section = False
    for line in dotnet48.split('\n'):
        line = line.rstrip('\r')
        key_match = re.match(r'^\[(.+)\]$', line)
        if key_match:
            current_key = key_match.group(1)
            skip_section = current_key in seen_keys
            if not skip_section:
                result.append(line)
                seen_keys.add(current_key)
        elif not skip_section:
            result.append(line)
    
    return result

def main():
    print("Reading system.reg...")
    sections = read_system_reg(os.path.join(WORKDIR, "system.reg"))
    print(f"Found {len(sections)} .NET-related sections in system.reg")
    
    # Count total lines
    total_lines = sum(len(s) for s in sections)
    print(f"Total lines: {total_lines}")
    
    print("Converting to REGEDIT4 format...")
    regedit4_lines = convert_to_regedit4(sections)
    
    print("Merging with dotnet48.reg...")
    merged = merge_reg_files(regedit4_lines, os.path.join(WORKDIR, "dotnet48.reg"))
    
    print("Writing output...")
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(merged))
    
    total_keys = sum(1 for l in merged if l.startswith('[') and l.endswith(']'))
    total_lines = len(merged)
    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f"Done! {total_keys} keys, {total_lines} lines, {size_kb:.0f} KB -> {OUTPUT}")

if __name__ == "__main__":
    main()
