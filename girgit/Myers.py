from collections import defaultdict
from Edit_Wrapper import Edit,Line
from girgit.Edit_Wrapper import Edit


class Myers:
    def __init__(self,a,b):
        self.a = a
        self.b = b
    def diff(self):
        m = len(self.a)
        n = len(self.b)
        v = defaultdict(int)
        v[1] = 0
        trace = []
        for d in range(m+n+1):
            trace.append(dict(v.copy()))
            for k in range(-d,d+1,2):
                if (k == -d) or (k!=d and v[k-1]<v[k+1]):
                    x = v[k+1]
                else:
                    x = v[k-1] + 1
                y = x-k
                while (x < m and y < n) and self.a[x] == self.b[y]:
                    x = x+1
                    y = y+1 # snake

                v[k] = x
                if x >= m and y>=n :
                    return trace


        raise Exception("No diff found") # as myers will always

    def back_track(self):

        x = len(self.a)
        y = len(self.b)
        for d,v in reversed(list(enumerate(self.diff()))):
            k = x - y

            if k == -d or (k != d and v[k-1] < v[k+1]):
                prev_k = k + 1
            else:
                prev_k = k - 1

            prev_x = v[prev_k]
            prev_y = prev_x - prev_k

            while x > prev_x and y > prev_y:
                yield x - 1 , y - 1 , x , y
                x -= 1
                y -= 1

            if d > 0 :
                yield prev_x , prev_y , x , y

            x = prev_x
            y = prev_y

    def diff_operations(self):
        diff = []
        for prev_x , prev_y , x , y in self.back_track():
            if x == prev_x : # downward / insert
                diff.insert(0,Edit("ins",None,Line(prev_y + 1 ,self.b[prev_y])))
                # this means at this point source has nothing but target has self.b[prev_y]
            elif y == prev_y : # rightward / delete
                diff.insert(0,Edit("del",Line(prev_x+1,self.a[prev_x]),None))
            else:
                diff.insert(0,Edit("eql",Line(prev_x+1 ,self.a[prev_x]),Line(prev_y+1,self.b[prev_y])))
        return diff

    def print_diff(self):
        edits = self.diff_operations()
        for edit in edits:
            prefix = {"ins": "+ ", "del": "- ", "eql": "  "}[edit.type]
            print(prefix + edit.text,end="")
            












