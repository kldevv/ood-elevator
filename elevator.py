import heapq

from enums import Direction, ButtonType


class Elevator:
    def __init__(self, cur_level: int = 0):
        self.up_stops = []
        self.down_stops = []
        self.p_queue = set()

        self.cur_level = cur_level
        self.cur_dir = Direction.IDLE
        self.in_buttons = dict()
        self.ex_buttons = dict()

    def register(self, button) -> bool:
        # can be done in python 3.10 match statement
        if button.btype == ButtonType.IN:
            self.in_buttons[button.level] = button
        if button.btype == ButtonType.EX:
            self.ex_buttons[button.level] = button
        button.register(self)
        print(f"Registered Button: {button.level}, From Source: {button.btype}")
        return True

    def request(self, level: int, source: ButtonType) -> bool:
        if level == self.cur_level:
            return False

        r_dir = Direction.UP if level > self.cur_level else Direction.DOWN
        if source == ButtonType.IN and self.cur_dir != Direction.IDLE and r_dir != self.cur_dir:
            return False

        if level not in self.p_queue:
            print(f"Received Request At: {level}, From Source: {source}, While At {self.cur_level}")
            self.p_queue.add(level)
            if r_dir == Direction.UP:
                heapq.heappush(self.up_stops, level)

            if r_dir == Direction.DOWN:
                heapq.heappush(self.down_stops, -level)
        self._set_dir()
        return True

    def _set_dir(self):
        if len(self.p_queue) == 0:
            self.cur_dir = Direction.IDLE
        elif len(self.up_stops) == 0:
            self.cur_dir = Direction.DOWN
        else:
            self.cur_dir = Direction.UP

    def _move(self):
        self._set_dir()
        print(f"Moving {self.cur_dir}")
        if self.cur_dir == Direction.DOWN:
            self.cur_level = -1 * heapq.heappop(self.down_stops)
        elif self.cur_dir == Direction.UP:
            self.cur_level = heapq.heappop(self.up_stops)

        self.p_queue.remove(self.cur_level)
        print("Stop At: ", self.cur_level)

        if self.cur_level in self.in_buttons:
            self.in_buttons[self.cur_level].reset()
        if self.cur_level in self.ex_buttons:
            self.ex_buttons[self.cur_level].reset()
        self._set_dir()

    def start(self):
        if self.p_queue:
            self._move()
