#!/usr/bin/python
# -*- coding: utf-8 -*-


__author__ = 'qmax'

import sys

from ctypes import *
from ccdefines import *

libc = CDLL("/home/qmax/Documents/project/TSP/concorde_build_dynamic/temp/libconcorde.so")


def getfromsql(ncount=0, datatype="GEO", edgetype="MATRIX_LOWER_DIAG_ROW"):

    # need to verify edgetype and datatype

    rstate = CCrandstate()
    seed = libc.CCutil_real_zeit()
    libc.CCutil_sprand(seed, byref(rstate))

    dat = CCdatagroup()
    libc.CCutil_init_datagroup(byref(dat))

    if datatype == "EXPLICIT":
        norm = CC_MATRIXNORM
        for i in xrange(ncount):
            for j in xrange(ncount):#lower-triangular w\ diag
                if j < i:
                    dat.adj[i][j] = i
                elif j == i:
                    dat.adj[i][j] = i
                else:
                    pass
    elif datatype == "GEO":
        norm = CC_GEOGRAPHIC
        for i in xrange(ncount):
            dat.x[i] = i
            dat.y[i] = i
    else:
        pass

    libc.CCutil_dat_setnorm(dat, norm)

    return ncount, dat

    # geo format [id, x-coordinate, y-coordinate]



def linktour(filename, number_runs=0):
    rstate = CCrandstate()
    seed = libc.CCutil_real_zeit()
    libc.CCutil_sprand(seed, byref(rstate))

    ncount = c_int()
    dat = CCdatagroup()
    libc.CCutil_init_datagroup(byref(dat))
    datname = c_char_p(filename)
    #datname = c_char_p("/home/qmax/PycharmProjects/concorde/att48.tsp")

    """

    CCutil_gettsplib
    File:
        UTIL/getdata.c
    Header:
        util.h
    Prototype:
        int CCutil_gettsplib(char *datname, int *ncount, CCdatagroup *dat)
    Description:
        READS an xxx.tsp TSPLIB file, and returns the dat structure to
                generate edge lengths.
         -datname should be the name of a TSPLIB xxx.tsp file.
         -ncount returns the number of nodes.
         -dat returns the data.

    """
    gettsplib = libc.CCutil_gettsplib
    gettsplib.restype = c_int


    print "it is ok?"

    # 这里一定要通过byref，或者pointer初始化一个实例来进行传递，
    # ncount = (POINTER(c_int))()这个形式不行！！！
    gettsplib(datname, byref(ncount), byref(dat))
    # revise gettsplibFromMemory



    print "it is ok!"

    quadtry = c_int(2)
    tempcount = c_int()
    templist = POINTER(c_int)()
    run_silently = c_int(0)
    ff = POINTER(c_double)()
    qk_nearest = libc.CCedgegen_x_quadrant_k_nearest
    jk_nearest = libc.CCedgegen_junk_k_nearest

    val = c_double()
    allocrus = libc.CCutil_allocrus
    #incycle = POINTER(c_int)()
    incycle = cast(allocrus(c_size_t(ncount.value * 4)), POINTER(c_int))
    qboruvka = libc.CCedgegen_x_qboruvka_tour
    jqboruvka = libc.CCedgegen_junk_qboruvka_tour

    print dat.norm
    if dat.norm & CC_X_NORM_TYPE > 0:
        qk_nearest(ncount, quadtry, byref(dat), ff, 1, byref(tempcount), byref(templist), run_silently)
        qboruvka(ncount, byref(dat), incycle, byref(val), tempcount, templist, run_silently)
    elif dat.norm & CC_JUNK_NORM_TYPE > 0:
        jk_nearest(ncount, quadtry, byref(dat), ff, 1, byref(tempcount), byref(templist), run_silently)
        jqboruvka(ncount, byref(dat), incycle, byref(val), tempcount, templist, run_silently)
    else:
        print "not implement yet!"


    print 'qboruvka is ok '


    kick_type = c_int(3)
    saveit_name = c_char_p()
    length_bound = c_double(-1.0)
    time_bound = c_double(-1.0)
    in_repeater = ncount
    #outcycle = POINTER(c_int)()
    outcycle = cast(allocrus(c_size_t(ncount.value * 4)), POINTER(c_int))
    tour = libc.CClinkern_tour

    resrouter = list()

    if number_runs > 0:
        best = BIGDOUBLE
        while True:
            number_runs -= 1
            tour(ncount, byref(dat), tempcount, templist, 10000000,
                   in_repeater, incycle, outcycle, byref(val), run_silently,
                   time_bound, length_bound, saveit_name, kick_type,
                   byref(rstate))
            if val.value < best:
                best = val.value
                for i in xrange(ncount.value):
                    resrouter.append(outcycle[i])
            if number_runs <= 0:
                break
        print best
    else:
        while True:
            tour(ncount, byref(dat), tempcount, templist, 10000000,
                   in_repeater, incycle, outcycle, byref(val), run_silently,
                   time_bound, length_bound, saveit_name, kick_type,
                   byref(rstate))
            if length_bound != c_double(-1.0) and val.value > length_bound.value:
                for i in range(ncount.value):
                    resrouter.append(outcycle[i])
                break

    for i in xrange(ncount.value):
        print resrouter[i]

if __name__ == "__main__":
    linktour(sys.argv[1], 10)