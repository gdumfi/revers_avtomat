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
            end = start + RIGHT * 1
            return DashedLine(
                start,
                end,
                dash_length=0.08,
                color=LINE_COLOR
            )
        
        def dashed_from_left(block):
            start = block.get_corner(UL)
            end = start + LEFT * 1
            return DashedLine(
                start,
                end,
                dash_length=0.08,
                color=LINE_COLOR
            )
        
        

        def dashed_from_bottom(block):
            start = block.get_corner(DR)
            end = start + RIGHT * 1
            return DashedLine(
                start,
                end,
                dash_length=0.08,
                color=LINE_COLOR
            )
        

        def create_vertical_dashed_lines(start_pos, interval, count=5, length=1):
            """
            Создает вертикальные пунктирные линии одна под другой через равные промежутки

            Parameters:
            start_pos: начальная позиция (np.array или list) для первой линии
            interval: расстояние между линиями по вертикали (float)
            count: количество линий (int)
            length: длина линий по горизонтали (float)
            """
            lines = VGroup()

            for i in range(count):
                # Вычисляем позицию для текущей линии
                line_start = start_pos + np.array([0, -i * interval, 0])
                line_end = line_start + np.array([length, 0, 0])

                # Создаем пунктирную линию
                line = DashedLine(
                    start=line_start,
                    end=line_end,
                    dash_length=0.08,
                    color=LINE_COLOR
                )
                lines.add(line)

            return lines
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
            font_size=28,
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
            font_size=16,
            color=TEXT_COLOR
        ).move_to(header_block.get_center())

        # =========================
        # 4. Три блока РАЗНОЙ высоты
        # =========================
        # Разные высоты для каждого блока
        stripe_heights = [0.6, 1.0, 1.5]  # разная высота для .text, .data, .rdata
        colors_my = ["RED_A", "BLUE_A", "GREEN_A"]
        
        stripes = VGroup(*[
            Rectangle(
                width=container_width,
                height=stripe_heights[i],
                fill_opacity=0.2,
                stroke_color=LINE_COLOR,
                stroke_width=1,
                fill_color=colors_my[i]
            )
            for i in range(3)
        ])
        
        # Располагаем блоки вертикально под header_block
        stripes.arrange(DOWN, buff=0, aligned_edge=UP)
        stripes.next_to(header_block, DOWN, buff=0.2)
        
        text_labels = [
            Text(".text", font_size=14, color=YELLOW_B),
            Text(".data", font_size=14, color=YELLOW_B),
            Text(".rdata", font_size=14, color=YELLOW_B)
        ]
        
        for stripe, label in zip(stripes, text_labels):
            label.move_to(stripe.get_center())
            stripe.add(label)
        # =========================
        # 5. Пунктирные линии
        # =========================
        dashed_lines = create_vertical_dashed_lines(stripes[0].get_corner(UR) + LEFT*0.2, 0.7 , 5, 1)   # ← новая линия
        
        stripes[0].next_to(dashed_lines[0].get_start() + LEFT * 1.8, DOWN, buff=0)
        stripes[1].next_to(dashed_lines[1].get_start() + LEFT * 1.8, DOWN, buff=0)
        stripes[2].next_to(dashed_lines[3].get_start() + LEFT * 1.8, DOWN, buff=0)
        # =========================
        # Добавление вертикальных двунаправленных стрелочек
        # =========================
        arrows = VGroup()
        arrow_offset = 0.6
        for i in range(0, 4):
            upper_end = dashed_lines[i].get_end() + LEFT * arrow_offset
            lower_end = dashed_lines[i + 1].get_end() + LEFT * arrow_offset
            arrow = DoubleArrow(
                upper_end,
                lower_end,
                buff=0,
                color=LINE_COLOR,
                tip_length=0.2,  # ← добавить это
                stroke_width=2
            )
            arrows.add(arrow)

        align_labels = VGroup()
        for arrow in arrows:
            label = Text(
                "0x1000",
                font_size=16,
                color=TEXT_COLOR
            ).next_to(arrow, RIGHT*0.5, buff=0.2)
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
            Text("Image base", font_size=16, color=TEXT_COLOR),
            Text("0x140000000", font_size=16, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT)

        right_text.next_to(header_block.get_corner(UR), RIGHT*0.3, buff=1.0)
        line_header = dashed_from(header_block)

        

        # =========================
        # 8. Подпись слева
        # =========================
        left_text = VGroup(
            Text("0x140001000", font_size=14, color=TEXT_COLOR),
            Text("Image base +", font_size=14, color=TEXT_COLOR),
            Text("Base of code", font_size=14, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        left_text.next_to(stripes.get_corner(UL) - 0.15, LEFT, buff=1.0)
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
            line_header,
            left_text,
            left_dashed_line
        )

        main_container.move_to(ORIGIN)
        main_container.to_edge(RIGHT, buff=1.0)  # ← начальная позиция справа (~40% экрана)
        self.add(main_container)
    # Этап 1 - убираем ненужные элементы
        self.play(
            FadeOut(left_text),
            FadeOut(align_labels),
            FadeOut(arrows),
            FadeOut(dashed_lines),
            FadeOut(left_dashed_line),
            FadeOut(right_text),
            FadeOut(line_header),
            run_time=1
        )
        
        main_container.remove(left_text, align_labels, arrows, dashed_lines, left_dashed_line, right_text, line_header)
        self.wait(0.3)
        # Этап 2 - сдвигаем схему
        self.play(
            main_container.animate.shift(LEFT * 7.4),
            run_time=2
        )
        self.wait(0.3)
        # self.play(main_container.animate.shift(LEFT * 6), run_time=2)  # ← плавный сдвиг в левую половину; подберите дистанцию
        # self.wait(1)

        # =========================
        # Этап 3 - Фокусируем внимание на третьем блоке
        # =========================
        
        # 3.1 Мигаем границами нижнего прямоугольника два раза
        for _ in range(2):
            # Меняем цвет границ на желтый
            self.play(
                stripes[2].animate.set_stroke(color=RED_A, width=6),
                run_time=0.2
            )
            self.wait(0.2)
            # Возвращаем исходный цвет
            self.play(
                stripes[2].animate.set_stroke(color=LINE_COLOR, width=1),
                run_time=0.2
            )
            self.wait(0.2)
        
        self.wait(0.5)
        
        # 3.2 Удаляем верхние два прямоугольника и заголовочный блок
        elements_to_remove = VGroup(stripes[0], stripes[1], header_block, header_text)
        self.play(
            FadeOut(elements_to_remove),
            run_time=1.5
        )
        
        # Удаляем из main_container
        main_container.remove(stripes[0], stripes[1], header_block, header_text)
        stripes[2].remove(text_labels[2])
        
        # 3.3 Растягиваем оставшийся нижний блок на всю высоту
        # Сохраняем текущую позицию нижнего края блока
        current_bottom = stripes[2].get_bottom()
        
        # Вычисляем новую высоту (от текущего верха до верха outer_shape)
        new_top = outer_shape.get_top()[1] - 0.3  # немного отступа от верха
        new_bottom = outer_shape.get_bottom()[1] + 0.3  # немного отступа от низа
        
        # Вычисляем центр нового положения
        new_center_y = (new_top + new_bottom) / 2
        new_height = new_top - new_bottom

        # self.play(
        #     FadeOut(text_labels[2]),
        #     run_time=0.5
        # )
        # stripes[2].remove(text_labels[2])
        
        # Создаем анимацию растягивания
        self.play(
            stripes[2].animate.move_to([stripes[2].get_center()[0], new_center_y, 0])
                            .stretch_to_fit_height(new_height),
            run_time=2
        )
        
        # # 3.4 Добавляем подпись к растянутому блоку (опционально)
        # expanded_label = Text(
        #     "Расширенный блок",
        #     font_size=18,
        #     color=TEXT_COLOR
        # ).next_to(stripe_bottom, UP, buff=0.2)
        
        # self.play(
        #     Write(expanded_label),
        #     run_time=1
        # )
        
        self.wait(0.5)
        expanded_label = Text(
            ".rdata",
            font_size=16,
            color=TEXT_COLOR
        )
        expanded_label.align_to(stripes[2].get_corner(UL), LEFT)  # выравнивание по левому краю
        expanded_label.align_to(stripes[2].get_top(), UP)        # выравнивание по верхнему краю
        expanded_label.shift(DOWN*0.02, RIGHT*0.05)  # маленький вертикальный отступ, если нужен
        
        self.play(
            Write(expanded_label),
            run_time=1
        )
        self.wait(1)