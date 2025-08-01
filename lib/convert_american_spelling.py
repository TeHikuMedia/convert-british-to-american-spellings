import json
import re
import glob
from tqdm import tqdm

# Extract and filter spelling pairs from PHP files
patterns = {
    '-our vs. -or': (r'\b(\w+)our\b', r'\b(\w+)or\b'),
    '-re vs. -er': (r'\b(\w+)re\b', r'\b(\w+)er\b'),
    '-ise vs. -ize': (r'\b(\w+)ise\b', r'\b(\w+)ize\b'),
    '-ogue vs. -og': (r'\b(\w+)ogue\b', r'\b(\w+)og\b'),
    '-ll- vs. -l-': (r'\b(\w+)ll(\w+)\b', r'\b(\w+)l(\w+)\b')
}

pairs = []
for file in glob.glob('./Words/AmericanBritish/*.php'):
    with open(file, 'r') as f:
        all_pairs = re.findall(r"['\"](\w+)['\"]\s*=>\s*['\"](\w+)['\"]", f.read())
        
    # Filter pairs by patterns
    for british_pat, american_pat in patterns.values():
        pairs.extend([pair for pair in all_pairs 
                     if re.match(british_pat, pair[0]) and re.match(american_pat, pair[1])])

# Create regex mapping
mapping = {re.compile(r'\b' + re.escape(british) + r'\b'): american 
           for british, american in pairs}

def normalize_text(text):
    for regex, american in mapping.items():
        text = regex.sub(american, text)
    return text

# Process JSON file
input_file = '/home/jovyan/conformer-asr-rnnt/data/common_voice_train.json'
output_file = 'test.json'

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in tqdm(infile, desc="Normalizing"):
        obj = json.loads(line)
        if 'text' in obj:
            obj['text'] = normalize_text(obj['text'])
        outfile.write(json.dumps(obj, ensure_ascii=False) + '\n')