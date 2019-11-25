from typing import Union

from mathutil import Point, Vector, Line


class GameObject:
    def __init__(self, body, init_v: float):
        self.body = body
        self.v = init_v
