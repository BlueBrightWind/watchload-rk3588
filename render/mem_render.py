import curses
import math
import psutil
import re
import subprocess

from render.base_render import BaseRender

class MemRender(BaseRender):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.mode = []
        self.load = []
        self.used = []
        self.freq = []

    def update(self):
        self.y_offset = len(BaseRender.logo) + BaseRender.y_offset + BaseRender.offset.mem_offset + 1
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
        self.draw_bar(self.load, self.used, self.freq)

    def draw_bar(self, load, used, freqs=None,offset=3):
        prefix_offset_length = 7 + 7 + 10 + 1
        suffix_offset_length = 2
        column = BaseRender.offset.column
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
