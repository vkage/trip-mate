import sys
import os

log = open('Class2.txt','r').readlines()
res = open('Class2_res.txt','w')

sum  = 0.0
num_of_weights = 0


for l in log:
	if l.find('conv') != -1:
		ls = l.split()
		if len(ls) == 21:
			layer = int(ls[0])
			n = int(ls[2])
			f = int(ls[3])
			s = int(ls[7])
			h0 = int(ls[8])
			w0 = int(ls[10])
			c0 = int(ls[12])
			h1 = int(ls[14])
			w1 = int(ls[16])
			c1 = int(ls[18])

			curr_wts = f*f*c0*c1 + c1
			num_of_weights += curr_wts

			res.write('layer:%d weights:%d Sub Sum:%d\n'%(layer,curr_wts,num_of_weights))			

		else:
			f = int(ls[3])
			
			if ls[11].find('1024') != -1:
				c0 = 1024
				c1 = int(ls[17])
			else:
				c0 = int(ls[12])
				c1 = 1024

			curr_wts = f*f*c0*c1 + c1
			num_of_weights += curr_wts

			res.write('layer:%d weights:%d Sub Sum:%d\n'%(layer,curr_wts,num_of_weights))			

			

res.write('Total number of weights : %d\n'%(num_of_weights))
res.write('Total number of weights in bytes : %d\n'%(num_of_weights*4))
res.write('Total number of weights in Mbytes : %d\n'%(num_of_weights*4/(1024.0*1024)))
res.close()
