import os


def search_text(**kwargs):
    text_path = os.path.join(os.getcwd(), kwargs["text_path"])
    words_to_find = kwargs["words_to_find"]
    words_found = kwargs["words_found"]
    with open(text_path, "r") as file:
        for line in file.readlines():
            words = line.split()
            for w in words:
                if w in words_to_find:
                    if text_path not in words_found[w]:
                        words_found[w].append(text_path)


def print_results(results: dict):
    [print(f"{k}:", list(set(v))) for k, v in results.items()]
