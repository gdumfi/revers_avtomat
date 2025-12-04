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

        # =========================================================
        # === ЭТАП 1 ===
        # Сдвинуть секции и SectionAlignment вниз, потом только надпись
        self.play(VGroup(mem_box, sect_align).animate.shift(DOWN * 0.6), run_time=0.8)
        self.wait(0.3)

        # Появляется текст SectionAlignment над стопкой (уже после сдвига)
        """self.play(FadeIn(sect_align))
        self.wait(0.5)"""
        base_old = Text("ImageBase = 0x140000000", font_size=20, color=GREY)
        base_old.next_to(sect_align, UP, buff=0.15).align_to(sect_align, LEFT)
        self.play(FadeIn(base_old))
        self.wait(0.3)
        # =========================================================
        # === ЭТАП 2 ===
        # Изменить ImageBase, подчеркнуть его, написать Δ над SectionAlignment,
        # потом всю стопку и SectionAlignment сдвинуть вниз
        self.play(base_old.animate.shift(UP * 0.3), run_time=0.8)
        self.wait(0.3)

        # Новый базовый адрес
        base_new = Text("ImageBase(new) = 0x141000000", font_size=20, color=GREY)
        base_new.next_to(sect_align, UP, buff=0.15).align_to(sect_align, LEFT)
        underline = Underline(base_new, buff=0.04, color=GREY)

        # показать и подчеркнуть ImageBase
        self.play(FadeIn(base_new))
        self.play(Create(underline))
        
        # вся стопка вниз
        self.play(VGroup(mem_box, sect_align).animate.shift(DOWN * 0.4), run_time=0.8)
        self.wait(0.5)
        # Δ над SectionAlignment
        delta = Text("Δ = 0x01000000", font_size=20, color=RED)
        delta.next_to(sect_align, UP, buff=0.15).align_to(sect_align, LEFT)
        # показать Δ
        self.play(FadeIn(delta))

        # =========================================================
        # === ЭТАП 3 ===
        # да Релокации
        reloc_label = Text("Релокации: исправление адресов", font_size=20, color=RED)
        reloc_label.next_to(mem_box, DOWN, buff=0.25).align_to(mem_box, LEFT)
        self.play(FadeIn(reloc_label))

        # --- Красная точка-сканер ---
        scanner = Dot(color=RED).scale(1.2)

        # да начальная позиция — немного выше верхней секции
        start_y = mem_box[4].get_right()[1] + 0.5
        start_x = mem_box[4].get_right()[0]
        scanner.move_to([start_x, start_y, 0])
        self.play(FadeIn(scanner))

        # секции, на которых оставляем след (например, .text, .rdata, .data)
        target_indices = [0, 1, 2]
        marks = []

        # проход сверху вниз
        for i in range(len(mem_box)):
            target_y = mem_box[len(mem_box)-1-i].get_right()[1]
            target_pos = [start_x, target_y, 0]
            # движение к секции
            self.play(scanner.animate.move_to(target_pos), run_time=0.6)

            # если секция в списке — оставляем точку
            if i in target_indices:
                mark = Dot(color=RED).scale(1).move_to(target_pos)
                marks.append(mark)
                self.play(FadeIn(mark), run_time=0.2)

        # точка уходит ниже последней секции
        end_y = mem_box[0].get_right()[1] - 2
        self.play(scanner.animate.move_to([start_x, end_y, 0]), run_time=0.5)
        self.play(FadeOut(scanner))
        self.wait(1)
