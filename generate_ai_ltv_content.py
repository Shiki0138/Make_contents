# -*- coding: utf-8 -*-
"""
Instagram Carousel: 2026 AI時代の集客 x LTV (10 slides)
"""

from carousel_generator import (
    IMAGE_SIZE, MARGIN, MAX_WIDTH, COLORS,
    hex_to_rgb, get_font, get_text_size, fit_font_size,
    create_content_slide, create_cta_slide,
)
from PIL import Image, ImageDraw
import os


OUTPUT_DIR = "output/ai_ltv_shukyaku"


def create_slide_1(output_path):
    """Slide 1: Hook"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)

    lines = [
        {"text": "2026年、AIが変えたのは", "size": 85, "highlight": False},
        {"text": "「集客の方法」ではない。", "size": 85, "highlight": False},
        {"text": "「来る客の質」だ。", "size": 140, "highlight": True},
    ]
    sub_lines = [
        {"text": "AI時代の集客で差がつくのは", "size": 44},
        {"text": "LTVという考え方。", "size": 44},
    ]

    rendered = []
    total_h = 0
    for item in lines:
        font, _ = fit_font_size(draw, item["text"], item["size"], MAX_WIDTH - 40, min_size=40)
        w, h = get_text_size(draw, item["text"], font)
        rendered.append({"text": item["text"], "font": font, "w": w, "h": h,
                         "highlight": item.get("highlight", False)})
        total_h += h + 25

    sub_rendered = []
    for item in sub_lines:
        font = get_font(item["size"], "thin")
        w, h = get_text_size(draw, item["text"], font)
        sub_rendered.append({"text": item["text"], "font": font, "w": w, "h": h})
        total_h += h + 20

    total_h += 40
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
        draw.text((x, y), r["text"], font=r["font"], fill=hex_to_rgb(COLORS["text"]))
        y += r["h"] + 25

    y += 40
    for s in sub_rendered:
        x = (IMAGE_SIZE[0] - s["w"]) // 2
        draw.text((x, y), s["text"], font=s["font"], fill=hex_to_rgb(COLORS["gray"]))
        y += s["h"] + 20

    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_slide_2(output_path):
    """Slide 2: 現状の問題"""
    lines = [
        {"text": "クーポンで来た客は", "size": "l", "center": True},
        {"text": "クーポンがなくなれば消える。", "size": "l", "center": True, "highlight": True},
        {"text": ""},
        {"text": "広告サイトで来た客は", "size": "m", "center": True},
        {"text": "来月には別の店に行く。", "size": "m", "center": True},
        {"text": ""},
        {"text": "集客数は増えても", "size": "s", "center": True},
        {"text": "売上が安定しない理由はここにある。", "size": "m", "center": True},
    ]
    create_content_slide(lines, output_path)


def create_slide_3(output_path):
    """Slide 3: LTVの概念提示"""
    lines = [
        {"text": "集客で見るべき数字は", "size": "l", "center": True},
        {"text": "「新規の数」ではない。", "size": "l", "center": True, "highlight": True},
        {"text": ""},
        {"text": "1人の客が生涯でいくら使うか。", "size": "m", "center": True},
        {"text": "これがLTV。", "size": "l", "center": True},
        {"text": ""},
        {"text": "月10人の新規より", "size": "s", "center": True},
        {"text": "月3人の「通い続ける客」のほうが", "size": "s", "center": True},
        {"text": "売上は大きくなる。", "size": "m", "center": True},
    ]
    create_content_slide(lines, output_path)


def create_slide_4(output_path):
    """Slide 4: なぜLTVが低くなるか"""
    lines = [
        {"text": "LTVが低い店には", "size": "l", "center": True},
        {"text": "共通点がある。", "size": "l", "center": True},
        {"text": ""},
        {"text": "「来る理由」を", "size": "m", "center": True},
        {"text": "客に決めさせていない。", "size": "l", "center": True, "highlight": True},
        {"text": ""},
        {"text": "比較で選ばれ、値段で選ばれる。", "size": "s", "center": True},
        {"text": "理由なく来た客は", "size": "m", "center": True},
        {"text": "理由なく離れる。", "size": "m", "center": True},
    ]
    create_content_slide(lines, output_path)


def create_slide_5(output_path):
    """Slide 5: AI時代の変化"""
    lines = [
        {"text": "2026年、", "size": "m", "center": True},
        {"text": "客は来店前にAIに聞く。", "size": "l", "center": True},
        {"text": ""},
        {"text": "「この悩みに合う店はどこ？」", "size": "m", "center": True},
        {"text": ""},
        {"text": "AIが返すのは", "size": "s", "center": True},
        {"text": "広告サイトのランキングではない。", "size": "s", "center": True},
        {"text": "その悩みに「明確な答え」を", "size": "m", "center": True},
        {"text": "持っているページだ。", "size": "l", "center": True, "highlight": True},
    ]
    create_content_slide(lines, output_path)


def create_slide_6(output_path):
    """Slide 6: 対比 - LTV高い店 vs 低い店"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)

    half_h = IMAGE_SIZE[1] // 2

    # -- Top half: HIGH LTV --
    draw.rectangle([0, 0, IMAGE_SIZE[0], half_h], fill=hex_to_rgb("#F2F9F2"))

    font_label = get_font(44, "thin")
    font_detail = get_font(58, "black")

    label = "LTVが高い店"
    lw, lh = get_text_size(draw, label, font_label)

    detail_lines = [
        "「産後の抜け毛に悩む30代女性」",
        "に向けた専用ページがある。",
        "悩みを理解している店として",
        "選ばれる。",
    ]
    detail_heights = []
    for line in detail_lines:
        _, dh = get_text_size(draw, line, font_detail)
        detail_heights.append(dh)

    top_content_h = lh + 30 + sum(detail_heights) + 16 * (len(detail_lines) - 1)
    y = (half_h - top_content_h) // 2

    draw.rectangle([MARGIN, y - 10, MARGIN + 8, y + lh + 10], fill=hex_to_rgb("#4CAF50"))
    draw.text((MARGIN + 24, y), label, font=font_label, fill=hex_to_rgb("#4CAF50"))
    y += lh + 30

    for line in detail_lines:
        draw.text((MARGIN + 24, y), line, font=font_detail, fill=hex_to_rgb("#333333"))
        _, dh = get_text_size(draw, line, font_detail)
        y += dh + 16

    # -- Bottom half: LOW LTV --
    draw.rectangle([0, half_h, IMAGE_SIZE[0], IMAGE_SIZE[1]], fill=hex_to_rgb("#F0EDED"))

    lose_label = "LTVが低い店"
    llw, llh = get_text_size(draw, lose_label, font_label)

    lose_lines = [
        "「メニュー一覧」と",
        "「アクセス」だけのHP。",
        "誰でも来れるが、誰も通わない。",
    ]
    lose_heights = []
    for line in lose_lines:
        _, lhh = get_text_size(draw, line, font_detail)
        lose_heights.append(lhh)

    bot_content_h = llh + 30 + sum(lose_heights) + 16 * (len(lose_lines) - 1)
    y = half_h + (half_h - bot_content_h) // 2

    draw.rectangle([MARGIN, y - 10, MARGIN + 8, y + llh + 10], fill=hex_to_rgb("#E53935"))
    draw.text((MARGIN + 24, y), lose_label, font=font_label, fill=hex_to_rgb("#E53935"))
    y += llh + 30

    for line in lose_lines:
        draw.text((MARGIN + 24, y), line, font=font_detail, fill=hex_to_rgb("#999999"))
        _, dh = get_text_size(draw, line, font_detail)
        y += dh + 16

    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")


