
import sys
import copy
import time
import heapq as hq
visited = {}

def read(path):
    f = open(path, 'r')
    contents = f.readlines()
    f.close()
    print(contents)
    grid = []
    for i in range(len(contents)):
        lst = []
        for n in range(len(contents[i])):
            lst.append(contents[i][n])
        if lst[-1] == '\n' and lst[0] != lst[-1]:
            grid.append(lst[:-1])
        elif lst != []:
            grid.append(lst)
    return grid 

def output_format(grid):
    s = ""

    for i in range(len(grid)):
        for n in range(len(grid[i])):
            s = s + grid[i][n]
        s = s + '\n'
    return s

def get_pieces(board, util=False):
    red = []
    black = []
    red_king_count = 0
    black_king_count = 0
    for i in range(len(board)):
        for n in range(len(board[i])):
            if board[i][n] == 'r' or board[i][n] == 'R':
                if board[i][n] == 'R':
                    red_king_count += 1
                red.append((i,n))
            elif board[i][n] == 'b' or board[i][n] == 'B':
                if board[i][n] == 'B':
                    black_king_count += 1
                black.append((i,n))
    if util:
        return red, black, red_king_count, black_king_count
    return red, black

def utility(board):
    count_red = 0
    count_black = 0

    for i in range(len(board)):
        for n in range(len(board[i])):
            if board[i][n] == 'r':
                count_red += 1
            elif board[i][n] == 'R':
                count_red += 2
            elif board[i][n] == 'b':
                count_black += 1
            elif board[i][n] == 'B':
                count_black += 2
    
    return count_red - count_black

def advanced_utility(board):
    red = 0
    black = 0
    for i in range(len(board)):
        for n in range(len(board[i])):
            if i == 0 or i == 7 or n == 0 or n == 7:
                weight = 1
            elif i == 1 or i == 6 or n == 6 or n == 1:
                weight = 2
            else:
                weight = 3
            if board[i][n] == 'r':
                red += 1 * weight
            elif board[i][n] == 'R':
                red += 2 * weight
            elif board[i][n] == 'b':
                black += 1 * weight
            elif board[i][n] == 'B':
                black += 2 * weight
    return red - black

def adv_utility(board):
    red, black, red_kings, black_kings = get_pieces(board, True)
    red_moves = get_successors(board, red, black, 'r', util=True)
    black_moves = get_successors(board, red, black, 'b', util=True)
    return (len(red_moves) + red_kings) - (len(black_moves) + black_kings)

