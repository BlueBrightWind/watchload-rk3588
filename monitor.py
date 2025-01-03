import os
import subprocess
import re
import psutil
import math
import argparse
import curses
import time

logo = [
 "====================================",
 " __  __             _ _             ",
 "|  \/  | ___  _ __ (_) |_ ___  _ __ ",
 "| |\/| |/ _ \| '_ \| | __/ _ \| '__|",
 "| |  | | (_) | | | | | || (_) | |   ",
 "|_|  |_|\___/|_| |_|_|\__\___/|_|   ",
 "                                    ",
 "====================================",
]

DEVICES = ['CPU', 'GPU', 'MEM', 'NPU', 'RGA']

INTERVAL = 1

class Order(object):
    def __init__(self):
        self.title_length = 3
        self.column = 1
        self.offset_dict = {'CPU': 8, 'GPU': 1, 'NPU': 3, 'RGA': 3, 'MEM': 2}

    def update_dict(self, label, value):
        self.offset_dict[label] = value

    def update_column(self, column):
        self.column = column
    
    @property
    def total_offset(self):
        offset = 0
        for key, value in self.offset_dict.items():
            if key in DEVICES:
                offset += math.ceil(value / self.column) + self.title_length
        return offset

    @property
    def cpu_offset(self):
        index = DEVICES.index('CPU')
        offset = 0
        for i in range(index):
            offset += math.ceil(self.offset_dict[DEVICES[i]] / self.column) + self.title_length
        return offset
    
    @property
    def gpu_offset(self):
        index = DEVICES.index('GPU')
        offset = 0
        for i in range(index):
            offset += math.ceil(self.offset_dict[DEVICES[i]] / self.column) + self.title_length
        return offset
    
    @property
    def npu_offset(self):
        index = DEVICES.index('NPU')
        offset = 0
        for i in range(index):
            offset += math.ceil(self.offset_dict[DEVICES[i]] / self.column) + self.title_length
        return offset
    
    @property
    def rga_offset(self):
        index = DEVICES.index('RGA')
        offset = 0
        for i in range(index):
            offset += math.ceil(self.offset_dict[DEVICES[i]] / self.column) + self.title_length
        return offset
    
    @property
    def mem_offset(self):
        index = DEVICES.index('MEM')
        offset = 0
        for i in range(index):
            offset += math.ceil(self.offset_dict[DEVICES[i]] / self.column) + self.title_length
        return offset  

ORDER = Order()

