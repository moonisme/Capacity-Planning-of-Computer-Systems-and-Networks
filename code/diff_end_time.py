from sim import *

time_end = 0

while(time_end <= 1000):
    paralist    = read_file('para_8.txt')
    arrivallist = read_file('arrival_8.txt')
    servicelist = read_file('service_8.txt')
    networklist = read_file('network_8.txt')

    fogTimeLimit = float(paralist[0])
    fogTimeTocloud = float(paralist[1])
    time_end = float(paralist[2])
    #print(fogTimeLimit)

    fog_sim = random_fog(arrivallist, paralist, servicelist, networklist, 32767)

    with open('fog_dep_8.txt','w') as f:
        for j in range(0, len(fog_sim)):
            f.writelines(fog_sim[j][0] + '  ' + fog_sim[j][1] +'\n')

    orderlist = read_file_split('fog_dep_test.txt')
    network_service = read_file('network_service.txt')
    network_network = read_file('network_network.txt')
    network_sim = random_network(paralist, orderlist, network_service, network_network)

    with open('net_dep_8.txt','w') as f:
        for j in range(0,len(network_sim)):
            f.writelines(network_sim[j][0] + '  ' + network_sim[j][1] +'\n')

    netdeparturelist = read_file_split('net_dep_test.txt')
    cloud_sim = random_cloud(paralist, netdeparturelist, network_service)

    with open('cloud_dep_8.txt','w') as f:
        for j in range(0,len(cloud_sim)):
            f.writelines(cloud_sim[j][0] + '  ' + cloud_sim[j][1] +'\n')

    Response = meanResponseTime('response.txt')
    with open('mrt_8.txt','a+') as f:
        f.writelines('%.4f'% Response + '  ' + str(time_end) + '\n')

    time_end += 1
    with open('para_8.txt','w') as f:
        f.write('%.4f'% fogTimeLimit + '\n')
        f.write(str(fogTimeTocloud) +'\n')
        f.write(str(time_end) + '\n')


