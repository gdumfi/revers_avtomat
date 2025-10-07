from manim import *

class Example(Scene):
    def construct(self):
        c=Circle()
        cq= Square()
        c.set_fill(WHITE, opacity=1)
        c.set_stroke(BLACK, width=20)
        cq.set_color(RED)
        self.play(Create(c))
        self.remove(c)
        self.wait(3)
        self.play(Create(cq))
