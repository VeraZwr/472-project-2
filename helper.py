import re

ALPHA_CONSTANT = 116766


def clean(v, path):
    formatted_tweet = []

    regex = re.compile('[^a-zA-Z]')
    test_file = open(path, "r", encoding="utf-8")
    text = test_file.read()
    text_lines = text.splitlines()
    for line in text_lines:
        split_content = line.split("\t")

        if len(split_content) == 4:
            tweet = {'id': split_content[0], 'lang': split_content[2]}
            if v == 0:
                tweet['text'] = (regex.sub('*', split_content[3])).lower()
            elif v == 1:

                tweet['text'] = regex.sub('*', split_content[3])
            elif v == 2:
                chars = [char for char in split_content[3]]
                for i in range(len(chars)):
                    if not chars[i].isalpha():
                        chars[i] = '*'
                tweet['text'] = ''.join([str(elem) for elem in chars])
        formatted_tweet.append(tweet)
    return formatted_tweet
