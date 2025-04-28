import threading
import queue
import time

class Process(threading.Thread):
    def __init__(self, name, next_process):
        super().__init__(daemon=True)
        self.name = name
        self.next_process = next_process
        self.token_queue = queue.Queue(maxsize=1)
        self.wants_to_print = False

    def request_print(self):
        self.wants_to_print = True

    def run(self):
        while True:
            token = self.token_queue.get()
            if self.wants_to_print:
                print(f"{self.name} is printing!")
                time.sleep(2)
                self.wants_to_print = False  # Reset after printing
            try:
                self.next_process.token_queue.put(token, block=False)
            except queue.Full:
                pass

# Set up the ring
p1 = Process("P1", None)
p2 = Process("P2", None)
p3 = Process("P3", None)
p1.next_process = p2
p2.next_process = p3
p3.next_process = p1

# Start processes
p1.start()
p2.start()
p3.start()

p1.token_queue.put("TOKEN")

# Simulate periodic print requests
def simulate_requests():
    time.sleep(1)
    p2.request_print()  # P2 wants to print at 1s
    time.sleep(2)
    p1.request_print()  # P1 wants to print at 3s
    time.sleep(2)
    p3.request_print()  # P3 wants to print at 5s

# Run requests in a background thread
threading.Thread(target=simulate_requests, daemon=True).start()

# Let the simulation run indefinitely
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nSimulation stopped.")