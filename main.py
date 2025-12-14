from manim import *

class FileToMemoryScene(Scene):
    def construct(self):
        # === Заголовок ===
        title = Text("Проецирование PE-файла в виртуальную память", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # === Данные секций ===
        sections = [
            (".reloc", 0.5, GRAY),
            (".rsrc", 0.4, GREEN),
            (".data", 0.5, ORANGE),
            (".rdata", 0.6, PURPLE),
            (".text", 0.8, BLUE)
        ]

        file_label = Text("Файл на диске", font_size=28).move_to(LEFT * 3.5 + UP * 2.5)

        # === Контейнер ===
        container = Rectangle(
            width=4,
            height=4,
            color=WHITE,
            stroke_width=2,
            fill_opacity=0
        ).move_to(LEFT * 3.5)
        zeros_in_conteiner = Text("0000000000000000000",font_size=24).move_to(container.get_left()+RIGHT * 2+ UP*1.8)
        zeros_in_conteiner1 = Text("0000000000000000000", font_size=24).move_to(container.get_left() + RIGHT * 2 + DOWN * 1.8)
        zeros_in_conteiner2 = Text("0000000000000000000", font_size=24).move_to(container.get_left() + RIGHT * 2 + DOWN * 1.45)
        group_zeros  = VGroup(container,zeros_in_conteiner,zeros_in_conteiner1, zeros_in_conteiner2)
        # === Секции ===
        file_box = VGroup()

        for name, height, color in sections[::-1]:
            rect = Rectangle(width=4, height=height, color=color, fill_opacity=0.5)
            text = Text(name, font_size=24).move_to(rect.get_center())
            group = VGroup(rect, text)
            file_box.add(group)

        # === Ровное выравнивание секций ===
        file_box.arrange(DOWN, buff=0)

        # Привязка к верхней части контейнера
        file_box.move_to(container.get_top(), UP).shift(DOWN * (file_box[0].height / 2))

        self.play(Create(group_zeros ))
        self.play(FadeIn(file_label))
        self.play(LaggedStart(*[FadeIn(g) for g in file_box], lag_ratio=0.15))

        self.wait(0.5)
        # ===============================
        #    FILE ALIGNMENT GRID (LEFT)
        # ===============================

        # подпись
        # fa_label = Text("File alignment", font_size=22, color= YELLOW)
        # fa_label.next_to(container, UP, buff=0.2).move_to(LEFT * 1.4)
        # self.play(FadeIn(fa_label), run_time=0.5)

        # базовый адрес для примера
        base_addr = 0x140001000

        alignment_lines = VGroup()
        addr_texts = VGroup()
        extra = Text("File alignment", font_size=20, color=YELLOW)
        addr_texts.add(extra.move_to(UP* 2.3 + LEFT*0.7 ))
        for i, group in enumerate(file_box):
            bottom_y = group[0].get_bottom()[1]

            line = DashedLine(
                start=[container.get_left()[0] - 0.05, bottom_y, 0],
                end=[group[0].get_right()[0] + 1.5, bottom_y, 0],
                dash_length=0.15,
                color=YELLOW,
                stroke_width=1
            )
            alignment_lines.add(line)

            addr = Text(hex(base_addr + i)[2:], font_size=20, color=GREY_A)
            addr.move_to([group[0].get_right()[0] + 0.7, bottom_y + 0.1, 0])
            addr_texts.add(addr)

        # Пунктиры поверх всего
        self.bring_to_front(alignment_lines)

        self.play(
            LaggedStart(*[Create(l) for l in alignment_lines], lag_ratio=0.15),
            LaggedStart(*[FadeIn(t) for t in addr_texts], lag_ratio=0.15),
            run_time=1.2
        )

        # дополнительная подпись
        # extra = Text("image base + base of code", font_size=20, color=GREY_A)
        # extra.next_to(addr_texts[1], RIGHT, buff=0.3)
        # self.play(FadeIn(extra), run_time=0.6)
        # self.wait(2)
        self.wait(0.5)


        #
        #
        #
        #
        # === Правая колонка: "Виртуальная память" ===
        mem_label = Text("Виртуальная память", font_size=28).move_to(RIGHT * 3.5 + UP * 2.5)

        # === Контейнер для памяти ===
        mem_container = Rectangle(
            width=4,
            height=4,
            color=WHITE,
            stroke_width=2,
            fill_opacity=0
        ).move_to(RIGHT * 3.5)

        # === Нули в контейнере памяти ===
        mem_zero1 = Text("0000000000000000000", font_size=24).move_to(mem_container.get_left() + RIGHT * 2 + UP * 1.8)
        mem_zero2 = Text("0000000000000000000", font_size=24).move_to(
            mem_container.get_left() + RIGHT * 2 + DOWN * 1.45)
        mem_zero3 = Text("0000000000000000000", font_size=24).move_to(mem_container.get_left() + RIGHT * 2 + DOWN * 1.8)

        mem_zeros = VGroup(mem_container, mem_zero1, mem_zero2, mem_zero3)

        # === Секции памяти (как слева, но отдельный VGroup) ===
        mem_box = VGroup()

        for name, height, color in sections[::-1]:
            rect = Rectangle(width=4, height=height, color=color, fill_opacity=0.5)
            text = Text(name, font_size=24).move_to(rect.get_center())
            group = VGroup(rect, text)
            mem_box.add(group)

        # === Ровное выравнивание секций (как слева) ===
        mem_box.arrange(DOWN, buff=0)
        mem_box.move_to(mem_container.get_top(), UP).shift(DOWN * (mem_box[0].height / 2))

        # === Отрисовка правой колонки ===
        self.play(Create(mem_zeros))
        self.play(FadeIn(mem_label))
        self.wait(0.5)

        # === Перенос секций (как раньше) ===
        for i in range(len(sections)):
            self.play(TransformFromCopy(file_box[i], mem_box[i]), run_time=0.8)

        self.wait(0.5)

