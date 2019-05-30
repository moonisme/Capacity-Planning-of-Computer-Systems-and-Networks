import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from sim import *

"""
#--------------------------------#
# project for COMP9334           #
# author: Zheyuan Xu             #
# zid: z5190669                  #
# last commit time: 18.4.2019    #
#--------------------------------#
"""

# use this file to draw figures.
# run files such as sim_report.py, same_seed.py, diff_seed.py, diff_end_time.py first.
# then use data generated by those files to draw different figures.
# figures for inter-arrival or service time distribution can be draw directly, no need to run those files before.
# Remember to change different axis, label and legand.

# s = read_file_split('mrt_8.txt')
#
# a = []
# b = []
# for i in range(0,len(s)):
#     a.append(float(s[i][0]))
#     b.append(float(s[i][1]))

# k = 0
# for i in range(0,len(a)):
#     k += float(a[i])
#
# print(k/len(a))
#np.random.seed(32767)
# L = []

# for i in range(0,10000):
#     #L.append(-np.log(1-np.random.uniform(0,1))/9.72)       # inter-arrival
#     #L.append((np.random.uniform(0,1)*(1-0.86)/0.3946 + 0.01**(1-0.86))**(1/(1-0.86)))  # service time
#     L.append(np.random.uniform(1.2, 1.47))
# plt.hist(L,rwidth=0.8,bins=30)
# L =[]
# for i in range(0,len(s)):
#     L.append(float(s[i][0]))
# plt.hist(L,rwidth=0.8,bins=30)
# plt.xlabel('mean response time')
# plt.ylabel('number of generate data')
####################################
#diff_end_time
# s = read_file_split('mrt_8.txt')
# a = []
# b = []
# for i in range(0,len(s)):
#     a.append(float(s[i][0]))
#     b.append(float(s[i][1]))
# plt.plot(b,a)
# plt.axis([1,1000,0,1.5])
# plt.xlabel('end time')
# plt.ylabel('mean response time')
# plt.legend(['fogTimeLimit = 0.11'])
##################################
# sim_report diff_fogTimeLimit
# s = read_file_split('mrt_8.txt')
# a = []
# b = []
# for i in range(0,len(s)):
#     a.append(float(s[i][0]))
#     b.append(float(s[i][1]))
# plt.plot(b,a)
# #plt.axis([0.05,0.16,0,1])
# plt.xlabel('fogTimeLimit')
# plt.ylabel('mean response time')
# plt.legend(['end time = 1000'])
# plt.show()
###################################
# diff_seed
s = read_file_split('mrt_8.txt')

a = []
b = []
for i in range(0,len(s)):
    a.append(float(s[i][0]))
    b.append(float(s[i][1]))

r = np.std(a, ddof = 1)
print(r)
k = 0
for i in range(0,len(a)):
    k += float(a[i])
print(k/len(a))
plt.hist(a,rwidth=0.8,bins=30)
plt.xlabel('mean response time')
plt.ylabel('number of generate data')
plt.legend(['replications: 1000\n'+'fogTimeLimit = 0.108'])
plt.show()
#plt.xlabel('network latency')
#plt.xlabel('fogTimeLimit')
#plt.ylabel('number of generate data')
#plt.ylabel('mean response time')
#plt.scatter(b,a,s = 1)
#plt.legend(['fogTimeLimit = 0.112\n'+'       end time = 700'])
#plt.legend(['total number of generate data: 10000'])
#plt.legend(['end time = 700'])
#plt.legend(['replications: 1000\n'+'fogTimeLimit = 0.106'])
# plt.show()
