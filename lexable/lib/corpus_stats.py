def lexical_density(counts: list[int], window: int):
    corpus_size = sum(counts)
    out = 0
    for count in counts:
        odds_of_exclusion = 1
        for i in range(window):
            odds_of_exclusion *= corpus_size - count - i
            odds_of_exclusion /= corpus_size - i

        out += 1 - odds_of_exclusion

    return round(out)
