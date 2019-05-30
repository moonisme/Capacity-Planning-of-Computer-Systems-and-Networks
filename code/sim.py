import numpy as np
from sys import maxsize
from scipy.stats import *
from math import *
import copy
import operator

"""
#--------------------------------#
# project for COMP9334           #
# author: Zheyuan Xu             #
# zid: z5190669                  #
# last commit time: 18.4.2019    #
#--------------------------------#
"""

# This is the final version of simulation for this project, all the simulation functions are included in this file.
# Do not run this file directly.If you want to run through a number of tests, run wrapper.py
# If you want to run a single test, run test.py.
# other files such as sim_report.py, same_seed.py, diff_seed.py, diff_end_time.py are used for generate different data
# for draw.py to draw figures.Remember to clear mrt_8.txt since the write mode is a+.


def get_key(dict,value):
    s = [k for k, v in dict.items() if v == value]
    return float(s[0])

def trace_fog(paralist,arrivallist,servicelist,networklist):
    masterclock = 0                         # update when there is an event
    responseTime = []
    jobcount = 0                            # count number of requests in the fog
    joblist = {}                            # contain arrival time and amount of service still need
    event = []                              # a list of masterclock
    order = []                              # contain arrival time of each request                                         # contain departure time from fog of each request
    current = []                            # contain departure time of each request
    arrivalTime = []                        # store arrival time read from file
    arrivalcount = 0                        # count arrival number
    departureTime = maxsize                 # departure time
    departurecount = 0                      # count departure number
    serviceTime = []                        # store service time read from file
    networkTime = []                        # store network time read from file
    fogTimeLimit = float(paralist[0])
    bias = 1/100000
    deparr = []

    for i in arrivallist:
        arrivalTime.append(float(str(i)))
    for i in servicelist:
        serviceTime.append(float(str(i)))
    for i in networklist:
        networkTime.append(float(str(i)))

    for i in range(1,len(arrivalTime)):
        if(arrivalTime[i-1] == arrivalTime[i]):
            arrivalTime[i] += bias

    while(departurecount < len(arrivalTime)):       # stop simulation when all requests has been departured
        if(arrivalcount >= len(arrivalTime)):       # to handle margin issue
            masterclock = departureTime
        else:
            masterclock = min(arrivalTime[arrivalcount],departureTime)
        event.append(masterclock)
        if(joblist):
            for key in joblist:
                joblist[key] -= (event[-1] - event[-2])/jobcount
        if(masterclock in arrivalTime):
            jobcount += 1
            if(serviceTime[arrivalcount] <= fogTimeLimit):
                joblist[arrivalTime[arrivalcount]] = serviceTime[arrivalcount]
                a = []
                for value in joblist.values():
                    a.append(value)
                departureTime = min(a)*jobcount + event[-1]
                #print(f'departureTime: {departureTime}\n')
                #print(joblist)
                arrivalcount +=1
            else:
                joblist[arrivalTime[arrivalcount]] = fogTimeLimit
                a = []
                for value in joblist.values():
                    a.append(value)
                if(len(joblist) != 1):
                    departureTime = min(a) * jobcount + event[-1]
                else:
                    departureTime = event[-1] + fogTimeLimit
                #joblist[arrivalTime[arrivalcount]] = fogTimeLimit
                #print(f'departureTime: {departureTime}\n')
                #print(joblist)
                arrivalcount +=1
            #print(f'masterclock:{masterclock} joblist:{joblist}')
            #print(f'Masterclock: {masterclock}, arrival {arrivalcount}')
        else:
            if(len(joblist) == 1):
                minValue = min(joblist.values())
                for i, j in joblist.items():
                    if j == minValue:
                        #order.append(i)
                        deparr.append(get_key(joblist, j))
                current.append(masterclock)
                #deparr.append(get_key(joblist, j))

                joblist = {}
                departureTime = maxsize
                jobcount -= 1
            else:
                minValue = min(joblist.values())
                for i, j in joblist.items():
                    if j == minValue:
                        #order.append(i)
                        deparr.append(get_key(joblist, j))
                current.append(masterclock)
                #deparr.append(get_key(joblist, j))
                a = []
                for value in joblist.values():
                    a.append(value)
                del joblist[get_key(joblist,min(a))]
                jobcount -= 1
                a = []
                for value in joblist.values():
                    a.append(value)
                departureTime = min(a) * jobcount + event[-1]
            #print(f'departureTime: {departureTime}\n')
            departurecount +=1
            #print(f'masterclock:{masterclock} joblist:{joblist}')
            #print(f'Masterclock: {masterclock}, departure {departurecount}')

    #order = [('%.4f'%i) for i in order]
    current = [('%.20f'%i) for i in current]
    deparr = [('%.20f'%i) for i in deparr]
    arrivalTime = [('%.20f'%i) for i in arrivalTime]
    k = [list(x) for x in zip(deparr, current)]
    k.sort(key=lambda x: float(x[0]))
    s = copy.deepcopy(k)
    # for i in range(0, len(k)):
    #     k[i][0] = arrivalTime[i]
    for i in range(0,len(k)):
        k[i][0] = '%.4f' %float(k[i][0])
        k[i][1] = '%.4f' % float(k[i][1])

    #print(k)
    for i in range(0,len(networkTime)):
        if(networkTime[i] == 0):
            responseTime.append(float(k[i][1]) - float(k[i][0]))
    responseTime = [('%.20f' % i) for i in responseTime]

    with open('response.txt','w') as f:
        for i in range(0,len(responseTime)):
            f.writelines(responseTime[i] + '\n')

    with open('fog_dep_test.txt','w') as f:
        for i in range(0,len(s)):
            f.writelines(s[i][0] + '  ' + s[i][1] +'\n')
    return k

