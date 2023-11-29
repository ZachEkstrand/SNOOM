class Stopwatch:
    def __init__(self, time_now):
        self.time_of_start = time_now
        self.elapsed_time = 0

    def update(self, time):
        self.elapsed_time += time