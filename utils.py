def clamp(value:int, min_v: int, max_v:int):
    return min(max_v, max(min_v, value))

def sum_to(tab: list, last_index:int):
    res = 0
    for i in range(0, clamp(last_index, 0, len(tab))):
        res += tab[i]
    return res