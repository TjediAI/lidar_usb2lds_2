import math
"""

serialbyte_process(inp_byte)
input (inp_byte= byte(42 byte lenth)

retern 6 values sets (angle(current angle lidar position) : distance(for current angle position))
return (result= dictionary( 1angle:distvalue1,
                            1angle+1:distvalue2,
                            1angle+2:distvalue3,
                            1angle+3:distvalue4,
                            1angle+4:distvalue5,
                            1angle+5:distvalue6)
1angle = 1~360 grad

serialbyte_process_withcut(inp_byte, )


input (inp_byte= byte(42 byte lenth), left_start_read(int), left_end_read(int), 
                right_start_read(int), right_end_read(int))

retern 6 values sets (angle(current angle lidar position) : distance(for current angle position))
return (result= dictionary( 1angle:distvalue1,
                            1angle+1:distvalue2,
                            1angle+2:distvalue3,
                            1angle+3:distvalue4,
                            1angle+4:distvalue5,
                            1angle+5:distvalue6)
1angle = 1~360 grad
"""
global badcount_sb
badcount_sb = 0


def serialbyte_process(inp_byte, mode=0, abs_mode=0):
    s = inp_byte
    angl = int((s[1] - 160) * 6)
    rads = math.pi / 180
    global badcount_sb
    # print("angl", angl)
    # rpm = (s[3]) * 256 + (s[2])
    # print("rpm", rpm)
    # print(type(init), len(init), hex(init[0]), b2)
    result = {}
    if mode == 0:
        for i in range(6, (len(s) - 2), 6):
            angl_i = int(angl + i / 6)
            res = ((s[i + 1]) * 256 + (s[i]))  # * math.sin((180 - angl_i) * math.p / 180))
            # print(i, angl_i,  res)
            if 0 < angl_i <= 360 and res > 12:
                # print(type(res))
                result[angl_i] = res
            elif res <= 0:
                result[angl_i] = 99999
            else:
                badcount_sb += 1
                # print("outrange", "Angle", 0 < angl_i <= 360, angl_i,
                #      "Distance", res > 12, res, "Total outrange errors", badcount_sb)
        # print("result", type(result), len(result), result)
        return result
    elif mode == 1:
        for i in range(6, (len(s) - 2), 6):
            angl_i = int(angl + i / 6)
            res = ((s[i + 1]) * 256 + (s[i]))   # * math.sin((180 - angl_i) * math.p / 180)
            res2 = (res * math.sin(angl_i * rads))
            # print(i, angl_i,  res, res2)
            if 0 < angl_i <= 360 and res > 12:
                if abs_mode == 1:
                    res2 = abs(res2)
                # res2 = round(res2)
                result[angl_i] = res2
            else:
                badcount_sb += 1
                print("outrange", "Angle", 0 < angl_i <= 360, angl_i,
                     "Distance", res > 12, res, "Total outrange errors", badcount_sb)
        # print("result", type(result), len(result), result)
        # print("outrange", badcount_sb)
        return result

    elif mode == 2:
        for i in range(6, (len(s) - 2), 6):
            angl_i = int(angl + i / 6)
            res = ((s[i + 1]) * 256 + (s[i]))
            res2 = (res * math.cos(angl_i * rads))
            # print("byte" + str(i), "ang=" + str(angl_i), "abs=" + str(res), "Hight(sin) ||" + str(round(res3, 2)),
            #       "Hight(cos) ==" + str(round(res2, 2)))
            if (0 < angl_i <= 360) and res > 12:
                if abs_mode == 1:
                    res2 = abs(res2)
                result[angl_i] = res2
            else:
                badcount_sb += 1
                print("outrange", 0 < angl_i <= 360, angl_i, res > 12, res, badcount_sb)
        # print("result",angl_i, rads, angl_i*rads, res*math.sin(45*rads), res*math.cos(45*rads),
        # type(result), len(result), result)
        # print("outrange","Angle", 0 < angl_i <= 360, angl_i,
        # "Distance", res > 12, res, "Total outrange errors", badcount_sb)

        return result

    elif mode == 3:
        for i in range(6, (len(s) - 2), 6):
            angl_i = int(angl + i / 6)
            res = ((s[i + 1]) * 256 + (s[i]))
            res2 = abs((res * math.cos(angl_i * rads)))
            if (225 < angl_i <= 360) or (0 < angl_i <= 45) or (135 < angl_i <= 225):
                res2 = (res * math.cos(angl_i * rads))
            elif (45 < angl_i <= 135) or (135 < angl_i <= 225):
                res2 = (res * math.sin(angl_i * rads))
                print(angl_i)
            if 0 < angl_i <= 360 and res > 12:
                if abs_mode == 1:
                    res2 = abs(res2)
                result[angl_i] = res2
            else:
                badcount_sb += 1
                print("outrange", 0 < angl_i <= 360, angl_i, res > 12, res, badcount_sb)
        print("result", type(result), len(result), result)
        # print("outrange","Angle", 0 < angl_i <= 360, angl_i,
        # "Distance", res > 12, res, "Total outrange errors", badcount_sb)
        return result
