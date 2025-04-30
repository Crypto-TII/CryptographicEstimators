#!/usr/bin/env python3

import atheris
from data import exclude_list
import argparse

# rather important, the fuzzing range will be 2**size
size = 1


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


def main():
    parser = argparse.ArgumentParser(
        description="CLI tool that allows only one of several flags to be passed."
    )

    parser.add_argument('--bytes', type=int, default=1, help='number of bytes')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--sd', action='store_true', help='Enable SD mode')
    group.add_argument('--mq', action='store_true', help='Enable MQ mode')
    group.add_argument('--sdfq', action='store_true', help='Enable SDFQ mode')
    group.add_argument('--regsd', action='store_true', help='Enable REGSD mode')
    group.add_argument('--ranksd', action='store_true', help='Enable RANKSD mode')
    group.add_argument('--pk', action='store_true', help='Enable PK mode')
    group.add_argument('--lw', action='store_true', help='Enable LW mode')
    group.add_argument('--pe', action='store_true', help='Enable PE mode')
    group.add_argument('--mr', action='store_true', help='Enable MR mode')
    group.add_argument('--uov', action='store_true', help='Enable UOV mode')
    group.add_argument('--mayo', action='store_true', help='Enable MAYO mode')

    args = parser.parse_args()
    global size
    size = args.bytes

    if args.sd:
        atheris.Setup(sys.argv, SDFuzz)
    elif args.mq:
        atheris.Setup(sys.argv, MQFuzz)
    elif args.sdfq:
        atheris.Setup(sys.argv, SDFqFuzz)
    elif args.regsd:
        atheris.Setup(sys.argv, RegSDFuzz)
    elif args.ranksd:
        atheris.Setup(sys.argv, RankSDFuzz)
    elif args.pk:
        atheris.Setup(sys.argv, PKFuzz)
    elif args.le:
        atheris.Setup(sys.argv, LEFuzz)
    elif args.pe:
        atheris.Setup(sys.argv, PEFuzz)
    elif args.mr:
        atheris.Setup(sys.argv, MRFuzz)
    elif args.uov:
        atheris.Setup(sys.argv, UOVFuzz)
    elif args.mayo:
        atheris.Setup(sys.argv, MAYOFuzz)

    atheris.Fuzz()


if __name__ == '__main__':
    main()
