import copy
import sys

COL_LEN = 12


def get_input_list(input_type):
    return map(input_type, raw_input().split())


def get_input_value(input_type):
    return input_type(raw_input())


def print_board(board):
    for row in board:
        print ' ',
        for element in row:
            print element,
        print


def print_board_mysql_style(board, rows_num, cols_num, col_len=COL_LEN):

    def print_horizontal_border():
        line_str = ' +' + '-'*col_len
        for _ in range(cols_num):
            line_str += '+' + '-'*col_len
        line_str += '+'
        print line_str

    def print_line(values_list):
        print_horizontal_border()
        line_str = ' '
        for value in values_list:
            value = str(value)
            line_str += '|' + ' '*(col_len - len(value)) + value
        line_str += '|'
        print line_str

    values = [''] + ['Column ' + str(x) for x in range(cols_num)]
    print_line(values)

    for index, row in enumerate(board):
        values = ['Row ' + str(index)]
        for element in row:
            if type(element) == float:
                element = round(element, 3)
            values.append(element)
        print_line(values)

    print_horizontal_border()


class MDP:

    def __init__(self, board, end_states, walls, unit_step_reward, probability, alternate_probability, delta, discount, rows_num, cols_num):
        self.walls = walls
        self.end_states = end_states
        self.unit_step_reward = unit_step_reward
        self.utility_map = board
        self.probability = probability
        self.alternate_probability = alternate_probability
        self.delta = delta
        self.discount = discount
        self.reward = board
        self.rows_num = rows_num
        self.cols_num = cols_num
        self.policy = [['-' for _ in range(cols_num)] for _ in range(rows_num)]
        self.vertical_change = [(1, 0), (-1, 0)]
        self.horizontal_change = [(0, 1), (0, -1)]
        self.dir_char = {
            (1, 0): 'Go Down', (-1, 0): 'Go Up', (0, 1): 'Go Right', (0, -1): 'Go Left'
        }

    def will_go(self, x, y):
        return (x, y) not in self.walls and x >= 0 and x < len(self.utility_map) and y >= 0 and y < len(self.utility_map[0]) and self.utility_map[x][y] is not None

    def get_utility(self, px, py, x, y):
        if self.will_go(x, y):
            return self.utility_map[x][y]
        return self.utility_map[px][py]

    def new_utility(self, x, y):

        max_neighbour = float('-inf')

        for (dx, dy) in self.vertical_change:
            value = self.probability * self.get_utility(x, y, x + dx, y + dy)
            for (dx_w, dy_w) in self.horizontal_change:
                value += self.alternate_probability * \
                    self.get_utility(x, y, x + dx_w, y + dy_w)
            max_neighbour = max(max_neighbour, value)

        for (dx, dy) in self.horizontal_change:
            value = self.probability * self.get_utility(x, y, x + dx, y + dy)
            for (dx_w, dy_w) in self.vertical_change:
                value += self.alternate_probability * \
                    self.get_utility(x, y, x + dx_w, y + dy_w)
            max_neighbour = max(max_neighbour, value)

        return self.reward[x][y] + self.unit_step_reward + self.discount * max_neighbour

    def value_iteration(self):

        iterations = 0

        print '\n Iteration', iterations
        print_board_mysql_style(
            self.utility_map, self.rows_num, self.cols_num)

        while 1:
            new_utility_map = copy.deepcopy(self.utility_map)
            max_diff = float('-inf')
            iterations += 1

            for i in range(self.rows_num):
                for j in range(self.cols_num):
                    if (i, j) not in self.end_states and self.will_go(i, j):
                        new_utility_map[i][j] = self.new_utility(i, j)
                        if self.utility_map[i][j] != 0:
                            frac_change = (
                                new_utility_map[i][j] - self.utility_map[i][j])/self.utility_map[i][j]
                            max_diff = max(max_diff, abs(frac_change))

            self.utility_map = copy.deepcopy(new_utility_map)

            print '\n Iteration', iterations
            print_board_mysql_style(
                self.utility_map, self.rows_num, self.cols_num)

            if max_diff == float('-inf'):
                continue

            if max_diff < self.delta:
                break

    def get_direction(self, x, y):

        max_neighbour = float('-inf')
        max_dir = '-'

        for (dx, dy) in self.vertical_change:
            value = self.probability * self.get_utility(x, y, x + dx, y + dy)
            for (dx_w, dy_w) in self.horizontal_change:
                value += self.alternate_probability * \
                    self.get_utility(x, y, x + dx_w, y + dy_w)
            if value > max_neighbour:
                max_neighbour = value
                max_dir = self.dir_char[(dx, dy)]

        for (dx, dy) in self.horizontal_change:
            value = self.probability * self.get_utility(x, y, x + dx, y + dy)
            for (dx_w, dy_w) in self.vertical_change:
                value += self.alternate_probability * \
                    self.get_utility(x, y, x + dx_w, y + dy_w)
            if value > max_neighbour:
                max_neighbour = value
                max_dir = self.dir_char[(dx, dy)]

        return max_dir

    def calculate_policy(self):

        for i in range(self.rows_num):
            for j in range(self.cols_num):
                if (i, j) in self.end_states:
                    self.policy[i][j] = 'Goal State' if self.utility_map[i][j] > 0 else 'End State'
                else:
                    if (i, j) in self.walls:
                        self.policy[i][j] = 'Wall'
                    else:
                        self.policy[i][j] = self.get_direction(i, j)

    def print_policy(self):

        print '\n Final Policy'
        print_board_mysql_style(self.policy, self.rows_num, self.cols_num)


if __name__ == '__main__':
    n, m = get_input_list(int)

    board = []
    for _ in range(n):
        board.append(get_input_list(float))

    e, w = get_input_list(int)

    E = []
    for _ in range(e):
        E.append(tuple(get_input_list(int)))

    W = []
    for _ in range(w):
        W.append(tuple(get_input_list(int)))

    start_state = tuple(get_input_list(int))
    unit_step_reward = get_input_value(float)

    mdp = MDP(
        board,            # Reward Board
        E,                # End States
        W,                # Walls
        unit_step_reward, # Step Reward
        0.8,              # Intended Action Probability
        0.1,              # Wrong Action Probability
        0.01,             # Convergence Percentage
        0.99,             # Discount Factor
        n,                # Number of Rows
        m                 # Number of Columns
    )

    mdp.value_iteration()
    mdp.calculate_policy()
    mdp.print_policy()
