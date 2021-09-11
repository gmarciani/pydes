from copy import deepcopy


def merge(a, b):
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key])
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


if __name__ == "__main__":
    d1 = dict(a="1", b=dict(c="2", d="3"))
    print(d1)
    d2 = dict(b=dict(d="5"))
    print(d2)
    d3 = merge(d1, d2)
    print(d3)
