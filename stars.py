"""
The MIT-Zero License

Copyright (c) 2026 Timothy Rezendes & 232 Software

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from datetime import datetime
from math import floor
from random import choice
from typing import TextIO, Union

import numpy as np

numeric = Union[int, float]


def duration_calculator(x1: numeric, multiplier: numeric = 1) -> str:
    dur: numeric
    if 0 < x1 <= 360:
        dur = 1
    elif 360 < x1 <= 720:
        dur = 2
    elif 720 < x1 <= 1080:
        dur = 3
    elif 1080 < x1 <= 1440:
        dur = 4
    elif 1440 < x1 <= 2160:
        dur = 5
    elif 2160 < x1 <= 2520:
        dur = 4
    elif 2520 < x1 <= 2880:
        dur = 3
    elif 2880 < x1 <= 3240:
        dur = 2
    elif 3240 < x1 <= 3600:
        dur = 1

    dur = dur * multiplier
    durstr: str = f"{dur}s"

    return durstr


def starMapper(xmax: numeric, ymax: numeric, n: int) -> list[tuple[int, int]]:
    xlist: list[int] = [0]
    ylist: list[int] = [0]
    i: int
    for i in range(n):
        a: int = 0
        b: int = 0
        alist: list[int] = [i for i in range(floor(xmax))]
        blist: list[int] = [i for i in range(floor(ymax))]
        a_third = floor(xmax / 3)
        alist = alist + [i for i in range(a_third, 2 * a_third)]
        while a in xlist:
            a = choice(alist)
        x1: int = a
        while b in ylist:
            b = choice(blist)
        y1: int = b
        xlist.append(x1)
        ylist.append(y1)

    del xlist[0]
    del ylist[0]

    returnList: list[tuple[int, int]] = []
    if len(xlist) == len(ylist):
        for i in range(len(xlist)):
            star_tup: tuple[int, int] = (xlist[i], ylist[i])
            returnList.append(star_tup)

    else:
        print("Welp, *something* went wrong")

    return returnList


def point_star_builder(
    star_points: list[tuple[int, int]], p2: tuple[numeric, numeric] | list[numeric]
) -> list[str]:
    star_list: list[str] = []
    p1: tuple[int, int]
    for p1 in star_points:
        x1: numeric = p1[0]
        y1: numeric = p1[1]
        x3: numeric
        y3: numeric
        x3, y3 = line_func(p1, p2)
        dur: str = duration_calculator(x1, 20)
        start_time_seq: list[float] = [
            float(r) for r in np.linspace(30, 90, 5000, endpoint=False)
        ]
        random_start: numeric = choice(start_time_seq)
        dur: str = f"{random_start}s"
        joiner: str = "\n"
        star_open = '<use href="#starModel">'
        animation = f"""<animate
  attributeName="x"
  values="{x1};{x1};{x3}"
  keyTimes="0;0.5;1"
  dur="{dur}"
  begin="0s"
  repeatCount="indefinite"
  fill="freeze"
/>
<animate
  attributeName="y"
  values="{y1};{y1};{y3}"
  keyTimes="0;0.5;1"
  dur="{dur}"
  begin="0s"
  repeatCount="indefinite"
  fill="freeze"
