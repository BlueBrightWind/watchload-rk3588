import curses
import math
import subprocess

from render.base_render import BaseRender

class TempRender(BaseRender):
    def __init__(self, stdscr, devices):
        super().__init__(stdscr)
        self.devices = devices
        self.labels = []
        self.temps = []
        BaseRender.offset.update_dict('TEMP', len(devices))

    def update(self):
        self.y_offset = len(BaseRender.logo) + BaseRender.y_offset + BaseRender.offset.temp_offset + 1
        try:
            process = subprocess.run('sudo cat /sys/class/thermal/thermal_zone*/type', stdout=subprocess.PIPE, shell=True)
            output = process.stdout.decode('utf-8').strip()
            labels = output.split()
            process = subprocess.run('sudo cat /sys/class/thermal/thermal_zone*/temp', stdout=subprocess.PIPE, shell=True)
            output = process.stdout.decode('utf-8').strip()
            temps = output.split()
            self.labels = labels
            self.temps = [float(temp) / 1000 for temp in temps]
        except Exception as e:
            print("Error when getting temperature info:", e)
            self.labels = []
            self.temps = []

    def render(self):
        self.draw_mode("TEMPERATURE")
        self.draw_bar(self.labels, self.temps)

    def draw_mode(self, label):
        self.clear_line(self.y_offset+0)
        self.stdscr.addstr(self.y_offset+0, self.x_offset, '|' + '-'*(self.container_max_width-2) + '|')
        self.clear_line(self.y_offset+1)
        self.stdscr.addstr(self.y_offset+1, self.x_offset, f"| {label}: ".ljust(self.container_max_width-2) + " |")
        self.clear_line(self.y_offset+2)
        self.stdscr.addstr(self.y_offset+2, self.x_offset, '|' + '-'*(self.container_max_width-2) + '|')

    def draw_bar(self, labels, values, offset=3):
        prefix_offset_length = 7 + 7 + 10 + 1
        suffix_offset_length = 2
        column = BaseRender.offset.column
        column_width = math.floor(self.container_max_width / column)
        bar_max_width = column_width - prefix_offset_length - suffix_offset_length
        x_offset = self.x_offset
        y_offset = self.y_offset + offset

        count = 0
        for i, label in enumerate(labels):
            if 'CPU' in self.devices and label == 'center-thermal':
                label = 'CPU'
                value = values[i]
            elif 'GPU' in self.devices and label == 'gpu-thermal':
                label = 'GPU'
                value = values[i]
            elif 'NPU' in self.devices and label == 'npu-thermal':
                label = 'NPU'
                value = values[i]
            else:
                continue
            bar_length = int((value / 100) * bar_max_width)
            color = 1 if value < 80 else 2  # 确定条形图颜色: 低于 80°C 使用颜色1，其他使用颜色2
            self.stdscr.addstr(y_offset, x_offset + (count % column) * column_width, f"| {label}:  ".ljust(7) + "".ljust(7) + f"{format(value, '.1f')}°C | ".rjust(10))
            self.stdscr.addstr(y_offset, x_offset + (count % column) * column_width + prefix_offset_length, "▩" * bar_length, curses.color_pair(color))
            self.stdscr.addstr(y_offset, x_offset + (count % column) * column_width + prefix_offset_length + bar_length, " " * (bar_max_width - bar_length))
            self.stdscr.addstr(y_offset, x_offset + (count % column) * column_width + prefix_offset_length + bar_max_width, " |")
            if (count + 1) % column == 0: 
                y_offset += 1
            count += 1
        
        if len(self.devices) % column != 0:
            for i in range(column - count % column):
                self.stdscr.addstr(y_offset, x_offset + (column - i - 1) * column_width, "|" + " " * (column_width - 2) + "|")
 