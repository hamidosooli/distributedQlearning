import numpy as np
import matplotlib.pyplot as plt
import h5py
from gridworld_ma import Qcheck

map = np.zeros((10, 10))
map[2, 7] = 1  # Agent 1 Goal position
map[2, 2] = 2  # Agent 2 Goal position
init_pose1 = (9, 0)
init_pose2 = (9, 9)


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

    if map[next_state] == 1 or map[next_state] == 2:
        return next_state, 100
    else:
        return next_state, 0


with h5py.File('gridworld_agent1.hdf5', "r") as f1:
    T1 = np.asarray(f1['T'])
    A1 = np.asarray(f1['A'])
    Q1 = np.asarray(f1['Q'])
    rewards1 = np.asarray(f1['rewards'])
    steps1 = np.asarray(f1['steps'])


    with h5py.File('gridworld_agent2.hdf5', "r") as f2:
        T2 = np.asarray(f2['T'])
        A2 = np.asarray(f2['A'])
        Q2 = np.asarray(f2['Q'])
        rewards2 = np.asarray(f2['rewards'])
        steps2 = np.asarray(f2['steps'])
        Qcheck(Q2, init_pose1, init_pose2)
        print('Beginning the search')
        for i in range(10000):
            s1 = init_pose1
            s2 = init_pose2
            traj1 = [s1]
            traj2 = [s2]
            T1 = []
            T2 = []
            T2_num = []
            a2_steps = 0
            while True:
                a1 = np.argmax(Q1[s1[0], s1[1], :])
                sp1, re1 = transition(s1, a1)
                traj1.append(sp1)

                a2 = np.argmax(Q2[s2[0], s2[1], :])
                sp2, re2 = transition(s2, a2)
                traj2.append(sp2)

                s1 = sp1
                s2 = sp2
                if map[sp1[0], sp1[1]] == 1:
                    T1.append(traj1)
                    break
            while map[sp2[0], sp2[1]] != 2:
                a2_steps += 1
                a2 = np.argmax(Q2[s2[0], s2[1], :])
                sp2, re2 = transition(s2, a2)

                traj2.append(sp2)
                s2 = sp2
            T2.append(traj2)
            T2_num.append(a2_steps)
            print(f'{i+1} trajectory checked')

with h5py.File('gridworld_results.hdf5', "w") as f:
    f.create_dataset('T1', data=T1)
    f.create_dataset('T2', data=T2)
    f.create_dataset('traj1', data=traj1)
    f.create_dataset('traj2', data=traj2)
    f.create_dataset('T2_num', data=T2_num)