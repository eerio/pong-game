from __future__ import annotations
from typing import Set
import math


def euclid_dist(a: Point, b: Point):
    dy = b.y - a.y
    dx = b.x - a.x
    return math.sqrt(dy*dy + dx*dx)


class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def reflect_by_line(self, l):
        alfa = math.atan(l.slope)
        beta = math.atan2(self.y, self.x)
        print(alfa, beta)
        self.rotate(2*alfa - 2*beta)

    def rotate(self, theta: float):
        self.x = self.x * math.cos(theta) - self.y * math.sin(theta)
        self.y = self.x * math.sin(theta) + self.y * math.cos(theta)

    def issimiliar(self, v: Vector, *args, **kwargs):
        result = math.isclose(self.x, v.x, *args, **kwargs)
        result &= math.isclose(self.y, v.y, *args, **kwargs)
        return result

    def __mul__(self, z):
        return Vector(self.x * z, self.y * z)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __repr__(self):
        return '<Vector: x={} y={}>'.format(self.x, self.y)


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def to_tuple(self):
        return (self.x, self.y)

    def isclose(self, p: Point, *args, **kwargs):
        d = euclid_dist(self, p)
        return math.isclose(d, 0.0, *args, **kwargs)

    def distance_from_line(self, l: Line):
        return abs(l.a*self.x + l.b*self.y + l.c) / math.sqrt(l.a**2 + l.b**2)

    def __add__(self, v: Vector):
        return Point(self.x + v.x, self.y + v.y)

    def __repr__(self):
        return '<Point x={} y={}>'.format(self.x, self.y)


class Line:
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def get_perpendicular(self, p: Point):
        if self.a != 0 and self.b != 0:
            return Line(-self.b, self.a, p.y - self.b/self.a * p.x)
        elif self.a == 0:
            return Line(1, 0, -p.x)
        elif self.b == 0:
            return Line(0, 1, -p.y)

    def y_where(x0: float):
        if self.b == 0:
            raise Exception('Cannot get y value of a vertical line')
        return -self.a/self.b*x0 + -self.c/self.b

    def is_vertical(self):
        return self.b == 0

    def is_horizontal(self):
        return self.a == 0

    def is_parallel(self, l: Line):
        if self.is_horizontal(): return l.is_horizontal()
        if l.is_horizontal(): return self.is_horizontal()
        if self.is_vertical(): return l.is_vertical()
        if l.is_vertical(): return self.is_vertical()
        return self.a / l.a == self.b / l.b

    def eval_at(self, x=None, y=None):
        if x is not None and not self.is_vertical():
            return Point(x=x, y=(-self.c - self.a*x) / self.b)
        if y is not None and not self.is_horizontal():
            return Point(x=x, y=(-self.c - self.b*y) / self.a)
        raise Exception()

    def to_slope_intercept(self):
        return -self.a/self.b, -self.c/self.b

    @staticmethod
    def from_two_points(p1: Point, p2: Point):
        return Line(p1.y - p2.y, p2.x - p1.x, p1.x*p2.y - p2.x*p1.y)

    @staticmethod
    def from_slope_intercept(slope: float, y_intercept: float):
        return Line(-slope, 1, -y_intercept)

    def __and__(self, obj):
        if self is obj:
            return self
        if isinstance(obj, Segment):
            return (self & obj.get_direction()) in obj
        if isinstance(obj, Line):
            #  if self.b*obj.a - self.a*obj.b == 0:
            if self.is_parallel(obj):
                return set()
            elif self.is_vertical() and not obj.is_vertical():
                return obj.eval_at(x=-self.c/self.a)
            elif obj.is_vertical() and not self.is_vertical():
                return self.eval_at(x=-obj.c/obj.a)
            return self.eval_at(y=(self.a*obj.c - self.c*obj.a) / (self.b*obj.a - self.a*obj.b))

    def __contains__(self, p: Point):
        if self.is_horizontal(): return p.y == -self.c / self.b
        if self.is_vertical(): return p.x == -self.c / self.a
        return self.eval_at(x=p.x) == p.y

    def __repr__(self):
        return '<Line: a={} b={} c={}'.format(self.a, self.b, self.c)


class Line2:
    _registry = set()
    def __new__(cls, slope: float, y_intercept: float):
        for inst in cls._registry:
            if (slope, y_intercept) == (inst.slope, inst.y_intercept):
                return inst
        else:
            self = object.__new__(cls)
            self.slope = slope
            self.y_intercept = y_intercept
            self.is_horizontal = self.slope == 0
            self.is_vertical = self.slope is float('inf')
            cls._registry.add(self)
            return self

    def get_perpendicular(self, p: Point) -> Line:
        slope = -1 / self.slope
        y_intercept = p.y - slope * p.x
        return Line(slope, y_intercept)



