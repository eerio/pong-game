from mathutil import *


def test_solve_quadratic():
    assert len(solve_quadratic(1, 1, 1)) == 0
    assert solve_quadratic(1, -2, 1) == {1}
    assert solve_quadratic(1, -1, -2) == {-1, 2}


def test_intersect():
    a, b = Point(0, 0), Point(1, 1)
    cir = Circle(Point(0, 0), 1)
    assert intersect(Segment(a, b), cir)

    a, b = Point(0, 0), Point(0.5, 0.5)
    assert not intersect(Segment(a, b), cir)


def test_segment():
    s = Segment(Point(500, 325), Point(500, 475))
    p = Point(500, 233)
    assert p not in s
    p = Point(500, 400)
    assert p in s

    s = Segment(Point(116, 107), Point(140, 107))
    p = Point(116, 107)
    assert p in s


def test_circle():
    seg = Segment(Point(116, 525), Point(140, 525))
    c = Circle(Point(302, 240), 25)
    inter = c & seg.get_direction()
    ok = {p for p in inter if p in seg}
    assert len(ok) == 0


if __name__ == '__main__':
    test_solve_quadratic()
    test_intersect()
    test_segment()
    test_circle()
