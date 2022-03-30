import matplotlib.pyplot as plt
import numpy as np
from action_selection import eps_greedy
from gridworld_ma import animate
import h5py


NUM_RUNS = 50
NUM_EPISODES = 250000
MAX_STEP = 1000
MAX_REW = 100
MID_REW = 1
MIN_REW = 0.01
Row_num = 10
Col_num = 10
RIGHT = 0
LEFT = 1
FORWARD = 2
BACKWARD = 3
ACTIONS = [RIGHT, LEFT, FORWARD, BACKWARD]
Act_num = len(ACTIONS)

Agent_num = 2
gamma = .99

map = np.zeros((10, 10))
map[0, 7] = 1  # Agent 1 Goal position
map[0, 2] = 2  # Agent 2 Goal position

# global game_mat1, game_mat2
# game_mat1 = np.zeros((Row_num, Col_num, Act_num, Act_num))
# game_mat2 = np.zeros((Row_num, Col_num, Act_num, Act_num))


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

    return next_state

global flag1
flag1 = True
def reward(next_state1, next_state2, t_step):
    global flag1
    if map[next_state1] == 1 and map[next_state2] == 2:
        return MAX_REW, MAX_REW
    elif (map[next_state1] == 1 or map[next_state2] == 2) and flag1:
        flag1 = False
        return MIN_REW, MIN_REW
    # elif (((map[min(next_state1[0]+1, 9), next_state1[1]] == 1) or
    #        (map[max(next_state1[0]-1, 0), next_state1[1]] == 1) or
    #        (map[next_state1[0], min(next_state1[1]+1, 9)] == 1) or
    #        (map[next_state1[0], max(next_state1[1]-1, 0)] == 1) or
    #       (map[max(next_state1[0]-1, 0), max(next_state1[1]-1, 0)] == 1) or
    #       (map[min(next_state1[0]+1, 9), min(next_state1[1]+1, 9)] == 1) or
    #       (map[max(next_state1[0]-1, 0), min(next_state1[1]+1, 9)] == 1) or
    #       (map[min(next_state1[0]+1, 9), max(next_state1[1]-1, 0)] == 1)) and
    #        ((map[min(next_state2[0]+1, 9), next_state2[1]] == 2) or
    #         (map[max(next_state2[0]-1, 0), next_state2[1]] == 2) or
    #         (map[next_state2[0], min(next_state2[1]+1, 9)] == 2) or
    #         (map[next_state2[0], max(next_state2[1]-1, 0)] == 2) or
    #         (map[max(next_state2[0]-1, 0), max(next_state2[1]-1, 0)] == 2) or
    #         (map[min(next_state2[0]+1, 9), min(next_state2[1]+1, 9)] == 2) or
    #         (map[max(next_state2[0]-1, 0), min(next_state2[1]+1, 9)] == 2) or
    #         (map[min(next_state2[0]+1, 9), max(next_state2[1]-1, 0)] == 2))):
    #     return MID_REW, MID_REW
    else:
        return 0, 0


def q_learning(epsilon=0.1):
    global game_mat1, game_mat2
    flag = True
    finish_eps = 1
    re1 = 0
    re2 = 0
    eps = 0
    Q1 = np.zeros((Row_num, Col_num, Act_num))
    Q2 = np.zeros((Row_num, Col_num, Act_num))

    steps = []
    rewards = []
    init_pose1 = [9, 0]#tuple(np.asarray((np.where(map == 0)[0], np.where(map == 0)[1]))[:,
    #                    np.random.randint(len(np.asarray((np.where(map == 0)[0]))))])
    init_pose2 = [9, 9]#tuple(np.asarray((np.where(map == 0)[0], np.where(map == 0)[1]))[:,
    #                    np.random.randint(len(np.asarray((np.where(map == 0)[0]))))])
    # if init_pose2 == init_pose1:
    #     init_pose2 = tuple(np.asarray((np.where(map == 0)[0], np.where(map == 0)[1]))[:,
    #                        np.random.randint(len(np.asarray((np.where(map == 0)[0]))))])

    for eps in range(NUM_EPISODES):
        flag = True
        global flag1
        flag1 = True
    # while flag or finish_eps > 0:

        # eps += 1
        # if eps % (NUM_EPISODES / 1000) == 0:
        #     s1 = tuple(np.asarray((np.where(map == 0)[0], np.where(map == 0)[1]))[:,
        #                np.random.randint(len(np.asarray((np.where(map == 0)[0]))))])
        #     s2 = tuple(np.asarray((np.where(map == 0)[0], np.where(map == 0)[1]))[:,
        #                np.random.randint(len(np.asarray((np.where(map == 0)[0]))))])
        #     if s2 == s1:
        #         s2 = tuple(np.asarray((np.where(map == 0)[0], np.where(map == 0)[1]))[:,
        #                    np.random.randint(len(np.asarray((np.where(map == 0)[0]))))])
        # else:
        s1 = init_pose1
        s2 = init_pose2
        T1 = [s1]
        R1 = []
        A1 = []

        T2 = [s2]
        R2 = []
        A2 = []

        t_step = 0
        while True:

            t_step += 1
            # if not flag:
            #     epsilon /= t_step
