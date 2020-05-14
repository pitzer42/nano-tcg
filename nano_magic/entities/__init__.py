from typing import List, AnyStr


def draw(n: int, source: List[AnyStr], destination: List[AnyStr]):
    drawn = source[-n:]
    del source[-n:]
    destination += drawn


def move(i: int, source: List[AnyStr], destination: List[AnyStr]):
    moved = source.pop(i)
    destination.append(moved)

