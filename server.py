import glob
import json
import re
import threading
import socket
from time import time

dictionary_word = {}
mutex = threading.Lock()

def prepare_text(files_array):
    regex = re.compile('[^a-zA-Z]')

    for file_name in files_array:
        f = open(file_name, "r")
        text = f.readlines()
        for line in text:
            mutex.acquire()
            word_list = line.split(' ')
            mutex.release()
            current_line = []
            for word in word_list:
                mutex.acquire()
                current_line.append(regex.sub('', word).lower())
                mutex.release()
            inverted_index(current_line, file_name)
        f.close()


def inverted_index(current_line, file_name):
    position_word = 0
    for word in current_line:
        if word not in dictionary_word.keys():
            dictionary_word[word] = [(position_word, file_name)]
        else:
            dictionary_word[word] += [(position_word, file_name)]
        mutex.acquire()
        position_word += 1
        mutex.release()


def write_dictionary():
    f = open('multi_dictionary.txt', 'w')
    f.write(json.dumps(dictionary_word, indent=4))
    f.close()

def separate_content(files_array, number_processes):
    if len(files_array) < number_processes:
        return [files_array]
    files_batch = []
    part_size = int(len(files_array) / number_processes)
    for process in range(number_processes-1):
        files_batch.append(files_array[part_size * process : part_size * (process + 1)])
    files_batch.append(files_array[part_size * (number_processes - 1):])
    return files_batch

def lookup_query(query):
    if(dictionary_word.get(query, False)) :
        return('The reasult of search: ' + json.dumps(dictionary_word[query],indent=4))

    return('Sorry, there is no such word :(')


if __name__ == '__main__':
    # server basics
    HOST = '127.0.0.1'
    PORT = 10000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    conn, addr = s.accept()
    print('Connected by', addr)
    # end of server basics

    # basic variables
    files_path = '/Users/dianakoval/Downloads/parallel_projects/course_work/datasets'
    number_processes = 4

    start_time = time()
    files_array = list(glob.iglob(files_path + "/*.txt"))
    separation_array = separate_content(files_array, number_processes)
    threads = []
    # end of basic variables

    # starting threads
    for file_batch in separation_array:
        thread = threading.Thread(target=prepare_text, args=(file_batch,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    # end of threads

    # save inverted index in file
    write_dictionary()

    # duration time counted
    duration = time() - start_time
    print('Multi dictionary is ready')
    print('Multi duration time: ' + str(duration))
    # end of duration count block

    # server's communication with client
    while True:
        print('sending message...')
        conn.sendall('\n Enter word: '.encode('utf-8'))
        print('receiving message...')
        data = conn.recv(1024)
        if not data:
            break
        print('sending response...')
        conn.sendall(lookup_query(data.decode('utf-8')).encode('utf-8'))
    # end of server's communication with client