###############################################################
            # if np.count_nonzero(game_mat1[s1[0], s1[1], :, :]) == Act_num * Act_num:
            #     # print('GT')
            #     a1 = np.argmax(np.argmax(game_mat1[s1[0], s1[1], :, :], axis=0))
            # else:
            #     # print('non-GT')
            #     a1 = np.random.choice(ACTIONS)#eps_greedy(Q1[s1[0], s1[1], :], ACTIONS, epsilon)
###############################################################
            a1 = eps_greedy(Q1[s1[0], s1[1], :], ACTIONS, epsilon)
            A1.append(a1)
###############################################################
            # if np.count_nonzero(game_mat2[s2[0], s2[1], :, :]) == Act_num * Act_num:
            #     # print('GT')
            #     a2 = np.argmax(np.argmax(game_mat2[s2[0], s2[1], :, :], axis=1))
            # else:
            #     # print('non-GT')
            #     a2 = np.random.choice(ACTIONS)#eps_greedy(Q2[s2[0], s2[1], :], ACTIONS, epsilon)
###############################################################
            a2 = eps_greedy(Q2[s2[0], s2[1], :], ACTIONS, epsilon)
            A2.append(a2)
            if s1 != (3, 4):
                sp1 = transition(s1, a1)
            T1.append(sp1)

            if s2 != (0, 2):
                sp2 = transition(s2, a2)
            T2.append(sp2)

            re1, re2 = reward(sp1, sp2, t_step)
            if re1!=0:
                print(re1, re2)
            R1.append(re1)
            R2.append(re2)

            Q1[s1[0], s1[1], a1] = np.max([re1 + gamma * np.max(Q1[sp1[0], sp1[1], :]), Q1[s1[0], s1[1], a1]])
            Q2[s2[0], s2[1], a2] = np.max([re2 + gamma * np.max(Q2[sp2[0], sp2[1], :]), Q2[s2[0], s2[1], a2]])
#################################################################################
            # game_mat1[s1[0], s1[1], a1, a2] = re1 + gamma * np.max(Q1[sp1[0], sp1[1], :])
            # game_mat2[s2[0], s2[1], a1, a2] = re2 + gamma * np.max(Q2[sp2[0], sp2[1], :])
#################################################################################

            s1 = sp1
            s2 = sp2
            if re1 + re2 == 2*(MAX_REW) or re1 + re2 == 2*(MIN_REW) or t_step == MAX_STEP:
            #     flag = False
            #     finish_eps = eps
            # if not flag:
            #     finish_eps -= 1
            # if not flag:
                # Q1[sp1[0], sp1[1], :] = 0
                # Q2[sp2[0], sp2[1], :] = 0
                steps.append(t_step)
                rewards.append(np.sum(R1+R2))
                print(f'Episode {eps + 1} finished in {t_step} steps')
                break

    return T1, T2, rewards, A1, A2, steps, Q1, Q2

# for i in range(4, 11):
T1, T2, rewards, A1, A2, steps, Q1, Q2 = q_learning(epsilon=0.2)
f = h5py.File('gridworld_ma_GT.hdf5', "w")
f.create_dataset('T1', data=T1)
f.create_dataset('T2', data=T2)
f.create_dataset('rewards_run', data=rewards)
f.create_dataset('A1', data=A1)
f.create_dataset('A2', data=A2)
f.create_dataset('steps_run', data=steps)
f.create_dataset('Q1', data=Q1)
f.create_dataset('Q2', data=Q2)
# animate(T1, T2, A1, A2, wait_time=0.5)

# plt.figure('rewards')
# plt.xlabel('Episodes')
# plt.ylabel('Sum of Rewards during each Episode')
# plt.plot(rewards)
# plt.figure('steps')
# plt.xlabel('Episodes')
# plt.ylabel('Number of Steps on each Episode')
# plt.plot(steps)
# plt.show()
