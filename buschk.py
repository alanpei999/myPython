#!/usr/bin/env python

#   This tool is used for Stingray-HPC64 
#   Check PLX979 and V100 
#   Check : V100 amount, bus band width
#   Alan Chien(Orion Chien)  2019/04/26
#   command : ./buschk.py
#   v1: first version
#   v2: add try except
#   v3: modified list for dynamic

# Color defining
red_clr = "\033[1;33;31m"
green_clr = "\033[1;33;32m"
ylw_clr = "\033[1;33;33m"
def_clr = "\033[0m"

import subprocess

bus1 = []  # 9797
bus2 = []  # V100

# Procees PLX9797 bus
a = 0
msg1 = subprocess.check_output("lspci | grep 9797", shell=True)
plx_split = msg1.split("\n") # split to a list

try:
    for i in range((len(plx_split)-1) / 6):
        plx_temp = plx_split[a].split(":")
        bus1.append(plx_temp[0])
        a = a + 6
    print "\n"
    print green_clr + " == PLX 9797 Bus :" + ylw_clr, bus1, def_clr
    #  Display PLX 9797 band width
    print "\n"
    print
    green_clr + " == PLX9797 Bus Check ==" + def_clr
    for n in bus1:
        cmd = "lspci -vvv -s " + n + ":00 | grep LnkSta:"
        print ylw_clr + cmd + def_clr
        subprocess.call(cmd, shell=True)
		
except(subprocess.CalledProcessError):
  print red_clr + "  No PLX 9797 found!!" + def_clr

# Prcoess NVIDIA V100 bus
msg2 = subprocess.check_output("lspci | grep NVIDIA", shell=True)
gpu_split = msg2.split("\n") # split to a list

try:
    for j in range(len(gpu_split)-1):
        gpu_temp = gpu_split[j].split(":")
        bus2.append(gpu_temp[0])
        j = j + 1

    print green_clr + " == NVIDIA V100 bus :" + ylw_clr, bus2, def_clr
    print green_clr + " == Total GPU V100 : " + ylw_clr + str(j) + def_clr

    #  Display V100 band width
    print "\n"
    print green_clr + " == NVIDIA V100 Bus Check ==" + def_clr
    for n in bus2:
      cmd = "lspci -vvv -s " + n + ":00 | grep LnkSta:"
      print ylw_clr + cmd + def_clr
      subprocess.call(cmd, shell=True)

except(subprocess.CalledProcessError):
  print red_clr + " No NVidia V100 found!!" + def_clr
