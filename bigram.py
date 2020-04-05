import helper
import unigram
import numpy


# 数一数某种语言的某种字母组合有多少个，比如bigram["en"]["ab"] = 5，就是在英语里，ab这个字母组合出现了5次。
def generate_bigram(vocabulary, v_type, smooth_value):
    bigram = dict()
    unigram_map = unigram.generate_unigram(vocabulary, v_type, smooth_value)

    for lang in vocabulary:
        bigram[lang] = dict()
        for tweet in vocabulary[lang]:
            for i in range(len(tweet) - 1):
                if tweet[i] != '*' and tweet[i + 1] != '*':
                    combination = str(tweet[i]) + str(tweet[i + 1])
                    if bigram[lang].get(combination) is None:
                        bigram[lang][combination] = {"count": 1, "probability": 0}
                    else:
                        bigram[lang][combination]["count"] = bigram[lang][combination]["count"] + 1

        if v_type == 0:
            for i in range(97, 123):
                for j in range(97, 123):
                    denominator = unigram_map[lang][chr(i)]["count"] + 26 * 26 * smooth_value
                    combination = str(chr(i)) + str(chr(j))
                    if bigram[lang].get(combination) is None:
                        bigram[lang][combination] = {"count": smooth_value, "probability": smooth_value / denominator}
                    else:
                        bigram[lang][combination]['probability'] = (smooth_value + bigram[lang][combination][
                            'count']) / denominator

        if v_type == 1:
            for i in range(65, 123):
                if 90 < i < 97:
                    continue
                for j in range(65, 123):
                    if 90 < j < 97:
                        continue
                    denominator = unigram_map[lang][chr(i)]["count"] + 52 * 52 * smooth_value
                    combination = str(chr(i)) + str(chr(j))
                    if bigram[lang].get(combination) is None:
                        bigram[lang][combination] = {"count": smooth_value, "probability": smooth_value / denominator}
                    else:
                        bigram[lang][combination]['probability'] = (smooth_value + bigram[lang][combination][
                            'count']) / denominator

        if v_type == 2:
            denominator = smooth_value + pow(helper.ALPHA_CONSTANT, 2) * smooth_value
            bigram[lang]['not found'] = {"count": smooth_value, "probability": smooth_value / denominator}

            for combination in bigram[lang]:
                nominator = smooth_value + bigram[lang][combination]['count']
                first_char = combination[0]
                denominator = unigram_map[lang][first_char]["count"] + pow(helper.ALPHA_CONSTANT, 2) * smooth_value

                bigram[lang][combination]["probability"] = nominator / denominator

    return bigram


def generate_segments(tweet):
    arr = []

    for i in range(len(tweet) - 1):
        if tweet[i] != '*' and tweet[i + 1] != '*':
            arr.append(str(tweet[i]) + str(tweet[i + 1]))

    return arr


def make_guess(tweet, bigram):
    arr = generate_segments(tweet['text'])

    max = None
    guess = ''

    for lang in bigram:
        temp = 0
        for bi in arr:
            if bigram[lang].get(bi) is None:
                temp = temp + numpy.log(bigram[lang]['not found']['probability'])
            else:
                temp = temp + numpy.log(bigram[lang][bi]['probability'])

        if max is None or temp > max:
            max = temp
            guess = lang

    return {"id": tweet['id'], 'lang': tweet['lang'],'score': max,  'guess': guess, 'isCorrect': tweet['lang'] == guess}
