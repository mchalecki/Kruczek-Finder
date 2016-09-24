from nltk.tokenize import sent_tokenize
import Levenshtein


def search_for_phrase(page, paragraph_original):
    indices = []
    phrase_list = sent_tokenize(paragraph_original)
    process_page(indices, page, paragraph_original, phrase_list)
    return indices


def process_page(indices, page, paragraph_original, phrase_list):
    for i, sentence in enumerate(page):
        end = i + len(phrase_list) + 5
        if end >= len(page):
            end = len(page)

        sentences = []
        for sent in page[i: end]:
            sentences.append(sent.content)
        sentences = ' '.join(sentences)
        ratio = Levenshtein.ratio(str(sentences), str(paragraph_original))
        if ratio > 0.60:
            indices.append((i, page[i: end], ratio))
