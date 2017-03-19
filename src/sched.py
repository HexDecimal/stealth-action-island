
import heapq

class Scheduler(object):
    def __init__(self):
        super().__init__()
        self.time = 0
        self.pqueue = []
        self._next_id = 0

    def schedule(self, interval, func):
        ticket = (self.time + interval, self._next_id, func)
        self._next_id += 1
        heapq.heappush(self.pqueue, ticket)
        return ticket

    def next(self):
        self.time, _, func = heapq.heappop(self.pqueue)
        func()
