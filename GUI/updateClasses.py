import sys
import os
import subprocess


Num_classes = int(sys.argv[1])
classes = str(sys.argv[2:])

#print(Num_classes)

wd = os.getcwd()

#file_name = ''

#--------------------------------------------------------------------
# creating voc.names file as voc_gui.names
#--------------------------------------------------------------------
voc_gui = open('%s/modified/voc_gui.names'%(wd),'w')
for l in sys.argv[2:]:
    voc_gui.write(l+'\n')
    #file_name+=l[0]
voc_gui.close()

#--------------------------------------------------------------------
# Converting scripts/voc_label.py
#--------------------------------------------------------------------
voc_label = open('%s/scripts/voc_label.py'%(wd),'r').readlines()
voc_label_gui = open('%s/voc_label_gui.py'%(wd), 'w')
for line in voc_label:
    if line.find('classes') == 0:
        voc_label_gui.write('classes = '+classes+'\n')
    else:
        voc_label_gui.write(line)
voc_label_gui.close()

#--------------------------------------------------------------------
# Creating train file 
#--------------------------------------------------------------------
subprocess.call('python voc_label_gui.py',shell=True)


#--------------------------------------------------------------------
# Converting cfg/voc.data
#--------------------------------------------------------------------
voc_data_gui = open('%s/modified/voc_gui.data'%(wd),'w')

voc_data_gui.write('classes = '+str(Num_classes)+'\n')
voc_data_gui.write('train  = train.txt\n')
voc_data_gui.write('valid  = 2007_test.txt\n')
voc_data_gui.write('names  = modified/voc_gui.names\n')
voc_data_gui.write('backup  = backup\n')

voc_data_gui.close()

#--------------------------------------------------------------------
# Converting cfg/yolov3-voc.cfg
#--------------------------------------------------------------------
yolov3_voc = open('%s/cfg/yolov3-voc.cfg'%(wd),'r').readlines()
#yolov3_voc_gui = open('cfg/yolov3-%s'%(file_name)+'.cfg', 'w')
yolov3_voc_gui = open('modified/yolov3-voc_gui.cfg', 'w')

train_flag = 0
test_flag = 0

index_arr = []
index = 0

for line in yolov3_voc:
    if line.find('classes') != -1:
        index_arr.append(index)
    index+=1

index = 0

for line in yolov3_voc:

    if train_flag != 0:
        train_flag-=1
        index+=1
        continue

    if test_flag != 0:
        test_flag-=1
        index+=1
        continue

    if line.find('Testing') != -1:
        yolov3_voc_gui.write('#Testing\n#batch=1\n#subdivisions=1\n')
        test_flag = 2
        index+=1
        continue

    if line.find('Training') != -1:
        yolov3_voc_gui.write('#Training\nbatch=64\nsubdivisions=16\n')
        train_flag = 2
        index+=1
        continue

    if index == index_arr[0]-6:
        yolov3_voc_gui.write('filters=%d'%(3*(Num_classes+5))+'\n')
        index+=1
        continue

    if index == index_arr[1]-6:
        yolov3_voc_gui.write('filters=%d'%(3*(Num_classes+5))+'\n')
        index+=1
        continue

    if index == index_arr[2]-6:
        yolov3_voc_gui.write('filters=%d'%(3*(Num_classes+5))+'\n')
        index+=1
        continue

    # for i in index_arr:
    #     if index == index_arr[0]-6:
    #         yolov3_voc_gui.write('filters=%d'%(3*(Num_classes+5))+'\n')
    #         index+=1
    #         continue



    if index == index_arr[0]:
        yolov3_voc_gui.write('classes=%d'%(Num_classes)+'\n')
        index+=1
        continue


    if index == index_arr[1]:
        yolov3_voc_gui.write('classes=%d'%(Num_classes)+'\n')
        index+=1
        continue

    if index == index_arr[2]:
        yolov3_voc_gui.write('classes=%d'%(Num_classes)+'\n')
        index+=1
        continue

    yolov3_voc_gui.write(line)
    index+=1

yolov3_voc_gui.close()

