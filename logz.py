import sys
import os

log = open('Class20.txt','r').readlines()
res = open('Class20_res.txt','w')
res1 = open('cmp1','w')

# cfg_file = open('modified/yolov3-voc_gui.cfg','r').readlines()
# weight = open('modified/gui_weights.txt','w')

num_of_weights = 0

class Layer:
	layer_no = 0
	type_l = ''
	filters = 0
	f = 0
	s = 0
	h0 = 0
	w0 = 0
	h1 = 0
	w1 = 0
	c0 = 0
	c1 = 0
	#res or shortcut
	toLayer = 0
	#route
	toLayerList = []
	#upsample
	factor = 0

	def conv_pram(self,line):
		print('--------cp----------')
		self.type_l = 'conv'
		self.filters = line[2]
		self.f = int(line[3])
		self.s = int(line[7])
		self.h0 = int(line[8])
		self.w0 = int(line[10])
		if len(line) == 21:
			self.c0 = int(line[12])
			self.c1 = int(line[18])
			self.h1 = int(line[14])
			self.w1 = int(line[16])
		elif line[11].find('1024') != -1:
			self.c0 = 1024
			self.c1 = int(line[17])
			self.h1 = int(line[13])
			self.w1 = int(line[15])
		else:
			self.c0 = int(line[12])
			self.c1 = 1024
			self.h1 = int(line[14])
			self.w1 = int(line[16])

	def res_pram(self,line):
		print('--------rp----------')
		self.type_l = 'res'
		self.toLayer = int(line[2])
		self.h0 = int(line[3])
		self.w0 = int(line[5])
		if len(line) == 14:
			self.c0 = int(line[7])
			self.c1 = int(line[13])
			self.h1 = int(line[9])
			self.w1 = int(line[11])

		else:
			self.c0 = 1024
			self.c1 = 1024
			self.h1 = int(line[8])
			self.w1 = int(line[10])
	
	def route_pram(self,line):
		print('--------rop----------')
		self.type_l = 'route'
		self.toLayerList = [i for i in line[2:]]
		
	def upsample_pram(self,line):
		print('--------up----------')
		self.type_l = 'upsample'
		self.factor = int( line[2].split('x')[0] )
		self.h0 = int(line[3])
		self.w0 = int(line[5])
		self.c0 = int(line[7])
		self.h1 = int(line[9])
		self.w1 = int(line[11])
		self.c1 = int(line[13])		

	def weight(self):
		print('--------wt----------')
		if self.type_l == 'conv':
			print('--------f - %d c0 - %d c1 - %d----------'%(self.f,self.c0,self.c1))
			res1.write(str(self.c1)+'\n')
			return self.f*self.f*self.c0*self.c1*1.0 + self.c1
		elif self.type_l == 'res':
			return 0
		elif self.type_l == 'route':
			return 0
		elif self.type_l == 'upsample':
			return 0
		else: 
			return 0

	# def printer(self):
	# 	print('--------1----------')
	# 	print(self.layer_no,self.type_l,self.f,self.s,self.h0,self.w0,self.c0,self.h1,self.w1,self.c1)


#	GLOBAL

Layer_list = []

for line in log:
	lst = line.split()

	print(line)
	print(lst)

	L = Layer()
	if lst[1] == 'conv':
		L.conv_pram(lst)
	elif lst[1] == 'res':
		L.res_pram(lst)
	elif lst[1] == 'upsample':
		L.upsample_pram(lst)
	else:
		L.route_pram(lst)
	Layer_list.append(L)


for l in Layer_list:
	num_of_weights = num_of_weights + l.weight()
	#print(num_of_weights)



num_of_weights = num_of_weights + 78917

print('Total number of weights : %d\n'%(num_of_weights))
print('Total number of weights in bytes : %d bytes\n'%(num_of_weights*4))
print('Total number of weights in Mbytes : %d Mbytes\n'%(num_of_weights*4/(1000000.0)))

res.write('Total number of weights : %d\n'%(num_of_weights))
res.write('Weights in bytes : %d bytes\n'%(num_of_weights*4))
res.write('Weights in Mbytes : %d Mbytes\n'%(num_of_weights*4/(1000000.0)))
res.close()
res1.close()
#54--conv--512--3--x--3--/--1--26--x--26--x--256--->--26--x--26--x--512--1.595--BFLOPs
#['63', 'conv', '512', '1', 'x', '1', '/', '1', '13', 'x', '13', 'x1024', '->', '13', 'x', '13', 'x', '512', '0.177', 'BFLOPs']
#['64', 'conv', '1024', '3', 'x', '3', '/', '1', '13', 'x', '13', 'x', '512', '->', '13', 'x', '13', 'x1024', '1.595', 'BFLOPs']

# conv ----------
# res -----------

# route ---------
# upsample 	