def trace_network(paralist,orderlist,servicelist,networklist):
    fogTimeLimit = float(paralist[0])
    order = []
    _order = []     # eliminate requests finish in fog
    current = []
    serviceTime = []
    networkTime = []
    networkdeparture = []   # departure time + network lantency
    for i in orderlist:
        order.append(float(str(i[0])))
        current.append(float(str(i[1])))
    for i in servicelist:
        serviceTime.append(float(str(i)))
    for i in networklist:
        networkTime.append(float(str(i)))
    for i in range(0,len(current)):
        if(networkTime[i] == 0):
            pass
        else:
            _order.append(order[i])
            networkdeparture.append(current[i] + networkTime[i])

    _order = [('%.20f' % i) for i in _order]
    networkdeparture = [('%.20f' % i) for i in networkdeparture]

    k = [list(x) for x in zip(_order, networkdeparture)]
    k.sort(key = lambda x: float(x[0]))
    s = copy.deepcopy(k)
    for i in range(0,len(k)):
        k[i][0] = '%.4f' %float(k[i][0])
        k[i][1] = '%.4f' % float(k[i][1])

    with open('net_dep_test.txt','w') as f:
        for i in range(0,len(s)):
            f.writelines(s[i][0] + '  ' + s[i][1] +'\n')
    return k


