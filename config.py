# Instagram Content Generator Configuration

BRAND_COLORS = {
    "primary": "#1a237e",      # 濃紺
    "highlight": "#FFD700",    # 黄色アンダーライン
    "text": "#000000",         # 黒
    "background": "#FFFFFF",   # 白
    "emphasis": "#1a237e",     # 強調文字色（濃紺）
}

# Image Settings
IMAGE_SIZE = (1080, 1080)
MARGIN_PERCENT = 0.15  # 15% margin

# Font Settings
FONT_PATH = "fonts/ipaexm.ttf"
FONT_SIZES = {
    "title": 96,      # タイトル用（72→96）
    "heading": 72,    # 見出し用（56→72）
    "body": 64,       # 本文用（48→64）
    "emphasis": 80,   # 強調文字用（64→80）
    "small": 52,      # 小さめ文字（40→52）
}

# Target Audience
TARGET_AUDIENCE = "美容師"

# Default Hashtags
HASHTAGS = [
    "#美容師",
    "#AI活用",
    "#生成AI",
    "#インスタ集客",
    "#美容室経営",
    "#サロン集客",
    "#ChatGPT",
    "#美容師さんと繋がりたい",
]

# Story Structure (8 slides)
STORY_STRUCTURE = [
    {"role": "title", "description": "タイトル・キャッチコピー"},
    {"role": "problem", "description": "問題提起・共感"},
    {"role": "point1", "description": "本論・ポイント1"},
    {"role": "point2", "description": "本論・ポイント2"},
    {"role": "example1", "description": "具体例・事例1"},
    {"role": "example2", "description": "具体例・事例2"},
    {"role": "summary", "description": "まとめ・結論"},
    {"role": "cta", "description": "CTA・保存促し"},
]

# Instagram Account
INSTAGRAM_ACCOUNT = "shiki_fp_138"
