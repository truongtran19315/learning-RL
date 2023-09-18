import numpy as np
import pandas as pd
import time

np.random.seed(2)  # Để có thể tạo kết quả giống nhau mỗi lần chạy (đảm bảo tái tạo)

N_STATES = 6  # Độ dài của thế giới 1 chiều
ACTIONS = ['left', 'right']  # Các hành động có sẵn
EPSILON = 0.9  # Tham lam (epsilon-greedy)
ALPHA = 0.1  # Tốc độ học (learning rate)
GAMMA = 0.9  # Hệ số giảm (discount factor)
MAX_EPISODES = 13  # Số tối đa các tình huống
FRESH_TIME = 0.3  # Thời gian mỗi bước di chuyển

def build_q_table(n_states, actions):
    # Tạo một bảng Q-table ban đầu với giá trị ban đầu là 0
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))),
        columns=actions
    )
    return table

def choose_action(state, q_table):
    # Chọn một hành động dựa trên chiến lược epsilon-greedy
    state_actions = q_table.iloc[state, :]
    if (np.random.uniform() > EPSILON) or (state_actions.all() == 0):
        action_name = np.random.choice(ACTIONS)  # Thực hiện hành động ngẫu nhiên
    else:
        action_name = state_actions.idxmax()  # Thực hiện hành động tham lam
    return action_name

def get_env_feedback(S, A):
    # Tương tác của tác nhân với môi trường
    if A == 'right':  # Di chuyển sang phải
        if S == N_STATES - 2:  # Điều kiện dừng
            S_ = 'terminal'
            R = 1
        else:
            S_ = S + 1
            R = 0
    else:  # Di chuyển sang trái
        R = 0
        if S == 0:
            S_ = S  # Đến tường
        else:
            S_ = S - 1
    return S_, R

def update_env(S, episode, step_counter):
    # Cập nhật môi trường hiển thị
    env_list = ['-'] * (N_STATES - 1) + ['T']  # Môi trường của chúng ta: '---------T'
    if S == 'terminal':
        interaction = 'Tình huống %s: Tổng số bước = %s' % (episode + 1, step_counter)
        print('\r{}'.format(interaction), end='')
        time.sleep(2)
        print('\r ', end='')
    else:
        env_list[S] = 'o'
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction), end='')
        time.sleep(FRESH_TIME)

def rl():
    # Phần chính của vòng lặp Q-learning
    q_table = build_q_table(N_STATES, ACTIONS)
    for episode in range(MAX_EPISODES):
        step_counter = 0
        S = 0
        is_terminated = False
        update_env(S, episode, step_counter)
        while not is_terminated:
            A = choose_action(S, q_table)
            S_, R = get_env_feedback(S, A)  # Thực hiện hành động và nhận trạng thái tiếp theo và phần thưởng
            q_predict = q_table.loc[S, A]
            if S_ != 'terminal':
                q_target = R + GAMMA * q_table.iloc[S_].max()  # Trạng thái tiếp theo không phải là trạng thái kết thúc
            else:
                q_target = R  # Trạng thái tiếp theo là trạng thái kết thúc
                is_terminated = True  # Kết thúc tình huống này
            q_table.loc[S, A] += ALPHA * (q_target - q_predict)  # Cập nhật giá trị Q
            S = S_  # Di chuyển đến trạng thái tiếp theo
            update_env(S, episode, step_counter + 1)
            step_counter += 1
    return q_table

if __name__ == "__main__":
    q_table = rl()
    print('\r\nBảng Q:\n')
    print(q_table)
