# Team Number
X = 30.0

n, m = 4, 4

reward = [
    [X/10, 0, 0, X],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, -X/5, 0]
]

e, w = 3, 2

E = [
    (0, 0),
    (0, 3),
    (3, 2)
]

W = [
    (0, 1),
    (2, 2),
]

start_state = (3, 0)
step_cost = -X/10

print n, m

for row in reward:
    for ele in row:
        print ele,
    print

print e, w

for (x, y) in E:
    print x, y

for (x, y) in W:
    print x, y

print start_state[0], start_state[1]

print step_cost

