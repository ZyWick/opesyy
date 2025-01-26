import operator
import statistics as s

def runSJF (process_array):
    time = 0
    allprocess = process_array.copy()
    queue = []

    while (not not allprocess or not not queue):

        #add all process that's arrived to the queue
        queue.extend(filter(lambda process: process.arrival_time <= time, allprocess))
        allprocess = [process for process in allprocess if process.arrival_time > time]
        
        if (not not queue):
            
            # sort queue on attributes
            queue = sorted(queue, key=operator.attrgetter('burst_time', 'arrival_time', 'pid'))
            process = queue[0]

            #complete the process
            process.start_time = time
            process.wait_time = time - process.arrival_time
            time += process.burst_time 
            process.last_end_time = time 
            queue.pop(0)
            
            print("P[{}] start time: {} end time: {} | Waiting time: {}".format(process.pid, process.start_time, process.last_end_time, process.wait_time))
        else:
            time += 1;
    
    print("Average waiting time: ", format(s.mean(p.wait_time for p in process_array), ".2f"))
        