def trace_cloud(paralist,netdeparturelist,servicelist):
    fogTimeLimit = float(paralist[0])
    fogTimeToCloudTime = float(paralist[1])
    responseTime = []
    arrivalinFog = []
    arrivalinCloud = []
    serviceTime = []
    serviceTimeinCloud = []
    masterclock = 0
    arrivalcount = 0
    departurecount = 0
    departureTime = maxsize
    bias = 1/100000
    event = []
    joblist = {}
    jobcount = 0
    order = []          # conatin arrival at cloud time for each request
    current = []        # contain departure time from cloud for each request
    deparr = []            # get the correct order of departure time

    for i in servicelist:
        serviceTime.append(float(str(i)))

    for i in range(0,len(serviceTime)):
        if serviceTime[i] > fogTimeLimit:
            serviceTimeinCloud.append(float(fogTimeToCloudTime*(serviceTime[i]-fogTimeLimit)))
    for i in netdeparturelist:
        arrivalinFog.append(float(str(i[0])))
        arrivalinCloud.append(float(str(i[1])))

    for i in range(1,len(arrivalinCloud)):              # handle special case when arrival time is not ordered
        if arrivalinCloud[i] < arrivalinCloud[i-1]:
            arrivalinCloud[i-1],arrivalinCloud[i] = arrivalinCloud[i],arrivalinCloud[i-1]
            serviceTimeinCloud[i-1],serviceTimeinCloud[i] = serviceTimeinCloud[i],serviceTimeinCloud[i-1]
            arrivalinFog[i-1], arrivalinFog[i] = arrivalinFog[i], arrivalinFog[i-1]

    for i in range(1,len(arrivalinCloud)):
        if(arrivalinCloud[i-1] == arrivalinCloud[i]):
            arrivalinCloud[i] += bias

    while (departurecount < len(arrivalinCloud)):  # stop simulation when all requests has been departured
        if (arrivalcount >= len(arrivalinCloud)):  # to handle boundary issue
            masterclock = departureTime
        else:
            masterclock = min(arrivalinCloud[arrivalcount], departureTime)
        event.append(masterclock)
        if (joblist):
            for key in joblist:
                joblist[key] -= (event[-1] - event[-2]) / jobcount
        if (masterclock in arrivalinCloud):
            jobcount += 1
            joblist[arrivalinCloud[arrivalcount]] = serviceTimeinCloud[arrivalcount]
            a = []
            for value in joblist.values():
                a.append(value)
            departureTime = min(a) * jobcount + event[-1]
            # print(f'departureTime: {departureTime}\n')
            # print(joblist)
            arrivalcount += 1
            #print(f'masterclock:{masterclock} joblist:{joblist}')
        else:
            if (len(joblist) == 1):
                minValue = min(joblist.values())
                for i, j in joblist.items():
                    if j == minValue:
                        #order.append(i)
                        deparr.append(get_key(joblist, j))
                current.append(masterclock)
                #deparr.append(get_key(joblist,j))
                joblist = {}
                departureTime = maxsize
                jobcount = 0
            else:
                minValue = min(joblist.values())
                for i, j in joblist.items():
                    if j == minValue:
                        #order.append(i)
                        deparr.append(get_key(joblist, j))
                current.append(masterclock)
                a = []
                for value in joblist.values():
                    a.append(value)
                del joblist[get_key(joblist, min(a))]
                jobcount -= 1
                a = []
                for value in joblist.values():
                    a.append(value)
                departureTime = min(a) * jobcount + event[-1]
            # print(f'departureTime: {departureTime}\n')
            departurecount += 1
            #print(f'masterclock:{masterclock} joblist:{joblist}')
    #order = [('%.4f' % i) for i in order]
    current = [('%.20f' % i) for i in current]
    deparr = [('%.20f' % i) for i in deparr]
    arrivalinFog = [('%.20f' % i) for i in arrivalinFog]

    k = [list(x) for x in zip(deparr, current)]
    k.sort(key = lambda x: float(x[0]))

    for i in range(0,len(k)):
        k[i][0] = arrivalinFog[i]
    k.sort(key = lambda x: float(x[0]))

    for i in range(0,len(k)):
        k[i][0] = '%.4f' %float(k[i][0])
        k[i][1] = '%.4f' % float(k[i][1])
    #print(k)
    # with open('cloud_dep_test.txt','w') as f:
    #     for i in range(0,len(k)):
    #         f.writelines(k[i][0] + '  ' + k[i][1] +'\n')

    for i in k:
        responseTime.append(float(i[1]) - float(i[0]))
    responseTime = [('%.20f' % i) for i in responseTime]

    with open('response.txt','a+') as f:
        for i in range(0,len(responseTime)):
            f.writelines(responseTime[i] + '\n')

    return k

def meanResponseTime(filename):
    with open(filename, 'r') as f:
        responselist = f.readlines()
    for i in range(0, len(responselist)):
        responselist[i] = responselist[i].rstrip()

    ResponseTime = 0
    for i in range(0,len(responselist)):
        ResponseTime += float(responselist[i])
    ResponseTime /= len(responselist)

    # with open('mrt_test.txt','w') as f:
    #     f.writelines('%.4f'% ResponseTime)
    return ResponseTime

