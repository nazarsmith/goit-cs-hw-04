import logging
import os
import threading


def search_key_words(words_to_find: list[str], text: str, words_found: dict):
    words_found.update({text: {}})
    with open(os.path.join(os.getcwd(), text), "r") as file:
        for line in file.readlines():
            words = line.split()
            for w in words:
                if w in words_to_find:
                    if w not in list(words_found[text].keys()):
                        words_found[text].update({w: 1})
                    else:
                        words_found[text][w] += 1
                        continue
    logging.debug("Done.")


def handle_threads(file_list: list[str], words_to_find) -> dict:
    threads = []
    words_found = {}
    for text in file_list:
        threads.append(
            threading.Thread(
                target=search_key_words, args=(words_to_find, text, words_found)
            )
        )

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    [print(f"{text}: {words}") for text, words in words_found.items()]


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")

    file_list = [file for file in os.listdir(os.getcwd()) if file.endswith(".txt")]
    words_to_find = ("the", "a", "was", "is")

    handle_threads(file_list, words_to_find)
