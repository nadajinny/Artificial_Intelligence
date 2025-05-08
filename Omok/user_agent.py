import numpy as np
from omok import OmokState
import copy

def act(state : OmokState) : 
    
    #  첫 수를 둘 때에는 연산을 하기 어려우므로 시작점을 랜덤으로 잡기 
    if state.num_stones == 0 : 
        return np.random.randint(19), np.random.randint(19)

    depth = 2
    player = True
    unuse, move_node = alpha_beta(depth, state, player, -float('inf'), float('inf'))
    
    if not move_node or move_node[0] is None: 
        while True:
            y_pos, x_pos = np.random.randint(19), np.random.randint(19)
            # state에서 생성된 좌표에 돌이 올려져 있는지 여부 체크
            if state.is_valid_position(x_pos, y_pos):
                break
        return y_pos, x_pos

    move_x = move_node[0]
    move_y = move_node[1]

    return move_y, move_x


def alpha_beta(depth,  state: OmokState, player, alpha, beta): 
    #종료조건이 필요함 - depth가 0이거나, 칸이 모두 찼을 경우
    if depth == 0 or state.num_stones == state.board_size * state.board_size: 
        last_x, last_y = state.history[-1]
        my_stone = state.turn
        return evaluate(state, last_x, last_y, my_stone), (0,0)
    #player일 때!
    if player : 
        returned_node = tuple()
        check_list = checking_moves(state)
        value = -float('inf')
        for x, y in check_list: 
            #상태 복사 필요 
            copied_state = copy.deepcopy(state)
            copied_state.update(x, y)
            
            next_score, unuse = alpha_beta( depth-1, copied_state,False, alpha, beta) 
            
            value = max(value, next_score)
            if value <= next_score : 
                value = next_score
                returned_node = (x,y)
            if value > beta : 
                break
        return value, returned_node
    #상대방의 다음수를 계산할 때
    else : 
        value = float('inf')
        returned_node = tuple()
        check_list = checking_moves(state)
        for x, y in check_list : 
            copied_state = copy.deepcopy(state)
            copied_state.update(x, y)
            next_score, unuse = alpha_beta(depth-1, copied_state, True, alpha, beta)
            if value >= next_score : 
                value = next_score
                returned_node = (x,y)
            
            if value >= beta : 
                beta = value 
            
            if value < alpha : 
                break
        return value, returned_node

def evaluate(state: OmokState, x: int, y: int, my_stone: int) :
    score = 0
    dir = [ (1, 0), (0, 1), (1, 1), (1, -1) ]  

    for dx, dy in dir:
        for history in range(-5, 5): 
            check = []
            end = 0
            for i in range(5):
                nx = x + (history + i) * dx
                ny = y + (history + i) * dy
                if 0 <= nx < 19 and 0 <= ny < 19:
                    check.append(state.game_board[ny][nx])
                else:
                    check.append(None) 
                    end += 1

            if check.count(None) > 0:
                continue  

            count = check.count(my_stone)
            another = check.count(-my_stone)

            if another == 0:
                # 방해 없는 순수한 연속돌
                get_score = {1: 8, 2: 80, 3: 800, 4: 80000, 5: 1000000}
                score += get_score.get(count, 0)*1.3

            elif count == 0:
                # 방어 고려: 상대방 연속
                minus_score = {1: 8, 2: 80, 3: 800, 4: 80000, 5: 1000000}
                score -= minus_score.get(another, 0)*0.8
    return score

def checking_moves(state : OmokState): 
    size = state.board_size
    board = state.game_board
    moves = set()

    for x, y in state.history[-4:]: 
        for dy in range(-3, 4): 
            for dx in range(-3, 4): 
                nx = x + dx
                ny = y + dy 
                if 0 <= ny < size and 0 <= nx < size : 
                    if board[ny][nx] == 0 : 
                        moves.add((nx, ny)) 

    if not moves : 
        for y in range(size): 
            for x in range(size): 
                if board[y][x] == 0: 
                    moves.add((x, y))
                    
    return moves
