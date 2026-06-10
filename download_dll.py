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
        container_height = 6.4
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
        title = VGroup(
            Text("Виртуальная память", font_size=22),
            Text("приложения", font_size=22)
        ).arrange(DOWN, buff=0.1).next_to(top_wave, UP, buff=0.25)

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
        zero_bytes.move_to(rdata.get_bottom()).shift(UP * 0.35)

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
            zero_bytes
        ).to_edge(LEFT, buff=1.1)

        # =========================
        # 6) Правый стакан (Память ОС / Section Objects)
        # =========================
        right_container = outer_shape.copy().to_edge(RIGHT, buff=1.1)

        right_title = Text(
            "Память ОС (Object Manager)",
            font_size=18,
            color=WHITE,
            weight=BOLD
        ).next_to(right_container, UP, buff=0.25)

        section_title = VGroup(
            Text("Section Objects", font_size=16, color=YELLOW_B, weight=BOLD),
            Text("(\\\\KnownDlls)", font_size=16, color=YELLOW_B, weight=BOLD)
        ).arrange(DOWN, buff=0.1)
        
        section_list = VGroup(
            Text("ntdll.dll", font_size=14, color=WHITE),
            Text("kernel32.dll", font_size=14, color=WHITE),
            Text("user32.dll", font_size=14, color=WHITE),
        ).arrange(DOWN, buff=0.2)

        section_group_text = VGroup(section_title, section_list).arrange(DOWN, buff=0.25)

        section_box_width = max(container_width * 0.95, section_group_text.width + 0.4)
        section_box = RoundedRectangle(
            corner_radius=0.15,
            width=section_box_width,
            height=section_group_text.height + 0.6,
            color=GREEN_A,
            stroke_width=3,
            fill_opacity=0.1,
            fill_color=GREEN_E
        )
        section_group_text.move_to(section_box.get_center())
        
        section_objects_group = VGroup(section_box, section_group_text)
        
        right_content = VGroup(section_objects_group).arrange(DOWN, buff=0.22)
        right_content.set_x(right_container.get_center()[0])
        fit_inside_container(right_content, right_container, pad_x=0.26, pad_y=0.52)
        right_content.next_to(right_container.get_top(), DOWN, buff=0.4)
        right_content.set_x(right_container.get_center()[0])

        # =========================
        # 7) Элементы для kernel32.dll
        # =========================
        gap_center_x = (left_final.get_right()[0] + right_container.get_left()[0]) / 2

        call_1_k32 = Text("1. LdrpCheckKnownDll(\"kernel32.dll\")", font_size=14, color=YELLOW)
        result_1_k32 = Text("   -> System DLL (True)", font_size=14, color=GREEN)
        group_call_1_k32 = VGroup(call_1_k32, result_1_k32).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        call_2_k32 = Text("2. NtOpenSection(\\\\KnownDlls\\\\kernel32.dll)", font_size=14, color=YELLOW)
        group_call_2_k32 = VGroup(call_2_k32)

        call_3_k32 = Text("3. NtMapViewOfSection()", font_size=14, color=YELLOW)
        group_call_3_k32 = VGroup(call_3_k32)
        
        VGroup(group_call_1_k32, group_call_2_k32, group_call_3_k32).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(np.array([gap_center_x, 0.5, 0]))

        mapped_kernel32_rect = Rectangle(width=rdata.width * 0.9, height=0.6, color=LINE_COLOR, stroke_width=2, fill_color=BLUE_E, fill_opacity=0.4)
        mapped_kernel32_text = Text("kernel32.dll", font_size=14, color=WHITE)
        mapped_kernel32_text.move_to(mapped_kernel32_rect.get_center())
        mapped_kernel32_group = VGroup(mapped_kernel32_rect, mapped_kernel32_text)
        mapped_kernel32_group.next_to(import_table_group, DOWN, buff=0.35).set_x(rdata.get_center()[0])

        arrow_check_k32 = Arrow(dll_entries[0].get_right(), group_call_1_k32.get_left(), buff=0.1, color=WHITE)
        arrow_open_k32 = Arrow(group_call_2_k32.get_right(), section_list[1].get_left(), buff=0.1, color=GREEN)

        # =========================
        # 8) Элементы для libmysql.dll (Поиск в PATH)
        # =========================
        call_1_mysql = Text("1. LdrpCheckKnownDll(\"libmysql.dll\")", font_size=14, color=YELLOW)
        result_1_mysql = Text("   -> Not Found (False)", font_size=14, color=RED)
        group_call_1_mysql = VGroup(call_1_mysql, result_1_mysql).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        path_search_text = VGroup(
            Text("2. Поиск в путях PATH:", font_size=14, color=YELLOW, weight=BOLD),
            Text("   - C:\\App\\libmysql.dll (Not found)", font_size=12, color=GRAY),
            Text("   - C:\\Windows\\System32\\libmysql.dll (Not found)", font_size=12, color=GRAY),
            Text("   - C:\\MySQL\\bin\\libmysql.dll (Found!)", font_size=12, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        create_section_mysql = Text("3. NtCreateSection()", font_size=14, color=YELLOW)
        map_mysql = Text("4. NtMapViewOfSection()", font_size=14, color=YELLOW)
        
        VGroup(group_call_1_mysql, path_search_text, create_section_mysql, map_mysql).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(np.array([gap_center_x, 0.2, 0]))

        # Section Object в памяти ОС
        mysql_os_section_rect = RoundedRectangle(corner_radius=0.1, width=section_box_width, height=0.5, color=ORANGE, stroke_width=2, fill_opacity=0.1, fill_color=ORANGE)
        mysql_os_section_text = Text("libmysql.dll", font_size=14, color=WHITE)
        mysql_os_section_text.move_to(mysql_os_section_rect.get_center())
        mysql_os_section_group = VGroup(mysql_os_section_rect, mysql_os_section_text)
        mysql_os_section_group.next_to(section_objects_group, DOWN, buff=0.3).set_x(right_container.get_center()[0])

        mapped_mysql_rect = Rectangle(width=rdata.width * 0.9, height=0.6, color=LINE_COLOR, stroke_width=2, fill_color=ORANGE, fill_opacity=0.4)
        mapped_mysql_text = Text("libmysql.dll", font_size=14, color=WHITE)
        mapped_mysql_text.move_to(mapped_mysql_rect.get_center())
        mapped_mysql_group = VGroup(mapped_mysql_rect, mapped_mysql_text)
        mapped_mysql_group.next_to(mapped_kernel32_group, DOWN, buff=0.15).set_x(rdata.get_center()[0])
        
        arrow_check_mysql = Arrow(dll_entries[2].get_right(), group_call_1_mysql.get_left(), buff=0.1, color=WHITE)
        arrow_create_mysql = Arrow(create_section_mysql.get_right(), mysql_os_section_group.get_left(), buff=0.1, color=ORANGE)

        # =========================
        # 9) Страницы памяти (VA/PA) и скриншот
        # =========================


        screenshot_path = "kernel32_map.png"
        dbg_img = ImageMobject(screenshot_path).scale_to_fit_width(5.0)
        dbg_frame = RoundedRectangle(corner_radius=0.15, width=dbg_img.width + 0.18, height=dbg_img.height + 0.18, color=LINE_COLOR, stroke_width=2, fill_opacity=0.06)
        dbg_img.move_to(dbg_frame.get_center())
        kernel32_highlight = Rectangle(width=4.9881, height=0.6116, color=RED, stroke_width=3)
        kernel32_highlight.move_to(dbg_img.get_center() + np.array([0, 0.1158, 0]))
        dbg_block = Group(dbg_frame, dbg_img, kernel32_highlight).move_to(np.array([gap_center_x + 1.5, mapped_kernel32_group.get_center()[1] - 1.5, 0]))
        dbg_text = Text("Реальный диапазон загрузки в памяти", font_size=16, color=YELLOW_B).next_to(dbg_block, UP, buff=0.2)
        dbg_group = Group(dbg_block, dbg_text)
        
        kernel32_left_highlight = SurroundingRectangle(mapped_kernel32_rect, color=RED, buff=0, stroke_width=3)
        line_top = Line(kernel32_left_highlight.get_corner(UR), kernel32_highlight.get_corner(UL), color=RED, stroke_width=2)
        line_bot = Line(kernel32_left_highlight.get_corner(DR), kernel32_highlight.get_corner(DL), color=RED, stroke_width=2)
        dbg_group.add(kernel32_left_highlight, line_top, line_bot)

        # =========================
        # 10) Анимация
        # =========================
        master_shift_group = Group(
            left_final, right_container, right_title, section_objects_group,
            group_call_1_k32, group_call_2_k32, group_call_3_k32,
            mapped_kernel32_group, arrow_check_k32, arrow_open_k32,
            group_call_1_mysql, path_search_text, create_section_mysql, map_mysql,
            mysql_os_section_group, mapped_mysql_group, arrow_check_mysql, arrow_create_mysql,
            dbg_group
        )
        master_shift_group.shift(DOWN * 0.6)

        self.add(left_final, right_container)

        # --- ЧАСТЬ 1: Системная DLL (kernel32.dll) ---
        self.play(FadeIn(right_title, shift=UP * 0.08), run_time=1.0)
        self.play(FadeIn(section_objects_group, shift=UP * 0.06), run_time=1.0)
        self.wait(0.5)

        highlight_import_k32 = SurroundingRectangle(dll_entries[0], color=YELLOW_B, buff=0.05, stroke_width=2)
        self.play(Create(highlight_import_k32), run_time=0.8)
        self.play(Create(arrow_check_k32), FadeIn(group_call_1_k32), run_time=1.2)
        self.wait(1.0)

        self.play(FadeIn(group_call_2_k32, shift=DOWN*0.2), run_time=0.8)
        self.play(Create(arrow_open_k32), run_time=0.8)
        highlight_section_k32 = SurroundingRectangle(section_list[1], color=GREEN_A, buff=0.05, stroke_width=2)
        self.play(Create(highlight_section_k32), run_time=0.8)
        self.wait(1.0)

        self.play(FadeIn(group_call_3_k32, shift=DOWN*0.2), run_time=0.8)
        
        projection_ghost_k32 = section_list[1].copy()
        projection_ghost_k32.set_color(BLUE_C)
        self.play(Transform(projection_ghost_k32, mapped_kernel32_group), run_time=2.0, path_arc=-0.5)
        self.wait(0.5)

        # Показываем скриншот
        self.play(FadeOut(group_call_1_k32), FadeOut(group_call_2_k32), FadeOut(group_call_3_k32), FadeOut(arrow_check_k32), FadeOut(arrow_open_k32))

        self.play(FadeIn(dbg_group, shift=DOWN * 0.1), run_time=1.5)
        self.wait(3.0)

        self.play(FadeOut(dbg_group), FadeOut(highlight_section_k32), FadeOut(highlight_import_k32), run_time=1.0)

        # --- ЧАСТЬ 2: Сторонняя DLL (libmysql.dll) ---
        highlight_import_mysql = SurroundingRectangle(dll_entries[2], color=YELLOW_B, buff=0.05, stroke_width=2)
        self.play(Create(highlight_import_mysql), run_time=0.8)
        
        self.play(Create(arrow_check_mysql), FadeIn(group_call_1_mysql), run_time=1.2)
        self.wait(1.0)

        self.play(FadeIn(path_search_text[0]), run_time=0.5)
        self.play(FadeIn(path_search_text[1]), run_time=0.8)
        self.wait(0.3)
        self.play(FadeIn(path_search_text[2]), run_time=0.8)
        self.wait(0.3)
        self.play(FadeIn(path_search_text[3]), run_time=0.8)
        self.wait(1.0)

        # Список остается на экране до конца анимации mysql
        self.wait(0.5)

        self.play(FadeIn(create_section_mysql, shift=DOWN*0.1), run_time=0.8)
        self.play(Create(arrow_create_mysql), FadeIn(mysql_os_section_group, shift=UP*0.1), run_time=1.2)
        self.wait(1.0)

        self.play(FadeIn(map_mysql, shift=DOWN*0.1), run_time=0.8)

        projection_ghost_mysql = mysql_os_section_group.copy()
        projection_ghost_mysql.set_color(ORANGE)
        self.play(Transform(projection_ghost_mysql, mapped_mysql_group), run_time=2.0, path_arc=-0.3)
        self.wait(1.0)

        self.play(FadeOut(group_call_1_mysql), FadeOut(path_search_text), FadeOut(create_section_mysql), FadeOut(arrow_create_mysql), FadeOut(map_mysql), FadeOut(highlight_import_mysql), FadeOut(arrow_check_mysql), run_time=1.0)

        # --- ЧАСТЬ 3: Обновление IAT ---
        iat_caption = Text("Заполнение IAT из Export Table загруженных DLL", font_size=14, color=YELLOW_B).next_to(zero_bytes, UP, buff=0.2)
        self.play(FadeIn(iat_caption), run_time=1.0)
        
        # Стрелки, показывающие откуда берутся адреса (из загруженных библиотек) - "воронкой"
        arrow_eat_1_r = CurvedArrow(mapped_kernel32_group.get_right(), zero_bytes.get_right() + UP*0.1, angle=-TAU/4, color=GREEN_C)
        
        arrow_eat_2_r = CurvedArrow(mapped_mysql_group.get_right(), zero_bytes.get_right() + DOWN*0.1, angle=-TAU/4, color=GREEN_C)
        
        self.play(
            Create(arrow_eat_1_r),
            Create(arrow_eat_2_r),
            run_time=1.5
        )
        
        real_addresses = VGroup(
            Text("... 0x7FF84B341000", font_size=16, color=GREEN),
            Text("0x7FF84B401000 ...", font_size=16, color=GREEN)
        ).arrange(DOWN, aligned_edge=RIGHT, buff=0.1).move_to(zero_bytes.get_center())

        self.play(Transform(zero_bytes, real_addresses), run_time=1.5)
        self.wait(3.0)
