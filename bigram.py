import helper
import unigram


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
                bigram[lang][combination]["probability"] = (smooth_value + bigram[lang][combination][
                    'count']) / unigram_map[lang][bigram[lang][combination][0]]["count"] + pow(helper.ALPHA_CONSTANT,
                                                                                               2) * smooth_value

    return bigram
