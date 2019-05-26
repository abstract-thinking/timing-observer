import numpy as np
import pandas as pd


def calculate_relative_strength(rows):
    if len(rows) < 27:
        raise ValueError('Length should be a least 27 entries.')

    result = []
    for x in range(0, len(rows) - 27):
        #print("x=" + str(x))
        sum = 0
        for y in range(x, x + 27):
            #print("y=" + str(y))
            sum += rows[y][1]

        rsl = rows[x][1] / (sum / 27)
        rsl = round(rsl, 4)
        result.append([rows[x][0], rsl])

    return result


def old_calculate_relative_strength(closes):
    _, close_array = np.split(np.array(closes), 2, 1)
    close_series = pd.Series(close_array.flatten()[::-1], dtype=np.float)
    rsl = close_series.tail(1) / close_series.tail(27).mean()

    return float(rsl)

