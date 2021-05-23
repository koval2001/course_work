import glob
import json
import re
from time import time
from matplotlib import pyplot
import multiprocessing as mp

dictionary_word = {}

def prepare_text(files_array):
    regex = re.compile('[^a-zA-Z]')

    for file_name in files_array:
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

def draw_results(list, num_process):
    array_x = num_process
    array_y = list

    figure = pyplot.figure()
    ax = figure.add_subplot()
    ax.set_xlabel('Number of processes')
    ax.set_ylabel('Time')
    ax.set_title("Graph", fontsize=15)
    ax.grid(False)
    ax.plot(array_x, array_y)
    ax.plot(array_x, array_y, 'ro')
    pyplot.show()

if __name__ == '__main__':
    files_path = '/Users/dianakoval/Downloads/parallel_projects/course_work/datasets'

    number_processes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    times = []
    for i in number_processes:
        start_time = time()
        for j in range(10):
            files_array = list(glob.iglob(files_path + "/*.txt"))
            separation_array = separate_content(files_array, i)
            processes = []

            for file_batch in separation_array:
                process = mp.Process(target=prepare_text, args=(file_batch,))
                process.start()
                processes.append(process)

            for process in processes:
                process.join()
            write_dictionary()
        duration = (time() - start_time)/10
        times.append(duration)

    draw_results(times, number_processes)

    print('Multi dictionary is ready')
    print('Multi duration time: ' + str(duration))