import json
import re

with open("words.txt", "r") as f:
    words = [line.rstrip() for line in f]

with open("test.json", "r") as f:
    data = json.load(f)

def text_search(word, txt):
    result = []
    plus = 0
    while True:
        s = re.search(word, txt)
        if s == None:
            break
        else:
            result.append({"start":s.start() + plus, "end":s.end() + plus})
            plus = plus + s.end()
            txt = txt[s.end():]
    return result

text = data["text"]
spans = data["spans"]
tokens = data["tokens"]
relations = data["relations"]

def tokens_move(tokens, point):
    for dic in tokens:
        if dic["start"] > point:
            dic["start"] += 1
        if dic["end"] > point:
            dic["end"] += 1
    return(tokens)


search_result = []
for word in words:
    search_result += text_search(word, text)

print(search_result)

plus = 0
for e in search_result:
    if (text[e["end"] + plus].isalpha()) and (text[e["end"] + plus + 1].isalpha()):
        text = text[:e["end"] + plus] + " " + text[e["end"] + plus:]
        plus += 1

        spans = tokens_move(spans, e["end"])
        tokens = tokens_move(tokens, e["end"])

        for relation in relations:
            
            if relation["head_span"]["start"] > e["end"]:
                relation["head_span"]["start"] += 1
            if relation["head_span"]["end"] > e["end"]:
                relation["head_span"]["end"] += 1

            if relation["child_span"]["start"] > e["end"]:
                relation["child_span"]["start"] += 1
            if relation["child_span"]["end"] > e["end"]:
                relation["child_span"]["end"] += 1

result = {
    "text" : text,
    "spans" : spans,
    "tokens" : tokens,
    "relations" : relations
}

with open("cleaned.json", "w") as f:
    json.dump(result, f)
