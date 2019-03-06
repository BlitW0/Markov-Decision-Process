import sys, copy


class MDP:

    def __init__(self, board, policy, walls, end_states, step_reward, start):
        """Initializing the class."""
        self.board = board
        self.walls = walls
        self.start = start
        self.old_board = copy.deepcopy(self.board)
        self.original = copy.deepcopy(self.board)
        self.end_states = end_states
        self.policy = policy
        self.probability = {
        'target' : 0.8,
        'alt':     0.1,
        }
        self.delta = 0.01
        self.step_reward = step_reward
        self.init_board()
        self.init_policy()
        self.value_iteration()
        self.policy_function()

    def init_board(self):
        """Initializing the board with the walls. Replacing walls with NaN."""
        for i in range(len(self.walls)):
            x, y = self.walls[i]
            self.board[x][y] =  None
            self.policy[x][y] = None

    def init_policy(self):
        """Initializing policy for the board."""
        for i in range(len(self.end_states)):
            x, y = self.end_states[i]
            if self.board[x][y] > 0:
                self.policy[x][y] = "Goal"
            else:
                self.policy[x][y] = "Bad"

    def print_policy(self):
        sys.stdout.write(' ')
        for j in range(len(self.policy[0])):
            sys.stdout.write(' | %16s' % str(j))
        print
        for i in range(len(self.policy)):
            print('_' * 80)
            sys.stdout.write(str(i))
            for j in range(len(self.policy[i])):
                sys.stdout.write(' | %16s' % self.policy[i][j])
            print('|')
        print('_' * 80)

    def print_board(self):
        sys.stdout.write(' ')
        for j in range(len(self.board[0])):
            sys.stdout.write(' | %16s' % str(j))
        print
        for i in range(len(self.board)):
            print('_' * 80)
            sys.stdout.write(str(i))
            for j in range(len(self.board[i])):
                x = self.board[i][j]
                if type(x)==float:
                    x = round(x, 3)
                sys.stdout.write(' | %16s' % x)
            print('|')
        print('_' * 80)

    def value_iteration(self):
        """Running value iteration algorithm."""
        iteration_no = 0
        print "Iteration #0"
        self.print_board()
        while True:
            iteration_no += 1
            print "Iteration #%d" % iteration_no
            changed_pairs = []
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if (i, j) not in self.walls and (i,j) not in self.end_states:
                        self.board[i][j] = self.update(tuple((i, j)))
                        if self.old_board[i][j]!=0:
                            changed_pairs.append((self.board[i][j] - self.old_board[i][j])/self.old_board[i][j])
                        else:
                            changed_pairs.append(69.0)
            self.print_board()
            # Adding code to check if change is less than delta and then terminate
            if (max(changed_pairs) <= self.delta):
                return

            # Setting old_board as new board for next iteration
            self.old_board = copy.deepcopy(self.board)

    def policy_function(self):

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (i, j) not in self.end_states and (i, j) not in self.walls:
                    # self.policy[i][j] = self.policy_update((i, j))

                    util = [0.0, 0.0, 0.0, 0.0]
                    # right neighbour
                    util[0] = self.get_state_utility(self.old_board[i][j], (i, j+1))
                    # bottom neighbour
                    util[1] = self.get_state_utility(self.old_board[i][j], (i+1, j))
                    # left neighbour
                    util[2] = self.get_state_utility(self.old_board[i][j], (i, j-1))
                    # above neighbour
                    util[3] = self.get_state_utility(self.old_board[i][j], (i-1, j))

                    val = [0.0, 0.0, 0.0, 0.0]
                    val[0] = util[0]*self.probability['target'] + (util[1]+util[3])*self.probability['alt']
                    val[1] = util[1]*self.probability['target'] + (util[0]+util[2])*self.probability['alt']
                    val[2] = util[2]*self.probability['target'] + (util[1]+util[3])*self.probability['alt']
                    val[3] = util[3]*self.probability['target'] + (util[0]+util[2])*self.probability['alt']

                    total_utility =  self.step_reward + max(val) + self.original[i][j]
                    # print total_utility

                    pos = "0"
                    if (val[0] == max(val) ):
                        pos = "4"
                    elif (val[1] == max(val) ):
                        pos = "2"
                    elif (val[2] == max(val) ):
                        pos = "3"
                    elif (val[3] == max(val)):
                        pos = "1"

                    self.policy[i][j] = pos
                    # self.print_policy()
        return


    def update(self, state):
        x, y = state

        util = [0.0, 0.0, 0.0, 0.0]
        # right neighbour
        util[0] = self.get_state_utility(self.old_board[x][y], (x, y+1))
        # bottom neighbour
        util[1] = self.get_state_utility(self.old_board[x][y], (x+1, y))
        # left neighbour
        util[2] = self.get_state_utility(self.old_board[x][y], (x, y-1))
        # above neighbour
        util[3] = self.get_state_utility(self.old_board[x][y], (x-1, y))

        val = [0.0, 0.0, 0.0, 0.0]
        val[0] = util[0]*self.probability['target'] + (util[1]+util[3])*self.probability['alt']
        val[1] = util[1]*self.probability['target'] + (util[0]+util[2])*self.probability['alt']
        val[2] = util[2]*self.probability['target'] + (util[1]+util[3])*self.probability['alt']
        val[3] = util[3]*self.probability['target'] + (util[0]+util[2])*self.probability['alt']

        total_utility =  self.step_reward +  max(val) + self.original[x][y]
        return total_utility

    def get_state_utility(self, curVal, state):
        x, y = state
        if x < 0 or y < 0 or x>len(self.board)-1 or y>len(self.board[x])-1 or self.old_board[x][y]==0 or self.old_board[x][y]==None:
            return curVal
        return self.old_board[x][y]

    def get_state_policy(self, curVal, state):
        x, y = state
        if x < 0 or y < 0 or x>len(self.board)-1 or y>len(self.board[x])-1 or self.old_board[x][y]==0 or self.old_board[x][y]==None:
            return curVal
        return self.board[x][y]


if __name__ == '__main__':

    # Taking input for size of board
    inp = raw_input()
    inp = inp.split()
    n = int(inp[0])
    m = int(inp[1])

    # Initializing board with 0
    board = [[0 for i in range(m)] for j in range(n)]

    # Initializing policy
    policy = [["n/a" for i in range(m)] for j in range(n)]

    # Taking row wise input
    for i in range(n):
        rows = raw_input()
        rows = rows.split()
        for j in range(m):
            board[i][j] = float(rows[j])
    # original = copy.deepcopy(board)
    # Taking input for e and w, number of end states and number of walls
    inp = raw_input()
    inp = inp.split()
    e = int(inp[0])
    w = int(inp[1])

    # Initializing end states and walls arrays
    end_states = []
    walls = []

    # Taking input for all end states
    for i in range(e):
        inp = raw_input()
        inp = inp.split()
        end_states.append(tuple((int(inp[0]), int(inp[1]))))

    # Taking input for all walls
    for i in range(w):
        inp = raw_input()
        inp = inp.split()
        walls.append(tuple((int(inp[0]), int(inp[1]))))

    # Taking input for start state
    inp = raw_input()
    inp = inp.split()

    start = tuple((inp[0], inp[1]))

    # Taking input for unit step reward
    unit_step_reward = float(raw_input())

    # Creating class object and beginning value iteration
    m = MDP(board, policy, walls, end_states, unit_step_reward, start)
    # m.print_board()
    print "Optimal policy:"
    m.print_policy()
