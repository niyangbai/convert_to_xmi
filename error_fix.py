import re

word = "startup"
txt = "A startupor startupor startupor start-up is a, startupor startups face high uncertainty and have high rates of failure."

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


spans = [{'start': 6, 'end': 12}, {'start': 15, 'end': 17}]

search_result = text_search(word, txt)
plus = 0
for e in search_result:
    if (txt[e["end"] + plus].isalpha()) and (txt[e["end"] + plus + 1].isalpha()):
        txt = txt[:e["end"] + plus] + " " + txt[e["end"] + plus:]
        plus += 1

    for dic in spans:
        if dic["start"] > e["end"]:
            dic["start"] += 1
        if dic["end"] > e["end"]:
            dic["end"] += 1