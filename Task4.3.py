

# def normalize_text(text):
#     sentences = text.split('.')
#     # Trim spaces and capitalize the first letter of each sentence
#     capitalized_sentences = [sentence.strip().capitalize() for sentence in sentences if sentence.strip()]
#     last_words = [capitalized_sentences.strip().split()[-1] for capitalized_sentences in capitalized_sentences if capitalized_sentences.strip()]
#     new_sentence = ' '.join(last_words) + '.'
#
#     # Join the sentences back into a single string with a period and space
#     normalized_text = '.\n'.join(capitalized_sentences) + '.' + '\n' + new_sentence.capitalize()
#
#     # replace ' iz ' by ' is '
#     normalized_text = normalized_text.replace(' iz ' , ' is ' )
#     return normalized_text


def capitalized_sentences(text):
    sentences = text.split('.')
    capitalized = [sentence.strip().capitalize() for sentence in sentences if sentence.strip()]
    normalized_text = '.\n'.join(capitalized) + '.'
    return normalized_text

def create_last_word_sentence(text):
    sentences = text.split('.')
    last_words = [sentences.strip().split()[-1] for sentences in sentences if sentences.strip()]
    new_sentence = (' '.join(last_words) + '.').capitalize()
    return new_sentence


def replace_iz(text):
    text = text.replace(' iz ' , ' is ' )
    return text


def count_whitespaces(text):
    whitespaces = 0
    for symbol in text:
        if symbol.isspace():
            whitespaces += 1
    return whitespaces




### usage

hm3 = """
tHis iz your homeWork, copy these Text to variable.



You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""


print('Capitalized text:\n', capitalized_sentences(hm3))
print('Replaced iz to is:\n', replace_iz(hm3))
print('Last word sentence text:\n', create_last_word_sentence(hm3))
print('\n\nMy own calculated value of whitespaces is', count_whitespaces(hm3))

