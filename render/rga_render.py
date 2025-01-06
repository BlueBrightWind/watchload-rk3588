import re
import subprocess

from render.base_render import BaseRender

class RgaRender(BaseRender):
    def __init__(self, stdscr):
        super().__init__(stdscr)
        self.mode = []
        self.load = []

    def update(self):
        self.y_offset = len(BaseRender.logo) + BaseRender.y_offset + BaseRender.offset.rga_offset + 1
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
  