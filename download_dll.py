from manim import *
import numpy as np


class VirtualMemoryScheme(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        LINE_COLOR = WHITE
        TEXT_COLOR = WHITE

        # -------------------------
        # helpers
        # -------------------------
        def dashed_from_left(block):
            start = block.get_corner(UL)
            end = start + LEFT * 1
            return DashedLine(start, end, dash_length=0.08, color=LINE_COLOR)

        def dashed_from_left_bottom(block):
            start = block.get_corner(DL)
            end = start + LEFT * 1
            return DashedLine(start, end, dash_length=0.08, color=LINE_COLOR)

        def clamp(v, lo, hi):
            return max(lo, min(hi, v))

        def left_edge_point_at_y(mob, y, inset=0.06, outside=0.06):
            topy = mob.get_top()[1] - inset
            boty = mob.get_bottom()[1] + inset
            yy = clamp(y, boty, topy)
            return np.array([mob.get_left()[0] - outside, yy, 0])

        def right_edge_point_at_y(mob, y, inset=0.06, outside=0.06):
            topy = mob.get_top()[1] - inset
            boty = mob.get_bottom()[1] + inset
            yy = clamp(y, boty, topy)
            return np.array([mob.get_right()[0] + outside, yy, 0])

        def fit_inside_container(content: Mobject, container: Mobject, pad_x=0.25, pad_y=0.45):
            avail_w = (container.get_right()[0] - container.get_left()[0]) - 2 * pad_x
            avail_h = (container.get_top()[1] - container.get_bottom()[1]) - 2 * pad_y
            if content.width > avail_w:
                content.scale_to_fit_width(avail_w)
            if content.height > avail_h:
                content.scale_to_fit_height(avail_h)
            return content

        def set_tip_height(arrow_mob: Mobject, h: float):
            """
            Fixes arrow head size to an absolute height (in manim units),
            removing dependence on arrow length.
            """
            try:
                tip = arrow_mob.get_tip()
            except Exception:
                tip = getattr(arrow_mob, "tip", None)
            if tip is not None:
                tip.scale_to_fit_height(h)

        def curved_arrow(start, end, angle, color, sw=2.0, tip_h=0.16):
            a = CurvedArrow(start, end, angle=angle, color=color, stroke_width=sw)
            # Force an absolute tip height (fixes "huge heads" and mismatch)
            set_tip_height(a, tip_h)
            return a

        # =========================
        # 1) Контейнер
        # =========================
        container_height = 5.5
        container_width = 3

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
            color=LINE_COLOR,
            stroke_width=2
        )

        bottom_wave = ParametricFunction(
            lambda t: np.array([
                t,
                bottom + wave_amplitude * np.sin(1.5 * PI * t / wave_length),
                0
            ]),
            t_range=[-left, left],
            color=LINE_COLOR,
            stroke_width=2
        )

        left_line = Line(bottom_wave.get_start(), top_wave.get_start(), color=LINE_COLOR)
        right_line = Line(bottom_wave.get_end(), top_wave.get_end(), color=LINE_COLOR)

        outer_shape = VGroup(top_wave, bottom_wave, left_line, right_line)

        # Заголовок
        title = Paragraph(
            "Виртуальная память",
            "приложения",
            font_size=22,
            line_spacing=0.1,
            alignment="center"
        ).next_to(top_wave, UP, buff=0.1)

        # =========================
        # 2) Три секции (.text/.data/.rdata) -> оставляем только .rdata
        # =========================
        stripe_heights = [0.6, 1.0, 1.5]
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

        stripes.arrange(DOWN, buff=0, aligned_edge=UP)
        stripes.move_to([0, 0, 0])
        stripes.align_to(left_line, LEFT)

        text_labels = [
            Text(".text", font_size=14, color=YELLOW_B),
            Text(".data", font_size=14, color=YELLOW_B),
            Text(".rdata", font_size=14, color=YELLOW_B)
        ]
        for stripe, label in zip(stripes, text_labels):
            label.move_to(stripe.get_center())
            stripe.add(label)

        # =========================
        # 3) СРАЗУ ФИНАЛ: оставляем .rdata и растягиваем
        # =========================
        rdata = stripes[2]
        rdata.remove(text_labels[2])

        new_top = outer_shape.get_top()[1] - 0.3
        new_bottom = outer_shape.get_bottom()[1] + 0.3
        new_center_y = (new_top + new_bottom) / 2
        new_height = new_top - new_bottom

        rdata.move_to([rdata.get_center()[0], new_center_y, 0]).stretch_to_fit_height(new_height)
        rdata.align_to(left_line, LEFT)

        expanded_label = Text(".rdata", font_size=16, color=TEXT_COLOR)
        expanded_label.align_to(rdata.get_corner(UL), LEFT)
        expanded_label.align_to(rdata.get_top(), UP)
        expanded_label.shift(DOWN * 0.02 + RIGHT * 0.05)

        adress_top = Text("0x140004000", font_size=10, color=TEXT_COLOR)
        adress_bot = Text("0x140007000", font_size=10, color=TEXT_COLOR)
        adress_top.next_to(rdata.get_corner(UL), LEFT, buff=0.1).shift(UP * 0.1)
        adress_bot.next_to(rdata.get_corner(DL), LEFT, buff=0.1).shift(UP * 0.1)

        left_rdata_top_dashed = dashed_from_left(rdata)
        left_rdata_down_dashed = dashed_from_left_bottom(rdata)

        # =========================
        # 4) Import Table
        # =========================
        dir_title = Text("Import Table", font_size=16, color=YELLOW_B, weight=BOLD)

        dll_entries = VGroup(
            Text("kernel32.dll", font_size=16, color=WHITE),
            Text("user32.dll", font_size=16, color=WHITE),
            Text("libmysql.dll", font_size=16, color=WHITE),
            Text("Qt6Gui.dll", font_size=16, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        dir_group = VGroup(dir_title, dll_entries).arrange(DOWN, buff=0.2, aligned_edge=LEFT)

        target_width = rdata.width * 0.9
        import_table_rect = Rectangle(
            width=target_width,
            height=dir_group.height + 0.5,
            color=LINE_COLOR,
            stroke_width=2,
            fill_color="#1E3A8A",
            fill_opacity=0.3
        )

        dir_group.move_to(import_table_rect.get_center())
        dir_group.align_to(import_table_rect.get_left() + RIGHT * 0.2, LEFT)

        import_table_group = VGroup(import_table_rect, dir_group)
        import_table_group.next_to(expanded_label, DOWN, buff=0.3)
        import_table_group.set_x(rdata.get_center()[0])

        if import_table_group.height > rdata.height * 0.8:
            import_table_group.scale_to_fit_height(rdata.height * 0.8)
            import_table_group.set_x(rdata.get_center()[0])

        # байты
        zero_bytes = VGroup(
            Text("... 00 00 00", font_size=16, color=TEXT_COLOR),
            Text("00 00 00 00 00 00 00 00", font_size=16, color=TEXT_COLOR)
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.1)
        zero_bytes.move_to(rdata.get_bottom()).shift(UP * 0.3)

        # отметки
        marks = VGroup(
            Tex("\\checkmark", color=GREEN).scale(0.7).next_to(dll_entries[0], RIGHT * 0.8, buff=0.2),
            Tex("\\checkmark", color=GREEN).scale(0.7).next_to(dll_entries[1], RIGHT * 0.8, buff=0.2),
            Tex("\\checkmark", color=GREEN).scale(0.7).next_to(dll_entries[2], RIGHT * 0.8, buff=0.2),
            Text("×", color=RED).scale(1).next_to(dll_entries[3], RIGHT * 0.8, buff=0.2)
        )

        # =========================
        # 5) Левая финальная композиция (НЕ МЕНЯТЬ)
        # =========================
        left_final = VGroup(
            outer_shape,
            title,
            rdata,
            expanded_label,
            left_rdata_top_dashed,
            left_rdata_down_dashed,
            adress_top,
            adress_bot,
            import_table_group,
            zero_bytes,
            marks
        ).to_edge(LEFT, buff=1.1)

        # =========================
        # 6) Правый стакан
        # =========================
        right_container = outer_shape.copy().to_edge(RIGHT, buff=1.1)

        right_title = Text(
            "где-то в физ. памяти",
            font_size=20,
            color=WHITE,
            weight=BOLD
        ).next_to(right_container, UP, buff=0.1)

        mapped_title = Text("Mapped DLLs", font_size=16, color=YELLOW_B, weight=BOLD)
        mapped_list = VGroup(
            Text("ntdll.dll", font_size=14, color=WHITE),
            Text("kernel32.dll", font_size=14, color=WHITE),
            Text("user32.dll", font_size=14, color=WHITE),
            Text("gdi32.dll", font_size=14, color=WHITE),
            Text("advapi32.dll", font_size=14, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        mapped_group_text = VGroup(mapped_title, mapped_list).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        mapped_box = RoundedRectangle(
            corner_radius=0.15,
            width=container_width * 0.95,
            height=mapped_group_text.height + 0.55,
            color=LINE_COLOR,
            stroke_width=2,
            fill_opacity=0.12,
            fill_color=GRAY_E
        )
        mapped_group_text.move_to(mapped_box.get_center())
        mapped_group_text.align_to(mapped_box.get_left() + RIGHT * 0.2, LEFT)
        mapped_dlls = VGroup(mapped_box, mapped_group_text)

        # kernel32 callout
        k32_focus_box = RoundedRectangle(
            corner_radius=0.28,
            width=container_width * 0.95,
            height=1.05,
            color=LINE_COLOR,
            stroke_width=2,
            fill_opacity=0.16,
            fill_color=GREEN_E
        )
        k32_focus_outline = RoundedRectangle(
            corner_radius=0.30,
            width=k32_focus_box.width + 0.08,
            height=k32_focus_box.height + 0.08,
            color=GREEN_A,
            stroke_width=2,
            fill_opacity=0.0
        )
        k32_focus_title = Text("kernel32.dll", font_size=18, color=YELLOW_B, weight=BOLD)
        k32_r1 = Text("VA start: 0x00007FF84B340000", font_size=12, color=TEXT_COLOR)
        k32_r2 = Text("VA end:   0x00007FF84B402000", font_size=12, color=TEXT_COLOR)
        k32_note = Text("end = Base(.reloc) + Size", font_size=10, color=GRAY_A)

        k32_focus_text = VGroup(k32_focus_title, k32_r1, k32_r2, k32_note).arrange(
            DOWN, buff=0.06, aligned_edge=LEFT
        )
        k32_focus_text.move_to(k32_focus_box.get_center())
        k32_focus_text.align_to(k32_focus_box.get_left() + RIGHT * 0.18, LEFT)
        k32_focus = VGroup(k32_focus_outline, k32_focus_box, k32_focus_text)

        # Paging stacks
        n_pages = 4
        page_h = 0.42
        page_w = 1.05

        def make_stack(header_text):
            header = Text(header_text, font_size=14, color=WHITE, weight=BOLD)
            rects = VGroup(*[
                Rectangle(width=page_w, height=page_h, stroke_color=LINE_COLOR, stroke_width=1, fill_opacity=0.10)
                for _ in range(n_pages)
            ]).arrange(DOWN, buff=0.06)
            nums = VGroup(*[
                Text(str(i), font_size=12, color=TEXT_COLOR).move_to(rects[i].get_center())
                for i in range(n_pages)
            ])
            for i in range(n_pages):
                rects[i].add(nums[i])
            return VGroup(header, rects).arrange(DOWN, buff=0.12)

        va_stack = make_stack("VA pages")
        pa_stack = make_stack("PA frames")
        paging_group = VGroup(va_stack, pa_stack).arrange(RIGHT, buff=0.55)

        right_content = VGroup(mapped_dlls, k32_focus, paging_group).arrange(
            DOWN, buff=0.22, aligned_edge=LEFT
        )
        right_content.set_x(right_container.get_center()[0])
        fit_inside_container(right_content, right_container, pad_x=0.26, pad_y=0.52)
        right_content.next_to(right_title, DOWN, buff=0.34)
        right_content.shift(DOWN * 0.05)
        right_content.set_x(right_container.get_center()[0])

        # VA->PA arrows: ABSOLUTE SAME TIP SIZE
        map_idx = [2, 0, 3, 1]
        arrows_va_pa = VGroup()
        for i in range(n_pages):
            a = Arrow(
                right_edge_point_at_y(va_stack[1][i], va_stack[1][i].get_center()[1], outside=0.02),
                left_edge_point_at_y(pa_stack[1][map_idx[i]], va_stack[1][i].get_center()[1], outside=0.02),
                buff=0.04,
                stroke_width=2.2,
            )
            # Force equal tip height for each VA->PA arrow
            set_tip_height(a, 0.12)
            arrows_va_pa.add(a)

        # =========================
        # 7) Связь между стаканами: tips ABSOLUTE SAME SIZE (small)
        # =========================
        lib_colors = [BLUE_B, GREEN_B, ORANGE, RED_B]
        lib_angles = [0.18, 0.06, -0.06, -0.18]

        starts = []
        for i in range(4):
            yy = dll_entries[i].get_center()[1]
            starts.append(right_edge_point_at_y(import_table_rect, yy, outside=0.05))

        targets = []
        for i in range(4):
            if i == 0:
                yy = mapped_list[1].get_center()[1]  # kernel32
            elif i == 1:
                yy = mapped_list[2].get_center()[1]  # user32
            else:
                yy = mapped_dlls.get_top()[1] - 0.55 - (i * 0.22)
            targets.append(left_edge_point_at_y(mapped_dlls, yy, outside=0.03))

        trigger_to_mapped = VGroup()
        for i in range(4):
            trigger_to_mapped.add(
                curved_arrow(
                    starts[i],
                    targets[i],
                    angle=lib_angles[i],
                    color=lib_colors[i],
                    sw=2.0,
                    tip_h=0.14  # FIXED SMALL TIP (no more huge heads)
                )
            )

        k32_import_to_focus = curved_arrow(
            right_edge_point_at_y(import_table_rect, dll_entries[0].get_center()[1], outside=0.05),
            left_edge_point_at_y(k32_focus, dll_entries[0].get_center()[1], outside=0.03),
            angle=0.10,
            color=BLUE_B,
            sw=2.0,
            tip_h=0.12
        )

        trigger_caption = Text(
            "Импорт → загрузчик ОС мапит DLL\nв адресное пространство процесса",
            font_size=11,
            color=GRAY_A
        )
        gap_center_x = (left_final.get_right()[0] + right_container.get_left()[0]) / 2
        trigger_caption.move_to(np.array([gap_center_x, mapped_dlls.get_top()[1] - 0.12, 0]))

        # =========================
        # 8) Скрин: плавно в центре, 3 секунды, плавно исчезает
        # =========================
        screenshot_path = "kernel32_map.png"
        dbg_img = ImageMobject(screenshot_path)
        dbg_img.scale_to_fit_width(9.0)

        dbg_frame = RoundedRectangle(
            corner_radius=0.15,
            width=dbg_img.width + 0.18,
            height=dbg_img.height + 0.18,
            color=LINE_COLOR,
            stroke_width=2,
            fill_opacity=0.06
        )
        dbg_img.move_to(dbg_frame.get_center())
        dbg_block = Group(dbg_frame, dbg_img).move_to(ORIGIN)

        # =========================
        # 9) Показ (замедлено)
        # =========================
        self.add(left_final, right_container)

        self.play(FadeIn(right_title, shift=UP * 0.08), run_time=1.2)
        self.wait(0.5)

        self.play(FadeIn(mapped_dlls, shift=UP * 0.06), run_time=1.6)
        self.wait(0.7)

        self.play(Create(trigger_to_mapped), FadeIn(trigger_caption), run_time=2.2)
        self.wait(0.9)

        highlight = SurroundingRectangle(mapped_list[1], color=YELLOW_B, buff=0.08, corner_radius=0.10)
        self.play(Create(highlight), run_time=1.1)
        self.wait(0.5)

        k32_focus_start = k32_focus.copy().scale(0.45).move_to(mapped_list[1].get_center()).set_opacity(0.0)
        self.add(k32_focus_start)
        self.play(FadeIn(k32_focus_start, run_time=0.8))

        self.play(
            k32_focus_start.animate.set_opacity(1.0).scale(2.22).move_to(k32_focus.get_center()),
            FadeOut(highlight),
            run_time=2.2
        )
        self.remove(k32_focus_start)
        self.add(k32_focus)

        self.play(Create(k32_import_to_focus), run_time=1.6)
        self.wait(0.6)

        self.play(FadeIn(paging_group, shift=UP * 0.05), run_time=1.6)
        self.play(Create(arrows_va_pa), run_time=2.0)
        self.wait(1.0)

        self.play(FadeIn(dbg_block), run_time=2.5)
        self.wait(3.0)
        self.play(FadeOut(dbg_block), run_time=2.5)

        self.wait(2.0)
