import re
import sys
import json

def get_text(data):
    text = []
    if type(data) is str or type(data) is list:
        return text
    if 'text' in data.keys():
        return data['text']
    for label in data:
        text += get_text(data[label])
    return text


with open(sys.argv[1], "r") as f:
    data = json.load(f)

band_name = data['Name']
text = "".join(get_text(data))
text = re.sub(r'\[[0-9]+\]', "", text)
text = re.sub(band_name, "[BAND_NAME_PLACEHOLDER]", text)
print(text)
