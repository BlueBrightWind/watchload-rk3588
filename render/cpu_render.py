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
            load = psutil.cpu_percent(percpu=True)[:8]
            process = subprocess.run(['sudo cat /sys/devices/system/cpu/cpufreq/*/scaling_governor'], stdout=subprocess.PIPE, shell=True)
            output = process.stdout.decode('utf-8').strip()
            mode = output.split()

            process = subprocess.run(['sudo cat /sys/devices/system/cpu/cpufreq/*/related_cpus'], stdout=subprocess.PIPE, shell=True)
            output = process.stdout.decode('utf-8').strip()
            cpus = output.split("\n")
            
            process = subprocess.run(['sudo cat /sys/devices/system/cpu/cpufreq/*/cpuinfo_cur_freq'], stdout=subprocess.PIPE, shell=True)
            output = process.stdout.decode('utf-8').strip()
            freqs = output.split()
            freq = [int(x) / 1000000 for x, cpu in zip(freqs, cpus) for _ in cpu.split()]

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
 