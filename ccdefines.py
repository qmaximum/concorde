#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'qmax'

from ctypes import *

BIGDOUBLE = 100000000.0

CC_KD_NORM_TYPE = 128
CC_X_NORM_TYPE = 256
CC_JUNK_NORM_TYPE = 512

CC_D2_NORM_SIZE = 1024
CC_D3_NORM_SIZE = 2048
CC_MATRIX_NORM_SIZE = 4096

CC_NORM_BITS = (CC_KD_NORM_TYPE | CC_X_NORM_TYPE | CC_JUNK_NORM_TYPE)
CC_NORM_SIZE_BITS = (CC_D2_NORM_SIZE | CC_D3_NORM_SIZE | CC_MATRIX_NORM_SIZE)

CC_MAXNORM = (0 | CC_KD_NORM_TYPE | CC_D2_NORM_SIZE)
CC_EUCLIDEAN_CEIL = (1 | CC_KD_NORM_TYPE | CC_D2_NORM_SIZE)
CC_EUCLIDEAN = (2 | CC_KD_NORM_TYPE | CC_D2_NORM_SIZE)
CC_EUCLIDEAN_3D = (3 | CC_X_NORM_TYPE | CC_D3_NORM_SIZE)
CC_USER = (4 | CC_JUNK_NORM_TYPE | 0)
CC_ATT = (5 | CC_X_NORM_TYPE | CC_D2_NORM_SIZE)
CC_GEOGRAPHIC = (6 | CC_X_NORM_TYPE | CC_D2_NORM_SIZE)
CC_MATRIXNORM = (7 | CC_JUNK_NORM_TYPE | CC_MATRIX_NORM_SIZE)
CC_DSJRANDNORM = (8 | CC_JUNK_NORM_TYPE | 0)
CC_CRYSTAL = (9 | CC_X_NORM_TYPE | CC_D3_NORM_SIZE)
CC_SPARSE = (10 | CC_JUNK_NORM_TYPE | 0)
CC_RHMAP1 = (11 | CC_JUNK_NORM_TYPE | 0)
CC_RHMAP2 = (12 | CC_JUNK_NORM_TYPE | 0)
CC_RHMAP3 = (13 | CC_JUNK_NORM_TYPE | 0)
CC_RHMAP4 = (14 | CC_JUNK_NORM_TYPE | 0)
CC_RHMAP5 = (15 | CC_JUNK_NORM_TYPE | 0)
CC_EUCTOROIDAL = (16 | CC_JUNK_NORM_TYPE | CC_D2_NORM_SIZE)
CC_GEOM =  (17 | CC_X_NORM_TYPE | CC_D2_NORM_SIZE)
CC_MANNORM = (18 | CC_KD_NORM_TYPE | CC_D2_NORM_SIZE)
CC_SUBDIVISION = (99 | CC_JUNK_NORM_TYPE | 0)



TenIntegers = c_int * 55

class CCrandstate(Structure):
	_fields_ = [("a", c_int),
				("b", c_int),
				("arr", TenIntegers)]


class CCdata_user(Structure):
    _fields_ = [("x", POINTER(c_double)),
    ("y", POINTER(c_double))]


class CCdata_rhvector(Structure):
    _fields_ = [("dist_00", c_int),
				("dist_01", c_int),
				("dist_02", c_int),
				("dist_12", c_int),
				("dist_22", c_int),
				("p", c_double),
				("rhlength", c_int),
				("space", c_char_p),
				("vectors", POINTER(c_char_p))	]


class CCdatagroup(Structure):
	pass

prototype = CFUNCTYPE(c_int, c_int, c_int, POINTER(CCdatagroup))


CCdatagroup._fields_ = [("edgelen", POINTER(prototype)),
						("x", POINTER(c_double)),
						("y", POINTER(c_double)),
						("z", POINTER(c_double)),
						("adj", POINTER(POINTER(c_int))),
						("adjspace", POINTER(c_int)),
						("len", POINTER(POINTER(c_int))),
						("lenspace", POINTER(c_int)),
						("degree", POINTER(c_int)),
						("norm", c_int),
						("dsjrand_param", c_int),
						("default_len", c_int),
						("sparse_ecount", c_int),
						("gridsize", c_double),
						("dsjrand_factor", c_double),
						("rhdat", CCdata_rhvector),
						("userdat", CCdata_user),
						("ndepot", c_int),
						("orig_ncount", c_int),
						("depotcost", POINTER(c_int)),
						("orig_names", POINTER(c_int))
]