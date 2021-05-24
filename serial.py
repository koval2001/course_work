import glob
import json
import re
from time import time

dictionary_word = {}

def prepare_text(files_path):
    """
    Normalizing words for building inverted index
    :param files_path: list of files' path
    :return:
    """
    regex = re.compile('[^a-zA-Z]')

    for file_name in glob.iglob(files_path + "/*.txt"):
        f = open(file_name, "r")
        text = f.readlines()
        for line in text:
            word_list = line.split(' ')
            current_line = []
            for word in word_list:
                current_line.append(regex.sub('', word).lower())
            inverted_index(current_line, file_name)
        f.close()


def inverted_index(current_line, file_name):
    """
    Creating an inverted index
    :param current_line:
    :param file_name:
    :return:
    """
    position_word = 0
    for word in current_line:
        if word not in dictionary_word.keys():
            dictionary_word[word] = [(position_word, file_name)]
        else:
            dictionary_word[word] += [(position_word, file_name)]
        position_word += 1


def write_dictionary():
    """
    Writing inverted index to .txt file
    :return:
    """
    f = open('serial_dictionary.txt', 'w')
    f.write(json.dumps(dictionary_word, indent=4))
    f.close()


def lookup_query(query):
    """
    Seeking a word in inverted index
    :param query:
    :return: a word's position and files' names where it was found
    """
    if (dictionary_word.get(query, False)):
        return ('The reasult of search: ' + json.dumps(dictionary_word[query], indent=4))

    return ('Sorry, there is no such word :(')


if __name__ == '__main__':
    # basic variables
    files_path = '/Users/dianakoval/Downloads/parallel_projects/course_work/datasets/aclImdb'
    start_time = time()

    # indexing
    prepare_text(files_path)
    write_dictionary()
    duration = time() - start_time

    # seeking a word in inverted index
    search_term = input("Enter term to search: ")
    search_result = lookup_query(search_term)
    print(search_result)

    # finishing main and printing duration time
    print('Serial dictionary is ready')
    print('Serial duration time: ' + str(duration))