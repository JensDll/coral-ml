import dataclasses
from typing import Any


@dataclasses.dataclass
class BBox:
    ymin: Any
    xmin: Any
    ymax: Any
    xmax: Any

    @property
    def width(self):
        return self.xmax - self.xmin

    @property
    def height(self):
        return self.ymax - self.ymin

    @property
    def area(self):
        return self.width * self.height

    @property
    def valid(self):
        return self.width >= 0 and self.height >= 0

    def scale(self, sx, sy):
        return BBox(
            xmin=sx * self.xmin,
            ymin=sy * self.ymin,
            xmax=sx * self.xmax,
            ymax=sy * self.ymax,
        )

    def translate(self, dx, dy):
        return BBox(
            xmin=dx + self.xmin,
            ymin=dy + self.ymin,
            xmax=dx + self.xmax,
            ymax=dy + self.ymax,
        )

    def map(self, f):
        return BBox(
            xmin=f(self.xmin), ymin=f(self.ymin), xmax=f(self.xmax), ymax=f(self.ymax)
        )

    @staticmethod
    def intersect(a, b):
        return BBox(
            xmin=max(a.xmin, b.xmin),
            ymin=max(a.ymin, b.ymin),
            xmax=min(a.xmax, b.xmax),
            ymax=min(a.ymax, b.ymax),
        )

    @staticmethod
    def union(a, b):
        return BBox(
            xmin=min(a.xmin, b.xmin),
            ymin=min(a.ymin, b.ymin),
            xmax=max(a.xmax, b.xmax),
            ymax=max(a.ymax, b.ymax),
        )
