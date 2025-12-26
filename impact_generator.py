"""
Instagram Image Generator - High Impact Bauhaus Style v3 (Simplified)
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
    """Slide 1: Maximum impact (Main=center, Sub=3/4)"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    font_main, _ = fit_font_size(draw, main_text, 300, MAX_WIDTH)
    font_sub = get_font(56)
    
    # Main text: vertically centered (anchor='mm' = middle-middle)
    main_x = IMAGE_SIZE[0] // 2
    main_y = IMAGE_SIZE[1] // 2  # Vertical center
    draw.text((main_x, main_y), main_text, font=font_main, fill=hex_to_rgb(COLORS["text"]), anchor='mm')
    
    # Subtitle: at 3/4 of image height (1/4 from bottom)
    sub_x = IMAGE_SIZE[0] // 2
    sub_y = (IMAGE_SIZE[1] * 3) // 4  # 3/4 = 810px from top
    draw.text((sub_x, sub_y), sub_text, font=font_sub, fill=hex_to_rgb(COLORS["text"]), anchor='mm')
    
    # English text (bottom right)
    font_eng = ImageFont.truetype(FONTS["thin"], 32)
    eng_w, _ = get_text_size(draw, english_text, font_eng)
    draw.text((IMAGE_SIZE[0] - eng_w - 80, IMAGE_SIZE[1] - 100), english_text, 
              font=font_eng, fill=hex_to_rgb(COLORS["gray"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")




def draw_mixed_line(draw, x, y, parts):
    """
    Draw a line with mixed font sizes
    parts = [(text, size, highlight), ...]
    Returns total width and max height
    """
    current_x = x
    max_h = 0
    sizes = {"xl": 240, "l": 140, "m": 110, "s": 90}
    
    # First pass: calculate positions
    positions = []
    for text, size_key, _ in parts:
        size = sizes.get(size_key, 52)
        font, _ = fit_font_size(draw, text, size, MAX_WIDTH // 2)
        w, h = get_text_size(draw, text, font)
        # Increased spacing between segments
        positions.append({"x": current_x, "text": text, "font": font, "w": w, "h": h})
        max_h = max(max_h, h)
        current_x += w + (size * 0.1) 
    
    # Draw text only
    for pos in positions:
        draw.text((pos["x"], y), pos["text"], font=pos["font"], fill=hex_to_rgb(COLORS["text"]))
    
    return current_x - x, max_h


def create_impact_slide(content, output_path, accent="bar"):
    """
    Simplified content slide
    """
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    sizes = {"xl": 240, "l": 140, "m": 110, "s": 90}
    
    # Calculate line heights
    line_data = []
    # Dynamic spacing instead of fixed 12
    default_spacing = 30 
    
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
                "width": w
            })
    
    total_height = sum(ld["height"] + default_spacing for ld in line_data) - default_spacing
    start_y = (IMAGE_SIZE[1] - total_height) // 2 - 10
    start_y = max(start_y, 50)
    
    # Calculate positions
    current_y = start_y
    for ld in line_data:
        ld["y"] = current_y
        ld["x"] = MARGIN + 20
        # Multi-line spacing based on line height
        current_spacing = ld["height"] * 0.2 if ld["height"] > 0 else default_spacing
        current_y += ld["height"] + current_spacing
    
    # Draw all content
    for ld in line_data:
        if ld["type"] == "empty":
            continue
        elif ld["type"] == "mixed":
            draw_mixed_line(draw, ld["x"], ld["y"], ld["parts"])
        else:
            draw.text((ld["x"], ld["y"]), ld["text"], font=ld["font"], fill=hex_to_rgb(COLORS["text"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_vertical_slide(main_text, sub_text, output_path, highlight_main=False):
    """Vertical text slide (Simplified)"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    font_main = get_font(180)
    char_heights = []
    total_height = 0
    
    for char in main_text:
        w, h = get_text_size(draw, char, font_main)
        char_heights.append({"char": char, "w": w, "h": h})
        total_height += h + 10
    
    start_y = (IMAGE_SIZE[1] - total_height) // 2
    x = 150
    
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
    """CTA slide (Re-centered & Larger text)"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)
    
    # Increased font sizes
    font_cta, _ = fit_font_size(draw, main_cta, 100, MAX_WIDTH - 60)
    cta_w, cta_h = get_text_size(draw, main_cta, font_cta)
    
    # Calculate total height for centering
    sub_heights = []
    for line in sub_lines:
        font_sub, _ = fit_font_size(draw, line, 64, MAX_WIDTH)
        w, h = get_text_size(draw, line, font_sub)
        sub_heights.append({"font": font_sub, "w": w, "h": h, "line": line})
    
    total_sub_height = sum(sh["h"] + 30 for sh in sub_heights)
    total_height = cta_h + 50 + total_sub_height
    
    # Center Y
    start_y = (IMAGE_SIZE[1] - total_height) // 2
    
    # Draw main CTA
    cta_x = (IMAGE_SIZE[0] - cta_w) // 2
    draw.text((cta_x, start_y), main_cta, font=font_cta, fill=hex_to_rgb(COLORS["text"]))
    
    # Draw sub lines
    sub_y = start_y + cta_h + 50
    for sh in sub_heights:
        x = (IMAGE_SIZE[0] - sh["w"]) // 2
        draw.text((x, sub_y), sh["line"], font=sh["font"], fill=hex_to_rgb(COLORS["text"]))
        sub_y += sh["h"] + 30
    
    # Bottom follow text
    font_follow = ImageFont.truetype(FONTS["thin"], 36)
    fw, _ = get_text_size(draw, follow_text, font_follow)
    draw.text(((IMAGE_SIZE[0] - fw) // 2, IMAGE_SIZE[1] - 100), follow_text, 
              font=font_follow, fill=hex_to_rgb(COLORS["gray"]))
    
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")



def generate_btob_part1():
    """Part 1: 集客の構造変革 - 「即予約」から「リード獲得」へ"""
    output_dir = "output/btob_part1"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1 - 衝撃
    create_impact_slide_1("即予約", "その戦略、もう通用しない", "lead generation", f"{output_dir}/slide_01.png")
    
    # Slide 2 - 共感
    create_impact_slide([
        {"text": "Instagramから", "size": "l"},
        {"text": "即予約を期待している", "size": "l"},
        {"text": ""},
        {"text": "こんな経験ありませんか？", "size": "m"},
    ], f"{output_dir}/slide_02.png")
    
    # Slide 3 - 縦文字
    create_vertical_slide("比較", "2026年は比較検討の時代", f"{output_dir}/slide_03.png")
    
    # Slide 4 - 真実①
    create_impact_slide([
        {"parts": [("初見", "xl", False), ("で予約は", "l", False)]},
        {"text": "もはやレアケース", "size": "l"},
        {"text": ""},
        {"text": "見込み客は比較検討する", "size": "m"},
        {"text": "「すぐ予約」は心理障壁が高い", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # Slide 5 - 真実②
    create_impact_slide([
        {"text": "2段階集客という考え方", "size": "l"},
        {"text": ""},
        {"parts": [("まず", "l", False), ("繋がる", "xl", False)]},
        {"text": ""},
        {"text": "LINE登録 or フォロー", "size": "m"},
        {"text": "小さなコミットメントから始める", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # Slide 6 - 縦文字
    create_vertical_slide("信頼", "まず関係を築く", f"{output_dir}/slide_06.png")
    
    # Slide 7 - アクション①
    create_impact_slide([
        {"text": "リード獲得の2つの方法", "size": "l"},
        {"text": ""},
        {"text": "A: LINE登録を促す", "size": "m"},
        {"text": "B: フォローを促す", "size": "m"},
        {"text": ""},
        {"text": "→ ストーリーズで教育", "size": "m"},
    ], f"{output_dir}/slide_07.png")
    
    # Slide 8 - 具体例
    create_impact_slide([
        {"text": "教育の具体例", "size": "l"},
        {"text": ""},
        {"text": "LINE→ステップ配信", "size": "m"},
        {"text": "フォロー→ストーリーズ", "size": "m"},
        {"text": ""},
        {"text": "毎日の接点で信頼を築く", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # Slide 9 - まとめ
    create_vertical_slide("育成", "見込み客を育てる発想", f"{output_dir}/slide_09.png")
    
    # Slide 10 - CTA (保存される情報付き)
    create_impact_cta(
        "2段階集客を始める",
        ["A: LINE登録→ステップ配信", "B: フォロー→ストーリーズ教育", "→予約オファー"],
        "保存して実践 → 明日は「経営の科学化」",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ Part 1 complete! Check {output_dir}/")


def generate_btob_part2():
    """Part 2: 経営の科学化と権威化"""
    output_dir = "output/btob_part2"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1 - 衝撃
    create_impact_slide_1("単価UP", "価格を言う前にやること", "pricing", f"{output_dir}/slide_01.png")
    
    # Slide 2 - 共感
    create_impact_slide([
        {"text": "高単価メニューを提案すると", "size": "l"},
        {"text": "「高い」と言われる", "size": "l"},
        {"text": ""},
        {"text": "こんな経験ないだろうか", "size": "m"},
    ], f"{output_dir}/slide_02.png")
    
    # Slide 3 - 縦文字
    create_vertical_slide("原因", "伝える順番が逆", f"{output_dir}/slide_03.png")
    
    # Slide 4 - 真実
    create_impact_slide([
        {"text": "価格より先に", "size": "l"},
        {"text": "「価値」を伝える", "size": "xl"},
        {"text": ""},
        {"text": "順番を変えるだけで", "size": "m"},
        {"text": "納得感が生まれる", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # Slide 5 - テンプレート
    create_impact_slide([
        {"text": "伝える順番", "size": "l"},
        {"text": ""},
        {"text": "①お客様の悩み", "size": "m"},
        {"text": "②解決できる理由", "size": "m"},
        {"text": "③価格", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # Slide 6 - 具体例①
    create_impact_slide([
        {"text": "NG例", "size": "l"},
        {"text": ""},
        {"text": "「トリートメント3,000円です」", "size": "m"},
        {"text": ""},
        {"text": "→価格だけ聞くと高く感じる", "size": "m"},
    ], f"{output_dir}/slide_06.png")
    
    # Slide 7 - 具体例②
    create_impact_slide([
        {"text": "OK例", "size": "l"},
        {"text": ""},
        {"text": "「毛先のパサつき気になりますよね」", "size": "s"},
        {"text": "「このトリートメントで", "size": "s"},
        {"text": "1ヶ月まとまりが続きます」", "size": "s"},
        {"text": "「3,000円で悩みが解決します」", "size": "s"},
    ], f"{output_dir}/slide_07.png")
    
    # Slide 8 - 応用
    create_impact_slide([
        {"text": "使える場面", "size": "l"},
        {"text": ""},
        {"text": "施術中の追加提案", "size": "m"},
        {"text": "次回予約のメニュー提案", "size": "m"},
        {"text": "店販商品の紹介", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # Slide 9 - まとめ
    create_vertical_slide("順番", "価値→価格の順で伝える", f"{output_dir}/slide_09.png")
    
    # Slide 10 - CTA
    create_impact_cta(
        "今日から使ってみる",
        ["①お客様の悩みを確認", "②解決できる理由を説明", "③最後に価格を伝える"],
        "保存して施術中に実践",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ Part 2 complete! Check {output_dir}/")


def generate_btob_part3():
    """Part 3: 紹介を増やす仕組み"""
    output_dir = "output/btob_part3"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1 - 衝撃
    create_impact_slide_1("紹介", "偶然ではなく仕組みで増やす", "referral", f"{output_dir}/slide_01.png")
    
    # Slide 2 - 共感
    create_impact_slide([
        {"text": "紹介がなかなか", "size": "l"},
        {"text": "増えない", "size": "l"},
        {"text": ""},
        {"text": "待っているだけになっていないか", "size": "m"},
    ], f"{output_dir}/slide_02.png")
    
    # Slide 3 - 縦文字
    create_vertical_slide("原因", "「紹介してね」だけでは弱い", f"{output_dir}/slide_03.png")
    
    # Slide 4 - 真実
    create_impact_slide([
        {"text": "紹介は", "size": "l"},
        {"text": "仕組みで増える", "size": "xl"},
        {"text": ""},
        {"text": "お客様が紹介しやすい", "size": "m"},
        {"text": "状況を作ってあげる", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # Slide 5 - テンプレート
    create_impact_slide([
        {"text": "紹介が増える3ステップ", "size": "l"},
        {"text": ""},
        {"text": "①紹介カードを渡す", "size": "m"},
        {"text": "②紹介された人に特典", "size": "m"},
        {"text": "③紹介してくれた人にお礼", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # Slide 6 - 具体例①
    create_impact_slide([
        {"text": "紹介カードの文言例", "size": "l"},
        {"text": ""},
        {"text": "「〇〇さんのご紹介で」", "size": "m"},
        {"text": "「初回20%OFF」", "size": "m"},
        {"text": ""},
        {"text": "→お客様が説明しなくて済む", "size": "m"},
    ], f"{output_dir}/slide_06.png")
    
    # Slide 7 - 具体例②
    create_impact_slide([
        {"text": "お礼メッセージ例", "size": "l"},
        {"text": ""},
        {"text": "「〇〇様のご紹介で", "size": "s"},
        {"text": "△△様がご来店されました」", "size": "s"},
        {"text": "「次回トリートメント", "size": "s"},
        {"text": "サービスさせてください」", "size": "s"},
    ], f"{output_dir}/slide_07.png")
    
    # Slide 8 - タイミング
    create_impact_slide([
        {"text": "紹介カードを渡すタイミング", "size": "l"},
        {"text": ""},
        {"text": "「仕上がりいかがですか」", "size": "m"},
        {"text": "「ありがとうございます」", "size": "m"},
        {"text": "→のタイミングで自然に", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # Slide 9 - まとめ
    create_vertical_slide("仕組", "紹介しやすい環境を作る", f"{output_dir}/slide_09.png")
    
    # Slide 10 - CTA
    create_impact_cta(
        "紹介の仕組みを作る",
        ["①紹介カードを作る", "②特典を決める", "③お礼の流れを決める"],
        "3日間の投稿を保存して実践",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ Part 3 complete! Check {output_dir}/")


def generate_hourglass_part1():
    """Hourglass Part 1: 戦略と理想の顧客"""
    output_dir = "output/hourglass_part1"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1 - 衝撃
    create_impact_slide_1("戦略", "Instagramの前にやるべきこと", "strategy first", f"{output_dir}/slide_01.png")
    
    # Slide 2 - 共感
    create_impact_slide([
        {"text": "毎日投稿しているのに", "size": "l"},
        {"text": "予約に繋がらない", "size": "l"},
        {"text": ""},
        {"text": "こんな状況ではないだろうか", "size": "m"},
    ], f"{output_dir}/slide_02.png")
    
    # Slide 3 - 縦文字
    create_vertical_slide("戦術", "投稿は戦術に過ぎない", f"{output_dir}/slide_03.png")
    
    # Slide 4 - 真実①
    create_impact_slide([
        {"text": "戦略なくして戦術なし", "size": "l"},
        {"text": ""},
        {"parts": [("誰", "xl", False), ("に売るか", "l", False)]},
        {"text": ""},
        {"text": "これを決めずに投稿しても", "size": "m"},
        {"text": "時間の無駄になる", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # Slide 5 - 真実②
    create_impact_slide([
        {"text": "理想のクライアントを", "size": "l"},
        {"text": "極小化する", "size": "xl"},
        {"text": ""},
        {"text": "「近所の人」ではなく", "size": "m"},
        {"text": "収益性が高く推薦してくれる人", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # Slide 6 - 縦文字
    create_vertical_slide("言語", "「美容師です」は価値ゼロ", f"{output_dir}/slide_06.png")
    
    # Slide 7 - アクション①
    create_impact_slide([
        {"text": "トーキング・ロゴを作る", "size": "l"},
        {"text": ""},
        {"text": "動詞＋ターゲット＋価値", "size": "m"},
        {"text": ""},
        {"text": "「忙しい働く女性に", "size": "m"},
        {"text": "朝のセット時間を半分にする」", "size": "m"},
    ], f"{output_dir}/slide_07.png")
    
    # Slide 8 - 具体例
    create_impact_slide([
        {"text": "聞き手が思わず", "size": "l"},
        {"text": "「もっと知りたい」", "size": "xl"},
        {"text": ""},
        {"text": "そう思わせるメッセージが", "size": "m"},
        {"text": "全ての起点になる", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # Slide 9 - まとめ
    create_vertical_slide("起点", "戦略が全ての土台", f"{output_dir}/slide_09.png")
    
    # Slide 10 - CTA
    create_impact_cta(
        "戦略を言語化する",
        ["1. 理想のクライアントを定義", "2. トーキング・ロゴを作る", "3. 全ての発信に一貫性を"],
        "保存して実践 → 明日は「砂時計の7ステップ」",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ Hourglass Part 1 complete! Check {output_dir}/")


def generate_hourglass_part2():
    """Hourglass Part 2: 砂時計の7ステップ"""
    output_dir = "output/hourglass_part2"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1 - 衝撃
    create_impact_slide_1("砂時計", "サロン経営の7段階設計", "hourglass", f"{output_dir}/slide_01.png")
    
    # Slide 2 - 共感
    create_impact_slide([
        {"text": "新規客は来るのに", "size": "l"},
        {"text": "リピートしてくれない", "size": "l"},
        {"text": ""},
        {"text": "紹介もなかなか生まれない", "size": "m"},
    ], f"{output_dir}/slide_02.png")
    
    # Slide 3 - 縦文字
    create_vertical_slide("漏斗", "ファネルだけでは不十分", f"{output_dir}/slide_03.png")
    
    # Slide 4 - 真実①
    create_impact_slide([
        {"text": "砂時計の7ステップ", "size": "l"},
        {"text": ""},
        {"text": "知る→好きになる→信頼", "size": "m"},
        {"text": "→試す→買う", "size": "m"},
        {"text": "→リピート→推薦", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # Slide 5 - 真実②
    create_impact_slide([
        {"text": "「教育」で信頼を築く", "size": "l"},
        {"text": ""},
        {"parts": [("出版社", "xl", False), ("の熱量で", "l", False)]},
        {"text": ""},
        {"text": "広告よりも有益な情報", "size": "m"},
        {"text": "これが競合との差別化になる", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # Slide 6 - 縦文字
    create_vertical_slide("試用", "お試しで最初の一歩を", f"{output_dir}/slide_06.png")
    
    # Slide 7 - アクション①
    create_impact_slide([
        {"text": "お試しステップの設計", "size": "l"},
        {"text": ""},
        {"text": "無料診断", "size": "m"},
        {"text": "低価格トライアル", "size": "m"},
        {"text": ""},
        {"text": "ハードルを下げて一歩目を", "size": "m"},
    ], f"{output_dir}/slide_07.png")
    
    # Slide 8 - 具体例
    create_impact_slide([
        {"text": "紹介はシステムである", "size": "l"},
        {"text": ""},
        {"text": "偶然ではなく", "size": "m"},
        {"parts": [("仕組み", "xl", False), ("として作る", "l", False)]},
        {"text": ""},
        {"text": "既存客が新規を連れてくる", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # Slide 9 - まとめ
    create_vertical_slide("循環", "砂時計は回り続ける", f"{output_dir}/slide_09.png")
    
    # Slide 10 - CTA
    create_impact_cta(
        "砂時計を設計する",
        ["1. 教育コンテンツを作る", "2. お試しを設計する", "3. 紹介をシステム化"],
        "保存して実践 → 明日は「自動灌漑システム」",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ Hourglass Part 2 complete! Check {output_dir}/")


def generate_hourglass_part3():
    """Hourglass Part 3: 自動灌漑システム"""
    output_dir = "output/hourglass_part3"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1 - 衝撃
    create_impact_slide_1("灌漑", "花火ではなく、毎日水を", "irrigation", f"{output_dir}/slide_01.png")
    
    # Slide 2 - 共感
    create_impact_slide([
        {"text": "キャンペーンを打っても", "size": "l"},
        {"text": "効果が一時的で終わる", "size": "l"},
        {"text": ""},
        {"text": "こんな経験はないだろうか", "size": "m"},
    ], f"{output_dir}/slide_02.png")
    
    # Slide 3 - 縦文字
    create_vertical_slide("花火", "単発施策は消えてなくなる", f"{output_dir}/slide_03.png")
    
    # Slide 4 - 真実①
    create_impact_slide([
        {"text": "自動灌漑システム", "size": "l"},
        {"text": ""},
        {"parts": [("毎日", "xl", False), ("水を供給", "l", False)]},
        {"text": ""},
        {"text": "24時間365日", "size": "m"},
        {"text": "教育と信頼構築を自動で", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # Slide 5 - 真実②
    create_impact_slide([
        {"text": "ウェブサイトを", "size": "l"},
        {"text": "「ハブ」にする", "size": "xl"},
        {"text": ""},
        {"text": "SNSは入り口に過ぎない", "size": "m"},
        {"text": "全てを集約する場所を作る", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # Slide 6 - 縦文字
    create_vertical_slide("価値", "安売りはブランドを殺す", f"{output_dir}/slide_06.png")
    
    # Slide 7 - アクション①
    create_impact_slide([
        {"text": "価格は価値を語る", "size": "l"},
        {"text": ""},
        {"text": "高価格は信頼された", "size": "m"},
        {"text": "顧客にだけ売る", "size": "m"},
        {"text": ""},
        {"text": "特別感と収益性を両立", "size": "m"},
    ], f"{output_dir}/slide_07.png")
    
    # Slide 8 - 具体例
    create_impact_slide([
        {"text": "マーケティング", "size": "l"},
        {"text": "カレンダーを作る", "size": "l"},
        {"text": ""},
        {"text": "感情や思いつきではなく", "size": "m"},
        {"text": "年間計画に沿って一貫性を", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # Slide 9 - まとめ
    create_vertical_slide("種撒", "顧客が種を撒いてくれる", f"{output_dir}/slide_09.png")
    
    # Slide 10 - CTA
    create_impact_cta(
        "灌漑システムを構築",
        ["1. ウェブサイトをハブに", "2. 価格で価値を語る", "3. 年間カレンダーを作る"],
        "3日間の投稿を保存して実践",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ Hourglass Part 3 complete! Check {output_dir}/")


def generate_practical_day1():
    """実践シリーズ Day 1: 予約が入る自己紹介の作り方"""
    output_dir = "output/practical_day1"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1 - 衝撃
    create_impact_slide_1("自己紹介のコツ", "インスタで覚えてもらうために", "self intro", f"{output_dir}/slide_01.png")
    
    # Slide 2 - 共感
    create_impact_slide([
        {"text": "プロフィールを見ても", "size": "l"},
        {"text": "何の専門家かわからない", "size": "l"},
        {"text": ""},
        {"text": "こんなアカウント多くないか", "size": "m"},
    ], f"{output_dir}/slide_02.png")
    
    # Slide 3 - 縦文字
    create_vertical_slide("原因", "肩書きだけでは伝わらない", f"{output_dir}/slide_03.png")
    
    # Slide 4 - 真実
    create_impact_slide([
        {"text": "覚えてもらえる自己紹介", "size": "l"},
        {"text": ""},
        {"text": "誰に＋何を＋どうなる", "size": "xl"},
        {"text": ""},
        {"text": "この3つを入れるだけ", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # Slide 5 - テンプレート（保存ポイント①）
    create_impact_slide([
        {"text": "テンプレート", "size": "l"},
        {"text": ""},
        {"text": "「〇〇な人に」", "size": "m"},
        {"text": "「〇〇を提供して」", "size": "m"},
        {"text": "「〇〇になれる美容師」", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # Slide 6 - 具体例①
    create_impact_slide([
        {"text": "例①", "size": "l"},
        {"text": ""},
        {"text": "「忙しい30代ママに」", "size": "m"},
        {"text": "「朝10分でキマるカットで」", "size": "m"},
        {"text": "「毎朝をラクにする美容師」", "size": "m"},
    ], f"{output_dir}/slide_06.png")
    
    # Slide 7 - 具体例②
    create_impact_slide([
        {"text": "例②", "size": "l"},
        {"text": ""},
        {"text": "「白髪が気になる40代に」", "size": "m"},
        {"text": "「ダメージレスなカラーで」", "size": "m"},
        {"text": "「−5歳を叶える美容師」", "size": "m"},
    ], f"{output_dir}/slide_07.png")
    
    # Slide 8 - 具体例③
    create_impact_slide([
        {"text": "例③", "size": "l"},
        {"text": ""},
        {"text": "「くせ毛に悩む人に」", "size": "m"},
        {"text": "「縮毛矯正なしのカットで」", "size": "m"},
        {"text": "「毎朝の悩みを解消する美容師」", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # Slide 9 - 使い方
    create_impact_slide([
        {"text": "この自己紹介を使う場所", "size": "l"},
        {"text": ""},
        {"text": "プロフィール欄", "size": "m"},
        {"text": "名刺・チラシ", "size": "m"},
        {"text": "初対面の挨拶", "size": "m"},
    ], f"{output_dir}/slide_09.png")
    
    # Slide 10 - CTA
    create_impact_cta(
        "自分の自己紹介を作る",
        ["誰に：ターゲットを1つに絞る", "何を：自分の強みを1つ選ぶ", "どうなる：お客様の変化を書く"],
        "保存してプロフに反映 → 明日は「リピートの7タイミング」",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ Practical Day 1 complete! Check {output_dir}/")


def generate_practical_day2():
    """実践シリーズ Day 2: リピートを増やすタイミング"""
    output_dir = "output/practical_day2"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1 - 衝撃
    create_impact_slide_1("リピート", "次回予約を取るベストタイミング", "repeat", f"{output_dir}/slide_01.png")
    
    # Slide 2 - 共感
    create_impact_slide([
        {"text": "次回予約を提案しても", "size": "l"},
        {"text": "断られることが多い", "size": "l"},
        {"text": ""},
        {"text": "こんな経験ないだろうか", "size": "m"},
    ], f"{output_dir}/slide_02.png")
    
    # Slide 3 - 縦文字
    create_vertical_slide("原因", "タイミングが遅い", f"{output_dir}/slide_03.png")
    
    # Slide 4 - 真実
    create_impact_slide([
        {"text": "次回予約は", "size": "l"},
        {"text": "会計前に取る", "size": "xl"},
        {"text": ""},
        {"text": "帰る準備を始めると", "size": "m"},
        {"text": "断りやすくなる", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # Slide 5 - テンプレート
    create_impact_slide([
        {"text": "次回予約の流れ", "size": "l"},
        {"text": ""},
        {"text": "①仕上がり確認", "size": "m"},
        {"text": "②次回の提案", "size": "m"},
        {"text": "③日程を決める", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # Slide 6 - 具体例①
    create_impact_slide([
        {"text": "トーク例①", "size": "l"},
        {"text": ""},
        {"text": "「仕上がりいかがですか」", "size": "m"},
        {"text": "「このスタイルを保つには", "size": "m"},
        {"text": "〇週間後がベストです」", "size": "m"},
    ], f"{output_dir}/slide_06.png")
    
    # Slide 7 - 具体例②
    create_impact_slide([
        {"text": "トーク例②", "size": "l"},
        {"text": ""},
        {"text": "「次はこの辺りがオススメ」", "size": "m"},
        {"text": "「ご都合いかがですか」", "size": "m"},
        {"text": ""},
        {"text": "→具体的な日程を先に提案", "size": "m"},
    ], f"{output_dir}/slide_07.png")
    
    # Slide 8 - ポイント
    create_impact_slide([
        {"text": "断られにくくするコツ", "size": "l"},
        {"text": ""},
        {"text": "「予約しますか？」ではなく", "size": "m"},
        {"text": "「いつにしますか？」", "size": "m"},
        {"text": ""},
        {"text": "→予約する前提で聞く", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # Slide 9 - まとめ
    create_vertical_slide("先手", "会計前に日程を決める", f"{output_dir}/slide_09.png")
    
    # Slide 10 - CTA
    create_impact_cta(
        "今日から実践",
        ["①仕上がり確認の後に提案", "②具体的な日程を先に出す", "③「いつにしますか」と聞く"],
        "保存して次の施術で使う → 明日は「紹介の仕組み」",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ Practical Day 2 complete! Check {output_dir}/")


def generate_practical_day3():
    """実践シリーズ Day 3: 紹介を増やす仕組み"""
    output_dir = "output/practical_day3"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1 - 衝撃
    create_impact_slide_1("紹介", "偶然ではなく仕組みで増やす", "referral", f"{output_dir}/slide_01.png")
    
    # Slide 2 - 共感
    create_impact_slide([
        {"text": "紹介がなかなか", "size": "l"},
        {"text": "増えない", "size": "l"},
        {"text": ""},
        {"text": "待っているだけになっていないか", "size": "m"},
    ], f"{output_dir}/slide_02.png")
    
    # Slide 3 - 縦文字
    create_vertical_slide("原因", "「紹介してね」だけでは弱い", f"{output_dir}/slide_03.png")
    
    # Slide 4 - 真実
    create_impact_slide([
        {"text": "紹介は", "size": "l"},
        {"text": "仕組みで増える", "size": "xl"},
        {"text": ""},
        {"text": "お客様が紹介しやすい", "size": "m"},
        {"text": "状況を作ってあげる", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # Slide 5 - テンプレート
    create_impact_slide([
        {"text": "紹介が増える3ステップ", "size": "l"},
        {"text": ""},
        {"text": "①紹介カードを渡す", "size": "m"},
        {"text": "②紹介された人に特典", "size": "m"},
        {"text": "③紹介してくれた人にお礼", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # Slide 6 - 具体例①
    create_impact_slide([
        {"text": "紹介カードの文言例", "size": "l"},
        {"text": ""},
        {"text": "「〇〇さんのご紹介で」", "size": "m"},
        {"text": "「初回20%OFF」", "size": "m"},
        {"text": ""},
        {"text": "→お客様が説明しなくて済む", "size": "m"},
    ], f"{output_dir}/slide_06.png")
    
    # Slide 7 - 具体例②
    create_impact_slide([
        {"text": "お礼メッセージ例", "size": "l"},
        {"text": ""},
        {"text": "「〇〇様のご紹介で", "size": "s"},
        {"text": "△△様がご来店されました」", "size": "s"},
        {"text": "「次回トリートメント", "size": "s"},
        {"text": "サービスさせてください」", "size": "s"},
    ], f"{output_dir}/slide_07.png")
    
    # Slide 8 - タイミング
    create_impact_slide([
        {"text": "紹介カードを渡すタイミング", "size": "l"},
        {"text": ""},
        {"text": "「仕上がりいかがですか」", "size": "m"},
        {"text": "「ありがとうございます」", "size": "m"},
        {"text": "→のタイミングで自然に", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # Slide 9 - まとめ
    create_vertical_slide("仕組", "紹介しやすい環境を作る", f"{output_dir}/slide_09.png")
    
    # Slide 10 - CTA
    create_impact_cta(
        "紹介の仕組みを作る",
        ["①紹介カードを作る", "②特典を決める", "③お礼の流れを決める"],
        "3日間の投稿を保存して実践",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ Practical Day 3 complete! Check {output_dir}/")


def generate_scientific_mgmt():
    """経営の科学化 - 単価UPへの導入"""
    output_dir = "output/scientific_mgmt"
    os.makedirs(output_dir, exist_ok=True)
    
    # Slide 1 - 衝撃
    create_impact_slide_1("数字", "なんとなく経営を卒業する", "data driven", f"{output_dir}/slide_01.png")
    
    # Slide 2 - 共感
    create_impact_slide([
        {"text": "上手くいった理由が", "size": "l"},
        {"text": "わからない", "size": "l"},
        {"text": ""},
        {"text": "失敗した理由もわからない", "size": "m"},
    ], f"{output_dir}/slide_02.png")
    
    # Slide 3 - 縦文字
    create_vertical_slide("原因", "感覚で判断している", f"{output_dir}/slide_03.png")
    
    # Slide 4 - 真実
    create_impact_slide([
        {"text": "まず", "size": "l"},
        {"text": "記録する", "size": "xl"},
        {"text": ""},
        {"text": "数字がないと", "size": "m"},
        {"text": "改善のしようがない", "size": "m"},
    ], f"{output_dir}/slide_04.png")
    
    # Slide 5 - テンプレート
    create_impact_slide([
        {"text": "記録すべき3つの数字", "size": "l"},
        {"text": ""},
        {"text": "①新規数", "size": "m"},
        {"text": "②リピート率", "size": "m"},
        {"text": "③客単価", "size": "m"},
    ], f"{output_dir}/slide_05.png")
    
    # Slide 6 - 具体例①
    create_impact_slide([
        {"text": "新規数の見方", "size": "l"},
        {"text": ""},
        {"text": "どこから来たか", "size": "m"},
        {"text": "（インスタ/紹介/HPB）", "size": "m"},
        {"text": ""},
        {"text": "→効果のある集客に集中", "size": "m"},
    ], f"{output_dir}/slide_06.png")
    
    # Slide 7 - 具体例②
    create_impact_slide([
        {"text": "リピート率の見方", "size": "l"},
        {"text": ""},
        {"text": "新規のリピート率", "size": "m"},
        {"text": "既存のリピート率", "size": "m"},
        {"text": ""},
        {"text": "→どちらが課題か明確に", "size": "m"},
    ], f"{output_dir}/slide_07.png")
    
    # Slide 8 - 予告
    create_impact_slide([
        {"text": "客単価を上げるには", "size": "l"},
        {"text": ""},
        {"text": "数字を見るだけでなく", "size": "m"},
        {"text": "「伝え方」を変える必要がある", "size": "m"},
        {"text": ""},
        {"text": "→明日詳しく解説", "size": "m"},
    ], f"{output_dir}/slide_08.png")
    
    # Slide 9 - まとめ
    create_vertical_slide("習慣", "まず記録から始める", f"{output_dir}/slide_09.png")
    
    # Slide 10 - CTA
    create_impact_cta(
        "今月から記録を始める",
        ["①新規数を記録", "②リピート率を計算", "③客単価を把握"],
        "保存して実践 → 明日は「単価UPの伝え方」",
        f"{output_dir}/slide_10.png"
    )
    
    print(f"\n✅ Scientific Management complete! Check {output_dir}/")


if __name__ == "__main__":
    generate_scientific_mgmt()
