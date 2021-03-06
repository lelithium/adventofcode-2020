from tool.runners.python import SubmissionPy

from itertools import permutations
from random import randint
from collections import deque
from copy import deepcopy

palette = {0: " ", 1: "#", 2: "x", 3: "_", 4: "o"}


class RemiSubmission(SubmissionPy):
    def run(self, s):
        p = [int(n) for n in s.split(",")]
        droid = IntCode(p)
        self.directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        self.maze = {(0, 0): "."}
        coor = (0, 0)
        self.oxygen = (0, 0)

        queue = deque([(coor, droid)])

        while queue:
            coor, droid = queue.popleft()
            for direction, adj in enumerate(self.adjacent(coor)):
                if self.maze.get(adj, "?") != "?":
                    continue

                ddroid = droid.copy()
                ddroid.p_input.append(direction + 1)
                ddroid.execute()
                code = ddroid.p_output.pop()
                if code == 0:
                    self.maze[
                        (
                            coor[0] + self.directions[direction][0],
                            coor[1] + self.directions[direction][1],
                        )
                    ] = "#"
                elif code == 1 or code == 2:
                    new_coor = (
                        coor[0] + self.directions[direction][0],
                        coor[1] + self.directions[direction][1],
                    )
                    self.maze[new_coor] = "."
                    queue.append((new_coor, ddroid))
                    if code == 2:
                        self.oxygen = new_coor

        step = 0
        found = True
        self.maze[self.oxygen] = "O"
        while found:
            # self.display_maze()
            new_o = []
            for coor, tile in self.maze.items():
                if tile == "O":
                    for adj in self.adjacent(coor):
                        if self.maze.get(adj, "#") == ".":
                            new_o.append(adj)
            for coor in new_o:
                self.maze[coor] = "O"
            step += 1
            found = len(new_o) > 0

        return step - 1

    def adjacent(self, coor):
        adj = []
        for direction in self.directions:
            adj.append((coor[0] + direction[0], coor[1] + direction[1]))

        return adj

    def display_maze(self, coor=(0, 0)):
        maxx = max(x for (x, y) in self.maze.keys())
        minx = min(x for (x, y) in self.maze.keys())
        maxy = max(y for (x, y) in self.maze.keys())
        miny = min(y for (x, y) in self.maze.keys())

        for y in range(miny, maxy + 1)[::-1]:
            for x in range(minx, maxx + 1):
                if (x, y) == self.oxygen:
                    print("O", end="")
                elif (x, y) == coor:
                    print("D", end="")
                else:
                    print(self.maze.get((x, y), "?"), end="")
            print("")
        print("")


class IntCode:
    def __init__(self, p):
        self.p = [0] * (10 * len(p))
        for i, b in enumerate(p):
            self.p[i] = b

        self.pc = 0
        self.p_input = []
        self.p_output = []
        self.exited = False
        self.relative_base = 0

    def copy(self):
        return deepcopy(self)

    def get_param_p(self, index):
        param = self.p[self.pc + index + 1]
        opcode = self.p[self.pc]
        modes = opcode // 100
        for _ in range(index):
            modes //= 10
        mode = modes % 10

        if mode == 0:
            return param
        elif mode == 1:
            return None
        elif mode == 2:
            return param + self.relative_base

    def get_param(self, index):
        d = self.get_param_p(index)
        if d is not None:
            return self.p[d]
        else:
            # for immediate mode
            return self.p[self.pc + index + 1]

    def execute(self):
        if self.exited:
            return

        while True:
            opcode = self.p[self.pc]
            if opcode % 100 == 1:
                a = self.get_param(0)
                b = self.get_param(1)
                c = self.get_param_p(2)
                self.p[c] = a + b
                self.pc += 4

            elif opcode % 100 == 2:
                a = self.get_param(0)
                b = self.get_param(1)
                c = self.get_param_p(2)
                self.p[c] = a * b
                self.pc += 4

            elif opcode % 100 == 3:
                try:
                    a = self.get_param_p(0)
                    self.p[a] = self.p_input[0]
                    self.p_input = self.p_input[1:]
                except:
                    return
                self.pc += 2

            elif opcode % 100 == 4:
                self.p_output.append(self.get_param(0))
                self.pc += 2

            elif opcode % 100 == 5:
                a = self.get_param(0)
                b = self.get_param(1)
                if a != 0:
                    self.pc = b
                    continue
                self.pc += 3

            elif opcode % 100 == 6:
                a = self.get_param(0)
                b = self.get_param(1)
                if a == 0:
                    self.pc = b
                    continue
                self.pc += 3

            elif opcode % 100 == 7:
                a = self.get_param(0)
                b = self.get_param(1)
                c = self.get_param_p(2)
                if a < b:
                    self.p[c] = 1
                else:
                    self.p[c] = 0
                self.pc += 4

            elif opcode % 100 == 8:
                a = self.get_param(0)
                b = self.get_param(1)
                c = self.get_param_p(2)
                if a == b:
                    self.p[c] = 1
                else:
                    self.p[c] = 0
                self.pc += 4

            elif opcode % 100 == 9:
                a = self.get_param(0)
                self.relative_base += a
                self.pc += 2

            elif opcode % 100 == 99:
                self.exited = True
                break

        return
