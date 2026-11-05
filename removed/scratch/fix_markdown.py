import re
import sys
from pathlib import Path

def clean_markdown(file_path: Path):
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    # Pass 1: Handle MD010 (hard tabs), MD009 (trailing whitespace), MD040 (fence language), and MD050 (strong style)
    processed_lines = []
    in_code_block = False
    
    for line in lines:
        # MD010: Convert hard tabs to 4 spaces
        line = line.replace('\t', '    ')
        
        # MD009: Strip trailing whitespace
        stripped = line.rstrip()
        
        # Track fenced code blocks
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            
            # MD040: Fenced code blocks should have a language specified
            if in_code_block and stripped == "```":
                stripped = "```text"
                
        # MD050: Convert bold asterisks **text** to underscores __text__ if not in code block
        if not in_code_block:
            stripped = re.sub(r'\*\*(.*?)\*\*', r'__\1__', stripped)
            
        processed_lines.append(stripped)

    # Pass 2: Handle MD012 (multiple blanks), MD022 (headings), MD031 (fences), MD032 (list surrounding)
    final_lines = []
    in_code_block = False
    
    def is_list_item(text: str) -> bool:
        trimmed = text.strip()
        if not trimmed:
            return False
        # Unordered list marker
        if trimmed.startswith(('* ', '- ', '+ ')):
            return True
        # Ordered list marker
        if re.match(r'^\d+\.\s', trimmed):
            return True
        return False

    for idx, line in enumerate(processed_lines):
        # Track code block
        if line.startswith("```"):
            in_code_block = not in_code_block
            
            # MD031: Ensure blank line before code block fence
            if final_lines and final_lines[-1].strip() != "":
                final_lines.append("")
                
            final_lines.append(line)
            
            # MD031: Ensure blank line after code block fence
            if not in_code_block and idx + 1 < len(processed_lines):
                next_line = processed_lines[idx + 1]
                if next_line.strip() != "":
                    final_lines.append("")
            continue
            
        if in_code_block:
            final_lines.append(line)
            continue
            
        # MD012: Squash consecutive blank lines (except in code blocks)
        if line.strip() == "":
            if final_lines and final_lines[-1].strip() == "":
                continue # Skip duplicate blank lines
            final_lines.append(line)
            continue
            
        # MD022: Headings should be surrounded by blank lines
        is_heading = line.startswith("#") and re.match(r"^#{1,6}\s+", line)
        if is_heading:
            # Ensure blank line before heading
            if final_lines and final_lines[-1].strip() != "":
                final_lines.append("")
                
            final_lines.append(line)
            
            # Ensure blank line after heading
            if idx + 1 < len(processed_lines):
                next_line = processed_lines[idx + 1]
                if next_line.strip() != "":
                    final_lines.append("")
            continue
            
        # MD032: Lists should be surrounded by blank lines
        if is_list_item(line):
            # Ensure blank line before list starts if previous line is not a list and not empty
            if final_lines and final_lines[-1].strip() != "" and not is_list_item(final_lines[-1]):
                final_lines.append("")
                
            # MD030: Fix multiple spaces after list marker to exactly 1 space
            list_match = re.match(r"^(\s*)([\*\-\+]|\d+\.)(\s{2,})(.*)$", line)
            if list_match:
                indent, marker, spaces, rest = list_match.groups()
                line = f"{indent}{marker} {rest}"
                
            final_lines.append(line)
            
            # Ensure blank line after list ends if next line is not a list and not empty
            if idx + 1 < len(processed_lines):
                next_line = processed_lines[idx + 1]
                if next_line.strip() != "" and not is_list_item(next_line):
                    final_lines.append("")
            continue
            
        final_lines.append(line)

    # Re-assemble and write back
    new_content = "\n".join(final_lines)
    # MD047: Ensure single trailing newline
    new_content = new_content.rstrip() + "\n"
        
    file_path.write_text(new_content, encoding="utf-8")
    print(f"[SUCCESS] Successfully cleaned markdown: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        clean_markdown(Path(sys.argv[1]))
    else:
        print("Usage: python fix_markdown.py <path_to_md_file>")
