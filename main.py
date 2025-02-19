import os
import sys
from SJF import SJF
from SRTF import SRTF
from FCFS import FCFS
from RR import RR

# Process class
class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.wait_time = 0

# Context class for scheduling execution
class Scheduler:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def set_strategy(self, strategy):
        self.strategy = strategy
    
    def execute_strategy(self, process_array, quantum_value=1):
        self.strategy.execute(process_array, quantum_value)

# Function to process inputs
def process_inputs():
    file_name = input("Enter filename (include file extension e.g. 'input.txt'): ")
    if not os.path.exists(file_name):
        print(f"{file_name} not found")
        sys.exit()
    
    with open(file_name, "r") as f:
        first_line = f.readline().split()
        sched_algo = int(first_line[0])
        quantum_value = int(first_line[2]) if sched_algo == 3 else 1

        algo_map = {0: "FCFS", 1: "SJF", 2: "SRTF", 3: "RR"}
        process_array = [Process(*map(int, line.split())) for line in f]
    
    return algo_map[sched_algo], quantum_value, process_array

if __name__ == '__main__':
    sched_algo, quantum_value, process_array = process_inputs()
    scheduler = None
    
    if sched_algo == "FCFS":
        scheduler = Scheduler(FCFS())
    elif sched_algo == "SJF":
        scheduler = Scheduler(SJF())
    elif sched_algo == "SRTF":
        scheduler = Scheduler(SRTF())
    elif sched_algo == "RR":
        scheduler = Scheduler(RR())
    
    if scheduler:
        scheduler.execute_strategy(process_array, quantum_value)
    
    input("Press Enter to continue...")
