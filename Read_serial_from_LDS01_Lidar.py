import serial
import time
from serial_byte_proc import serialbyte_process
import sys
import glob
import heapq
import math
from collections import deque
"""
min_selection(input_array, st_ang = 30, end_ang = 120, quant=3, sensity = 10)
return min_values[], index_minv[], no_deviation(Bool), mean(float) 
Input
min_selection(input_array, st_ang = 30, end_ang = 120, quant=3, sensity = 10)
input_array (LIST) (array, list format), start(Int) (start of range for minimal value search),
end_ang (Int) (end of range for minimal value search, quant(Int)(quantity of minimal values),
sensity (Int) (allowable deviation of selected minimum values, to eliminate peaks and noise)
excludes values with a large deviation from the mean of the variables

Function return group of minimum values, return index of this value,
do checks that they are in the same index area, returns the mean

Output(min_values, index_minv, no_deviationiation, mean)
return (List) of
min_values(List) [...quant minimal values...]
index_minv(List) [...quant index for minimal values...]
no_deviationiation(Bool) [True] then index near, [False] then index defuse
mean(Float) [mean value for minimum values]


"""


def min_selection(input_array, st_ang=29, end_ang=119, quant=3, sens=10):
    quant1 = int(2*quant)
    print (input_array)
    if quant1 >= len(input_array):
        quant1 = len(input_array)
        if quant >= len(input_array):
            quant = len(input_array)
    # print("__34__", quant, quant1, int(quant1/4))
    min_values = heapq.nsmallest(quant1, input_array[st_ang:end_ang:1])
    # print("__36__", min_values, quant1 != quant)
    for i in range(quant1-quant+1):
        # print("__38__", i,"q1-q", quant1-quant, "Len", len(min_values),"q1", quant1,"q", quant,
        # (int(len(min_values)/2)+2), (int(len(min_values)/2)+1 ))
        # print("__39__", quant1, sum(min_values[1:(int(len(min_values)/2)+2):])/(int(len(min_values)/2)+1), min_values)
        if (abs(min_values[0] - sum(min_values[1:(int(len(min_values) / 2) + 2):1]) / (
                int(len(min_values) / 2) + 1))) > sens:
            min_values = min_values[1:quant1+1:1]
            # print("__45__", quant1, min_values)
            # print("__46__2check", quant1, len(min_values), min_values[0], sum(min_values) / len(min_values))
        else:
            min_values = min_values[0:quant1:1]
            # print("__49__", min_values)
        quant1 -= 1
    index_minv = []
    for i in range(quant):
        index_minv.append(input_array.index(min_values[i]))
    # print("54", min_values)
    if (sum(index_minv)/quant - index_minv[int(quant/2)]) < 2:
        no_deviation = True
    else:
        no_deviation = False
    mean = sum(min_values)/quant
    return min_values, index_minv, no_deviation, mean


def read_serial():

    if sys.platform.startswith('win'):
        ports = 'COM3'
        # ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/ttyUSB*')  # ubuntu is /dev/ttyUSB0
    else:
        raise EnvironmentError('Unsupported platform')
    # print("72__", sys.platform.startswith('win'))
    ser = serial.Serial(str(ports), baudrate=230400, timeout=5, parity=serial.PARITY_EVEN, rtscts=1)

    badcount = 0
    readcount = 0
    readcount_ttl = 0
    arraycount = 0
    total = {}
    # logging_en = True
    start_time = time.time()
    for d in range(1, 361, 1):
        total[d] = 99999
 #   data_collector = deque([], maxlen=50)
    data_collector = []
    while True:
        # print("start", start)
        s = ser.read(42)
        # print("ch29",hex(s_prev), hex(s[1]), hex(s[1]-7), (s_prev != s[1]))
        slc = s[0:39:1]
        slc2 = s[0:40:1]
        # slc3 = s[0:41:1] #checksumm control
        # print("ch33", hex(sum(slc)), hex(sum(slc2)), hex(sum(slc3)), sum(slc3))
        # print("ch38", hex(s_prev), hex(s[1]), hex(s[1] - 6), (s_prev != s[1]))
        # s_prev = s[1]
        start_time1 = time.time()
        if s[0] != 250 or hex(sum(slc)) != hex(sum(slc2)):
            ser.close()
            ser.open()
            badcount += 1
            print("Bad data", badcount, "Errors")
        else:
            # print("Read")
            # print("main1", (time.time() - start_time), (time.time() - start_time1))
            total = total | serialbyte_process(s, 1, 1)
            # print("main2", (time.time() - start_time), (time.time() - start_time1))
            # logging(s, 100)
            # print("main3", (time.time() - start_time), (time.time() - start_time1))
            # logging(s, 120, "rlog.txt")
            # print("main4", (time.time() - start_time), (time.time() - start_time1))
            readcount += 1
            readcount_ttl += 1

        t3 = (time.time() - start_time)

        # print("Read data", readcount, "packs", "Bad data", badcount, "Errors", (readcount + badcount)/badcount)
        if readcount >= 120:
           # print("Time", t3, total)
            if arraycount >= 50:
                # print(data_collector[0])
                data_collector.pop(0)
                arraycount = 50
            data_collector.append(total)
            readcount = 0
            arraycount += 1
        n = 6
        st_ang = 50
        end_ang = 120
        if (arraycount % 5) == 0 and arraycount > 5:
            x0 = data_collector[0]
            x = data_collector[5]
            z = list(x.values())
            z0 = list(x0.values())
            h1_0 = (min_selection(z0, st_ang, end_ang, n))
            h2_0 = (min_selection(z0, 359 - end_ang, 359 - st_ang, n))
            h1 = (min_selection(z, st_ang, end_ang, n))
            h2 = (min_selection(z, 359 - end_ang, 359 - st_ang, n))
            # print(arraycount, "Minimum", min(z0[st_ang - 1:end_ang - 1:1]), h1_0[3], h1_0[2],
            #       min(z0[359 - end_ang:359 - st_ang:1]), h2_0[3], h2_0[2])

            # print(arraycount, "Minimum", min(z[st_ang-1:end_ang-1:1]), h1[3], h1[2],
            #       min(z[359-end_ang:359-st_ang:1]), h2[3], h2[2])
            print(arraycount, "Minimum", h1, h2)
            print(arraycount, "Minimum", h1_0, h2_0)
            dist_bw = h1[3] + h2[3]
            measured_lenth = h1[3] + h2[3] + 50
            angle = math.acos(dist_bw/measured_lenth) * 180 / math.pi
            print("Angle", angle, "Dist bw walls", dist_bw, h1[3]-h1_0[3], h2[3]-h2_0[3])
        if (t3 >= 60 and readcount == 0) or arraycount == 10:
            print(t3, arraycount)
            badcount_pct = badcount*100/(readcount_ttl + badcount)
            print(len(data_collector), arraycount, readcount_ttl, "Bads=", badcount, str(round(badcount_pct))+"%")
            # print(data_collector)

            return
        #    break

        # print("tot", total)

read_serial()