import numpy

import helper
import bigram


def generate_trigram(vocabulary_list, v_type, smooth_value):
    trigram = dict()
    bigramMap = bigram.generate_bigram(vocabulary_list, v_type, smooth_value)

    for lang in vocabulary_list:
        trigram[lang] = dict()

        # calculate count
        for tweet in vocabulary_list[lang]:
            for i in range(0, len(tweet)):
                segment = generate_trigram_segment(tweet, i)

                if segment is not None:
                    if trigram[lang].get(segment) is None:
                        trigram[lang][segment] = {'count': 1, 'probability': 0}
                    else:
                        trigram[lang][segment]['count'] = trigram[lang][segment]['count'] + 1

        # calculate probability
        if v_type == 0:
            for x in range(97, 123):
                for y in range(97, 123):
                    for z in range(97, 123):
                        segment = str(chr(x)) + str(chr(y)) + str(chr(z))
                        denominator = bigramMap[lang][segment[0:2]]["count"] + pow(26, 3) * smooth_value

                        if trigram[lang].get(segment) is None:
                            trigram[lang][segment] = {"count": smooth_value,
                                                      "probability": smooth_value / denominator}
                        else:
                            trigram[lang][segment]['probability'] = (smooth_value + trigram[lang][segment][
                                'count']) / denominator

        if v_type == 1:
            for x in range(65, 123):
                if 90 < x < 97:
                    continue
                for y in range(65, 123):
                    if 90 < y < 97:
                        continue
                    for z in range(65, 123):
                        if 90 < z < 97:
                            continue

                        segment = str(chr(x)) + str(chr(y)) + str(chr(z))
                        denominator = bigramMap[lang][segment[0:2]]["count"] + pow(52, 3) * smooth_value

                        if trigram[lang].get(segment) is None:
                            trigram[lang][segment] = {"count": smooth_value,
                                                      "probability": smooth_value / denominator}
                        else:
                            trigram[lang][segment]['probability'] = (smooth_value + trigram[lang][segment][
                                'count']) / denominator

        if v_type == 2:
            for trigram_segment in trigram[lang]:
                denominator = pow(helper.ALPHA_CONSTANT, 3) * smooth_value + bigramMap[lang][trigram_segment[0:2]]['count']
                trigram[lang][trigram_segment]['probability'] = (trigram[lang][trigram_segment][
                                                                     'count'] + smooth_value) / denominator

            trigram[lang]['not found'] = {"count": smooth_value,
                                          "probability": smooth_value / (smooth_value + pow(helper.ALPHA_CONSTANT,
                                                                                           3) * smooth_value)}

    return trigram


def generate_trigram_segment(tweet, index):
    if index >= len(tweet) - 2:
        return None

    for i in range(index, index + 3):
        if tweet[i] == '*':
            return None

    return tweet[index: index + 3]


def make_guess(tweet, trigramMap):
    arr = []
    for i in range(0, len(tweet['text'])):
        segment = generate_trigram_segment(tweet['text'], i)
        if segment is not None:
            arr.append(segment)

    guess = None
    max = None

    for lang in trigramMap:
        temp = 0

        for tri in arr:
            if trigramMap[lang].get(tri) is None:
                temp = temp + numpy.log(trigramMap[lang]['not found']['probability'])
            else:
                temp = temp + numpy.log(trigramMap[lang][tri]['probability'])

        if max is None or temp > max:
            max = temp
            guess = lang

    return {"id": tweet['id'], 'lang': tweet['lang'], 'score': max, 'guess': guess,  'isCorrect': tweet['lang'] == guess}
