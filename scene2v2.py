from manim import *

class ImportDirectoryFocus(Scene):
    def construct(self):
        # ──────────────────────────────────────────────
        # 🔹 Шаг 2. Появление EXE
        # ──────────────────────────────────────────────
        exe_color = "#4A90E2"
        exe_rect = Rectangle(width=4.0, height=1.5,
                             color=exe_color, fill_color=exe_color, fill_opacity=1.0)
        exe_label = Text("main.exe", color=WHITE, font_size=36).move_to(exe_rect)
        exe_group = VGroup(exe_rect, exe_label).move_to(UP * 2.0 + UP * 2.0)
        self.play(FadeIn(exe_group), exe_group.animate.shift(DOWN * 2.0), run_time=1.2)

        # ──────────────────────────────────────────────
        # 🔹 Шаг 3. Секции .text / .data / .rdata
        # ──────────────────────────────────────────────
        self.wait(0.6)
        base_y = exe_group.get_bottom()[1] - 0.9
        gap_x = 0.6

        def make_section(name, color, desc, x_offset,y_offset):
            rect = Rectangle(width=1.8, height=0.6,
                             color=color, fill_color=color, fill_opacity=1.0)
            rect.move_to([x_offset, y_offset, 0])
            label = Text(name, color=WHITE, font_size=26).move_to(rect)
            caption = Text(desc, color=WHITE, font_size=18).next_to(rect, DOWN, buff=0.2)
            return VGroup(rect, label, caption)

        text_sec = make_section(".text", "#888888",
                                "Содержит машинные инструкции программы.",
                                x_offset=-4.2,y_offset=base_y)
        data_sec = make_section(".data", "#FF9F43",
                                "Содержит инициализированные переменные.",
                                x_offset=0,y_offset=base_y-0.9)
        rdata_sec = make_section(".rdata", "#2ECC71",
                                 "Содержит данные структуры Import Directory.",
                                 x_offset=4.2,y_offset=base_y-1.8)

        #sections = VGroup(text_sec, data_sec, rdata_sec)
        self.play(FadeIn(text_sec), run_time=0.7)
        self.play(FadeIn(data_sec), run_time=0.7)
        self.play(FadeIn(rdata_sec), run_time=0.7)

        # ──────────────────────────────────────────────
        # 🔹 Шаг 4. Фокус на .rdata
        # ──────────────────────────────────────────────
        self.play(
            rdata_sec.animate.scale(1.4).shift(LEFT * 1.0),
            run_time=1.0
        )

        # ──────────────────────────────────────────────
        # 🔹 Шаг 5. Поясняющая подпись
        # ──────────────────────────────────────────────
        self.wait(0.5)
        footer = Text(
            "ОС читает список требуемых DLL из Import Directory внутри EXE",
            color=WHITE, font_size=28
        ).move_to(DOWN * 3.0)
        self.play(Write(footer), run_time=1.0)

        # ──────────────────────────────────────────────
        # 🔹 Шаг 6. Финал — заморозка
        # ──────────────────────────────────────────────
        self.wait(2.5)