def random_fog(arrivallist,paralist,servicelist,networklist,random_seed):

    lambd = float(arrivallist[0])
    masterclock = 0  # update when there is an event
    responseTime = []
    jobcount = 0  # count number of requests in the fog
    joblist = {}  # contain arrival time and amount of service still need
    event = []  # a list of masterclock
    order = []  # contain arrival time of each request
    current = []  # contain departure time of each request
    arrivalTime = []  # store arrival time read from file
    arrivalcount = 0  # count arrival number
    departureTime = maxsize  # departure time
    departurecount = 0  # count departure number
    serviceTime = []  # store service time read from file
    networkTime = []  # store network time read from file
    fogTimeLimit = float(paralist[0])
    deparr = []

    end_time = float(paralist[2])
    alpha1 = float(servicelist[0])
    alpha2 = float(servicelist[1])
    beta = float(servicelist[2])
    gamma = (1-beta)/((alpha2**(1-beta))-(alpha1**(1-beta)))
    networkTime = []
    np.random.seed(random_seed)
    next_arrival = -np.log(1-np.random.uniform(0,1))/lambd
    next_service = (np.random.uniform(0,1)*(1-beta)/gamma + alpha1**(1-beta))**(1/(1-beta))

    while (next_arrival < end_time-1):
        arrivalTime.append(next_arrival)
        next_arrival += (-np.log(1-np.random.uniform(0,1))/lambd)
        serviceTime.append(next_service)
        next_service = (np.random.uniform(0,1)*(1-beta)/gamma + alpha1**(1-beta))**(1/(1-beta))

    for i in networklist:
        networkTime.append(float(str(i)))
    v1 = float(networkTime[0])
    v2 = float(networkTime[1])

    while (departurecount < len(arrivalTime)):  # stop simulation when all requests has been departured
        if (arrivalcount >= len(arrivalTime)):  # to handle margin issue
            masterclock = departureTime
        else:
            masterclock = min(arrivalTime[arrivalcount], departureTime)
        event.append(masterclock)
        if (joblist):
            for key in joblist:
                joblist[key] -= (event[-1] - event[-2]) / jobcount
        if (masterclock in arrivalTime):
            jobcount += 1
            if (serviceTime[arrivalcount] <= fogTimeLimit):
                joblist[arrivalTime[arrivalcount]] = serviceTime[arrivalcount]
                a = []
                for value in joblist.values():
                    a.append(value)
                departureTime = min(a) * jobcount + event[-1]
                # print(f'departureTime: {departureTime}\n')
                # print(joblist)
                arrivalcount += 1
            else:
                joblist[arrivalTime[arrivalcount]] = fogTimeLimit
                a = []
                for value in joblist.values():
                    a.append(value)
                if (len(joblist) != 1):
                    departureTime = min(a) * jobcount + event[-1]
                else:
                    departureTime = event[-1] + fogTimeLimit
                # joblist[arrivalTime[arrivalcount]] = fogTimeLimit
                # print(f'departureTime: {departureTime}\n')
                # print(joblist)
                arrivalcount += 1
            # print(f'Masterclock: {masterclock}, arrival {arrivalcount}')
        else:
            if (len(joblist) == 1):
                minValue = min(joblist.values())
                for i, j in joblist.items():
                    if j == minValue:
                        # order.append(i)
                        deparr.append(get_key(joblist, j))
                current.append(masterclock)
                # deparr.append(get_key(joblist, j))

                joblist = {}
                departureTime = maxsize
                jobcount = 0
                departurecount += 1
            else:
                minValue = min(joblist.values())
                for i, j in joblist.items():
                    if j == minValue:
                        # order.append(i)
                        deparr.append(get_key(joblist, j))
                current.append(masterclock)
                # deparr.append(get_key(joblist, j))
                a = []
                for value in joblist.values():
                    a.append(value)
                del joblist[get_key(joblist, min(a))]
                jobcount -= 1
                a = []
                for value in joblist.values():
                    a.append(value)
                departureTime = min(a) * jobcount + event[-1]
            # print(f'departureTime: {departureTime}\n')
                departurecount += 1
            # print(f'Masterclock: {masterclock}, departure {departurecount}')

    # order = [('%.4f'%i) for i in order]
    current = [('%.20f' % i) for i in current]
    deparr = [('%.20f' % i) for i in deparr]
    arrivalTime = [('%.20f' % i) for i in arrivalTime]
    k = [list(x) for x in zip(deparr, current)]
    k.sort(key=lambda x: float(x[0]))

    networkTime = []
    for i in range(0,len(k)):
        if(float(serviceTime[i]) <= fogTimeLimit):
            networkTime.append(0)
        else:
            networkTime.append(np.random.uniform(v1,v2))

    # for i in range(0, len(k)):
    #     k[i][0] = arrivalTime[i]
    s = copy.deepcopy(k)
    for i in range(0,len(k)):
        k[i][0] = '%.4f' %float(k[i][0])
        k[i][1] = '%.4f' % float(k[i][1])

    for i in range(0, len(networkTime)):
        if (networkTime[i] == 0):
            responseTime.append(float(k[i][1]) - float(k[i][0]))

    responseTime = [('%.20f' % i) for i in responseTime]
    serviceTime = [('%.20f' % i) for i in serviceTime]
    networkTime = [('%.20f' % i) for i in networkTime]

    with open('response.txt', 'w') as f:
        for i in range(0, len(responseTime)):
            f.writelines(responseTime[i] + '\n')

    with open('fog_dep_test.txt', 'w') as f:
        for i in range(0, len(s)):
            f.writelines(s[i][0] + '  ' + s[i][1] + '\n')

    with open('network_service.txt', 'w') as f:
        for i in range(0,len(serviceTime)):
            f.writelines(serviceTime[i] + '\n')

    with open('network_network.txt','w') as f:
        for i in range(0,len(networkTime)):
            f.writelines(networkTime[i] + '\n')

    return k

