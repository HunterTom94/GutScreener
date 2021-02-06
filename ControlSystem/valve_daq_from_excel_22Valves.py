import nidaqmx
from nidaqmx.constants import (LineGrouping)
import numpy as np
from time import time
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--reset", default=0, type=int)
parser.add_argument("--valve", default='1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22', type=str)

args = parser.parse_args()
reset = args.reset
valve_ls = args.valve

signal_ls = np.array([int(valve_arg) for valve_arg in valve_ls.split(',')] + [23, 24]) - 1

schedule_resolution = -3  # input integer N where resolution is 10^N second
schedule_resolution_factor = np.power(10, -schedule_resolution)

camera_sampling_rate = 1 # s

valve_1_port = [3, 1, 0]
valve_2_port = [3, 1, 1]
valve_3_port = [3, 1, 2]
valve_4_port = [3, 1, 3]
valve_5_port = [3, 1, 4]
valve_6_port = [3, 1, 5]
valve_7_port = [3, 1, 6]

valve_8_port = [3, 2, 0]
valve_9_port = [3, 2, 1]
valve_10_port = [3, 2, 2]
valve_11_port = [3, 2, 3]
valve_12_port = [3, 2, 4]
valve_13_port = [3, 2, 6]
valve_14_port = [3, 2, 7]

valve_15_port = [3, 0, 0]
valve_16_port = [3, 0, 1]
valve_17_port = [3, 0, 2]
valve_18_port = [3, 0, 3]
valve_19_port = [3, 0, 4]
valve_20_port = [3, 0, 5]
valve_21_port = [3, 0, 6]
valve_22_port = [3, 0, 7]

camera_port = [3, 1, 7]
pump_port = [3, 2, 5]

port_ls = [valve_1_port, valve_2_port, valve_3_port, valve_4_port, valve_5_port, valve_6_port, valve_7_port, valve_8_port,
           valve_9_port, valve_10_port, valve_11_port, valve_12_port, valve_13_port, valve_14_port, valve_15_port,
           valve_16_port, valve_17_port, valve_18_port, valve_19_port, valve_20_port, valve_21_port,
           valve_22_port, camera_port, pump_port]

def excel2schedule(excel):
    total_time = excel.iloc[1,:].sum()
    schedule = np.zeros((24, total_time*schedule_resolution_factor))
    schedule[-1, :] = schedule[0:-2].any(axis=0).astype('uint8')

    signal_hold = 0.01
    assert camera_sampling_rate > signal_hold, 'Frame Rate Too High!'
    sample_num = int(total_time / camera_sampling_rate)
    for sample_ind in range(sample_num + 1):
        sample_start = int((camera_sampling_rate * sample_ind) * schedule_resolution_factor)
        sample_end = int(signal_hold * schedule_resolution_factor + sample_start)
        schedule[-2, sample_start:sample_end] = 1

    cum_time = 0

    for column in excel:
        valve_ind, span, camera_bool = excel[column].values
        if valve_ind != 0:
            schedule[valve_ind - 1, cum_time*schedule_resolution_factor:(cum_time+span)*schedule_resolution_factor] = 1


        if not camera_bool:
            schedule[-2, cum_time*schedule_resolution_factor:(cum_time+span)*schedule_resolution_factor] = 0

        cum_time += span
    return schedule

def schedule_exe(schedule_matrix, port_ls, reset=0):
    assert schedule_matrix.shape[0] == len(port_ls), 'Schedule Numer Not Equal to Port Number'
    channel_ls = 'Dev{}/port{}/line{}'.format(port_ls[0][0], port_ls[0][1], port_ls[0][2])
    print('{} online'.format(channel_ls))
    for valve_port in port_ls[1:]:
        valve_port_str = 'Dev{}/port{}/line{}'.format(valve_port[0], valve_port[1], valve_port[2])
        channel_ls += ', {}'.format(valve_port_str)
        print('{} online'.format(valve_port_str))

    mask = np.zeros(schedule_matrix.shape)
    mask[signal_ls, :] = 1
    schedule_matrix *= mask

    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(channel_ls, line_grouping=LineGrouping.CHAN_PER_LINE)
        start_time = time()
        time_elapsed = time() - start_time
        while int(time_elapsed * schedule_resolution_factor) < schedule_matrix.shape[1]:
            if reset:
                task.write(np.zeros((len(port_ls),)).astype(bool).tolist())
            else:
                task.write(schedule_matrix[:, int(time_elapsed * schedule_resolution_factor)].astype(bool).tolist())
            time_elapsed = time() - start_time
            # print(time_elapsed)
            # print(schedule_matrix[:, int(time_elapsed * schedule_resolution_factor)].astype(bool).tolist())

        print('Schedule Finished')


if __name__ == "__main__":
    excel = pd.read_excel('Schedule.xlsx', header=None, index_col=0).iloc[:3,:].astype('int16')
    schedule_matrix = excel2schedule(excel)

    schedule_exe(schedule_matrix, port_ls, reset=reset)
