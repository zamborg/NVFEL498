import numpy as np

def pke(d, v, a):
    begin_accel = None
    end_accel = None
    total = 0
    for i in range(len(a)):
        if a[i] > 0:
            if begin_accel is None:
                begin_accel = i - 1
        else:
            end_accel = i - 1
            if begin_accel is not None:
                
                pke_segment = v[end_accel] ** 2 - v[begin_accel] ** 2
                assert(pke_segment > 0)

                total += pke_segment
                begin_accel = None

    if begin_accel < len(a) - 1:
        pke_segment = v[len(a) - 1] ** 2 - v[begin_accel] ** 2
        total += pke_segment
    
    return total / np.sum(d)

d = np.array([ 0, 10, 20, 30, 20, 10, 20, 25])
v = np.array([ 0, 10, 20, 30, 20, 10, 20, 25])
a = np.array([  0,  10,  10,  10, -10, -10,  10,   5])

print(pke(d, v, a))