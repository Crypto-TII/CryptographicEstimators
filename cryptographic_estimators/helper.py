from math import log2
from enum import Enum


class ComplexityType(Enum):
    """
    distinguish between normal optimisation and tilde O optimisation
    """
    ESTIMATE = 0
    TILDEO = 1


def memory_access_cost(mem, memory_access):
    if memory_access == 0:
        return 0
    elif memory_access == 1:
        return log2(mem)
    elif memory_access == 2:
        return mem / 2
    elif memory_access == 3:
        return mem / 3
    elif callable(memory_access):
        return memory_access(mem)
    return 0

def concat_all_tables(tables):
    tbl_join = concat_pretty_tables(str(tables[0]), str(tables[1]))
    for i in range(2, len(tables)):
        tbl_join = concat_pretty_tables(tbl_join, str(tables[i]))
    return tbl_join

def concat_pretty_tables(t1, t2):
    v = t1.split("\n")
    v2 = t2.split("\n")
    vnew = ""
    for i in range(len(v)):
        vnew += v[i] + v2[i][1:] + "\n"
    return vnew[:-1]


def _truncate(x, precision):
    return float(int(x * 10 ** precision) / 10 ** precision)


def round_or_truncate(x, truncate, precision):
    val = _truncate(x, precision) if truncate \
        else round(float(x), precision)
    return '{:.{p}f}'.format(val, p=precision)

