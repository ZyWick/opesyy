from SchedulingStrategy import SchedulingStrategy

# Concrete Strategy for First-Come, First-Served (FCFS)
class FCFS(SchedulingStrategy):
    def execute(self, process_array, quantum_value=1):
        process_array.sort(key=lambda x: x.arrival_time)
        curr_time = 0
        total_waiting = []

        for x in process_array:
            if curr_time < x.arrival_time:
                curr_time = x.arrival_time

            start_time = curr_time
            curr_time += x.burst_time
            x.wait_time = start_time - x.arrival_time
            total_waiting.append(x.wait_time)

            print(f"P[{x.pid}] start time: {start_time} end time: {curr_time} | Waiting time: {x.wait_time}")
        
        print("Average waiting time:", format(sum(total_waiting) / len(total_waiting), ".2f"))

