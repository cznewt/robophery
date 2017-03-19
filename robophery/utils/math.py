
def list_avg(list):
    sum = 0
    for elm in list:
        sum += elm
    return sum/(len(list)*1.0)


def list_min(list):
    min = list[0]
    for elm in list[1:]:
        if elm < min:
            min = elm
    return min


def list_max(list):
    max = list[0]
    for elm in list[1:]:
        if elm > max:
            max = elm
    return max
