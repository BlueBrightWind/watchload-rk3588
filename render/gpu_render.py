import re
import subprocess

from render.base_render import BaseRender

class GpuRender(BaseRender):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.mode = []
        self.load = []
        self.freq = []

    def update(self):
        self.y_offset = len(BaseRender.logo) + BaseRender.y_offset + BaseRender.offset.gpu_offset + 1
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
 