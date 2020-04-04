

def generate_trigram(vocabulary_list, smooth_value, v_type, bigram):
    trigram = dict()

    for lang in vocabulary_list:
        trigram[lang] = dict()

        for tweet in vocabulary_list[lang]:
            for i in range(0, len(tweet)):
                segment = generate_trigram_segment(tweet, i)

                if segment is not None:
                    if trigram[lang].get(segment) is None:
                        trigram[lang][segment] = {'count': 1, 'probability': 0}
                    else:
                        trigram[lang][segment]['count'] = trigram[lang][segment]['count'] + 1

        for trigram_segment in trigram[lang]:
            if v_type == 0:
                trigram[lang][trigram_segment]['probability'] = (trigram_segment['count'] + smooth_value) / (
                        pow(26, 3) * smooth_value + bigram[lang][trigram_segment[0:2]['count']])

                trigram[lang]['not found'] = {"count": smooth_value,
                                              "probability": smooth_value / pow(26, 3) * smooth_value}

            if v_type == 1:
                trigram[lang][trigram_segment]['probability'] = (trigram_segment['count'] + smooth_value) / (
                        pow(52, 3) * smooth_value + bigram[lang][trigram_segment[0:2]['count']])

                trigram[lang]['not found'] = {"count": smooth_value,
                                              "probability": smooth_value / pow(52, 3) * smooth_value}

            if v_type == 2:
                trigram[lang][trigram_segment]['probability'] = (trigram_segment['count'] + smooth_value) / (
                        pow(116766, 3) * smooth_value + bigram[lang][trigram_segment[0:2]['count']])

                trigram[lang]['not found'] = {"count": smooth_value,
                                              "probability": smooth_value / pow(116766, 3) * smooth_value}

    print(trigram)


def generate_trigram_segment(tweet, index):
    if index >= len(tweet) - 2:
        return None

    for i in range(index, index + 3):
        if tweet[i] == '*':
            return None

    return tweet[index: index + 3]
