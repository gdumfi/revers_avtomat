from manim import *

class VirtualMemoryScheme(Scene):
    def construct(self):

        # =========================
        # Цветовая схема (инверсия)
        # =========================
        self.camera.background_color = BLACK
        LINE_COLOR = WHITE
        TEXT_COLOR = WHITE

        

        def dashed_from(block):
            start = block.get_corner(UR)
            end = start + RIGHT * 1.5
            return DashedLine(
                start,
                end,
                dash_length=0.08,
                color=LINE_COLOR
            )
        
        def dashed_from_left(block):
            start = block.get_corner(UL)
            end = start + LEFT * 1.5
            return DashedLine(
                start,
                end,
                dash_length=0.08,
                color=LINE_COLOR
            )
        
        

        def dashed_from_bottom(block):
            start = block.get_corner(DR)
            end = start + RIGHT * 1.5
            return DashedLine(
                start,
                end,
                dash_length=0.08,
                color=LINE_COLOR
            )
        # =========================
        # 1. Центральный контейнер
        # =========================
        container_height = 5.5
        container_width = 4

        left = container_width / 2
        top = container_height / 2
        bottom = -container_height / 2

        wave_amplitude = 0.12
        wave_length = 1.2

        top_wave = ParametricFunction(
            lambda t: np.array([
                t,
                top + wave_amplitude * np.sin(1.5 * PI * t / wave_length),
                0
            ]),
            t_range=[-left, left],
            color=LINE_COLOR
        )

        bottom_wave = ParametricFunction(
            lambda t: np.array([
                t,
                bottom + wave_amplitude * np.sin(1.5 * PI * t / wave_length),
                0
            ]),
            t_range=[-left, left],
            color=LINE_COLOR
        )

        left_line = Line(
            bottom_wave.get_start(),
            top_wave.get_start(),
            color=LINE_COLOR
        )

        right_line = Line(
            bottom_wave.get_end(),
            top_wave.get_end(),
            color=LINE_COLOR
        )

        outer_shape = VGroup(
            top_wave,
            bottom_wave,
            left_line,
            right_line
        )

        # =========================
        # 2. Заголовок
        # =========================
        title = Text(
            "Виртуальная память",
            font_size=32,
            color=TEXT_COLOR
        ).next_to(top_wave, UP, buff=0.3)

        # =========================
        # 3. Блок "заголовок"
        # =========================
        header_block = Rectangle(
            width=container_width,
            height=0.5,
            fill_opacity=0,
            stroke_color=LINE_COLOR,
            stroke_width=1,
        ).move_to([0, top - 1, 0])

        header_text = Text(
            "заголовок",
            font_size=20,
            color=TEXT_COLOR
        ).move_to(header_block.get_center())

        # =========================
        # 4. Три одинаковые полосы
        # =========================
        stripe_height = 1.3

        stripes = VGroup(*[
            Rectangle(
                width=container_width,
                height=stripe_height,
                fill_opacity=0,
                stroke_color=LINE_COLOR,
                stroke_width=1
            )
            for _ in range(3)
        ]).arrange(DOWN, buff=0)

        stripes.next_to(header_block, DOWN, buff=0.2)

        # =========================
        # 5. Пунктирные линии
        # =========================
        dashed_lines = VGroup(
            dashed_from(header_block),
            *[dashed_from(stripe) for stripe in stripes],
            dashed_from_bottom(stripes[-1])   # ← новая линия
        )

        # =========================
        # Добавление вертикальных двунаправленных стрелочек
        # =========================
        arrows = VGroup()
        for i in range(1, 4):
            upper_end = dashed_lines[i].get_end()
            lower_end = dashed_lines[i + 1].get_end()
            arrow = DoubleArrow(
                upper_end,
                lower_end,
                buff=0,
                color=LINE_COLOR,
                tip_length=0.2  # ← добавить это
            )
            arrows.add(arrow)

        align_labels = VGroup()
        for arrow in arrows:
            label = Text(
                "0x1000",
                font_size=18,
                color=TEXT_COLOR
            ).next_to(arrow, RIGHT, buff=0.2)
            align_labels.add(label)
        # # =========================
        # # 6. Подписи слева
        # # =========================
        # left_text = VGroup(
        #     Text("0x140001000", font_size=18, color=TEXT_COLOR),
        #     Text("Image base + base of code", font_size=16, color=TEXT_COLOR)
        # ).arrange(DOWN, aligned_edge=LEFT)

        # left_text.next_to(stripes[0], LEFT, buff=1.0)

        # vertical_line = Line(
        #     left_text.get_top() + UP * 0.3,
        #     left_text.get_bottom() + DOWN * 0.3,
        #     color=LINE_COLOR
        # )

        # crosses = VGroup(*[
        #     Text("×", font_size=14, color=TEXT_COLOR).move_to(
        #         vertical_line.point_from_proportion(p)
        #     )
        #     for p in [0.25, 0.5, 0.75]
        # ])

        # arrow_up = Arrow(
        #     vertical_line.get_top() + UP * 0.1,
        #     vertical_line.get_top() + UP * 0.4,
        #     buff=0,
        #     color=LINE_COLOR
        # )

        # arrow_down = Arrow(
        #     vertical_line.get_bottom() + DOWN * 0.1,
        #     vertical_line.get_bottom() + DOWN * 0.4,
        #     buff=0,
        #     color=LINE_COLOR
        # )

        # left_annotations = VGroup(
        #     left_text,
        #     vertical_line,
        #     crosses,
        #     arrow_up,
        #     arrow_down
        # )

        # =========================
        # 7. Подпись справа
        # =========================
        right_text = VGroup(
            Text("Image base", font_size=18, color=TEXT_COLOR),
            Text("0x140000000", font_size=18, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT)

        right_text.next_to(header_block.get_corner(UR), RIGHT, buff=1.0)

        

        # =========================
        # 8. Подпись слева
        # =========================
        left_text = VGroup(
            Text("0x140001000", font_size=16, color=TEXT_COLOR),
            Text("Image base +", font_size=16, color=TEXT_COLOR),
            Text("Base of code", font_size=16, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        left_text.next_to(stripes.get_corner(UL) - 0.2, LEFT, buff=1.0)
        left_text.shift(RIGHT)
        left_dashed_line = dashed_from_left(stripes)
        # =========================
        # 9. Финальная сборка
        # =========================
        main_container = VGroup(
            outer_shape,
            title,
            header_block,
            header_text,
            stripes,
            dashed_lines,
            arrows,
            align_labels,
            # left_annotations,
            right_text,
            left_text,
            left_dashed_line
        )

        main_container.move_to(ORIGIN)
        self.add(main_container)
        
