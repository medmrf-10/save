import json, re

def clean_json(text):
    # This regex handles comments but respects strings
    # However a simpler way is to find URLs and ignore them, or precisely match strings
    out = []
    in_string = False
    escape = False
    i = 0
    while i < len(text):
        c = text[i]
        if not in_string:
            if c == '/' and i + 1 < len(text) and text[i+1] == '/':
                # skip until newline
                while i < len(text) and text[i] != '\n':
                    i += 1
                continue
            elif c == '/' and i + 1 < len(text) and text[i+1] == '*':
                # skip until /*
                i += 2
                while i < len(text) and not (text[i-1] == '*' and text[i] == '/'):
                    i += 1
                i += 1
                continue
            elif c == '"':
                in_string = True
        else:
            if escape:
                escape = False
            elif c == '\\':
                escape = True
            elif c == '"':
                in_string = False
        out.append(c)
        i += 1
    
    cleaned = ''.join(out)
    # remove trailing commas
    cleaned = re.sub(r',\s*}', '}', cleaned)
    cleaned = re.sub(r',\s*\]', ']', cleaned)
    return cleaned

with open('default.json', 'r') as f:    
    content = f.read()

try:
    data = json.loads(clean_json(content))
    lines = [json.dumps({k: v}) for k, v in data.items()]
    chunk_size = 1000
    for i in range(0, len(lines), chunk_size):
        chunk = lines[i:i+chunk_size]
        with open(f'default_part_{i//chunk_size + 1:02d}.jsonl', 'w') as out:
            out.write('\n'.join(chunk) + '\n')
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()