def random_network(paralist,orderlist,network_service,network_network):
    fogTimeLimit = float(paralist[0])
    end_time = float(paralist[2])
    order = []
    _order = []  # eliminate requests finish in fog
    current = []
    serviceTime = []
    networkTime = []
    networkdeparture = []  # departure time + network lantency
    for i in orderlist:
        order.append(float(str(i[0])))
        current.append(float(str(i[1])))
    for i in network_service:
        serviceTime.append(float(str(i)))
    for i in network_network:
        networkTime.append(float(str(i)))

    for i in range(0, len(current)):
        if (networkTime[i] == 0):
            pass
        else:
            _order.append(order[i])
            networkdeparture.append(current[i] + networkTime[i])

    #print(serviceTime)
    _order = [('%.20f' % i) for i in _order]
    networkdeparture = [('%.20f' % i) for i in networkdeparture]
    #print(order)
    k = [list(x) for x in zip(_order, networkdeparture)]
    k.sort(key=lambda x: float(x[0]))
    s = copy.deepcopy(k)
    for i in range(0,len(k)):
        k[i][0] = '%.4f' %float(k[i][0])
        k[i][1] = '%.4f' % float(k[i][1])

    with open('net_dep_test.txt', 'w') as f:
        for i in range(0, len(s)):
            f.writelines(s[i][0] + '  ' + s[i][1] + '\n')
    return k

