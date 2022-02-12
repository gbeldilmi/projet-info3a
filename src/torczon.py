import math
import random
import time
import tkinter

EPSILON = 0.0001

########################################################################################################################
# newton.py (by D.M.)
########################################################################################################################

def square(v):
    return v * v

def vecteur(n, fonc):
    return [fonc(i) for i in range(n)]

def matrice(nl, nc, fonc):
    return vecteur(nl, lambda l: vecteur(nc, lambda c: fonc(l, c)))

def pscal(U, V):
    assert (len(U) == len(V))
    s = 0.
    for k in range(len(U)):
        s += U[k] * V[k]
    return s

def eval_sys(eq_sys, X):
    return vecteur(len(eq_sys), (lambda l: (eq_sys[l])(X)))

def carre_dist(a, b):
    (xa, ya) = a
    (xb, yb) = b
    return square(xa - xb) + square(ya - yb)

def dist_pp(p1, p2):
    (x1, y1) = p1
    (x2, y2) = p2
    return math.sqrt(carre_dist(p1, p2))

def v_mod_u(v, u):
    k = pscal(u, v) / pscal(u, u)
    return vecteur(len(v), (lambda i: v[i] - k * u[i]))

def dist_c_ab(c, a, b):
    (xa, ya) = a
    (xb, yb) = b
    (xc, yc) = c
    ab = [xb - xa, yb - ya]
    ac = [xc - xa, yc - ya]
    reste = v_mod_u(ac, ab)
    return math.sqrt(pscal(reste, reste))

########################################################################################################################
# utils, le couteau suisse
########################################################################################################################

def swap(arr, a, b): # échange deux éléments d'un tableau à partir de leurs indices
    foo = arr[a]
    arr[a] = arr[b]
    arr[b] = foo

def idx_crcl(r, c):  # donne l'indev du cercle à partir de sa position
    return r * (r + 1) // 2 + c

########################################################################################################################
# tk(in)t(er) pilou
########################################################################################################################

CNVS = tkinter.Canvas(tkinter.Tk(), width = 800, height = 800)
CNVS.pack()

def cnvsup(circles):
    CNVS.delete('all')
    for i in range(len(circles) // 3):
        x, y, r = circles[3 * i], circles[3 * i + 1], circles[3 * i + 2]
        CNVS.create_oval(x - r, y - r, x + r, y + r)
    CNVS.create_line(A[0], A[1], B[0], B[1])
    CNVS.create_line(B[0], B[1], C[0], C[1])
    CNVS.create_line(C[0], C[1], A[0], A[1])
    CNVS.update()

########################################################################################################################
# la choucroute
########################################################################################################################

A = (100, 100)
B = (700, 100)
C = (random.randint(100, 700), 700)

def pizza(n):
    r = 1. / (2 * (n - 1 + math.sqrt(3.)))
    circles = []
    for i in range(n):
        for j in range(i + 1):
            x = (r * math.sqrt(3.) + (n - 1) * r) - i * r + j * 2 * r
            y = (r + (n - 1) * r * math.sqrt(3.)) - i * r * math.sqrt(3.)
            a = 2 * y / math.sqrt(3)
            b = 1 - 2 * y / math.sqrt(3) - x + y / math.sqrt(3)
            g = x - y / math.sqrt(3)
            circles.append(a * A[0] + b * B[0] + g * C[0])
            circles.append(a * A[1] + b * B[1] + g * C[1])
            circles.append(1.)
    return circles

def lambtas(n):
    eqs = []
    def eqcd(ic, a, b):
        return lambda circles : dist_c_ab((circles[3 * ic], circles[3 * ic + 1]), a, b) - abs(circles[3 * ic + 2])
    def eqcc(ic1, ic2):
        return lambda circles : dist_pp((circles[3 * ic1], circles[3 * ic1 + 1]), (circles[3 * ic2], circles[3 * ic2 + 1])) - (abs(circles[3 * ic1 + 2]) + abs(circles[3 * ic2 + 2]))
    for i in range(n):
        for j in range(i + 1):
            ic = idx_crcl(i, j)
            if j == 0:
                eqs.append(eqcd(ic, A, B))
            if j == i:
                eqs.append(eqcd(ic, C, A))
            if i == n - 1:
                eqs.append(eqcd(ic, B, C))
            if j < i:
                eqs.append(eqcc(ic, idx_crcl(i, j + 1)))
            if i > 0 and j < i:
                eqs.append(eqcc(ic, idx_crcl(i - 1, j)))
            if i > 0 and j > 0:
                eqs.append(eqcc(ic, idx_crcl(i - 1, j - 1)))
    return eqs

def fsimp(fn, s):
    fs = vecteur(len(s), lambda v : fn(s[v]))
    imin = 0
    for i in range(1, len(fs)):
        if fs[i] < fs[imin]:
            imin = i
    swap(s, imin, 0)
    swap(fs, imin, 0)
    return (s, fs)

def t(fn, s, k):
    n = len(s)
    d = len(s[0])
    assert (d + 1 == n)
    st = vecteur(n, lambda v : vecteur(d, lambda i: k * s[v][i] + (1. - k) * s[0][i]))
    st[0] = vecteur(d, lambda i : s[0][i])
    return fsimp(fn, st)

def torczon(fn, crcls):
    iter = 0
    h = time.time_ns()
    d = len(crcls)
    def end(s):
        v = vecteur(d, lambda i : s[0][i] - s[d][i])
        return pscal(v, v) < EPSILON
    s = vecteur(d + 1, (lambda iv : vecteur(d, lambda ic : crcls[ic])))
    for i in range(1, d + 1):
        s[i][i - 1] += 0.1
    s, fs = fsimp(fn, s)
    while not end(s):
        sr, fsr = t(fn, s, -1.)
        if fsr[0] < fs[0]:
            se, fse = t(fn, sr, 2.)
            if fse[0] < fsr[0]:
                s = se
                fs = fse
            else:
                s = sr
                fs = fsr
        else:
            s, fs = t(fn, s, 0.5)
        if iter % 200 == 0:
            cnvsup(s[0])
        iter += 1
    h = (time.time_ns() - h) / 1000000000.
    return s[0], iter, h

def solve(n):
    cs = pizza(n)
    eqs = lambtas(n)
    cnvsup(cs)
    def fn(c):
        fc = eval_sys(eqs, c)
        return pscal(fc, fc)
    ce, iter, h = torczon(fn, cs)
    cnvsup(ce)
    return iter, h

########################################################################################################################
# pied
########################################################################################################################

def main():
    n = 6
    for n in range(1, n):
        c = n * (n + 1) // 2
        e = c * 3
        i, h = solve(n)
        print(f"==> {n} cercles par coté, {c} cercles, {e} inconnues, {i} itérations, {h} secondes écoulées")
        input("Done.")

if __name__ == '__main__':
    main()
