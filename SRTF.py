import operator
import statistics as s
from SchedulingStrategy import SchedulingStrategy

class SRTF(SchedulingStrategy):
    def execute(self, process_array, quantum_value=1):
        def get_wait_time(process, time):
            last = max(process.last_end_time, process.arrival_time)
            process.wait_time += time - last

        time = 0
        allprocess = process_array.copy()
        queue = []
        prev_process = None

        while allprocess or queue:
            # Add all arrived processes to the queue
            queue.extend(filter(lambda process: process.arrival_time <= time, allprocess))
            allprocess = [p for p in allprocess if p.arrival_time > time]

            if queue:
                # Sort queue by burst_time, then arrival_time, then pid
                queue.sort(key=operator.attrgetter("burst_time", "arrival_time", "pid"))
                process = queue[0]

                # Set start time and wait time if needed
                if prev_process is None or prev_process.pid != process.pid:
                    process.start_time = time
                    get_wait_time(process, time)

                    if prev_process:
                        prev_process.last_end_time = time
                        print(f"P[{prev_process.pid}] start time: {prev_process.start_time} end time: {prev_process.last_end_time} | Waiting time: {prev_process.wait_time}")

                prev_process = process

                # Execute process for 1 time unit
                process.burst_time -= 1
                if process.burst_time == 0:
                    process.last_end_time = time + 1
                    print(f"P[{process.pid}] start time: {process.start_time} end time: {process.last_end_time} | Waiting time: {process.wait_time}")
                    queue.pop(0)
                    prev_process = None

            time += 1

        print("Average waiting time: ", format(s.mean(p.wait_time for p in process_array), ".2f"))
