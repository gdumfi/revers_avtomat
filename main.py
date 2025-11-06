from manim import *

class FileToMemoryScene(Scene):
    def construct(self):
        # === Заголовок ===
        title = Text("Проецирование PE-файла в виртуальную память", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # === Данные секций ===
        sections = [
            (".text", 2.0, BLUE),
            (".rdata", 1.5, PURPLE),
            (".data", 1, ORANGE),
            (".rsrc", 1.3, GREEN),
            (".reloc", 1, GRAY),
        ]

        # === Левая колонка: "Файл на диске" ===
        file_label = Text("Файл на диске", font_size=28).move_to(LEFT * 3.5 + UP * 2.5)
        file_box = VGroup()
        y_offset = 2
        for name, width, color in sections[::-1]:
            rect = Rectangle(width=width, height=0.4, color=color, fill_opacity=0.5)
            text = Text(name, font_size=24).move_to(rect.get_center())
            group = VGroup(rect, text).move_to(LEFT * 3.5 + DOWN * y_offset)
            y_offset -= 0.8
            file_box.add(group)
        self.play(FadeIn(file_label), LaggedStart(*[FadeIn(g) for g in file_box], lag_ratio=0.15))
        self.wait(0.5)

        # === Правая колонка: "Виртуальная память" ===
        mem_label = Text("Виртуальная память", font_size=28).move_to(RIGHT * 2.5 + UP * 2.5)
        mem_box = VGroup()
        y_offset = 2
        for name, width, color in sections[::-1]:
            rect = Rectangle(width=2.3, height=0.4, color=color, fill_opacity=0.5)
            text = Text(name, font_size=24).move_to(rect.get_center())
            group = VGroup(rect, text).move_to(RIGHT * 2.5 + DOWN * y_offset)
            y_offset -= 0.8
            mem_box.add(group)

        self.play(FadeIn(mem_label))
        self.wait(0.5)

        # === Перенос секций (слева → направо) ===
        for i in range(len(sections)):
            self.play(TransformFromCopy(file_box[i], mem_box[i]), run_time=0.8)
        self.wait(0.5)

        # === Подписи FileAlignment / SectionAlignment ===
        file_align = Text("FileAlignment = 0x200", font_size=20, color=YELLOW)
        sect_align = Text("SectionAlignment = 0x1000", font_size=20, color=YELLOW)
        file_align.next_to(file_label, DOWN, buff=0.2)
        sect_align.next_to(mem_label, DOWN, buff=0.2)
        self.play(FadeIn(file_align), FadeIn(sect_align))
        self.wait(1)

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
