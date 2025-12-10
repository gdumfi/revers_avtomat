from manim import *
import random

# Генерация 16-байтовой строки случайных HEX байт
def random_hex_row(n=16):
    return " ".join(f"{random.randint(0,255):02X}" for _ in range(n))

class ImportTableZoom(Scene):
    def construct(self):
        # =====================================================
        #                 ПРАВЫЙ СТОЛБЕЦ СЕГМЕНТОВ
        # =====================================================
        title = Text("Виртуальная память (фрагмент)", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        segments_info = [
            (".text", BLUE, 8),
            (".rdata", PURPLE, 10),  # центральный сегмент
            (".data", ORANGE, 7),
        ]

        segment_groups = VGroup()
        x0 = 3.5  # координата для правой стороны

        for name, color, rows in segments_info:

            rect = Rectangle(
                width=4.2,
                height=0.32 * rows + 0.6,
                color=color,
                stroke_width=2,
                fill_opacity=0.05
            )

            label = Text(name, font_size=22).next_to(rect, UP, buff=0.1)

            hex_rows = VGroup()
            for _ in range(rows):
                row = Text(random_hex_row(), font_size=18)
                hex_rows.add(row)

            hex_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.05)
            hex_rows.move_to(rect.get_center())

            group = VGroup(rect, label, hex_rows)
            segment_groups.add(group)

        segment_groups.arrange(DOWN, buff=0.4)
        segment_groups.move_to([x0, 0, 0])

        align_text = Text("SectionAlignment = 0x1000", font_size=20, color=YELLOW)
        align_text.next_to(segment_groups, RIGHT, buff=0.3)

        self.play(FadeIn(segment_groups), FadeIn(align_text))
        self.wait(0.5)

        # =====================================================
        #                 СДВИГ В ЛЕВУЮ ПОЛОВИНУ
        # =====================================================
        self.play(
            segment_groups.animate.shift(LEFT * 5),
            align_text.animate.shift(LEFT * 5),
            run_time=1.2
        )
        self.wait(0.5)

        # =====================================================
        #                 ZOOM НА ЦЕНТРАЛЬНЫЙ СЕГМЕНТ
        # =====================================================

        # Выбираем .rdata
        rdata_group = segment_groups[1]
        rdata_rect = rdata_group[0]
        rdata_content = rdata_group[2]

        # Импорт-таблица: выделим первые 3 строки
        import_rows = rdata_content[:3]
        import_box = SurroundingRectangle(
            import_rows,
            color=RED,
            buff=0.1,
            corner_radius=0.05
        )

        import_label = Text("Import Table", font_size=20, color=RED)
        import_label.next_to(import_box, UP, buff=0.1)

        # =====================================================
        #                 СКРЫВАЕМ ОСТАЛЬНЫЕ СЕГМЕНТЫ
        # =====================================================
        other_segments = VGroup(segment_groups[0], segment_groups[2])

        self.play(
            other_segments.animate.set_opacity(0),
            align_text.animate.set_opacity(0),
            run_time=0.5
        )

        # =====================================================
        #                 УВЕЛИЧИВАЕМ .rdata
        # =====================================================
        original_pos = rdata_group.get_center()

        self.play(
            rdata_group.animate.scale(1.8).move_to(ORIGIN),
            run_time=1.5
        )

        # =====================================================
        #     ПОЯВЛЕНИЕ РАМКИ И ПОДПИСИ IMPORT TABLE
        # =====================================================
        self.play(Create(import_box))
        self.play(FadeIn(import_label))

        self.wait(1.5)

        # (опционально) если вы потом будете возвращать сцену
        # self.play(
        #     rdata_group.animate.scale(1/1.8).move_to(original_pos),
        #     run_time=1.5
        # )
