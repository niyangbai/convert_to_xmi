import sys
import json
import re


if ((sys.argv[1][-4:] != ".txt") and (sys.argv[2][-6:] != ".jsonl")):
    print("Please use .txt and .jsonl")
    sys.exit(1)
else:
    txtfile = sys.argv[1]
    jsonlfile = sys.argv[2]

if len(sys.argv) > 3:
    print("Please only use 3 command line arguement")
    sys.exit(1)


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


def tokens_move(tokens, point):
    for dic in tokens:
        if dic["start"] > point:
            dic["start"] += 1
        if dic["end"] > point:
            dic["end"] += 1
    return(tokens)


def main(txtfile, jsonlfile):
    with open(txtfile, "r") as f:
        words = [line.rstrip() for line in f]

    with open(jsonlfile, "r") as f:
        for row in f:
            data = json.loads(row)

            text = data["text"]
            spans = data["spans"]
            tokens = data["tokens"]
            relations = data["relations"]

            search_result = []
            for word in words:
                search_result += text_search(word, text)

            for e in search_result:
                if (text[e["end"]].isalpha()) and (text[e["end"] + 1].isalpha()):
                    text = text[:e["end"]] + " " + text[e["end"]:]

                    spans = tokens_move(spans, e["end"])
                    tokens = tokens_move(tokens, e["end"])
                    search_result = tokens_move(search_result, e["end"])

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

            with open("cleaned.jsonl", "a") as f:
                f.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    main(txtfile, jsonlfile)