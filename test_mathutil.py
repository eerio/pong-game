from mathutil import *


def test_line():
    a = Line(0, 0)
    b = Line(0, 0)
    c = b
    assert a is b is c
    
    a = Line(1, 0)
    perp = a.get_perpendicular(Point(0, 0))
    assert perp is Line(-1, 0)
    perp = a.get_perpendicular(Point(1, 1))
    assert perp is Line(-1, 2)


def test_circle():
    c = Circle(Point(0, 0), 1)
    p0 = Point(0, 0)
    p1 = Point(2, 0)
    p2 = Point(1, 0)
    assert p0 in c
    assert p1 not in c
    assert p2 in c


def test_vector():
    v = Vector(1, 1)
    assert v.issimiliar(v)
    assert not v.issimiliar(-v)
    assert not v.issimiliar(Vector(0.99, 1), abs_tol=1e-5)
    
    v = Vector(1, 0)
    l = Line(1, 0)
    print(v)
    v.reflect_by_line(l)
    print(v)
    assert v.issimiliar(Vector(2**(-.5), 2**(-.5)), abs_tol=1e-5)
    

def test_get_on_circle():
    c = Circle(Point(0, 0), 1)
    l = Line(slope=1, y_intercept=0)
    points = get_on_circle(c, l)
    a, b = {
        Point( 2**(-.5),  2**(-.5)),
        Point(-2**(-.5), -2**(-.5))
        }
    assert len(points) == 2
    for p in points:
        assert p.isclose(a, abs_tol=1e-5) or p.isclose(b)
    d = euclid_dist(*points)
    r = d / 2
    assert math.isclose(r, 1.0, abs_tol=1e-5)
    
    ox, oy, r = 5, 7.5, 1.5
    c = Circle(Point(ox, oy), r)
    l = Line(0, oy-r)
    points = get_on_circle(c, l)
    a = Point(ox, oy-r)
    assert len(points) == 1
    assert points.pop().isclose(a, abs_tol=1e-5)


def test_get_line_between_points():
    p0 = Point(0, 0)
    p1 = Point(1, 1)
    l = Line(1, 0)
    assert get_line_between_points(p0, p1) is Line(1, 0)


def test_overlap():
    pass


def test_dist():
    pass


def test():
    test_line()
    test_get_on_circle()
    test_get_line_between_points()
    test_overlap()
    test_dist()
    test_vector()

if __name__ == '__main__':
    test()
