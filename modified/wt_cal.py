import subprocess
import os
import sys
#train_cmd_str = './darknet detector train modified/voc_gui.data modified/yolov3-voc_gui.cfg darknet53.conv.74 -gpus 0'
train_cmd_str = './darknet detector train modified/voc_gui.data cfg/yolov3-voc_gui.cfg backup/yolov3-voc_gui.backup -gpus 0,1'

print('\n\n\n\n---------------------\n\n\n\n')

proc = subprocess.Popen(train_cmd_str,stdout = subprocess.PIPE, shell=True)

print('\n\n\n\n---------------------\n\n\n\n')

print(proc.pid)

print('\n\n\n\n---------------------\n\n\n\n')

proc.terminate()

out, err = proc.communicate()

print('\n\n\n\n---------------------\n\n\n\n')


print(out)

print('\n\n\n\n---------------------\n\n\n\n')

print(err)