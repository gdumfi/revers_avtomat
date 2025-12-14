from manim import *


class FileToMemoryScene(Scene):
    def construct(self):
        self.camera.background_color = GREY_E

        title = Text(
            "Проецирование PE-файла в виртуальную память",
            font_size=36
        )
        title.to_edge(UP)


        file_label = Text(
            "Файл на диске",
            font_size=28
        ).move_to(LEFT * 3.5 + UP * 2.5)

        container = Rectangle(
            width=2.8,
            height=4.2,
            color=WHITE,
            stroke_width=2,
            fill_opacity=0
        ).move_to(LEFT * 3.5 + DOWN * 0.5)

        zeros_in_container = VGroup(
            Text("00 00 00 00 00 00 00 00", font_size=16),
            Text("00 00 00 00 00 00 00 00", font_size=16),
            Text("00 00 00 00 00 00 00 00", font_size=16),
            Text("00 00 00 00 00 00 00 00", font_size=16),
            Text("00 00 00 00 00 00 00 00", font_size=16),
            Text("00 00 00 00 00 00 00 00", font_size=16),
            Text("00 00 00", font_size=16),
            Text("00 00 00 00", font_size=16),
            Text("00", font_size=16),
            Text("0x1000", font_size=16),
            Text("0x1400", font_size=16),
            Text("0x1600", font_size=16),
            Text("00 00 00 00 00 00 00 00", font_size=16),
            Text("00 00 00 00 00 00 00 00", font_size=16),
        )

        zeros_in_container[0].move_to(container.get_left() + RIGHT * 1.4 + UP * 1.5)  # над текстом
        zeros_in_container[1].move_to(container.get_left() + RIGHT * 1.4 + UP * 0.3)  # над датой
        zeros_in_container[2].move_to(container.get_left() + RIGHT * 1.4 + DOWN * 0.75)  # над рдатой
        zeros_in_container[3].move_to(container.get_left() + RIGHT * 1.4 + DOWN * 1.5)  # подвал
        zeros_in_container[4].move_to(container.get_left() + RIGHT * 1.4 + DOWN * 1.75)  # подвал
        zeros_in_container[5].move_to(container.get_left() + RIGHT * 1.4 + DOWN * 2.0)  # подвал
        zeros_in_container[6].move_to(container.get_right() + LEFT * 0.5 + UP * 0.57)  # нули текста
        zeros_in_container[7].move_to(container.get_right() + LEFT * 0.7 + DOWN * 0.5)  # нули даты
        zeros_in_container[8].move_to(container.get_right() + LEFT * 0.18 + DOWN * 1.3)  # нули рдаты
        zeros_in_container[9].move_to(container.get_left() + LEFT * 0.5 + UP * 1.3)  # адрес текста
        zeros_in_container[10].move_to(container.get_left() + LEFT * 0.5)  # адрес даты
        zeros_in_container[11].move_to(container.get_left() + LEFT * 0.5 + DOWN)  # адрес рдаты
        zeros_in_container[12].move_to(container.get_left() + RIGHT * 1.4 + UP * 1.75)  # над текстом
        zeros_in_container[13].move_to(container.get_left() + RIGHT * 1.4 + UP * 2)  # над текстом
        group_zeros = VGroup(container, zeros_in_container)

        # ======================================================
        # Функция полилайна по координатам
        # ======================================================
        def polyline(points, label, color):
            line = VMobject()
            line.set_points_as_corners(points)
            line.set_stroke(color=color, width=3)

            text = Text(label, font_size=24)
            text.move_to(line.get_center())

            group = VGroup(line, text)
            group.scale(0.7)

            return group

        # ======================================================
        # КООРДИНАТЫ СЕКЦИЙ
        # ======================================================

        # 1️⃣ .rdata — выше (+30%)
        rdata_points = [
            [0, 0, 0],
            [4, 0, 0],
            [4, -0.94, 0],
            [2.5, -0.94, 0],
            [2.5, -1.43, 0],
            [0, -1.43, 0],
            [0, 0, 0],
        ]

        # 2️⃣ .data — эталон
        data_points = [
            [0, 0, 0],
            [4, 0, 0],
            [4, -0.73, 0],
            [2, -0.73, 0],
            [2, -1.1, 0],
            [0, -1.1, 0],
            [0, 0, 0],
        ]

        # 3️⃣ .text — ниже (−30%)
        text_points = [
            [0, 0, 0],
            [4, 0, 0],
            [4, -0.51, 0],
            [3.5, -0.51, 0],
            [3.5, -0.77, 0],
            [0, -0.77, 0],
            [0, 0, 0],
        ]

        sec_rdata = polyline(rdata_points, ".text", ORANGE)
        sec_data = polyline(data_points, ".data", PURPLE)
        sec_text = polyline(text_points, ".rdata", GREEN)

        file_box = VGroup(sec_rdata, sec_data, sec_text)
        file_box.arrange(DOWN, buff=0.25)
        file_box.move_to(container.get_center())

        # ======================================================
        # Заголовок над полилайнами
        # ======================================================
        sections_header_box = Rectangle(
            width=2.8,
            height=0.7,
            fill_color=BLUE_D,
            fill_opacity=1,
            stroke_color=BLUE_B,
            stroke_width=2
        )

        sections_header_text = Text(
            "Заголовки",
            font_size=16,
            color=WHITE
        )

        sections_header = VGroup(
            sections_header_box,
            sections_header_text
        )

        sections_header.next_to(file_box, UP * 3.4, buff=0.2)
        sections_header_text.move_to(sections_header_box.get_center())

        # ======================================================
        # Анимация появления
        # ======================================================

        # ======================================================
        # FILE ALIGNMENT (пунктиры и адреса)
        # ======================================================

        alignment_lines = VGroup()
        addr_texts = VGroup()

        extra = Text("      File\n alignment \n    0x200", font_size=14, color=YELLOW)
        extra.move_to(UP * 0.25 + LEFT * 0.9).rotate(PI / 2)
        addr_texts.add(extra)

        for i, group in enumerate(file_box):
            bottom_y = group.get_bottom()[1]
            top_y = group.get_top()[1]

            line_top = DashedLine(
                start=[container.get_left()[0] - 0.05, top_y, 0],
                end=[group.get_right()[0] + 1.5, top_y, 0],
                dash_length=0.15,
                color=YELLOW,
                stroke_width=1
            )
            alignment_lines.add(line_top)
        # ======================================================
        # Стрелка желтая в file aligment
        # ======================================================
        arrow = DoubleArrow(
            start=[-0.5, -0.6, 0],
            end=[-0.5, 1.15, 0],
            color=YELLOW,
            stroke_width=2,
            tip_length=0.15
        )

        # ======================================================
        # ПРАВЫЙ БЛОК — КОПИЯ СЕКЦИЙ (ПРАВИЛЬНЫЙ ПОРЯДОК)
        # ======================================================

        mem_container = Rectangle(
            width=2.8,
            height=4.2,
            color=WHITE,
            stroke_width=2,
            fill_opacity=0
        ).move_to(RIGHT * 3.5 + DOWN * 0.5)

        mem_label = Text(
            "Виртуальная память",
            font_size=28
        ).move_to(RIGHT * 3.5 + UP * 2.5)

        mem_sec_rdata = sec_text.copy()
        mem_sec_data = sec_data.copy()
        mem_sec_text = sec_rdata.copy()

        # ГРУППА справа с БОЛЬШИМ расстоянием
        mem_file_box = VGroup(
            mem_sec_text,  # .text
            mem_sec_data,  # .data
            mem_sec_rdata  # .rdata
        )

        sections_header_box_right = Rectangle(
            width=2.8,
            height=0.7,
            fill_color=BLUE_D,
            fill_opacity=1,
            stroke_color=BLUE_B,
            stroke_width=2
        )

        sections_header_text_right = Text(
            "Заголовки",
            font_size=16,
            color=WHITE
        )

        # ← ВАЖНО: увеличенный buff
        mem_file_box.arrange(DOWN, buff=0.65)

        # центрируем внутри контейнера памяти
        mem_file_box.move_to(mem_container.get_center())

        sections_header_right = VGroup(
            sections_header_box_right,
            sections_header_text_right
        )

        sections_header_right.next_to(mem_file_box, UP * 1.45, buff=0.2)
        sections_header_text_right.move_to(sections_header_box_right.get_center())

        self.play(Write(title))
        # анимация появления
        self.play(Create(group_zeros))
        self.play(FadeIn(file_label))
        self.play(
            FadeIn(sections_header),
            LaggedStart(
                FadeIn(sec_rdata),
                FadeIn(sec_data),
                FadeIn(sec_text),
                lag_ratio=0.15
            )
        )

        self.wait(0.5)

        self.bring_to_front(alignment_lines)
        self.play(
            LaggedStart(*[Create(l) for l in alignment_lines], lag_ratio=0.15),
            LaggedStart(*[FadeIn(t) for t in addr_texts], lag_ratio=0.15),
            run_time=1.5
        )
        self.add(arrow)
        self.wait(1)

        self.play(Create(mem_container), FadeIn(mem_label), run_time=0.8)
        # АНИМАЦИЯ перелёта
        self.play(FadeIn(sections_header_right))
        self.play(TransformFromCopy(sec_rdata, mem_sec_text), run_time=1.5)
        self.play(TransformFromCopy(sec_data, mem_sec_data), run_time=1.5)
        self.play(TransformFromCopy(sec_text, mem_sec_rdata), run_time=1.5)
        self.add(mem_file_box)

        # ======================================================
        # SECTION ALIGNMENT (ПРАВЫЙ БЛОК — ТОЧНО КАК СЛЕВА)
        # ======================================================

        section_alignment_lines = VGroup()
        section_addr_texts = VGroup()

        section_extra = Text(
            "    Section\n alignment \n  0x1000",
            font_size=14,
            color=YELLOW
        )
        section_extra.rotate(PI / 2)
        section_extra.move_to(UP * 0.45 + RIGHT * 6.3)
        section_addr_texts.add(section_extra)

        for group in mem_file_box:
            bottom_y = group.get_bottom()[1]
            top_y = group.get_top()[1]

            line_top = DashedLine(
                start=[mem_container.get_left()[0] - 0.05, top_y, 0],
                end=[group.get_right()[0] + 1.5, top_y, 0],
                dash_length=0.15,
                color=YELLOW,
                stroke_width=1
            )

            section_alignment_lines.add(line_top)

        # ======================================================
        # Стрелка для section alignment (копия file alignment)
        # ======================================================

        section_arrow = DoubleArrow(
            start=[mem_container.get_right()[0] + 1.7, -0.6, 0],
            end=[mem_container.get_right()[0] + 1.7, 1.5, 0],
            color=YELLOW,
            stroke_width=2,
            tip_length=0.15
        )
        virt_address = VGroup(
            Text("0x1000", font_size=16),
            Text("0x2000", font_size=16),
            Text("0x3000", font_size=16),
        )

        zeros_in_right_container = VGroup(
            Text("00 00 00 00 00 00 00 00 00 00 00", font_size=10),
            Text("00 00 00 00 00 00 00 00 00 00 00", font_size=10),
            Text("00 00 00 00 00 00 00 00 00 00 00", font_size=10),
            Text("00 00 00 00 00 00 00 00 00 00 00", font_size=10),
            Text("00 00 00 00 00 00 00 00 00 00 00", font_size=10),
            Text("00 00 00 00 00 00 00 00 00 00 00", font_size=10),
            Text("00 00 00 00 00 00 00 00 00 00 00", font_size=10),
            Text("00 00 00 00 00 00 00 00 00 00 00", font_size=10),
            Text("00 00 00 00 00 00 00 00 00 00 00", font_size=10),
            Text("00 00 00 00 00 00 00 00 00 00 00", font_size=10),
            Text("00 00 00 00 00 00 00 00 00 00 00", font_size=10),
            Text("00 00 00 00 00 00 00 00 00 00 00", font_size=10),
            Text("00 00 00 00 00 00 00 00 00 00 00", font_size=10),
            Text("00 00 00 00 00 00 00 00 00 00 00", font_size=10), )

        zeros_in_right_container2 = VGroup(Text("00 00 00 00", font_size=10),
                                           Text("00 00 00 00", font_size=10),
                                           Text("00 00 00 00", font_size=10),
                                           Text("0 00 00 00 00 00", font_size=10),
                                           Text("0 00 00 00 00 00", font_size=10),
                                           Text("00", font_size=10),

                                           )
        # ----------------------------------------------------------------------------------------
        zeros_in_right_container[0].move_to(mem_container.get_right() + LEFT * 1.4 + UP * 2)
        zeros_in_right_container[1].move_to(mem_container.get_right() + LEFT * 1.4 + UP * 1.9)

        zeros_in_right_container[2].move_to(mem_container.get_right() + LEFT * 1.4 + UP * 0.68)
        zeros_in_right_container[3].move_to(mem_container.get_right() + LEFT * 1.4 + UP * 0.58)
        zeros_in_right_container[4].move_to(mem_container.get_right() + LEFT * 1.4 + UP * 0.48)
        zeros_in_right_container[5].move_to(mem_container.get_right() + LEFT * 1.4 + UP * 0.38)
        zeros_in_right_container[6].move_to(mem_container.get_right() + LEFT * 1.4 + UP * 0.28)

        zeros_in_right_container[7].move_to(mem_container.get_right() + LEFT * 1.4 + DOWN * 0.75)
        zeros_in_right_container[8].move_to(mem_container.get_right() + LEFT * 1.4 + DOWN * 0.85)
        zeros_in_right_container[9].move_to(mem_container.get_right() + LEFT * 1.4 + DOWN * 0.95)
        zeros_in_right_container[10].move_to(mem_container.get_right() + LEFT * 1.4 + DOWN * 1.05)
        zeros_in_right_container[11].move_to(mem_container.get_right() + LEFT * 1.4 + DOWN * 1.15)

        zeros_in_right_container[12].move_to(mem_container.get_right() + LEFT * 1.4 + DOWN * 1.9)
        zeros_in_right_container[13].move_to(mem_container.get_right() + LEFT * 1.4 + DOWN * 2.0)
        # ----------------------------------------------------------------------------------------
        zeros_in_right_container2[0].move_to(mem_container.get_right() + LEFT * 0.53 + UP * 1.06)
        zeros_in_right_container2[1].move_to(mem_container.get_right() + LEFT * 0.53 + UP * 0.96)
        zeros_in_right_container2[2].move_to(mem_container.get_right() + LEFT * 0.53 + UP * 0.86)

        zeros_in_right_container2[3].move_to(mem_container.get_right() + LEFT * 0.71 + DOWN * 0.45)
        zeros_in_right_container2[4].move_to(mem_container.get_right() + LEFT * 0.71 + DOWN * 0.55)
        zeros_in_right_container2[5].move_to(mem_container.get_right() + LEFT * 0.18 + DOWN * 1.73)

        group_zeros_in_right_container = VGroup(mem_container, zeros_in_right_container, zeros_in_right_container2)

        virt_address[0].move_to(mem_container.get_left() + LEFT * 0.5 + UP * 1.6)  # адрес текста
        virt_address[1].move_to(mem_container.get_left() + LEFT * 0.5)  # адрес даты
        virt_address[2].move_to(mem_container.get_left() + LEFT * 0.5 + DOWN * 1.3)  # адрес рдаты
        group_address = VGroup(mem_container, virt_address)

        self.play(Create(group_zeros_in_right_container))
        self.play(Create(group_address))
        self.bring_to_front(section_alignment_lines)
        self.play(
            LaggedStart(*[Create(l) for l in section_alignment_lines], lag_ratio=0.15),
            LaggedStart(*[FadeIn(t) for t in section_addr_texts], lag_ratio=0.15),
            run_time=1.2
        )
        self.add(section_arrow)
        self.wait(3)
