import csv
import sys
from cassis import *
import spacy
import os

if ((sys.argv[1][-4:] != ".xml") and (sys.argv[2][-4:] != ".csv")):
    print("Please use .xml and .jsonl")
    sys.exit(1)
else:
    xmlfile = sys.argv[1]
    csvfile = sys.argv[2]

if len(sys.argv) > 4:
    print("Please only use 3 command line arguement")
    sys.exit(1)

if len(sys.argv) == 3:
    output = os.getcwd()
else:
    output = sys.argv[3]




def main(xmlfile, csvfile, output):
    
    
    with open(xmlfile, "rb") as f:
        ts = load_typesystem(f)

    SENTENCE_TYPE = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence"
    TOKEN_TYPE = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token"
    Sentence = ts.get_type(SENTENCE_TYPE)
    Token = ts.get_type(TOKEN_TYPE)
    
    nlp = spacy.load("en_core_web_sm")
    csv.field_size_limit(sys.maxsize)
    
    with open(csvfile, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)
        counter = 0
        for row in reader:
            text = row[4]
            
            cas = Cas(typesystem=ts)
            
            doc = nlp(text)
            cas.sofa_string = text
            
            for sentence in doc.sents:
                cas_sentence = Sentence(begin=sentence.start_char, end=sentence.end_char)
                cas.add_annotation(cas_sentence)

            for token in doc:
                cas_token = Token(begin=token.idx, end=token.idx + len(token))
                cas.add_annotation(cas_token)
            
            cas.to_xmi(f"{output}/text_{counter}.xmi")
            counter += 1
            
    sys.exit(0)
    

if __name__ == "__main__":
    main(xmlfile, csvfile, output)