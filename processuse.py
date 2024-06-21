import logging
import os
from multiprocessing import Manager, Process, current_process


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def search_key_words(words_to_find: list[str], text: str, words_found: dict):
    name = current_process().name
    logger.debug(f"{name} started...")
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
    logger.debug(f"{name} is done.")


def handle_threads(file_list: list[str], words_to_find):
    name = current_process().name
    logger.debug(f"{name} started...")
    processes = []
    with Manager() as manager:
        words_found = manager.dict()
        for text in file_list:
            inside_dict = manager.dict()
            words_found.update({text: inside_dict})
        for text in file_list:
            processes.append(
                Process(
                    target=search_key_words,
                    args=(
                        words_to_find,
                        text,
                        words_found,
                    ),
                )
            )
        [process.start() for process in processes]
        [process.join() for process in processes]

        [print(dict(words_in_text)) for words_in_text in words_found.values()]


if __name__ == "__main__":
    file_list = [file for file in os.listdir(os.getcwd()) if file.endswith(".txt")]
    words_to_find = ("the", "a", "was", "is")

    handle_threads(file_list, words_to_find)
