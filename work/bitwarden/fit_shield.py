#!/usr/bin/env python3
"""Fit clean shield curves to the potrace trace of the user's Bitwarden icon.
Measurement only: prints the fitted control points + IoU vs the trace."""
import re, sys
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
from svgpathtools import parse_path
from shapely.geometry import Polygon, LineString

HERE = Path(__file__).resolve().parent
t = (HERE / "source-trace.svg").read_text()
parts = dict(re.findall(r'id="([^"]+)"[^>]*d="([^"]+)"', t))

def poly(d, n=3000):
    sp = parse_path(d).continuous_subpaths()[0]
    return Polygon([(z.real, z.imag) for z in (sp.point(i / n) for i in range(n))]).buffer(0)

OUT = poly(parts["trace-01-fefeff"])
INN = poly(parts["trace-02-175bd6"])

def profile(P, ys):
    pts = []
    for y in ys:
        L = LineString([(0, y), (128, y)]).intersection(P)
        if not L.is_empty:
            pts.append((L.bounds[2], y))
    return np.array(pts)

def bez(P0, P1, P2, P3, n=200):
    t = np.linspace(0, 1, n)[:, None]
    return (1-t)**3*P0 + 3*(1-t)**2*t*P1 + 3*(1-t)*t**2*P2 + t**3*P3

def fit(P, xr, xc, tip_y, y_lo, y_hi):
    pts = profile(P, np.arange(y_lo, y_hi, 0.5))
    def curve(p):
        y0, a, b, ang = p
        P0 = np.array([xr, y0]); P1 = np.array([xr, y0 + a])
        P3 = np.array([xc, tip_y]); P2 = P3 + b * np.array([np.cos(ang), -np.sin(ang)])
        return P0, P1, P2, P3
    def res(p):
        c = bez(*curve(p), n=400)
        return [np.min(np.hypot(c[:, 0]-x, c[:, 1]-y)) for x, y in pts]
    r = least_squares(res, [70, 12, 15, 0.35], bounds=([55, 0, 1, 0], [85, 40, 40, 1.2]))
    return curve(r.x), np.max(np.abs(r.fun)), np.mean(np.abs(r.fun))

o, omax, omean = fit(OUT, 97.0, 64.0, 107.5, 72, 107.2)
i, imax, imean = fit(INN, 88.3, 64.2, 97.8, 70, 97.5)
np.set_printoptions(precision=2, suppress=True)
print("outer", [list(np.round(p, 2)) for p in o], f"max {omax:.2f} mean {omean:.2f}")
print("inner", [list(np.round(p, 2)) for p in i], f"max {imax:.2f} mean {imean:.2f}")
