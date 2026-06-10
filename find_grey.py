from PIL import Image

img = Image.open('kernel32_map.png').convert('RGB')
w, h = img.size
grey_pixels = []
for y in range(h):
    for x in range(w):
        if img.getpixel((x, y)) == (192, 192, 192):
            grey_pixels.append((x, y))

if grey_pixels:
    min_x = min(p[0] for p in grey_pixels)
    max_x = max(p[0] for p in grey_pixels)
    min_y = min(p[1] for p in grey_pixels)
    max_y = max(p[1] for p in grey_pixels)
    print(f"Grey box bounding box (pixels): x=[{min_x}, {max_x}], y=[{min_y}, {max_y}]")
    print(f"Image size (pixels): {w}x{h}")
    
    # Calculate relative coordinates (from center, scaled)
    # In Manim, the image is scaled to width = 5.0
    manim_width = 5.0
    manim_height = 5.0 * (h / w)
    
    center_x_px = w / 2
    center_y_px = h / 2
    
    box_center_x_px = (min_x + max_x) / 2
    box_center_y_px = (min_y + max_y) / 2
    
    box_w_px = max_x - min_x
    box_h_px = max_y - min_y
    
    # In Manim, Y axis is inverted relative to pixel coordinates (Y goes up)
    rel_x = (box_center_x_px - center_x_px) / w * manim_width
    rel_y = -(box_center_y_px - center_y_px) / h * manim_height
    
    box_w_manim = box_w_px / w * manim_width
    box_h_manim = box_h_px / h * manim_height
    
    print(f"Manim Box: center relative to image center: ({rel_x:.4f}, {rel_y:.4f})")
    print(f"Manim Box: width={box_w_manim:.4f}, height={box_h_manim:.4f}")

else:
    print("No grey pixels found.")
