"""
Utilities to compute error w.r.t. double tails and single tail for a given
confidence.
"""


def error_two_tails(data, mn, mx, confidence):
    """
    Computes error statistics for data w.r.t. upper and lower bounds at the
    level of confidence.
    :param data: (List(Float)) sample.
    :param mn: (Float) lower bound.
    :param mx: (Float) upper bound.
    :param confidence: (Float) confidence in [0,1].
    :return: (Dict)
    """
    samsize = len(data)

    # Theoretical Error
    err_thr = round((1 - confidence) * samsize)
    err_thr_perc = err_thr / samsize

    # Empirical Error
    err_mn = 0
    err_mx = 0
    for value in data:
        if value[1] < mn:
            err_mn += 1
        elif value[1] > mx:
            err_mx += 1
    err_emp = err_mn + err_mx
    err_mn_perc = err_mn / samsize
    err_mx_perc = err_mx / samsize
    err_emp_perc = err_emp / samsize
    err_emp_thr_perc = (err_emp - err_thr) / err_thr

    error = dict(
        err_thr=err_thr,
        err_thr_perc=err_thr_perc,
        err_mn=err_mn,
        err_mx=err_mx,
        err_emp=err_emp,
        err_mn_perc=err_mn_perc,
        err_mx_perc=err_mx_perc,
        err_emp_perc=err_emp_perc,
        err_emp_thr_perc=err_emp_thr_perc,
    )

    return error


def error_one_tail(data, mx, confidence):
    """
    Computes error statistics for data w.r.t. upper bound at the level of
    confidence.
    :param data: (List(Float)) sample.
    :param mx: (Float) upper bound.
    :param confidence: (Float) confidence in [0,1].
    :return: (Dict)
    """
    samsize = len(data)

    # Theoretical Error
    err_thr = round((1 - confidence) * samsize)
    err_thr_perc = err_thr / samsize

    # Empirical Error
    err_mx = 0
    for value in data:
        if value[1] > mx:
            err_mx += 1
    err_emp = err_mx
    err_mx_perc = err_mx / samsize
    err_emp_perc = err_emp / samsize
    err_emp_thr_perc = (err_emp - err_thr) / err_thr

    error = dict(
        err_thr=err_thr,
        err_thr_perc=err_thr_perc,
        err_mx=err_mx,
        err_emp=err_emp,
        err_mx_perc=err_mx_perc,
        err_emp_perc=err_emp_perc,
        err_emp_thr_perc=err_emp_thr_perc,
    )

    return error