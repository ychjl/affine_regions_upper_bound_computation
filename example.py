from ubc import ubc
from math import log10
from matplotlib import pyplot as plt 
import numpy as np

def solvefor(n ,m):
    l = 1
    r = m
    while r - l > 1e-6:
        mid = (l+r)/2
        if sum([mid**(2*i+1) for i in range(n)]) > m:
            r = mid
        else:
            l = mid
    return (l+r)/2

max_depth = 20
input_dim_range = range(1, 64)
img = np.empty((len(input_dim_range), max_depth))
solver = ubc(max_depth * max(input_dim_range))

for i in input_dim_range:
    for j in range(1, max_depth + 1):
        factor = solvefor(j, max_depth)
        ns = [round(i*factor**k) for k in range(j+1)]
        g = solver(ns)
        img[i - min(input_dim_range), j - 1] = log10(g[i])

plt.title("uncollapsed affine regions(1e)")
plt.xlabel("width")
plt.ylabel("depth")
plt.imshow(img.transpose(), origin="lower", extent=(min(input_dim_range) - 0.5,
                                                    max(input_dim_range) + 0.5,
                                                    0.5, max_depth + 0.5))
plt.colorbar()
plt.show()