def get_successors(grid, red, black, r_or_b, cap=False, util=False):
    successors = []
    captures = []
    if r_or_b == 'r' or r_or_b == 'R':
        
        for m in range(len(red)):
            
            i = red[m][0]
            n = red[m][1]
            assert(grid[i][n] == 'r' or grid[i][n] == 'R')
            if i - 1 >= 0 and n - 1 >= 0:
                
                if grid[i - 1][n - 1] == '.':
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    if i - 1 == 0:
                        grid_copy[i - 1][n - 1] = 'R'
                    else:
                        grid_copy[i - 1][n - 1] = grid[i][n]
                    successors.append(grid_copy)
                elif (grid[i - 1][n - 1] == 'b' or grid[i - 1][n - 1] == 'B') and i - 2 >= 0 and n - 2 >= 0 and grid[i - 2][n - 2] == '.':
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    grid_copy[i - 1][n - 1] = '.'
                    if i - 2 == 0:
                        grid_copy[i - 2][n - 2] = 'R'
                        captures.append(grid_copy)
                    else:
                        grid_copy[i - 2][n - 2] = grid[i][n]
                        captures = captures + get_successors(grid_copy, [(i - 2, n - 2)], [], 'r', True)

            if i - 1 >= 0 and n + 1 < len(grid[i]):
                
                if grid[i - 1][n + 1] == '.':
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    if i - 1 == 0:
                        grid_copy[i - 1][n + 1] = 'R'
                    else:
                        grid_copy[i - 1][n + 1] = grid[i][n]
                    successors.append(grid_copy)
                elif (grid[i - 1][n + 1] == 'b' or grid[i - 1][n + 1] == 'B') and i - 2 >= 0 and n + 2 < len(grid[i]) and grid[i - 2][n + 2] == '.':
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    grid_copy[i - 1][n + 1] = '.'
                    if i - 2 == 0:
                        grid_copy[i - 2][n + 2] = 'R'
                        captures.append(grid_copy)
                    else:
                        grid_copy[i - 2][n + 2] = grid[i][n]
                        captures = captures + get_successors(grid_copy, [(i - 2, n + 2)], [], 'r', True)
            

            if grid[i][n] == 'R' and i + 1 < len(grid) and n + 1 < len(grid[i]):

                if grid[i + 1][n + 1] == '.':
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    grid_copy[i + 1][n + 1] = grid[i][n]
                    successors.append(grid_copy)
                elif ((grid[i + 1][n + 1] == 'b' or grid[i + 1][n + 1] == 'B') and i + 2 < len(grid)
                 and n + 2 < len(grid[i]) and grid[i + 2][n + 2] == '.'):
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    grid_copy[i + 1][n + 1] = '.'
                    grid_copy[i + 2][n + 2] = grid[i][n]
                    captures = captures + get_successors(grid_copy, [(i + 2, n + 2)], [], 'r', True)
            
            if grid[i][n] == 'R' and i + 1 < len(grid) and n - 1 >= 0:
                
                if grid[i + 1][n - 1] == '.':
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    grid_copy[i + 1][n - 1] = grid[i][n]
                    successors.append(grid_copy)
                elif (grid[i + 1][n - 1] == 'b' or grid[i + 1][n - 1] == 'B') and i + 2 < len(grid) and n - 2 >= 0 and grid[i + 2][n - 2] == '.':
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    grid_copy[i + 1][n - 1] = '.'
                    grid_copy[i + 2][n - 2] = grid[i][n]
                    captures = captures + get_successors(grid_copy, [(i + 2, n - 2)], [], 'r', True)

    else:
        for m in range(len(black)):
            
            i = black[m][0]
            n = black[m][1]
            
            assert(grid[i][n] == 'b' or grid[i][n] == 'B')
            if i + 1 < len(grid) and n + 1 < len(grid[i]):
                
                if grid[i + 1][n + 1] == '.':
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    if i + 1 == len(grid) - 1:
                        grid_copy[i + 1][n + 1] = 'B'
                    else:
                        grid_copy[i + 1][n + 1] = grid[i][n]
                    successors.append(grid_copy)
                elif (grid[i + 1][n + 1] == 'r' or grid[i + 1][n + 1] == 'R') and i + 2 < len(grid) and n + 2 < len(grid[i]) and grid[i + 2][n + 2] == '.':
                    assert(n + 2 < len(grid[i]))
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    grid_copy[i + 1][n + 1] = '.'
                    if i + 2 == len(grid) - 1:
                        grid_copy[i + 2][n + 2] = 'R'
                        captures.append(grid_copy)
                    else:
                        assert(len(grid_copy) == len(grid) == len(grid[i]) == len(grid_copy[i]) and i + 2 < len(grid))
                        assert(n + 2 < len(grid[i]))
                        grid_copy[i + 2][n + 2] = grid[i][n]
                        captures = captures + get_successors(grid_copy, [], [(i + 2, n + 2)], 'b', True)

            if i + 1 < len(grid) and n - 1 >= 0:
                
                if grid[i + 1][n - 1] == '.':
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    if i + 1 == len(grid) - 1:
                        grid_copy[i + 1][n - 1] = 'B'
                    else:
                        grid_copy[i + 1][n - 1] = grid[i][n]
                    successors.append(grid_copy)
                elif ((grid[i + 1][n - 1] == 'r' or grid[i - 1][n - 1] == 'R') and i + 2 < len(grid) and n - 2 >= 0 
                        and grid[i + 2][n - 2] == '.'):
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    grid_copy[i + 1][n - 1] = '.'
                    if i + 2 == len(grid) - 1:
                        grid_copy[i + 2][n - 2] = 'B'
                        captures.append(grid_copy)
                    else:
                        grid_copy[i + 2][n - 2] = grid[i][n]
                        captures = captures + get_successors(grid_copy, [], [(i + 2, n - 2)], 'b', True)
            

            if grid[i][n] == 'B' and i - 1 >= 0 and n - 1 >= 0:

                if grid[i - 1][n - 1] == '.':
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    grid_copy[i - 1][n - 1] = grid[i][n]
                    successors.append(grid_copy)
                elif ((grid[i - 1][n - 1] == 'r' or grid[i - 1][n - 1] == 'R') 
                and i - 2 >=0 and n - 2 >= 0 and grid[i - 2][n - 2] == '.'):
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    grid_copy[i - 1][n - 1] = '.'
                    grid_copy[i - 2][n - 2] = grid[i][n]
                    captures = captures + get_successors(grid_copy, [], [(i - 2, n - 2)], 'b', True)
            
            if grid[i][n] == 'B' and i - 1 >= 0 and n + 1 < len(grid[i]):
                if grid[i - 1][n + 1] == '.':
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    grid_copy[i - 1][n + 1] = grid[i][n]
                    successors.append(grid_copy)
                elif (grid[i - 1][n + 1] == 'r' or grid[i - 1][n + 1] == 'R') and i - 2 >= 0 and n + 2 < len(grid[i]) and grid[i - 2][n + 2] == '.':
                    grid_copy = copy.deepcopy(grid)
                    grid_copy[i][n] = '.'
                    grid_copy[i - 1][n + 1] = '.'
                    grid_copy[i - 2][n + 2] = grid[i][n]
                    captures = captures + get_successors(grid_copy, [], [(i - 2, n + 2)], 'b', True)

    # in the end
    if util:
        return captures + successors
    if captures == [] and not cap:
        return successors
    elif cap and captures == []:
        return [grid]
    elif captures != []:
        return captures

