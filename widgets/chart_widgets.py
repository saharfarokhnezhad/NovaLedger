from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse
from kivy.properties import ListProperty


class LineChart(Widget):

    income = ListProperty([])
    expense = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(
            pos=self.update_chart,
            size=self.update_chart,
            income=self.update_chart,
            expense=self.update_chart,
        )

    def update_chart(self, *args):

        self.canvas.clear()

        if not self.income:
            self.income = [1200, 1600, 1800, 1500, 2200, 2000]

        if not self.expense:
            self.expense = [900, 1200, 1000, 1400, 1700, 1800]

        margin = 45

        w = self.width - margin * 2
        h = self.height - margin * 2

        if w <= 0 or h <= 0:
            return

        maximum = max(self.income + self.expense)

        step = w / (len(self.income) - 1)

        with self.canvas:

            Color(.92, .92, .92)

            for i in range(6):
                y = margin + i * h / 5
                Line(points=[margin, y, margin + w, y], width=1)

            Line(points=[margin, margin, margin, margin + h], width=1)
            Line(points=[margin, margin, margin + w, margin], width=1)

            Color(.10, .72, .25)

            pts = []

            for i, value in enumerate(self.income):
                x = margin + i * step
                y = margin + value / maximum * h

                pts.extend([x, y])

            Line(points=pts, width=2)

            for i, value in enumerate(self.income):
                x = margin + i * step
                y = margin + value / maximum * h

                Ellipse(pos=(x - 4, y - 4), size=(8, 8))

            Color(.93, .24, .23)

            pts = []

            for i, value in enumerate(self.expense):
                x = margin + i * step
                y = margin + value / maximum * h

                pts.extend([x, y])

            Line(points=pts, width=2)

            for i, value in enumerate(self.expense):
                x = margin + i * step
                y = margin + value / maximum * h

                Ellipse(pos=(x - 4, y - 4), size=(8, 8))


class PieChart(Widget):

    values = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(
            pos=self.update_chart,
            size=self.update_chart,
            values=self.update_chart,
        )

    def update_chart(self, *args):

        self.canvas.clear()

        if not self.values:
            self.values = [40, 25, 20, 15]

        colors = [
            (.16, .64, .95),
            (.10, .73, .25),
            (.98, .67, .17),
            (.91, .30, .35),
        ]

        total = sum(self.values)

        radius = min(self.width, self.height) * .75

        x = self.center_x - radius / 2
        y = self.center_y - radius / 2

        angle = 0

        with self.canvas:

            for value, color in zip(self.values, colors):

                Color(*color)

                sweep = value / total * 360

                Ellipse(
                    pos=(x, y),
                    size=(radius, radius),
                    angle_start=angle,
                    angle_end=angle + sweep,
                )

                angle += sweep

            Color(1, 1, 1)

            Ellipse(
                pos=(
                    self.center_x - radius * .23,
                    self.center_y - radius * .23,
                ),
                size=(
                    radius * .46,
                    radius * .46,
                ),
            )