class BaseRenderer(object):
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.y_offset = 0
        self.x_offset = 2
        self.window_max_width = 0
        self.container_max_width = 0

    def clear_line(self, line):
        self.stdscr.addstr(line, 0, ' ' * self.window_max_width)

    def change_width(self, window_width, container_width):
        self.window_max_width = window_width
        self.container_max_width = container_width

    def draw_mode(self, label, values):
        self.clear_line(self.y_offset+0)
        self.stdscr.addstr(self.y_offset+0, self.x_offset, '|' + '-'*(self.container_max_width-2) + '|')
        self.clear_line(self.y_offset+1)
        self.stdscr.addstr(self.y_offset+1, self.x_offset, f"| {label} MODE: {' '.join(str(mode) for mode in values)}".ljust(self.container_max_width-2) + " |")
        self.clear_line(self.y_offset+2)
        self.stdscr.addstr(self.y_offset+2, self.x_offset, '|' + '-'*(self.container_max_width-2) + '|')

    def draw_bar(self, label, values, freqs=None, offset=3):
        prefix_offset_length = 7 + 7 + 10 + 1
        suffix_offset_length = 2
        column = ORDER.column
        column_width = math.floor(self.container_max_width / column)
        bar_max_width = column_width - prefix_offset_length - suffix_offset_length
        y_offset = self.y_offset + offset

        for i, value in enumerate(values):
            bar_length = int((value / 100) * bar_max_width)
            color = 1 if value < 50 else 2  # 确定条形图颜色: 低于 50% 使用颜色1，其他使用颜色2
            if freqs is not None:
                freq = format(freqs[i], ".1f") + " GHz"
            else:
                freq = ""
            if len(values) > 1:
                self.stdscr.addstr(y_offset, self.x_offset + (i % column) * column_width, f"| {label}{i}: ".ljust(7) + f"{freq}".ljust(7) + f"{format(value, '.1f')}% | ".rjust(10))
            else:
                self.stdscr.addstr(y_offset, self.x_offset + (i % column) * column_width, f"| {label}:  ".ljust(7) + f"{freq}".ljust(7) + f"{format(value, '.1f')}% | ".rjust(10))
            self.stdscr.addstr(y_offset, self.x_offset + (i % column) * column_width + prefix_offset_length, "▩" * bar_length, curses.color_pair(color))
            self.stdscr.addstr(y_offset, self.x_offset + (i % column) * column_width + prefix_offset_length + bar_length, " " * (bar_max_width - bar_length))
            self.stdscr.addstr(y_offset, self.x_offset + (i % column) * column_width + prefix_offset_length + bar_max_width, " |")
            if (i + 1) % column == 0: 
                y_offset += 1
        
        if len(values) % column != 0:
            for i in range(column - len(values) % column):
                self.stdscr.addstr(y_offset, self.x_offset + (column - i - 1) * column_width, "|" + " " * (column_width - 2) + "|")

    def draw_bar_memory(self, load, used, freqs=None,offset=3):
        prefix_offset_length = 7 + 7 + 10 + 1
        suffix_offset_length = 2
        column = ORDER.column
        column_width = math.floor(self.container_max_width / column)
        bar_max_width = column_width - prefix_offset_length - suffix_offset_length
        y_offset = self.y_offset + offset

        labels = ["LOAD", "USED"]
        freq = format(freqs[0], ".1f") + " GHz"
        for i, label in enumerate(labels):
            value = load[0] if i == 0 else used[0]
            bar_length = int((value / 100) * bar_max_width)
            color = 1 if value < 50 else 2  # 确定条形图颜色: 低于 50% 使用颜色1，其他使用颜色2
            if i == 0:
                self.stdscr.addstr(y_offset, self.x_offset + (i % column) * column_width, f"| {label}: ".ljust(7) + f"{freq}".ljust(7) + f"{format(value, '.1f')}% | ".rjust(10))
            else:
                self.stdscr.addstr(y_offset, self.x_offset + (i % column) * column_width, f"| {label}: ".ljust(7) + f"".ljust(7) + f"{format(value, '.1f')}% | ".rjust(10))
            self.stdscr.addstr(y_offset, self.x_offset + (i % column) * column_width + prefix_offset_length, "▩" * bar_length, curses.color_pair(color))
            self.stdscr.addstr(y_offset, self.x_offset + (i % column) * column_width + prefix_offset_length + bar_length, " " * (bar_max_width - bar_length))
            self.stdscr.addstr(y_offset, self.x_offset + (i % column) * column_width + prefix_offset_length + bar_max_width, " |")
            if (i + 1) % column == 0: 
                y_offset += 1

        if column > 2:
            for i in range(column - 2 % column):
                self.stdscr.addstr(y_offset, self.x_offset + (column - i - 1) * column_width, "|" + " " * (column_width - 2) + "|")

class CpuInfo(BaseRenderer):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.mode = []
        self.freq = []
        self.load = []

    def update(self):
        self.y_offset = len(logo) + ORDER.cpu_offset + 1
        try:
            mode = []
            load = psutil.cpu_percent(percpu=True)[:8]
            dirs = sorted(os.listdir('/sys/devices/system/cpu/cpufreq'))
            for dir in dirs:
                process = subprocess.run(['sudo', 'cat', f'/sys/devices/system/cpu/cpufreq/{dir}/scaling_governor'], stdout=subprocess.PIPE)
                output = process.stdout.decode('utf-8').strip()
                mode.append(output)
            freq = []
            for dir in dirs:
                process = subprocess.run(['sudo', 'cat', f'/sys/devices/system/cpu/cpufreq/{dir}/related_cpus'], stdout=subprocess.PIPE)
                output = process.stdout.decode('utf-8').strip()
                cpus = output.split(" ")
                process = subprocess.run(['sudo', 'cat', f'/sys/devices/system/cpu/cpufreq/{dir}/cpuinfo_cur_freq'], stdout=subprocess.PIPE)
                output = process.stdout.decode('utf-8').strip()
                freq = freq + [int(output) / 1000000 for _ in cpus]
            self.mode = mode
            self.load = load
            self.freq = freq
        except Exception as e:
            print("Error when getting cpu info:", e)
            self.mode = []
            self.load = []
            self.freq = []

    def render(self):
        self.draw_mode("CPU", self.mode)
        self.draw_bar("CPU", self.load, self.freq)
        
