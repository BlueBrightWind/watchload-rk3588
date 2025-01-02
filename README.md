# watchload for 3588/3588s
The project is mainly designed to conveniently view information about the devices(CPU/GPU/RGA/NPU/MEM), and provide the ability to switch between different modes of operation for the devices.

## Highlights
 - Monitor support automatically adjust the size base on the console window size.
 - Monitor support customize the devices being monitored.
 - Support device mode quick switching between performance/ondemand/powersave.

## How to install
```bash
git clone https://github.com/BlueBrightWind/watchload-for-rk3588.git --depth=1 watchload
cd watchload
sudo bash install.sh
```

## How to use
```bash
Options:
    -h, --help      show the help message
    -s, --show      show options   (combination of c,g,n,r,m)
                    set the device information and display order in the monitor(cpu/gpu/npu/rga/memory), default is cgmnr
    -n, --interval  interval time  (number)
                    set the refresh interval time (seconds) of the monitor, default is 1
    -m, --mode      mode selection (ondemand/performance/powersave/none)
                    set the mode of the cpu/gpu/npu/memory, default is none

Examples:
    watchload -s cgmn -n 2
    watchload --mode performance
```
