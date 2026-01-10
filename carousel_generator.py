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
        
        # Highlight background
        if ld.get("highlight"):
            padding = 12
            draw.rectangle([
                x - padding, 
                current_y - padding,
                x + ld["width"] + padding,
                current_y + ld["height"] + padding
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
        "詳しくはFleeksで →",
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
        "詳しくはFleeksで →",
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
        "詳しくはFleeksで →",
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
        "詳しくはFleeksで →",
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
        "詳しくはFleeksで →",
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
        "詳しくはFleeksで →",
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
        "詳しくはFleeksで →",
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
        "詳しくはFleeksで →",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ Day 8 complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_day9():
    """Day 9: 丁寧すぎる接客が失客の原因（返報性の原理）- 15枚版"""
    output_dir = "output/day9_reciprocity"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル
    create_title_slide_two_line(
        "良かれと思ってやってた",
        "丁寧すぎ",
        "は失客する",
        "尽くしすぎが逆効果な理由",
        "RECIPROCITY",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. ストーリー開始
    create_content_slide([
        {"text": "お客様のために...", "size": "l"},
        {"text": ""},
        {"text": "お茶菓子をサービス", "size": "m"},
        {"text": "マッサージを延長", "size": "m"},
        {"text": "おまけのトリートメント", "size": "m"},
        {"text": ""},
        {"text": "喜んでくれるはず！", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 悲劇
    create_content_slide([
        {"text": "なのに...", "size": "xl"},
        {"text": ""},
        {"text": "「ありがとうございます！」", "size": "m"},
        {"text": "と笑顔で帰ったお客様が", "size": "m"},
        {"text": ""},
        {"text": "二度と来ない", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 疑問
    create_content_slide([
        {"text": "「なぜ？」", "size": "xl"},
        {"text": ""},
        {"text": "嫌な顔はしてなかった", "size": "m"},
        {"text": "むしろ感謝してくれた", "size": "m"},
        {"text": ""},
        {"text": "尽くしたのに、なぜ？", "size": "m"},
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
        "詳しくはFleeksで →",
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
        "詳しくはFleeksで →",
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
        "「口コミ書いてね」と言っても",
        "書いて",
        "もらえない理由",
        "たった1つの変化で5倍に",
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
    
    # 11. 効果
    create_content_slide([
        {"text": "すると...", "size": "l"},
        {"text": ""},
        {"text": "口コミ数が", "size": "m"},
        {"text": "5倍になった", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "ハードルを下げるだけで変わる", "size": "m"},
    ], f"{output_dir}/slide_11.png")
    
    # 12. 重要ポイント
    create_content_slide([
        {"text": "重要なのは", "size": "l"},
        {"text": ""},
        {"text": "「後で」を「今」に変える", "size": "xl"},
        {"text": ""},
        {"text": "今やらないと", "size": "m"},
        {"text": "永遠にやらない", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_12.png")
    
    # 13. 比較
    create_content_slide([
        {"text": "Before → After", "size": "l"},
        {"text": ""},
        {"text": "❌「口コミお願いします」（曖昧）", "size": "m"},
        {"text": ""},
        {"text": "⭕️「今ここで1分で書けますよ」", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "まとめ", "size": "l"},
        {"text": ""},
        {"text": "① その場でQRコードを見せる", "size": "m"},
        {"text": "② 何を書けばいいか伝える", "size": "m"},
        {"text": "③ 他の人の口コミを見せる", "size": "m"},
        {"text": ""},
        {"text": "ハードルを下げる＝行動が増える", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["QRコードを用意する", "書き方を伝える", "その場でお願いする"],
        "詳しくはFleeksで →",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ Day 11 complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_day12():
    """Day 12: 指名されない本当の理由（単純接触効果）- 15枚版"""
    output_dir = "output/day12_shimei"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル
    create_title_slide(
        "指名率20%だった私が,80%になった話",
        "たった一つの習慣",
        "MERE EXPOSURE",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. ストーリー開始
    create_content_slide([
        {"text": "フリーになって1年目", "size": "l"},
        {"text": ""},
        {"text": "技術には自信があった", "size": "m"},
        {"text": "でも指名が全然つかない", "size": "m"},
        {"text": ""},
        {"text": "指名率はたった20%", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 悩み
    create_content_slide([
        {"text": "「なぜ？」", "size": "xl"},
        {"text": ""},
        {"text": "施術は褒められる", "size": "m"},
        {"text": "リピートもしてくれる", "size": "m"},
        {"text": ""},
        {"text": "でも「誰でもいい」と言われる", "size": "m"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 心理学解説
    create_content_slide([
        {"text": "心理学で言う", "size": "l"},
        {"text": ""},
        {"text": "単純接触効果", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "人は接触回数が多いほど", "size": "m"},
        {"text": "好感度が上がる", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. 問題
    create_content_slide([
        {"text": "つまり...", "size": "l"},
        {"text": ""},
        {"text": "月1回の施術だけでは", "size": "m"},
        {"text": "接触が少なすぎる", "size": "xl"},
        {"text": ""},
        {"text": "印象に残らない", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # 6. 気づき
    create_content_slide([
        {"text": "気づいた", "size": "l"},
        {"text": ""},
        {"text": "来店以外の接点を", "size": "m"},
        {"text": "増やす必要がある", "size": "xl"},
        {"text": ""},
        {"text": "「思い出してもらう」機会を作る", "size": "m"},
    ], f"{output_dir}/slide_06.png")
    
    # 7. 転換
    create_vertical_text_slide("接触", "来店以外で会え", f"{output_dir}/slide_07.png")
    
    # 8. 解決策①
    create_content_slide([
        {"text": "解決策①", "size": "l"},
        {"text": ""},
        {"text": "インスタのストーリーズ更新", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "毎日見てもらえる", "size": "m"},
        {"text": "「また見た」が好感に変わる", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # 9. 解決策②
    create_content_slide([
        {"text": "解決策②", "size": "l"},
        {"text": ""},
        {"text": "来店後フォローメッセージ", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「調子どうですか？」", "size": "m"},
        {"text": "「気になることあればぜひ」", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # 10. 解決策③
    create_content_slide([
        {"text": "解決策③", "size": "l"},
        {"text": ""},
        {"text": "次回予約のリマインド", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「そろそろいかがですか？」", "size": "m"},
        {"text": "思い出させるきっかけに", "size": "m"},
    ], f"{output_dir}/slide_10.png")
    
    # 11. 効果
    create_content_slide([
        {"text": "すると...", "size": "l"},
        {"text": ""},
        {"text": "指名率が", "size": "m"},
        {"text": "20% → 80%に", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「〇〇さんにお願いしたい」が増えた", "size": "m"},
    ], f"{output_dir}/slide_11.png")
    
    # 12. 重要ポイント
    create_content_slide([
        {"text": "重要なのは", "size": "l"},
        {"text": ""},
        {"text": "「上手い」だけじゃ足りない", "size": "m"},
        {"text": ""},
        {"text": "「思い出してもらう」回数を増やす", "size": "xl"},
    ], f"{output_dir}/slide_12.png")
    
    # 13. 比較
    create_content_slide([
        {"text": "Before → After", "size": "l"},
        {"text": ""},
        {"text": "❌ 月1回の来店だけ", "size": "m"},
        {"text": "→ 忘れられる", "size": "m"},
        {"text": ""},
        {"text": "⭕️ 週3回ストーリーズに登場", "size": "m"},
        {"text": "→ 覚えてもらえる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "まとめ", "size": "l"},
        {"text": ""},
        {"text": "① ストーリーズを更新する", "size": "m"},
        {"text": "② フォローメッセージを送る", "size": "m"},
        {"text": "③ リマインドを忘れない", "size": "m"},
        {"text": ""},
        {"text": "接触回数＝指名率", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["ストーリーズを毎日更新", "フォローメッセージを送る", "接触回数を増やす"],
        "詳しくはFleeksで →",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ Day 12 complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_day13():
    """Day 13: 時間に追われる働き方（パーキンソンの法則）- 15枚版"""
    output_dir = "output/day13_jikan"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル
    create_title_slide_two_line(
        "営業時間を2時間減らしたら",
        "売上が",
        "上がった話",
        "なぜ短くすると増える？",
        "PARKINSON",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. ストーリー開始
    create_content_slide([
        {"text": "朝9時から夜9時まで", "size": "l"},
        {"text": ""},
        {"text": "毎日12時間働いていた", "size": "m"},
        {"text": ""},
        {"text": "でも売上は頭打ち", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 悩み
    create_content_slide([
        {"text": "体も心も限界", "size": "l"},
        {"text": ""},
        {"text": "「これ以上無理...」", "size": "m"},
        {"text": "「でも予約があるし...」", "size": "m"},
        {"text": ""},
        {"text": "どうすればいい？", "size": "xl"},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 心理学解説
    create_content_slide([
        {"text": "心理学で言う", "size": "l"},
        {"text": ""},
        {"text": "パーキンソンの法則", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "仕事は与えられた時間いっぱいに", "size": "m"},
        {"text": "膨張する", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. 問題
    create_content_slide([
        {"text": "つまり...", "size": "l"},
        {"text": ""},
        {"text": "12時間あるから", "size": "m"},
        {"text": "12時間使ってしまう", "size": "xl"},
        {"text": ""},
        {"text": "ダラダラと仕事が伸びる", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # 6. 実験
    create_content_slide([
        {"text": "試しに...", "size": "l"},
        {"text": ""},
        {"text": "営業時間を10時間に", "size": "m"},
        {"text": "減らしてみた", "size": "m"},
        {"text": ""},
        {"text": "最初は怖かった", "size": "xl"},
    ], f"{output_dir}/slide_06.png")
    
    # 7. 転換
    create_vertical_text_slide("集中", "短くすれば密度が上がる", f"{output_dir}/slide_07.png")
    
    # 8. 変化①
    create_content_slide([
        {"text": "変化①", "size": "l"},
        {"text": ""},
        {"text": "予約を詰められるようになった", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "空き時間が減った", "size": "m"},
        {"text": "効率が上がった", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # 9. 変化②
    create_content_slide([
        {"text": "変化②", "size": "l"},
        {"text": ""},
        {"text": "「予約取れない」感が出た", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「早く予約しないと」", "size": "m"},
        {"text": "次回予約率が上がった", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # 10. 変化③
    create_content_slide([
        {"text": "変化③", "size": "l"},
        {"text": ""},
        {"text": "自分の時間ができた", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "勉強、休息、家族との時間", "size": "m"},
        {"text": "心に余裕が生まれた", "size": "m"},
    ], f"{output_dir}/slide_10.png")
    
    # 11. 結果
    create_content_slide([
        {"text": "結果...", "size": "l"},
        {"text": ""},
        {"text": "2時間減らしたのに", "size": "m"},
        {"text": "売上は10%アップ", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "密度の高い働き方ができた", "size": "m"},
    ], f"{output_dir}/slide_11.png")
    
    # 12. 教訓
    create_content_slide([
        {"text": "教訓", "size": "l"},
        {"text": ""},
        {"text": "長く働く＝売上アップ", "size": "m"},
        {"text": "ではない", "size": "xl"},
        {"text": ""},
        {"text": "密度を上げることが大事", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_12.png")
    
    # 13. 比較
    create_content_slide([
        {"text": "Before → After", "size": "l"},
        {"text": ""},
        {"text": "❌ 12時間ダラダラ", "size": "m"},
        {"text": "→ 疲弊、売上頭打ち", "size": "m"},
        {"text": ""},
        {"text": "⭕️ 10時間集中", "size": "m"},
        {"text": "→ 効率UP、売上UP", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "まとめ", "size": "l"},
        {"text": ""},
        {"text": "① 営業時間を見直す", "size": "m"},
        {"text": "② 空き時間を減らす", "size": "m"},
        {"text": "③ 密度を上げる", "size": "m"},
        {"text": ""},
        {"text": "時間を制限すれば集中できる", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["営業時間を見直す", "予約を詰める", "密度を上げる"],
        "詳しくはFleeksで →",
        f"{output_dir}/slide_15.png"
    )
    
    print(f"\n✅ Day 13 complete! Check {output_dir}/ (15 slides)")
    return output_dir


def generate_day14():
    """Day 14: お客様が離れる瞬間（心理的安全性）- 15枚版"""
    output_dir = "output/day14_hanare"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. タイトル
    create_title_slide(
        "何か違うと言われない,たった1つの理由",
        "心理的安全性の魔法",
        "PSYCHOLOGICAL SAFETY",
        f"{output_dir}/slide_01.png"
    )
    
    # 2. ストーリー開始
    create_content_slide([
        {"text": "施術後...", "size": "l"},
        {"text": ""},
        {"text": "「うーん、何か違う...」", "size": "xl"},
        {"text": ""},
        {"text": "そう言われると心が折れる", "size": "m"},
    ], f"{output_dir}/slide_02.png")
    
    # 3. 悩み
    create_content_slide([
        {"text": "「何が違うの？」", "size": "l"},
        {"text": ""},
        {"text": "要望通りにやったのに", "size": "m"},
        {"text": "写真通りにカットしたのに", "size": "m"},
        {"text": ""},
        {"text": "なぜか満足してもらえない", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_03.png")
    
    # 4. 心理学解説
    create_content_slide([
        {"text": "心理学で言う", "size": "l"},
        {"text": ""},
        {"text": "心理的安全性", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "本音を言えない環境では", "size": "m"},
        {"text": "後から不満が出る", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # 5. 問題
    create_content_slide([
        {"text": "つまり...", "size": "l"},
        {"text": ""},
        {"text": "カウンセリング時に", "size": "m"},
        {"text": "本音を言えていなかった", "size": "xl"},
        {"text": ""},
        {"text": "結果、ズレが生まれる", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # 6. お客様の心理
    create_content_slide([
        {"text": "お客様の心理", "size": "l"},
        {"text": ""},
        {"text": "「こう言ったら失礼かな」", "size": "m"},
        {"text": "「プロに任せた方がいいかな」", "size": "m"},
        {"text": "「言いにくい...」", "size": "m"},
        {"text": ""},
        {"text": "遠慮して本音を言えない", "size": "xl", "highlight": True},
    ], f"{output_dir}/slide_06.png")
    
    # 7. 転換
    create_vertical_text_slide("安心", "本音を引き出せ", f"{output_dir}/slide_07.png")
    
    # 8. 解決策①
    create_content_slide([
        {"text": "解決策①", "size": "l"},
        {"text": ""},
        {"text": "「嫌なこと」を先に聞く", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「されたくないことありますか？」", "size": "m"},
        {"text": "「過去に失敗したことは？」", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # 9. 解決策②
    create_content_slide([
        {"text": "解決策②", "size": "l"},
        {"text": ""},
        {"text": "途中で確認する", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「ここまでどうですか？」", "size": "m"},
        {"text": "「気になるところあれば教えて」", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # 10. 解決策③
    create_content_slide([
        {"text": "解決策③", "size": "l"},
        {"text": ""},
        {"text": "「言いにくいことも言って」と伝える", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "「遠慮なく言ってくださいね」", "size": "m"},
        {"text": "「修正した方がいい場合もあるので」", "size": "m"},
    ], f"{output_dir}/slide_10.png")
    
    # 11. 効果
    create_content_slide([
        {"text": "すると...", "size": "l"},
        {"text": ""},
        {"text": "「何か違う」が", "size": "m"},
        {"text": "ほぼゼロになった", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "事前にズレを解消できるから", "size": "m"},
    ], f"{output_dir}/slide_11.png")
    
    # 12. 重要ポイント
    create_content_slide([
        {"text": "重要なのは", "size": "l"},
        {"text": ""},
        {"text": "技術を磨くより", "size": "m"},
        {"text": "本音を引き出す環境を作る", "size": "xl"},
        {"text": ""},
        {"text": "これが失客を防ぐ", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_12.png")
    
    # 13. 比較
    create_content_slide([
        {"text": "Before → After", "size": "l"},
        {"text": ""},
        {"text": "❌「お任せで」→ 後から不満", "size": "m"},
        {"text": ""},
        {"text": "⭕️「嫌なこと教えて」→ 事前に解消", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_13.png")
    
    # 14. まとめ
    create_content_slide([
        {"text": "まとめ", "size": "l"},
        {"text": ""},
        {"text": "① 「嫌なこと」を先に聞く", "size": "m"},
        {"text": "② 途中で確認する", "size": "m"},
        {"text": "③ 「言いにくいことも言って」と伝える", "size": "m"},
        {"text": ""},
        {"text": "安心感＝本音＝満足", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_14.png")
    
    # 15. CTA
    create_cta_slide(
        "保存して振り返ってね",
        ["嫌なことを先に聞く", "途中で確認する", "本音を引き出す"],
        "詳しくはFleeksで →",
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
        "詳しくはFleeksで →",
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
    print("\n🎉 All 15 days complete!")


if __name__ == "__main__":
    generate_all()


