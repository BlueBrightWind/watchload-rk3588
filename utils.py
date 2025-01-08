import subprocess

def change_mode(mode):
    if mode == 'performance':
        commands = ['echo performance | sudo tee /sys/devices/system/cpu/cpufreq/policy6/scaling_governor',
                    'echo performance | sudo tee /sys/devices/system/cpu/cpufreq/policy4/scaling_governor',
                    'echo performance | sudo tee /sys/devices/system/cpu/cpufreq/policy0/scaling_governor',
                    'echo performance | sudo tee /sys/class/devfreq/fb000000.gpu/governor',
                    'echo performance | sudo tee /sys/class/devfreq/fdab0000.npu/governor',
                    'echo performance | sudo tee /sys/class/devfreq/dmc/governor'
                    ]
    elif mode == 'ondemand':
        commands = ['echo schedutil | sudo tee /sys/devices/system/cpu/cpufreq/policy6/scaling_governor',
                    'echo schedutil | sudo tee /sys/devices/system/cpu/cpufreq/policy4/scaling_governor',
                    'echo schedutil | sudo tee /sys/devices/system/cpu/cpufreq/policy0/scaling_governor',
                    'echo simple_ondemand | sudo tee /sys/class/devfreq/fb000000.gpu/governor',
                    'echo simple_ondemand | sudo tee /sys/class/devfreq/fdab0000.npu/governor',
                    'echo simple_ondemand | sudo tee /sys/class/devfreq/dmc/governor'
                    ]
    elif mode == 'powersave':
        commands = ['echo powersave | sudo tee /sys/devices/system/cpu/cpufreq/policy6/scaling_governor',
                    'echo powersave | sudo tee /sys/devices/system/cpu/cpufreq/policy4/scaling_governor',
                    'echo powersave | sudo tee /sys/devices/system/cpu/cpufreq/policy0/scaling_governor',
                    'echo powersave | sudo tee /sys/class/devfreq/fb000000.gpu/governor',
                    'echo powersave | sudo tee /sys/class/devfreq/fdab0000.npu/governor',
                    'echo powersave | sudo tee /sys/class/devfreq/dmc/governor'
                    ]
    subprocess.run(';'.join(commands), stdout=subprocess.PIPE, shell=True)
