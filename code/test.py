from sim import *

"""
#--------------------------------#
# project for COMP9334           #
# author: Zheyuan Xu             #
# zid: z5190669                  #
# last commit time: 18.4.2019    #
#--------------------------------#
"""

# I used this file to test the correctness of my random mode simulation.
# All parts should work fine now.

paralist    = read_file('para_7.txt')
arrivallist = read_file('arrival_7.txt')
servicelist = read_file('service_7.txt')
networklist = read_file('network_7.txt')

fogTimeLimit = float(paralist[0])
fogTimeTocloud = float(paralist[1])
time_end = float(paralist[2])
    #print(fogTimeLimit)

fog_sim = random_fog(arrivallist, paralist, servicelist, networklist, 32767)

with open('fog_dep_7.txt','w') as f:
    for j in range(0, len(fog_sim)):
        f.writelines(fog_sim[j][0] + '  ' + fog_sim[j][1] +'\n')

orderlist = read_file_split('fog_dep_test.txt')
network_service = read_file('network_service.txt')
network_network = read_file('network_network.txt')
network_sim = random_network(paralist, orderlist, network_service, network_network)

with open('net_dep_7.txt','w') as f:
    for j in range(0,len(network_sim)):
        f.writelines(network_sim[j][0] + '  ' + network_sim[j][1] +'\n')

netdeparturelist = read_file_split('net_dep_test.txt')
cloud_sim = random_cloud(paralist, netdeparturelist, network_service)

with open('cloud_dep_7.txt','w') as f:
    for j in range(0,len(cloud_sim)):
        f.writelines(cloud_sim[j][0] + '  ' + cloud_sim[j][1] +'\n')

# Response = meanResponseTime('response.txt')
# with open('mrt_4.txt','a+') as f:
#     f.writelines('%.4f'% Response + '  ' + str(fogTimeLimit) + '\n')

Response = meanResponseTime('response.txt')
with open('mrt_7.txt','w') as f:
    f.writelines('%.4f'% Response)