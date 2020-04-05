import re
import unigram
import bigram
import trigram
import helper

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


def run_model(training_path, test_path, v_type, model_type, smooth_value):
    trace_file = open("trace_" + str(v_type) + "_" + str(model_type) + "_" + str(smooth_value) + ".txt", "w", encoding ="utf-8")
    eval_file = open("eval_" + str(v_type) + "_" + str(model_type) + "_" + str(smooth_value) + ".txt", "w",
                      encoding="utf-8")
    isCorrect = ""
    generate_v(parseFile(training_path), v_type)

    tweets = helper.clean(v_type, test_path)

    total = 0
    correct = 0

    if model_type == 1:

        unigramMap = unigram.generate_unigram(v0, v_type, smooth_value)

        for tweet in tweets:
            result = unigram.make_guess(tweet, unigramMap)
            total += 1
            if result['isCorrect']:
                correct += 1

    elif model_type == 2:
        bigramMap = bigram.generate_bigram(v0, v_type, smooth_value)

        for tweet in tweets:
            result = bigram.make_guess(tweet, bigramMap)
            total += 1
            if result['isCorrect']:
                correct += 1


    elif model_type == 3:
        trigramMap = trigram.generate_trigram(v0, v_type, smooth_value)

        for tweet in tweets:
            result = trigram.make_guess(tweet, trigramMap)
            total += 1
            if result['isCorrect']:
                correct += 1

    print('total: ', total)
    print(correct / total)


run_model("./training-tweets.txt", "./test-tweets-given.txt", 2, 3, 0.00000000000001)
