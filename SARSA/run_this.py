from maze_env import Maze
from RL_brain import SarsaTable

def update():
    for episode in range(100):
        # Quan sát ban đầu
        observation = env.reset()
        
        # RL chọn hành động dựa trên quan sát
        action = RL.choose_action(str(observation))
        
        while True:
            # Môi trường mới
            env.render()
            
            # RL thực hiện hành động và nhận quan sát và phần thưởng
            observation_, reward, done = env.step(action)
            
            # RL chọn hành động dựa trên quan sát tiếp theo
            action_ = RL.choose_action(str(observation_))
            
            # RL học từ chuyển tiếp này (s, a, r, s, a) ==> Sarsa
            RL.learn(str(observation), action, reward, str(observation_), action_)
            
            # Hoán đổi quan sát và hành động
            observation = observation_
            action = action_
            
            # Thoát khỏi vòng lặp khi kết thúc tập
            if done:
                break
        
        # Kết thúc trò chơi
        print('Kết thúc trò chơi')
        env.destroy()

if __name__ == "__main__":
    env = Maze()
    RL = SarsaTable(actions=list(range(env.n_actions)))
    env.after(100, update)
    env.mainloop()
