import sys
import json
import numpy as np
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


def main(txtfile, jsonlfile):
    with open(txtfile, "r") as f:
        words = [line.rstrip() for line in f]

    with open(jsonlfile, "r") as f:
        for row in f:
            data = json.loads(row)

            text = data["text"]
            spans = data["spans"]
            relations = data["relations"]

            search_results = []
            for word in words:
                search_results += text_search(word, text)
            
            for search_result in search_results:
                error_token = []
                for token in data["tokens"]:
                    if (token["start"] == search_result["start"]) and token["end"] != search_result["end"]:
                        error_token.append(token["text"])

                if len(error_token):
                    for error in error_token:
                        key = None
                        for i in data["spans"]:
                            if (text[i["start"]:i["end"]] in error) and (i["label"] == "ORG"):
                                key = text[i["start"]:i["end"]]
                                break
            
                        if key == None:
                            continue

                        word_len = search_result["end"] - search_result["start"]

                        clean = [
                            text[:search_result["start"] + word_len], 
                            text[search_result["start"] + word_len:search_result["start"] + word_len + len(key)],
                            text[search_result["start"] + word_len + len(key):]
                        ]

                        spans.append({
                            "text": text[search_result["start"] + word_len:search_result["start"] + word_len + len(key)],
                            "start": search_result["start"] + word_len,
                            "end": search_result["start"] + word_len + len(key),
                            "label" : "ORG"
                        })

                        if not clean[2][0].isalnum():
                            clean = [clean[0], clean[1] + clean[2]]

                        placeholder = [len(x) for x in clean]
                        check_ponits = list(np.cumsum(placeholder[:-1]))
                        text = " ".join(clean)

                        for check_point in check_ponits:

                            for span in spans:
                                if span["start"] > check_point:
                                    span["start"] += 1
                                if span["end"] > check_point:
                                    span["end"] += 1
                            
                            for relation in relations:
                                if relation["head_span"]["start"] > check_point:
                                    relation["head_span"]["start"] += 1
                                if relation["head_span"]["end"] > check_point:
                                    relation["head_span"]["end"] += 1

                                if relation["child_span"]["start"] > check_point:
                                    relation["child_span"]["start"] += 1
                                if relation["child_span"]["end"] > check_point:
                                    relation["child_span"]["end"] += 1         

            result = {
                "text" : text,
                "spans" : spans,
                "relations" : relations
            }

            with open("cleaned.jsonl", "a") as f:
                f.write(json.dumps(result) + "\n")
            
    sys.exit(0)

if __name__ == "__main__":
    main(txtfile, jsonlfile)