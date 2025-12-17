#!/usr/bin/env python3
"""
Instagram Content Generator CLI

Main entry point for generating Instagram carousel posts.

Usage:
    python insta_generator.py --youtube "https://youtube.com/..."
    python insta_generator.py --blog "https://example.com/..."
    python insta_generator.py --text "コンテンツのテキスト..."
    python insta_generator.py --interactive
"""

import argparse
import os
import sys
import json
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import HASHTAGS, TARGET_AUDIENCE
from image_generator import ImageGenerator
from content_extractor import ContentExtractor
from caption_generator import CaptionGenerator


def get_openai_key():
    """Get OpenAI API key from environment."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("⚠️  OPENAI_API_KEY not set. AI features will be limited.")
        print("   Set it with: export OPENAI_API_KEY='your-key'")
    return key


def create_manual_slides():
    """Interactive mode for creating slides manually."""
    print("\n📝 マニュアル入力モード")
    print("=" * 40)
    print("8枚のスライドを順番に入力してください。")
    print("複数行入力するには、空行でEnterを押してください。")
    print("=" * 40)
    
    slide_roles = [
        "タイトル（キャッチコピー）",
        "問題提起・共感",
        "本論・ポイント1",
        "本論・ポイント2",
        "具体例・事例1",
        "具体例・事例2",
        "まとめ・結論",
        "CTA（保存促し）",
    ]
    
    slides = []
    
    for i, role in enumerate(slide_roles):
        print(f"\n📌 スライド {i+1}: {role}")
        print("テキストを入力（終了は空行Enter）:")
        
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        
        text = "\n".join(lines)
        
        # Ask for highlight
        highlight = input("黄色アンダーラインを引くフレーズ（なければEnter）: ").strip()
        
        slide_type = "title" if i == 0 else ("cta" if i == 7 else "body")
        
        slide = {
            "text": text,
            "type": slide_type,
            "highlights": [highlight] if highlight else [],
            "emphasis_lines": []
        }
        
        slides.append(slide)
        print(f"✅ スライド {i+1} 保存完了")
    
    return slides


def process_ai_slides(raw_slides):
    """Convert AI-generated slide format to image generator format."""
    processed = []
    
    for slide in raw_slides:
        slide_num = slide.get("slide", 0)
        
        if slide_num == 1:
            slide_type = "title"
        elif slide_num == 8:
            slide_type = "cta"
        else:
            slide_type = "body"
        
        highlight = slide.get("highlight")
        highlights = [highlight] if highlight else []
        
        processed.append({
            "text": slide.get("text", ""),
            "type": slide_type,
            "highlights": highlights,
            "emphasis_lines": slide.get("emphasis_lines", [])
        })
    
    return processed


def main():
    parser = argparse.ArgumentParser(
        description="Instagram Content Generator - 8枚カルーセル画像＋キャプション生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python insta_generator.py --youtube "https://youtube.com/watch?v=xxx"
  python insta_generator.py --blog "https://example.com/article"
  python insta_generator.py --text "美容師がAIを活用すべき理由..."
  python insta_generator.py --interactive
        """
    )
    
    parser.add_argument("--youtube", "-y", help="YouTube URL to extract content from")
    parser.add_argument("--blog", "-b", help="Blog URL to extract content from")
    parser.add_argument("--text", "-t", help="Direct text input")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode for manual input")
    parser.add_argument("--output", "-o", default="output", help="Output directory (default: output)")
    parser.add_argument("--name", "-n", help="Content name for output folder")
    
    args = parser.parse_args()
    
    # Check if any input provided
    if not any([args.youtube, args.blog, args.text, args.interactive]):
        parser.print_help()
        print("\n❌ Error: Please provide one of --youtube, --blog, --text, or --interactive")
        sys.exit(1)
    
    print("=" * 50)
    print("🎨 Instagram Content Generator")
    print("=" * 50)
    
    # Get OpenAI key
    openai_key = get_openai_key()
    
    # Initialize components
    extractor = ContentExtractor(openai_api_key=openai_key)
    generator = ImageGenerator()
    caption_gen = CaptionGenerator(openai_api_key=openai_key)
    
    slides = None
    
    # Process input
    if args.interactive:
        slides = create_manual_slides()
    else:
        # Extract content
        print("\n📥 コンテンツを抽出中...")
        
        try:
            if args.youtube:
                print(f"   YouTube: {args.youtube}")
                content = extractor.extract_content(args.youtube, "youtube")
            elif args.blog:
                print(f"   Blog: {args.blog}")
                content = extractor.extract_content(args.blog, "blog")
            else:
                content = args.text
            
            print(f"   抽出完了: {len(content)} 文字")
            
            # Generate slides with AI
            if openai_key:
                print("\n🤖 AIでスライド構成を生成中...")
                raw_slides = extractor.summarize_for_instagram(content, TARGET_AUDIENCE)
                slides = process_ai_slides(raw_slides)
                print(f"   {len(slides)} 枚のスライド構成完了")
            else:
                print("\n⚠️  OpenAI APIキーがないため、インタラクティブモードに切り替えます")
                slides = create_manual_slides()
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = args.name or timestamp
    output_dir = os.path.join(args.output, folder_name)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n📁 出力先: {output_dir}")
    
    # Generate images
    print("\n🎨 画像を生成中...")
    image_paths = generator.generate_carousel(slides, output_dir)
    print(f"   {len(image_paths)} 枚の画像生成完了")
    
    # Generate caption
    print("\n✍️  キャプションを生成中...")
    caption = caption_gen.generate_caption(slides)
    
    # Save caption
    caption_path = os.path.join(output_dir, "caption.txt")
    with open(caption_path, "w", encoding="utf-8") as f:
        f.write(caption)
    print(f"   キャプション保存: {caption_path}")
    
    # Save slides data
    slides_path = os.path.join(output_dir, "slides.json")
    with open(slides_path, "w", encoding="utf-8") as f:
        json.dump(slides, f, ensure_ascii=False, indent=2)
    print(f"   スライドデータ保存: {slides_path}")
    
    # Summary
    print("\n" + "=" * 50)
    print("✅ 生成完了!")
    print("=" * 50)
    print(f"\n📁 出力フォルダ: {output_dir}")
    print(f"🖼️  画像: {len(image_paths)} 枚")
    print(f"📝 キャプション: caption.txt")
    print(f"\n🚀 次のステップ:")
    print("   1. 画像を確認してAirDropでスマホに送信")
    print("   2. Instagramでカルーセル投稿")
    print("   3. caption.txt の内容をキャプションに貼り付け")
    
    # Open output folder
    if sys.platform == "darwin":
        os.system(f'open "{output_dir}"')


if __name__ == "__main__":
    main()
