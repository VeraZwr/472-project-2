import helper
import numpy as ny

unigram = dict()


def generate_unigram(vocabulary, v_type, smooth_value):
    for lang in vocabulary:
        unigram[lang] = dict()

        total_count = 0

        for twit in vocabulary[lang]:
            for character in twit:
                if character is not '*':
                    total_count += 1

                    if unigram.get(lang).get(character) is None:
                        unigram[lang][character] = {"count": 1, "probability": 0}
                    else:
                        unigram[lang][character]['count'] = unigram[lang][character]["count"] + 1

        if v_type == 0:
            for i in range(97, 123):

                denominator = (total_count + 26 * smooth_value)

                if unigram[lang][chr(i)] is None:
                    unigram[lang][chr(i)] = {"count": smooth_value, "probability": smooth_value / denominator}
                else:
                    unigram[lang][chr(i)]['probability'] = (smooth_value + unigram[lang][chr(i)]["count"]) / denominator

        elif v_type == 1:
            for i in range(65, 123):
                if 90 < i < 97:
                    continue
                denominator = (total_count + 52 * smooth_value)

                if unigram[lang][chr(i)] is None:
                    unigram[lang][chr(i)] = {"count": smooth_value, "probability": smooth_value / denominator}
                else:
                    unigram[lang][chr(i)]['probability'] = (smooth_value + unigram[lang][chr(i)]["count"]) / denominator

        elif v_type == 2:
            denominator = (total_count + helper.ALPHA_CONSTANT * smooth_value)

            unigram[lang]['not found'] = {"count": smooth_value, "probability": smooth_value / denominator}

            for char in unigram[lang]:
                unigram[lang][char]["probability"] = unigram[lang][char]['count'] / denominator

    return unigram


def make_guess(tweet, unigram):
    max = None
    guess = ''

    for lang in unigram:
        temp = 0
        for char in tweet['text']:
            if char != '*':
                if unigram[lang].get(char) is None:
                    temp = temp + ny.log(unigram[lang]['not found']['probability'])
                else:
                    temp = temp + ny.log(unigram[lang][char]['probability'])

        if max is None or temp > max:
            max = temp
            guess = lang

    return {"id": tweet['id'], 'lang': tweet['lang'], 'guess': guess, 'score': max, 'isCorrect': tweet['lang'] == guess}
