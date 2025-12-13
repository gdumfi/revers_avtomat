from manim import *
import random

def random_hex_row(n=16):
    return " ".join(f"{random.randint(0,255):02X}" for _ in range(n))

class ImportTableZoom(Scene):
    def construct(self):

        # =====================================================
        #                 ЗАГОЛОВОК
        # =====================================================
        title = Text("Виртуальная память (фрагмент)", font_size=28)  # уменьшено
        title.to_edge(UP)

        # =====================================================
        #                 СЕГМЕНТЫ
        # =====================================================
        segments_info = [
            (".text", BLUE, 8),
            (".rdata", PURPLE, 10),
            (".data", ORANGE, 7),
        ]

        segment_groups = VGroup()
        x0 = 3.5

        for name, color, rows in segments_info:

            rect = Rectangle(
                width=3.4,                          # уменьшено
                height=0.26 * rows + 0.45,          # уменьшено
                color=color,
                stroke_width=2,
                fill_opacity=0.05
            )

            label = Text(name, font_size=18).next_to(rect, UP, buff=0.05)

            hex_rows = VGroup()
            for _ in range(rows):
                row = Text(random_hex_row(), font_size=15)  # уменьшено
                hex_rows.add(row)

            hex_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.03)
            hex_rows.move_to(rect.get_center())

            segment_groups.add(VGroup(rect, label, hex_rows))

        segment_groups.arrange(DOWN, buff=0.3)
        segment_groups.move_to([x0, 0, 0])

        align_text = Text("SectionAlignment = 0x1000", font_size=16, color=YELLOW)
        align_text.next_to(segment_groups, RIGHT, buff=0.25)

        # =====================================================
        #    ГЛАВНОЕ ИЗМЕНЕНИЕ: уменьшаем всё перед появлением
        # =====================================================
        full_group = VGroup(title, segment_groups, align_text)
        full_group.scale(0.55)  # ключевой коэффициент

        # Отображение
        self.play(Write(title))
        self.play(FadeIn(segment_groups), FadeIn(align_text))
        self.wait(0.4)

        # =====================================================
        #          СДВИГ В ЛЕВОЕ ПОЛЕ (учитывая масштаб)
        # =====================================================
        self.play(
            segment_groups.animate.shift(LEFT * 5 * 0.55),
            align_text.animate.shift(LEFT * 5 * 0.55),
            run_time=1.1
        )
        self.wait(0.4)

        # =====================================================
        #                 ZOOM НА .rdata
        # =====================================================

        rdata_group = segment_groups[1]
        rdata_content = rdata_group[2]

        import_rows = rdata_content[:3]
        import_box = SurroundingRectangle(
            import_rows,
            color=RED,
            buff=0.1,
            corner_radius=0.05
        )

        import_label = Text("Import Table", font_size=16, color=RED)
        import_label.next_to(import_box, UP, buff=0.05)

        other_segments = VGroup(segment_groups[0], segment_groups[2])

        self.play(
            other_segments.animate.set_opacity(0),
            align_text.animate.set_opacity(0),
            run_time=0.4
        )

        self.play(
            rdata_group.animate.scale(1.8).move_to(ORIGIN),
            run_time=1.3
        )

        self.play(Create(import_box))
        self.play(FadeIn(import_label))

        self.wait(1.2)
