from collections import defaultdict


class Myers:
    def __init__(self,a,b):
        self.a = a
        self.b = b
    def diff(self):
        m = len(self.a)
        n = len(self.b)
        v = defaultdict(int)
        v[1] = 0
        for d in range(m+n+1):
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
                    return d
        return None






