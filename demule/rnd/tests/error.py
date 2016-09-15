def error_two_tails(data, mn, mx, confidence):
    streams = len(data)

    # Theoretical Error
    err_thr = round((1 - confidence) * streams)
    err_thr_perc = err_thr / streams

    # Empirical Error
    err_mn = 0
    err_mx = 0
    for value in data:
        if value[1] < mn:
            err_mn += 1
        elif value[1] > mx:
            err_mx += 1
    err_emp = err_mn + err_mx
    err_mn_perc = err_mn / streams
    err_mx_perc = err_mx / streams
    err_emp_perc = err_emp / streams
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
    streams = len(data)

    # Theoretical Error
    err_thr = round((1 - confidence) * streams)
    err_thr_perc = err_thr / streams

    # Empirical Error
    err_mx = 0
    for value in data:
        if value[1] > mx:
            err_mx += 1
    err_emp = err_mx
    err_mx_perc = err_mx / streams
    err_emp_perc = err_emp / streams
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