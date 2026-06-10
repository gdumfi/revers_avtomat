from manim import *

class TestRect(Scene):
    def construct(self):
        screenshot_path = "kernel32_map.png"
        dbg_img = ImageMobject(screenshot_path).scale_to_fit_width(5.0)
        self.add(dbg_img)
        
        # We need to find the bounding box of the kernel32.dll region.
        # Let's draw a grid to help measure
        grid = NumberPlane(x_range=[-3, 3, 0.5], y_range=[-3, 3, 0.5])
        self.add(grid)
