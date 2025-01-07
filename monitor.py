import math
import time

from render.base_render import BaseRender
from render.cpu_render import CpuRender
from render.gpu_render import GpuRender
from render.npu_render import NpuRender
from render.mem_render import MemRender
from render.rga_render import RgaRender
from render.logo_render import LogoRender
from render.temp_render import TempRender

class Monitor(object):
    def __init__(self, stdscr, interval=1, devices=['CPU', 'GPU', 'MEM', 'NPU', 'RGA'], temps=['CPU', 'GPU', 'NPU']):
        self.stdscr = stdscr
        self.interval = interval
        BaseRender.change_devices(devices)
        self.logo = LogoRender(stdscr)
        self.temp = TempRender(stdscr, temps)
        self.cpu = CpuRender(stdscr)
        self.gpu = GpuRender(stdscr)
        self.npu = NpuRender(stdscr)
        self.rga = RgaRender(stdscr)
        self.mem = MemRender(stdscr)
        self.current_width = 0

    def update(self):
        _, width = self.stdscr.getmaxyx()
        container_width = width - BaseRender.x_offset * 2
        column = math.floor(container_width / 50)
        container_width = container_width - container_width % column
        if self.current_width != width:
            self.current_width = width
            BaseRender.change_width(width, container_width)
            BaseRender.offset.update_column(column)
            self.stdscr.clear()
        self.temp.update() if 'TEMP' in BaseRender.devices else None
        self.cpu.update() if 'CPU' in BaseRender.devices else None
        self.gpu.update() if 'GPU' in BaseRender.devices else None
        self.npu.update() if 'NPU' in BaseRender.devices else None
        self.rga.update() if 'RGA' in BaseRender.devices else None
        self.mem.update() if 'MEM' in BaseRender.devices else None

    def render(self):
        self.logo.render()
        self.temp.render() if 'TEMP' in BaseRender.devices else None
        self.cpu.render() if 'CPU' in BaseRender.devices else None
        self.gpu.render() if 'GPU' in BaseRender.devices else None
        self.npu.render() if 'NPU' in BaseRender.devices else None
        self.rga.render() if 'RGA' in BaseRender.devices else None
        self.mem.render() if 'MEM' in BaseRender.devices else None

    def loop_back(self):
        while True:
            try:
                self.update()
                self.render()
                self.stdscr.refresh()
                time.sleep(self.interval)
            except Exception as e:
                height, width = self.stdscr.getmaxyx()
                self.stdscr.clear()
                prompt = "Insufficient window size. Please adjust the window size."
                self.stdscr.addstr(int(height / 2), max(int((width - len(prompt))/2), 0), "Insufficient window size. Please adjust the window size.")
                self.stdscr.refresh()
                time.sleep(self.interval)  
