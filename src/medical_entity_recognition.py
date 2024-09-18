from functools import reduce
import spacy
sci_nlp = spacy.load('en_ner_bc5cdr_md')

def get_appos_for_ent(ent, docx):
    return [w for w in docx if w.dep_ == 'appos' and w.head == ent.root]

def are_connected_by_conjunction(src_token, dest_token):
    while src_token != src_token.head and dest_token != src_token:
        if src_token.dep_ != 'conj':
            return False
        src_token = src_token.head

    return src_token == dest_token

def expand_list_by_conjunction(filtered_list, candidates):
    connected_diseases = []
    for candidate in candidates:
        flag = False
        for disease in filtered_list:
            if are_connected_by_conjunction(candidate.root, disease.root):
                connected_diseases.append(candidate)
                flag = True
                break
        if flag:
            continue
    return connected_diseases

def extract_diseases(text, validation_data):
    if 'not' in text:
        return []
    
    validation_lambda = eval('lambda mc_ent: ' + ' and '.join([f'{k} == \'{validation_data[k]}\'' for k in validation_data.keys() if validation_data[k] != '*']))

    docx = sci_nlp(text)

    diseases = [ent for ent in docx.ents if ent.label_ == 'DISEASE']

    filtered_list = list(filter(validation_lambda, diseases))

    if len(filtered_list) == 0: # no relevant disease found
        return []

    filtered_list = expand_list_by_conjunction(filtered_list, diseases)

    appos_list = [get_appos_for_ent(ent, docx) for ent in filtered_list]
    appos = reduce(lambda xs, ys: xs + ys, appos_list)

    filtered_diseases = filtered_list + appos

    filtered_diseases = [str(disease) for disease in filtered_diseases]

    return filtered_diseases