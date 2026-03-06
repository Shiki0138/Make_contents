# -*- coding: utf-8 -*-
"""
Instagram Carousel: LP content (10 slides)
"""

from carousel_generator import (
    IMAGE_SIZE, MARGIN, MAX_WIDTH, COLORS,
    hex_to_rgb, get_font, get_text_size, fit_font_size,
    create_title_slide, create_content_slide, create_cta_slide,
    add_avatar,
)
from PIL import Image, ImageDraw
import os


OUTPUT_DIR = "output/lp_shukyaku"


def create_hook_slide(output_path):
    """Slide 1: Hook - 集客にお金をかけるほど貧乏になる"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)

    lines = [
        {"text": "集客にお金をかけるほど", "size": 70, "color": "text"},
        {"text": "貧乏になる。", "size": 120, "highlight": True},
    ]
    sub_lines = [
        {"text": "美容師・歯医者の9割がやっている", "size": 44, "color": "gray"},
        {"text": "「集客の大きな勘違い」について。", "size": 44, "color": "gray"},
    ]

    # Main lines
    total_h = 0
    rendered = []
    for item in lines:
        font, _ = fit_font_size(draw, item["text"], item["size"], MAX_WIDTH - 40, min_size=40)
        w, h = get_text_size(draw, item["text"], font)
        rendered.append({"text": item["text"], "font": font, "w": w, "h": h,
                         "highlight": item.get("highlight", False),
                         "color": item.get("color", "text")})
        total_h += h + 25

    sub_rendered = []
    for item in sub_lines:
        font = get_font(item["size"], "thin")
        w, h = get_text_size(draw, item["text"], font)
        sub_rendered.append({"text": item["text"], "font": font, "w": w, "h": h})
        total_h += h + 20

    total_h += 40  # gap between main and sub
    start_y = (IMAGE_SIZE[1] - total_h) // 2
    y = start_y

    for r in rendered:
        x = (IMAGE_SIZE[0] - r["w"]) // 2
        if r["highlight"]:
            bar_h = max(int(r["h"] * 0.3), 10)
            pad_x = 8
            draw.rectangle([x - pad_x, y + r["h"] - bar_h + 4,
                            x + r["w"] + pad_x, y + r["h"] + 4],
                           fill=hex_to_rgb(COLORS["accent"]))
        color = hex_to_rgb(COLORS.get(r["color"], COLORS["text"]))
        draw.text((x, y), r["text"], font=r["font"], fill=color)
        y += r["h"] + 25

    y += 40
    for s in sub_rendered:
        x = (IMAGE_SIZE[0] - s["w"]) // 2
        draw.text((x, y), s["text"], font=s["font"], fill=hex_to_rgb(COLORS["gray"]))
        y += s["h"] + 20

    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_slide_2(output_path):
    """Slide 2: HPの否定"""
    lines = [
        {"text": "「HPを作れば集客できる」", "size": "l", "center": True},
        {"text": "はもう終わった。", "size": "l", "center": True, "highlight": True},
        {"text": ""},
        {"text": 'HPはサロンの"会社案内"だ。', "size": "m", "center": True},
        {"text": "情報を読んだお客さんは", "size": "s"},
        {"text": "「なるほど」と思って、帰る。", "size": "s"},
        {"text": "予約しない。", "size": "m", "highlight": True},
        {"text": ""},
        {"text": "HPは情報を置く場所であって", "size": "s"},
        {"text": "「人を動かす」場所ではない。", "size": "m"},
    ]
    create_content_slide(lines, output_path)


def create_slide_3(output_path):
    """Slide 3: 広告サイトの問題"""
    lines = [
        {"text": "広告サイトを使うほど", "size": "l", "center": True},
        {"text": "「あなたの客」は消える。", "size": "l", "center": True, "highlight": True},
        {"text": ""},
        {"text": "月6万円 → 年72万円が広告会社へ", "size": "s"},
        {"text": "掲載をやめた瞬間 → 集客ゼロ", "size": "s"},
        {"text": "比較画面の隣 → 常に競合が並ぶ", "size": "s"},
        {"text": ""},
        {"text": "育てているのは自分のサロンではなく", "size": "m"},
        {"text": "広告サイトだ。", "size": "l", "highlight": True},
    ]
    create_content_slide(lines, output_path)


def create_slide_4(output_path):
    """Slide 4: 構造的な問題の暴露"""
    lines = [
        {"text": "広告サイトは", "size": "m", "center": True},
        {"text": "「あなたを使って", "size": "l", "center": True},
        {"text": "競合を育てている」", "size": "l", "center": True, "highlight": True},
        {"text": ""},
        {"text": "・他店と必ず比較される", "size": "s"},
        {"text": "・安さ目当ての客が集まる", "size": "s"},
        {"text": "・客リストは広告サイトのもの", "size": "s"},
        {"text": "・やめたら全てリセット", "size": "s"},
    ]
    create_content_slide(lines, output_path)


def create_slide_5(output_path):
    """Slide 5: 本質 - 人が動く理由"""
    lines = [
        {"text": "人が動く理由は", "size": "l", "center": True},
        {"text": "たった一つだ。", "size": "xl", "center": True},
        {"text": ""},
        {"text": "「情報が多いから」ではない。", "size": "s", "center": True},
        {"text": "「安いから」でもない。", "size": "s", "center": True},
        {"text": ""},
        {"text": "「これは自分のことだ」", "size": "l", "center": True, "highlight": True},
        {"text": "と感じた瞬間に、人は動く。", "size": "m", "center": True},
    ]
    create_content_slide(lines, output_path)


def create_slide_6(output_path):
    """Slide 6: 勝ち負けの対比 - 上下2分割、背景色で明確に区別"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)

    half_h = IMAGE_SIZE[1] // 2

    # -- Top half: WIN (very light green tint) --
    draw.rectangle([0, 0, IMAGE_SIZE[0], half_h], fill=hex_to_rgb("#F2F9F2"))

    font_label = get_font(44, "thin")
    font_detail = get_font(62, "black")

    label = "集客で勝っているオーナー"
    lw, lh = get_text_size(draw, label, font_label)

    detail_lines = [
        "「白髪が気になり始めた",
        "30代女性」だけに",
        "語りかけるページを持っている",
    ]
    detail_heights = []
    for line in detail_lines:
        _, dh = get_text_size(draw, line, font_detail)
        detail_heights.append(dh)

    top_content_h = lh + 30 + sum(detail_heights) + 18 * (len(detail_lines) - 1)
    y = (half_h - top_content_h) // 2

    # Green accent bar left
    draw.rectangle([MARGIN, y - 10, MARGIN + 8, y + lh + 10], fill=hex_to_rgb("#4CAF50"))
    draw.text((MARGIN + 24, y), label, font=font_label, fill=hex_to_rgb("#4CAF50"))
    y += lh + 30

    for line in detail_lines:
        dw, dh = get_text_size(draw, line, font_detail)
        draw.text((MARGIN + 24, y), line, font=font_detail, fill=hex_to_rgb("#333333"))
        y += dh + 18

    # -- Bottom half: LOSE (light warm gray) --
    draw.rectangle([0, half_h, IMAGE_SIZE[0], IMAGE_SIZE[1]], fill=hex_to_rgb("#F0EDED"))

    lose_label = "集客で負けているオーナー"
    llw, llh = get_text_size(draw, lose_label, font_label)

    lose_lines = [
        "「当店のメニューはこちら」",
        "全員に向けて、誰にも刺さらない",
    ]
    lose_heights = []
    for line in lose_lines:
        _, lhh = get_text_size(draw, line, font_detail)
        lose_heights.append(lhh)

    bot_content_h = llh + 30 + sum(lose_heights) + 18 * (len(lose_lines) - 1)
    y = half_h + (half_h - bot_content_h) // 2

    # Red accent bar left
    draw.rectangle([MARGIN, y - 10, MARGIN + 8, y + llh + 10], fill=hex_to_rgb("#E53935"))
    draw.text((MARGIN + 24, y), lose_label, font=font_label, fill=hex_to_rgb("#E53935"))
    y += llh + 30

    for line in lose_lines:
        dw, dh = get_text_size(draw, line, font_detail)
        draw.text((MARGIN + 24, y), line, font=font_detail, fill=hex_to_rgb("#999999"))
        y += dh + 18

    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_slide_7(output_path):
    """Slide 7: 解決策 = LP"""
    lines = [
        {"text": "「一枚のLP」が", "size": "l", "center": True},
        {"text": "集客を資産に変える", "size": "l", "center": True, "highlight": True},
        {"text": ""},
        {"text": "① 来る理由を決めてから来る", "size": "s"},
        {"text": "→ 値引き交渉なし、初回から単価UP", "size": "s"},
        {"text": ""},
        {"text": "② 24時間365日、代わりに営業", "size": "s"},
        {"text": "→ 寝ている間に予約が届く", "size": "s"},
        {"text": ""},
        {"text": "③ 積み上がるから消えない", "size": "s"},
        {"text": "→ 広告と違い、資産として残る", "size": "s"},
    ]
    create_content_slide(lines, output_path)


