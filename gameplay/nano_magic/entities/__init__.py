from typing import List, AnyStr


def draw(n: int, source: List[AnyStr], destination: List[AnyStr]):
    drawn = source[-n:]
    del source[-n:]
    destination += drawn
