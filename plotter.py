from gridworld_ma import animate
import numpy as np
import matplotlib.pyplot as plt
import h5py
import time
T1 = []
T2 = []
A1 = []
A2 = []
Q1 = []
Q2 = []
rewards = []
steps = []
# for i in range(1, 6):
with h5py.File('gridworld_ma_5.hdf5', 'r') as gw_ma:
    T1.append(np.asarray(gw_ma['T1']))
    T2.append(np.asarray(gw_ma['T2']))
    rewards.append(np.asarray(gw_ma['rewards_run']))
    A1.append(np.asarray(gw_ma['A1']))
    A2.append(np.asarray(gw_ma['A2']))
    steps.append(np.asarray(gw_ma['steps_run']))
    Q1.append(np.asarray(gw_ma['Q1']))
    Q2.append(np.asarray(gw_ma['Q2']))
    # time.sleep(5)
    # animate(T1[0], T2[0], A1[0], A2[0], wait_time=0.5)
    plt.figure('rewards')
    plt.xlabel('Episodes')
    plt.ylabel('Sum of Rewards during each Episode')
    plt.plot(rewards[0])
    plt.plot(np.mean(np.asarray(rewards), axis=0))
    plt.figure('steps')
    plt.xlabel('Episodes')
    plt.ylabel('Number of Steps on each Episode')
    plt.plot(steps[0])
    plt.plot(np.mean(np.asarray(steps), axis=0))
    plt.show()
