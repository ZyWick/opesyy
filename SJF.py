import operator
import statistics as s
from SchedulingStrategy import SchedulingStrategy

class SJF(SchedulingStrategy):
    def execute(self, process_array, quantum_value=1):
        time = 0
        allprocess = process_array.copy()
        queue = []

        while allprocess or queue:
            # Add all processes that have arrived to the queue
            queue.extend(filter(lambda process: process.arrival_time <= time, allprocess))
            allprocess = [p for p in allprocess if p.arrival_time > time]
            
            if queue:
                # Sort queue by burst_time, then arrival_time, then pid
                queue.sort(key=operator.attrgetter("burst_time", "arrival_time", "pid"))
                process = queue.pop(0)

                # Complete the process
                process.start_time = time
                process.wait_time = time - process.arrival_time
                time += process.burst_time
                process.last_end_time = time
                
                print(f"P[{process.pid}] start time: {process.start_time} end time: {process.last_end_time} | Waiting time: {process.wait_time}")
            else:
                time += 1

        print("Average waiting time: ", format(s.mean(p.wait_time for p in process_array), ".2f"))
