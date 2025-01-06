import subprocess

def change_mode(mode):
    if mode == 'performance':
        # CPU
        subprocess.run(['echo performance | sudo tee /sys/devices/system/cpu/cpufreq/policy6/scaling_governor'], stdout=subprocess.PIPE, shell=True)
        subprocess.run(['echo performance | sudo tee /sys/devices/system/cpu/cpufreq/policy4/scaling_governor'], stdout=subprocess.PIPE, shell=True)
        subprocess.run(['echo performance | sudo tee /sys/devices/system/cpu/cpufreq/policy0/scaling_governor'], stdout=subprocess.PIPE, shell=True)
        # GPU
        subprocess.run(['echo performance | sudo tee /sys/class/devfreq/fb000000.gpu/governor'], stdout=subprocess.PIPE, shell=True)
        # NPU
        subprocess.run(['echo performance | sudo tee /sys/class/devfreq/fdab0000.npu/governor'], stdout=subprocess.PIPE, shell=True)
        # MEM
        subprocess.run(['echo performance | sudo tee /sys/class/devfreq/dmc/governor'], stdout=subprocess.PIPE, shell=True)
    elif mode == 'ondemand':
        # CPU
        subprocess.run(['echo schedutil | sudo tee /sys/devices/system/cpu/cpufreq/policy6/scaling_governor'], stdout=subprocess.PIPE, shell=True)
        subprocess.run(['echo schedutil | sudo tee /sys/devices/system/cpu/cpufreq/policy4/scaling_governor'], stdout=subprocess.PIPE, shell=True)
        subprocess.run(['echo schedutil | sudo tee /sys/devices/system/cpu/cpufreq/policy0/scaling_governor'], stdout=subprocess.PIPE, shell=True)
        # GPU
        subprocess.run(['echo simple_ondemand | sudo tee /sys/class/devfreq/fb000000.gpu/governor'], stdout=subprocess.PIPE, shell=True)
        # NPU
        subprocess.run(['echo simple_ondemand | sudo tee /sys/class/devfreq/fdab0000.npu/governor'], stdout=subprocess.PIPE, shell=True)
        # MEM
        subprocess.run(['echo simple_ondemand | sudo tee /sys/class/devfreq/dmc/governor'], stdout=subprocess.PIPE, shell=True)
    elif mode == 'powersave':
        # CPU
        subprocess.run(['echo powersave | sudo tee /sys/devices/system/cpu/cpufreq/policy6/scaling_governor'], stdout=subprocess.PIPE, shell=True)
        subprocess.run(['echo powersave | sudo tee /sys/devices/system/cpu/cpufreq/policy4/scaling_governor'], stdout=subprocess.PIPE, shell=True)
        subprocess.run(['echo powersave | sudo tee /sys/devices/system/cpu/cpufreq/policy0/scaling_governor'], stdout=subprocess.PIPE, shell=True)
        # GPU
        subprocess.run(['echo powersave | sudo tee /sys/class/devfreq/fb000000.gpu/governor'], stdout=subprocess.PIPE, shell=True)
        # NPU
        subprocess.run(['echo powersave | sudo tee /sys/class/devfreq/fdab0000.npu/governor'], stdout=subprocess.PIPE, shell=True)
        # MEM
        subprocess.run(['echo powersave | sudo tee /sys/class/devfreq/dmc/governor'], stdout=subprocess.PIPE, shell=True)
