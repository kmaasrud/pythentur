def prettyTime(diffInSecs):
    """Returns a human-readable string from time-difference (in seconds).
    Uses absolute value of time-diff, and thus does not care about before/after.

    Args:
        diffInSecs (int): Timedifference in seconds.
    """
    intervals = [('minute', 60), ('hour', 60), ('day', 24), ('week', 7), ('month', 4.34811904762), ('year', 12)]

    unit, number = 'second', abs(diffInSecs)
    for new_unit, ratio in intervals:
        new_number = float(number) / ratio
        if new_number < 2:
            break
        unit, number = new_unit, new_number
    shown_num = int(number)

    return '{} {}'.format(shown_num, unit + ('' if shown_num == 1 else 's'))