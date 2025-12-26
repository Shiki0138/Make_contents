with open('impact_generator.py', 'rb') as f:
    content = f.readlines()
    line_idx = 75 # 0-indexed for line 76
    if line_idx < len(content):
        line = content[line_idx]
        print(f"Line {line_idx + 1} raw: {line}")
        print(f"Line {line_idx + 1} hex: {line.hex()}")
        for char in line:
            print(f"Char: {chr(char)} (Hex: {hex(char)})")
