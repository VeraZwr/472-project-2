import numpy

import helper
import bigram
import trigram


def make_guess(tweet, bigramMap, trigramMap, emojis_count):
    scores = dict()
    bigram_segments = bigram.generate_segments(tweet['text'])

    trigram_segments = []
    for i in range(0, len(tweet['text'])):
        segment = trigram.generate_trigram_segment(tweet['text'], i)
        if segment is not None:
            trigram_segments.append(segment)

    guess = None
    max = None

    for lang in trigramMap:
        temp = 0

        for tri in trigram_segments:
            if trigramMap[lang].get(tri) is None:
                temp = temp + numpy.log(trigramMap[lang]['not found']['probability'])
            else:
                temp = temp + numpy.log(trigramMap[lang][tri]['probability'])

        scores[lang] = temp

        for bi in bigram_segments:
            if bigramMap[lang].get(bi) is None:
                temp = temp + numpy.log(bigramMap[lang]['not found']['probability'])
            else:
                temp = temp + numpy.log(bigramMap[lang][bi]['probability'])

        scores[lang] = scores[lang]*0.4 + temp*0.6

    for emoji in tweet['emojis']:
        for lang in scores:
            if emoji in emojis_count[lang]:
                scores[lang] += numpy.log(emojis_count[lang][emoji]['count'])

    for lang in scores:
        if max is None or scores[lang] > max:
            max = scores[lang]
            guess = lang

    return {"id": tweet['id'], 'lang': tweet['lang'], 'guess': guess, 'score': max, 'isCorrect': tweet['lang'] == guess}