def create_slide_7(output_path):
    """Slide 7: LPが解決する理由"""
    lines = [
        {"text": "LPは「来る理由」を", "size": "l", "center": True},
        {"text": "先に決める装置だ。", "size": "l", "center": True, "highlight": True},
        {"text": ""},
        {"text": "① 悩み別にページを分ける", "size": "s"},
        {"text": "→「自分のための店」だと感じる", "size": "s"},
        {"text": ""},
        {"text": "② 価格ではなく価値で選ばれる", "size": "s"},
        {"text": "→ 初回から単価UP、値引き交渉なし", "size": "s"},
        {"text": ""},
        {"text": "③ 納得して来るからリピートする", "size": "s"},
        {"text": "→ LTVが上がり、広告費が下がる", "size": "s"},
    ]
    create_content_slide(lines, output_path)


def create_slide_8(output_path):
    """Slide 8: Before/After"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)

    half_h = IMAGE_SIZE[1] // 2
    font_heading = get_font(64, "black")
    font_item = get_font(42, "black")

    # -- Top: BEFORE --
    draw.rectangle([0, 0, IMAGE_SIZE[0], half_h], fill=hex_to_rgb("#F5F2F0"))

    before_title = "LP導入前"
    tw, th = get_text_size(draw, before_title, font_heading)

    before_items = [
        "広告サイトで月10人の新規",
        "半分がクーポン客、リピート率20%",
        "年間広告費72万円",
        "LTV：1人あたり8,000円",
    ]
    item_heights = []
    for item in before_items:
        _, ih = get_text_size(draw, item, font_item)
        item_heights.append(ih)

    content_h = th + 25 + sum(item_heights) + 20 * (len(before_items) - 1)
    y = (half_h - content_h) // 2

    tx = (IMAGE_SIZE[0] - tw) // 2
    draw.text((tx, y), before_title, font=font_heading, fill=hex_to_rgb("#E53935"))
    draw.rectangle([tx, y + th + 5, tx + tw, y + th + 11], fill=hex_to_rgb("#E53935"))
    y += th + 25

    for item in before_items:
        iw, ih = get_text_size(draw, item, font_item)
        ix = (IMAGE_SIZE[0] - iw) // 2
        draw.text((ix, y), item, font=font_item, fill=hex_to_rgb("#888888"))
        y += ih + 20

    # -- Bottom: AFTER --
    draw.rectangle([0, half_h, IMAGE_SIZE[0], IMAGE_SIZE[1]], fill=hex_to_rgb("#2D2D2D"))

    after_title = "LP導入後"
    tw, th = get_text_size(draw, after_title, font_heading)

    after_items = [
        "LPから月5人の新規",
        "「お願いしたい」と来てリピート率70%",
        "広告費ゼロ",
        "LTV：1人あたり120,000円",
    ]
    item_heights = []
    for item in after_items:
        _, ih = get_text_size(draw, item, font_item)
        item_heights.append(ih)

    content_h = th + 25 + sum(item_heights) + 20 * (len(after_items) - 1)
    y = half_h + (half_h - content_h) // 2

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
    """Slide 9: 気づき"""
    lines = [
        {"text": "新規の数を追いかける集客は", "size": "l", "center": True},
        {"text": "走り続けないと止まる。", "size": "l", "center": True, "highlight": True},
        {"text": ""},
        {"text": "LTVの高い客を集める仕組みは", "size": "m", "center": True},
        {"text": "一度作れば積み上がる。", "size": "m", "center": True},
        {"text": ""},
        {"text": "どちらを選ぶかで", "size": "m", "center": True},
        {"text": "1年後のサロンの景色は", "size": "m", "center": True},
        {"text": "まったく違う。", "size": "l", "center": True},
    ]
    create_content_slide(lines, output_path)


def create_slide_10(output_path):
    """Slide 10: CTA"""
    img = Image.new('RGB', IMAGE_SIZE, hex_to_rgb(COLORS["background"]))
    draw = ImageDraw.Draw(img)

    lines = [
        {"text": "LTVの高い客だけが集まる", "size": 72},
        {"text": "LPの仕組み。", "size": 72},
        {"text": "あなたのサロンでも作れる。", "size": 72},
        {"text": "", "size": 0},
        {"text": "詳細はプロフィールから", "size": 56},
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
        ("slide_01_hook.png", create_slide_1),
        ("slide_02_problem.png", create_slide_2),
        ("slide_03_ltv.png", create_slide_3),
        ("slide_04_why_low_ltv.png", create_slide_4),
        ("slide_05_ai_change.png", create_slide_5),
        ("slide_06_comparison.png", create_slide_6),
        ("slide_07_lp_solution.png", create_slide_7),
        ("slide_08_before_after.png", create_slide_8),
        ("slide_09_insight.png", create_slide_9),
        ("slide_10_cta.png", create_slide_10),
    ]

    for filename, func in slides:
        path = os.path.join(OUTPUT_DIR, filename)
        func(path)

    print(f"\n全10枚の生成が完了しました: {OUTPUT_DIR}/")


if __name__ == "__main__":
    generate_all()
