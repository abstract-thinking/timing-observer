import numpy as np
import pandas as pd

# RSL 27 weeks
PAST_WEEKS = 27


def calculate_relative_strength(rows):
    """
    :param rows: [x] = week, [x][0] = date Id, [x][1] = weekly quote, [x][2] = date
    :return: list of date id, RSL and date
    """
    if len(rows) < PAST_WEEKS:
        raise ValueError('Length should be a least 27.')

    result = []
    for x in range(0, len(rows) - PAST_WEEKS):
        sum = 0
        for y in range(x, x + PAST_WEEKS):
            sum += rows[y][1]

        rsl = rows[x][1] / (sum / PAST_WEEKS)
        rsl = round(rsl, 4)
        result.append([rows[x][0], rsl, rows[x][2]])

    return result


def old_calculate_relative_strength(closes):
    _, close_array = np.split(np.array(closes), 2, 1)
    close_series = pd.Series(close_array.flatten()[::-1], dtype=np.float)
    rsl = close_series.tail(1) / close_series.tail(27).mean()

    return float(rsl)

