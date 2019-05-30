from sim import *

"""
#--------------------------------#
# project for COMP9334           #
# author: Zheyuan Xu             #
# zid: z5190669                  #
# last commit time: 18.4.2019    #
#--------------------------------#
"""

# This wrapper file can loop through all the test cases.

num_test = read_file('num_tests.txt')

for i in range(1,int(num_test[0])+1):

    mode = read_file('mode_'+str(i)+'.txt')

    paralist    = read_file('para_'+str(i)+'.txt')
    arrivallist = read_file('arrival_'+str(i)+'.txt')
    servicelist = read_file('service_'+str(i)+'.txt')
    networklist = read_file('network_'+str(i)+'.txt')

    if (str(mode[0]) == 'random'):

        fog_sim = random_fog(arrivallist, paralist, servicelist, networklist, 32767)

        with open('fog_dep_'+str(i)+'.txt','w') as f:
            for j in range(0,len(fog_sim)):
                f.writelines(fog_sim[j][0] + '  ' + fog_sim[j][1] +'\n')

        orderlist = read_file_split('fog_dep_test.txt')
        network_service = read_file('network_service.txt')
        network_network = read_file('network_network.txt')
        network_sim = random_network(paralist, orderlist, network_service, network_network)

        with open('net_dep_'+str(i)+'.txt','w') as f:
            for j in range(0,len(network_sim)):
                f.writelines(network_sim[j][0] + '  ' + network_sim[j][1] +'\n')

        netdeparturelist = read_file_split('net_dep_test.txt')
        cloud_sim = random_cloud(paralist, netdeparturelist, network_service)

        with open('cloud_dep_'+str(i)+'.txt','w') as f:
            for j in range(0,len(cloud_sim)):
                f.writelines(cloud_sim[j][0] + '  ' + cloud_sim[j][1] +'\n')

        Response = meanResponseTime('response.txt')
        with open('mrt_'+str(i)+'.txt','w') as f:
            f.writelines('%.4f'% Response)

    elif (str(mode[0]) == 'trace'):

        fog_sim = trace_fog(paralist, arrivallist, servicelist, networklist)

        with open('fog_dep_'+str(i)+'.txt','w') as f:
            for j in range(0,len(fog_sim)):
                f.writelines(fog_sim[j][0] + '  ' + fog_sim[j][1] +'\n')

        orderlist = read_file_split('fog_dep_test.txt')
        network_sim = trace_network(paralist, orderlist, servicelist, networklist)

        with open('net_dep_'+str(i)+'.txt','w') as f:
            for j in range(0,len(network_sim)):
                f.writelines(network_sim[j][0] + '  ' + network_sim[j][1] +'\n')

        netdeparturelist = read_file_split('net_dep_test.txt')
        cloud_sim = trace_cloud(paralist, netdeparturelist, servicelist)

        with open('cloud_dep_'+str(i)+'.txt','w') as f:
            for j in range(0,len(cloud_sim)):
                f.writelines(cloud_sim[j][0] + '  ' + cloud_sim[j][1] +'\n')

        Response = meanResponseTime('response.txt')
        with open('mrt_'+str(i)+'.txt','w') as f:
            f.writelines('%.4f'% Response)
    else:
        print('Invalid input, giving up.')

    print(f'test{i} finished')

