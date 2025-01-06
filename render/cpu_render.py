import os
import psutil
import subprocess

from render.base_render import BaseRender

class CpuRender(BaseRender):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.mode = []
        self.freq = []
        self.load = []

    def update(self):
        self.y_offset = len(BaseRender.logo) + BaseRender.y_offset + BaseRender.offset.cpu_offset + 1
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
 
