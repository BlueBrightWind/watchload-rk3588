import re
import subprocess

from render.base_render import BaseRender

class NpuRender(BaseRender):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.mode = []
        self.load = []
        self.freq = []

    def update(self):
        self.y_offset = len(BaseRender.logo) + BaseRender.y_offset + BaseRender.offset.npu_offset + 1
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
