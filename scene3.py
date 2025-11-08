from manim import *

class DllSearchScene(Scene):
    def construct(self):
        # === Заголовок ===
        title = Text("Поиск динамических библиотек (PATH search)", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # === Блок Import Directory ===
        dir_title = Text("Import Directory", font_size=28, color=YELLOW).move_to(LEFT*4 + UP*1.5)
        dll_entries = VGroup(
            Text("kernel32.dll", font_size=24),
            Text("user32.dll", font_size=24),
            Text("ws2_32.dll", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(dir_title, DOWN, buff=0.2).shift(RIGHT*0.2)
        dir_box = SurroundingRectangle(VGroup(dir_title, dll_entries), color=YELLOW, buff=0.15)
        self.play(FadeIn(dir_title), FadeIn(dll_entries), Create(dir_box))
        self.wait(0.5)

        # === "Полка" системных путей ===
        path_title = Text("Системные пути (PATH)", font_size=28, color=GREY_B).move_to(RIGHT*2.5 + UP*1.5)
        paths = VGroup(
            Text(".\\", font_size=22),
            Text("C:\\Program Files\\App\\", font_size=22),
            Text("C:\\Windows\\", font_size=22),
            Text("C:\\Windows\\System32\\", font_size=22)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(path_title, DOWN, buff=0.3)
        path_box = SurroundingRectangle(VGroup(path_title, paths), color=GREY_B, buff=0.2)
        self.play(FadeIn(path_title), FadeIn(paths), Create(path_box))
        self.wait(0.5)



        insert_slots = [0] * len(paths)   # счётчики занятости для каждой строки путей
        row_margin   = 0.25               # отступ от правой границы path_box
        dll_w, dll_h = 1.8, 0.4           # размеры прямоугольника DLL
        row_step     = 0.45               # вертикальный шаг, чтобы блоки не накладывались

        def scan_dll(entry, found_index, color):
            start = entry.get_right() + RIGHT * 0.2
            dot = Dot(start, color=color)
            self.play(FadeIn(dot))

            for i, p in enumerate(paths):
                target = p.get_left() + LEFT * 0.3
                self.play(dot.animate.move_to(target), run_time=0.6)

                if found_index is not None and i == found_index:
                    # подсветили найденный путь
                    box = SurroundingRectangle(p, color=GREEN, buff=0.05)
                    check = Text("✔", font_size=26, color=GREEN).next_to(p, RIGHT, buff=0.2)
                    self.play(Create(box), FadeIn(check))
                    self.wait(0.2)

                    # --- вставляем DLL внутрь прямоугольника "System32" ---
                    # правая граница строки (внутри рамки списка путей)
                    row_right_x = path_box.get_right()[0] - row_margin
                    # координата X центра блока при правом выравнивании
                    x = row_right_x - dll_w / 2
                    # координата Y — центр строки минус шаг * сколько уже вставлено в эту строку
                    y = p.get_bottom()[1] - row_step * insert_slots[i] - 0.45

                    dll_block = Rectangle(width=dll_w, height=dll_h, color=color, fill_opacity=0.5)
                    dll_label = Text(entry.text, font_size=18).move_to(dll_block.get_center())
                    dll_group = VGroup(dll_block, dll_label).move_to([x, y, 0])

                    # увеличиваем счётчик для этой строки (чтобы следующие уходили ниже)
                    insert_slots[i] += 1

                    self.play(TransformFromCopy(entry, dll_group), run_time=0.8)
                    self.wait(0.2)
                    break

            self.play(FadeOut(dot))





        # === Поиск kernel32.dll ===
        scan_dll(dll_entries[0], found_index=3, color=TEAL_C)  # найдено в System32
        self.wait(0.5)

        # === Поиск user32.dll ===
        scan_dll(dll_entries[1], found_index=3, color=BLUE_C)
        self.wait(0.5)

        # === Поиск ws2_32.dll (пример "не найдено") ===
        scan_dll(dll_entries[2], found_index=None, color=RED_C)
        self.wait(0.5)

        # Подпись снизу
        comment = Text("Порядок поиска: текущая папка → Program Files → Windows → System32", font_size=20, color=YELLOW).to_edge(DOWN)
        self.play(Write(comment))
        self.wait(1)

        # Завершение сцены
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.3)
