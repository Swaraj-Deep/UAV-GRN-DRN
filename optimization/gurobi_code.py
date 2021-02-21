# Imports
from gurobipy import *
from itertools import chain, combinations
import time
import math

start_time = time.time()

# Utility functions


def powerset(V):
    return chain.from_iterable(combinations(V, r) for r in range(len(V)+1))


def euc_dist(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) + 0.1


# Inputs
gamma_temp = []
phi_temp = []
pos_user = [[8.13, 1.13], [8.64, 5.11], [1.56, 4.64], [3.07, 8.74], [2.09, 5.45], [0.22, 7.2], [7.08, 5.78], [0.06, 1.61], [3.63, 3.78], [8.42, 5.14], [5.38, 2.71], [3.58, 5.89], [8.76, 8.84], [1.02, 4.17], [3.73, 7.68], [8.21, 8.23], [4.8, 4.41], [2.78, 1.13], [2.96, 5.9], [0.94, 3.78], [
    3.62, 6.95], [7.02, 6.02], [7.56, 7.08], [5.69, 8.46], [0.54, 6.75], [0.63, 4.75], [3.89, 1.48], [3.93, 6.35], [3.08, 7.26], [4.57, 4.41], [3.28, 4.6], [6.84, 4.39], [7.08, 7.69], [2.02, 7.06], [3.82, 2.0], [0.49, 6.75], [5.56, 8.28], [7.56, 2.0], [2.81, 3.17], [3.51, 5.92]]  # User locations
# Undirected GRN Graph
grn_neigh_list = [
    [1, 2, 3],
    [0, 3],
    [0, 3],
    [0, 1, 2, 4],
    [3, 5, 6, 7],
    [4, 7],
    [4, 7],
    [4, 5, 6, 8],
    [7, 9, 10, 11],
    [8, 11],
    [8, 11],
    [8, 9, 10, 12],
    [11, 13, 14],
    [12, 15],
    [12, 15],
    [13, 14, 16],
    [15, 17, 19, 18],
    [16, 18],
    [16, 17, 19, 20],
    [16, 18, 20],
    [18, 19],
    []
]  # GRN neighbour list
phi0 = 8  # SNR UAV to UAV
gamma0 = 1  # SNR UAV to user
c_thresh = 0.9  # Coverage threshold
s_thresh = 0.30  # Similarity threshold
M = 10  # Simulation Area
V = 10  # Number of UAVs
N = 30  # Number of users
Vg = 21  # Number of vertices in GRN
Pj = 2  # Power of jth UAV
# emc = [
#     [0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
#     [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0],
#     [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0],
#     [0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# ]  # Edge motif centrality of GRN

fc = 2
eta_n = 21
eta_l = 0.1


for i in range(N):
    temp = []
    for j in range(M):
        for k in range(M):
            temp.append(round(euc_dist(pos_user[i], [j, k]), 4))
    gamma_temp.append(temp)

for i in range(M):
    for j in range(M):
        temp = []
        for k in range(M):
            for l in range(M):
                temp.append(round(euc_dist([i, j], [k, l]), 4))
        phi_temp.append(temp)


hj = 100

a = 1  # Constant parameters calculated based on environment (urban or rural)
b = 1  # Constant parameters calculated based on environment (urban or rural)
speed_of_light = 3.2


def dist(i, j, flag):
    if flag:
        # Calculate for Gamma
        return gamma_temp[i][j]
    else:
        # Calculate for phi
        return phi_temp[i][j]


def theta(i, j, flag):
    return math.atan(100 / dist(i, j, flag))


def p_l(i, j, flag):
    return 1 + a * math.exp(-b * (theta(i, j, flag) - a)) ** -1


def p_n(i, j, flag):
    return 1 - p_l(i, j, flag)


def get_inter(i, j, flag):
    return 20 * math.log((4 * math.pi * fc * dist(i, j, flag)) / speed_of_light)


def phi_l_ij(i, j, flag):
    return get_inter(i, j, flag) * eta_l


def phi_n_ij(i, j, flag):
    return get_inter(i, j, flag) * eta_n


def phiij(i, j, flag):
    return ((p_l(i, j, flag) * phi_l_ij(i, j, flag)) + (p_n(i, j, flag) * phi_n_ij(i, j, flag)))


