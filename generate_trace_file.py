
final = {"eu": {"p":0, "r": 0, "f1": 0}, "ca": {"p":0, "r": 0, "f1": 0}, "gl": {"p":0, "r": 0, "f1": 0},
         "es": {"p":0, "r": 0, "f1": 0}, "en": {"p":0, "r": 0, "f1": 0}, "pt": {"p":0, "r": 0, "f1": 0}}
c = {"eu": {"correct": 0, "wrong": 0, "FP": 0}, "ca": {"correct": 0, "wrong": 0, "FP": 0}, "gl": {"correct": 0, "wrong": 0, "FP": 0},
     "es": {"correct": 0, "wrong": 0, "FP": 0}, "en": {"correct": 0, "wrong": 0, "FP": 0}, "pt": {"correct": 0, "wrong": 0, "FP": 0}}

def parseFile(file):
    f = open(file, "r", encoding="utf-8")
    text = f.read()
    f.close()
    return text

def genetate_trace_file(trace_file, result):
    if result["isCorrect"]:
        isCorrect = "correct"
    else:
        isCorrect = "wrong"
    s = str(result["id"]) + "  " + str(result["lang"]) + "  " + str(result["score"]) + "  " + str(result["guess"]) + "  " + isCorrect
    trace_file.write(s + "\n")

def count_result(result):
    if result["isCorrect"]:
        c[result["lang"]]["correct"] = 1
    else:
        c[result["lang"]]["wrong"] = 1
        c[result["guess"]]["FP"] = 1


def generate_eval(eval_file, c, result):
    total = 0
    weighted_total = 0
    for key in final:
        final[key]["p"] = c[key].get("correct")/(c[key].get("correct") + c[key].get("FP"))
        final[key]["r"] = c[key].get("correct")/(c[key].get("correct")+c[key].get("wrong"))
        final[key]["f1"] = 2 * final[key].get("p") * final[key].get("r") / (final[key].get("p") + final[key].get("r") )
        weighted_total += final[key].get("f1") * (c[key].get("correct")+c[key].get("wrong"))
        total += final[key].get("f1")

    f1_macro = total/len(final)
    f1_weighted = weighted_total/len(final)

