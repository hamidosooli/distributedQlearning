import numpy as np
from action_selection import eps_greedy
import h5py


NUM_EPISODES = 10000

'''If you need to use the big environment in "gridworld_template" make BIG_ENV = True'''
agent = 2
# map = np.zeros((10, 10))
# map[2, 7] = 1  # Agent 1 Goal position
# map[2, 2] = 2  # Agent 2 Goal position
GOAL1 = (2, 7)  # Agent 1 goal state
GOAL2 = (2, 2)  # Agent 2 goal state

if agent == 1:
    GOAL = GOAL1
else:
    GOAL = GOAL2

# Actions
FORWARD = 0
BACKWARD = 1
RIGHT = 2
LEFT = 3
ACTIONS = [FORWARD, BACKWARD, RIGHT, LEFT]
nA = len(ACTIONS)
gamma = .95
Row_num = 10
Col_num = 10


def transition(state, action):
    row = state[0]
    column = state[1]

    row_lim = 9
    column_lim = 9
    if action == 0:  # up
        next_state = (max(row - 1, 0), column)
    elif action == 1:  # down
        next_state = (min(abs(row + 1), row_lim), column)
    elif action == 2:  # right
        next_state = (max(row, 0), min(column + 1, column_lim))
    elif action == 3:  # left
        next_state = (max(row, 0), max(column - 1, 0))
    if next_state == GOAL:
        return next_state, 100
    else:
        return next_state, 0


def rl_agent(alpha=0.5, epsilon=0.1):
    # init_states = np.asarray((np.where(map == 0)[0], np.where(map == 0)[1]))
    # init_states_size = len(init_states[0])
    Q = np.zeros((Row_num, Col_num, nA))
    # Q_star = np.zeros((Row_num, Col_num, nA, init_states_size))


    steps = []
    rewards = []

    # for init in range(init_states_size):
    #     print('initial state ' + str(init+1) + ' of ' + str(init_states_size))
    if agent == 1:
        init_pose = (9, 0)#tuple(init_states[:, init])
    else:
        init_pose = (9, 9)
    for eps in range(NUM_EPISODES):
        s = init_pose

        T = [s]
        R = []
        A = []

        t_step = 0
        while True:
            t_step += 1

            a = eps_greedy(Q[s[0], s[1], :], ACTIONS, epsilon)
            A.append(a)

            sp, re = transition(s, a)
            T.append(sp)
            R.append(re)

            Q[s[0], s[1], a] += alpha * (re + gamma * np.max(Q[sp[0], sp[1], :]) - Q[s[0], s[1], a])

            s = sp

            if sp == GOAL:
                Q[sp[0], sp[1], :] = 0
                steps.append(t_step)
                rewards.append(sum(R))
                print('Episode ' + str(eps + 1) + ' of ' + str(NUM_EPISODES) +
                      ' finished in ' + str(t_step + 1) + ' steps')
                break
    # Q_star[:, :, :, init] = Q
    return T, rewards, A, steps, Q


Trajectory, Reward, ActionHistory, steps, Q_star = rl_agent(alpha=0.5, epsilon=0.2)

with h5py.File(f'gridworld_new_agent{agent}.hdf5', "w") as f:
    f.create_dataset('T', data=Trajectory)
    f.create_dataset('rewards', data=Reward)
    f.create_dataset('A', data=ActionHistory)
    f.create_dataset('steps', data=steps)
    f.create_dataset('Q', data=Q_star)