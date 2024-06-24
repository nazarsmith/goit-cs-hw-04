import logging
import os
import time

from multiprocessing import Manager, Queue, Process, current_process, cpu_count

from utils import utils

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def search_key_words(
    # words_to_find: list[str],
    # text: str | list,
    # words_found: dict,
    queue: Queue,
):
    name = current_process().name
    logger.debug(f"{name} started...")
    words_to_find, text, words_found = queue.get()
    try:
        if isinstance(text, str):
            utils.search_text(
                text_path=text, words_to_find=words_to_find, words_found=words_found
            )
        elif isinstance(text, list):
            for t in text:
                utils.search_text(
                    text_path=text, words_to_find=words_to_find, words_found=words_found
                )
    except FileNotFoundError as e:
        logger.debug(
            f"{text} was not found in the current working directory. Moving on to the next text.."
        )
    except Exception as e:
        raise Exception from e
    logger.debug(f"{name} is done.")


def handle_processes(file_list: list[str], words_to_find):
    time_now = time.time()
    name = current_process().name
    logger.debug(f"{name} started...")

    queue = Queue()
    processes = []
    cpu_number = cpu_count()
    # cpu_number = 4 # for testing purposes
    num_texts = len(file_list)

    if num_texts > cpu_number:
        splitter = num_texts // cpu_number
    else:
        splitter = 0

    with Manager() as manager:
        # words_found = manager.dict()
        words_found = {}
        # create a dict with sought words as keys
        for word in words_to_find:
            inside_list = manager.list()
            words_found.update({word: inside_list})
        start_index = end_index = num_texts - cpu_number
        texts = file_list[start_index:]
        while splitter >= 0:
            for text in texts:
                processes.append(
                    Process(
                        target=search_key_words,
                        args=(queue,),
                    )
                )
                queue.put([words_to_find, text, words_found])

            [process.start() for process in processes]
            [process.join() for process in processes]
            processes.clear()

            start_index = start_index - cpu_number if start_index >= cpu_number else 0
            texts = file_list[start_index:end_index]
            end_index = start_index
            splitter -= 1
        logger.debug("No more texts to process. Printing out the results..")
        time.sleep(0.1)

        utils.print_results(words_found)
        print("\nExecution time:", time.time() - time_now)


if __name__ == "__main__":
    file_list = [file for file in os.listdir(os.getcwd()) if file.endswith(".txt")]
    file_list.append("kinda/path/to/file")
    words_to_find = ("the", "a", "was", "is", "world")

    handle_processes(file_list, words_to_find)
