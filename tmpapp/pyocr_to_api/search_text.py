from nltk.tokenize import sent_tokenize
import Levenshtein


def search_for_phrase(page, paragraph_original):
    indices = []
    process_page(indices, page, paragraph_original)
    return indices


def process_page(indices, page, clause):
    phrase_list = sent_tokenize(clause.postanowienie_wzorca)
    for i, sentence in enumerate(page):
        end = i + len(phrase_list) + 5
        if end >= len(page):
            end = len(page)

        sentences = []
        for sent in page[i: end]:
            sentences.append(sent.content)
        sentences = ' '.join(sentences)
        ratio = Levenshtein.ratio(str(sentences), str(clause.postanowienie_wzorca))
        if ratio > 0.60:
            indices.append((clause, (page[i].position[0], page[end].position[1])))
