import json
import re
import glob
from tqdm import tqdm

# British-American spelling patterns
patterns = [
    (r'\b(\w*)our\b', r'\b(\w*)or\b'),     # colour/color
    (r'\b(\w*)re\b', r'\b(\w*)er\b'),      # centre/center
    (r'\b(\w*)ise\b', r'\b(\w*)ize\b'),    # realise/realize
    (r'\b(\w*)ogue\b', r'\b(\w*)og\b'),    # catalogue/catalog
    (r'\b(\w*)ll(\w+)\b', r'\b(\w*)l(\w+)\b')  # travelling/traveling
]

# Extract spelling pairs from PHP files
pairs = []
for file in glob.glob('./Words/AmericanBritish/*.php'):
    all_pairs = re.findall(r"['\"](\w+)['\"]\s*=>\s*['\"](\w+)['\"]", open(file).read())
    for brit_pat, amer_pat in patterns:
        for first, second in all_pairs:
            if re.match(brit_pat, first, re.I) and re.match(amer_pat, second, re.I):
                pairs.append((first, second))
            elif re.match(amer_pat, first, re.I) and re.match(brit_pat, second, re.I):
                pairs.append((second, first))

# Create American-British mapping
mapping = {re.compile(r'\b' + re.escape(american) + r'\b', re.I): british 
           for british, american in pairs}

def normalize(text):
    for regex, british in mapping.items():
        text = regex.sub(british, text)
    return text

# Process JSON file
with open('/home/jovyan/conformer-asr-rnnt/data/common_voice_train.json') as infile, \
     open('test_final.json', 'w') as outfile:
    for line in tqdm(infile, desc="Normalizing"):
        obj = json.loads(line)
        if 'text' in obj:
            obj['text'] = normalize(obj['text'])
        outfile.write(json.dumps(obj, ensure_ascii=False) + '\n')