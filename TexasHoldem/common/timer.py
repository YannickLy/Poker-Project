import time

class timer:
    
    def __init__(self):
        self.start_time = None
        self.stop_time = None
        
    def start(self):
        self.start_time = time.time()
    
    def stop(self):
        self.stop_time = time.time()
    
    def total_run_time(self):
        return self.stop_time - self.start_time