def minimax_max(board, depth):
    
    red_pieces, black_pieces = get_pieces(board)
    successors = get_successors(board, red_pieces, black_pieces, 'r')
    best = []
    if len(successors) == 0 or depth == 0:
        return best, utility(board)
    value = -999999999
    for move in successors:
        nxt_move, nxt_val = minimax_min(move, depth - 1)
        if value < nxt_val:
            value, best = nxt_val, move
    return best, value


def minimax_min(board, depth):
    red_pieces, black_pieces = get_pieces(board)
    successors = get_successors(board, red_pieces, black_pieces, 'b')
    best = []
    if len(successors) == 0 or depth == 0:
        return best, utility(board)
    value = 999999999
    for move in successors:
        nxt_move, nxt_val = minimax_max(move, depth - 1)
        if value > nxt_val:
            value, best = nxt_val, move
    return best, value

def compute_heuristics(successors):
    lst = []
    for board in successors:
        tup = (advanced_utility(board), board)
        hq.heappush(lst, tup)
    return lst

def alpha_beta_max(board, alpha, beta, depth):
    red_pieces, black_pieces = get_pieces(board)
    successors = get_successors(board, red_pieces, black_pieces, 'r')
    lst = compute_heuristics(successors)
    best = []
    if len(successors) == 0 or depth == 0:
        return best, advanced_utility(board)
    value = -999999999
    for move in lst:
        key = output_format(move[1])
        if key in visited and visited[key][0] == alpha and visited[key][1] == beta and visited[key][2] == depth and visited[key][3] == 'r':
            nxt_val = visited[key][4]
        else:
            nxt_move, nxt_val = alpha_beta_min(move[1], alpha, beta, depth - 1)
            visited[output_format(move[1])] = (alpha, beta, depth - 1, 'b', nxt_val)
        if value < nxt_val:
            value, best = nxt_val, move[1]
        if value >= beta: return best, value
        alpha = max(alpha, value)
        
    return best, value

def alpha_beta_min(board, alpha, beta, depth):
    red_pieces, black_pieces = get_pieces(board)
    successors = get_successors(board, red_pieces, black_pieces, 'b')
    lst = compute_heuristics(successors)
    best = []
    if len(successors) == 0 or depth == 0:
        return best, advanced_utility(board)
    value = 999999999
    for move in lst:
        key = output_format(move[1])
        if key in visited and visited[key][0] == alpha and visited[key][1] == beta and visited[key][2] == depth and visited[key][3] == 'b':
            nxt_val = visited[key][4]
        else:
            nxt_move, nxt_val = alpha_beta_max(move[1], alpha, beta, depth - 1)
            visited[output_format(move[1])] = (alpha, beta, depth - 1, 'r', nxt_val)
        if value > nxt_val:
            value, best = nxt_val, move[1]
        if value <= alpha: return best, value
        beta = min(beta, value)
        
    return best, value

if __name__ == "__main__":
    start_time = time.time()
    array = read(sys.argv[1])
    red, black = get_pieces(array)
    print(output_format(array))
    # successors = get_successors(array, red, black, 'r', False)
    # print(len(successors))
    # for grid in successors:
    #     print(output_format(grid))
    final = output_format(alpha_beta_max(array, -999999999, 999999999, 10)[0])
    # final = output_format(minimax_max(array, 7)[0])
    # final = output_format(alpha_beta_min(array, -999999999, 999999999, 10)[0])
    print(final)
    f = open(sys.argv[2], "w")
    f.write(final)
    f.close()
    print("--- %s seconds ---" % (time.time() - start_time))