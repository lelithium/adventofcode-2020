from tool.runners.python import SubmissionPy


class BebertSubmission(SubmissionPy):

    def run(self, s):
        # s = """R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83"""
        # s = """R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7"""
        wires = {}
        cross = set()
        w1t, w2t = s.splitlines()
        w1 = w1t.strip().split(',')
        w2 = w2t.strip().split(',')
        for i, w in enumerate([w1, w2]):
            x, y = 0, 0
            for c in w:
                direction = c[0]
                step = int(c[1:])
                if direction == 'U':
                    dx, dy = 0, 1
                elif direction == 'D':
                    dx, dy = 0, -1
                elif direction == 'R':
                    dx, dy = 1, 0
                else:  # direction == 'L':
                    dx, dy = -1, 0

                for _ in range(step):
                    x, y = x + dx, y + dy
                    if wires.get((x, y), i) != i:
                        cross.add(abs(x) + abs(y))
                    else:
                        wires[(x, y)] = i

        return min(cross)
