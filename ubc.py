from math import comb
class ubc:
    def __init__(self, max = 1024):
        tab = {}
        tmp = [1] + [0]*max
        for i in range(max+1):
            tab[(0, i)] = tmp
            tab[(1, i)] = i//2*[0] + i%2*[1] + i//2*[2] + [1]
            if i%2 == 0:
                tab[(2, i)] = (i-1)//2*[0] + [i//2] + i//2*[i] + [1]
            else:
                tab[(2, i)] = i//2*[0] + (i+1)//2*[i] + [1]
        for i in range(3, max+1):
            tmp = [0] + tab[(i-1, i-1)]
            for j in range(len(tmp) - 1):
                tmp[j] += tmp[j+1]
            tab[(i, i)] = tmp
        self.tab = tab
    
    def clip(self, g, n):
        if len(g) <= n + 1:
            return g
        return g[:n] + [sum(g[n:])]

    def ub(self, n, m):
        if (n, m) in self.tab:
            return self.tab[(n, m)]
        if n > m:
            return self.tab[(m, m)]
        a = [comb(i, n-3) for i in range(m-4, n-4, -1)]
        b = [comb(m-4-i, n-3-i) for i in range(n-2)]
        t = [0]*(m+1)
        g = m - n
        c = 3
        for i in b:
            h = self.tab[(c, c)]
            c += 1
            for j in range(len(h)):
                t[j+g] += i*h[j]
        c = 3
        for i in a:
            h = self.tab[(2, c)]
            c += 1
            g -= 1
            for j in range(len(h)):
                t[j+g] += i*h[j]
        self.tab[(n, m)] = t
        return t
        
    def forward(self, h, n):
        out = [0] * min(len(h), n+1)
        for i in range(len(h)):
            if h[i] == 0:
                continue
            b = self.ub(i, n)
            b = self.clip(b, i)
            for j in range(min(i+1, n+1)):
                out[j] += b[j] * h[i]
        return out

    def __call__(self, ns):
        h = ns[0]*[0] + [1]
        for i in ns[1:]:
            h = self.forward(h, i)
        return h
