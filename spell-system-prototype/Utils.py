__author__ = 'thecomet'


def metric_scale(value, unit, decimal_places=2):
    if value > 1.0:
        for metric in ('', 'k', 'M', 'G', 'T', 'P', 'E'):
            if value <= 1000:
                break
    else:
        for metric in ('', 'm', 'u', 'n', 'p', 'f', 'a'):
            if value >= 1.0:
                break
    if value == 0.0:
        metric = ''
    return ('{0:.' + str(decimal_places) + 'f} {1}{2}').format(value, metric, unit)
