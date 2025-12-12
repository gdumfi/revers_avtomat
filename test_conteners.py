from manim import *


class FileToMemoryScene(Scene):
    def construct(self):
        # ======================================================
        # Фон
        # ======================================================
        self.camera.background_color = GREY_E

        grid = NumberPlane(
            x_range=[-8, 8, 0.5],
            y_range=[-4.5, 4.5, 0.5],
            background_line_style={
                "stroke_color": GREY_C,
                "stroke_width": 1,
                "stroke_opacity": 0.4,
            }
        )

        self.add(grid)
        # ======================================================
        # Заголовок сцены
        # ======================================================
        title = Text(
            "Проецирование PE-файла в виртуальную память",
            font_size=36
        )
        title.to_edge(UP)
        self.play(Write(title))

        # ======================================================
        # Контейнер файла
        # ======================================================
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
        ).move_to(LEFT * 3.5)

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
        )

        zeros_in_container[0].move_to(container.get_left() + RIGHT * 1.4 + UP * 1.5) #над текстом
        zeros_in_container[1].move_to(container.get_left() + RIGHT * 1.4 + UP * 0.3) #над датой
        zeros_in_container[2].move_to(container.get_left() + RIGHT * 1.4 + DOWN * 0.75)# над рдатой
        zeros_in_container[3].move_to(container.get_left() + RIGHT * 1.4 + DOWN * 1.5)#подвал
        zeros_in_container[4].move_to(container.get_left() + RIGHT * 1.4 + DOWN * 1.75)#подвал
        zeros_in_container[5].move_to(container.get_left() + RIGHT * 1.4 + DOWN * 2.0)# подвал
        zeros_in_container[6].move_to(container.get_right() + LEFT * 0.5 + UP * 0.57)# нули текста
        zeros_in_container[7].move_to(container.get_right() + LEFT * 0.7 + DOWN * 0.5)# нули даты
        zeros_in_container[8].move_to(container.get_right() + LEFT * 0.18 + DOWN * 1.3)# нули рдаты
        zeros_in_container[9].move_to(container.get_left()+ LEFT * 0.5 + UP * 1.4)  # адрес текста
        zeros_in_container[10].move_to(container.get_left()+ LEFT * 0.5)  # адрес даты
        zeros_in_container[11].move_to(container.get_left()+ LEFT * 0.5 + DOWN)  # адрес рдаты

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
            [4, -0.91, 0],
            [2.5, -0.91, 0],
            [2.5, -1.43, 0],
            [0, -1.43, 0],
            [0, 0, 0],
        ]

        # 2️⃣ .data — эталон
        data_points = [
            [0, 0, 0],
            [4, 0, 0],
            [4, -0.7, 0],
            [2, -0.7, 0],
            [2, -1.1, 0],
            [0, -1.1, 0],
            [0, 0, 0],
        ]

        # 3️⃣ .text — ниже (−30%)
        text_points = [
            [0, 0, 0],
            [4, 0, 0],
            [4, -0.49, 0],
            [3.5, -0.49, 0],
            [3.5, -0.77, 0],
            [0, -0.77, 0],
            [0, 0, 0],
        ]

        sec_rdata = polyline(rdata_points, ".text", ORANGE)
        sec_data  = polyline(data_points,  ".data",  PURPLE)
        sec_text  = polyline(text_points,  ".rdata",  GREEN)

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

        sections_header.next_to(file_box, UP, buff=0.2)
        sections_header_text.move_to(sections_header_box.get_center())

        # ======================================================
        # Анимация появления
        # ======================================================
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

        # ======================================================
        # FILE ALIGNMENT (пунктиры и адреса)
        # ======================================================
        base_addr = 0x140001000

        alignment_lines = VGroup()
        addr_texts = VGroup()

        extra = Text("File alignment", font_size=20, color=YELLOW)
        extra.move_to(UP * 2.3 + LEFT * 0.7)
        addr_texts.add(extra)

        for i, group in enumerate(file_box):
            bottom_y = group.get_bottom()[1]

            line = DashedLine(
                start=[container.get_left()[0] - 0.05, bottom_y, 0],
                end=[group.get_right()[0] + 1.5, bottom_y, 0],
                dash_length=0.15,
                color=YELLOW,
                stroke_width=1
            )
            alignment_lines.add(line)

            addr = Text(
                hex(base_addr + i)[2:],
                font_size=20,
                color=GREY_A
            )
            addr.move_to([group.get_right()[0] + 0.7, bottom_y + 0.1, 0])
            addr_texts.add(addr)

        self.bring_to_front(alignment_lines)

        self.play(
            LaggedStart(*[Create(l) for l in alignment_lines], lag_ratio=0.15),
            LaggedStart(*[FadeIn(t) for t in addr_texts], lag_ratio=0.15),
            run_time=1.2
        )

        self.wait(1)