def random_cloud(paralist,netdeparturelist,network_service):
    fogTimeLimit = float(paralist[0])
    fogTimeToCloudTime = float(paralist[1])
    end_time = float(paralist[2])
    responseTime = []
    arrivalinFog = []
    arrivalinCloud = []
    serviceTime = []
    serviceTimeinCloud = []
    masterclock = 0
    arrivalcount = 0
    departurecount = 0
    departureTime = maxsize
    event = []
    joblist = {}
    jobcount = 0
    order = []  # conatin arrival at cloud time for each request
    current = []  # contain departure time from cloud for each request
    deparr = []  # get the correct order of departure time

    for i in network_service:
        serviceTime.append(float(str(i)))
    for i in range(0, len(serviceTime)):
        if serviceTime[i] > fogTimeLimit:
            serviceTimeinCloud.append(float(fogTimeToCloudTime * (serviceTime[i] - fogTimeLimit)))
    for i in netdeparturelist:
        arrivalinFog.append(float(str(i[0])))
        arrivalinCloud.append(float(str(i[1])))

    for i in range(1, len(arrivalinCloud)):  # handle special case when arrival time is not ordered
        if (arrivalinCloud[i] < arrivalinCloud[i - 1]):
            arrivalinCloud[i - 1], arrivalinCloud[i] = arrivalinCloud[i], arrivalinCloud[i - 1]
            serviceTimeinCloud[i - 1], serviceTimeinCloud[i] = serviceTimeinCloud[i], serviceTimeinCloud[i - 1]
            arrivalinFog[i - 1], arrivalinFog[i] = arrivalinFog[i], arrivalinFog[i - 1]

    while (departurecount < len(arrivalinCloud)):  # stop simulation when all requests has departured
        if (arrivalcount >= len(arrivalinCloud)):  # to handle boundary issue
            masterclock = arrivalinCloud[-1]
        else:
            masterclock = min(arrivalinCloud[arrivalcount], departureTime)
            event.append(masterclock)
        if (joblist):
            for key in joblist:
                joblist[key] -= (event[-1] - event[-2]) / jobcount

        if (masterclock in arrivalinCloud and arrivalcount < len(arrivalinCloud)):
            jobcount += 1
            joblist[arrivalinCloud[arrivalcount]] = serviceTimeinCloud[arrivalcount]
            a = []
            for value in joblist.values():
                a.append(value)
            departureTime = min(a) * jobcount + event[-1]
            # print(f'departureTime: {departureTime}\n')
            arrivalcount += 1
        else:
            if(len(joblist) == 1):
                minValue = min(joblist.values())
                for i, j in joblist.items():
                    if j == minValue:
                        # order.append(i)
                        deparr.append(get_key(joblist, j))
                current.append(departureTime)
                # deparr.append(get_key(joblist,j))
                joblist = {}
                departureTime = maxsize
                jobcount = 0
                departurecount += 1
            else:
                if(len(joblist) == 0):
                    print('fking bullshit')
                minValue = min(joblist.values())
                for i, j in joblist.items():
                    if j == minValue:
                            # order.append(i)
                        deparr.append(get_key(joblist, j))
                current.append(departureTime)
                a = []
                for value in joblist.values():
                    a.append(value)
                del joblist[get_key(joblist, min(a))]
                a = []
                for value in joblist.values():
                    a.append(value)
                departureTime = min(a) * jobcount + event[-1]
                jobcount -= 1
                departurecount += 1

    # order = [('%.4f' % i) for i in order]
    current = [('%.20f' % i) for i in current]
    deparr = [('%.20f' % i) for i in deparr]
    arrivalinFog = [('%.20f' % i) for i in arrivalinFog]

    k = [list(x) for x in zip(deparr, current)]
    k.sort(key=lambda x: float(x[0]))
    for i in range(0, len(k)):
        k[i][0] = arrivalinFog[i]
    k.sort(key=lambda x: float(x[0]))

    for i in range(0,len(k)):
        k[i][0] = '%.4f' %float(k[i][0])
        k[i][1] = '%.4f' % float(k[i][1])

    #print(len(k))
    # with open('cloud_dep_test.txt', 'w') as f:
    #     for i in range(0, len(k)):
    #         f.writelines(k[i][0] + '  ' + k[i][1] + '\n')

    for i in k:
        responseTime.append(float(i[1]) - float(i[0]))
    responseTime = [('%.20f' % i) for i in responseTime]

    with open('response.txt', 'a+') as f:
        for i in range(0, len(responseTime)):
            f.writelines(responseTime[i] + '\n')
    return k

def read_file(filename):        # read file and store in list as str
    with open(filename, 'r') as f:
        s = f.readlines()
    s = [i.rstrip() for i in s]
    return s

def read_file_split(filename):
    with open(filename, 'r') as f:
        s = f.readlines()
    s = [i.split() for i in s]
    return s

# if __name__ == '__main__':
#
#     paralist    = read_file('para_3.txt')
#     arrivallist = read_file('arrival_3.txt')
#     servicelist = read_file('service_3.txt')
#     networklist = read_file('network_3.txt')
#
#     mode = str(input(f'Please type the mode you want to test: (trace or random): '))
#
#     if(str(mode) == 'random'):
#
#         random_fog(arrivallist, paralist, servicelist, networklist, 2120)
#         orderlist = read_file_split('fog_dep_test.txt')
#         network_service = read_file('network_service.txt')
#         network_network = read_file('network_network.txt')
#         random_network(paralist,orderlist,network_service,network_network)
#         netdeparturelist = read_file_split('net_dep_test.txt')
#         random_cloud(paralist,netdeparturelist,network_service)
#         meanResponseTime('response.txt')
#
#     elif(str(mode) == 'trace'):
#
#         trace_fog(paralist, arrivallist, servicelist, networklist)
#         orderlist = read_file_split('fog_dep_test.txt')
#         trace_network(paralist, orderlist, servicelist, networklist)
#         netdeparturelist = read_file_split('net_dep_test.txt')
#         trace_cloud(paralist, netdeparturelist, servicelist)
#         meanResponseTime('response.txt')
#     else:
#         print('Invalid input, giving up.')








