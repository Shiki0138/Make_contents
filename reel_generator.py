"""
Instagram Reel Generator - Vertical (9:16) Slideshow with Avatar
Marketer-perspective content for beauty industry
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Reel specifications (9:16 vertical)
IMAGE_SIZE = (1080, 1920)
MARGIN = 80
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


def fit_font_size(draw, text, max_size, max_width, min_size=24):
    """Reduce font size until text fits"""
    size = max_size
    while size > min_size:
        font = get_font(size)
        w, _ = get_text_size(draw, text, font)
        if w <= max_width:
            return font, size
        size -= 4
    return get_font(min_size), min_size


def add_avatar(img, position="bottom_left", size_height=200):
    """Add avatar character to image"""
    try:
        avatar = Image.open(AVATAR_PATH).convert("RGBA")
        # Resize maintaining aspect ratio
        ratio = size_height / avatar.height
        new_size = (int(avatar.width * ratio), size_height)
        avatar = avatar.resize(new_size, Image.Resampling.LANCZOS)
        
        # Position
        if position == "bottom_left":
            x = 40
            y = img.height - avatar.height - 60
        
        # Paste with transparency
        img.paste(avatar, (x, y), avatar)
    except Exception as e:
        print(f"Avatar not found or error: {e}")
    return img


def create_title_slide(main_text, sub_text, tag_text, output_path):
    """Slide 1: Maximum impact title"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    # Tag at top
    font_tag = get_font(36, "thin")
    tag_w, _ = get_text_size(draw, tag_text, font_tag)
    draw.text(((IMAGE_SIZE[0] - tag_w) // 2, 200), tag_text, 
              font=font_tag, fill=hex_to_rgb(COLORS["gray"]))
    
    # Main text - center
    font_main, _ = fit_font_size(draw, main_text, 160, MAX_WIDTH - 40)
    main_w, main_h = get_text_size(draw, main_text, font_main)
    main_y = (IMAGE_SIZE[1] // 2) - (main_h // 2) - 50
    draw.text(((IMAGE_SIZE[0] - main_w) // 2, main_y), main_text, 
              font=font_main, fill=hex_to_rgb(COLORS["text"]))
    
    # Subtitle
    font_sub = get_font(48)
    sub_w, _ = get_text_size(draw, sub_text, font_sub)
    draw.text(((IMAGE_SIZE[0] - sub_w) // 2, main_y + main_h + 40), sub_text, 
              font=font_sub, fill=hex_to_rgb(COLORS["text"]))
    
    # Add avatar
    img = add_avatar(img)
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_content_slide(lines, output_path, with_avatar=True):
    """Content slide with multiple lines"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    sizes = {"xl": 140, "l": 100, "m": 72, "s": 56}
    
    # Calculate heights
    line_data = []
    for item in lines:
        if item.get("text") == "":
            line_data.append({"type": "empty", "height": 30})
            continue
        
        text = item["text"]
        size = sizes.get(item.get("size", "m"), 72)
        font, _ = fit_font_size(draw, text, size, MAX_WIDTH)
        w, h = get_text_size(draw, text, font)
        line_data.append({
            "type": "single",
            "text": text,
            "font": font,
            "height": h,
            "width": w,
            "highlight": item.get("highlight", False)
        })
    
    total_height = sum(ld["height"] + 30 for ld in line_data)
    start_y = (IMAGE_SIZE[1] - total_height) // 2 - 100
    start_y = max(start_y, 150)
    
    # Draw lines
    current_y = start_y
    for ld in line_data:
        if ld["type"] == "empty":
            current_y += ld["height"]
            continue
        
        x = MARGIN + 20
        
        # Highlight background
        if ld.get("highlight"):
            padding = 15
            draw.rectangle([
                x - padding, 
                current_y - padding,
                x + ld["width"] + padding,
                current_y + ld["height"] + padding
            ], fill=hex_to_rgb(COLORS["accent"]))
        
        draw.text((x, current_y), ld["text"], font=ld["font"], 
                  fill=hex_to_rgb(COLORS["text"]))
        current_y += ld["height"] + 30
    
    if with_avatar:
        img = add_avatar(img)
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_vertical_text_slide(main_char, sub_text, output_path):
    """Vertical text emphasis slide"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    # Main vertical text
    font_main = get_font(200)
    chars = list(main_char)
    total_height = 0
    char_data = []
    
    for char in chars:
        w, h = get_text_size(draw, char, font_main)
        char_data.append({"char": char, "w": w, "h": h})
        total_height += h + 20
    
    # Center vertically
    start_y = (IMAGE_SIZE[1] - total_height) // 2 - 100
    x = IMAGE_SIZE[0] // 2 - 100
    
    current_y = start_y
    for cd in char_data:
        draw.text((x, current_y), cd["char"], font=font_main, 
                  fill=hex_to_rgb(COLORS["text"]))
        current_y += cd["h"] + 20
    
    # Subtitle at bottom right
    if sub_text:
        font_sub = get_font(48)
        sw, _ = get_text_size(draw, sub_text, font_sub)
        draw.text((IMAGE_SIZE[0] - sw - 100, IMAGE_SIZE[1] - 400), sub_text, 
                  font=font_sub, fill=hex_to_rgb(COLORS["text"]))
    
    img = add_avatar(img)
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_cta_slide(main_cta, sub_lines, follow_text, output_path):
    """Call-to-action slide"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    # Main CTA
    font_cta, _ = fit_font_size(draw, main_cta, 90, MAX_WIDTH - 60)
    cta_w, cta_h = get_text_size(draw, main_cta, font_cta)
    
    # Calculate sub heights
    sub_data = []
    for line in sub_lines:
        font_sub, _ = fit_font_size(draw, line, 52, MAX_WIDTH)
        w, h = get_text_size(draw, line, font_sub)
        sub_data.append({"font": font_sub, "w": w, "h": h, "line": line})
    
    total_sub = sum(sd["h"] + 25 for sd in sub_data)
    total_height = cta_h + 60 + total_sub
    start_y = (IMAGE_SIZE[1] - total_height) // 2 - 100
    
    # Draw CTA
    draw.text(((IMAGE_SIZE[0] - cta_w) // 2, start_y), main_cta, 
              font=font_cta, fill=hex_to_rgb(COLORS["text"]))
    
    # Draw sub lines
    sub_y = start_y + cta_h + 60
    for sd in sub_data:
        x = (IMAGE_SIZE[0] - sd["w"]) // 2
        draw.text((x, sub_y), sd["line"], font=sd["font"], 
                  fill=hex_to_rgb(COLORS["text"]))
        sub_y += sd["h"] + 25
    
    # Follow text at bottom
    font_follow = get_font(32, "thin")
    fw, _ = get_text_size(draw, follow_text, font_follow)
    draw.text(((IMAGE_SIZE[0] - fw) // 2, IMAGE_SIZE[1] - 350), follow_text, 
              font=font_follow, fill=hex_to_rgb(COLORS["gray"]))
    
    img = add_avatar(img)
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def generate_day1():
    """Day 1: 予約率が上がるカウンセリングの心理学"""
    output_dir = "output/day1_counseling_psychology"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1 - Title
    create_title_slide(
        "「今日どうします？」",
        "この質問が予約率を下げている",
        "BEHAVIORAL ECONOMICS",
        f"{output_dir}/slide_01.png"
    )
    
    # Slide 2 - Empathy
    create_content_slide([
        {"text": "カウンセリングで", "size": "l"},
        {"text": "お客様が迷う", "size": "l"},
        {"text": ""},
        {"text": "「うーん、お任せで...」", "size": "m"},
        {"text": ""},
        {"text": "こう言われた経験ない？", "size": "m"},
    ], f"{output_dir}/slide_02.png")
    
    # Slide 3 - Vertical keyword
    create_vertical_text_slide("選択", "選択のパラドックス", f"{output_dir}/slide_03.png")
    
    # Slide 4 - Theory 1
    create_content_slide([
        {"text": "行動経済学の研究", "size": "l"},
        {"text": ""},
        {"text": "選択肢が多いほど", "size": "m"},
        {"text": "人は決められなくなる", "size": "xl", "highlight": True},
        {"text": ""},
        {"text": "ジャムの法則", "size": "m"},
        {"text": "（シーナ・アイエンガー）", "size": "s"},
    ], f"{output_dir}/slide_04.png")
    
    # Slide 5 - Theory 2
    create_content_slide([
        {"text": "成功サロンの共通点", "size": "l"},
        {"text": ""},
        {"text": "提案を3つに絞る", "size": "xl"},
        {"text": ""},
        {"text": "「松・竹・梅」の法則", "size": "m"},
        {"text": "→真ん中が選ばれやすい", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # Slide 6 - Template 1
    create_content_slide([
        {"text": "NG質問", "size": "l"},
        {"text": ""},
        {"text": "「今日どうされますか？」", "size": "m"},
        {"text": "「何かご希望は？」", "size": "m"},
        {"text": ""},
        {"text": "→選択肢が無限=決められない", "size": "m"},
    ], f"{output_dir}/slide_06.png")
    
    # Slide 7 - Template 2
    create_content_slide([
        {"text": "OK質問", "size": "l"},
        {"text": ""},
        {"text": "「前回と同じ感じ or", "size": "m"},
        {"text": "少し変化つけますか？」", "size": "m"},
        {"text": ""},
        {"text": "→2択で答えやすい", "size": "m", "highlight": True},
    ], f"{output_dir}/slide_07.png")
    
    # Slide 8 - Application
    create_content_slide([
        {"text": "フェーズ別の質問例", "size": "l"},
        {"text": ""},
        {"text": "カット→「軽め or 重め」", "size": "m"},
        {"text": "カラー→「明るめ or 落ち着き」", "size": "m"},
        {"text": "仕上げ→「巻く or ストレート」", "size": "m"},
        {"text": ""},
        {"text": "常に2〜3択で聞く", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # Slide 9 - Summary
    create_vertical_text_slide("絞る", "選択肢を減らす＝決断を助ける", f"{output_dir}/slide_09.png")
    
    # Slide 10 - CTA
    create_cta_slide(
        "明日から使ってみて",
        ["✓ 質問は2〜3択に絞る", "✓ 「どうしますか」は封印", "✓ 松竹梅で真ん中を意識"],
        "保存して次回の施術で実践 →",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ Day 1 complete! Check {output_dir}/")
    return output_dir


if __name__ == "__main__":
    generate_day1()
