"""
Instagram Image Generator - High Impact Bauhaus Style v3
Mixed-size text support, auto-fit, vertical text
"""

from PIL import Image, ImageDraw, ImageFont
import os

IMAGE_SIZE = (1080, 1080)
MARGIN = 60
MAX_WIDTH = IMAGE_SIZE[0] - (MARGIN * 2) - 40

COLORS = {
    "background": "#FFFFFF",
    "text": "#000000",
    "yellow": "#FFE500",
    "red": "#FF3333",
    "gray": "#666666",
}

FONTS = {
    "black": "fonts/NotoSansJP-Black.ttf",
    "thin": "fonts/NotoSansJP-Thin.ttf",
}


def hex_to_rgb(hex_color):
    return tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))


def get_font(size):
    try:
        return ImageFont.truetype(FONTS["black"], size)
    except:
        return ImageFont.load_default()


def get_text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def fit_font_size(draw, text, max_size, max_width):
    """Reduce font size until text fits"""
    size = max_size
    while size > 24:
        font = get_font(size)
        w, _ = get_text_size(draw, text, font)
        if w <= max_width:
            return font, size
        size -= 4
    return get_font(24), 24


def create_impact_slide_1(main_text, sub_text, english_text, output_path):
    """Slide 1: Maximum impact"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    font_main, _ = fit_font_size(draw, main_text, 220, MAX_WIDTH)
    main_w, main_h = get_text_size(draw, main_text, font_main)
    
    block_x, block_y = 50, 250
    draw.rectangle([block_x, block_y, block_x + main_w + 60, block_y + main_h + 50], 
                   fill=hex_to_rgb(COLORS["yellow"]))
    
    draw.text((80, 270), main_text, font=font_main, fill=hex_to_rgb(COLORS["text"]))
    
    font_sub = get_font(56)
    draw.text((85, 270 + main_h + 80), sub_text, font=font_sub, fill=hex_to_rgb(COLORS["text"]))
    
    draw.rectangle([0, IMAGE_SIZE[1] - 40, IMAGE_SIZE[0], IMAGE_SIZE[1]], fill=hex_to_rgb(COLORS["red"]))
    
    font_eng = ImageFont.truetype(FONTS["thin"], 32)
    eng_w, _ = get_text_size(draw, english_text, font_eng)
    draw.text((IMAGE_SIZE[0] - eng_w - 80, IMAGE_SIZE[1] - 100), english_text, 
              font=font_eng, fill=hex_to_rgb(COLORS["gray"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def draw_mixed_line(draw, x, y, parts, yellow):
    """
    Draw a line with mixed font sizes
    parts = [(text, size, highlight), ...]
    Returns total width and max height
    """
    current_x = x
    max_h = 0
    
    # First pass: calculate positions and draw highlights
    positions = []
    for text, size, highlight in parts:
        font, _ = fit_font_size(draw, text, size, MAX_WIDTH // 2)
        w, h = get_text_size(draw, text, font)
        positions.append({"x": current_x, "text": text, "font": font, "w": w, "h": h, "highlight": highlight})
        max_h = max(max_h, h)
        current_x += w + 5
    
    # Draw underlines first (for highlighted text)
    for pos in positions:
        if pos["highlight"]:
            underline_y = y + pos["h"] + 5
            underline_thickness = 15
            draw.rectangle([pos["x"], underline_y, 
                          pos["x"] + pos["w"], underline_y + underline_thickness], fill=yellow)
    
    # Draw text
    for pos in positions:
        draw.text((pos["x"], y), pos["text"], font=pos["font"], fill=hex_to_rgb(COLORS["text"]))
    
    return current_x - x, max_h


def create_impact_slide(content, output_path, accent="bar"):
    """
    content can be:
    - {"text": str, "size": "xl"|"l"|"m"|"s", "highlight": bool}
    - {"parts": [(text, size, highlight), ...]}  # for mixed-size lines
    """
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    sizes = {"xl": 170, "l": 100, "m": 88, "s": 80}
    yellow = hex_to_rgb(COLORS["yellow"])
    red = hex_to_rgb(COLORS["red"])
    
    # Accent
    if accent == "bar":
        draw.rectangle([0, 0, IMAGE_SIZE[0], 20], fill=yellow)
    elif accent == "side":
        draw.rectangle([0, 150, 25, 930], fill=red)
    elif accent == "corner":
        draw.polygon([(0, 0), (250, 0), (0, 250)], fill=yellow)
    elif accent == "dual":
        draw.rectangle([0, 0, IMAGE_SIZE[0], 15], fill=yellow)
        draw.rectangle([0, IMAGE_SIZE[1] - 15, IMAGE_SIZE[0], IMAGE_SIZE[1]], fill=red)
    
    # Calculate line heights
    line_data = []
    spacing = 12
    
    for item in content:
        if item.get("text") == "":
            line_data.append({"type": "empty", "height": 15})
            continue
        
        if "parts" in item:
            # Mixed-size line
            temp_img = Image.new('RGB', (1, 1))
            temp_draw = ImageDraw.Draw(temp_img)
            total_w = 0
            max_h = 0
            for text, size_key, _ in item["parts"]:
                size = sizes.get(size_key, 52)
                font, _ = fit_font_size(temp_draw, text, size, MAX_WIDTH // 2)
                w, h = get_text_size(temp_draw, text, font)
                total_w += w + 5
                max_h = max(max_h, h)
            line_data.append({"type": "mixed", "parts": item["parts"], "height": max_h, "width": total_w})
        else:
            # Single line
            text = item["text"]
            size = sizes.get(item.get("size", "m"), 52)
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
    
    total_height = sum(ld["height"] + spacing for ld in line_data) - spacing
    start_y = (IMAGE_SIZE[1] - total_height) // 2 - 10
    start_y = max(start_y, 50)
    
    # Calculate positions
    current_y = start_y
    for ld in line_data:
        ld["y"] = current_y
        ld["x"] = MARGIN + 20
        current_y += ld["height"] + spacing
    
    # Draw underlines first (for highlighted single lines)
    for ld in line_data:
        if ld["type"] == "single" and ld.get("highlight"):
            underline_y = ld["y"] + ld["height"] + 5
            underline_thickness = 15
            draw.rectangle([ld["x"], underline_y, 
                          ld["x"] + ld["width"], underline_y + underline_thickness],
                          fill=yellow)
    
    # Draw all content
    for ld in line_data:
        if ld["type"] == "empty":
            continue
        elif ld["type"] == "mixed":
            draw_mixed_line(draw, ld["x"], ld["y"], 
                          [(t, sizes.get(s, 52), h) for t, s, h in ld["parts"]], yellow)
        else:
            draw.text((ld["x"], ld["y"]), ld["text"], font=ld["font"], fill=hex_to_rgb(COLORS["text"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_vertical_slide(main_text, sub_text, output_path, highlight_main=True):
    """Vertical text slide"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    yellow = hex_to_rgb(COLORS["yellow"])
    red = hex_to_rgb(COLORS["red"])
    
    draw.rectangle([IMAGE_SIZE[0] - 30, 0, IMAGE_SIZE[0], IMAGE_SIZE[1]], fill=red)
    
    font_main = get_font(180)
    char_heights = []
    total_height = 0
    
    for char in main_text:
        w, h = get_text_size(draw, char, font_main)
        char_heights.append({"char": char, "w": w, "h": h})
        total_height += h + 10
    
    start_y = (IMAGE_SIZE[1] - total_height) // 2
    x = 150
    
    # Draw underline for vertical text (side bar style)
    if highlight_main:
        max_w = max(ch["w"] for ch in char_heights)
        underline_x = x + max_w + 15
        underline_thickness = 15
        draw.rectangle([underline_x, start_y - 10, 
                       underline_x + underline_thickness, start_y + total_height],
                      fill=yellow)
    
    current_y = start_y
    for ch in char_heights:
        draw.text((x, current_y), ch["char"], font=font_main, fill=hex_to_rgb(COLORS["text"]))
        current_y += ch["h"] + 10
    
    if sub_text:
        font_sub = get_font(48)
        sw, sh = get_text_size(draw, sub_text, font_sub)
        draw.text((IMAGE_SIZE[0] - sw - 100, IMAGE_SIZE[1] - 150), sub_text, 
                 font=font_sub, fill=hex_to_rgb(COLORS["text"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_impact_cta(main_cta, sub_lines, follow_text, output_path):
    """CTA slide"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    yellow = hex_to_rgb(COLORS["yellow"])
    red = hex_to_rgb(COLORS["red"])
    
    draw.rectangle([0, 0, IMAGE_SIZE[0], 30], fill=yellow)
    draw.rectangle([0, IMAGE_SIZE[1] - 30, IMAGE_SIZE[0], IMAGE_SIZE[1]], fill=red)
    
    font_cta, _ = fit_font_size(draw, main_cta, 72, MAX_WIDTH - 60)
    cta_w, cta_h = get_text_size(draw, main_cta, font_cta)
    cta_x = (IMAGE_SIZE[0] - cta_w) // 2
    cta_y = 250
    
    draw.rectangle([cta_x - 30, cta_y - 25, cta_x + cta_w + 30, cta_y + cta_h + 25], fill=yellow)
    draw.text((cta_x, cta_y), main_cta, font=font_cta, fill=hex_to_rgb(COLORS["text"]))
    
    sub_y = 420
    for line in sub_lines:
        font_sub, _ = fit_font_size(draw, line, 48, MAX_WIDTH)
        w, h = get_text_size(draw, line, font_sub)
        x = (IMAGE_SIZE[0] - w) // 2
        draw.text((x, sub_y), line, font=font_sub, fill=hex_to_rgb(COLORS["text"]))
        sub_y += h + 25
    
    font_follow = ImageFont.truetype(FONTS["thin"], 36)
    fw, _ = get_text_size(draw, follow_text, font_follow)
    draw.text(((IMAGE_SIZE[0] - fw) // 2, IMAGE_SIZE[1] - 120), follow_text, 
              font=font_follow, fill=hex_to_rgb(COLORS["gray"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def generate_post_1_impact():
    """Generate Post 1 with mixed-size text support"""
    output_dir = "output/post1_ai_impact"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1
    create_impact_slide_1("使えない", "その常識を疑え", "AI", f"{output_dir}/slide_01.png")
    
    # Slide 2
    create_impact_slide([
        {"text": "AIは難しそう", "size": "l"},
        {"text": "プログラミングが必要", "size": "l"},
        {"text": "自分には関係ない", "size": "l"},
        {"text": ""},
        {"text": "そう思っていませんか？", "size": "m"},
    ], f"{output_dir}/slide_02.png", accent="corner")
    
    # Slide 3 - 縦文字
    create_vertical_slide("9割", "の美容師が損をしている", f"{output_dir}/slide_03.png", highlight_main=False)
    
    # Slide 4 - 混合サイズ: 「質問」大 + 「するだけ」通常
    create_impact_slide([
        {"text": "ChatGPTは", "size": "l"},
        {"parts": [("質問", "xl", False), ("するだけ", "l", False)]},
        {"text": "で使える", "size": "l"},
        {"text": ""},
        {"text": "必要なのは", "size": "m"},
        {"text": "スマホと日本語だけ", "size": "m"},
    ], f"{output_dir}/slide_04.png", accent="bar")
    
    # Slide 5 - 「任せる」強調
    create_impact_slide([
        {"text": "美容師がAIに", "size": "l"},
        {"parts": [("任せる", "xl", False), ("べきこと", "l", False)]},
        {"text": ""},
        {"text": "・キャプション作成", "size": "m"},
        {"text": "・お客様への返信文", "size": "m"},
        {"text": "・メニュー説明文", "size": "m"},
    ], f"{output_dir}/slide_05.png", accent="dual")
    
    # Slide 6 - 縦文字
    create_vertical_slide("30秒", "で完成", f"{output_dir}/slide_06.png", highlight_main=False)
    
    # Slide 7 - 「今日」強調
    create_impact_slide([
        {"parts": [("今日", "xl", False), ("から使える", "l", False)]},
        {"text": "3つのプロンプト", "size": "l"},
        {"text": ""},
        {"text": "1. 説明文を書いて", "size": "m"},
        {"text": "2. もっと短くして", "size": "m"},
        {"text": "3. 返信を考えて", "size": "m"},
    ], f"{output_dir}/slide_07.png", accent="side")
    
    # Slide 8 - 「簡単」強調
    create_impact_slide([
        {"parts": [("始め方は", "l", False), ("簡単", "xl", False)]},
        {"text": ""},
        {"text": "1. アプリをダウンロード", "size": "m"},
        {"text": "2. Googleでログイン", "size": "m"},
        {"text": "3. 日本語で質問するだけ", "size": "m"},
    ], f"{output_dir}/slide_08.png", accent="bar")
    
    # Slide 9 - 縦文字
    create_vertical_slide("終了", "今日で終わりにしよう", f"{output_dir}/slide_09.png", highlight_main=False)
    
    # Slide 10 - CTA
    create_impact_cta(
        "保存して今日から実践",
        ["明日はインスタ集客の真実", "フォロワー数より大事な数字がある"],
        "フォローで見逃さない",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ Post 1 complete! Check {output_dir}/")


def generate_post_repeat_rate():
    """Generate リピート率シリーズ - 覆す常識: リピート率80%=成功 → 新規比率とのバランスが本質"""
    output_dir = "output/post_repeat_rate"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1 - 衝撃
    create_impact_slide_1("80%", "その数字に騙されるな", "repeat rate", f"{output_dir}/slide_01.png")
    
    # Slide 2 - 共感
    create_impact_slide([
        {"text": "リピート率80%", "size": "l"},
        {"text": "うちは高いから大丈夫", "size": "l"},
        {"text": ""},
        {"text": "そう思っていませんか？", "size": "m"},
    ], f"{output_dir}/slide_02.png", accent="corner")
    
    # Slide 3 - 縦文字で否定
    create_vertical_slide("危険", "その安心感が危ない", f"{output_dir}/slide_03.png", highlight_main=False)
    
    # Slide 4 - 真実①
    create_impact_slide([
        {"text": "リピート率が高すぎると", "size": "l"},
        {"parts": [("新規", "xl", False), ("が来ない", "l", False)]},
        {"text": ""},
        {"text": "客層が固定化する", "size": "m"},
        {"text": "売上の天井ができる", "size": "m"},
    ], f"{output_dir}/slide_04.png", accent="bar")
    
    # Slide 5 - 真実②
    create_impact_slide([
        {"text": "理想のバランス", "size": "xl"},
        {"text": ""},
        {"text": "リピート率 60-70%", "size": "l"},
        {"text": "新規比率 30-40%", "size": "l"},
        {"text": ""},
        {"text": "これが成長するサロン", "size": "m"},
    ], f"{output_dir}/slide_05.png", accent="dual")
    
    # Slide 6 - 縦文字
    create_vertical_slide("新規", "を恐れるな", f"{output_dir}/slide_06.png", highlight_main=False)
    
    # Slide 7 - アクション①
    create_impact_slide([
        {"parts": [("今すぐ", "xl", False), ("確認すべきこと", "l", False)]},
        {"text": ""},
        {"text": "1. 過去3ヶ月の新規数", "size": "m"},
        {"text": "2. 新規のリピート率", "size": "m"},
        {"text": "3. 客単価の推移", "size": "m"},
    ], f"{output_dir}/slide_07.png", accent="side")
    
    # Slide 8 - アクション②
    create_impact_slide([
        {"text": "新規を増やす方法", "size": "xl"},
        {"text": ""},
        {"text": "・紹介カードを配る", "size": "m"},
        {"text": "・SNSで発信する", "size": "m"},
        {"text": "・口コミを増やす", "size": "m"},
    ], f"{output_dir}/slide_08.png", accent="bar")
    
    # Slide 9 - 危機感
    create_vertical_slide("衰退", "リピートだけでは", f"{output_dir}/slide_09.png", highlight_main=False)
    
    # Slide 10 - CTA
    create_impact_cta(
        "保存して数字を見直す",
        ["あなたのサロンは", "成長型？それとも衰退型？"],
        "フォローで経営のヒントを",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ リピート率シリーズ Post 1 complete! Check {output_dir}/")


def generate_repeat_rate_post2():
    """Post 2: 根拠（数学的証明）"""
    output_dir = "output/repeat_rate_post2"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1
    create_impact_slide_1("証明", "リピート率の落とし穴", "proof", f"{output_dir}/slide_01.png")
    
    # Slide 2
    create_impact_slide([
        {"text": "2つのサロンを", "size": "l"},
        {"text": "比較しよう", "size": "xl"},
    ], f"{output_dir}/slide_02.png", accent="corner")
    
    # Slide 3
    create_impact_slide([
        {"text": "サロンA", "size": "xl"},
        {"text": "リピート率 90%", "size": "l"},
        {"text": "新規 10人/月", "size": "m"},
    ], f"{output_dir}/slide_03.png", accent="bar")
    
    # Slide 4
    create_impact_slide([
        {"text": "3年後のサロンA", "size": "l"},
        {"text": ""},
        {"parts": [("顧客", "l", False), ("100人", "xl", False)]},
        {"text": "で頭打ち", "size": "l"},
        {"text": ""},
        {"text": "予約が取れず新規が来ない", "size": "m"},
    ], f"{output_dir}/slide_04.png", accent="side")
    
    # Slide 5
    create_impact_slide([
        {"text": "サロンB", "size": "xl"},
        {"text": "リピート率 65%", "size": "l"},
        {"text": "新規 35人/月", "size": "m"},
    ], f"{output_dir}/slide_05.png", accent="bar")
    
    # Slide 6
    create_impact_slide([
        {"text": "3年後のサロンB", "size": "l"},
        {"text": ""},
        {"parts": [("顧客プール", "l", False), ("665人", "xl", False)]},
        {"text": ""},
        {"text": "常に選べる状態", "size": "m"},
    ], f"{output_dir}/slide_06.png", accent="dual")
    
    # Slide 7 - 縦書き
    create_vertical_slide("6.6倍", "の差がつく", f"{output_dir}/slide_07.png", highlight_main=False)
    
    # Slide 8
    create_impact_slide([
        {"text": "なぜ差がつくのか", "size": "xl"},
        {"text": ""},
        {"text": "新規=成長エンジン", "size": "l"},
        {"text": ""},
        {"text": "新規がいないと", "size": "m"},
        {"text": "顧客プールが増えない", "size": "m"},
    ], f"{output_dir}/slide_08.png", accent="corner")
    
    # Slide 9
    create_vertical_slide("新規", "が全てを決める", f"{output_dir}/slide_09.png", highlight_main=False)
    
    # Slide 10
    create_impact_cta(
        "昨日の投稿も保存",
        ["明日はこのバランスの", "メリットを解説"],
        "フォローで見逃さない",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ リピート率シリーズ Post 2 complete! Check {output_dir}/")


def generate_repeat_rate_post3():
    """Post 3: メリット"""
    output_dir = "output/repeat_rate_post3"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1
    create_impact_slide_1("安定", "新陳代謝が生む強さ", "benefit", f"{output_dir}/slide_01.png")
    
    # Slide 2
    create_impact_slide([
        {"text": "リピート65%の", "size": "l"},
        {"parts": [("3つの", "xl", False), ("メリット", "l", False)]},
    ], f"{output_dir}/slide_02.png", accent="corner")
    
    # Slide 3
    create_impact_slide([
        {"text": "メリット①", "size": "l"},
        {"text": ""},
        {"parts": [("値上げ", "xl", False), ("しやすい", "l", False)]},
        {"text": ""},
        {"text": "新規が常にいる=試せる", "size": "m"},
    ], f"{output_dir}/slide_03.png", accent="bar")
    
    # Slide 4
    create_impact_slide([
        {"text": "既存客だけだと", "size": "l"},
        {"text": "値上げは難しい", "size": "l"},
        {"text": ""},
        {"text": "新規なら最初から", "size": "m"},
        {"text": "新価格でスタート", "size": "m"},
    ], f"{output_dir}/slide_04.png", accent="side")
    
    # Slide 5
    create_impact_slide([
        {"text": "メリット②", "size": "l"},
        {"text": ""},
        {"parts": [("客層が", "l", False), ("若返る", "xl", False)]},
        {"text": ""},
        {"text": "10年後も新しい顧客がいる", "size": "m"},
    ], f"{output_dir}/slide_05.png", accent="bar")
    
    # Slide 6
    create_vertical_slide("成長", "し続けられる", f"{output_dir}/slide_06.png", highlight_main=False)
    
    # Slide 7
    create_impact_slide([
        {"text": "メリット③", "size": "l"},
        {"text": ""},
        {"parts": [("リスク", "xl", False), ("分散", "l", False)]},
        {"text": ""},
        {"text": "1人失客しても影響が小さい", "size": "m"},
    ], f"{output_dir}/slide_07.png", accent="bar")
    
    # Slide 8
    create_impact_slide([
        {"text": "100人に依存", "size": "l"},
        {"text": "vs", "size": "m"},
        {"text": "665人から選ぶ", "size": "l"},
        {"text": ""},
        {"text": "どちらが安心？", "size": "m"},
    ], f"{output_dir}/slide_08.png", accent="dual")
    
    # Slide 9
    create_vertical_slide("安心", "経営の土台", f"{output_dir}/slide_09.png", highlight_main=False)
    
    # Slide 10
    create_impact_cta(
        "保存して振り返る",
        ["明日は具体的な施策を", "解説します"],
        "フォローで見逃さない",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ リピート率シリーズ Post 3 complete! Check {output_dir}/")


def generate_repeat_rate_post4():
    """Post 4: 具体的な施策"""
    output_dir = "output/repeat_rate_post4"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1
    create_impact_slide_1("行動", "今日からできること", "action", f"{output_dir}/slide_01.png")
    
    # Slide 2
    create_impact_slide([
        {"text": "まずは", "size": "l"},
        {"parts": [("数字を", "xl", False), ("把握", "l", False)]},
    ], f"{output_dir}/slide_02.png", accent="corner")
    
    # Slide 3
    create_impact_slide([
        {"text": "確認①", "size": "l"},
        {"text": ""},
        {"text": "過去3ヶ月の新規比率", "size": "l"},
        {"text": ""},
        {"text": "30%以下なら要注意", "size": "m"},
    ], f"{output_dir}/slide_03.png", accent="bar")
    
    # Slide 4
    create_impact_slide([
        {"text": "確認②", "size": "l"},
        {"text": ""},
        {"text": "新規のリピート率", "size": "l"},
        {"text": ""},
        {"text": "50%以下なら接客を見直す", "size": "m"},
    ], f"{output_dir}/slide_04.png", accent="side")
    
    # Slide 5
    create_impact_slide([
        {"parts": [("新規を", "l", False), ("増やす", "xl", False)]},
        {"text": "3つの方法", "size": "l"},
    ], f"{output_dir}/slide_05.png", accent="dual")
    
    # Slide 6
    create_impact_slide([
        {"text": "方法①", "size": "l"},
        {"text": ""},
        {"text": "紹介カードを配る", "size": "xl"},
        {"text": ""},
        {"text": "お会計時に必ず渡す", "size": "m"},
    ], f"{output_dir}/slide_06.png", accent="bar")
    
    # Slide 7
    create_impact_slide([
        {"text": "方法②", "size": "l"},
        {"text": ""},
        {"text": "SNSで毎週発信", "size": "xl"},
        {"text": ""},
        {"text": "保存される投稿を意識", "size": "m"},
    ], f"{output_dir}/slide_07.png", accent="bar")
    
    # Slide 8
    create_impact_slide([
        {"text": "方法③", "size": "l"},
        {"text": ""},
        {"text": "口コミを依頼する", "size": "xl"},
        {"text": ""},
        {"text": "満足度が高い時に声かけ", "size": "m"},
    ], f"{output_dir}/slide_08.png", accent="bar")
    
    # Slide 9
    create_vertical_slide("実践", "今日から始める", f"{output_dir}/slide_09.png", highlight_main=False)
    
    # Slide 10
    create_impact_cta(
        "4日間の投稿を保存",
        ["実践して", "成長するサロンへ"],
        "フォローで経営のヒントを",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ リピート率シリーズ Post 4 complete! Check {output_dir}/")


def generate_all_repeat_rate():
    """Generate all 4 posts of リピート率シリーズ"""
    generate_post_repeat_rate()  # Post 1
    generate_repeat_rate_post2()  # Post 2
    generate_repeat_rate_post3()  # Post 3
    generate_repeat_rate_post4()  # Post 4
    print("\n✅ 全4投稿完成！")


if __name__ == "__main__":
    generate_all_repeat_rate()