class NpuInfo(BaseRenderer):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.mode = []
        self.load = []
        self.freq = []

    def update(self):
        self.y_offset = len(logo) + ORDER.npu_offset + 1
        try:
            mode = []
            process = subprocess.run(['sudo', 'cat', '/sys/class/devfreq/fdab0000.npu/governor'], stdout=subprocess.PIPE)
            output = process.stdout.decode('utf-8').strip()
            mode.append(output)
            process = subprocess.run(['sudo', 'cat', '/sys/kernel/debug/rknpu/load'], stdout=subprocess.PIPE)
            output = process.stdout.decode('utf-8').strip()
            load = [int(x) for x in re.findall(r'Core\d+: *(\d+)%', output)]
            process = subprocess.run(['sudo', 'cat', '/sys/class/devfreq/fdab0000.npu/cur_freq'], stdout=subprocess.PIPE)
            output = process.stdout.decode('utf-8').strip()
            freq = [int(output) / 1000000000 for _ in load]
            self.mode = mode
            self.load = load
            self.freq = freq
        except Exception as e:
            print("Error when getting npu info:", e)
            self.mode = []
            self.load = []
            self.freq = []

    def render(self):
        self.draw_mode("NPU", self.mode)
        self.draw_bar("NPU", self.load, self.freq)

class GpuInfo(BaseRenderer):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.mode = []
        self.load = []
        self.freq = []

    def update(self):
        self.y_offset = len(logo) + ORDER.gpu_offset + 1
        try:
            mode = []
            process = subprocess.run(['sudo', 'cat', '/sys/class/devfreq/fb000000.gpu/governor'], stdout=subprocess.PIPE)
            output = process.stdout.decode('utf-8').strip()
            mode.append(output)
            process = subprocess.run(['sudo', 'cat', '/sys/class/devfreq/fb000000.gpu/load'], stdout=subprocess.PIPE)
            output = process.stdout.decode('utf-8').strip()
            match = re.match(r"(\d+)@(\d+)Hz", output)
            if match:
                load = match.group(1)
                freq = match.group(2)
            else:
                raise Exception("result match error")
            self.mode = mode
            self.load = [int(load)]
            self.freq = [int(freq) / 1000000000]
        except Exception as e:
            print("Error when getting gpu info:", e)
            self.mode = []
            self.load = []
            self.freq = []

    def render(self):
        self.draw_mode("GPU", self.mode)
        self.draw_bar("GPU", self.load, self.freq)
    
class RgaInfo(BaseRenderer):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.mode = []
        self.load = []

    def update(self):
        self.y_offset = len(logo) + ORDER.rga_offset + 1
        try:
            process = subprocess.run(['sudo', 'cat', '/sys/kernel/debug/rkrga/load'], stdout=subprocess.PIPE)
            output = process.stdout.decode('utf-8').strip()
            load = re.findall(r'load\s*=\s*(\d+)%', output)
            self.load = [int(x) for x in load]
        except Exception as e:
            print("Error when getting rga info:", e)
            self.load = []

    def render(self):
        self.draw_mode("RGA", self.mode)
        self.draw_bar("RGA", self.load)
    
class MemInfo(BaseRenderer):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.mode = []
        self.load = []
        self.used = []
        self.freq = []

    def update(self):
        self.y_offset = len(logo) + ORDER.mem_offset + 1
        try:
            mode = []
            process = subprocess.run(['sudo', 'cat', '/sys/class/devfreq/dmc/governor'], stdout=subprocess.PIPE)
            output = process.stdout.decode('utf-8').strip()
            mode.append(output)
            process = subprocess.run(['sudo', 'cat', '/sys/class/devfreq/dmc/load'], stdout=subprocess.PIPE)
            output = process.stdout.decode('utf-8').strip()
            match = re.match(r"(\d+)@(\d+)Hz", output)
            if match:
                load = match.group(1)
                freq = match.group(2)
            used = psutil.virtual_memory().percent
            self.mode = mode
            self.load = [int(load)]
            self.used = [float(used)]
            self.freq = [int(freq) / 1000000000]
        except Exception as e:
            print("Error when getting memory info:", e)
            self.mode = []
            self.load = []
            self.freq = []

    def render(self):
        self.draw_mode("MEM", self.mode)
        self.draw_bar_memory(self.load, self.used, self.freq)

