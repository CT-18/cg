from hidden import turn, VType

def compute_vtype_answer(v1, v2, v3):
    if v1 > v2 and v3 > v2: # greater means below
        if turn(v1,v2,v3) > 0:
            return VType.start
        else:
            return VType.split
    elif v1 < v2 and v3 < v2:
        if turn(v1,v2,v3) > 0:
            return VType.end
        else:
            return VType.merge
    return VType.regular


def different_chains_answer(h1, h2):
    down1 = h1.origin < h1.twin.origin
    down2 = h2.origin < h2.twin.origin
    return down1 != down2