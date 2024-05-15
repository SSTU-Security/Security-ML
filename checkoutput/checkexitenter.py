def check_exit(last, now, size):
    output = {}
    for i in last.keys():
        last_i = last[i]
        now_i = False
        if i in now:
            now_i = True
        if not now_i and (last_i[0] - 100) < 0:
            output[i] = True
        else:
            output[i] = False
    return output

def check_enter(last, now, size):
    output = {}
    for i in last.keys():
        last_i = last[i]
        now_i = False
        if i in now:
            now_i = True
        if not now_i and (last_i[2] + 100) > size[2]:
            output[i] = True
        else:
            output[i] = False
    return output