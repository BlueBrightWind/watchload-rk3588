import math
import subprocess

from render.base_render import BaseRender

class LogoRender(BaseRender):
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
        end_offset = self.y_offset + len(BaseRender.logo) + BaseRender.offset.total_offset + 1
        for i, line in enumerate(BaseRender.logo):
            prefix_logo = math.ceil((self.container_max_width-len(line)-4) / 2.0)
            suffix_logo = math.floor((self.container_max_width-len(line)-4) / 2.0)
            if i==0:
                self.clear_line(self.y_offset + i)
                self.stdscr.addstr(self.y_offset + i, self.x_offset, '==' + '=' * prefix_logo + line + '=' * suffix_logo + "==")
            elif i==len(BaseRender.logo)-1:
                self.clear_line(self.y_offset + i)
                self.stdscr.addstr(self.y_offset + i, self.x_offset, '|=' + '=' * prefix_logo + line + '=' * suffix_logo + "=|")
            else:
                self.clear_line(self.y_offset + i)
                self.stdscr.addstr(self.y_offset + i, self.x_offset, '||' + ' ' * prefix_logo + line + ' ' * suffix_logo + "||")

        prefix_version = math.ceil((self.container_max_width-len(self.npu_version)-4) / 2.0)
        suffix_version = math.floor((self.container_max_width-len(self.npu_version)-4) / 2.0)
        self.clear_line(self.y_offset + len(BaseRender.logo))
        self.stdscr.addstr(self.y_offset + len(BaseRender.logo), self.x_offset, '| ' + ' ' * prefix_version + self.npu_version + ' ' * suffix_version + " |")
        self.clear_line(end_offset)
        self.stdscr.addstr(end_offset, self.x_offset, "=" * self.container_max_width)