/>"""
        # mpath = f'  <animateMotion path="M {x1} {y1} L {x3} {y3}" dur="{dur}" begin="{random_start}s" repeatCount="indefinite" fill="freeze" />'
        star_close = "</use>"
        star: str = joiner.join([star_open, animation, star_close])
        star_list.append(star)

    return star_list


def line_func(
    p1: tuple[numeric, numeric] | list[numeric],
    p2: tuple[numeric, numeric] | list[numeric],
) -> tuple[numeric, numeric]:
    x1: numeric = p1[0]
    y1: numeric = p1[1]
    x2: numeric = p2[0]
    y2: numeric = p2[1]
    x3: numeric
    y3: numeric
    if x1 == x2:
        x3 = x1
        if y1 <= y2:
            y3 = -2338
        else:
            y3 = 4676
    else:
        m = (y1 - y2) / (x1 - x2)
        b = (x1 * y2 - x2 * y1) / (x1 - x2)
        if x1 <= x2:
            x3 = -3600
        else:
            x3 = 7200
        y3 = m * x3 + b
    return (x3, y3)


def star_builder(
    p1: tuple[numeric, numeric] | list[numeric],
    p2: tuple[numeric, numeric] | list[numeric],
) -> str:
    x1: numeric = p1[0]
    y1: numeric = p1[1]
    x3: numeric
    y3: numeric
    x3, y3 = line_func(p1, p2)

    star_open = f'<circle id="star{x1}{y1}" class="stationary" r="5">'
    start_time_seq: list[float] = [
        float(r) for r in np.linspace(0, 25, 2500, endpoint=False)
    ]
    random_start: numeric = choice(start_time_seq)
    dur: str = duration_calculator(x1)
    mpath = f'<animateMotion dur="{dur}" begin="{random_start}s" repeatCount="indefinite" path="M {x1} {y1} L {x3} {y3}" />'

    joiner: str = "\n"
    star: str = joiner.join([star_open, mpath, "</circle>"])

    return star


def trail_builder(
    p1: tuple[numeric, numeric] | list[numeric],
    p2: tuple[numeric, numeric] | list[numeric],
) -> str:
    x1: numeric = p1[0]
    y1: numeric = p1[1]
    x2: numeric = p2[0]
    x3: numeric
    y3: numeric
    x3, y3 = line_func(p1, p2)

    start_time_seq: list[float] = [
        float(r) for r in np.linspace(0, 25, 2500, endpoint=False)
    ]
    random_start: numeric = choice(start_time_seq)
    if x1 <= x2:
        gradient_class = "star-trail-gradient-left"
    else:
        gradient_class = "star-trail-gradient-right"

    dur: str = duration_calculator(x1, 2)

    star_trail: str = f"""<line
    id="trail{x1}{y1}"
    class="star-line {gradient_class}"
  >
    <animate
      attributeName="x1"
      values="{x1};{x3};{x3}"
      keyTimes="0;0.5;1"
      dur="{dur}"
      begin="{random_start}s"
      repeatCount="indefinite"
      fill="freeze"
    />
    <animate
      attributeName="y1"
      values="{y1};{y3};{y3}"
      keyTimes="0;0.5;1"
      dur="{dur}"
      begin="{random_start}s"
      repeatCount="indefinite"
      fill="freeze"
    />
    <animate
      attributeName="x2"
      values="{x1};{x3}"
      keyTimes="0;1"
      dur="{dur}"
      begin="{random_start}s"
      repeatCount="indefinite"
      fill="freeze"
    />
    <animate
      attributeName="y2"
      values="{y1};{y3}"
      keyTimes="0;1"
      dur="{dur}"
      begin="{random_start}s"
      repeatCount="indefinite"
      fill="freeze"
    />
  </line>"""

    return star_trail


def starfield_writer(xmax: numeric = 3600, ymax: numeric = 2338, n: int = 400) -> str:
    n = floor(min(n, xmax - 1, ymax - 1))
    star_points: list[tuple[int, int]] = starMapper(xmax, ymax, n)
    p2: tuple[numeric, numeric] = (xmax / 2, ymax / 2)
    points_list: list[str] = point_star_builder(star_points, p2)
    trails_list: list[str] = []
    p1: tuple[int, int]
    for p1 in star_points:
        trails_list.append(trail_builder(p1, p2))

    joiner: str = "\n"
    now_str = datetime.now().strftime("%H%M%S")
    file_name = f"starField_{now_str}.txt"

    f: TextIO
    with open(file_name, "a") as f:
        f.write(joiner.join(points_list))
        f.write(joiner.join(trails_list))

    returnString = f"Number of stars generated: {n}"
    return returnString
