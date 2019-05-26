from tasks.calculator import old_calculate_relative_strength, calculate_relative_strength


def test_old_calculate_relative_strength():
    closes = list()
    for x in range(28):
        closes.append(['2018-1-1', 100.0])

    rsl = old_calculate_relative_strength(closes)

    assert rsl == 1.0


def test_calculate_relative_strength():
    closes = list()
    for x in range(1, 29):
        closes.append(['2018-1-' + str(x), 100.0])
    closes.reverse()

    rsl = calculate_relative_strength(closes)

    assert rsl == [['2018-1-28', 1.0]]


def test_calculate_relative_strength_with_30_entries():
    closes = list()
    for x in range(1, 31):
        closes.append(['2018-1-' + str(x), 100.0])
    closes.reverse()

    rsl = calculate_relative_strength(closes)

    assert rsl == [['2018-1-30', 1.0], ['2018-1-29', 1.0], ['2018-1-28', 1.0]]