def gij(i, j, flag):
    return 10 ** (-phiij(i, j, flag) / 10)


def gamma(i, j, flag):
    return Pj * gij(i, j, flag) / 4


# Gurobi Model
model = Model("Network Model")

z = model.addVars(N, vtype=GRB.BINARY, name="z")
za = model.addVars(N, V, vtype=GRB.BINARY, name="za")
zb = model.addVars(V, V, vtype=GRB.BINARY, name="zb")
y = model.addVars(V, V, vtype=GRB.BINARY, name="y")
c = model.addVars(V, vtype=GRB.BINARY, name="c")
u = model.addVars(V, V, vtype=GRB.BINARY, name="u")
x = model.addVars(V, Vg, vtype=GRB.BINARY, name="x")
P = model.addVars(V, M, M, vtype=GRB.BINARY, name='P')
model.update()

for i in range(N):
    model.addConstr(z[i] <= quicksum(za[i, j] for j in range(V)), "C13.1")
model.addConstr(quicksum(z[i] for i in range(N)) >= c_thresh * N, "C13.2")
model.addConstr(quicksum(y[i, j] for i in range(V) for j in range(V) if i != j) >=
                s_thresh * quicksum(zb[i, j] for i in range(V) for j in range(V) if i != j), "C14")
# for i in range(V):
#     model.addConstr(quicksum(P[i, j, k] for j in range(M)
#                              for k in range(M)) <= 1, "C15")

# for i in range(V):
#     model.addConstr(c[i] == quicksum(P[i, j, k]
#                                      for j in range(M) for k in range(M)), "C16")

# for j in range(M):
#     for k in range(M):
#         model.addConstr(quicksum(P[i, j, k] for i in range(V)) <= 1, "C17")

for i in range(N):
    for j in range(V):
        model.addConstr(gamma(i, j, True) *
                        za[i, j] >= gamma0 * za[i, j], "C18")
for i in range(V):
    for j in range(V):
        if i != j:
            model.addConstr(gamma(i, j, False) *
                            zb[i, j] >= phi0 * zb[i, j], "C19")

for i in range(N):
    for j in range(V):
        model.addConstr(za[i, j] <= c[j], "C20")

for i in range(V):
    for j in range(V):
        model.addConstr(zb[i, j] <= c[i], "C21.1")
        model.addConstr(zb[i, j] <= c[j], "C21.2")
for j in range(V):
    model.addConstr(quicksum(zb[i, j] for i in range(V)) >= 1, "C22")
for i in range(V):
    for j in range(V):
        model.addConstr(u[i, j] <= zb[i, j], "C23")
model.addConstr(quicksum(u[i, j] for i in range(V) for j in range(
    V) if i != j) >= quicksum(c[i] for i in range(V)) - 1, "C24")

subset = list(powerset(list(range(V))))
for S in subset[1:]:
    S = set(S)
    model.addConstr(quicksum(u[i, j]
                             for i in S for j in S if i != j) <= len(S) - 1, "C25")
for k in range(Vg):
    model.addConstr(quicksum(x[i, k] for i in range(V)) <= 1, "C26")

for i in range(V):
    model.addConstr(quicksum(x[i, k] for k in range(Vg)) <= 1, "C27")

for i in range(V):
    for j in range(V):
        for k in range(Vg):
            model.addConstr(x[i, k] + y[i, j] <= 1 + quicksum(x[j, l]
                                                              for l in grn_neigh_list[j]), "C28")
for i in range(V):
    for k in range(Vg):
        model.addConstr(x[i, k] <= c[i], "C29")
for i in range(V):
    for j in range(V):
        model.addConstr(y[i, j] <= zb[i, j], "C30")

model.setObjective(quicksum(c[i] for i in range(V)) / 5, GRB.MINIMIZE)
model.optimize()

model.write("Model.lp")
model.write("Solution.sol")

print("######################### C ###########################")
for i in c:
    if c[i].X == 1:
        print(i)
print("######################### Zb ###########################")
for i in zb:
    if zb[i].X == 1:
        print(i)
print("######################### Za ###########################")
for i in za:
    if za[i].X == 1:
        print(i)
