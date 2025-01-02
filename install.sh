#!/bin/bash

#######################################################################
WATCHLOAD_INSTALL_PATH=/usr/local/watchload
#######################################################################

# Install Dependencies
sudo apt install -y python3-pip
sudo pip3 install psutil
sudo mkdir -p $WATCHLOAD_INSTALL_PATH/bin
sudo mkdir -p $WATCHLOAD_INSTALL_PATH/script
sudo cat << END_OF_SCRIPT > watchload
#!/bin/bash

# Default Args
MODE=none
SHOW=cgmnr
INTERVAL=1

usage() {
    cat << EOF
Usage: watchload [options]

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
EOF
    exit 1
}

validate_mode() {
    local mode=\$1
    case \$mode in
        ondemand|performance|powersave|none) return 0 ;;
        *) return 1 ;;
    esac
}

validate_show() {
    local show=\$1
    # check for letters
    if [[ ! \$show =~ ^[cgnrm]+$ ]]; then
        return 1
    fi
    # check for duplicates
    if [ "\$(echo \$show | grep -o . | sort | uniq | tr -d '\n')" != "\$(echo \$show | grep -o . | sort | tr -d '\n')" ]; then
        return 1
    fi
    return 0
}

validate_interval() {
    local interval=\$1
    if [[ \$interval =~ ^[0-9]+\.?[0-9]*$ ]]; then
        return 0
    fi
    return 1
}

change_performance_mode() {
    # CPU
    echo performance | sudo tee /sys/devices/system/cpu/cpufreq/policy6/scaling_governor > /dev/null
    echo performance | sudo tee /sys/devices/system/cpu/cpufreq/policy4/scaling_governor > /dev/null
    echo performance | sudo tee /sys/devices/system/cpu/cpufreq/policy0/scaling_governor > /dev/null
    # GPU
    echo performance | sudo tee /sys/class/devfreq/fb000000.gpu/governor > /dev/null
    # NPU
    echo performance | sudo tee /sys/class/devfreq/fdab0000.npu/governor > /dev/null
    # MEM
    echo performance | sudo tee /sys/class/devfreq/dmc/governor > /dev/null
}

change_ondemand_mode() {
    # CPU
    echo schedutil | sudo tee /sys/devices/system/cpu/cpufreq/policy6/scaling_governor > /dev/null
    echo schedutil | sudo tee /sys/devices/system/cpu/cpufreq/policy4/scaling_governor > /dev/null
    echo schedutil | sudo tee /sys/devices/system/cpu/cpufreq/policy0/scaling_governor > /dev/null
    # GPU
    echo simple_ondemand | sudo tee /sys/class/devfreq/fb000000.gpu/governor > /dev/null
    # NPU
    echo simple_ondemand | sudo tee /sys/class/devfreq/fdab0000.npu/governor > /dev/null
    # MEM
    echo simple_ondemand | sudo tee /sys/class/devfreq/dmc/governor > /dev/null
}

change_powersave_mode() {
    # CPU
    echo powersave | sudo tee /sys/devices/system/cpu/cpufreq/policy6/scaling_governor > /dev/null
    echo powersave | sudo tee /sys/devices/system/cpu/cpufreq/policy4/scaling_governor > /dev/null
    echo powersave | sudo tee /sys/devices/system/cpu/cpufreq/policy0/scaling_governor > /dev/null
    # GPU
    echo powersave | sudo tee /sys/class/devfreq/fb000000.gpu/governor > /dev/null
    # NPU
    echo powersave | sudo tee /sys/class/devfreq/fdab0000.npu/governor > /dev/null
    # MEM
    echo powersave | sudo tee /sys/class/devfreq/dmc/governor > /dev/null
}

# Parse Args
while [[ \$# -gt 0 ]]; do
    case \$1 in
        -m|--mode)
            if [ -n "\$2" ] && ! [[ "\$2" =~ ^- ]]; then
                if validate_mode "\$2"; then
                    MODE=\$2
                    shift 2
                else
                    echo "Error: Invalid mode. Must be ondemand, performance, powersave or none."
                    exit 1
                fi
            else
                echo "Error: Missing mode argument"
                exit 1
            fi
            ;;
        -s|--show)
            if [ -n "\$2" ] && ! [[ "\$2" =~ ^- ]]; then
                if validate_show "\$2"; then
                    SHOW=\$2
                    shift 2
                else
                    echo "Error: Invalid show option. Must be combination of c,g,n,r,m without duplicates."
                    exit 1
                fi
            else
                echo "Error: Missing show argument"
                exit 1
            fi
            ;;
        -n|--interval)
            if [ -n "\$2" ] && ! [[ "\$2" =~ ^- ]]; then
                if validate_interval "\$2"; then
                    INTERVAL=\$2
                    shift 2
                else
                    echo "Error: Invalid interval. Must be a number."
                    exit 1
                fi
            else
                echo "Error: Missing interval argument"
                exit 1
            fi
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown parameter: \$1"
            usage
            ;;
    esac
done

if [[ "\$MODE" == "none" ]]; then
    sudo python3 $WATCHLOAD_INSTALL_PATH/script/monitor.py --show \$SHOW --interval \$INTERVAL 2> /dev/null
elif [[ "\$MODE" == "ondemand" ]]; then
    change_ondemand_mode
elif [[ "\$MODE" == "performance" ]]; then
    change_performance_mode
elif [[ "\$MODE" == "powersave" ]]; then
    change_powersave_mode
fi

END_OF_SCRIPT

sudo mv watchload $WATCHLOAD_INSTALL_PATH/bin
sudo chmod +x $WATCHLOAD_INSTALL_PATH/bin/watchload
sudo cp monitor.py $WATCHLOAD_INSTALL_PATH/script

# Set Bash Environment
echo  >> ~/.bashrc
echo '# Watchload Tool' >> ~/.bashrc
echo export PATH=$WATCHLOAD_INSTALL_PATH/bin:'$PATH' >> ~/.bashrc
