import glob
import json
import re
from time import time

from pip._vendor.distlib.compat import raw_input

dictionary_word = {}

def prepare_text(files_path):
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
    position_word = 0
    for word in current_line:
        if word not in dictionary_word.keys():
            dictionary_word[word] = [(position_word, file_name)]
        else:
            dictionary_word[word] += [(position_word, file_name)]
        position_word += 1


def write_dictionary():
    f = open('serial_dictionary.txt', 'w')
    f.write(json.dumps(dictionary_word, indent=4))
    f.close()


def lookup_query(query):
    for word in dictionary_word.keys() :
        if(query == word) :
            return('The reasult of search: ' + json.dumps(dictionary_word[word],indent=4))
    return ('Sorry, there is no such word :(')

if __name__ == '__main__':
    files_path = '/Users/dianakoval/Downloads/parallel_projects/course_work/datasets'
    start_time = time()
    prepare_text(files_path)
    write_dictionary()
    duration = time() - start_time

    print(dictionary_word)

    search_term = raw_input("Enter term(s) to search: ")
    lookup_query(search_term)

    print('Serial dictionary is ready')
    print('Serial duration time: ' + str(duration))