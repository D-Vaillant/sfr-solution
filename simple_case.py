""" simple_case.py:
        A Sympy verbose Python represention of the simple surface friction
        problem.
"""
# import click
import argparse
import sympy as sym
from functools import partial
from sympy import Eq, Interval, FiniteSet
from sympy import sin, sec, pi
from sympy import solveset, diff


class NoSolutionError(Exception):
    pass


case_description = """
            b
   I-------------------
   | \                |
   |X \               |
 a |   \     m        |
   |    ...           |
   |                  |
   |   x   \          |
   O------n-==========F

Euclidean plane (R x R)
O = (0, 0)
I = (0, a)
F = (b, 0)

a, b, m, n, x :: Float
X :: Radians
a, b, x :: Lengths
m, n :: Distance Travelled/Time Unit
m is within the region, n is on the bottom line segment.
    (If m > n, optimal X is <OIF.)

Parameters: a, b, m, n
Critical variables: X

Finds X to minimize time needed to go from I to F.
"""
a, b, m, n, X = sym.symbols('a b m n X')
h = a*sec(X)  # a/cos(X)
x = h*sin(X)

new_x = a * sym.tan(X)


def ins_paras(height: float, width: float,
              region_rot: float, line_rot: float) -> sym.Add:
    """ Takes the parameters, returns an Equation with those parameters. """
    travel_func = h/m + (b-new_x)/n
    return travel_func.subs([(a, height), (b, width),
                             (m, region_rot), (n, line_rot)])


def solve_simple_func(tf: sym.Add) -> sym.Union:
    """ Takes a travel function with one free parameter. """
    results = solveset(Eq(diff(tf), 0), X, domain=Interval(0, pi/2))
    return results


def process_solveset_output(output: sym.Union):
    """
    Takes a union of ImageSets, returns all solutions in Interval(0, pi/2).

    Not needed as of the latest Sympy development version, but included
    here for use with sympy==1.0.2.
    """
    funcs = FiniteSet(*[img_set.lamda(0) for img_set in output.args])
    values = Interval(0, pi/2).intersect(funcs)
    try:
        return next(iter(values))
    except StopIteration:
        print("funcs: {}".format(funcs))
        raise NoSolutionError("There are no solutions in [0, pi/2].")


def find_optimal_angle(a, b, m, n):
    # max_ang is maximum possible angle
    # otherwise you overshoot F
    max_ang = sym.atan(sym.S(b)/a)

    if m < n:
        out = solve_simple_func(ins_paras(a, b, m, n))
        sol_zero = process_solveset_output(out)

        sol = sol_zero
        # sol = min(sol_zero, max_ang)
    else:
        sol = max_ang
    return sol


# Argparse stuff
parser = argparse.ArgumentParser(description="Solves a simple case of the"
                                      "surface friction routing (sfr) problem.",
                                 prog="solve_case")
parser.add_argument('height', metavar='a', type=float,
                    help='The vertical length of the rectangle.')
parser.add_argument('width', metavar='b', type=float,
                    help='The horizontal length of the rectangle.')
parser.add_argument('region_rot', metavar='m', type=float,
                    help='The distance travelled in the region each time unit.')
parser.add_argument('line_rot', metavar='n', type=float,
                    help='The distanced travelled on the line each time unit.')


def argparse_decorator(func):
    """Originally, I wrote this program using Click but I got strange results.
       I found that feeding in the numbers directly to the function worked,
       causing me to blame click.Float and try using argparse instead.

       I decided to just replace the click decorators with a single argparse
       decorator, because I didn't want to figure out how to get setup.py to
       work otherwise."""
    args = parser.parse_args()
    a, b, m, n = (args.height, args.width,
                  args.region_rot, args.line_rot)
    return partial(func, a, b, m, n)


# The main user-interface function.
@argparse_decorator
def solve_case(height, width, region_rot, line_rot):
    """ Takes the user's input, solves for optimal angle with those parameters.
        height :: Length (vertical)
        width :: Length (horizontal)
        region_rot :: Rate-of-travel in region.
        line_rot :: Rate-of-travel on the line. """
    print("Parameters: ")
    print("    Height = {}\n    Width = {}".format(height, width))
    print("    Region ROT = {}\n    Line ROT = {}".format(region_rot,
                                                          line_rot))

    sol = find_optimal_angle(height, width, region_rot, line_rot)
    print("Optimal angle is {}.".format(sol))


if __name__ == "__main__":
    # I get some strange, strange results sometimes. I'm not sure why.
    # Use with caution!
    solve_case()