class Segment:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b

    def __repr__(self):
        return 'Segment: from {} to {}'.format(self.a, self.b)

    def __iand__(self, l: Line):
        my_l = Line.from_two_points(self.a, self.b)
        if my_l is l:
            return self
        else:
            return intersection(my_l, l)

    def get_direction(self):
        return Line.from_two_points(self.a, self.b)

    def __contains__(self, p: Point):
        if p in self.get_direction():
            return self.a.x <= p.x <= self.b.x or self.a.x >= p.x >= self.b.x

class Rect:
    def __init__(self, init_pos: Point, width: int, height: int):
        self.pos = init_pos
        self.w = width
        self.h = height

    def sides(self):
        # FIXME: it assumes it's axes-parallel
        x, y, w, h = self.pos.x, self.pos.y, self.w // 2, self.h // 2
        a, b, c, d = (
            Point(x - w, y + h),
            Point(x + w, y + h),
            Point(x + w, y - h),
            Point(x - w, y - h)
            )
        return (Segment(a, b), Segment(b, c), Segment(c, d), Segment(d, a))

    def get_vertices(self):
        ul = Point(self.pos.x - self.w // 2, self.pos.y + self.h // 2)
        ur = Point(self.pos.x + self.w // 2, self.pos.y + self.h // 2)
        bl = Point(self.pos.x - self.w // 2, self.pos.y - self.h // 2)
        br = Point(self.pos.x + self.w // 2, self.pos.y - self.h // 2)
        return (ul, ur, bl, br)

    def get_pygame_rect(self):
        return (self.pos.x - self.w // 2, self.pos.y - self.h // 2, self.w, self.h)

    def move_to(self, p: Point):
        self.pos = p

    def __contains__(self, p: Point):
        return (
        (self.pos.x - self.w // 2 <= p.x <= self.pos.x + self.w // 2) and
        (self.pos.y - self.h // 2 <= p.y <= self.pos.y + self.h // 2)
        )


class Circle:
    def __init__(self, init_pos: Point, r: int):
        self.pos = init_pos
        self.r = r

    def __contains__(self, p: Point):
        return euclid_dist(self.pos, p) <= self.r

    def __repr__(self):
        return 'circle: pos: {}, r='.format(self.pos, self.r)

def overlap(ball_body, rect):
    pos = ball_body.pos
    if pos in rect:
        return True
    if any(intersect(side, ball_body) for side in rect.sides()):
        return True
    return False


def intersect(seg: Segment, circle: Circle):
    line = Line.from_two_points(seg.a, seg.b)
    norm = line.get_perpendicular(circle.pos)
    return bool(norm & seg)


def line_point_distance(l: Line, p: Point):
    a, b, c = -l.slope, 1, -l.y_intercept
    x0, y0 = p.x, p.y
    return abs(a*x0 + b*y0 + c) / math.sqrt(a*a + b*b)


def get_on_circle(circle: Circle, l: Line) -> Set[Point]:
    a = l.slope**2 + 1
    b = 2*l.slope*(l.y_intercept-circle.pos.y) - 2*circle.pos.x
    c = circle.pos.x**2 + (l.y_intercept - circle.pos.y)**2 - circle.r**2

    delta = b**2 - 4*a*c

    if delta < 0:
        return set()
    elif delta == 0:
        p = -b / (2*a)
        q = l.slope*p + l.y_intercept
        return {Point(p, q)}
    else:
        p0, p1 = (-b + math.sqrt(delta)) / (2 * a), (-b - math.sqrt(delta)) / (2 * a)
        q0, q1 = l.slope*p0 + l.y_intercept, l.slope*p1 + l.y_intercept
        return {Point(p0, q0), Point(p1, q1)}


def reflect_by_rect(ball, rect):
    for vert in rect.body.get_vertices():
        if vert in ball.body:
            line = Line.from_two_points(ball.body.pos, vert)
            line = line.get_perpendicular(vert)
            ball.v.reflect_by_line(line)
            return line.get_perpendicular(vert)
    else:
        ball.v = -ball.v


def reflect(vect, line):
    vx, vy = vect
    grad = line[0]

    tana = grad
    cota = 1/tana
    sin2a = 2 * tana / (1 + tana * tana)
    cos2a = (1 - sin2a * sin2a) ** 0.5

    vx2 = vx * (cos2a - sin2a * tana)
    vy2 = vy * (sin2a * cota - cos2a)
