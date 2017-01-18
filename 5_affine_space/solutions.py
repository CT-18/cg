import numpy as np
from numpy import sqrt

def orientation(points, p):
    """Возвращает ориентацию точки p относительно точек points (0, 1 или -1)."""
    return np.sign(np.linalg.det(np.array(points) - p))

def do_intersect(a, b, c, d):
    """Возвращает True, если отрезки ab и cd пересекаются."""
    abc = orientation((a, b), c)
    abd = orientation((a, b), d)
    cda = orientation((c, d), a)
    cdb = orientation((c, d), b)

    if abc != abd and cda != cdb:
        return True
    elif abc == abd == cda == cdb == 0:
        # Less or equal
        def leq(a, b):
            return a[0] < b[0] or a[0] == b[0] and a[1] <= b[1]
        
        # l <= x <= r
        def between(x, l, r):
            return leq(l, x) and leq(x, r)
        
        if leq(b, a):
            a, b = b, a
        if leq(d, c):
            c, d = d, c
            
        return (between(c, a, b) or between(d, a, b) or
                between(a, c, d) or between(b, c, d))
    else:
        return False

def batman(plt, f):
    xs = np.arange(-7.25, 7.25, 0.01)
    ys = np.arange(-5, 5, 0.01)
    x, y = np.meshgrid(xs, ys)

    old_settings = np.seterr(all='ignore')

    n112 = f(4, 4) * 21 / 2
    n05 = f(1, 5) * 60
    n8 = f(4, 2)
    n33 = f(6, 3) - f(3, 1)

    eq1 = ((x/7)**2*sqrt(abs(abs(x)-3)/(abs(x)-3))+(y/3)**2*sqrt(abs(y+3/7*sqrt(n33))/(y+3/7*sqrt(n33)))-1)
    eq2 = (abs(x/2)-((3*sqrt(n33)-7)/n112)*x**2-3+sqrt(1-(abs(abs(x)-2)-1)**2)-y)
    eq3 = (9*sqrt(abs((abs(x)-1)*(abs(x)-.75))/((1-abs(x))*(abs(x)-.75)))-n8*abs(x)-y)
    eq4 = (3*abs(x)+.75*sqrt(abs((abs(x)-.75)*(abs(x)-n05))/((.75-abs(x))*(abs(x)-n05)))-y)
    eq5 = (2.25*sqrt(abs((x-n05)*(x+n05))/((n05-x)*(n05+x)))-y)
    eq6 = (6*sqrt(10)/7+(1.5-n05*abs(x))*sqrt(abs(abs(x)-1)/(abs(x)-1))-(6*sqrt(10)/14)*sqrt(4-(abs(x)-1)**2)-y)

    np.seterr(**old_settings)

    for f in [eq1,eq2,eq3,eq4,eq5,eq6]:
        plt.contour(x, y, f, [0])

    for f in [eq1,eq2,eq3,eq4,eq5,eq6]:
        plt.contour(-x, y, f, [0])

    plt.show()