class Logo(BaseRenderer):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        try:
            process = subprocess.run(['sudo', 'cat', '/sys/kernel/debug/rknpu/version'], stdout=subprocess.PIPE)
            output = process.stdout.decode('utf-8').strip()
            self.npu_version = output
        except Exception as e:
            print("Error when getting npu version:", e)
            self.npu_version = ''

    def render(self):
        end_offset = self.y_offset + len(logo) + ORDER.total_offset + 1
        for i, line in enumerate(logo):
            prefix_logo = math.ceil((self.container_max_width-len(line)-4) / 2.0)
            suffix_logo = math.floor((self.container_max_width-len(line)-4) / 2.0)
            if i==0:
                self.clear_line(self.y_offset + i)
                self.stdscr.addstr(self.y_offset + i, self.x_offset, '==' + '=' * prefix_logo + line + '=' * suffix_logo + "==")
            elif i==len(logo)-1:
                self.clear_line(self.y_offset + i)
                self.stdscr.addstr(self.y_offset + i, self.x_offset, '|=' + '=' * prefix_logo + line + '=' * suffix_logo + "=|")
            else:
                self.clear_line(self.y_offset + i)
                self.stdscr.addstr(self.y_offset + i, self.x_offset, '||' + ' ' * prefix_logo + line + ' ' * suffix_logo + "||")

        prefix_version = math.ceil((self.container_max_width-len(self.npu_version)-4) / 2.0)
        suffix_version = math.floor((self.container_max_width-len(self.npu_version)-4) / 2.0)
        self.clear_line(self.y_offset + len(logo))
        self.stdscr.addstr(self.y_offset + len(logo), self.x_offset, '| ' + ' ' * prefix_version + self.npu_version + ' ' * suffix_version + " |")
        self.clear_line(end_offset)
        self.stdscr.addstr(end_offset, self.x_offset, "=" * self.container_max_width)

class Controller:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.logo = Logo(stdscr)
        self.cpu = CpuInfo(stdscr)
        self.gpu = GpuInfo(stdscr)
        self.npu = NpuInfo(stdscr)
        self.rga = RgaInfo(stdscr)
        self.mem = MemInfo(stdscr)
        self.width = 0

    def update(self):
        _, width = self.stdscr.getmaxyx()
        container_width = width - 4
        column = math.floor(container_width / 50)
        container_width = container_width - container_width % column
        if self.width != width:
            self.width = width
            self.cpu.change_width(width, container_width) if 'CPU' in DEVICES else None
            self.gpu.change_width(width, container_width) if 'GPU' in DEVICES else None
            self.npu.change_width(width, container_width) if 'NPU' in DEVICES else None
            self.rga.change_width(width, container_width) if 'RGA' in DEVICES else None
            self.mem.change_width(width, container_width) if 'MEM' in DEVICES else None
            self.logo.change_width(width, container_width)
            ORDER.update_column(column)
            self.stdscr.clear()
        self.cpu.update() if 'CPU' in DEVICES else None
        self.gpu.update() if 'GPU' in DEVICES else None
        self.npu.update() if 'NPU' in DEVICES else None
        self.rga.update() if 'RGA' in DEVICES else None
        self.mem.update() if 'MEM' in DEVICES else None

    def render(self):
        self.logo.render()
        self.cpu.render() if 'CPU' in DEVICES else None
        self.gpu.render() if 'GPU' in DEVICES else None
        self.npu.render() if 'NPU' in DEVICES else None
        self.rga.render() if 'RGA' in DEVICES else None
        self.mem.render() if 'MEM' in DEVICES else None

    def loop_back(self):
        while True:
            try:
                self.update()
                self.render()
                self.stdscr.refresh()
                time.sleep(INTERVAL)
            except Exception as e:
                height, width = self.stdscr.getmaxyx()
                self.stdscr.clear()
                prompt = "Insufficient window size. Please adjust the window size."
                self.stdscr.addstr(int(height / 2), max(int((width - len(prompt))/2), 0), "Insufficient window size. Please adjust the window size.")
                self.stdscr.refresh()
                time.sleep(INTERVAL)  

def main(stdscr):
    controller = Controller(stdscr)
    controller.loop_back()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--interval', type=float, help='update interval time(seconds)')
    parser.add_argument('--show', type=str, help='show options(combination of c,g,n,r,m)')
    args = parser.parse_args()
    if args.interval is not None:
        INTERVAL = float(args.interval)
    if args.show is not None:
        NEW_DEVICES = []
        for device in args.show:
            NEW_DEVICES.append('CPU') if device == 'c' else None
            NEW_DEVICES.append('GPU') if device == 'g' else None
            NEW_DEVICES.append('NPU') if device == 'n' else None
            NEW_DEVICES.append('RGA') if device == 'r' else None
            NEW_DEVICES.append('MEM') if device == 'm' else None
        DEVICES = NEW_DEVICES

    curses.initscr()
    curses.curs_set(0)
    curses.start_color() 
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)  # 负载低于 50% 使用绿色
    curses.init_pair(2, curses.COLOR_RED, -1)    # 负载高于 50% 使用红色
    curses.wrapper(main)
