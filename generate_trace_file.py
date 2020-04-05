
final = {"eu": {"p": 0.0, "r": 0.0, "f1": 0.0}, "ca": {"p": 0.0, "r": 0.0, "f1": 0.0},
         "gl": {"p": 0.0, "r": 0.0, "f1": 0.0}, "es": {"p": 0.0, "r": 0.0, "f1": 0.0},
         "en": {"p": 0.0, "r": 0.0, "f1": 0.0}, "pt": {"p": 0.0, "r": 0.0, "f1": 0.0}}
c = {"eu": {"correct": 0, "wrong": 0, "FP": 0}, "ca": {"correct": 0, "wrong": 0, "FP": 0}, "gl": {"correct": 0, "wrong": 0, "FP": 0},
     "es": {"correct": 0, "wrong": 0, "FP": 0}, "en": {"correct": 0, "wrong": 0, "FP": 0}, "pt": {"correct": 0, "wrong": 0, "FP": 0}}


def parseFile(file):
    f = open(file, "r", encoding="utf-8")
    text = f.read()
    f.close()
    return text


def genetate_trace_file(trace_file, result):
    if result["isCorrect"]:
        is_correct = "correct"
    else:
        is_correct = "wrong"
    s = str(result["id"]) + "  " + str(result["lang"]) + "  " + str(result["score"]) + "  " + str(result["guess"]) + "  " + is_correct
    trace_file.write(s + "\n")


def count_result(result):
    if result["isCorrect"]:
        c[result["lang"]]["correct"] += 1
    else:
        c[result["lang"]]["wrong"] += 1
        c[result["guess"]]["FP"] += 1


def generate_eval(v_type, model_type, smooth_value, accuracy, tweet_number):
    eval_file = open("eval_" + str(v_type) + "_" + str(model_type) + "_" + str(smooth_value) + ".txt", "w",
                     encoding="utf-8")
    total = 0
    weighted_total = 0
    eval_file.write(str(accuracy) + "\n")
    p = ""
    r = ""
    f1 = ""
    for lang in final:
        denominator = c[lang].get("correct") + c[lang].get("FP")
        if denominator == 0:
            final[lang]["p"] = 0.0
        else:
            final[lang]["p"] = c[lang].get("correct") / denominator
        p = p + str(final[lang]["p"]) + "  "

        denominator = c[lang].get("correct") + c[lang].get("wrong")
        if denominator == 0:
            final[lang]["r"] = 0.0
        else:
            final[lang]["r"] = c[lang].get("correct") / denominator
        r = r + str(final[lang]["r"]) + "  "

        denominator = final[lang].get("p") + final[lang].get("r")
        if denominator == 0:
            final[lang]["f1"] = 0.0
        else:
            final[lang]["f1"] = 2 * final[lang].get("p") * final[lang].get("r") / denominator
        f1 = f1 + str(final[lang]["f1"]) + "  "
        weighted_total += final[lang].get("f1") * (c[lang].get("correct")+c[lang].get("wrong"))
        total += final[lang].get("f1")
    eval_file.write(p + "\n" + r + "\n" + f1 + "\n")
    f1_macro = total / len(final)
    f1_weighted = weighted_total / tweet_number
    eval_file.write(str(f1_macro) + "  " + str(f1_weighted))
    eval_file.close()

