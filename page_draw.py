# This function takes text and splits it intp line that will fit within an e reader screen 
def page_prep(text, max_char, breakpoint) -> [str]:
    
    words = text.split()
    lines = []
    current_line = words[0]
    
    for word in words[1:]:
        if len(word) > max_char:
            if current_line:
                lines.append(current_line)
                current_line = ""
            while len(word) > max_char:
                lines.append(word[:max_char-1] + "-")
                word = word[max_char-1:]
            current_line = word
        elif len(current_line + word) + 1 > max_char or len(current_line) >= breakpoint:
            lines.append(current_line)
            current_line = word
        else:
            current_line += ' ' + word
    
    if current_line:
        lines.append(current_line)
    
    return lines

text = """If you are still wondering how to get free PDF EPUB of book The Schopenhauer Cure by Irvin D. Yalom. Click on below buttons to start Download The Schopenhauer Cure by Irvin D. Yalom PDF EPUB without registration. This is free download The Schopenhauer Cure by Irvin D. Yalom complete book soft copy."""
lines = page_prep(text, 50, 55) 
for line in lines:
    print(line)

