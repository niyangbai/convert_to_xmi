import sys
from cassis import *
import json
import spacy

if len(sys.argv) != 3:
    if (sys.argv[1][-4] != ".xml") and (sys.argv[1][-6] != ".jsonl"):
        print("Please use .xml and .jsonl")
    print("Please use .xml and .jsonl")
    sys.exit(1)

def find_nearest(arr, num):
    return min(arr, key=lambda x: abs(x - num))

def main(argv):

    xml = argv[1]
    jsonl = argv[2]

    # Load our type system
    with open(xml, "rb") as f:
        ts = load_typesystem(f)
    cas = Cas(typesystem=ts)

    # Create the CAS
    SENTENCE_TYPE = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence"
    TOKEN_TYPE = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token"
    SERE_TYPE = "webanno.custom.SemanticRelations"
    NER_TYPE = "de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity"

    Sentence = ts.get_type(SENTENCE_TYPE)
    Token = ts.get_type(TOKEN_TYPE)
    SemanticRelations = ts.get_type(SERE_TYPE)
    NamedEntity = ts.get_type(NER_TYPE)

    # Set counter for .xmi file name
    counter = 0

    # Convert .jsonl file to .xmi
    with open(jsonl) as f:
        for row in f:
            data = json.loads(row)
            text = data["text"]

            nlp = spacy.load("en_core_web_sm")
            doc = nlp(text)

            cas.sofa_string = text


            for sentence in doc.sents:
                cas_sentence = Sentence(begin=sentence.start_char, end=sentence.end_char)
                cas.add_annotation(cas_sentence)
                assert sentence.text == cas_sentence.get_covered_text()

            b = []
            e = []
            for token in doc:
                cas_token = Token(begin=token.idx, end=token.idx + len(token))
                cas.add_annotation(cas_token)
                assert token.text == cas_token.get_covered_text()
                b.append(token.idx)
                e.append(token.idx + len(token))

            d = {}
            for entity in data["relations"]:
                head_begin = find_nearest(b, entity["head_span"]["start"])
                head_end = find_nearest(e, entity["head_span"]["end"])
                child_begin = find_nearest(b, entity["child_span"]["start"])
                child_end = find_nearest(e, entity["child_span"]["end"])

                cas_head_entity = NamedEntity(begin=head_begin, end=head_end, value = entity["head_span"]["label"])
                cas_child_entity = NamedEntity(begin=child_begin, end=child_end, value = entity["child_span"]["label"])

                if head_begin not in d.keys():
                    cas.add_annotation(cas_head_entity)
                    d[head_begin] = cas_head_entity
                    goverbor = cas_head_entity
                else:
                    goverbor = d[head_begin]

                if child_begin not in d.keys():
                    cas.add_annotation(cas_child_entity)
                    d[child_begin] = cas_child_entity
                    dependent = cas_child_entity
                else:
                    dependent = d[child_begin]

                cas_relation = SemanticRelations(begin=child_begin, end=child_end, Dependent=dependent, Governor=goverbor, Relation=entity["label"])
                cas.add_annotation(cas_relation)

            counter += 1
            cas.to_xmi(f"line_{counter}.xmi")

    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)