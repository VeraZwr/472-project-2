import re

ALPHA_CONSTANT = 116766
emojis = "".join(set(
    "🎿🏂💦🍍🎾🍻🍭🔦🏃✨🌴🕕🕡🕖🕢⛄🐺🏊🎳🎊📖🐼📝👰🔐🐣✈️🍃🍫🐌🐢❗🍓🌴⛅️☁💤🐍🔴⚪🐶🐻😷💏🐸👻🎇🎊🌽🎉🆙🏀🐭🎀👳🐭😿🍓🎧🎊🎁💝👭💁👗🎽👖🔝👦👉👊👈💑️💗🌜❄️😖🚀👒👣🐞🍯🍀🌚🎭📚🌑 🌒 🌓 🌔 🌕 🌖 🌗 🌘 🌑👆👟🙆🚤⚓🍛🍷💓💞💘💎🎈👽😡💃🚨🏠😤😩🔪👋🌀🏁👴😲😐👸💅🎀🙆🙅💁🙋💆👑👯💄🎶💐👎💀💂🎂☀📲😴💋🙏❤😳🔥🍔🍟🍷🍰😘◼️😋😕😂👑😘👌😊✌️🎉🎈🎊😩😩😴😤😣🌝💚😎☔🌊😰🙌🔮💖😞😂🏊😢💤😄😳😁🍞🕚😏😍🐶💕👪😜👠😝🌆🌃🐽💪🚺👉👨🙈🙉🙊😚🔫😧🎶😵⌚🎹🎸😷💩🐍🐜👀👊🌿😶😴👺😸😳😌😈😆🔒👧🌷🌹🌻🌺⚽😩"))


def clean(v, path):
    formatted_tweet = []

    regex = re.compile('[^a-zA-Z]')
    test_file = open(path, "r", encoding="utf-8")
    text = test_file.read()
    text = remove_noise(text)
    text_lines = text.splitlines()
    for line in text_lines:
        split_content = line.split("\t")

        if len(split_content) == 4:

            tweet = {'id': split_content[0], 'lang': split_content[2], 'emojis': extract_emojis(split_content[3])}
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


def remove_noise(document):
    noise_pattern = re.compile("|".join(["http\S+", "\@\w+", "\#\w+"]))
    clean_text = re.sub(noise_pattern, "", document)
    return clean_text.strip()


def extract_emojis(s):
    arr = []

    for emoji in emojis:
        if s.count(emoji) > 0:
            arr.append(emoji)

    return arr


def generate_emoji_count(text):
    emoji_unigram = dict()

    emoji_unigram['eu'] = dict()
    emoji_unigram['ca'] = dict()
    emoji_unigram['gl'] = dict()
    emoji_unigram['es'] = dict()
    emoji_unigram['en'] = dict()
    emoji_unigram['pt'] = dict()

    text_list = text.splitlines()
    for text_line in text_list:
        content = text_line.split("\t")
        if len(content) == 4:
            for emoji in extract_emojis(content[3]):

                if emoji in emoji_unigram[content[2]]:
                    emoji_unigram[content[2]][emoji]['count'] = emoji_unigram[content[2]][emoji]['count'] + 1
                else:
                    emoji_unigram[content[2]][emoji] = {'count': 1}

    return emoji_unigram
