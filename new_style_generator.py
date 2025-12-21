"""
Instagram Image Generator - Bauhaus/Swiss Style
New Economy Business Media Style for hairdressers
Auto-fits text to image bounds
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Configuration
IMAGE_SIZE = (1080, 1080)
MARGIN = 80  # Minimum margin from edges
MAX_TEXT_WIDTH = IMAGE_SIZE[0] - (MARGIN * 2)  # 920px

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
    "mincho": "fonts/ipaexm.ttf",
}


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def get_font(font_path, size):
    """Load font with fallback"""
    try:
        return ImageFont.truetype(font_path, size)
    except Exception as e:
        print(f"Font error: {e}")
        return ImageFont.load_default()


def fit_text_to_width(draw, text, font_path, max_size, max_width):
    """Reduce font size until text fits within max_width"""
    size = max_size
    while size > 20:
        font = get_font(font_path, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            return font, size
        size -= 4
    return get_font(font_path, 20), 20


def create_slide_1_bauhaus(main_text, sub_text, english_text, output_path, accent_color="yellow"):
    """
    Create Slide 1 in Bauhaus style - asymmetric, bold, impactful
    """
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    # Fit main text to width
    font_main, main_size = fit_text_to_width(draw, main_text, FONTS["black"], 200, MAX_TEXT_WIDTH - 40)
    font_sub = get_font(FONTS["black"], 48)
    font_english = get_font(FONTS["thin"], 36)
    
    # Accent color
    accent = hex_to_rgb(COLORS["accent_yellow"] if accent_color == "yellow" else COLORS["accent_red"])
    
    # Get main text dimensions
    main_bbox = draw.textbbox((0, 0), main_text, font=font_main)
    main_width = main_bbox[2] - main_bbox[0]
    main_height = main_bbox[3] - main_bbox[1]
    
    # Draw geometric accent rectangle (Bauhaus style)
    rect_x = 60
    rect_y = 280
    rect_width = min(main_width + 40, MAX_TEXT_WIDTH)
    rect_height = main_height + 40
    draw.rectangle([rect_x, rect_y, rect_x + rect_width, rect_y + rect_height], fill=accent)
    
    # Main text - positioned asymmetrically upper-left
    main_x = 80
    main_y = 300
    draw.text((main_x, main_y), main_text, font=font_main, fill=hex_to_rgb(COLORS["text"]))
    
    # Sub text - below main
    sub_x = 85
    sub_y = 300 + main_height + 60
    draw.text((sub_x, sub_y), sub_text, font=font_sub, fill=hex_to_rgb(COLORS["text"]))
    
    # English text - bottom right, thin
    eng_bbox = draw.textbbox((0, 0), english_text, font=font_english)
    eng_width = eng_bbox[2] - eng_bbox[0]
    eng_x = IMAGE_SIZE[0] - eng_width - 80
    eng_y = IMAGE_SIZE[1] - 120
    draw.text((eng_x, eng_y), english_text, font=font_english, fill=hex_to_rgb(COLORS["gray"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")
    return output_path


def create_slide_swiss(lines, highlight_text=None, output_path=None, emphasize_first=False):
    """
    Create slides 2-10 in Swiss style - clean, grid-based, intellectual
    Auto-fits text to image width
    """
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    # Calculate line data with auto-fitting
    line_spacing = 25
    line_data = []
    
    for i, line in enumerate(lines):
        if not line:  # Empty line for spacing
            line_data.append({"text": "", "font": None, "height": 30, "width": 0})
            continue
        
        # Choose base font size based on line type
        if i == 0 and emphasize_first:
            base_size = 80
        elif line.startswith("・") or line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
            base_size = 44
        else:
            base_size = 56
        
        # Fit text to width
        font, actual_size = fit_text_to_width(draw, line, FONTS["black"], base_size, MAX_TEXT_WIDTH)
        bbox = draw.textbbox((0, 0), line, font=font)
        height = bbox[3] - bbox[1]
        width = bbox[2] - bbox[0]
        
        line_data.append({"text": line, "font": font, "height": height, "width": width, "size": actual_size})
    
    # Calculate total height
    total_height = sum(ld["height"] + line_spacing for ld in line_data) - line_spacing
    
    # Start position - slightly above center for Swiss balance
    start_y = (IMAGE_SIZE[1] - total_height) // 2 - 20
    start_y = max(start_y, MARGIN)  # Ensure within bounds
    
    current_y = start_y
    for line_info in line_data:
        text = line_info["text"]
        font = line_info["font"]
        
        if not text:  # Empty line
            current_y += line_info["height"]
            continue
        
        # Draw highlight background if needed
        if highlight_text and highlight_text in text:
            bbox = draw.textbbox((MARGIN, current_y), text, font=font)
            padding = 8
            draw.rectangle(
                [bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding],
                fill=hex_to_rgb(COLORS["accent_yellow"])
            )
        
        draw.text((MARGIN, current_y), text, font=font, fill=hex_to_rgb(COLORS["text"]))
        current_y += line_info["height"] + line_spacing
    
    if output_path:
        img.save(output_path, "PNG", quality=95)
        print(f"Saved: {output_path}")
    
    return img


def create_slide_cta(main_cta, preview_text, follow_text, output_path):
    """
    Create CTA slide (slide 10) with next post preview
    """
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    # Fit CTA text
    font_cta, _ = fit_text_to_width(draw, main_cta, FONTS["black"], 64, MAX_TEXT_WIDTH - 60)
    font_preview, _ = fit_text_to_width(draw, preview_text.split("\n")[0], FONTS["black"], 42, MAX_TEXT_WIDTH)
    font_follow = get_font(FONTS["thin"], 36)
    
    # Yellow accent bar at top
    draw.rectangle([0, 0, IMAGE_SIZE[0], 20], fill=hex_to_rgb(COLORS["accent_yellow"]))
    
    # Main CTA with yellow background
    cta_bbox = draw.textbbox((0, 0), main_cta, font=font_cta)
    cta_width = cta_bbox[2] - cta_bbox[0]
    cta_height = cta_bbox[3] - cta_bbox[1]
    cta_x = (IMAGE_SIZE[0] - cta_width) // 2
    cta_y = 300
    
    # Yellow highlight behind CTA
    padding = 20
    draw.rectangle(
        [cta_x - padding, cta_y - padding, cta_x + cta_width + padding, cta_y + cta_height + padding],
        fill=hex_to_rgb(COLORS["accent_yellow"])
    )
    draw.text((cta_x, cta_y), main_cta, font=font_cta, fill=hex_to_rgb(COLORS["text"]))
    
    # Preview text
    preview_y = 480
    for i, line in enumerate(preview_text.split("\n")):
        font_line, _ = fit_text_to_width(draw, line, FONTS["black"], 42, MAX_TEXT_WIDTH)
        bbox = draw.textbbox((0, 0), line, font=font_line)
        line_width = bbox[2] - bbox[0]
        line_x = (IMAGE_SIZE[0] - line_width) // 2
        draw.text((line_x, preview_y + i * 70), line, font=font_line, fill=hex_to_rgb(COLORS["text"]))
    
    # Follow text at bottom
    follow_bbox = draw.textbbox((0, 0), follow_text, font=font_follow)
    follow_width = follow_bbox[2] - follow_bbox[0]
    follow_x = (IMAGE_SIZE[0] - follow_width) // 2
    follow_y = IMAGE_SIZE[1] - 150
    draw.text((follow_x, follow_y), follow_text, font=font_follow, fill=hex_to_rgb(COLORS["gray"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")
    return output_path


def generate_post_1():
    """Generate all 10 slides for Post 1: AI活用"""
    output_dir = "output/post1_ai"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1 - Bauhaus impact
    create_slide_1_bauhaus(
        main_text="使えない",
        sub_text="その常識を疑え",
        english_text="AI",
        output_path=f"{output_dir}/slide_01.png",
        accent_color="yellow"
    )
    
    # Slide 2 - 共感
    create_slide_swiss(
        lines=["AIは難しそう", "プログラミングが必要", "自分には関係ない", "", "そう思っていませんか？"],
        output_path=f"{output_dir}/slide_02.png"
    )
    
    # Slide 3 - 否定
    create_slide_swiss(
        lines=["9割の美容師が", "損をしている", "", "知らないだけで", "毎月10時間を失っている"],
        highlight_text="9割",
        output_path=f"{output_dir}/slide_03.png",
        emphasize_first=True
    )
    
    # Slide 4 - 真実①
    create_slide_swiss(
        lines=["ChatGPTは", "「質問するだけ」で使える", "", "必要なのは", "スマホと日本語だけ"],
        highlight_text="質問するだけ",
        output_path=f"{output_dir}/slide_04.png"
    )
    
    # Slide 5 - 真実②
    create_slide_swiss(
        lines=["美容師がAIに", "任せるべきこと", "", "・キャプション作成", "・お客様への返信文", "・メニュー説明文", "・ブログのたたき"],
        output_path=f"{output_dir}/slide_05.png"
    )
    
    # Slide 6 - 具体例
    create_slide_swiss(
        lines=["キャプション作成の例", "", "「今日のカラーについて", "文章を書いて」", "", "→ 30秒で完成"],
        highlight_text="30秒",
        output_path=f"{output_dir}/slide_06.png"
    )
    
    # Slide 7 - アクション①
    create_slide_swiss(
        lines=["今日から使える", "3つのプロンプト", "", "1. 説明文を書いて", "2. もっと短くして", "3. 返信を考えて"],
        output_path=f"{output_dir}/slide_07.png",
        emphasize_first=True
    )
    
    # Slide 8 - アクション② (修正: テキストを短く)
    create_slide_swiss(
        lines=["始め方は簡単", "", "1. アプリをダウンロード", "2. Googleでログイン", "3. 日本語で質問するだけ"],
        output_path=f"{output_dir}/slide_08.png"
    )
    
    # Slide 9 - 危機感
    create_slide_swiss(
        lines=["使わない理由が", "「難しそう」なら", "", "今日で終わりにしよう"],
        highlight_text="今日で終わり",
        output_path=f"{output_dir}/slide_09.png",
        emphasize_first=True
    )
    
    # Slide 10 - CTA
    create_slide_cta(
        main_cta="保存して今日から実践",
        preview_text="明日はインスタ集客の真実\nフォロワー数より大事な数字がある",
        follow_text="フォローで見逃さない",
        output_path=f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ Post 1 complete! Check {output_dir}/")
    return output_dir


if __name__ == "__main__":
    generate_post_1()
