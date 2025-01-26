# MADE BY: GROUP 21
# CORPUZ, DAVID JOSHUA
# GUANZON, CARLOS ANTONIO

import os
import sys
from SJF import runSJF
from SRTF import runSRTF

algo_index = ["FCFS", "SJF", "SRTF", "RR"]

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.start_time = 0
        self.wait_time = 0
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.order = 0
        self.last_end_time = 0

def averageTime(total_len, num_arr):
    temp_sum = 0
    result = 0
    for x in num_arr:
        temp_sum += x
        result = temp_sum / total_len

    result = format(result, ".2f")
    return result

def insertionSort(arr):
    n = len(arr)

    for i in range(1, n):
        key = arr[i].arrival_time
        key_obj = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j].arrival_time:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_obj

def insertionSortId(arr):
    n = len(arr)

    for i in range(1, n):
        key = arr[i].pid
        key_obj = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j].pid:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_obj


def firstCome(process_array):
    temp_array = process_array.copy()
    total_waiting = []
    insertionSort(temp_array)
    curr_time = 0
    for x in temp_array:
        if (curr_time == 0 or x.arrival_time > curr_time) and x.arrival_time != curr_time:
            curr_time = int(x.arrival_time)

        start_time = curr_time
        curr_time += int(x.burst_time)
        x.wait_time = (int(curr_time) - int(x.burst_time)) - int(x.arrival_time)
        total_waiting.append(int(x.wait_time))
        print("P[{}] start time: {} end time: {} | Waiting time: {}".format(x.pid, start_time, curr_time, x.wait_time))

    average_time = averageTime(len(total_waiting), total_waiting)
    print("Average waiting time: ", average_time)

def roundRobin(process_array, quantum_value):
    queued_pids = []
    quantum_value = int(quantum_value)
    temp_queue = []
    temp_array = process_array.copy()
    total_waiting = []
    insertionSort(temp_array)
    curr_time = 0
    total_running_time = 0
    queued_pids.append(temp_array[0])
    temp_queue.append(temp_array[0])

    #get total running time
    for x in temp_array:
        if (total_running_time == 0 or x.arrival_time > total_running_time) and x.arrival_time != curr_time:
            total_running_time += int(x.arrival_time)

        total_running_time += int(x.burst_time)

    while curr_time < total_running_time:
        if len(temp_queue) >= 1:
            if (curr_time == 0 or temp_queue[0].arrival_time > curr_time) and temp_queue[0].arrival_time != curr_time:
                curr_time = int(temp_queue[0].arrival_time)

            start_time = curr_time

            if quantum_value >= int(temp_queue[0].burst_time):
                temp_burst = int(temp_queue[0].burst_time)
                temp_queue[0].burst_time = 0

            else:
                temp_burst = quantum_value
                temp_queue[0].burst_time = int(temp_queue[0].burst_time) - quantum_value


            curr_time += temp_burst

            if temp_queue[0].last_end_time == 0:
                temp_queue[0].wait_time = temp_queue[0].wait_time + (
                            (int(curr_time) - temp_burst) - int(temp_queue[0].arrival_time))
            else:
                num = int(start_time) - int(temp_queue[0].last_end_time)
                temp_queue[0].wait_time = temp_queue[0].wait_time + num

            temp_queue[0].last_end_time = curr_time

            print("P[{}] start time: {} end time: {} | Waiting time: {}".format(temp_queue[0].pid, start_time, curr_time, temp_queue[0].wait_time))

            #now check for any new processes
            for x in temp_array:
                if x.pid != temp_queue[0].pid and x not in queued_pids:
                    if int(x.arrival_time) <= curr_time:
                        temp_queue.append(x)
                        queued_pids.append(x)

            if int(temp_queue[0].burst_time) > 0:
                temp_queue.append(temp_queue.pop(0))
            else:
                total_waiting.append(temp_queue[0].wait_time)
                temp_queue.pop(0)

        else:
            curr_time += 1
            for x in temp_array:
                if x not in queued_pids:
                    if int(x.arrival_time) <= curr_time:
                        temp_queue.append(x)
                        queued_pids.append(x)




    average_time = averageTime(len(total_waiting), total_waiting)
    print("Average waiting time: ", average_time)

def processInputs(process_array):
    file_name = input("Enter filename (include file extension e.g. 'input.txt'): ")
    if os.path.exists(file_name):
        f = open(file_name, "r")
        first_line = f.readline().split(" ")
        sched_algo = first_line[0]
        num_process = first_line[1]
        if sched_algo == "3":
            quantum_value = first_line[2]
        else:
            quantum_value = 1

        sched_algo = algo_index[int(sched_algo)]

        for idx, x in enumerate(f):
            proc_input = x.split(" ")

            temp_proc = Process(int(proc_input[0]), int(proc_input[1]), int(proc_input[2]))
            process_array.append(temp_proc)

        insertionSortId(process_array)

        f.close()

        return sched_algo, quantum_value
    else:
        print("{} not found".format(file_name))
        input("Press Enter to continue...")
        sys.exit()


if __name__ == '__main__':
    process_array = []
    sched_algo, quantum_value = processInputs(process_array)

    if sched_algo == 'FCFS':
        firstCome(process_array)
    elif sched_algo == 'SJF':
        runSJF(process_array)
    elif sched_algo == 'SRTF':
        runSRTF(process_array)
    elif sched_algo == 'RR':
        roundRobin(process_array, quantum_value)

    input("Press Enter to continue...")
