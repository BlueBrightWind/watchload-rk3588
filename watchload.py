import argparse
import curses
import sys

from monitor import Monitor
from utils import change_mode


def parse_show_param(params):
    valid_chars = set('tcgmnr')
    value_set = set(params)
    
    if not value_set.issubset(valid_chars):
        print("Show params error: Only 't,c,g,n,m,r' are allowed.")
        sys.exit(1)
    
    if len(params) != len(value_set):
        print("Show params error: Duplicate characters are not allowed.")
        sys.exit(1)

    devices = []
    for device in params:
        devices.append('TEMP') if device == 't' else None
        devices.append('CPU') if device == 'c' else None
        devices.append('GPU') if device == 'g' else None
        devices.append('NPU') if device == 'n' else None
        devices.append('RGA') if device == 'r' else None
        devices.append('MEM') if device == 'm' else None
    
    return devices


def parse_temp_param(params):
    valid_chars = set('cgn')
    value_set = set(params)
    
    if not value_set.issubset(valid_chars):
        print("Temperature params error: Only 'c,g,n' are allowed.")
        sys.exit(1)
    
    if len(params) != len(value_set):
        print("Temperature params error: Duplicate characters are not allowed.")
        sys.exit(1)

    devices = []
    for device in params:
        devices.append('CPU') if device == 'c' else None
        devices.append('GPU') if device == 'g' else None
        devices.append('NPU') if device == 'n' else None
    
    return devices


def parse_mode_param(params):
    if params is None:
        return None
    
    modes = {'ondemand', 'performance', 'powersave'}
    if params not in modes:
        print("Mode params error: Only 'ondemand', 'performance', 'powersave' are allowed.")
        sys.exit(1)

    return params


def main(stdscr, interval, devices, temps):
    monitor = Monitor(stdscr, interval, devices, temps)
    monitor.loop_back()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, default=None, help='mode selection (ondemand/performance/powersave)')
    parser.add_argument('-s', '--show', type=str, default='tcgmnr', help='show options (combination of c,g,n,r,m)')
    parser.add_argument('-t', '--temp', type=str, default='cgn', help='show temperatures (combination of c,g,n)')
    parser.add_argument('-n', '--intv', type=float, default=1, help='update interval time (seconds)')
    args = parser.parse_args()

    interval = args.intv
    devices = parse_show_param(args.show)
    temps = parse_temp_param(args.temp)
    mode = parse_mode_param(args.mode)

    if mode is not None:
        print(f"Setting device mode to {mode} ......")
        change_mode(mode)
        print(f"Current device mode: {mode}")
        sys.exit(0)

    try:
        curses.initscr()
        curses.curs_set(0)
        curses.start_color() 
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.wrapper(main, interval, devices, temps)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        pass
