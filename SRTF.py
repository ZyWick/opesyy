import operator
import statistics as s

def getWaitTime (process, time):
    # get the last time the current process has been preempted or arrived to compute wait time
    if (process.last_end_time >= process.arrival_time):
        last = process.last_end_time
    else:
        last = process.arrival_time
    process.wait_time = process.wait_time  + time - last

def runSRTF (process_array):
    time = 0;
    allprocess = process_array.copy()
    queue = []
    prev_process = None

    while (not not allprocess or not not queue):

        #add all process that's arrived to the queue
        queue.extend(filter(lambda process: process.arrival_time <= time, allprocess))
        allprocess = [process for process in allprocess if process.arrival_time > time]

        if (not not queue):
            
            # sort queue on attributes
            queue = sorted(queue, key=operator.attrgetter('burst_time', 'arrival_time', 'pid'))
            process = queue[0]
            
            # set start and wait time 
            # for when there's no process directly running before
            # for when the previous process has been preempted 
            if (prev_process == None or prev_process.pid != process.pid):
                process.start_time = time;
                getWaitTime (process, time)                

                # Enter if the previous process has been preempted
                if (prev_process != None):
                    # log the time the previous process was preempted and print values
                    prev_process.last_end_time = time
                    print("P[{}] start time: {} end time: {} | Waiting time: {}".format(prev_process.pid, prev_process.start_time, prev_process.last_end_time, prev_process.wait_time))

            #set the current process
            prev_process = process

            #decrease burst time and pop the process if completed
            process.burst_time = process.burst_time - 1;
            if (process.burst_time == 0):
                process.last_end_time = time + 1
                print("P[{}] start time: {} end time: {} | Waiting time: {}".format(process.pid, process.start_time, process.last_end_time, process.wait_time))
                queue.pop(0)
                prev_process = None
    
        time += 1;

    print("Average waiting time: ", format(s.mean(p.wait_time for p in process_array), ".2f"))

    