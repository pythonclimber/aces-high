from aces_high import coin_flip


def test_coin_flip_has_two_values():
    results = {}
    for _ in range(1000):
        result = coin_flip()
        results[result] = results[result] + 1 if result in results else 1
    assert results[0] > 0
    assert results[1] > 0
    assert len(results) == 2
    assert (results[0] + results[1]) == 1000
