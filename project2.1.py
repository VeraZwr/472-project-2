import re

v0 = {"eu": [], "ca": [], "gl": [], "es": [], "en": [], "pt": []}
unigram = dict()


def parseFile(file):
    f = open(file, "r", encoding="iso8859-2")
    text = f.read()
    f.close()
    return text


def generate_v(text, v_type):
    regex = re.compile('[^a-zA-Z]')
    text_list = text.splitlines()
    for text_line in text_list:
        content = text_line.split("\t")
        if len(content) == 4:
            if v_type == 0:
                v0[content[2]].append((regex.sub('*', content[3])).lower())
            elif v_type == 1:
                v0[content[2]].append((regex.sub('*', content[3])))
            elif v_type == 2:
                content[3] = [char for char in content[3]]
                for i in range(len(content[3])):
                    if not content[3][i].isalpha():
                        content[3][i] = '*'

                v0[content[2]].append(''.join([str(elem) for elem in content[3]]))


def generate_unigram(v_type, smooth_value):
    for lang in v0:
        unigram[lang] = dict()

        total_count = 0

        for twit in v0[lang]:
            for character in twit:
                if character is not '*':
                    total_count += 1

                    if unigram.get(lang).get(character) is None:
                        unigram[lang][character] = {"count": 1, "probability": 0}
                    else:
                        unigram[lang][character]['count'] = unigram[lang][character]["count"] + 1

        if v_type == 0:
            for i in range(97, 123):
                if 90 < i < 97:
                    continue

                denominator = (total_count + 26 * smooth_value)

                if unigram[lang][chr(i)] is None:
                    unigram[lang][chr(i)] = {"count": smooth_value, "probability": smooth_value / denominator}
                else:
                    unigram[lang][chr(i)]['probability'] = (smooth_value + unigram[lang][chr(i)]) / denominator

        elif v_type == 1:
            for i in range(65, 123):
                denominator = (total_count + 52 * smooth_value)

                if unigram[lang][chr(i)] is None:
                    unigram[lang][chr(i)] = {"count": smooth_value, "probability": smooth_value / denominator}
                else:
                    unigram[lang][chr(i)]['probability'] = (smooth_value + unigram[lang][chr(i)]) / denominator

        elif v_type == 2:
            denominator = (total_count + 116766 * smooth_value)

            unigram[lang]['not found'] = {"count": smooth_value, "probability": smooth_value / denominator}

            for char in unigram[lang]:
                unigram[lang][char]["probability"] = unigram[lang][char]['count'] / denominator

    print(unigram)


generate_v(parseFile("./training-tweets.txt"), 2)
generate_unigram(2, 0.1)
