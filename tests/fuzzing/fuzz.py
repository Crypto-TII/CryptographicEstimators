#!/usr/bin/env python3

import atheris
from data import exclude_list

with atheris.instrument_imports(exclude=exclude_list):
    from cryptographic_estimators.SDEstimator import SDEstimator
    from cryptographic_estimators.MQEstimator import MQEstimator
    from cryptographic_estimators.SDFqEstimator import SDFqEstimator
    from cryptographic_estimators.RegSDEstimator import RegSDEstimator
    from cryptographic_estimators.PKEstimator import PKEstimator
    from cryptographic_estimators.LEEstimator import LEEstimator
    from cryptographic_estimators.PEEstimator import PEEstimator
    from cryptographic_estimators.MREstimator import MREstimator
    from cryptographic_estimators.UOVEstimator import UOVEstimator
    from cryptographic_estimators.MAYOEstimator import MAYOEstimator
    from cryptographic_estimators.RankSDEstimator import RankSDEstimator
    import sys


def SDFuzz(d):
    fdp = atheris.FuzzedDataProvider(d)
    n, k, w = fdp.ConsumeIntList(3, size)
    try:
        A = SDEstimator(n, k, w)
        A.estimate()
    except Exception as e:
        print(e, type(e), n, k, w)
        if type(e) != ValueError or str(e) == "math domain error":
            raise


def MQFuzz(d):
    fdp = atheris.FuzzedDataProvider(d)
    n, m, q = fdp.ConsumeIntList(3, size)
    try:
        A = MQEstimator(n, m, q)
        A.estimate()
    except Exception as e:
        if type(e) != ValueError or str(e) == "math domain error":
            print(e, type(e), n, m, q)
            raise


def SDFqFuzz(d):
    fdp = atheris.FuzzedDataProvider(d)
    n, k, w, q = fdp.ConsumeIntList(4, size)
    try:
        A = SDFqEstimator(n, k, w, q)
        A.estimate()
    except Exception as e:
        print(e, type(e), n, k, w, q)
        if type(e) != ValueError or str(e) == "math domain error":
            raise


def RegSDFuzz(d):
    fdp = atheris.FuzzedDataProvider(d)
    n, k, w = fdp.ConsumeIntList(3, size)
    try:
        A = RegSDEstimator(n, k, w)
        A.estimate()
    except Exception as e:
        print(e, type(e), n, k, w)
        if type(e) != ValueError or str(e) == "math domain error":
            raise


def PKFuzz(d):
    fdp = atheris.FuzzedDataProvider(d)
    n, m, q, ell = fdp.ConsumeIntList(4, size)
    try:
        A = PKEstimator(n, m, q, ell)
        A.estimate()
    except Exception as e:
        print(e, type(e), n, m, q, ell)
        if type(e) != ValueError or str(e) == "math domain error":
            raise


def LEFuzz(d):
    fdp = atheris.FuzzedDataProvider(d)
    n, k, q = fdp.ConsumeIntList(3, size)
    try:
        A = LEEstimator(n, k, q)
        A.estimate()
    except Exception as e:
        print(e, type(e), n, k, q)
        if type(e) != ValueError or str(e) == "math domain error":
            raise


def PEFuzz(d):
    fdp = atheris.FuzzedDataProvider(d)
    n, k, q = fdp.ConsumeIntList(3, size)
    try:
        A = PEEstimator(n, k, q)
        A.estimate()
    except Exception as e:
        print(e, type(e), n, k, q)
        if type(e) != ValueError or str(e) == "math domain error":
            raise


def MRFuzz(d):
    fdp = atheris.FuzzedDataProvider(d)
    q, m, n, k, r = fdp.ConsumeIntList(5, size)
    try:
        A = MREstimator(q, m, n, k, r)
        A.estimate()
    except Exception as e:
        print(e, type(e), q, m, n, k, r)
        if type(e) != ValueError or str(e) == "math domain error":
            raise


def UOVFuzz(d):
    fdp = atheris.FuzzedDataProvider(d)
    n, m, q = fdp.ConsumeIntList(3, size)
    try:
        A = UOVEstimator(n, m, q)
        A.estimate()
    except Exception as e:
        print(e, type(e), n, m, q)
        if type(e) != ValueError or str(e) == "math domain error":
            raise


def MAYOFuzz(d):
    fdp = atheris.FuzzedDataProvider(d)
    n, m, o, k, q = fdp.ConsumeIntList(5, size)
    try:
        A = MAYOEstimator(n, m, o, k, q)
        A.estimate()
    except Exception as e:
        print(e, type(e), n, m, o, k, q)
        if type(e) != ValueError or str(e) == "math domain error":
            raise


def RankSDFuzz(d):
    fdp = atheris.FuzzedDataProvider(d)
    q, m, n, k, r = fdp.ConsumeIntList(5, size)
    try:
        A = RankSDEstimator(q, m, n, k, r)
        A.estimate()
    except Exception as e:
        print(e, type(e), q, m, n, k, r)
        if type(e) != ValueError or str(e) == "math domain error":
            raise


size = 1
#atheris.Setup(sys.argv, SDFuzz)
#atheris.Setup(sys.argv, MQFuzz)
#atheris.Setup(sys.argv, SDFqFuzz)
#atheris.Setup(sys.argv, RegSDFuzz)
#atheris.Setup(sys.argv, RankSDFuzz)
#atheris.Setup(sys.argv, PKFuzz)
#atheris.Setup(sys.argv, LEFuzz)
#atheris.Setup(sys.argv, PEFuzz)
#atheris.Setup(sys.argv, MRFuzz)
#atheris.Setup(sys.argv, UOVFuzz)
atheris.Setup(sys.argv, MAYOFuzz)
atheris.Fuzz()
