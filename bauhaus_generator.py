"""
Instagram Image Generator - Full Bauhaus Style
All slides with geometric accents, bold asymmetry, visual tension
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
IMAGE_SIZE = (1080, 1080)
MARGIN = 80
MAX_TEXT_WIDTH = IMAGE_SIZE[0] - (MARGIN * 2)

COLORS = {
    "background": "#FFFFFF",
    "text": "#000000",
    "accent_yellow": "#FFE500",
    "accent_red": "#FF3333",
    "gray": "#666666",
}

FONTS = {
    "black": "fonts/NotoSansJP-Black.ttf",
    "thin": "fonts/NotoSansJP-Thin.ttf",
}


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def get_font(font_path, size):
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()


def fit_text_to_width(draw, text, font_path, max_size, max_width):
    size = max_size
    while size > 20:
        font = get_font(font_path, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            return font, size
        size -= 4
    return get_font(font_path, 20), 20


def create_bauhaus_slide_1(main_text, sub_text, english_text, output_path, accent_color="yellow"):
    """Slide 1: Maximum impact, huge text, geometric accent"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    font_main, _ = fit_text_to_width(draw, main_text, FONTS["black"], 200, MAX_TEXT_WIDTH - 40)
    font_sub = get_font(FONTS["black"], 48)
    font_english = get_font(FONTS["thin"], 36)
    
    accent = hex_to_rgb(COLORS["accent_yellow"] if accent_color == "yellow" else COLORS["accent_red"])
    
    main_bbox = draw.textbbox((0, 0), main_text, font=font_main)
    main_height = main_bbox[3] - main_bbox[1]
    main_width = main_bbox[2] - main_bbox[0]
    
    # Large geometric rectangle
    draw.rectangle([60, 280, 60 + main_width + 40, 280 + main_height + 40], fill=accent)
    
    # Main text
    draw.text((80, 300), main_text, font=font_main, fill=hex_to_rgb(COLORS["text"]))
    
    # Sub text
    draw.text((85, 300 + main_height + 60), sub_text, font=font_sub, fill=hex_to_rgb(COLORS["text"]))
    
    # English
    eng_bbox = draw.textbbox((0, 0), english_text, font=font_english)
    draw.text((IMAGE_SIZE[0] - (eng_bbox[2] - eng_bbox[0]) - 80, IMAGE_SIZE[1] - 120), 
              english_text, font=font_english, fill=hex_to_rgb(COLORS["gray"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_bauhaus_slide(lines, output_path, accent_type="bar", highlight_line=None):
    """
    Bauhaus style slide with geometric accents
    accent_type: "bar" (top bar), "block" (side block), "corner" (corner triangle)
    """
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    yellow = hex_to_rgb(COLORS["accent_yellow"])
    red = hex_to_rgb(COLORS["accent_red"])
    
    # Geometric accent based on type
    if accent_type == "bar":
        draw.rectangle([0, 0, IMAGE_SIZE[0], 25], fill=yellow)
    elif accent_type == "block":
        draw.rectangle([0, 200, 30, 880], fill=red)
    elif accent_type == "corner":
        draw.polygon([(0, 0), (200, 0), (0, 200)], fill=yellow)
    elif accent_type == "bottom":
        draw.rectangle([0, IMAGE_SIZE[1] - 25, IMAGE_SIZE[0], IMAGE_SIZE[1]], fill=yellow)
    elif accent_type == "dual":
        draw.rectangle([0, 0, IMAGE_SIZE[0], 15], fill=yellow)
        draw.rectangle([0, IMAGE_SIZE[1] - 15, IMAGE_SIZE[0], IMAGE_SIZE[1]], fill=red)
    
    # Calculate lines
    line_data = []
    line_spacing = 25
    
    for i, line in enumerate(lines):
        if not line:
            line_data.append({"text": "", "height": 35, "font": None, "width": 0})
            continue
        
        # First line larger
        if i == 0:
            base_size = 72
        elif line.startswith("・") or line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
            base_size = 44
        else:
            base_size = 52
        
        font, _ = fit_text_to_width(draw, line, FONTS["black"], base_size, MAX_TEXT_WIDTH - 60)
        bbox = draw.textbbox((0, 0), line, font=font)
        line_data.append({
            "text": line, 
            "font": font, 
            "height": bbox[3] - bbox[1], 
            "width": bbox[2] - bbox[0]
        })
    
    total_height = sum(ld["height"] + line_spacing for ld in line_data) - line_spacing
    start_y = (IMAGE_SIZE[1] - total_height) // 2
    
    current_y = start_y
    for i, ld in enumerate(line_data):
        if not ld["text"]:
            current_y += ld["height"]
            continue
        
        x = MARGIN + 20  # Asymmetric left position
        
        # Highlight specific line
        if highlight_line is not None and i == highlight_line:
            padding = 10
            draw.rectangle(
                [x - padding, current_y - padding, x + ld["width"] + padding, current_y + ld["height"] + padding],
                fill=yellow
            )
        
        draw.text((x, current_y), ld["text"], font=ld["font"], fill=hex_to_rgb(COLORS["text"]))
        current_y += ld["height"] + line_spacing
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_bauhaus_cta(main_cta, preview_lines, follow_text, output_path):
    """CTA slide with bold Bauhaus treatment"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    yellow = hex_to_rgb(COLORS["accent_yellow"])
    red = hex_to_rgb(COLORS["accent_red"])
    
    # Top and bottom bars
    draw.rectangle([0, 0, IMAGE_SIZE[0], 30], fill=yellow)
    draw.rectangle([0, IMAGE_SIZE[1] - 30, IMAGE_SIZE[0], IMAGE_SIZE[1]], fill=red)
    
    # CTA text with background
    font_cta, _ = fit_text_to_width(draw, main_cta, FONTS["black"], 64, MAX_TEXT_WIDTH - 60)
    cta_bbox = draw.textbbox((0, 0), main_cta, font=font_cta)
    cta_width = cta_bbox[2] - cta_bbox[0]
    cta_height = cta_bbox[3] - cta_bbox[1]
    cta_x = (IMAGE_SIZE[0] - cta_width) // 2
    cta_y = 280
    
    draw.rectangle(
        [cta_x - 25, cta_y - 20, cta_x + cta_width + 25, cta_y + cta_height + 20],
        fill=yellow
    )
    draw.text((cta_x, cta_y), main_cta, font=font_cta, fill=hex_to_rgb(COLORS["text"]))
    
    # Preview lines
    font_preview = get_font(FONTS["black"], 40)
    preview_y = 450
    for i, line in enumerate(preview_lines):
        font_line, _ = fit_text_to_width(draw, line, FONTS["black"], 40, MAX_TEXT_WIDTH)
        bbox = draw.textbbox((0, 0), line, font=font_line)
        line_x = (IMAGE_SIZE[0] - (bbox[2] - bbox[0])) // 2
        draw.text((line_x, preview_y + i * 65), line, font=font_line, fill=hex_to_rgb(COLORS["text"]))
    
    # Follow text
    font_follow = get_font(FONTS["thin"], 36)
    follow_bbox = draw.textbbox((0, 0), follow_text, font=font_follow)
    follow_x = (IMAGE_SIZE[0] - (follow_bbox[2] - follow_bbox[0])) // 2
    draw.text((follow_x, IMAGE_SIZE[1] - 120), follow_text, font=font_follow, fill=hex_to_rgb(COLORS["gray"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def generate_post_1_bauhaus():
    """Generate all 10 slides in full Bauhaus style"""
    output_dir = "output/post1_ai_bauhaus"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1
    create_bauhaus_slide_1(
        main_text="使えない",
        sub_text="その常識を疑え",
        english_text="AI",
        output_path=f"{output_dir}/slide_01.png"
    )
    
    # Slide 2 - corner accent
    create_bauhaus_slide(
        lines=["AIは難しそう", "プログラミングが必要", "自分には関係ない", "", "そう思っていませんか？"],
        output_path=f"{output_dir}/slide_02.png",
        accent_type="corner"
    )
    
    # Slide 3 - block accent
    create_bauhaus_slide(
        lines=["9割の美容師が", "損をしている", "", "知らないだけで", "毎月10時間を失っている"],
        output_path=f"{output_dir}/slide_03.png",
        accent_type="block",
        highlight_line=0
    )
    
    # Slide 4
    create_bauhaus_slide(
        lines=["ChatGPTは", "「質問するだけ」で使える", "", "必要なのは", "スマホと日本語だけ"],
        output_path=f"{output_dir}/slide_04.png",
        accent_type="bar",
        highlight_line=1
    )
    
    # Slide 5
    create_bauhaus_slide(
        lines=["美容師がAIに", "任せるべきこと", "", "・キャプション作成", "・お客様への返信文", "・メニュー説明文", "・ブログのたたき"],
        output_path=f"{output_dir}/slide_05.png",
        accent_type="dual"
    )
    
    # Slide 6
    create_bauhaus_slide(
        lines=["キャプション作成の例", "", "「今日のカラーについて", "文章を書いて」", "", "→ 30秒で完成"],
        output_path=f"{output_dir}/slide_06.png",
        accent_type="corner",
        highlight_line=5
    )
    
    # Slide 7
    create_bauhaus_slide(
        lines=["今日から使える", "3つのプロンプト", "", "1. 説明文を書いて", "2. もっと短くして", "3. 返信を考えて"],
        output_path=f"{output_dir}/slide_07.png",
        accent_type="block"
    )
    
    # Slide 8
    create_bauhaus_slide(
        lines=["始め方は簡単", "", "1. アプリをダウンロード", "2. Googleでログイン", "3. 日本語で質問するだけ"],
        output_path=f"{output_dir}/slide_08.png",
        accent_type="bar"
    )
    
    # Slide 9
    create_bauhaus_slide(
        lines=["使わない理由が", "「難しそう」なら", "", "今日で終わりにしよう"],
        output_path=f"{output_dir}/slide_09.png",
        accent_type="dual",
        highlight_line=3
    )
    
    # Slide 10 - CTA
    create_bauhaus_cta(
        main_cta="保存して今日から実践",
        preview_lines=["明日はインスタ集客の真実", "フォロワー数より大事な数字がある"],
        follow_text="フォローで見逃さない",
        output_path=f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ Post 1 Bauhaus version complete! Check {output_dir}/")
    return output_dir


if __name__ == "__main__":
    generate_post_1_bauhaus()
