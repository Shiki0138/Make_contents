"""
Instagram Carousel Generator - 4:5 Format with Avatar (First Slide Only)
Marketer-perspective content for beauty industry
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Carousel specifications (4:5)
IMAGE_SIZE = (1080, 1350)
MARGIN = 70
MAX_WIDTH = IMAGE_SIZE[0] - (MARGIN * 2)

COLORS = {
    "background": "#FFFFFF",
    "text": "#000000",
    "accent": "#FFE500",
    "gray": "#666666",
    "light_gray": "#F5F5F5",
}

FONTS = {
    "black": "fonts/NotoSansJP-Black.ttf",
    "thin": "fonts/NotoSansJP-Thin.ttf",
}

AVATAR_PATH = "assets/avatar.png"


def hex_to_rgb(hex_color):
    return tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))


def get_font(size, style="black"):
    try:
        return ImageFont.truetype(FONTS[style], size)
    except:
        return ImageFont.load_default()


def get_text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def fit_font_size(draw, text, max_size, max_width, min_size=28):
    """Reduce font size until text fits"""
    size = max_size
    while size > min_size:
        font = get_font(size)
        w, _ = get_text_size(draw, text, font)
        if w <= max_width:
            return font, size
        size -= 4
    return get_font(min_size), min_size


def add_avatar(img, position="bottom_left", size_height=180):
    """Add avatar character to image"""
    try:
        avatar = Image.open(AVATAR_PATH).convert("RGBA")
        ratio = size_height / avatar.height
        new_size = (int(avatar.width * ratio), size_height)
        avatar = avatar.resize(new_size, Image.Resampling.LANCZOS)
        
        if position == "bottom_left":
            x = 50
            y = img.height - avatar.height - 50
        
        img.paste(avatar, (x, y), avatar)
    except Exception as e:
        print(f"Avatar not found or error: {e}")
    return img


def create_title_slide(main_text, sub_text, tag_text, output_path):
    """Slide 1: Maximum impact title with dramatic font size variation"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    # Tag at top - small
    font_tag = get_font(28, "thin")
    tag_w, _ = get_text_size(draw, tag_text, font_tag)
    draw.text(((IMAGE_SIZE[0] - tag_w) // 2, 100), tag_text, 
              font=font_tag, fill=hex_to_rgb(COLORS["gray"]))
    
    # Split main_text into smaller line + emphasized line
    # Format: "line1,EMPHASIZED" or just "text"
    if "," in main_text:
        parts = main_text.split(",", 1)
        line1 = parts[0].strip()
        emphasized = parts[1].strip()
    else:
        # If no comma, treat last few chars as emphasized
        line1 = main_text
        emphasized = ""
    
    center_y = IMAGE_SIZE[1] // 2 - 50
    
    if emphasized:
        # Line 1 - smaller size (60-80px)
        font_line1, _ = fit_font_size(draw, line1, 80, MAX_WIDTH - 40, min_size=50)
        l1_w, l1_h = get_text_size(draw, line1, font_line1)
        
        # Emphasized text - HUGE with yellow highlight (160-200px)
        font_emph, emph_size = fit_font_size(draw, emphasized, 200, MAX_WIDTH - 60, min_size=120)
        emph_w, emph_h = get_text_size(draw, emphasized, font_emph)
        
        # Calculate positions
        total_h = l1_h + 20 + emph_h
        start_y = center_y - (total_h // 2)
        
        # Draw line 1 (smaller, gray or black)
        draw.text(((IMAGE_SIZE[0] - l1_w) // 2, start_y), line1, 
                  font=font_line1, fill=hex_to_rgb(COLORS["text"]))
        
        # Draw yellow highlight bar behind emphasized text
        emph_x = (IMAGE_SIZE[0] - emph_w) // 2
        emph_y = start_y + l1_h + 20
        bar_padding = 10
        draw.rectangle([
            emph_x - bar_padding, 
            emph_y + emph_h - 35,
            emph_x + emph_w + bar_padding, 
            emph_y + emph_h + 5
        ], fill=hex_to_rgb(COLORS["accent"]))
        
        # Draw emphasized text
        draw.text((emph_x, emph_y), emphasized, 
                  font=font_emph, fill=hex_to_rgb(COLORS["text"]))
        
        sub_y = emph_y + emph_h + 50
    else:
        # Single line - just make it big
        font_main, _ = fit_font_size(draw, main_text, 180, MAX_WIDTH - 40)
        main_w, main_h = get_text_size(draw, main_text, font_main)
        draw.text(((IMAGE_SIZE[0] - main_w) // 2, center_y - main_h // 2), main_text, 
                  font=font_main, fill=hex_to_rgb(COLORS["text"]))
        sub_y = center_y + main_h // 2 + 50
    
    # Subtitle - medium size
    font_sub = get_font(52)
    sub_w, _ = get_text_size(draw, sub_text, font_sub)
    draw.text(((IMAGE_SIZE[0] - sub_w) // 2, sub_y), sub_text, 
              font=font_sub, fill=hex_to_rgb(COLORS["gray"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_title_slide_two_line(line1, line2, line2_highlight, sub_text, tag_text, output_path):
    """Title slide with dramatic font size contrast - line1 small, line2+highlight HUGE"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    # Tag at top - small
    font_tag = get_font(28, "thin")
    tag_w, _ = get_text_size(draw, tag_text, font_tag)
    draw.text(((IMAGE_SIZE[0] - tag_w) // 2, 100), tag_text, 
              font=font_tag, fill=hex_to_rgb(COLORS["gray"]))
    
    # Line 1 - SMALL (60-70px) - creates contrast
    font_line1, _ = fit_font_size(draw, line1, 70, MAX_WIDTH - 40, min_size=50)
    l1_w, l1_h = get_text_size(draw, line1, font_line1)
    
    # Line 2 with highlight - HUGE (160-200px)
    full_line2 = line2 + line2_highlight
    font_line2, _ = fit_font_size(draw, full_line2, 200, MAX_WIDTH - 40, min_size=120)
    l2_w, l2_h = get_text_size(draw, full_line2, font_line2)
    l2_normal_w, _ = get_text_size(draw, line2, font_line2)
    l2_highlight_w, _ = get_text_size(draw, line2_highlight, font_line2)
    
    # Calculate vertical center
    total_h = l1_h + 15 + l2_h
    start_y = (IMAGE_SIZE[1] - total_h) // 2 - 80
    
    # Draw line 1 (smaller)
    draw.text(((IMAGE_SIZE[0] - l1_w) // 2, start_y), line1, 
              font=font_line1, fill=hex_to_rgb(COLORS["gray"]))
    
    # Draw line 2 with highlight
    line2_y = start_y + l1_h + 15
    line2_x = (IMAGE_SIZE[0] - l2_w) // 2
    
    # Draw normal part
    if line2:
        draw.text((line2_x, line2_y), line2, 
                  font=font_line2, fill=hex_to_rgb(COLORS["text"]))
    
    # Draw yellow underline bar behind highlighted text
    highlight_x = line2_x + l2_normal_w
    bar_padding = 8
    draw.rectangle([
        highlight_x - bar_padding, 
        line2_y + l2_h - 30,
        highlight_x + l2_highlight_w + bar_padding, 
        line2_y + l2_h + 5
    ], fill=hex_to_rgb(COLORS["accent"]))
    
    # Draw highlighted text
    draw.text((highlight_x, line2_y), line2_highlight, 
              font=font_line2, fill=hex_to_rgb(COLORS["text"]))
    
    # Subtitle - medium
    font_sub = get_font(48)
    sub_w, _ = get_text_size(draw, sub_text, font_sub)
    draw.text(((IMAGE_SIZE[0] - sub_w) // 2, line2_y + l2_h + 60), sub_text, 
              font=font_sub, fill=hex_to_rgb(COLORS["gray"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_content_slide(lines, output_path):
    """Content slide with multiple lines - NO avatar"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    # Larger font sizes
    sizes = {"xl": 160, "l": 110, "m": 80, "s": 60}
    
    # Calculate heights
    line_data = []
    for item in lines:
        if item.get("text") == "":
            line_data.append({"type": "empty", "height": 40})
            continue
        
        text = item["text"]
        size = sizes.get(item.get("size", "m"), 80)
        font, _ = fit_font_size(draw, text, size, MAX_WIDTH)
        w, h = get_text_size(draw, text, font)
        line_data.append({
            "type": "single",
            "text": text,
            "font": font,
            "height": h,
            "width": w,
            "highlight": item.get("highlight", False),
            "center": item.get("center", False)
        })
    
    total_height = sum(ld["height"] + 35 for ld in line_data)
    start_y = (IMAGE_SIZE[1] - total_height) // 2
    start_y = max(start_y, 100)
    
    # Draw lines
    current_y = start_y
    for ld in line_data:
        if ld["type"] == "empty":
            current_y += ld["height"]
            continue
        
        # Center or left align
        if ld.get("center"):
            x = (IMAGE_SIZE[0] - ld["width"]) // 2
        else:
            x = MARGIN + 10
        
        # Highlight underline bar (bottom 30% of text height)
        if ld.get("highlight"):
            bar_h = max(int(ld["height"] * 0.3), 10)
            padding_x = 8
            draw.rectangle([
                x - padding_x,
                current_y + ld["height"] - bar_h + 4,
                x + ld["width"] + padding_x,
                current_y + ld["height"] + 4
            ], fill=hex_to_rgb(COLORS["accent"]))
        
        draw.text((x, current_y), ld["text"], font=ld["font"], 
                  fill=hex_to_rgb(COLORS["text"]))
        current_y += ld["height"] + 35
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_vertical_text_slide(main_char, sub_text, output_path):
    """Vertical text emphasis slide - NO avatar"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    # Main vertical text - larger
    font_main = get_font(220)
    chars = list(main_char)
    total_height = 0
    char_data = []
    
    for char in chars:
        w, h = get_text_size(draw, char, font_main)
        char_data.append({"char": char, "w": w, "h": h})
        total_height += h + 25
    
    start_y = (IMAGE_SIZE[1] - total_height) // 2 - 50
    x = IMAGE_SIZE[0] // 2 - 110
    
    current_y = start_y
    for cd in char_data:
        draw.text((x, current_y), cd["char"], font=font_main, 
                  fill=hex_to_rgb(COLORS["text"]))
        current_y += cd["h"] + 25
    
    # Subtitle at bottom right
    if sub_text:
        font_sub = get_font(52)
        sw, _ = get_text_size(draw, sub_text, font_sub)
        draw.text((IMAGE_SIZE[0] - sw - 80, IMAGE_SIZE[1] - 180), sub_text, 
                  font=font_sub, fill=hex_to_rgb(COLORS["text"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_cta_slide(main_cta, sub_lines, follow_text, output_path):
    """Call-to-action slide - NO avatar"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    # Main CTA - larger
    font_cta, _ = fit_font_size(draw, main_cta, 100, MAX_WIDTH - 40)
    cta_w, cta_h = get_text_size(draw, main_cta, font_cta)
    
    # Calculate sub heights
    sub_data = []
    for line in sub_lines:
        font_sub, _ = fit_font_size(draw, line, 56, MAX_WIDTH)
        w, h = get_text_size(draw, line, font_sub)
        sub_data.append({"font": font_sub, "w": w, "h": h, "line": line})
    
    total_sub = sum(sd["h"] + 30 for sd in sub_data)
    total_height = cta_h + 70 + total_sub
    start_y = (IMAGE_SIZE[1] - total_height) // 2 - 50
    
    # Draw CTA
    draw.text(((IMAGE_SIZE[0] - cta_w) // 2, start_y), main_cta, 
              font=font_cta, fill=hex_to_rgb(COLORS["text"]))
    
    # Draw sub lines
    sub_y = start_y + cta_h + 70
    for sd in sub_data:
        x = (IMAGE_SIZE[0] - sd["w"]) // 2
        draw.text((x, sub_y), sd["line"], font=sd["font"], 
                  fill=hex_to_rgb(COLORS["text"]))
        sub_y += sd["h"] + 30
    
    # Follow text - bold and closer to sub_lines
    font_follow = get_font(40, "black")
    fw, _ = get_text_size(draw, follow_text, font_follow)
    draw.text(((IMAGE_SIZE[0] - fw) // 2, sub_y + 40), follow_text, 
              font=font_follow, fill=hex_to_rgb(COLORS["text"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_cta_with_image(main_cta, sub_text, image_path, output_path):
    """CTA slide with embedded image and Fleeks branding"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    # Load and resize PDF image first to calculate layout
    pdf_img = None
    img_h = 0
    try:
        pdf_img = Image.open(image_path).convert("RGB")
        # Resize to fit (max width 750, max height 650)
        max_w = 750
        ratio = max_w / pdf_img.width
        new_size = (max_w, int(pdf_img.height * ratio))
        if new_size[1] > 650:
            ratio = 650 / pdf_img.height
            new_size = (int(pdf_img.width * ratio), 650)
        pdf_img = pdf_img.resize(new_size, Image.Resampling.LANCZOS)
        img_h = new_size[1]
    except Exception as e:
        print(f"Error loading image: {e}")
    
    # Calculate fonts
    font_cta, _ = fit_font_size(draw, main_cta, 72, MAX_WIDTH - 40)
    cta_w, cta_h = get_text_size(draw, main_cta, font_cta)
    
    font_sub = get_font(44)
    sw, sh = get_text_size(draw, sub_text, font_sub)
    
    # Calculate total height and center vertically
    spacing = 40
    total_h = cta_h + spacing + img_h + spacing + sh
    start_y = (IMAGE_SIZE[1] - total_h) // 2
    
    # Draw CTA at top
    draw.text(((IMAGE_SIZE[0] - cta_w) // 2, start_y), main_cta, 
              font=font_cta, fill=hex_to_rgb(COLORS["text"]))
    
    # Draw image in center
    if pdf_img:
        img_x = (IMAGE_SIZE[0] - pdf_img.width) // 2
        img_y = start_y + cta_h + spacing
        img.paste(pdf_img, (img_x, img_y))
    
    # Draw sub text at bottom
    sub_y = start_y + cta_h + spacing + img_h + spacing
    draw.text(((IMAGE_SIZE[0] - sw) // 2, sub_y), sub_text, 
              font=font_sub, fill=hex_to_rgb(COLORS["text"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_example_slide(image_path, title_text, example_lines, output_path):
    """Create a concrete example slide with isometric image background and text overlay"""
    bg_color = (245, 240, 235)
    img = Image.new('RGB', IMAGE_SIZE, bg_color)

    if os.path.exists(image_path):
        iso_img = Image.open(image_path).convert('RGBA')
        target_w = IMAGE_SIZE[0] - 80
        ratio = target_w / iso_img.width
        target_h = int(iso_img.height * ratio)
        iso_img = iso_img.resize((target_w, target_h), Image.LANCZOS)
        x = (IMAGE_SIZE[0] - target_w) // 2
        y = 40
        img.paste(iso_img, (x, y), iso_img if iso_img.mode == 'RGBA' else None)

    draw = ImageDraw.Draw(img)

    overlay_y = IMAGE_SIZE[1] - 520
    draw.rectangle([(0, overlay_y), (IMAGE_SIZE[0], IMAGE_SIZE[1])], fill=(30, 30, 30))

    font_title = get_font(52, "black")
    tw, th = get_text_size(draw, title_text, font_title)
    draw.text(((IMAGE_SIZE[0] - tw) // 2, overlay_y + 40), title_text,
              font=font_title, fill=(255, 255, 255))

    line_y = overlay_y + 40 + th + 40
    for line in example_lines:
        font_line = get_font(40, "black")
        lw, lh = get_text_size(draw, line, font_line)
        draw.text(((IMAGE_SIZE[0] - lw) // 2, line_y), line,
                  font=font_line, fill=(255, 255, 255))
        line_y += lh + 25

    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def generate_day1():
    """Day 1: お客様が技術より見ている3つのこと"""
    output_dir = "output/day1_customer_priority"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル
    create_title_slide(
        "接客のポイント３つ",
        "お客側が気にしていること",
        "CUSTOMER INSIGHT",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. 問題提起
    create_content_slide([
        {"text": "技術が上手ければ", "size": "l"},
        {"text": "選ばれる？", "size": "l"},
        {"text": ""},
        {"text": "実は、それだけじゃない", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 導入（3選への橋渡し）
    create_content_slide([
        {"text": "お客様が技術より", "size": "l"},
        {"text": "見ているのは", "size": "l"},
        {"text": ""},
        {"text": "次の3つ", "size": "xl"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. ① 話しやすさ
    create_content_slide([
        {"text": "① 話しやすさ", "size": "l"},
        {"text": ""},
        {"text": "「この人なら相談できる」", "size": "m"},
        {"text": "と思えるかどうか", "size": "m"},
        {"text": ""},
        {"text": "技術より先に見ている", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. ② 清潔感・雰囲気
    create_content_slide([
        {"text": "② 清潔感・雰囲気", "size": "l"},
        {"text": ""},
        {"text": "店内の印象", "size": "m"},
        {"text": "スタッフの身だしなみ", "size": "m"},
        {"text": ""},
        {"text": "「ここなら大丈夫」の判断材料", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # 6. ③ 任せて大丈夫感
    create_content_slide([
        {"text": "③ 任せて大丈夫感", "size": "l"},
        {"text": ""},
        {"text": "「お任せでも失敗しない」", "size": "m"},
        {"text": "という安心感", "size": "m"},
        {"text": ""},
        {"text": "これが一番の決め手", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")
    
    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "技術は「前提」でしかない", "size": "m"},
        {"text": ""},
        {"text": "選ばれるのは", "size": "m"},
        {"text": "信頼できる人", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")
    
    # 8. 縦文字キーワード
    create_vertical_text_slide("信頼", "技術＜信頼", f"{output_dir}/slide_08.png")
    
    # 9. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①話しやすさを意識する", "②清潔感を見直す", "③安心感を伝える"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_09.png"
    )
    
    print(f"\n✅ Day 1 complete! Check {output_dir}/")
    return output_dir


def generate_day2():
    """Day 2: 「また来ます」に隠された本音3選"""
    output_dir = "output/day2_mata_kimasu"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル
    create_title_slide_two_line(
        "「また来ます」の",
        "",
        "裏側",
        "お客が言わない本音",
        "CUSTOMER TRUTH",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. 問題提起
    create_content_slide([
        {"text": "「また来ます！」", "size": "l"},
        {"text": "と言われて安心してない？", "size": "l"},
        {"text": ""},
        {"text": "実は、本音は別にある", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 導入
    create_content_slide([
        {"text": "「また来ます」に隠された", "size": "l"},
        {"text": "本音は", "size": "l"},
        {"text": ""},
        {"text": "次の3つ", "size": "xl"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. ①
    create_content_slide([
        {"text": "① 社交辞令として言っている", "size": "l"},
        {"text": ""},
        {"text": "断るのが気まずいから", "size": "m"},
        {"text": "とりあえず言ってるだけ", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. ②
    create_content_slide([
        {"text": "② 他と比較してから決める", "size": "l"},
        {"text": ""},
        {"text": "良かったけど", "size": "m"},
        {"text": "「他も試したい」が本音", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # 6. ③
    create_content_slide([
        {"text": "③ 決め手がないとリピートしない", "size": "l"},
        {"text": ""},
        {"text": "「悪くなかった」では弱い", "size": "m"},
        {"text": "「ここじゃなきゃ」が必要", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")
    
    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "「また来ます」ではなく", "size": "m"},
        {"text": "「次は〇〇したい」を引き出す", "size": "m"},
        {"text": ""},
        {"text": "具体的な約束がリピートを生む", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_07.png")
    
    # 8. 縦文字
    create_vertical_text_slide("具体", "具体的な約束を引き出す", f"{output_dir}/slide_08.png")
    
    # 9. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["「また来ます」を鵜呑みにしない", "「次は何したい？」と聞く", "具体的な予約に繋げる"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_09.png"
    )
    
    print(f"\n✅ Day 2 complete! Check {output_dir}/")
    return output_dir


def generate_day3():
    """Day 3: 信頼されるカウンセリングの心理学"""
    output_dir = "output/day3_counseling"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル
    create_title_slide_two_line(
        "信頼を生む",
        "カウンセリング",
        "術",
        "お客様が心を開く3つのステップ",
        "TRUST PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. 問題提起
    create_content_slide([
        {"text": "お客様が本当に", "size": "l"},
        {"text": "求めているのは", "size": "l"},
        {"text": ""},
        {"text": "話を聞いてほしい", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 心理学的背景
    create_content_slide([
        {"text": "心理学：傾聴の効果", "size": "l"},
        {"text": ""},
        {"text": "悩みを聞いてもらえると", "size": "m"},
        {"text": "「この人ならわかってくれる」", "size": "m"},
        {"text": ""},
        {"text": "安心感 → 信頼に変わる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_03.png")
    
    # 4. ① 不安を受け止める
    create_content_slide([
        {"text": "① まず不安を受け止める", "size": "l"},
        {"text": ""},
        {"text": "「〇〇が気になるんですね」", "size": "m"},
        {"text": "「わかります、そう思いますよね」", "size": "m"},
        {"text": ""},
        {"text": "→ 否定せず、共感する", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. ② 悩みを言語化する
    create_content_slide([
        {"text": "② 悩みを言語化してあげる", "size": "l"},
        {"text": ""},
        {"text": "お客様は上手く言えない", "size": "m"},
        {"text": "「つまり〇〇ということですか？」", "size": "m"},
        {"text": ""},
        {"text": "→ 代わりに言葉にする", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_05.png")
    
    # 6. ③ 解決策を提示する
    create_content_slide([
        {"text": "③ 解決策を自信を持って提示", "size": "l"},
        {"text": ""},
        {"text": "「それなら〇〇がおすすめ」", "size": "m"},
        {"text": "「私に任せてください」", "size": "m"},
        {"text": ""},
        {"text": "→ 期待感を持たせる", "size": "m"},
    ], f"{output_dir}/slide_06.png")
    
    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "聞く → 共感 → 提案", "size": "m"},
        {"text": ""},
        {"text": "この順番で", "size": "m"},
        {"text": "信頼と期待が生まれる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_07.png")
    
    # 8. 縦文字
    create_vertical_text_slide("共感", "共感が信頼を生む", f"{output_dir}/slide_08.png")
    
    # 9. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①不安を受け止める", "②悩みを言語化する", "③解決策を自信を持って提示"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_09.png"
    )
    
    print(f"\n✅ Day 3 complete! Check {output_dir}/")
    return output_dir


def generate_day4():
    """Day 4: ビフォーアフターで予約が来ない理由（15枚版）"""
    output_dir = "output/day4_before_after"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル
    create_title_slide(
        "予約に繋がらない",
        "ビフォーアフターの特徴",
        "CONTENT STRATEGY",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. 問題提起
    create_content_slide([
        {"text": "ビフォーアフターを", "size": "l"},
        {"text": "毎日投稿してるのに...", "size": "l"},
        {"text": ""},
        {"text": "予約に繋がらない", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 共感
    create_content_slide([
        {"text": "頑張って撮影して", "size": "l"},
        {"text": "編集して投稿して", "size": "l"},
        {"text": ""},
        {"text": "なのに反応がない...", "size": "m"},
        {"text": ""},
        {"text": "その気持ち、わかります", "size": "m"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 導入
    create_content_slide([
        {"text": "でも実は", "size": "l"},
        {"text": "予約が来ない理由は", "size": "l"},
        {"text": ""},
        {"text": "明確にあります", "size": "xl"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. 問題①
    create_content_slide([
        {"text": "問題①", "size": "l"},
        {"text": ""},
        {"text": "全部同じに見える", "size": "xl"},
        {"text": ""},
        {"text": "上手い人はたくさんいる", "size": "m"},
        {"text": "差がわからない", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # 6. 問題②
    create_content_slide([
        {"text": "問題②", "size": "l"},
        {"text": ""},
        {"text": "「私もこうなれる？」", "size": "xl"},
        {"text": "がわからない", "size": "xl"},
        {"text": ""},
        {"text": "モデルさんは元が違う...", "size": "m"},
    ], f"{output_dir}/slide_06.png")
    
    # 7. 問題③
    create_content_slide([
        {"text": "問題③", "size": "l"},
        {"text": ""},
        {"text": "人柄が見えない", "size": "xl"},
        {"text": ""},
        {"text": "技術はわかった", "size": "m"},
        {"text": "でも「この人に頼みたい」がない", "size": "m"},
    ], f"{output_dir}/slide_07.png")
    
    # 8. 転換
    create_vertical_text_slide("解決", "じゃあどうする？", f"{output_dir}/slide_08.png")
    
    # 9. 解決策①
    create_content_slide([
        {"text": "解決策①", "size": "l"},
        {"text": ""},
        {"text": "過程を見せる", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "施術中の動画", "size": "m"},
        {"text": "ビフォー→途中→アフター", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # 10. 解決策②
    create_content_slide([
        {"text": "解決策②", "size": "l"},
        {"text": ""},
        {"text": "会話を見せる", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「こんな悩みがあって...」", "size": "m"},
        {"text": "お客様の声をストーリーに", "size": "m"},
    ], f"{output_dir}/slide_10.png")
    
    # 11. 解決策③
    create_content_slide([
        {"text": "解決策③", "size": "l"},
        {"text": ""},
        {"text": "人柄を出す", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "自分の考え・価値観", "size": "m"},
        {"text": "失敗談やこだわり", "size": "m"},
    ], f"{output_dir}/slide_11.png")
    
    # 12. 具体例
    create_content_slide([
        {"text": "具体例", "size": "l"},
        {"text": ""},
        {"text": "「髪が傷んでたお客様が", "size": "m"},
        {"text": "3ヶ月でここまで回復」", "size": "m"},
        {"text": ""},
        {"text": "↑ ストーリーがあると", "size": "m"},
        {"text": "自分ごとになる", "size": "m"},
    ], f"{output_dir}/slide_12.png")
    
    # 13. 比較
    create_content_slide([
        {"text": "比較してみて", "size": "l"},
        {"text": ""},
        {"text": "❌ 技術だけ見せる", "size": "m"},
        {"text": "→ 誰でも良くなる", "size": "m"},
        {"text": ""},
        {"text": "✅ ストーリーを見せる", "size": "m"},
        {"text": "→ この人に頼みたい", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "まとめ", "size": "l"},
        {"text": ""},
        {"text": "① 過程を見せる", "size": "m"},
        {"text": "② 会話を見せる", "size": "m"},
        {"text": "③ 人柄を出す", "size": "m"},
        {"text": ""},
        {"text": "技術＜ストーリー", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["過程を見せる投稿を作る", "お客様の声を載せる", "自分の考えを発信する"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ Day 4 complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_day5():
    """Day 5: 「どうしますか？」の心理学的間違い（15枚版）"""
    output_dir = "output/day5_dou_shimasuka"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル
    create_title_slide(
        "失客する質問",
        "その一言で台無しに...",
        "SERVICE DESIGN",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. ストーリー開始
    create_content_slide([
        {"text": "美容室での", "size": "l"},
        {"text": "あるある風景", "size": "l"},
        {"text": ""},
        {"text": "「いらっしゃいませ！」", "size": "m"},
        {"text": "「今日はどうしますか？」", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. お客様の心情
    create_content_slide([
        {"text": "その瞬間...", "size": "l"},
        {"text": ""},
        {"text": "（えっ...どうしよう...）", "size": "m"},
        {"text": "（専門用語わからないし...）", "size": "m"},
        {"text": "（似合うのがわからない...）", "size": "m"},
        {"text": ""},
        {"text": "お客様はフリーズする", "size": "xl"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 心理学解説
    create_content_slide([
        {"text": "なぜ固まるのか？", "size": "l"},
        {"text": ""},
        {"text": "心理学：選択のパラドックス", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "選択肢が無限にあると", "size": "m"},
        {"text": "人は選べず不幸になる", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. 決定疲れ
    create_content_slide([
        {"text": "さらに：決定疲れ", "size": "l"},
        {"text": ""},
        {"text": "人は1日に35,000回", "size": "m"},
        {"text": "決断をしている。", "size": "m"},
        {"text": ""},
        {"text": "「どうしますか？」は", "size": "m"},
        {"text": "脳に負担をかける質問", "size": "l", "highlight": True},
    ], f"{output_dir}/slide_05.png")
    
    # 6. 残念な結果
    create_content_slide([
        {"text": "脳が疲れた結果...", "size": "l"},
        {"text": ""},
        {"text": "「あ、いつもの感じで...」", "size": "m"},
        {"text": "「とりあえず揃えるだけで...」", "size": "m"},
        {"text": ""},
        {"text": "無難な選択になる", "size": "xl"},
    ], f"{output_dir}/slide_06.png")
    
    # 7. 共感
    create_content_slide([
        {"text": "これでは", "size": "l"},
        {"text": ""},
        {"text": "単価も上がらないし", "size": "m"},
        {"text": "感動も生まれない。", "size": "m"},
        {"text": ""},
        {"text": "「この人、提案してくれない」", "size": "m"},
        {"text": "と信頼も下がる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_07.png")
    
    # 8. 転換
    create_vertical_text_slide("提案", "聞くのではなく提案せよ", f"{output_dir}/slide_08.png")
    
    # 9. 解決策：2択
    create_content_slide([
        {"text": "鉄則", "size": "l"},
        {"text": ""},
        {"text": "思考させない", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "オープンクエスチョン禁止。", "size": "m"},
        {"text": "「2択」で選ばせる。", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # 10. 具体例①
    create_content_slide([
        {"text": "カラーの場合", "size": "l"},
        {"text": ""},
        {"text": "❌ どういう色にしますか？", "size": "m"},
        {"text": ""},
        {"text": "⭕️ 明るさ重視ならA", "size": "m"},
        {"text": "　 色持ち重視ならB", "size": "m"},
        {"text": "　 どっちが気分ですか？", "size": "l", "highlight": True},
    ], f"{output_dir}/slide_10.png")
    
    # 11. 具体例②
    create_content_slide([
        {"text": "カットの場合", "size": "l"},
        {"text": ""},
        {"text": "❌ どれくらい切りますか？", "size": "m"},
        {"text": ""},
        {"text": "⭕️ 結べる長さを残すか", "size": "m"},
        {"text": "　 バッサリ変えるか", "size": "m"},
        {"text": "　 今日はどっちにしますか？", "size": "l", "highlight": True},
    ], f"{output_dir}/slide_11.png")
    
    # 12. 心理的効果
    create_content_slide([
        {"text": "2択にする効果", "size": "l"},
        {"text": ""},
        {"text": "「考える作業」が", "size": "m"},
        {"text": "「選ぶ作業」に変わる。", "size": "m"},
        {"text": ""},
        {"text": "脳のストレスが", "size": "m"},
        {"text": "劇的に減る！", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_12.png")
    
    # 13. 結果
    create_content_slide([
        {"text": "すると...", "size": "l"},
        {"text": ""},
        {"text": "「じゃあ今回はAで！」", "size": "xl"},
        {"text": ""},
        {"text": "自分で選んだから納得する。", "size": "m"},
        {"text": "プロとしてリードしてくれた", "size": "m"},
        {"text": "安心感が生まれる。", "size": "m"},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "プロの仕事", "size": "l"},
        {"text": ""},
        {"text": "お客様に考えさせるな。", "size": "m"},
        {"text": "選択肢を絞って提示せよ。", "size": "m"},
        {"text": ""},
        {"text": "それが「提案」です", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["「どうしますか？」禁止", "2択で提案する", "選ぶストレスを減らす"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ Day 5 complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_day6():
    """Day 6: フォロワーが予約しない理由（15枚版）"""
    output_dir = "output/day6_follow_yoyaku"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル（インパクト重視）
    create_title_slide_two_line(
        "フォロワー1000人",
        "なのに",
        "予約ゼロ",
        "なぜ予約に繋がらない？",
        "CONVERSION",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. 状況
    create_content_slide([
        {"text": "投稿を頑張って", "size": "l"},
        {"text": "フォロワー1000人達成！", "size": "l"},
        {"text": ""},
        {"text": "...でも予約が来ない", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 共感
    create_content_slide([
        {"text": "「なんで？」", "size": "xl"},
        {"text": ""},
        {"text": "いいね！はもらえる", "size": "m"},
        {"text": "保存もされてる", "size": "m"},
        {"text": ""},
        {"text": "でも予約には繋がらない...", "size": "m"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 心理学
    create_content_slide([
        {"text": "心理学的に言うと", "size": "l"},
        {"text": ""},
        {"text": "「興味」と「行動」の間には", "size": "m"},
        {"text": "大きな壁がある", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "その壁を越えさせる設計が必要", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. 壁①
    create_content_slide([
        {"text": "壁①", "size": "l"},
        {"text": ""},
        {"text": "「この人に頼む理由」", "size": "xl"},
        {"text": "がない", "size": "xl"},
        {"text": ""},
        {"text": "上手そう。でも他との違いは？", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # 6. 壁②
    create_content_slide([
        {"text": "壁②", "size": "l"},
        {"text": ""},
        {"text": "料金・場所が", "size": "xl"},
        {"text": "わからない", "size": "xl"},
        {"text": ""},
        {"text": "調べるのが面倒 → 離脱", "size": "m"},
    ], f"{output_dir}/slide_06.png")
    
    # 7. 壁③
    create_content_slide([
        {"text": "壁③", "size": "l"},
        {"text": ""},
        {"text": "予約方法が", "size": "xl"},
        {"text": "わからない", "size": "xl"},
        {"text": ""},
        {"text": "リンクどこ？ → 離脱", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_07.png")
    
    # 8. 転換
    create_vertical_text_slide("導線", "壁を壊す設計をせよ", f"{output_dir}/slide_08.png")
    
    # 9. 解決策①
    create_content_slide([
        {"text": "解決策①", "size": "l"},
        {"text": ""},
        {"text": "差別化ポイントを明記", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「髪質改善専門」", "size": "m"},
        {"text": "「ショートカット特化」など", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # 10. 解決策②
    create_content_slide([
        {"text": "解決策②", "size": "l"},
        {"text": ""},
        {"text": "料金をプロフィールに", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「カット ¥6,000〜」", "size": "m"},
        {"text": "「カラー ¥8,000〜」など明記", "size": "m"},
    ], f"{output_dir}/slide_10.png")
    
    # 11. 解決策③
    create_content_slide([
        {"text": "解決策③", "size": "l"},
        {"text": ""},
        {"text": "予約リンクを目立たせる", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "プロフィールに1クリック導線", "size": "m"},
        {"text": "ストーリーズにリンクステッカー", "size": "m"},
    ], f"{output_dir}/slide_11.png")
    
    # 12. 具体例
    create_content_slide([
        {"text": "良いプロフィール例", "size": "l"},
        {"text": ""},
        {"text": "✅ 髪質改善専門 / 西尾市", "size": "m"},
        {"text": "✅ カット¥6,000〜", "size": "m"},
        {"text": "✅ 予約はリンクから👇", "size": "m"},
        {"text": ""},
        {"text": "3秒で全部わかる！", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_12.png")
    
    # 13. Before/After
    create_content_slide([
        {"text": "Before → After", "size": "l"},
        {"text": ""},
        {"text": "❌ 「美容師やってます」", "size": "m"},
        {"text": "→ 誰でも言える", "size": "m"},
        {"text": ""},
        {"text": "⭕️ 「髪質改善で指名No.1」", "size": "m"},
        {"text": "→ 専門性が伝わる", "size": "m"},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "予約されるには", "size": "l"},
        {"text": ""},
        {"text": "① 差別化ポイント明記", "size": "m"},
        {"text": "② 料金・場所を見せる", "size": "m"},
        {"text": "③ 予約導線を整える", "size": "m"},
        {"text": ""},
        {"text": "「興味→行動」の壁を壊す", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["プロフィール見直す", "料金を明記する", "予約リンク整備する"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ Day 6 complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_day7():
    """Day 7: 帰り際で決まるリピート（15枚版）"""
    output_dir = "output/day7_last_5min"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル（Day 6スタイル）
    create_title_slide_two_line(
        "施術は完璧だったのに",
        "",
        "リピートゼロ",
        "なぜ次に繋がらない？",
        "REPEAT",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. 状況
    create_content_slide([
        {"text": "カット上手くいった", "size": "l"},
        {"text": "カラーも綺麗に入った", "size": "l"},
        {"text": ""},
        {"text": "...でも2回目が来ない", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 共感
    create_content_slide([
        {"text": "「なんで？」", "size": "xl"},
        {"text": ""},
        {"text": "技術は褒められた", "size": "m"},
        {"text": "「また来ます」と言われた", "size": "m"},
        {"text": ""},
        {"text": "なのに2回目が来ない...", "size": "m"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 答え
    create_content_slide([
        {"text": "実は...", "size": "l"},
        {"text": ""},
        {"text": "人は「最後の印象」で", "size": "m"},
        {"text": "全体を評価する", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "帰り際が全てを決める", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. 具体例（悪い例）
    create_content_slide([
        {"text": "よくあるNG", "size": "l"},
        {"text": ""},
        {"text": "施術終了", "size": "m"},
        {"text": "↓", "size": "m"},
        {"text": "「ありがとうございました〜」", "size": "m"},
        {"text": "↓", "size": "m"},
        {"text": "終わり（それだけ？）", "size": "xl"},
    ], f"{output_dir}/slide_05.png")
    
    # 6. 問題点
    create_content_slide([
        {"text": "これだと...", "size": "l"},
        {"text": ""},
        {"text": "印象に残らない", "size": "m"},
        {"text": "「誰でもいい」になる", "size": "m"},
        {"text": ""},
        {"text": "結果：リピートなし", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_06.png")
    
    # 7. 転換
    create_vertical_text_slide("帰り際", "最後の5分が勝負", f"{output_dir}/slide_07.png")
    
    # 8. ポイント①
    create_content_slide([
        {"text": "ポイント①", "size": "l"},
        {"text": ""},
        {"text": "個人的な一言を添える", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「今日のスタイル似合ってます」", "size": "m"},
        {"text": "「〇〇楽しんできてくださいね」", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # 9. ポイント②
    create_content_slide([
        {"text": "ポイント②", "size": "l"},
        {"text": ""},
        {"text": "次回を提案する", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「〇週間後くらいが」", "size": "m"},
        {"text": "「ベストタイミングですよ」", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # 10. ポイント③
    create_content_slide([
        {"text": "ポイント③", "size": "l"},
        {"text": ""},
        {"text": "「また会いたい」を伝える", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「次も担当させてください」", "size": "m"},
        {"text": "「変化見せてくださいね」", "size": "m"},
    ], f"{output_dir}/slide_10.png")
    
    # 11. Before/After
    create_content_slide([
        {"text": "帰り際の比較", "size": "l"},
        {"text": ""},
        {"text": "❌「ありがとうございました」", "size": "m"},
        {"text": "→ 印象に残らない", "size": "m"},
        {"text": ""},
        {"text": "⭕️「〇〇楽しんできてね！」", "size": "m"},
        {"text": "→ 心に残る", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_11.png")
    
    # 12. 効果
    create_content_slide([
        {"text": "すると...", "size": "l"},
        {"text": ""},
        {"text": "「あの人良かったな」", "size": "m"},
        {"text": "「また行きたいな」", "size": "m"},
        {"text": ""},
        {"text": "自然とリピートに繋がる", "size": "xl"},
    ], f"{output_dir}/slide_12.png")
    
    # 13. シンプルルール
    create_content_slide([
        {"text": "シンプルルール", "size": "l"},
        {"text": ""},
        {"text": "帰り際に", "size": "m"},
        {"text": "「この人だから」と思わせる", "size": "m"},
        {"text": "一言を添える", "size": "m"},
        {"text": ""},
        {"text": "それだけでOK", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "まとめ", "size": "l"},
        {"text": ""},
        {"text": "① 個人的な一言を添える", "size": "m"},
        {"text": "② 次回を提案する", "size": "m"},
        {"text": "③ 「また会いたい」を伝える", "size": "m"},
        {"text": ""},
        {"text": "帰り際が全てを決める", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["帰り際に一言添える", "次回提案する", "「また会いたい」を伝える"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ Day 7 complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_day8():
    """Day 8: 値上げできない心理（損失回避）- 15枚版"""
    output_dir = "output/day8_neage"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル
    create_title_slide(
        "3年間値上げできなかった,本当の理由",
        "損失回避の心理学",
        "PRICING PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. ストーリー開始
    create_content_slide([
        {"text": "ある美容師の話", "size": "l"},
        {"text": ""},
        {"text": "技術には自信があった", "size": "m"},
        {"text": "リピーターも多かった", "size": "m"},
        {"text": ""},
        {"text": "でも3年間、値上げできなかった", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 心情
    create_content_slide([
        {"text": "心の中では...", "size": "l"},
        {"text": ""},
        {"text": "「値上げしたらお客様が離れる」", "size": "m"},
        {"text": "「今のお客様に申し訳ない」", "size": "m"},
        {"text": "「他の店に行かれたら...」", "size": "m"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 心理学解説
    create_content_slide([
        {"text": "これは心理学で言う", "size": "l"},
        {"text": ""},
        {"text": "損失回避", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "人は「得る喜び」より", "size": "m"},
        {"text": "「失う痛み」を2倍強く感じる", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. 問題
    create_content_slide([
        {"text": "つまり...", "size": "l"},
        {"text": ""},
        {"text": "「お客様を失うかも」という", "size": "m"},
        {"text": "恐怖が大きすぎて", "size": "m"},
        {"text": ""},
        {"text": "行動できなくなる", "size": "xl"},
    ], f"{output_dir}/slide_05.png")
    
    # 6. 現実
    create_content_slide([
        {"text": "でも現実は...", "size": "l"},
        {"text": ""},
        {"text": "材料費は上がる", "size": "m"},
        {"text": "家賃も上がる", "size": "m"},
        {"text": "体力は落ちる", "size": "m"},
        {"text": ""},
        {"text": "利益は減り続ける", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")
    
    # 7. 転換点
    create_vertical_text_slide("転換", "ある日、気づいた", f"{output_dir}/slide_07.png")
    
    # 8. 気づき
    create_content_slide([
        {"text": "値上げしないことで", "size": "l"},
        {"text": ""},
        {"text": "失っているものがあった", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "時間、余裕、成長機会...", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # 9. 解決策①
    create_content_slide([
        {"text": "解決策①", "size": "l"},
        {"text": ""},
        {"text": "既存客には据え置き期間を設ける", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「〇月までは今の料金です」", "size": "m"},
        {"text": "安心感を与える", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # 10. 解決策②
    create_content_slide([
        {"text": "解決策②", "size": "l"},
        {"text": ""},
        {"text": "新規から新料金を適用", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "既存客への影響なし", "size": "m"},
        {"text": "徐々に単価が上がる", "size": "m"},
    ], f"{output_dir}/slide_10.png")
    
    # 11. 解決策③
    create_content_slide([
        {"text": "解決策③", "size": "l"},
        {"text": ""},
        {"text": "価値を伝えてから値上げ", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「技術向上のため」", "size": "m"},
        {"text": "「より良い薬剤導入のため」", "size": "m"},
    ], f"{output_dir}/slide_11.png")
    
    # 12. 結果
    create_content_slide([
        {"text": "結果...", "size": "l"},
        {"text": ""},
        {"text": "値上げしても", "size": "m"},
        {"text": "離れたのは2割だけ", "size": "xl"},
        {"text": ""},
        {"text": "しかも時間に余裕ができて", "size": "m"},
        {"text": "サービスの質が上がった", "size": "m"},
    ], f"{output_dir}/slide_12.png")
    
    # 13. 教訓
    create_content_slide([
        {"text": "教訓", "size": "l"},
        {"text": ""},
        {"text": "値上げを恐れて", "size": "m"},
        {"text": "自分を安売りし続けることが", "size": "m"},
        {"text": ""},
        {"text": "本当の損失", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "まとめ", "size": "l"},
        {"text": ""},
        {"text": "① 据え置き期間を設ける", "size": "m"},
        {"text": "② 新規から新料金を適用", "size": "m"},
        {"text": "③ 価値を伝えてから値上げ", "size": "m"},
        {"text": ""},
        {"text": "恐怖に負けず、一歩踏み出す", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["損失回避を理解する", "段階的に値上げする", "価値を伝える"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ Day 8 complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_day9():
    """Day 9: 丁寧すぎる接客が失客の原因（返報性の原理）- 15枚版"""
    output_dir = "output/day9_reciprocity"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル（疑問形）
    create_title_slide_two_line(
        "丁寧すぎる接客は",
        "失客",
        "する？",
        "良かれと思ってやってたことが...",
        "RECIPROCITY",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. ストーリー開始（タイトルの疑問を受けて）
    create_content_slide([
        {"text": "たとえばこんなこと", "size": "l"},
        {"text": "やってませんか？", "size": "l"},
        {"text": ""},
        {"text": "お茶菓子をサービス", "size": "m"},
        {"text": "マッサージを延長", "size": "m"},
        {"text": "おまけのトリートメント", "size": "m"},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 共感
    create_content_slide([
        {"text": "お客様のためを思って", "size": "l"},
        {"text": ""},
        {"text": "「喜んでくれるはず！」", "size": "xl"},
        {"text": ""},
        {"text": "そう思ってやってますよね", "size": "m"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 悲劇
    create_content_slide([
        {"text": "でも実は...", "size": "l"},
        {"text": ""},
        {"text": "笑顔で帰ったお客様が", "size": "m"},
        {"text": ""},
        {"text": "二度と来ない", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "こんな経験ありませんか？", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. 心理学解説
    create_content_slide([
        {"text": "心理学で言う", "size": "l"},
        {"text": ""},
        {"text": "返報性の原理", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "人は何かをもらうと", "size": "m"},
        {"text": "「お返ししなきゃ」と感じる", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # 6. 問題
    create_content_slide([
        {"text": "つまり...", "size": "l"},
        {"text": ""},
        {"text": "過剰なサービスは", "size": "m"},
        {"text": "お客様にとって", "size": "m"},
        {"text": "「心理的負債」になる", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_06.png")
    
    # 7. お客様の心理
    create_content_slide([
        {"text": "お客様の心理", "size": "l"},
        {"text": ""},
        {"text": "「こんなに良くしてもらって...」", "size": "m"},
        {"text": "「次は高いメニュー頼まなきゃ」", "size": "m"},
        {"text": "「手ぶらで行きづらい」", "size": "m"},
        {"text": ""},
        {"text": "→ 行くのが重荷になる", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")
    
    # 8. 転換
    create_vertical_text_slide("対等", "媚びるな、プロであれ", f"{output_dir}/slide_08.png")
    
    # 9. 解決策①
    create_content_slide([
        {"text": "解決策①", "size": "l"},
        {"text": ""},
        {"text": "特別扱いしすぎない", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "サービスは「さりげなく」", "size": "m"},
        {"text": "恩着せがましくしない", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # 10. 解決策②
    create_content_slide([
        {"text": "解決策②", "size": "l"},
        {"text": ""},
        {"text": "お返しをさせてあげる", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「口コミ書いてくださいね」", "size": "m"},
        {"text": "「お友達紹介してください」", "size": "m"},
        {"text": "頼みごとで負い目を消す", "size": "m"},
    ], f"{output_dir}/slide_10.png")
    
    # 11. 解決策③
    create_content_slide([
        {"text": "解決策③", "size": "l"},
        {"text": ""},
        {"text": "プロとして接する", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "お客様が欲しいのは", "size": "m"},
        {"text": "「おまけ」ではなく「結果」", "size": "m"},
    ], f"{output_dir}/slide_11.png")
    
    # 12. 効果
    create_content_slide([
        {"text": "意識を変えたら...", "size": "l"},
        {"text": ""},
        {"text": "お客様との関係が", "size": "m"},
        {"text": "フラットになった", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "リピート率も上がった", "size": "m"},
    ], f"{output_dir}/slide_12.png")
    
    # 13. 比較
    create_content_slide([
        {"text": "Before → After", "size": "l"},
        {"text": ""},
        {"text": "❌ 尽くしすぎる", "size": "m"},
        {"text": "→ 相手の負担になる", "size": "m"},
        {"text": ""},
        {"text": "⭕️ プロとして価値提供", "size": "m"},
        {"text": "→ 信頼される", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "まとめ", "size": "l"},
        {"text": ""},
        {"text": "① 特別扱いしすぎない", "size": "m"},
        {"text": "② 「お返し」の場を作る", "size": "m"},
        {"text": "③ 結果で満足させる", "size": "m"},
        {"text": ""},
        {"text": "「親切」と「重荷」は紙一重", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["サービスの量を見直す", "頼みごとをしてみる", "対等な関係を作る"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ Day 9 complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_day10():
    """Day 10: 新規で埋める負のループ（サンクコスト効果）- 15枚版"""
    output_dir = "output/day10_loop"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル
    create_title_slide(
        "新規集客に疲れた,あなたへ",
        "負のループから抜ける方法",
        "MARKETING TRAP",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. ストーリー開始
    create_content_slide([
        {"text": "毎月、新規を追いかける", "size": "l"},
        {"text": ""},
        {"text": "インスタ更新、広告出稿", "size": "m"},
        {"text": "クーポンで集客...", "size": "m"},
        {"text": ""},
        {"text": "正直、疲れた", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 共感
    create_content_slide([
        {"text": "でもやめられない", "size": "l"},
        {"text": ""},
        {"text": "「新規が来ないと売上が...」", "size": "m"},
        {"text": "「ここまでやってきたし...」", "size": "m"},
        {"text": ""},
        {"text": "止まれない焦り", "size": "xl"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 心理学解説
    create_content_slide([
        {"text": "これは心理学で言う", "size": "l"},
        {"text": ""},
        {"text": "サンクコスト効果", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「ここまでやったから」と", "size": "m"},
        {"text": "損切りできなくなる心理", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. 問題の本質
    create_content_slide([
        {"text": "問題の本質", "size": "l"},
        {"text": ""},
        {"text": "新規 → 1回で終わる", "size": "m"},
        {"text": "→ また新規が必要", "size": "m"},
        {"text": "→ 永遠に集客が必要", "size": "m"},
        {"text": ""},
        {"text": "負のループ", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_05.png")
    
    # 6. 数字で見る
    create_content_slide([
        {"text": "数字で見ると", "size": "l"},
        {"text": ""},
        {"text": "新規獲得コスト：5,000円", "size": "m"},
        {"text": "リピート獲得コスト：500円", "size": "m"},
        {"text": ""},
        {"text": "10倍の差がある", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_06.png")
    
    # 7. 転換
    create_vertical_text_slide("転換", "リピートにシフトせよ", f"{output_dir}/slide_07.png")
    
    # 8. 気づき
    create_content_slide([
        {"text": "ある日、計算してみた", "size": "l"},
        {"text": ""},
        {"text": "リピート率が10%上がれば", "size": "m"},
        {"text": "新規が半分でも", "size": "m"},
        {"text": ""},
        {"text": "売上は同じ", "size": "xl"},
    ], f"{output_dir}/slide_08.png")
    
    # 9. 解決策①
    create_content_slide([
        {"text": "解決策①", "size": "l"},
        {"text": ""},
        {"text": "新規集客の時間を", "size": "m"},
        {"text": "リピート施策に回す", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "LINEフォロー、次回予約など", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # 10. 解決策②
    create_content_slide([
        {"text": "解決策②", "size": "l"},
        {"text": ""},
        {"text": "来店後のフォローを強化", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "3日後に「調子どうですか？」", "size": "m"},
        {"text": "1ヶ月後に「そろそろいかがですか？」", "size": "m"},
    ], f"{output_dir}/slide_10.png")
    
    # 11. 解決策③
    create_content_slide([
        {"text": "解決策③", "size": "l"},
        {"text": ""},
        {"text": "「また来たい」理由を作る", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "次回限定メニュー", "size": "m"},
        {"text": "継続特典など", "size": "m"},
    ], f"{output_dir}/slide_11.png")
    
    # 12. 結果
    create_content_slide([
        {"text": "結果...", "size": "l"},
        {"text": ""},
        {"text": "新規集客を減らして", "size": "m"},
        {"text": "リピート施策に集中したら", "size": "m"},
        {"text": ""},
        {"text": "売上が上がった", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_12.png")
    
    # 13. 比較
    create_content_slide([
        {"text": "Before → After", "size": "l"},
        {"text": ""},
        {"text": "❌ 新規を追い続ける（疲弊）", "size": "m"},
        {"text": ""},
        {"text": "⭕️ リピートを増やす（安定）", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "まとめ", "size": "l"},
        {"text": ""},
        {"text": "① 新規集客の時間をリピートに", "size": "m"},
        {"text": "② 来店後フォローを強化", "size": "m"},
        {"text": "③ 「また来たい」理由を作る", "size": "m"},
        {"text": ""},
        {"text": "負のループから抜け出す", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["リピート施策を見直す", "フォローを強化する", "継続特典を作る"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ Day 10 complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_day11():
    """Day 11: 口コミが書かれない理由（社会的証明）- 15枚版"""
    output_dir = "output/day11_kuchikomi"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル
    create_title_slide_two_line(
        "口コミをお願いしても",
        "書いて",
        "くれない",
        "仕組み化で解決できます",
        "SOCIAL PROOF",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. ストーリー開始
    create_content_slide([
        {"text": "「口コミお願いしますね」", "size": "l"},
        {"text": ""},
        {"text": "お客様は笑顔で「はい！」", "size": "m"},
        {"text": ""},
        {"text": "...でも書いてくれない", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 共感
    create_content_slide([
        {"text": "「なぜ？」", "size": "xl"},
        {"text": ""},
        {"text": "満足してくれてたはず", "size": "m"},
        {"text": "嫌われてはいないはず", "size": "m"},
        {"text": ""},
        {"text": "なのになぜ書いてくれない...", "size": "m"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 心理学解説
    create_content_slide([
        {"text": "心理学で言う", "size": "l"},
        {"text": ""},
        {"text": "社会的証明", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "人は「他の人がやっていること」", "size": "m"},
        {"text": "を参考にして行動する", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. 問題
    create_content_slide([
        {"text": "つまり...", "size": "l"},
        {"text": ""},
        {"text": "「口コミ書いてね」だけでは", "size": "m"},
        {"text": "行動のきっかけがない", "size": "xl"},
        {"text": ""},
        {"text": "面倒だし、後回しになる", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # 6. お客様の心理
    create_content_slide([
        {"text": "お客様の心理", "size": "l"},
        {"text": ""},
        {"text": "「何を書けばいいかわからない」", "size": "m"},
        {"text": "「恥ずかしい」", "size": "m"},
        {"text": "「後でやろう（忘れる）」", "size": "m"},
        {"text": ""},
        {"text": "ハードルが高い", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_06.png")
    
    # 7. 転換
    create_vertical_text_slide("転換", "お願いの仕方を変える", f"{output_dir}/slide_07.png")
    
    # 8. 解決策①
    create_content_slide([
        {"text": "解決策①", "size": "l"},
        {"text": ""},
        {"text": "その場でQRコードを見せる", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「今ここで開いてみて」", "size": "m"},
        {"text": "「1分で終わりますよ」", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # 9. 解決策②
    create_content_slide([
        {"text": "解決策②", "size": "l"},
        {"text": ""},
        {"text": "何を書けばいいか伝える", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「今日の〇〇について」", "size": "m"},
        {"text": "「感想だけでOKですよ」", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # 10. 解決策③
    create_content_slide([
        {"text": "解決策③", "size": "l"},
        {"text": ""},
        {"text": "他の人の口コミを見せる", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「こんな感じで書いてくれてます」", "size": "m"},
        {"text": "参考があると書きやすい", "size": "m"},
    ], f"{output_dir}/slide_10.png")
    
    # 11. 解決ツール紹介
    create_content_slide([
        {"text": "でも正直...", "size": "l"},
        {"text": ""},
        {"text": "毎回お願いするのって", "size": "m"},
        {"text": "大変じゃないですか？", "size": "m"},
        {"text": ""},
        {"text": "仕組み化したい", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_11.png")
    
    # 12. ふえるん紹介（テキスト導入）
    create_content_slide([
        {"text": "そこで...", "size": "l"},
        {"text": ""},
        {"text": "口コミ獲得ツール", "size": "m"},
        {"text": "「ふえるん」", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "無料で使える", "size": "m"},
        {"text": "美容室でも導入が進んでいる", "size": "m"},
    ], f"{output_dir}/slide_12.png")
    
    # 13. ふえるんプロモ画像
    fuerun_img_path = "assets/fuerun_promo.jpg"
    try:
        fuerun_img = Image.open(fuerun_img_path)
        # 4:5フォーマットにリサイズ
        fuerun_img = fuerun_img.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
        fuerun_img.save(f"{output_dir}/slide_13.png", "PNG", quality=95)
        print(f"Saved: {output_dir}/slide_13.png")
    except Exception as e:
        print(f"Fuerun image not found: {e}")
        # フォールバック
        create_content_slide([
            {"text": "QRコードを見せるだけで", "size": "l"},
            {"text": ""},
            {"text": "良質な口コミが", "size": "m"},
            {"text": "どんどん増える", "size": "xl", "highlight": True},
        ], f"{output_dir}/slide_13.png")
    
    # 14. ふえるんの特徴（公式サイトより）
    create_content_slide([
        {"text": "ふえるんの強み", "size": "l"},
        {"text": ""},
        {"text": "✓ お客様の手間ゼロ", "size": "m"},
        {"text": "✓ 投稿率が劇的に向上", "size": "m"},
        {"text": "✓ 高品質な口コミが増える", "size": "m"},
        {"text": "✓ MEO対策で検索上位へ", "size": "m"},
    ], f"{output_dir}/slide_14.png")
    
    # 15. まとめ
    create_content_slide([
        {"text": "まとめ", "size": "l"},
        {"text": ""},
        {"text": "① 口コミはその場でお願い", "size": "m"},
        {"text": "② 「何を書くか」を伝える", "size": "m"},
        {"text": "③ 仕組み化で効率UP", "size": "m"},
        {"text": ""},
        {"text": "口コミ＝Google集客の武器", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_15.png")
    
    # 16. CTA（ふえるん誘導）
    create_cta_slide(
        "保存して振り返ってね",
        ["口コミの仕組み化に興味あれば", "「ふえるん」で検索", "無料で始められます"],
        "詳しくはキャプションで →",
        f"{output_dir}/slide_16.png"
    )
    
    print(f"\n✅ Day 11 complete! Check {output_dir}/ (16 slides)")
    return output_dir


def generate_day12():
    """Day 12: 罪悪感をとれるかが勝負 - 15枚版"""
    output_dir = "output/day12_shimei"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル
    create_title_slide_two_line(
        "単価を上げたいなら",
        "罪悪感",
        "をとれ",
        "お客様が払えない本当の理由",
        "GUILT FREE",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. 問題提起
    create_content_slide([
        {"text": "高単価メニューを勧めても", "size": "l"},
        {"text": ""},
        {"text": "「今日はいいです...」", "size": "xl"},
        {"text": ""},
        {"text": "と断られること、ありませんか？", "size": "m"},
    ], f"{output_dir}/slide_02.png")
    
    # 3. よくある誤解
    create_content_slide([
        {"text": "こう思ってませんか？", "size": "l"},
        {"text": ""},
        {"text": "「お金がないんだろう」", "size": "m"},
        {"text": "「価値が伝わってない」", "size": "m"},
        {"text": "「押し売りに思われた」", "size": "m"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 本当の理由
    create_content_slide([
        {"text": "実は違います", "size": "l"},
        {"text": ""},
        {"text": "お客様が断る本当の理由は", "size": "m"},
        {"text": ""},
        {"text": "罪悪感", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_04.png")
    
    # 5. 罪悪感の正体
    create_content_slide([
        {"text": "お客様の心理", "size": "l"},
        {"text": ""},
        {"text": "「自分にこんなにお金かけていいの？」", "size": "m"},
        {"text": "「家族に悪い...」", "size": "m"},
        {"text": "「贅沢すぎるかな...」", "size": "m"},
        {"text": ""},
        {"text": "自分を後回しにする思考", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_05.png")
    
    # 6. 特に多いのは
    create_content_slide([
        {"text": "特に多いのは", "size": "l"},
        {"text": ""},
        {"text": "子育て中のママ", "size": "m"},
        {"text": "働く女性", "size": "m"},
        {"text": ""},
        {"text": "「自分より家族優先」が染み付いている", "size": "m"},
    ], f"{output_dir}/slide_06.png")
    
    # 7. 転換
    create_vertical_text_slide("許可", "自分にOKを出させる", f"{output_dir}/slide_07.png")
    
    # 8. 解決策の方向性
    create_content_slide([
        {"text": "売るのではなく", "size": "l"},
        {"text": ""},
        {"text": "「自分にお金をかけていい」", "size": "m"},
        {"text": "という許可を与える", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_08.png")
    
    # 9. 具体策①
    create_content_slide([
        {"text": "罪悪感を消す①", "size": "l"},
        {"text": ""},
        {"text": "「ご褒美」という言葉を使う", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「頑張ってる自分へのご褒美に」", "size": "m"},
        {"text": "自分を甘やかす正当化を提供", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # 10. 具体策②
    create_content_slide([
        {"text": "罪悪感を消す②", "size": "l"},
        {"text": ""},
        {"text": "「投資」として伝える", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「綺麗でいることは仕事にもプラス」", "size": "m"},
        {"text": "「自信につながる」", "size": "m"},
    ], f"{output_dir}/slide_10.png")
    
    # 11. 具体策③
    create_content_slide([
        {"text": "罪悪感を消す③", "size": "l"},
        {"text": ""},
        {"text": "「周りのため」に変換", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「ママが綺麗だと子供も嬉しい」", "size": "m"},
        {"text": "「家族のためにも自分を大切に」", "size": "m"},
    ], f"{output_dir}/slide_11.png")
    
    # 12. 効果
    create_content_slide([
        {"text": "すると...", "size": "l"},
        {"text": ""},
        {"text": "「じゃあ、やってみようかな」", "size": "xl"},
        {"text": ""},
        {"text": "気持ちよく払ってもらえる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_12.png")
    
    # 13. 比較
    create_content_slide([
        {"text": "Before → After", "size": "l"},
        {"text": ""},
        {"text": "❌「このメニューおすすめです」", "size": "m"},
        {"text": "→ 罪悪感で断られる", "size": "m"},
        {"text": ""},
        {"text": "⭕️「頑張ってるご褒美に」", "size": "m"},
        {"text": "→ 許可が出て受け入れる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "まとめ", "size": "l"},
        {"text": ""},
        {"text": "① 断られる理由は「罪悪感」", "size": "m"},
        {"text": "② 自分にOKを出す許可を与える", "size": "m"},
        {"text": "③ ご褒美・投資・周りのためで変換", "size": "m"},
        {"text": ""},
        {"text": "罪悪感をとれるかが勝負", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["断られた理由を振り返る", "「ご褒美」を使ってみる", "許可を与える提案を"],
        "詳しくはキャプションで →",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ Day 12 complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_day13():
    """Day 13: お客さんの本音を知る方法 - 15枚版"""
    output_dir = "output/day13_honne"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル
    create_title_slide_two_line(
        "お客さんの",
        "本音",
        "を知る方法",
        "「良かったです」を信じるな",
        "TRUE INSIGHT",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. 問題提起
    create_content_slide([
        {"text": "施術後に聞いてみた", "size": "l"},
        {"text": ""},
        {"text": "「今日いかがでしたか？」", "size": "xl"},
        {"text": ""},
        {"text": "「良かったです！」", "size": "m"},
    ], f"{output_dir}/slide_02.png")
    
    # 3. でも...
    create_content_slide([
        {"text": "でも...", "size": "l"},
        {"text": ""},
        {"text": "そのお客様", "size": "m"},
        {"text": "二度と来なかった", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_03.png")
    
    # 4. なぜ？
    create_content_slide([
        {"text": "なぜ？", "size": "l"},
        {"text": ""},
        {"text": "「良かったって言ってたのに...」", "size": "m"},
        {"text": ""},
        {"text": "実は、感想は嘘をつく", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_04.png")
    
    # 5. お客様の心理
    create_content_slide([
        {"text": "お客様の心理", "size": "l"},
        {"text": ""},
        {"text": "「微妙だった...」", "size": "m"},
        {"text": "「でも目の前で言えない」", "size": "m"},
        {"text": "「波風立てたくない」", "size": "m"},
        {"text": ""},
        {"text": "社交辞令で「良かった」と言う", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_05.png")
    
    # 6. 衝撃の事実
    create_content_slide([
        {"text": "衝撃の事実", "size": "l"},
        {"text": ""},
        {"text": "アンケートで「満足」と答えた人の", "size": "m"},
        {"text": ""},
        {"text": "40%はリピートしない", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_06.png")
    
    # 7. 転換
    create_vertical_text_slide("行動", "言葉より行動を見ろ", f"{output_dir}/slide_07.png")
    
    # 8. 本当の答え
    create_content_slide([
        {"text": "本音を知る方法", "size": "l"},
        {"text": ""},
        {"text": "感想を聞くのではなく", "size": "m"},
        {"text": "行動を見る", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_08.png")
    
    # 9. 見るべき行動①
    create_content_slide([
        {"text": "見るべき行動①", "size": "l"},
        {"text": ""},
        {"text": "施術中のスマホ率", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "スマホばかり見てる → 退屈", "size": "m"},
        {"text": "鏡を見てる → 興味あり", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # 10. 見るべき行動②
    create_content_slide([
        {"text": "見るべき行動②", "size": "l"},
        {"text": ""},
        {"text": "帰り際のスピード", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "ゆっくり帰る → 居心地が良い", "size": "m"},
        {"text": "すぐ出る → 早く帰りたかった", "size": "m"},
    ], f"{output_dir}/slide_10.png")
    
    # 11. 見るべき行動③
    create_content_slide([
        {"text": "見るべき行動③", "size": "l"},
        {"text": ""},
        {"text": "会計時に商品を見るか", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "見てる → 信頼してる", "size": "m"},
        {"text": "見ない → まだ距離がある", "size": "m"},
    ], f"{output_dir}/slide_11.png")
    
    # 12. まとめの前に
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "言葉は嘘をつく", "size": "m"},
        {"text": "行動は嘘をつかない", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_12.png")
    
    # 13. 比較
    create_content_slide([
        {"text": "Before → After", "size": "l"},
        {"text": ""},
        {"text": "❌「いかがでしたか？」と聞く", "size": "m"},
        {"text": "→ 社交辞令をもらう", "size": "m"},
        {"text": ""},
        {"text": "⭕️ 行動データを見る", "size": "m"},
        {"text": "→ 本音がわかる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "まとめ", "size": "l"},
        {"text": ""},
        {"text": "① 感想より行動を見る", "size": "m"},
        {"text": "② スマホ率・帰り際・商品を見るか", "size": "m"},
        {"text": "③ 言葉を鵜呑みにしない", "size": "m"},
        {"text": ""},
        {"text": "行動こそが本音", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["施術中の様子を観察", "帰り際の態度をチェック", "商品への関心を見る"],
        "詳しくはキャプションで →",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ Day 13 complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_day14():
    """Day 14: インスタで反応がない本当の理由 - 15枚版"""
    output_dir = "output/day14_copy"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル（驚き＋疑問）
    create_title_slide_two_line(
        "インスタ頑張ってるのに",
        "反応が",
        "ない理由",
        "コピーの本質を教えます",
        "COPY WRITING",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. 問題提起
    create_content_slide([
        {"text": "毎日投稿してる", "size": "l"},
        {"text": ""},
        {"text": "写真も綺麗", "size": "m"},
        {"text": "ハッシュタグもつけてる", "size": "m"},
        {"text": ""},
        {"text": "でも「いいね」も予約も増えない", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. よくある間違い
    create_content_slide([
        {"text": "こう思ってませんか？", "size": "l"},
        {"text": ""},
        {"text": "「もっと映える写真を...」", "size": "m"},
        {"text": "「投稿頻度を増やそう...」", "size": "m"},
        {"text": "「リール作らなきゃ...」", "size": "m"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 本当の問題
    create_content_slide([
        {"text": "実は違います", "size": "l"},
        {"text": ""},
        {"text": "問題は「コピー」です", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "文章が刺さってない", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. コピーの本質
    create_content_slide([
        {"text": "コピーの本質とは", "size": "l"},
        {"text": ""},
        {"text": "見込み客の心にある", "size": "m"},
        {"text": "不満や願望を", "size": "m"},
        {"text": ""},
        {"text": "言葉に翻訳すること", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_05.png")
    
    # 6. 重要な気づき
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "「伝えたいこと」を書くな", "size": "m"},
        {"text": ""},
        {"text": "「お客様が思ってること」を書け", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_06.png")
    
    # 7. 転換
    create_vertical_text_slide("翻訳", "心の声を言葉にしろ", f"{output_dir}/slide_07.png")
    
    # 8. 例：NG
    create_content_slide([
        {"text": "❌ ダメな例", "size": "l"},
        {"text": ""},
        {"text": "「当店自慢のカラー技術」", "size": "m"},
        {"text": "「丁寧なカウンセリング」", "size": "m"},
        {"text": "「駅近で便利」", "size": "m"},
        {"text": ""},
        {"text": "→ 店側の都合", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_08.png")
    
    # 9. 例：OK
    create_content_slide([
        {"text": "⭕️ 良い例", "size": "l"},
        {"text": ""},
        {"text": "「また失敗するの怖い...」", "size": "m"},
        {"text": "「本当の髪の悩み、言えてる？」", "size": "m"},
        {"text": "「忙しくても綺麗でいたい」", "size": "m"},
        {"text": ""},
        {"text": "→ お客様の心の声", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_09.png")
    
    # 10. なぜ効くのか
    create_content_slide([
        {"text": "なぜ刺さるのか？", "size": "l"},
        {"text": ""},
        {"text": "「わかってくれてる」", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "と感じるから", "size": "m"},
        {"text": "信頼が生まれる", "size": "m"},
    ], f"{output_dir}/slide_10.png")
    
    # 11. どうやって見つける？
    create_content_slide([
        {"text": "心の声の見つけ方", "size": "l"},
        {"text": ""},
        {"text": "① 口コミを読む", "size": "m"},
        {"text": "② カウンセリングで聞いた言葉", "size": "m"},
        {"text": "③ お客様の愚痴", "size": "m"},
        {"text": ""},
        {"text": "全部「使える言葉」の宝庫", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_11.png")
    
    # 12. まとめ前
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "コピーは「作る」ものじゃない", "size": "m"},
        {"text": ""},
        {"text": "「翻訳する」もの", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_12.png")
    
    # 13. 比較
    create_content_slide([
        {"text": "Before → After", "size": "l"},
        {"text": ""},
        {"text": "❌ 自分が言いたいことを書く", "size": "m"},
        {"text": "→ 反応なし", "size": "m"},
        {"text": ""},
        {"text": "⭕️ お客様の心の声を書く", "size": "m"},
        {"text": "→ 「これ私だ」と思われる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "まとめ", "size": "l"},
        {"text": ""},
        {"text": "① コピーは「翻訳」", "size": "m"},
        {"text": "② お客様の不満・願望を言葉に", "size": "m"},
        {"text": "③ 口コミ・カウンセリングがヒント", "size": "m"},
        {"text": ""},
        {"text": "心の声を代弁せよ", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["口コミを読み返す", "カウンセリングの言葉をメモ", "お客様目線で書き直す"],
        "詳しくはキャプションで →",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ Day 14 complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_day15():
    """Day 15: インスタで選ばれない理由（認知バイアス）- 15枚版"""
    output_dir = "output/day15_insta"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル
    create_title_slide_two_line(
        "投稿を変えただけで",
        "予約が",
        "3倍になった話",
        "なぜ見てるのに予約しない？",
        "COGNITIVE BIAS",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. ストーリー開始
    create_content_slide([
        {"text": "毎日投稿してるのに", "size": "l"},
        {"text": ""},
        {"text": "いいね!は増えた", "size": "m"},
        {"text": "保存も増えた", "size": "m"},
        {"text": ""},
        {"text": "でも予約が来ない", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 悩み
    create_content_slide([
        {"text": "「何が足りない？」", "size": "l"},
        {"text": ""},
        {"text": "ビフォーアフターも載せてる", "size": "m"},
        {"text": "プロフィールも整えた", "size": "m"},
        {"text": ""},
        {"text": "なのになぜ...", "size": "xl"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 心理学解説
    create_content_slide([
        {"text": "心理学で言う", "size": "l"},
        {"text": ""},
        {"text": "認知バイアス", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "人は自分に都合よく", "size": "m"},
        {"text": "情報を解釈する", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. 問題
    create_content_slide([
        {"text": "つまり...", "size": "l"},
        {"text": ""},
        {"text": "「上手いね」は伝わっても", "size": "m"},
        {"text": "「私に合う」は伝わらない", "size": "xl"},
        {"text": ""},
        {"text": "自分ごとにならない", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # 6. お客様の心理
    create_content_slide([
        {"text": "見てる人の心理", "size": "l"},
        {"text": ""},
        {"text": "「このモデルさんは可愛いけど」", "size": "m"},
        {"text": "「私とは髪質が違うし...」", "size": "m"},
        {"text": "「私には無理かも」", "size": "m"},
        {"text": ""},
        {"text": "自分には当てはまらないと思う", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_06.png")
    
    # 7. 転換
    create_vertical_text_slide("共感", "「私も」を作れ", f"{output_dir}/slide_07.png")
    
    # 8. 解決策①
    create_content_slide([
        {"text": "解決策①", "size": "l"},
        {"text": ""},
        {"text": "悩みを具体的に書く", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「広がりが気になる方に」", "size": "m"},
        {"text": "「白髪が増えてきた方に」", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # 9. 解決策②
    create_content_slide([
        {"text": "解決策②", "size": "l"},
        {"text": ""},
        {"text": "お客様の声を載せる", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「同じ悩みの人がいた」", "size": "m"},
        {"text": "「この人で解決できたんだ」", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # 10. 解決策③
    create_content_slide([
        {"text": "解決策③", "size": "l"},
        {"text": ""},
        {"text": "ターゲットを絞る", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「30代の髪質改善専門」", "size": "m"},
        {"text": "「ショートが得意」", "size": "m"},
    ], f"{output_dir}/slide_10.png")
    
    # 11. 効果
    create_content_slide([
        {"text": "投稿を変えたら...", "size": "l"},
        {"text": ""},
        {"text": "「私のことだ！」と", "size": "m"},
        {"text": "思ってもらえるように", "size": "m"},
        {"text": ""},
        {"text": "予約が3倍に", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_11.png")
    
    # 12. 重要ポイント
    create_content_slide([
        {"text": "重要なのは", "size": "l"},
        {"text": ""},
        {"text": "「上手い」を見せるのではなく", "size": "m"},
        {"text": ""},
        {"text": "「私に合う」を見せる", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_12.png")
    
    # 13. 比較
    create_content_slide([
        {"text": "Before → After", "size": "l"},
        {"text": ""},
        {"text": "❌ 「こんなに綺麗に」", "size": "m"},
        {"text": "→ 他人事", "size": "m"},
        {"text": ""},
        {"text": "⭕️ 「広がり悩んでた方が」", "size": "m"},
        {"text": "→ 自分ごと", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "まとめ", "size": "l"},
        {"text": ""},
        {"text": "① 悩みを具体的に書く", "size": "m"},
        {"text": "② お客様の声を載せる", "size": "m"},
        {"text": "③ ターゲットを絞る", "size": "m"},
        {"text": ""},
        {"text": "「私のことだ」を作る", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["悩みを具体的に書く", "お客様の声を載せる", "ターゲットを絞る"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ Day 15 complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_hp_cost():
    """美容室HPコスト最適化 - 毎月10,000円の無駄を省く提案（15枚版）"""
    output_dir = "output/hp_cost"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル - 衝撃的な事実（テキストが横幅に収まるよう短く）
    create_title_slide_two_line(
        "毎月のHP代",
        "高く",
        "ない？",
        "月1万円払ってるなら要注意",
        "HP COST",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. 共感 - 現状の問題提起
    create_content_slide([
        {"text": "外部業者に依頼して", "size": "l"},
        {"text": "ホームページを作った", "size": "l"},
        {"text": ""},
        {"text": "毎月の運用コストが", "size": "m"},
        {"text": "10,000円以上かかっている", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 問題の深掘り
    create_content_slide([
        {"text": "だけど...", "size": "l"},
        {"text": ""},
        {"text": "ホームページからの", "size": "m"},
        {"text": "予約ってほとんど来ない", "size": "xl"},
        {"text": ""},
        {"text": "こんな経験ありませんか？", "size": "m"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 現実
    create_content_slide([
        {"text": "年間にすると...", "size": "l"},
        {"text": ""},
        {"text": "12万円以上の", "size": "m"},
        {"text": "固定費になっている", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "効果がないのに払い続けている", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. 疑問
    create_content_slide([
        {"text": "「でも解約できない」", "size": "l"},
        {"text": ""},
        {"text": "「自分で作れないし...」", "size": "m"},
        {"text": "「業者に頼むしかない」", "size": "m"},
        {"text": ""},
        {"text": "本当にそうでしょうか？", "size": "xl"},
    ], f"{output_dir}/slide_05.png")
    
    # 6. 転換点
    create_vertical_text_slide("変化", "時代は変わった", f"{output_dir}/slide_06.png")
    
    # 7. 今の時代
    create_content_slide([
        {"text": "2026年の現実", "size": "l"},
        {"text": ""},
        {"text": "ホームページは", "size": "m"},
        {"text": "低コストで作れる時代", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "しかもAI機能付きで", "size": "m"},
    ], f"{output_dir}/slide_07.png")
    
    # 8. 具体的なメリット①
    create_content_slide([
        {"text": "メリット①", "size": "l"},
        {"text": ""},
        {"text": "月額運用コスト", "size": "m"},
        {"text": "数千円で済む", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "年間10万円以上の経費削減", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # 9. 具体的なメリット②
    create_content_slide([
        {"text": "メリット②", "size": "l"},
        {"text": ""},
        {"text": "AI搭載で", "size": "m"},
        {"text": "24時間対応が可能", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "お客様の質問に自動で回答", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # 10. 具体的なメリット③
    create_content_slide([
        {"text": "メリット③", "size": "l"},
        {"text": ""},
        {"text": "予約につながる", "size": "m"},
        {"text": "設計が最初からできる", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "見た目だけでなく集客導線も", "size": "m"},
    ], f"{output_dir}/slide_10.png")
    
    # 11. 結果
    create_content_slide([
        {"text": "つまり...", "size": "l"},
        {"text": ""},
        {"text": "乗り換えるだけで", "size": "m"},
        {"text": "経費削減＋集客UP", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "一石二鳥の効果", "size": "m"},
    ], f"{output_dir}/slide_11.png")
    
    # 12. 緊急性
    create_content_slide([
        {"text": "重要なのは", "size": "l"},
        {"text": ""},
        {"text": "払い続けるほど", "size": "m"},
        {"text": "損が増えていく", "size": "xl"},
        {"text": ""},
        {"text": "早く乗り換えた方が得", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_12.png")
    
    # 13. 比較
    create_content_slide([
        {"text": "Before → After", "size": "l"},
        {"text": ""},
        {"text": "❌ 月10,000円以上", "size": "m"},
        {"text": "→ 集客効果なし", "size": "m"},
        {"text": ""},
        {"text": "⭕️ 月数千円", "size": "m"},
        {"text": "→ AI対応＋集客UP", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "まとめ", "size": "l"},
        {"text": ""},
        {"text": "① 今のHP代は高すぎる", "size": "m"},
        {"text": "② AI搭載HPが低コストで作れる", "size": "m"},
        {"text": "③ 経費削減と集客が同時に可能", "size": "m"},
        {"text": ""},
        {"text": "今すぐ見直しを", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["今のHP代を確認", "AI搭載HPを検討", "コスト削減を実現"],
        "詳しくはキャプションで →",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ HP Cost content complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_a1():
    """A-1: 「おまかせで」が増えた本当の理由（決断疲れ）"""
    output_dir = "output/a1_omakase"
    os.makedirs(output_dir, exist_ok=True)

    # 1. タイトル
    create_title_slide_two_line(
        "「おまかせで」が",
        "増えた",
        "本当の理由",
        "それは信頼不足じゃない",
        "SALON PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )

    # 2. 問題提起 — 美容師あるある
    create_content_slide([
        {"text": "最近「おまかせで」の", "size": "l"},
        {"text": "お客様、増えてない？", "size": "l"},
        {"text": ""},
        {"text": "信頼されてるから？", "size": "m"},
        {"text": ""},
        {"text": "実は違う", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")

    # 3. 導入 — サロン文脈で原因提示
    create_content_slide([
        {"text": "仕事・家事・育児...", "size": "l"},
        {"text": "来店時にはもう", "size": "l"},
        {"text": ""},
        {"text": "選ぶ力が残っていない", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "だから「おまかせ」になる", "size": "m"},
    ], f"{output_dir}/slide_03.png")

    # 4. ① メニュー提示は3つまで
    create_content_slide([
        {"text": "① メニューは3つまで", "size": "l"},
        {"text": ""},
        {"text": "「カット＋カラー＋トリートメント」", "size": "m"},
        {"text": "「カラーのみ」「カット＋カラー」", "size": "m"},
        {"text": ""},
        {"text": "多いと選べない、3つが最適", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_04.png")

    # 5. ② 人気順を伝える
    create_content_slide([
        {"text": "② 人気順を伝える", "size": "l"},
        {"text": ""},
        {"text": "「一番人気はこちらです」", "size": "m"},
        {"text": "「8割の方がこちらを選びます」", "size": "m"},
        {"text": ""},
        {"text": "この一言で迷いが消える", "size": "m"},
    ], f"{output_dir}/slide_05.png")

    # 6. ③ 迷ったらこちらから提案
    create_content_slide([
        {"text": "③ こちらから提案する", "size": "l"},
        {"text": ""},
        {"text": "「迷いますよね」", "size": "m"},
        {"text": "「今の髪ならこちらがおすすめ」", "size": "m"},
        {"text": ""},
        {"text": "先に動くと信頼が生まれる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")

    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "「おまかせ」は信頼ではなく", "size": "m"},
        {"text": "疲れて選べないサイン", "size": "m"},
        {"text": ""},
        {"text": "選ばせるな、導け", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")

    # 8. 具体事例
    create_example_slide(
        "assets/isometric/a1_example.png",
        "具体事例：カウンセリング",
        ["スタイリスト：", "「今日はカット＋カラー、カラーのみ、", "カット＋トリートメントの3つから", "お選びいただけます。", "一番人気はカット＋カラーです"],
        f"{output_dir}/slide_08.png"
    )

    # 9. 縦文字キーワード
    create_vertical_text_slide("導線", "選ばせるな、導け", f"{output_dir}/slide_09.png")

    # 10. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①メニューは3つまでに絞る", "②人気順を伝える", "③迷ったらこちらから提案"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_10.png"
    )

    print(f"\n✅ A-1 complete! Check {output_dir}/")
    return output_dir


def generate_a2():
    """A-2: 変化を嫌うのは性格ではなく脳の仕様（現状維持バイアス）"""
    output_dir = "output/a2_status_quo"
    os.makedirs(output_dir, exist_ok=True)

    # 1. タイトル — サロンの日常から入る
    create_title_slide_two_line(
        "「いつも通りで」の",
        "",
        "正体",
        "提案が通らない本当の理由",
        "SALON PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )

    # 2. 問題提起 — 美容師の日常あるある
    create_content_slide([
        {"text": "「いつも通りで」", "size": "l"},
        {"text": "「前と同じ感じで」", "size": "l"},
        {"text": ""},
        {"text": "せっかくの提案が", "size": "m"},
        {"text": "毎回スルーされる...", "size": "m"},
    ], f"{output_dir}/slide_02.png")

    # 3. 導入 — 原因をサロン視点で
    create_content_slide([
        {"text": "原因は「あなたの提案」", "size": "l"},
        {"text": "ではない", "size": "l"},
        {"text": ""},
        {"text": "人の脳は変化を", "size": "m"},
        {"text": "「リスク」と感じる仕組み", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_03.png")

    # 4. ① いきなり大きく変えない
    create_content_slide([
        {"text": "① いきなり変えない", "size": "l"},
        {"text": ""},
        {"text": "「バッサリ切りましょう」", "size": "m"},
        {"text": "「ガラッとイメチェン」", "size": "m"},
        {"text": ""},
        {"text": "これが一番断られる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_04.png")

    # 5. ② 小さな変化から提案する
    create_content_slide([
        {"text": "② 小さく提案する", "size": "l"},
        {"text": ""},
        {"text": "「前髪だけ少し変えません？」", "size": "m"},
        {"text": "「色味だけワントーン上げて」", "size": "m"},
        {"text": ""},
        {"text": "小さいYESが次のYESを生む", "size": "m"},
    ], f"{output_dir}/slide_05.png")

    # 6. ③ 安心材料を先に伝える
    create_content_slide([
        {"text": "③ 安心を先に伝える", "size": "l"},
        {"text": ""},
        {"text": "「合わなければ戻せます」", "size": "m"},
        {"text": "「似た髪質の方で好評です」", "size": "m"},
        {"text": ""},
        {"text": "逃げ道があると人は動ける", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")

    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "「いつも通りで」を変えるには", "size": "m"},
        {"text": ""},
        {"text": "大きく変えるな", "size": "m"},
        {"text": "小さく提案しろ", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")

    # 8. 具体事例
    create_example_slide(
        "assets/isometric/a2_example.png",
        "具体事例：スタイル提案",
        ["スタイリスト：", "「今日は前髪だけ少し", "軽くしてみませんか？", "合わなければ次回戻せますよ"],
        f"{output_dir}/slide_08.png"
    )

    # 9. 縦文字キーワード
    create_vertical_text_slide("提案", "小さく提案する", f"{output_dir}/slide_09.png")

    # 10. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①いきなり変えない", "②小さな変化から提案", "③安心材料を先に伝える"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_10.png"
    )

    print(f"\n✅ A-2 complete! Check {output_dir}/")
    return output_dir


def generate_a3():
    """A-3: 最初の金額が高いほど単価は上がる（アンカリング効果）"""
    output_dir = "output/a3_anchoring"
    os.makedirs(output_dir, exist_ok=True)

    # 1. タイトル — サロンの単価問題から入る
    create_title_slide_two_line(
        "単価を上げたいなら",
        "見せる",
        "順番",
        "",
        "SALON PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )

    # 2. 問題提起 — 美容師あるある
    create_content_slide([
        {"text": "「もう少し単価を上げたい」", "size": "l"},
        {"text": ""},
        {"text": "でもお客様に高いと思われたら", "size": "m"},
        {"text": "失客しそうで怖い...", "size": "m"},
    ], f"{output_dir}/slide_02.png")

    # 3. 導入 — メニュー提示順が鍵
    create_content_slide([
        {"text": "実は単価は", "size": "l"},
        {"text": "「技術」ではなく", "size": "l"},
        {"text": ""},
        {"text": "メニューの見せ方で変わる", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_03.png")

    # 4. ① 先に上位メニューを見せる
    create_content_slide([
        {"text": "① 上位メニューを先に出す", "size": "l"},
        {"text": ""},
        {"text": "最初に¥15,000のメニューを見せると", "size": "m"},
        {"text": "¥8,000が「お手頃」に見える", "size": "m"},
        {"text": ""},
        {"text": "最初の価格が基準になる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_04.png")

    # 5. ② 次に標準メニューを出す
    create_content_slide([
        {"text": "② 次に標準メニューを出す", "size": "l"},
        {"text": ""},
        {"text": "「こちらもおすすめです」", "size": "m"},
        {"text": "と自然に案内する", "size": "m"},
        {"text": ""},
        {"text": "比較対象があると選びやすい", "size": "m"},
    ], f"{output_dir}/slide_05.png")

    # 6. ③ 価格差の理由を言語化する
    create_content_slide([
        {"text": "③ 価格差の理由を伝える", "size": "l"},
        {"text": ""},
        {"text": "「上位はダメージケア付きです」", "size": "m"},
        {"text": "「こちらは持ちが1ヶ月違います」", "size": "m"},
        {"text": ""},
        {"text": "納得すると単価が上がる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")

    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "安いメニューから見せると", "size": "m"},
        {"text": "そこが基準になる", "size": "m"},
        {"text": ""},
        {"text": "高い方から見せろ", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")

    # 8. 具体事例
    create_example_slide(
        "assets/isometric/a3_example.png",
        "具体事例：メニュー提示",
        ["スタイリスト：", "「プレミアムカラー¥15,000は", "ダメージケア付きです。", "通常カラー¥8,000もございます。", "持ちが1ヶ月違います"],
        f"{output_dir}/slide_08.png"
    )

    # 9. 縦文字キーワード
    create_vertical_text_slide("順番", "見せる順番を変えろ", f"{output_dir}/slide_09.png")

    # 10. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①上位メニューを先に見せる", "②次に標準メニューを出す", "③価格差の理由を伝える"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_10.png"
    )

    print(f"\n✅ A-3 complete! Check {output_dir}/")
    return output_dir


def generate_a4():
    """A-4: 最後の5分が次回来店を決める（ピークエンドの法則）"""
    output_dir = "output/a4_peak_end"
    os.makedirs(output_dir, exist_ok=True)

    # 1. タイトル
    create_title_slide_two_line(
        "リピートされたいなら",
        "最後の",
        "5分",
        "",
        "SALON PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )

    # 2. 問題提起
    create_content_slide([
        {"text": "技術には自信がある", "size": "l"},
        {"text": ""},
        {"text": "なのに次回予約が入らない", "size": "l"},
        {"text": ""},
        {"text": "なぜ？", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")

    # 3. 導入
    create_content_slide([
        {"text": "人の記憶に残るのは", "size": "l"},
        {"text": "「途中」ではなく", "size": "l"},
        {"text": ""},
        {"text": "最後の体験", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "会計前の5分が全てを決める", "size": "m"},
    ], f"{output_dir}/slide_03.png")

    # 4. ① 仕上がりを一緒に確認する
    create_content_slide([
        {"text": "① 仕上がりを一緒に確認", "size": "l"},
        {"text": ""},
        {"text": "「後ろもこんな感じです」", "size": "m"},
        {"text": "「ここ、こだわりました」", "size": "m"},
        {"text": ""},
        {"text": "満足を言語化してあげる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_04.png")

    # 5. ② 次回の時期を伝える
    create_content_slide([
        {"text": "② 次回の目安を伝える", "size": "l"},
        {"text": ""},
        {"text": "「1ヶ月半後がベストです」", "size": "m"},
        {"text": "「根元が気になる前に」", "size": "m"},
        {"text": ""},
        {"text": "理由があると予約しやすい", "size": "m"},
    ], f"{output_dir}/slide_05.png")

    # 6. ③ 次回来店のメリットを一言
    create_content_slide([
        {"text": "③ 次回のメリットを添える", "size": "l"},
        {"text": ""},
        {"text": "「次回はカラーだけで", "size": "m"},
        {"text": "キレイに保てますよ」", "size": "m"},
        {"text": ""},
        {"text": "来る理由を作ってあげる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")

    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "技術が良くても", "size": "m"},
        {"text": "最後が雑だと記憶に残らない", "size": "m"},
        {"text": ""},
        {"text": "最後の5分に全力を注げ", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")

    # 8. 具体事例
    create_example_slide(
        "assets/isometric/a4_example.png",
        "具体事例：お見送り",
        ["スタイリスト：", "「今日のスタイル、すごくお似合いです。", "1ヶ月半後くらいに", "カラーだけで維持できますよ。", "ご予約入れておきますか？"],
        f"{output_dir}/slide_08.png"
    )

    # 9. 縦文字キーワード
    create_vertical_text_slide("最後", "最後の5分に全力を", f"{output_dir}/slide_09.png")

    # 10. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①仕上がりを一緒に確認する", "②次回の目安時期を伝える", "③来店メリットを一言添える"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_10.png"
    )

    print(f"\n✅ A-4 complete! Check {output_dir}/")
    return output_dir


def generate_a5():
    """A-5: 「人気です」の一言が不安を消す（社会的証明）"""
    output_dir = "output/a5_social_proof"
    os.makedirs(output_dir, exist_ok=True)

    # 1. タイトル（命令口調NG）
    create_title_slide_two_line(
        "迷うお客様に効く",
        "たった",
        "一言",
        "",
        "SALON PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )

    # 2. 問題提起
    create_content_slide([
        {"text": "「どれがいいですか？」", "size": "l"},
        {"text": ""},
        {"text": "メニューを見ても決められない", "size": "m"},
        {"text": "お客様、増えてない？", "size": "m"},
    ], f"{output_dir}/slide_02.png")

    # 3. 導入
    create_content_slide([
        {"text": "人が迷ったときに", "size": "l"},
        {"text": "頼るのは", "size": "l"},
        {"text": ""},
        {"text": "「みんなの選択」", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "これが社会的証明", "size": "m"},
    ], f"{output_dir}/slide_03.png")

    # 4. ① 一番人気を明示する
    create_content_slide([
        {"text": "① 一番人気を伝える", "size": "l"},
        {"text": ""},
        {"text": "「一番人気はこちらです」", "size": "m"},
        {"text": ""},
        {"text": "たったこの一言で", "size": "m"},
        {"text": "迷いが消える", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_04.png")

    # 5. ② 実例を短く添える
    create_content_slide([
        {"text": "② 実例を短く添える", "size": "l"},
        {"text": ""},
        {"text": "「同じ髪質の方に好評です」", "size": "m"},
        {"text": "「先週も3名選ばれました」", "size": "m"},
        {"text": ""},
        {"text": "自分と似た人の実例が効く", "size": "m"},
    ], f"{output_dir}/slide_05.png")

    # 6. ③ 数字で根拠を出す
    create_content_slide([
        {"text": "③ 数字で伝える", "size": "l"},
        {"text": ""},
        {"text": "「リピート率80%のメニューです」", "size": "m"},
        {"text": "「月50名が選んでいます」", "size": "m"},
        {"text": ""},
        {"text": "数字があると安心できる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")

    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "迷うお客様に必要なのは", "size": "m"},
        {"text": "説得ではなく", "size": "m"},
        {"text": ""},
        {"text": "「みんな選んでますよ」", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")

    # 8. 具体事例
    create_example_slide(
        "assets/isometric/a5_example.png",
        "具体事例：メニュー案内",
        ["スタイリスト：", "「このトリートメント、", "同じ髪質の方にすごく好評で", "リピート率80%なんです。", "一番人気ですよ"],
        f"{output_dir}/slide_08.png"
    )

    # 9. 縦文字キーワード
    create_vertical_text_slide("人気", "人気の力を借りる", f"{output_dir}/slide_09.png")

    # 10. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①一番人気を伝える", "②実例を短く添える", "③数字で根拠を出す"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_10.png"
    )

    print(f"\n✅ A-5 complete! Check {output_dir}/")
    return output_dir


def generate_b1():
    """B-1: 保存ボタンの正体は「後で見る」ではない（自己効力感）"""
    output_dir = "output/b1_save_identity"
    os.makedirs(output_dir, exist_ok=True)

    # 1. タイトル
    create_title_slide_two_line(
        "保存ボタンの",
        "",
        "正体",
        "「後で見る」じゃない",
        "SNS PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )

    # 2. 問題提起
    create_content_slide([
        {"text": "投稿を頑張っている", "size": "l"},
        {"text": ""},
        {"text": "いいねは来る", "size": "m"},
        {"text": "でも保存がつかない", "size": "m"},
        {"text": ""},
        {"text": "なぜ？", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")

    # 3. 導入
    create_content_slide([
        {"text": "保存の正体は", "size": "l"},
        {"text": "「後で見る」ではなく", "size": "l"},
        {"text": ""},
        {"text": "「価値ある情報を\n見つけた自分」の証明", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_03.png")

    # 4. ① 使える知識を入れる
    create_content_slide([
        {"text": "① 使える知識を入れる", "size": "l"},
        {"text": ""},
        {"text": "「明日から試せる」情報は", "size": "m"},
        {"text": "「取っておきたい」に変わる", "size": "m"},
        {"text": ""},
        {"text": "実務で使えるかが鍵", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_04.png")

    # 5. ② 話したくなる知識を入れる
    create_content_slide([
        {"text": "② 話したくなる知識", "size": "l"},
        {"text": ""},
        {"text": "「知ってた？実は…」", "size": "m"},
        {"text": "と人に話したくなる知識", "size": "m"},
        {"text": ""},
        {"text": "人は驚きを共有したがる", "size": "m"},
    ], f"{output_dir}/slide_05.png")

    # 6. ③ 「自分だけ知ってる感」を出す
    create_content_slide([
        {"text": "③ 特別感を出す", "size": "l"},
        {"text": ""},
        {"text": "「プロしか知らない裏話」", "size": "m"},
        {"text": "「業界の常識、実は…」", "size": "m"},
        {"text": ""},
        {"text": "限定感が保存を生む", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")

    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "保存される投稿は", "size": "m"},
        {"text": "読んだ人を「賢くする」投稿", "size": "m"},
        {"text": ""},
        {"text": "価値を手元に残したくなる", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")

    # 8. 具体事例
    create_example_slide(
        "assets/isometric/b1_example.png",
        "具体事例：投稿設計",
        ["保存される投稿の例：", "「カラー後のシャンプー、", "実は24時間空けなくていい。", "正しい洗い方はこの3ステップ」"],
        f"{output_dir}/slide_08.png"
    )

    # 9. 縦文字キーワード
    create_vertical_text_slide("価値", "価値を残せ", f"{output_dir}/slide_09.png")

    # 10. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①使える知識を入れる", "②話したくなる知識を入れる", "③特別感を出す"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_10.png"
    )

    print(f"\n✅ B-1 complete! Check {output_dir}/")
    return output_dir


def generate_b2():
    """B-2: 数字が入る投稿ほど保存される理由（具体性バイアス）"""
    output_dir = "output/b2_numbers"
    os.makedirs(output_dir, exist_ok=True)

    # 1. タイトル
    create_title_slide_two_line(
        "保存される投稿には",
        "",
        "数字",
        "がある",
        "SNS PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )

    # 2. 問題提起
    create_content_slide([
        {"text": "同じテーマなのに", "size": "l"},
        {"text": ""},
        {"text": "保存される投稿と", "size": "m"},
        {"text": "されない投稿がある", "size": "m"},
        {"text": ""},
        {"text": "その差は何？", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")

    # 3. 導入
    create_content_slide([
        {"text": "違いは1つだけ", "size": "l"},
        {"text": ""},
        {"text": "数字があるかどうか", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "数字は「試せそう」を生む", "size": "m"},
    ], f"{output_dir}/slide_03.png")

    # 4. ① 日数を入れる
    create_content_slide([
        {"text": "① 日数を入れる", "size": "l"},
        {"text": ""},
        {"text": "❌「習慣化のコツ」", "size": "m"},
        {"text": "⭕️「3日で習慣化するコツ」", "size": "m"},
        {"text": ""},
        {"text": "期限があると行動できる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_04.png")

    # 5. ② 回数を入れる
    create_content_slide([
        {"text": "② 回数を入れる", "size": "l"},
        {"text": ""},
        {"text": "❌「効果的なヘアケア」", "size": "m"},
        {"text": "⭕️「週2回のヘアケア」", "size": "m"},
        {"text": ""},
        {"text": "回数があると再現できる", "size": "m"},
    ], f"{output_dir}/slide_05.png")

    # 6. ③ 比較数字を入れる
    create_content_slide([
        {"text": "③ 比較数字を入れる", "size": "l"},
        {"text": ""},
        {"text": "❌「リピート率が上がる」", "size": "m"},
        {"text": "⭕️「リピート率が30%→80%」", "size": "m"},
        {"text": ""},
        {"text": "差がわかると読みたくなる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")

    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "抽象的な投稿は流れる", "size": "m"},
        {"text": "数字がある投稿は残る", "size": "m"},
        {"text": ""},
        {"text": "数字を入れろ", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")

    # 8. 具体事例
    create_example_slide(
        "assets/isometric/b2_example.png",
        "具体事例：タイトル改善",
        ["Before：", "「ドライヤーの使い方」", "After：", "「3分で変わる", "ドライヤーの使い方5選」"],
        f"{output_dir}/slide_08.png"
    )

    # 9. 縦文字キーワード
    create_vertical_text_slide("数字", "数字で伝えろ", f"{output_dir}/slide_09.png")

    # 10. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①日数を入れる", "②回数を入れる", "③比較数字を入れる"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_10.png"
    )

    print(f"\n✅ B-2 complete! Check {output_dir}/")
    return output_dir


def generate_b3():
    """B-3: 保存される投稿は結論が早い（認知負荷理論）"""
    output_dir = "output/b3_conclusion_first"
    os.makedirs(output_dir, exist_ok=True)

    # 1. タイトル
    create_title_slide_two_line(
        "保存されたいなら",
        "",
        "結論",
        "を先に言え",
        "SNS PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )

    # 2. 問題提起
    create_content_slide([
        {"text": "丁寧に説明した投稿ほど", "size": "l"},
        {"text": ""},
        {"text": "保存されない", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "心当たり、ない？", "size": "m"},
    ], f"{output_dir}/slide_02.png")

    # 3. 導入
    create_content_slide([
        {"text": "前置きが長いと", "size": "l"},
        {"text": "人は離脱する", "size": "l"},
        {"text": ""},
        {"text": "判断に使える時間は", "size": "m"},
        {"text": "たった2秒", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_03.png")

    # 4. ① 1行目で結論
    create_content_slide([
        {"text": "① 1行目で結論を出す", "size": "l"},
        {"text": ""},
        {"text": "❌「今日は〜について」", "size": "m"},
        {"text": "⭕️「単価は提示順で決まる」", "size": "m"},
        {"text": ""},
        {"text": "結論が先にあると読み進める", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_04.png")

    # 5. ② 2行目で理由
    create_content_slide([
        {"text": "② 2行目で理由を出す", "size": "l"},
        {"text": ""},
        {"text": "「なぜなら人は最初の情報を", "size": "m"},
        {"text": "基準にするから」", "size": "m"},
        {"text": ""},
        {"text": "理由がないと信じない", "size": "m"},
    ], f"{output_dir}/slide_05.png")

    # 6. ③ 3行目で行動を促す
    create_content_slide([
        {"text": "③ 3行目で行動提案", "size": "l"},
        {"text": ""},
        {"text": "「明日のカウンセリングで", "size": "m"},
        {"text": "高いメニューから見せてみて」", "size": "m"},
        {"text": ""},
        {"text": "行動が見えると保存される", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")

    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "保存される投稿は", "size": "m"},
        {"text": "結論→理由→行動の3段構成", "size": "m"},
        {"text": ""},
        {"text": "前置きを削れ", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")

    # 8. 具体事例
    create_example_slide(
        "assets/isometric/b3_example.png",
        "具体事例：投稿構成",
        ["1行目：結論を一文で", "2行目：理由を短く", "3行目：今日やれることを提示", "この順番を守るだけで", "保存率が変わる"],
        f"{output_dir}/slide_08.png"
    )

    # 9. 縦文字キーワード
    create_vertical_text_slide("結論", "結論から言え", f"{output_dir}/slide_09.png")

    # 10. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①1行目で結論を出す", "②2行目で理由を添える", "③3行目で行動を促す"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_10.png"
    )

    print(f"\n✅ B-3 complete! Check {output_dir}/")
    return output_dir


def generate_b4():
    """B-4: チェックリスト形式が強い理由（再利用価値）"""
    output_dir = "output/b4_checklist"
    os.makedirs(output_dir, exist_ok=True)

    # 1. タイトル
    create_title_slide_two_line(
        "最も保存されるのは",
        "",
        "リスト",
        "型の投稿だった",
        "SNS PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )

    # 2. 問題提起
    create_content_slide([
        {"text": "どんな投稿が", "size": "l"},
        {"text": "一番保存されるか知ってる？", "size": "l"},
        {"text": ""},
        {"text": "答えは", "size": "m"},
        {"text": "チェックリスト型", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")

    # 3. 導入
    create_content_slide([
        {"text": "なぜチェックリストが", "size": "l"},
        {"text": "保存されるのか", "size": "l"},
        {"text": ""},
        {"text": "「再利用できる」から", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "読んで終わりにならない", "size": "m"},
    ], f"{output_dir}/slide_03.png")

    # 4. ① 項目は3〜5個にする
    create_content_slide([
        {"text": "① 項目は3〜5個", "size": "l"},
        {"text": ""},
        {"text": "多すぎると見る気が失せる", "size": "m"},
        {"text": "少なすぎると価値が薄い", "size": "m"},
        {"text": ""},
        {"text": "3〜5個が最も行動しやすい", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_04.png")

    # 5. ② Yes/Noで判断できるようにする
    create_content_slide([
        {"text": "② Yes/Noで判断させる", "size": "l"},
        {"text": ""},
        {"text": "❌「接客を見直す」", "size": "m"},
        {"text": "⭕️「名前で呼んでいるか？」", "size": "m"},
        {"text": ""},
        {"text": "判断基準が明確なほど使える", "size": "m"},
    ], f"{output_dir}/slide_05.png")

    # 6. ③ 読後すぐ使える構成にする
    create_content_slide([
        {"text": "③ 今日から使える構成", "size": "l"},
        {"text": ""},
        {"text": "□ 来店時に名前で呼んだか", "size": "m"},
        {"text": "□ 前回の内容に触れたか", "size": "m"},
        {"text": "□ 次回提案を伝えたか", "size": "m"},
        {"text": ""},
        {"text": "すぐ使えるから保存される", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")

    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "保存される投稿は", "size": "m"},
        {"text": "「また見返したい」投稿", "size": "m"},
        {"text": ""},
        {"text": "リスト化で再利用を設計しろ", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")

    # 8. 具体事例
    create_example_slide(
        "assets/isometric/b4_example.png",
        "具体事例：チェックリスト",
        ["接客チェックリスト：", "□ 名前で呼んだか", "□ 前回の内容に触れたか", "□ 次回提案を伝えたか", "□ お見送りで一言添えたか"],
        f"{output_dir}/slide_08.png"
    )

    # 9. 縦文字キーワード
    create_vertical_text_slide("確認", "リストで再利用を作れ", f"{output_dir}/slide_09.png")

    # 10. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①項目は3〜5個に絞る", "②Yes/Noで判断できるように", "③読後すぐ使える構成にする"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_10.png"
    )

    print(f"\n✅ B-4 complete! Check {output_dir}/")
    return output_dir


def generate_b5():
    """B-5: 保存される投稿は「再現できる」（手順化のパワー）"""
    output_dir = "output/b5_reproducible"
    os.makedirs(output_dir, exist_ok=True)

    # 1. タイトル
    create_title_slide_two_line(
        "保存される投稿の",
        "共通",
        "点",
        "",
        "SNS PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )

    # 2. 問題提起
    create_content_slide([
        {"text": "いい情報を書いている", "size": "l"},
        {"text": ""},
        {"text": "なのに保存されない", "size": "l"},
        {"text": ""},
        {"text": "その原因は「再現性」の欠如", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_02.png")

    # 3. 導入
    create_content_slide([
        {"text": "保存される投稿は", "size": "l"},
        {"text": "必ず", "size": "l"},
        {"text": ""},
        {"text": "手順がある", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "抽象論では行動できない", "size": "m"},
    ], f"{output_dir}/slide_03.png")

    # 4. ① ステップに分ける
    create_content_slide([
        {"text": "① ステップに分ける", "size": "l"},
        {"text": ""},
        {"text": "❌「カウンセリングを改善する」", "size": "m"},
        {"text": "⭕️「Step1: 現状を聞く", "size": "m"},
        {"text": "　Step2: 理想を聞く」", "size": "m"},
        {"text": ""},
        {"text": "分解すると行動できる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_04.png")

    # 5. ② 所要時間を明記する
    create_content_slide([
        {"text": "② 所要時間を書く", "size": "l"},
        {"text": ""},
        {"text": "「この方法は3分で完了」", "size": "m"},
        {"text": "「1日5分の習慣で変わる」", "size": "m"},
        {"text": ""},
        {"text": "時間がわかると取り組める", "size": "m"},
    ], f"{output_dir}/slide_05.png")

    # 6. ③ 失敗ポイントを先に提示する
    create_content_slide([
        {"text": "③ 失敗ポイントを先出し", "size": "l"},
        {"text": ""},
        {"text": "「よくある失敗：", "size": "m"},
        {"text": "一気にやろうとすること」", "size": "m"},
        {"text": ""},
        {"text": "失敗回避で信頼が生まれる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")

    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "保存される投稿は", "size": "m"},
        {"text": "「真似できる」投稿", "size": "m"},
        {"text": ""},
        {"text": "手順化で再現性を作れ", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")

    # 8. 具体事例
    create_example_slide(
        "assets/isometric/b5_example.png",
        "具体事例：手順化",
        ["カウンセリング3ステップ：", "Step1: 現状を聞く（2分）", "Step2: 理想を聞く（2分）", "Step3: 提案する（1分）", "合計5分で完了"],
        f"{output_dir}/slide_08.png"
    )

    # 9. 縦文字キーワード
    create_vertical_text_slide("再現", "再現できる投稿を作れ", f"{output_dir}/slide_09.png")

    # 10. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①ステップに分ける", "②所要時間を明記する", "③失敗ポイントを先に出す"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_10.png"
    )

    print(f"\n✅ B-5 complete! Check {output_dir}/")
    return output_dir


def generate_c1():
    """C-1: リピートは満足ではなく記憶で決まる"""
    output_dir = "output/c1_memory"
    os.makedirs(output_dir, exist_ok=True)

    # 1. タイトル
    create_title_slide_two_line(
        "リピートされない理由は",
        "満足度",
        "じゃない",
        "",
        "REPEAT PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )

    # 2. 問題提起
    create_content_slide([
        {"text": "お客様は満足していた", "size": "l"},
        {"text": ""},
        {"text": "でも戻ってこない", "size": "l"},
        {"text": ""},
        {"text": "なぜ？", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")

    # 3. 導入
    create_content_slide([
        {"text": "リピートを決めるのは", "size": "l"},
        {"text": "「満足」ではなく", "size": "l"},
        {"text": ""},
        {"text": "「記憶」", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "思い出せないサロンには戻れない", "size": "m"},
    ], f"{output_dir}/slide_03.png")

    # 4. ① 感情のピークを作る
    create_content_slide([
        {"text": "① 感情のピークを作る", "size": "l"},
        {"text": ""},
        {"text": "「わぁ、すごい」と思う瞬間を", "size": "m"},
        {"text": "意図的に1回つくる", "size": "m"},
        {"text": ""},
        {"text": "感情が動くと記憶に残る", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_04.png")

    # 5. ② 言葉で記憶に残す
    create_content_slide([
        {"text": "② 言葉で刻む", "size": "l"},
        {"text": ""},
        {"text": "「今日のポイントは", "size": "m"},
        {"text": "〇〇ですからね」と一言添える", "size": "m"},
        {"text": ""},
        {"text": "言語化されると記憶が定着する", "size": "m"},
    ], f"{output_dir}/slide_05.png")

    # 6. ③ 退店後に思い出すきっかけを渡す
    create_content_slide([
        {"text": "③ 思い出すきっかけを渡す", "size": "l"},
        {"text": ""},
        {"text": "帰宅後に「あのサロン」と", "size": "m"},
        {"text": "思い出すトリガーを作る", "size": "m"},
        {"text": ""},
        {"text": "ケアカード・LINE・香り", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")

    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "満足しても忘れられたら終わり", "size": "m"},
        {"text": ""},
        {"text": "記憶に残る体験を設計しろ", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")

    # 8. 具体事例
    create_example_slide(
        "assets/isometric/c1_example.png",
        "具体事例：記憶設計",
        ["施術中：「今日は毛先の艶が", "ポイントですからね」", "退店時：ケアカードを渡す", "→ 帰宅後に思い出すトリガー"],
        f"{output_dir}/slide_08.png"
    )

    # 9. 縦文字キーワード
    create_vertical_text_slide("記憶", "記憶に残せ", f"{output_dir}/slide_09.png")

    # 10. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①感情のピークを作る", "②言葉で記憶に残す", "③思い出すきっかけを渡す"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_10.png"
    )

    print(f"\n✅ C-1 complete! Check {output_dir}/")
    return output_dir


def generate_c2():
    """C-2: 次回予約は会計前が最も通る"""
    output_dir = "output/c2_next_booking"
    os.makedirs(output_dir, exist_ok=True)

    # 1. タイトル
    create_title_slide_two_line(
        "次回予約を取るなら",
        "会計",
        "前",
        "",
        "REPEAT PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )

    # 2. 問題提起
    create_content_slide([
        {"text": "「また来てくださいね」", "size": "l"},
        {"text": ""},
        {"text": "その一言で終わっていない？", "size": "m"},
        {"text": ""},
        {"text": "次回予約率が低い原因はそこ", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_02.png")

    # 3. 導入
    create_content_slide([
        {"text": "次回予約のベストタイミングは", "size": "l"},
        {"text": ""},
        {"text": "会計の前", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "お金を払った後では遅い", "size": "m"},
    ], f"{output_dir}/slide_03.png")

    # 4. ① 仕上がりを見せた直後に提案
    create_content_slide([
        {"text": "① 仕上がり直後に提案", "size": "l"},
        {"text": ""},
        {"text": "「この艶を維持するなら", "size": "m"},
        {"text": "次は1ヶ月半後がベストです」", "size": "m"},
        {"text": ""},
        {"text": "満足度が最高の瞬間に動く", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_04.png")

    # 5. ② 選択肢を2つに絞る
    create_content_slide([
        {"text": "② 選択肢を2つに絞る", "size": "l"},
        {"text": ""},
        {"text": "「○月の前半と後半、", "size": "m"},
        {"text": "どちらがご都合いいですか？」", "size": "m"},
        {"text": ""},
        {"text": "「いつにする？」は決められない", "size": "m"},
    ], f"{output_dir}/slide_05.png")

    # 6. ③ 理由と一緒に提案する
    create_content_slide([
        {"text": "③ 理由を添える", "size": "l"},
        {"text": ""},
        {"text": "「根元が伸びてくると", "size": "m"},
        {"text": "印象が変わりやすいので」", "size": "m"},
        {"text": ""},
        {"text": "理由があると断りにくい", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")

    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "次回予約は「お願い」ではなく", "size": "m"},
        {"text": "「提案」として出す", "size": "m"},
        {"text": ""},
        {"text": "タイミングは会計前の一瞬", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")

    # 8. 具体事例
    create_example_slide(
        "assets/isometric/c2_example.png",
        "具体事例：次回予約の流れ",
        ["仕上がり確認", "→「次は○月がベストです」", "→「前半と後半どちらが", "ご都合いいですか？」", "→ 予約確定 → 会計"],
        f"{output_dir}/slide_08.png"
    )

    # 9. 縦文字キーワード
    create_vertical_text_slide("予約", "会計前に取れ", f"{output_dir}/slide_09.png")

    # 10. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①仕上がり直後に提案する", "②選択肢を2つに絞る", "③理由を添えて提案する"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_10.png"
    )

    print(f"\n✅ C-2 complete! Check {output_dir}/")
    return output_dir


def generate_c3():
    """C-3: 顧客台帳の一言メモが売上を変える"""
    output_dir = "output/c3_customer_memo"
    os.makedirs(output_dir, exist_ok=True)

    # 1. タイトル
    create_title_slide_two_line(
        "売上を変えるのは",
        "一言",
        "メモ",
        "",
        "REPEAT PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )

    # 2. 問題提起
    create_content_slide([
        {"text": "顧客カルテ、書いてる？", "size": "l"},
        {"text": ""},
        {"text": "施術内容だけ記録しても", "size": "m"},
        {"text": "リピートにはつながらない", "size": "m"},
        {"text": ""},
        {"text": "何が足りない？", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")

    # 3. 導入
    create_content_slide([
        {"text": "足りないのは", "size": "l"},
        {"text": ""},
        {"text": "「人間」の情報", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "施術記録はデータ", "size": "m"},
        {"text": "一言メモは「関係性」", "size": "m"},
    ], f"{output_dir}/slide_03.png")

    # 4. ① 会話の内容を1行メモ
    create_content_slide([
        {"text": "① 会話を1行メモする", "size": "l"},
        {"text": ""},
        {"text": "「旅行の話をしていた」", "size": "m"},
        {"text": "「子どもの受験が近い」", "size": "m"},
        {"text": ""},
        {"text": "次回「あの話どうでした？」が", "size": "m"},
        {"text": "最強のリピート装置", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_04.png")

    # 5. ② 好みの傾向を記録
    create_content_slide([
        {"text": "② 好みの傾向を残す", "size": "l"},
        {"text": ""},
        {"text": "「短くしすぎると不安がる」", "size": "m"},
        {"text": "「明るめが好き」", "size": "m"},
        {"text": ""},
        {"text": "言わなくても分かってくれる安心", "size": "m"},
    ], f"{output_dir}/slide_05.png")

    # 6. ③ 感情の変化を記録
    create_content_slide([
        {"text": "③ 感情の変化を記録", "size": "l"},
        {"text": ""},
        {"text": "「前回は仕事で疲れてた」", "size": "m"},
        {"text": "「今回は明るい雰囲気だった」", "size": "m"},
        {"text": ""},
        {"text": "寄り添いの精度が上がる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")

    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "施術カルテは技術の記録", "size": "m"},
        {"text": "一言メモは関係性の記録", "size": "m"},
        {"text": ""},
        {"text": "一言メモが売上を変える", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")

    # 8. 具体事例
    create_example_slide(
        "assets/isometric/c3_example.png",
        "具体事例：一言メモ",
        ["施術記録：カット+カラー", "一言メモ：", "「来月旅行。明るめ希望。」", "「疲れ気味。静かに過ごしたい」", "→ 次回の接客精度が変わる"],
        f"{output_dir}/slide_08.png"
    )

    # 9. 縦文字キーワード
    create_vertical_text_slide("関係", "関係を記録しろ", f"{output_dir}/slide_09.png")

    # 10. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①会話を1行メモする", "②好みの傾向を残す", "③感情の変化を記録する"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_10.png"
    )

    print(f"\n✅ C-3 complete! Check {output_dir}/")
    return output_dir


def generate_c4():
    """C-4: 来店間隔を設計すると失客が減る"""
    output_dir = "output/c4_visit_interval"
    os.makedirs(output_dir, exist_ok=True)

    # 1. タイトル
    create_title_slide_two_line(
        "失客を減らすには",
        "間隔",
        "設計",
        "",
        "REPEAT PSYCHOLOGY",
        f"{output_dir}/slide_01.png"
    )

    # 2. 問題提起
    create_content_slide([
        {"text": "3回来たのに", "size": "l"},
        {"text": "4回目が来ない", "size": "l"},
        {"text": ""},
        {"text": "その失客、防げたかも", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_02.png")

    # 3. 導入
    create_content_slide([
        {"text": "失客の原因の多くは", "size": "l"},
        {"text": ""},
        {"text": "「来店間隔が空きすぎた」こと", "size": "m"},
        {"text": ""},
        {"text": "間隔を設計すれば", "size": "m"},
        {"text": "失客は減らせる", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_03.png")

    # 4. ① 理想の来店周期を伝える
    create_content_slide([
        {"text": "① 理想の周期を伝える", "size": "l"},
        {"text": ""},
        {"text": "「この髪型を維持するなら", "size": "m"},
        {"text": "○週間がベストです」", "size": "m"},
        {"text": ""},
        {"text": "根拠があると納得される", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_04.png")

    # 5. ② 間隔が空いた人にアプローチ
    create_content_slide([
        {"text": "② 空いた人にアプローチ", "size": "l"},
        {"text": ""},
        {"text": "来店から90日経過したら", "size": "m"},
        {"text": "「お元気ですか？」の一言", "size": "m"},
        {"text": ""},
        {"text": "催促ではなく気遣いとして", "size": "m"},
    ], f"{output_dir}/slide_05.png")

    # 6. ③ 次回来店の理由を作る
    create_content_slide([
        {"text": "③ 次回の理由を作る", "size": "l"},
        {"text": ""},
        {"text": "「梅雨前にストレートしておくと", "size": "m"},
        {"text": "楽ですよ」", "size": "m"},
        {"text": ""},
        {"text": "季節や行事は最高のきっかけ", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_06.png")

    # 7. まとめ
    create_content_slide([
        {"text": "つまり", "size": "l"},
        {"text": ""},
        {"text": "失客は「放置」の結果", "size": "m"},
        {"text": "来店間隔を管理すれば防げる", "size": "m"},
        {"text": ""},
        {"text": "間隔を設計しろ", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_07.png")

    # 8. 具体事例
    create_example_slide(
        "assets/isometric/c4_example.png",
        "具体事例：間隔管理",
        ["カラー：6週間周期で提案", "カット：4〜6週間で提案", "90日来店なし：DM送信", "季節の変わり目：", "「梅雨前のケア」を提案"],
        f"{output_dir}/slide_08.png"
    )

    # 9. 縦文字キーワード
    create_vertical_text_slide("間隔", "間隔で失客を防げ", f"{output_dir}/slide_09.png")

    # 10. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["①理想の来店周期を伝える", "②間隔が空いた人にアプローチ", "③次回来店の理由を作る"],
        "Fleeksオンラインセミナーの内容を抜粋しています",
        f"{output_dir}/slide_10.png"
    )

    print(f"\n✅ C-4 complete! Check {output_dir}/")
    return output_dir


def generate_d1():
    """D-1: 高い方を先に見せると安い方が売れる（コントラスト効果）"""
    output_dir = "output/d1_contrast"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("単価を上げたいなら", "見せる", "順番", "を変えろ", "PRICING PSYCHOLOGY", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "安いメニューから見せていない？", "size": "l"}, {"text": ""}, {"text": "それ、単価が上がらない原因", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "人は最初に見た価格を基準にする", "size": "l"}, {"text": ""}, {"text": "コントラスト効果", "size": "xl", "highlight": True}, {"text": ""}, {"text": "高い方を先に見せると安い方が「お得」に感じる", "size": "m"}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① メニュー表は高い順に並べる", "size": "l"}, {"text": ""}, {"text": "最初に見る価格が「基準」になる", "size": "m"}, {"text": "高い方を先に見せるだけで", "size": "m"}, {"text": "中間メニューが選ばれやすくなる", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② 提案も高い方から伝える", "size": "l"}, {"text": ""}, {"text": "「一番おすすめはこちらですが」", "size": "m"}, {"text": "「こちらもいい選択です」", "size": "m"}, {"text": ""}, {"text": "2番目が「ちょうどいい」に変わる", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ セットの比較を見せる", "size": "l"}, {"text": ""}, {"text": "単品とセットを並べるだけで", "size": "m"}, {"text": "セットの価値が際立つ", "size": "m"}, {"text": ""}, {"text": "比較対象を作るのがコツ", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "安い方から見せると安い方が売れる", "size": "m"}, {"text": ""}, {"text": "高い方から見せろ", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/d1_example.png", "具体事例：メニュー順", ["メニュー表：上から順に", "プレミアム → スタンダード → ベーシック", "→ スタンダードが最も選ばれる"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("順番", "見せる順番を変えろ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①メニュー表は高い順に並べる", "②提案も高い方から伝える", "③セットの比較を見せる"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ D-1 complete! Check {output_dir}/")
    return output_dir


def generate_d2():
    """D-2: 「松竹梅」の法則で真ん中が選ばれる"""
    output_dir = "output/d2_three_tier"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("選ばれるのはいつも", "真ん中", "", "", "PRICING PSYCHOLOGY", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "メニューが2つだと", "size": "l"}, {"text": "安い方が選ばれる", "size": "l"}, {"text": ""}, {"text": "でも3つにすると？", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "3つの選択肢があると", "size": "l"}, {"text": "人は真ん中を選ぶ", "size": "l"}, {"text": ""}, {"text": "松竹梅の法則", "size": "xl", "highlight": True}, {"text": ""}, {"text": "極端を避ける心理が働く", "size": "m"}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① 3段階のメニューを作る", "size": "l"}, {"text": ""}, {"text": "プレミアム・スタンダード・ベーシック", "size": "m"}, {"text": ""}, {"text": "真ん中が「売りたいメニュー」", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② 価格差のバランスを調整", "size": "l"}, {"text": ""}, {"text": "上と中の差 ＞ 中と下の差", "size": "m"}, {"text": ""}, {"text": "上が「高すぎ」に見えると", "size": "m"}, {"text": "真ん中が「ちょうどいい」になる", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ 上位メニューに特別感を出す", "size": "l"}, {"text": ""}, {"text": "「限定」「特別ケア付き」など", "size": "m"}, {"text": "上位の存在理由を明確にする", "size": "m"}, {"text": ""}, {"text": "比較の「引き立て役」になる", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "2択では安い方が選ばれる", "size": "m"}, {"text": "3択にすれば真ん中が売れる", "size": "m"}, {"text": ""}, {"text": "松竹梅で設計しろ", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/d2_example.png", "具体事例：3段階設計", ["プレミアムコース：¥15,000", "スタンダードコース：¥10,000", "ベーシックコース：¥7,000", "→ スタンダードが最多選択"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("三択", "3択で真ん中を売れ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①3段階のメニューを作る", "②価格差のバランスを調整", "③上位に特別感を出す"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ D-2 complete! Check {output_dir}/")
    return output_dir


def generate_d3():
    """D-3: セットメニューが単価を上げる理由（バンドリング効果）"""
    output_dir = "output/d3_bundling"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("単価を上げるなら", "セット", "メニュー", "", "PRICING PSYCHOLOGY", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "「カットだけで」と言われて", "size": "l"}, {"text": "そのまま終わっていない？", "size": "l"}, {"text": ""}, {"text": "セットの提案で変わる", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "セットにすると", "size": "l"}, {"text": "「お得感」が生まれる", "size": "l"}, {"text": ""}, {"text": "バンドリング効果", "size": "xl", "highlight": True}, {"text": ""}, {"text": "個別に売るより断然売れやすい", "size": "m"}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① メニューの組み合わせを作る", "size": "l"}, {"text": ""}, {"text": "カット＋トリートメント", "size": "m"}, {"text": "カラー＋ヘッドスパ", "size": "m"}, {"text": ""}, {"text": "相性の良い組み合わせで提案", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② セット割引を設定する", "size": "l"}, {"text": ""}, {"text": "個別合計より10〜15%オフ", "size": "m"}, {"text": ""}, {"text": "「一緒にやると少しお得です」", "size": "m"}, {"text": "この一言で決まる", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ 季節セットを作る", "size": "l"}, {"text": ""}, {"text": "「夏のダメージケアセット」", "size": "m"}, {"text": "「梅雨対策セット」", "size": "m"}, {"text": ""}, {"text": "期間限定が行動を促す", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "単品で売ると単価は上がらない", "size": "m"}, {"text": ""}, {"text": "セットで「お得」を設計しろ", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/d3_example.png", "具体事例：セット設計", ["カット¥5,000+トリートメント¥3,000", "= 単品合計¥8,000", "セット価格：¥7,000（12%OFF）", "→ セット選択率60%以上"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("束売", "セットで単価を上げろ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①メニューの組み合わせを作る", "②セット割引を設定する", "③季節セットを作る"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ D-3 complete! Check {output_dir}/")
    return output_dir


def generate_d4():
    """D-4: 「ついで買い」を設計する方法（クロスセル）"""
    output_dir = "output/d4_cross_sell"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("売上を伸ばすのは", "ついで", "買い", "", "PRICING PSYCHOLOGY", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "物販が売れないのは", "size": "l"}, {"text": "「売り方」の問題", "size": "l"}, {"text": ""}, {"text": "押し売りではない方法がある", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "施術中に使った商品を", "size": "l"}, {"text": "そのまま提案する", "size": "l"}, {"text": ""}, {"text": "クロスセル", "size": "xl", "highlight": True}, {"text": ""}, {"text": "体験後なら売り込み感がない", "size": "m"}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① 施術中に商品を体験させる", "size": "l"}, {"text": ""}, {"text": "「今日使ったオイル、いい香りでしょ？」", "size": "m"}, {"text": ""}, {"text": "体験が最強のセールス", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② 仕上がりと結びつけて提案", "size": "l"}, {"text": ""}, {"text": "「この艶を自宅でも維持するなら", "size": "m"}, {"text": "このトリートメントがおすすめです」", "size": "m"}, {"text": ""}, {"text": "結果と紐づけると説得力が出る", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ レジ横に小物を置く", "size": "l"}, {"text": ""}, {"text": "ヘアゴム・ミニサンプル・ケア剤", "size": "m"}, {"text": ""}, {"text": "「ついでにこれも」の動線を作る", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "物販は「売る」のではなく", "size": "m"}, {"text": "「体験の延長」として出す", "size": "m"}, {"text": ""}, {"text": "ついで買いを設計しろ", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/d4_example.png", "具体事例：クロスセル", ["施術中：オイルを使用", "→「いい香りでしょ？」", "仕上げ：「自宅でも使えますよ」", "レジ横：ミニサイズを陳列", "→ 物販率30%アップ"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("体験", "体験させてから売れ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①施術中に商品を体験させる", "②仕上がりと結びつけて提案", "③レジ横に小物を置く"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ D-4 complete! Check {output_dir}/")
    return output_dir


def generate_e1():
    """E-1: 最初の質問が全てを決める（プライミング効果）"""
    output_dir = "output/e1_priming"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("カウンセリングは", "最初の", "一問", "で決まる", "COUNSELING SCIENCE", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "「今日はどうしますか？」", "size": "l"}, {"text": ""}, {"text": "それ、最悪の一問目", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "最初の質問が", "size": "l"}, {"text": "会話の方向を決める", "size": "l"}, {"text": ""}, {"text": "プライミング効果", "size": "xl", "highlight": True}, {"text": ""}, {"text": "最初に聞いたことが基準になる", "size": "m"}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① ポジティブな質問から始める", "size": "l"}, {"text": ""}, {"text": "「最近、髪で気に入ってるところは？」", "size": "m"}, {"text": ""}, {"text": "良い方向に意識が向く", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② 理想を先に聞く", "size": "l"}, {"text": ""}, {"text": "「どんな印象になりたいですか？」", "size": "m"}, {"text": ""}, {"text": "不満ではなく理想から入る", "size": "m"}, {"text": "提案がポジティブになる", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ 選択肢付きで聞く", "size": "l"}, {"text": ""}, {"text": "「軽い感じと、まとまる感じ、", "size": "m"}, {"text": "どちらが好みですか？」", "size": "m"}, {"text": ""}, {"text": "選べると答えやすい", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "最初の一問が全てを決める", "size": "m"}, {"text": ""}, {"text": "一問目を設計しろ", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/e1_example.png", "具体事例：最初の質問", ["NG：「今日はどうしますか？」", "OK：「最近の髪で", "気に入ってるところは？」", "→ ポジティブな会話が始まる"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("一問", "最初の一問を変えろ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①ポジティブな質問から始める", "②理想を先に聞く", "③選択肢付きで聞く"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ E-1 complete! Check {output_dir}/")
    return output_dir


def generate_e2():
    """E-2: 「はい」を3回言わせると提案が通る（イエスセット）"""
    output_dir = "output/e2_yes_set"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("提案を通すには", "はい", "を3回", "言わせろ", "COUNSELING SCIENCE", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "提案しても「考えます」で終わる", "size": "l"}, {"text": ""}, {"text": "その前に仕込みが足りない", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "小さな「はい」を3回積むと", "size": "l"}, {"text": "大きな「はい」が出やすくなる", "size": "l"}, {"text": ""}, {"text": "イエスセット", "size": "xl", "highlight": True}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① 事実確認で「はい」を取る", "size": "l"}, {"text": ""}, {"text": "「前回カラーされましたよね？」", "size": "m"}, {"text": "「はい」", "size": "m"}, {"text": ""}, {"text": "否定しようがない事実から入る", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② 共感で「はい」を取る", "size": "l"}, {"text": ""}, {"text": "「根元が気になってきますよね？」", "size": "m"}, {"text": "「はい、そうなんです」", "size": "m"}, {"text": ""}, {"text": "共感は「はい」を引き出しやすい", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ 提案を出す", "size": "l"}, {"text": ""}, {"text": "「じゃあ今日リタッチしましょうか」", "size": "m"}, {"text": ""}, {"text": "「はい」の流れができているから", "size": "m"}, {"text": "提案が自然に通る", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "いきなり提案するから断られる", "size": "m"}, {"text": ""}, {"text": "「はい」を3回積んでから出せ", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/e2_example.png", "具体事例：イエスセット", ["①「前回カラーしましたよね？」→はい", "②「根元気になりますよね？」→はい", "③「艶もキープしたいですよね？」→はい", "④「今日リタッチしましょうか」→OK"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("同意", "小さな同意を積め", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①事実確認で「はい」を取る", "②共感で「はい」を取る", "③流れに乗せて提案を出す"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ E-2 complete! Check {output_dir}/")
    return output_dir


def generate_e3():
    """E-3: 聞く順番を変えるだけで満足度が上がる"""
    output_dir = "output/e3_question_order"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("満足度を上げるのは", "聞く", "順番", "", "COUNSELING SCIENCE", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "同じ質問をしているのに", "size": "l"}, {"text": "お客様の反応が違う", "size": "l"}, {"text": ""}, {"text": "それ、聞く順番の問題かも", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "聞く順番で印象が変わる", "size": "l"}, {"text": ""}, {"text": "広い質問→狭い質問", "size": "xl", "highlight": True}, {"text": ""}, {"text": "いきなり細かく聞くと窮屈に感じる", "size": "m"}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① まず全体像を聞く", "size": "l"}, {"text": ""}, {"text": "「普段どんな雰囲気が好き？」", "size": "m"}, {"text": ""}, {"text": "大きな方向性を先に確認", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② 次に具体的に聞く", "size": "l"}, {"text": ""}, {"text": "「長さはどのあたりまで？」", "size": "m"}, {"text": "「前髪はどうしましょう？」", "size": "m"}, {"text": ""}, {"text": "方向性が決まった後なら答えやすい", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ 最後に確認する", "size": "l"}, {"text": ""}, {"text": "「つまり〇〇な感じですね？」", "size": "m"}, {"text": ""}, {"text": "要約して確認すると安心感が生まれる", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "質問の内容より「順番」が大事", "size": "m"}, {"text": ""}, {"text": "広い→狭い→確認の順で聞け", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/e3_example.png", "具体事例：質問の順番", ["①「普段どんな雰囲気が好き？」", "②「長さはこのくらい？」", "③「前髪はどうしましょう？」", "④「つまり軽めのボブですね？」"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("順序", "聞く順番を設計しろ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①まず全体像を聞く", "②次に具体的に聞く", "③最後に要約して確認する"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ E-3 complete! Check {output_dir}/")
    return output_dir


def generate_e4():
    """E-4: 写真を使うと要望のズレが減る（ビジュアルアンカー）"""
    output_dir = "output/e4_visual_anchor"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("要望のズレを防ぐには", "写真", "を見せろ", "", "COUNSELING SCIENCE", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "「軽くしてください」", "size": "l"}, {"text": ""}, {"text": "あなたの「軽い」と", "size": "m"}, {"text": "お客様の「軽い」は違う", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "写真を共有すると", "size": "l"}, {"text": "認識のズレが激減する", "size": "l"}, {"text": ""}, {"text": "ビジュアルアンカー", "size": "xl", "highlight": True}, {"text": ""}, {"text": "言葉よりイメージが正確", "size": "m"}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① 参考写真を2〜3枚見せる", "size": "l"}, {"text": ""}, {"text": "「この中でイメージに近いのは？」", "size": "m"}, {"text": ""}, {"text": "選んでもらうと要望が明確になる", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② お客様のスマホ写真も活用", "size": "l"}, {"text": ""}, {"text": "「参考にしてる写真ありますか？」", "size": "m"}, {"text": ""}, {"text": "持ってきた写真から本音が見える", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ 仕上がり予測を共有", "size": "l"}, {"text": ""}, {"text": "「こんな感じになりますが", "size": "m"}, {"text": "大丈夫ですか？」", "size": "m"}, {"text": ""}, {"text": "施術前に期待値を揃える", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "言葉だけでは伝わらない", "size": "m"}, {"text": ""}, {"text": "写真で「見える化」しろ", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/e4_example.png", "具体事例：写真活用", ["参考写真を3枚用意", "→「この中でどれが近い？」", "→「ここをもう少し短く」", "→ ズレなく仕上がる"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("視覚", "写真でズレをなくせ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①参考写真を2〜3枚見せる", "②お客様のスマホ写真も活用", "③仕上がり予測を事前共有"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ E-4 complete! Check {output_dir}/")
    return output_dir


def generate_e5():
    """E-5: 沈黙の3秒がカウンセリングを変える"""
    output_dir = "output/e5_silence"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("カウンセリングを変える", "沈黙の", "3秒", "", "COUNSELING SCIENCE", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "質問した直後に", "size": "l"}, {"text": "自分で答えを埋めていない？", "size": "l"}, {"text": ""}, {"text": "それ、お客様の本音を消している", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "質問の後に3秒待つだけで", "size": "l"}, {"text": "お客様は自分で話し始める", "size": "l"}, {"text": ""}, {"text": "沈黙の力", "size": "xl", "highlight": True}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① 質問したら黙る", "size": "l"}, {"text": ""}, {"text": "沈黙が怖くても3秒待つ", "size": "m"}, {"text": ""}, {"text": "お客様は考えている最中", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② うなずきだけで待つ", "size": "l"}, {"text": ""}, {"text": "言葉を挟まず", "size": "m"}, {"text": "うなずきとアイコンタクトで待つ", "size": "m"}, {"text": ""}, {"text": "「聞いてもらえてる」感が生まれる", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ 出てきた言葉を繰り返す", "size": "l"}, {"text": ""}, {"text": "「〇〇が気になるんですね」", "size": "m"}, {"text": ""}, {"text": "繰り返すだけで信頼が深まる", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "しゃべりすぎると本音は出ない", "size": "m"}, {"text": ""}, {"text": "3秒の沈黙を味方にしろ", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/e5_example.png", "具体事例：3秒の沈黙", ["質問：「前髪どうしましょう？」", "→ 3秒待つ", "→ 客：「実は…伸ばしたいけど", "邪魔で迷ってて」", "→ 本音が出た！"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("沈黙", "3秒黙れ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①質問したら3秒黙る", "②うなずきだけで待つ", "③出てきた言葉を繰り返す"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ E-5 complete! Check {output_dir}/")
    return output_dir


def generate_f1():
    """F-1: 口コミは「感動」ではなく「語れるネタ」から生まれる"""
    output_dir = "output/f1_word_of_mouth"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("口コミが生まれるのは", "語れる", "ネタ", "があるとき", "REVIEW PSYCHOLOGY", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "「感動させれば口コミが増える」", "size": "l"}, {"text": ""}, {"text": "それ、半分間違い", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "口コミが生まれるのは", "size": "l"}, {"text": "「人に話したくなるネタ」", "size": "l"}, {"text": "があるとき", "size": "l"}, {"text": ""}, {"text": "語れるネタ", "size": "xl", "highlight": True}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① 驚きポイントを1つ作る", "size": "l"}, {"text": ""}, {"text": "「え、こんなこともしてくれるの？」", "size": "m"}, {"text": ""}, {"text": "想定外のサービスが「ネタ」になる", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② 比較しやすい特徴を持つ", "size": "l"}, {"text": ""}, {"text": "「あのサロン、〇〇が違うんだよ」", "size": "m"}, {"text": ""}, {"text": "一言で説明できる特徴が広まる", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ 帰ってから気づく仕掛け", "size": "l"}, {"text": ""}, {"text": "手書きのケアメモ・サンプル同封", "size": "m"}, {"text": ""}, {"text": "帰宅後の「発見」が口コミを生む", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "感動は忘れるが、ネタは語られる", "size": "m"}, {"text": ""}, {"text": "語れるネタを仕込め", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/f1_example.png", "具体事例：口コミネタ", ["驚き：頭皮診断をしてくれた", "特徴：「あの店、スパが最高」", "帰宅後：手書きケアメモ発見", "→ 友人に語るネタが3つ"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("語句", "語れるネタを仕込め", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①驚きポイントを1つ作る", "②一言で説明できる特徴を持つ", "③帰宅後の発見を仕掛ける"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ F-1 complete! Check {output_dir}/")
    return output_dir


def generate_f2():
    """F-2: 写真を撮りたくなる瞬間を設計する"""
    output_dir = "output/f2_photo_moment"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("口コミを増やすなら", "撮りたい", "瞬間", "を作れ", "REVIEW PSYCHOLOGY", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "SNSに投稿してもらいたい？", "size": "l"}, {"text": ""}, {"text": "なら「撮りたくなる瞬間」を", "size": "m"}, {"text": "設計するしかない", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "人が写真を撮るのは", "size": "l"}, {"text": "「見せたい自分」がいるとき", "size": "l"}, {"text": ""}, {"text": "自己表現欲求", "size": "xl", "highlight": True}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① 仕上げの鏡越しショット", "size": "l"}, {"text": ""}, {"text": "「すごくいい感じですね！", "size": "m"}, {"text": "写真撮りましょうか？」", "size": "m"}, {"text": ""}, {"text": "最高の瞬間を記録として渡す", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② フォトスポットを用意", "size": "l"}, {"text": ""}, {"text": "照明・背景・小物を整える", "size": "m"}, {"text": ""}, {"text": "「映える」環境を作れば撮る", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ Before/Afterを見せる", "size": "l"}, {"text": ""}, {"text": "「こんなに変わりましたよ」と", "size": "m"}, {"text": "並べて見せる", "size": "m"}, {"text": ""}, {"text": "変化が大きいほどシェアされる", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "「投稿してね」ではなく", "size": "m"}, {"text": "「撮りたくなる瞬間」を作れ", "size": "m"}, {"text": ""}, {"text": "仕組みで口コミを生め", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/f2_example.png", "具体事例：撮影導線", ["仕上げ後：鏡越しに撮影提案", "フォトスポット：壁面＋照明", "Before/After：並べて提示", "→ ストーリーズ投稿率UP"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("撮影", "撮りたい瞬間を作れ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①仕上げ時に撮影を提案する", "②フォトスポットを用意する", "③Before/Afterを見せる"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ F-2 complete! Check {output_dir}/")
    return output_dir


def generate_f3():
    """F-3: 紹介が起きる「頼み方」の科学"""
    output_dir = "output/f3_referral"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("紹介を増やすには", "頼み方", "にコツ", "がある", "REVIEW PSYCHOLOGY", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "「お友達紹介してね」", "size": "l"}, {"text": ""}, {"text": "それだけでは紹介は起きない", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "紹介が起きるのは", "size": "l"}, {"text": "「誰に・何を」が明確なとき", "size": "l"}, {"text": ""}, {"text": "具体的な導線", "size": "xl", "highlight": True}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① 対象を具体的にする", "size": "l"}, {"text": ""}, {"text": "「髪の悩みがある方いませんか？」", "size": "m"}, {"text": ""}, {"text": "「誰か」では思い浮かばない", "size": "m"}, {"text": "具体的にすると顔が浮かぶ", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② 紹介カードを渡す", "size": "l"}, {"text": ""}, {"text": "「この方に直接お渡しください」", "size": "m"}, {"text": ""}, {"text": "物理的なきっかけがあると動く", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ 双方にメリットを設計", "size": "l"}, {"text": ""}, {"text": "紹介者にも新規客にも特典", "size": "m"}, {"text": ""}, {"text": "「あなたにもメリットがある」", "size": "m"}, {"text": "これで心理的ハードルが下がる", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "紹介は「お願い」ではなく", "size": "m"}, {"text": "「仕組み」で起こす", "size": "m"}, {"text": ""}, {"text": "具体的な導線を設計しろ", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/f3_example.png", "具体事例：紹介の導線", ["「髪の悩みがある方いませんか？」", "→ 紹介カードを渡す", "→ 紹介者：次回10%OFF", "→ 新規客：初回20%OFF"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("紹介", "紹介の仕組みを作れ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①対象を具体的にする", "②紹介カードを渡す", "③双方にメリットを設計する"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ F-3 complete! Check {output_dir}/")
    return output_dir


def generate_f4():
    """F-4: Googleレビューを自然に増やす仕組み"""
    output_dir = "output/f4_google_review"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("レビューを増やすなら", "仕組み", "化", "しろ", "REVIEW PSYCHOLOGY", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "Googleレビューが少ない？", "size": "l"}, {"text": ""}, {"text": "お客様は「書きたくない」のではなく", "size": "m"}, {"text": "「きっかけがない」だけ", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "レビューを増やすコツは", "size": "l"}, {"text": "「書く導線を作る」こと", "size": "l"}, {"text": ""}, {"text": "行動設計", "size": "xl", "highlight": True}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① QRコードを設置する", "size": "l"}, {"text": ""}, {"text": "レジ横・カード・席の前", "size": "m"}, {"text": ""}, {"text": "「ここからお願いします」と", "size": "m"}, {"text": "一言添えるだけ", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② 満足度が高い瞬間に頼む", "size": "l"}, {"text": ""}, {"text": "仕上がりを確認した直後", "size": "m"}, {"text": ""}, {"text": "「気に入っていただけたら", "size": "m"}, {"text": "口コミいただけると嬉しいです」", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ スタッフの声かけを統一", "size": "l"}, {"text": ""}, {"text": "全員が同じタイミングで", "size": "m"}, {"text": "同じ言葉で依頼する", "size": "m"}, {"text": ""}, {"text": "仕組みにすると継続する", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "レビューは「待つ」のではなく", "size": "m"}, {"text": "「導線を作る」", "size": "m"}, {"text": ""}, {"text": "仕組みで増やせ", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/f4_example.png", "具体事例：レビュー導線", ["レジ横：QRコード設置", "仕上げ後：「口コミお願いします」", "カード：URL付きサンクスカード", "→ 月間レビュー数3倍"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("導線", "レビュー導線を作れ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①QRコードを設置する", "②満足度が高い瞬間に頼む", "③スタッフの声かけを統一"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ F-4 complete! Check {output_dir}/")
    return output_dir


def generate_g1():
    """G-1: 新規客の第一印象は30秒で決まる"""
    output_dir = "output/g1_first_impression"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("第一印象は", "30秒", "で決まる", "", "REPEAT DESIGN", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "技術がどれだけ上手くても", "size": "l"}, {"text": ""}, {"text": "最初の30秒で「合わない」と", "size": "m"}, {"text": "思われたら次はない", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "人は最初の印象を", "size": "l"}, {"text": "覆すのが苦手", "size": "l"}, {"text": ""}, {"text": "初頭効果", "size": "xl", "highlight": True}, {"text": ""}, {"text": "第一印象がその後を支配する", "size": "m"}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① 名前を呼んで迎える", "size": "l"}, {"text": ""}, {"text": "「〇〇様、お待ちしておりました」", "size": "m"}, {"text": ""}, {"text": "名前を呼ぶだけで特別感が出る", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② 席まで案内する", "size": "l"}, {"text": ""}, {"text": "「お荷物こちらにどうぞ」", "size": "m"}, {"text": ""}, {"text": "放置せず、最初から丁寧に導く", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ 最初にドリンクを出す", "size": "l"}, {"text": ""}, {"text": "「お飲み物いかがですか？」", "size": "m"}, {"text": ""}, {"text": "緊張をほぐすきっかけになる", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "技術の前に「迎え方」を磨け", "size": "m"}, {"text": ""}, {"text": "30秒で決まる", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/g1_example.png", "具体事例：迎え方", ["入口：名前を呼んで迎える", "→ 席まで案内する", "→ 荷物を預かる", "→ ドリンクを出す", "→ 30秒で好印象"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("迎接", "最初の30秒を設計しろ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①名前を呼んで迎える", "②席まで丁寧に案内する", "③最初にドリンクを出す"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ G-1 complete! Check {output_dir}/")
    return output_dir


def generate_g2():
    """G-2: 名前を呼ぶ回数と親密度の関係"""
    output_dir = "output/g2_name_recall"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("親密度を上げるなら", "名前", "を呼べ", "", "REPEAT DESIGN", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "「お客様」と呼んでいない？", "size": "l"}, {"text": ""}, {"text": "それ、距離が縮まらない原因", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "名前を呼ぶと", "size": "l"}, {"text": "脳は「特別扱い」と認識する", "size": "l"}, {"text": ""}, {"text": "カクテルパーティー効果", "size": "xl", "highlight": True}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① 施術中に3回は名前を呼ぶ", "size": "l"}, {"text": ""}, {"text": "「〇〇さんの髪質なら…」", "size": "m"}, {"text": ""}, {"text": "自然な文脈で名前を入れる", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② お見送りで名前を呼ぶ", "size": "l"}, {"text": ""}, {"text": "「〇〇さん、ありがとうございました」", "size": "m"}, {"text": ""}, {"text": "最後の印象が記憶に残る", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ 次回予約で名前を使う", "size": "l"}, {"text": ""}, {"text": "「〇〇さん、次回は3週間後が", "size": "m"}, {"text": "おすすめです」", "size": "m"}, {"text": ""}, {"text": "名前＋提案で特別感が増す", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "「お客様」ではなく名前で呼べ", "size": "m"}, {"text": ""}, {"text": "名前は最強の接客ツール", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/g2_example.png", "具体事例：名前の使い方", ["①「〇〇さんの髪質なら…」", "②「〇〇さん、いい色ですね」", "③「〇〇さん、ありがとうございました」", "→ 3回呼ぶだけで親密度UP"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("名前", "名前を3回呼べ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①施術中に3回は名前を呼ぶ", "②お見送りで名前を呼ぶ", "③次回予約で名前を使う"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ G-2 complete! Check {output_dir}/")
    return output_dir


def generate_g3():
    """G-3: 初回クーポンが「リピートを殺す」理由"""
    output_dir = "output/g3_coupon_trap"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("初回クーポンが", "リピート", "を殺す", "", "REPEAT DESIGN", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "初回50%OFFで集客していない？", "size": "l"}, {"text": ""}, {"text": "それ、リピートしない客を", "size": "m"}, {"text": "集めている", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "大幅割引で来た客は", "size": "l"}, {"text": "「安いから来た」だけ", "size": "l"}, {"text": ""}, {"text": "価格アンカリングの罠", "size": "xl", "highlight": True}, {"text": ""}, {"text": "正規料金に戻ると「高い」と感じる", "size": "m"}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① 割引率を下げる", "size": "l"}, {"text": ""}, {"text": "50%OFF → 20%OFFに変更", "size": "m"}, {"text": ""}, {"text": "価格差が小さいほど", "size": "m"}, {"text": "リピート率が上がる", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② 割引ではなく「体験」を付ける", "size": "l"}, {"text": ""}, {"text": "「初回限定：ヘッドスパ体験付き」", "size": "m"}, {"text": ""}, {"text": "価格を下げず価値を上げる", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ 2回目の来店動機を作る", "size": "l"}, {"text": ""}, {"text": "「次回使えるケアチケット」", "size": "m"}, {"text": ""}, {"text": "初回の特典ではなく", "size": "m"}, {"text": "2回目の理由を設計する", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "初回割引は「安い客」を集める", "size": "m"}, {"text": ""}, {"text": "2回目の仕掛けを設計しろ", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/g3_example.png", "具体事例：初回設計", ["初回：ヘッドスパ体験を無料追加", "→ 価格は正規のまま", "2回目：ケアチケット配布", "→ リピート率40%→65%"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("罠避", "安売りをやめろ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①割引率を下げる", "②割引ではなく体験を付ける", "③2回目の来店動機を作る"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ G-3 complete! Check {output_dir}/")
    return output_dir


def generate_g4():
    """G-4: 来店後24時間以内のDMがリピートを決める"""
    output_dir = "output/g4_follow_up_dm"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("リピートを決めるのは", "24時間", "以内のDM", "", "REPEAT DESIGN", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "来店後、何もフォローしていない？", "size": "l"}, {"text": ""}, {"text": "それ、忘れられている", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "来店後24時間以内に", "size": "l"}, {"text": "接触すると記憶が強化される", "size": "l"}, {"text": ""}, {"text": "記憶の定着", "size": "xl", "highlight": True}, {"text": ""}, {"text": "忘却曲線に逆らう方法", "size": "m"}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① 当日中にお礼DMを送る", "size": "l"}, {"text": ""}, {"text": "「今日はありがとうございました」", "size": "m"}, {"text": ""}, {"text": "短くていい、存在を思い出させる", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② ケアのアドバイスを添える", "size": "l"}, {"text": ""}, {"text": "「今夜のシャンプーは優しめに♪」", "size": "m"}, {"text": ""}, {"text": "プロとしての価値を伝える", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ 次回の提案を入れる", "size": "l"}, {"text": ""}, {"text": "「3週間後がベストタイミングです」", "size": "m"}, {"text": ""}, {"text": "次回来店の理由と時期を明確に", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "来店後が勝負", "size": "m"}, {"text": ""}, {"text": "24時間以内にDMを送れ", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/g4_example.png", "具体事例：フォローDM", ["当日夜：お礼メッセージ", "翌日：スタイリングTips", "1週間後：調子いかがですか？", "→ 次回予約率が2倍に"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("追跡", "24時間以内に動け", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①当日中にお礼DMを送る", "②ケアのアドバイスを添える", "③次回の提案を入れる"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ G-4 complete! Check {output_dir}/")
    return output_dir


def generate_g5():
    """G-5: 2回目来店時に「宿題」を出す"""
    output_dir = "output/g5_homework"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("2回目の来店で", "宿題", "を出す", "", "REPEAT DESIGN", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "2回目に来たお客様に", "size": "l"}, {"text": "何もしなければ3回目はない", "size": "l"}, {"text": ""}, {"text": "2→3回目が最難関", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "「宿題」を出すと", "size": "l"}, {"text": "次回来る理由ができる", "size": "l"}, {"text": ""}, {"text": "コミットメント効果", "size": "xl", "highlight": True}, {"text": ""}, {"text": "小さな約束が行動を促す", "size": "m"}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① ケア方法を教える", "size": "l"}, {"text": ""}, {"text": "「このドライヤーの当て方で", "size": "m"}, {"text": "持ちが全然変わりますよ」", "size": "m"}, {"text": ""}, {"text": "実践→結果確認の理由ができる", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② 経過観察を約束する", "size": "l"}, {"text": ""}, {"text": "「3週間後にカラーの様子、", "size": "m"}, {"text": "見せてくださいね」", "size": "m"}, {"text": ""}, {"text": "「見せに行く」理由ができる", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ 次のステップを提示", "size": "l"}, {"text": ""}, {"text": "「今日のケアが定着したら", "size": "m"}, {"text": "次はパーマもいけますよ」", "size": "m"}, {"text": ""}, {"text": "未来のビジョンを見せる", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "2回目の来店が終わりではない", "size": "m"}, {"text": ""}, {"text": "宿題で3回目を設計しろ", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/g5_example.png", "具体事例：宿題の出し方", ["「ドライヤーの当て方、", "試してみてくださいね」", "「3週間後に経過見せてください」", "→ 3回目来店率UP"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("宿題", "宿題で3回目を作れ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①ケア方法を教える", "②経過観察を約束する", "③次のステップを提示する"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ G-5 complete! Check {output_dir}/")
    return output_dir


def generate_h1():
    """H-1: 「見て覚えろ」が通用しない科学的理由"""
    output_dir = "output/h1_training_science"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("「見て覚えろ」は", "通用", "しない", "", "STAFF TRAINING", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "「背中を見て学べ」", "size": "l"}, {"text": ""}, {"text": "それ、教育ではなく放置", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "人は「見る」だけでは", "size": "l"}, {"text": "20%しか覚えない", "size": "l"}, {"text": ""}, {"text": "学習の定着率", "size": "xl", "highlight": True}, {"text": ""}, {"text": "やって教えて初めて身につく", "size": "m"}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① 手順を言語化する", "size": "l"}, {"text": ""}, {"text": "感覚ではなく手順で伝える", "size": "m"}, {"text": ""}, {"text": "「なぜそうするか」を明確に", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② やらせて見守る", "size": "l"}, {"text": ""}, {"text": "実際にやらせてから", "size": "m"}, {"text": "フィードバックする", "size": "m"}, {"text": ""}, {"text": "体験×指導が最強の組み合わせ", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ チェックリストを作る", "size": "l"}, {"text": ""}, {"text": "毎回同じ基準で確認できる", "size": "m"}, {"text": ""}, {"text": "属人化を防ぎ、質を安定させる", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "「見て覚えろ」は教育ではない", "size": "m"}, {"text": ""}, {"text": "言語化し、やらせ、確認しろ", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/h1_example.png", "具体事例：教育の3ステップ", ["①手順書で説明する", "②実際にやらせる", "③チェックリストで確認", "→ 習得速度が2倍に"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("教育", "見せるな、やらせろ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①手順を言語化する", "②やらせて見守る", "③チェックリストで確認する"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ H-1 complete! Check {output_dir}/")
    return output_dir


def generate_h2():
    """H-2: フィードバックは24時間以内が鉄則"""
    output_dir = "output/h2_feedback_timing"
    os.makedirs(output_dir, exist_ok=True)
    create_title_slide_two_line("フィードバックは", "24時間", "以内", "", "STAFF TRAINING", f"{output_dir}/slide_01.png")
    create_content_slide([{"text": "「後で言おう」と思ったまま", "size": "l"}, {"text": "忘れていない？", "size": "l"}, {"text": ""}, {"text": "遅いフィードバックは意味がない", "size": "m", "highlight": True}], f"{output_dir}/slide_02.png")
    create_content_slide([{"text": "フィードバックは", "size": "l"}, {"text": "行動の直後が最も効果的", "size": "l"}, {"text": ""}, {"text": "即時フィードバック", "size": "xl", "highlight": True}, {"text": ""}, {"text": "時間が経つほど効果が薄れる", "size": "m"}], f"{output_dir}/slide_03.png")
    create_content_slide([{"text": "① 良い行動はその場で褒める", "size": "l"}, {"text": ""}, {"text": "「今の声かけ、すごく良かった」", "size": "m"}, {"text": ""}, {"text": "即時の承認が行動を強化する", "size": "m", "highlight": True}], f"{output_dir}/slide_04.png")
    create_content_slide([{"text": "② 改善点は1対1で伝える", "size": "l"}, {"text": ""}, {"text": "人前では褒め、改善は個別に", "size": "m"}, {"text": ""}, {"text": "心理的安全性を守る", "size": "m"}], f"{output_dir}/slide_05.png")
    create_content_slide([{"text": "③ 「次はこうしよう」で終わる", "size": "l"}, {"text": ""}, {"text": "指摘だけではなく", "size": "m"}, {"text": "次のアクションを明確に", "size": "m"}, {"text": ""}, {"text": "建設的に終わると行動が変わる", "size": "m", "highlight": True}], f"{output_dir}/slide_06.png")
    create_content_slide([{"text": "つまり", "size": "l"}, {"text": ""}, {"text": "フィードバックは鮮度が命", "size": "m"}, {"text": ""}, {"text": "24時間以内に伝えろ", "size": "xl", "highlight": True}], f"{output_dir}/slide_07.png")
    create_example_slide("assets/isometric/h2_example.png", "具体事例：即時FB", ["良い行動：その場で「今の良かった」", "改善点：終業後に1対1で", "「次はこうしてみよう」で終わる", "→ スタッフの成長速度UP"], f"{output_dir}/slide_08.png")
    create_vertical_text_slide("即応", "その日のうちに伝えろ", f"{output_dir}/slide_09.png")
    create_cta_slide("保存して振り返ってね", ["①良い行動はその場で褒める", "②改善点は1対1で伝える", "③次のアクションを明確にする"], "Fleeksオンラインセミナーの内容を抜粋しています", f"{output_dir}/slide_10.png")
    print(f"\n✅ H-2 complete! Check {output_dir}/")
    return output_dir


def generate_all():
    """Generate all days"""
    generate_day1()
    generate_day2()
    generate_day3()
    generate_day4()
    generate_day5()
    generate_day6()
    generate_day7()
    generate_day8()
    generate_day9()
    generate_day10()
    generate_day11()
    generate_day12()
    generate_day13()
    generate_day14()
    generate_day15()
    generate_a1()
    generate_a2()
    generate_a3()
    generate_a4()
    generate_a5()
    generate_b1()
    generate_b2()
    generate_b3()
    generate_b4()
    generate_b5()
    generate_c1()
    generate_c2()
    generate_c3()
    generate_c4()
    generate_d1()
    generate_d2()
    generate_d3()
    generate_d4()
    generate_e1()
    generate_e2()
    generate_e3()
    generate_e4()
    generate_e5()
    generate_f1()
    generate_f2()
    generate_f3()
    generate_f4()
    generate_g1()
    generate_g2()
    generate_g3()
    generate_g4()
    generate_g5()
    generate_h1()
    generate_h2()
    print("\n🎉 All days complete!")


def generate_b_series():
    """Generate B series (B-1 to B-5)"""
    generate_b1()
    generate_b2()
    generate_b3()
    generate_b4()
    generate_b5()
    print("\n🎉 B series complete!")


def generate_c_series():
    """Generate C series (C-1 to C-4)"""
    generate_c1()
    generate_c2()
    generate_c3()
    generate_c4()
    print("\n🎉 C series complete!")


def generate_d_series():
    """Generate D series (D-1 to D-4)"""
    generate_d1()
    generate_d2()
    generate_d3()
    generate_d4()
    print("\n🎉 D series complete!")


def generate_e_series():
    """Generate E series (E-1 to E-5)"""
    generate_e1()
    generate_e2()
    generate_e3()
    generate_e4()
    generate_e5()
    print("\n🎉 E series complete!")


def generate_f_series():
    """Generate F series (F-1 to F-4)"""
    generate_f1()
    generate_f2()
    generate_f3()
    generate_f4()
    print("\n🎉 F series complete!")


def generate_g_series():
    """Generate G series (G-1 to G-5)"""
    generate_g1()
    generate_g2()
    generate_g3()
    generate_g4()
    generate_g5()
    print("\n🎉 G series complete!")


def generate_h_series():
    """Generate H series (H-1 to H-2)"""
    generate_h1()
    generate_h2()
    print("\n🎉 H series complete!")


def generate_d_to_h():
    """Generate all D through H series"""
    generate_d_series()
    generate_e_series()
    generate_f_series()
    generate_g_series()
    generate_h_series()
    print("\n🎉 D-H series all complete!")


if __name__ == "__main__":
    generate_d_to_h()


