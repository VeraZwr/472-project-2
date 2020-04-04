import re
import unigram
import bigram
import trigram

v0 = {"eu": [], "ca": [], "gl": [], "es": [], "en": [], "pt": []}


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


generate_v(parseFile("./training-tweets.txt"), 0)
# unigram.generate_unigram(v0, 0, 0.1)
bigram_model = bigram.generate_bigram(v0, 0, 0.1)


def clean(v):
    clean_text = []
    regex = re.compile('[^a-zA-Z]')
    test_file = open("test-tweets-given.txt", "r", encoding="utf-8")
    text = test_file.read()
    text_lines = text.splitlines()
    for line in text_lines:
        split_content = line.split("\t")
        content = ""
        if len(split_content) == 4:
            if v == 0:
                content = (regex.sub('*', split_content[3])).lower()
            elif v == 1:
                content = regex.sub('*', split_content[3])
            elif v == 2:
                chars = [char for char in split_content[3]]
                for i in range(len(chars)):
                    if not chars[i].isalpha():
                        chars[i] = '*'
                content = ''.join([str(elem) for elem in chars])
        clean_text.append(content)
    return clean_text


# trace_file = open("trace_" + str(v) + "_" + str(n) + "_" + str(d) + ".txt", "w")
