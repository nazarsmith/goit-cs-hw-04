import logging
import os
import threading
import time

from utils import utils


def search_key_words(words_to_find: list[str], text: str, words_found: dict):
    try:
        utils.search_text(
            text_path=text, words_to_find=words_to_find, words_found=words_found
        )
    except FileNotFoundError as e:
        logging.debug(
            f"{text} was not found in the current working directory. Moving on to the next text.."
        )
    except Exception as e:
        raise Exception from e
    logging.debug("Done.")


def handle_threads(file_list: list[str], words_to_find):
    time_now = time.time()
    threads = []
    # create a dict with sought words as keys
    words_found = {w: [] for w in words_to_find}
    for text in file_list:
        threads.append(
            threading.Thread(
                target=search_key_words, args=(words_to_find, text, words_found)
            )
        )

    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    logging.debug("No more texts to process. Printing out the results..")
    time.sleep(0.1)

    utils.print_results(words_found)
    time.sleep(0.1)
    logging.debug(f"Execution time: {time.time() - time_now}")


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")

    file_list = [file for file in os.listdir(os.getcwd()) if file.endswith(".txt")]
    file_list.append("kinda/path/to/file")
    words_to_find = ("the", "a", "was", "is", "world")

    handle_threads(file_list, words_to_find)
