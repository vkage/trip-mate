import sys
import os
import re

cfg_file = open('modified/yolov3-voc_gui.cfg','r').readlines()
weight = open('modified/gui_weights.txt','w')
res1 = open('cmp2','w')

#------------------------------------------------------------------

num_of_weights = 0

flag = -1
filters_list = []
size_list = []
layer_out = {}
layer_in = {}
layer_count = -1
conv_count = -1
prev_conv = -1
dic = {}
c0 = 3
temp = -1
temp = -1

#------------------------------------------------------------------

def route(lst,layer_no):
	# try:
	# 	dic[ lst[0] ]
	# 	if len(lst)>1:
	# 		dic[ lst[1] ]
	# except Exception as e:
	# 	lst[0]-=1

	# try:
	# 	if len(lst)>1:
	# 		dic[ lst[1] ]
	# except Exception as e:
	# 	lst[1]-=1
	
	# if len(lst)==1:
	# 	filters_list[conv_count] =  filters_list[ dic[ lst[0] ] ]
	# else:			
	# 	filters_list[conv_count] = filters_list[ dic[ lst[0] ] ] + filters_list[ dic[ lst[1] ] ]

	if len(lst)==1:
		temp = layer_out[lst[0]]
	else:
		temp = layer_out[lst[0]] + layer_out[lst[1]]

#------------------------------------------------------------------

for line in cfg_file:
	if line.find('filters') != -1:
		filt = int(line[line.find('=')+1:] )
		filters_list.append(filt)
		
	if line.find('size') != -1:
		sz = int(line[line.find('=')+1:] )
		size_list.append(sz)

layer_in.update({0:c0})

for line in cfg_file:
	
	line = line.strip()

	if line.find('[convolutional]') != -1:
		conv_count+=1
		layer_count+=1
		if conv_count > 0:
			layer_in.update({layer_count:filters_list[conv_count-1]})
		if temp > 0:
			layer_in.update({layer_count:temp})
			temp = 0
		layer_out.update({layer_count:filters_list[conv_count]})
		dic.update({layer_count:conv_count})
		res1.write(str(  layer_out[layer_count]  ) + '\n') # ----------
		flag = 1
		continue

	if line.find('[route]') != -1 :
		flag = 2
		layer_count+=1
		continue

	if line.find('[shortcut]') != -1 :
		layer_count+=1
		dic.update({layer_count:conv_count})
		layer_in.update({layer_count:filters_list[conv_count]})
		layer_out.update({layer_count:filters_list[conv_count]})
		continue

	if line.find('[upsample]') != -1 :
		layer_count+=1
		dic.update({layer_count:conv_count})
		layer_in.update({layer_count:filters_list[conv_count]})
		layer_out.update({layer_count:filters_list[conv_count]})
		continue

	if line.find('[yolo]') != -1 :
		layer_count+=1
		continue


	if flag == 1 and prev_conv != conv_count:
		prev_conv+=1

	if flag == 2 and line.find('layers') != -1:
		ls = re.split('=|= | = |, | , | ', line)
		ls.remove('layers')
		toLayer = [int(item) if int(item)>0 else layer_count + int(item) for item in ls]

		route(toLayer,layer_count)

#print(layer_in)
#print('---------')
#print(layer_out)


for conv_layer in dic.values():
	

for i in range(len(filters_list)):
	num_of_weights += size_list[i]*size_list[i]*c0*filters_list[i]+filters_list[i]
	c0 = filters_list[i]
	#res1.write(str(c0) + '\n')

#------------------------------------------------------------------
num_of_weights += 78917

print('Total number of weights : %d\n'%(num_of_weights))
print('Total number of weights in bytes : %d bytes\n'%(num_of_weights*4))
print('Total number of weights in Mbytes : %d Mbytes\n'%(num_of_weights*4/(1000000.0)))

weight.write('Total number of weights : %d\n'%(num_of_weights))
weight.write('Weights in bytes : %d bytes\n'%(num_of_weights*4))
weight.write('Weights in Mbytes : %d Mbytes\n'%(num_of_weights*4/(1000000.0)))
weight.close()

res1.close()