import sys
from cassis import *
import json
import spacy

if len(sys.argv) != 3:
    if ((sys.argv[1][-4] != ".xml") and (sys.argv[2][-6] != ".jsonl")):
        print("Please use .xml and .jsonl")
    print("Please use .xml and .jsonl")
    sys.exit(1)

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

    # Load spacy nlp fro sentences
    nlp = spacy.load("en_core_web_sm")

    # Convert .jsonl file to .xmi
    with open(jsonl) as f:
        for row in f:

            with open(xml, "rb") as f:
                ts = load_typesystem(f)
            cas = Cas(typesystem=ts)
            
            data = json.loads(row)
            text = data["text"]
            
            doc = nlp(text)
            cas.sofa_string = text

            for sentence in doc.sents:
                cas_sentence = Sentence(begin=sentence.start_char, end=sentence.end_char)
                cas.add_annotation(cas_sentence)
                assert sentence.text == cas_sentence.get_covered_text()

            for token in data["tokens"]:
                cas_token = Token(begin=token["start"], end=token["end"])
                cas.add_annotation(cas_token)
                assert token["text"] == cas_token.get_covered_text()

            d = {}
            for entity in data["relations"]:
                cas_head_entity = NamedEntity(begin=entity["head_span"]["start"], end=entity["head_span"]["end"], value = entity["head_span"]["label"])
                cas_child_entity = NamedEntity(begin=entity["child_span"]["start"], end=entity["child_span"]["end"], value = entity["child_span"]["label"])

                if entity["head_span"]["start"] not in d.keys():
                    cas.add_annotation(cas_head_entity)
                    d[entity["head_span"]["start"]] = cas_head_entity
                    governor = cas_head_entity
                else:
                    governor = d[entity["head_span"]["start"]]

                if entity["child_span"]["start"] not in d.keys():
                    cas.add_annotation(cas_child_entity)
                    d[entity["child_span"]["start"]] = cas_child_entity
                    dependent = cas_child_entity
                else:
                    dependent = d[entity["child_span"]["start"]]

                cas_relation = SemanticRelations(begin=entity["child_span"]["start"], end=entity["child_span"]["end"], Dependent=dependent, Governor=governor, Relation=entity["label"])
                cas.add_annotation(cas_relation)

            counter += 1
            cas.to_xmi(f"line_{counter}.xmi")

    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)