import trueskill


class Rating(trueskill.Rating):
    def __init__(self, mu=None, sigma=None):
        super().__init__(mu=mu, sigma=sigma)


def rate(rating_groups, ranks=None, scores=None, weights=None, min_delta=trueskill.DELTA):
    if scores is not None:
        pass
    return trueskill.rate(rating_groups=rating_groups,
                          ranks=ranks,
                          weights=weights,
                          min_delta=min_delta)


def expose(rating):
    return trueskill.expose(rating=rating)