def create_slide_8(output_path):
    """Slide 8: Before/After - 上下2分割、背景色で対比"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)

    half_h = IMAGE_SIZE[1] // 2
    font_heading = get_font(64, "black")
    font_item = get_font(42, "black")

    # -- Top half: BEFORE (light warm gray) --
    draw.rectangle([0, 0, IMAGE_SIZE[0], half_h], fill=hex_to_rgb("#F5F2F0"))

    before_title = "LP導入前"
    tw, th = get_text_size(draw, before_title, font_heading)

    before_items = [
        "毎月6万円を広告サイトに払う",
        "「いくらですか？」と聞かれる",
        "クーポン客が来てリピートしない",
        "やめたら翌月から予約ゼロ",
    ]
    item_heights = []
    for item in before_items:
        _, ih = get_text_size(draw, item, font_item)
        item_heights.append(ih)

    content_h = th + 25 + sum(item_heights) + 20 * (len(before_items) - 1)
    y = (half_h - content_h) // 2

    # Red heading with underline
    tx = (IMAGE_SIZE[0] - tw) // 2
    draw.text((tx, y), before_title, font=font_heading, fill=hex_to_rgb("#E53935"))
    draw.rectangle([tx, y + th + 5, tx + tw, y + th + 11], fill=hex_to_rgb("#E53935"))
    y += th + 25

    for item in before_items:
        iw, ih = get_text_size(draw, item, font_item)
        ix = (IMAGE_SIZE[0] - iw) // 2
        draw.text((ix, y), item, font=font_item, fill=hex_to_rgb("#888888"))
        y += ih + 20

    # -- Bottom half: AFTER (soft dark) --
    draw.rectangle([0, half_h, IMAGE_SIZE[0], IMAGE_SIZE[1]], fill=hex_to_rgb("#2D2D2D"))

    after_title = "LP導入後"
    tw, th = get_text_size(draw, after_title, font_heading)

    after_items = [
        "「予約したいです」と決めて来る",
        "「あなたに任せたい」と言われる",
        "広告費ゼロでも毎月新規が来る",
        "集客が「資産」になる",
    ]
    item_heights = []
    for item in after_items:
        _, ih = get_text_size(draw, item, font_item)
        item_heights.append(ih)

    content_h = th + 25 + sum(item_heights) + 20 * (len(after_items) - 1)
    y = half_h + (half_h - content_h) // 2

    # Yellow heading with underline bar
    tx = (IMAGE_SIZE[0] - tw) // 2
    bar_h = max(int(th * 0.3), 10)
    pad_x = 8
    draw.rectangle([tx - pad_x, y + th - bar_h + 4,
                    tx + tw + pad_x, y + th + 4],
                   fill=hex_to_rgb(COLORS["accent"]))
    draw.text((tx, y), after_title, font=font_heading, fill=hex_to_rgb("#FFFFFF"))
    y += th + 25

    for item in after_items:
        iw, ih = get_text_size(draw, item, font_item)
        ix = (IMAGE_SIZE[0] - iw) // 2
        draw.text((ix, y), item, font=font_item, fill=hex_to_rgb("#FFFFFF"))
        y += ih + 20

    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_slide_9(output_path):
    """Slide 9: 損失の可視化"""
    lines = [
        {"text": "「いつかやろう」と", "size": "l", "center": True},
        {"text": "思っている間も", "size": "l", "center": True},
        {"text": "毎月お金は消えていく。", "size": "l", "center": True, "highlight": True},
        {"text": ""},
        {"text": "広告サイトに払う月6万円があれば", "size": "s"},
        {"text": "LPは作れる。", "size": "m"},
        {"text": "しかも一度作れば資産として残る。", "size": "s"},
        {"text": ""},
        {"text": "今月やらなければ——", "size": "m"},
        {"text": "6万円x12ヶ月＝72万円がまた消える。", "size": "m", "highlight": True},
    ]
    create_content_slide(lines, output_path)


def create_slide_10(output_path):
    """Slide 10: CTA"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)

    lines = [
        {"text": "「来るべき客だけが来る仕組み」", "size": 72},
        {"text": "あなたのサロンにも作れる。", "size": 72},
        {"text": "", "size": 0},
        {"text": "LPの詳細はプロフィールから", "size": 56},
    ]

    rendered = []
    total_h = 0
    for item in lines:
        if item["text"] == "":
            rendered.append({"text": "", "h": 50})
            total_h += 50
            continue
        font, _ = fit_font_size(draw, item["text"], item["size"], MAX_WIDTH - 40, min_size=36)
        w, h = get_text_size(draw, item["text"], font)
        rendered.append({"text": item["text"], "font": font, "w": w, "h": h})
        total_h += h + 30

    y = (IMAGE_SIZE[1] - total_h) // 2
    for r in rendered:
        if r["text"] == "":
            y += r["h"]
            continue
        x = (IMAGE_SIZE[0] - r["w"]) // 2
        draw.text((x, y), r["text"], font=r["font"], fill=hex_to_rgb(COLORS["text"]))
        y += r["h"] + 30

    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def generate_all():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    slides = [
        ("slide_01_hook.png", create_hook_slide),
        ("slide_02_hp_denial.png", create_slide_2),
        ("slide_03_ad_problem.png", create_slide_3),
        ("slide_04_structure.png", create_slide_4),
        ("slide_05_essence.png", create_slide_5),
        ("slide_06_comparison.png", create_slide_6),
        ("slide_07_solution_lp.png", create_slide_7),
        ("slide_08_before_after.png", create_slide_8),
        ("slide_09_loss.png", create_slide_9),
        ("slide_10_cta.png", create_slide_10),
    ]

    for filename, func in slides:
        path = os.path.join(OUTPUT_DIR, filename)
        func(path)

    print(f"\n全10枚の生成が完了しました: {OUTPUT_DIR}/")


if __name__ == "__main__":
    generate_all()
