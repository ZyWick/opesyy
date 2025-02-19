from SchedulingStrategy import SchedulingStrategy

# Concrete Strategy for Round-Robin (RR)
class RoundRobin(SchedulingStrategy):
    def execute(self, process_array, quantum_value):
        queue = []
        process_array.sort(key=lambda x: x.arrival_time)
        curr_time = 0
        total_waiting = []
        queued_pids = set()
        
        queue.append(process_array[0])
        queued_pids.add(process_array[0].pid)
        total_runtime = sum(p.burst_time for p in process_array)

        while curr_time < total_runtime:
            if queue:
                proc = queue.pop(0)
                start_time = curr_time
                execute_time = min(proc.burst_time, quantum_value)
                proc.burst_time -= execute_time
                curr_time += execute_time
                
                if proc.burst_time == 0:
                    total_waiting.append(curr_time - proc.arrival_time - execute_time)
                else:
                    queue.append(proc)

                print(f"P[{proc.pid}] start time: {start_time} end time: {curr_time} | Waiting time: {proc.wait_time}")
            
            for p in process_array:
                if p.pid not in queued_pids and p.arrival_time <= curr_time:
                    queue.append(p)
                    queued_pids.add(p.pid)
        
        print("Average waiting time:", format(sum(total_waiting) / len(total_waiting), ".2f"))
