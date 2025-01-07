import math
import curses

class BaseOffset(object):
    def __init__(self, devices: list):
        self.column = 1
        self.title_length = 3
        self.devices = devices
        self.offset_dict = {'CPU': 8, 'GPU': 1, 'NPU': 3, 'RGA': 3, 'MEM': 2, 'TEMP': 1}

    def update_dict(self, label, value):
        self.offset_dict[label] = value

    def update_column(self, column):
        self.column = column
    
    @property
    def total_offset(self):
        offset = 0
        for key, value in self.offset_dict.items():
            if key in self.devices:
                offset += math.ceil(value / self.column) + self.title_length
        return offset

    @property
    def cpu_offset(self):
        index = self.devices.index('CPU')
        offset = 0
        for i in range(index):
            offset += math.ceil(self.offset_dict[self.devices[i]] / self.column) + self.title_length
        return offset
    
    @property
    def gpu_offset(self):
        index = self.devices.index('GPU')
        offset = 0
        for i in range(index):
            offset += math.ceil(self.offset_dict[self.devices[i]] / self.column) + self.title_length
        return offset
    
    @property
    def npu_offset(self):
        index = self.devices.index('NPU')
        offset = 0
        for i in range(index):
            offset += math.ceil(self.offset_dict[self.devices[i]] / self.column) + self.title_length
        return offset
    
    @property
    def rga_offset(self):
        index = self.devices.index('RGA')
        offset = 0
        for i in range(index):
            offset += math.ceil(self.offset_dict[self.devices[i]] / self.column) + self.title_length
        return offset
    
    @property
    def mem_offset(self):
        index = self.devices.index('MEM')
        offset = 0
        for i in range(index):
            offset += math.ceil(self.offset_dict[self.devices[i]] / self.column) + self.title_length
        return offset  
    
    @property
    def temp_offset(self):
        index = self.devices.index('TEMP')
        offset = 0
        for i in range(index):
            offset += math.ceil(self.offset_dict[self.devices[i]] / self.column) + self.title_length
        return offset  

class BaseRender(object):
    x_offset = 0
    y_offset = 0
    window_max_width = 0
    container_max_width = 0
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
    devices = ['TEMP', 'CPU', 'GPU', 'MEM', 'NPU', 'RGA']
    offset = BaseOffset(devices)

    @staticmethod
    def change_width(window_width, container_width):
        BaseRender.window_max_width = window_width
        BaseRender.container_max_width = container_width
    
    @staticmethod
    def change_devices(devices):
        BaseRender.devices = devices
        BaseRender.offset = BaseOffset(devices)

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.x_offset = BaseRender.x_offset
        self.y_offset = BaseRender.y_offset

    def clear_line(self, line):
        self.stdscr.addstr(line, 0, ' ' * self.window_max_width)

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
        column = BaseRender.offset.column
        column_width = math.floor(self.container_max_width / column)
        bar_max_width = column_width - prefix_offset_length - suffix_offset_length
        x_offset = self.x_offset
        y_offset = self.y_offset + offset

        for i, value in enumerate(values):
            bar_length = int((value / 100) * bar_max_width)
            color = 1 if value < 50 else 2  # 确定条形图颜色: 低于 50% 使用颜色1，其他使用颜色2
            if freqs is not None:
                freq = format(freqs[i], ".1f") + " GHz"
            else:
                freq = ""
            if len(values) > 1:
                self.stdscr.addstr(y_offset, x_offset + (i % column) * column_width, f"| {label}{i}: ".ljust(7) + f"{freq}".ljust(7) + f"{format(value, '.1f')}% | ".rjust(10))
            else:
                self.stdscr.addstr(y_offset, x_offset + (i % column) * column_width, f"| {label}:  ".ljust(7) + f"{freq}".ljust(7) + f"{format(value, '.1f')}% | ".rjust(10))
            self.stdscr.addstr(y_offset, x_offset + (i % column) * column_width + prefix_offset_length, "▩" * bar_length, curses.color_pair(color))
            self.stdscr.addstr(y_offset, x_offset + (i % column) * column_width + prefix_offset_length + bar_length, " " * (bar_max_width - bar_length))
            self.stdscr.addstr(y_offset, x_offset + (i % column) * column_width + prefix_offset_length + bar_max_width, " |")
            if (i + 1) % column == 0: 
                y_offset += 1
        
        if len(values) % column != 0:
            for i in range(column - len(values) % column):
                self.stdscr.addstr(y_offset, x_offset + (column - i - 1) * column_width, "|" + " " * (column_width - 2) + "|")
