# Instagram Content Generator

## Setup

Install dependencies:
```bash
pip install pillow youtube-transcript-api beautifulsoup4 requests openai
```

Set OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key'
```

## Usage

### YouTube URL から生成
```bash
cd /Users/leadfive/insta/insta_generator
python insta_generator.py --youtube "https://youtube.com/watch?v=xxx"
```

### ブログ URL から生成
```bash
python insta_generator.py --blog "https://example.com/article"
```

### テキスト直接入力
```bash
python insta_generator.py --text "美容師がAIを活用すべき理由..."
```

### インタラクティブモード（手動入力）
```bash
python insta_generator.py --interactive
```

## Output

- `output/[timestamp]/slide_01.png` ~ `slide_08.png`: 8枚のカルーセル画像
- `output/[timestamp]/caption.txt`: キャプション（ハッシュタグ付き）
- `output/[timestamp]/slides.json`: 元データ

## Files

- `config.py`: 設定（ブランドカラー、フォント、ハッシュタグ）
- `image_generator.py`: 画像生成エンジン
- `content_extractor.py`: コンテンツ抽出（YouTube/Blog）
- `caption_generator.py`: キャプション生成
- `insta_generator.py`: メインCLI
