"""
Caption Generator Module

Generates Instagram captions with hashtags.
"""

from config import HASHTAGS, TARGET_AUDIENCE

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class CaptionGenerator:
    def __init__(self, openai_api_key=None):
        if openai_api_key and OPENAI_AVAILABLE:
            openai.api_key = openai_api_key
        self.openai_available = OPENAI_AVAILABLE and openai_api_key is not None
    
    def generate_caption(self, slides, custom_hashtags=None):
        """
        Generate Instagram caption from slide content.
        
        Args:
            slides: List of slide dictionaries with 'text' key
            custom_hashtags: Optional list of additional hashtags
        
        Returns:
            Formatted caption string
        """
        # Extract title and key points from slides
        title = slides[0].get("text", "").replace("\n", " ") if slides else ""
        
        # Build summary from slides
        key_points = []
        for slide in slides[1:-1]:  # Exclude title and CTA
            text = slide.get("text", "").replace("\n", " ")
            if text:
                key_points.append(text)
        
        # If OpenAI is available, generate a polished caption
        if self.openai_available:
            return self._generate_ai_caption(title, key_points, custom_hashtags)
        else:
            return self._generate_basic_caption(title, key_points, custom_hashtags)
    
    def _generate_ai_caption(self, title, key_points, custom_hashtags=None):
        """Generate caption using AI."""
        prompt = f"""
以下の情報からInstagramのキャプションを作成してください。

【タイトル】
{title}

【要点】
{chr(10).join(key_points[:4])}

【ルール】
- 最初の1行で興味を引く
- 本文は3-4行で簡潔に
- 最後に保存・フォローを促す
- ハッシュタグは10個程度
- 改行で読みやすく
- {TARGET_AUDIENCE}向けのトーン

【出力形式】
キャプション本文のみ。ハッシュタグは含めないでください。
"""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"あなたは{TARGET_AUDIENCE}向けInstagramマーケターです。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            
            caption = response.choices[0].message.content.strip()
            
            # Add hashtags
            all_hashtags = HASHTAGS.copy()
            if custom_hashtags:
                all_hashtags.extend(custom_hashtags)
            
            hashtag_str = " ".join(all_hashtags[:12])
            
            return f"{caption}\n\n.\n.\n.\n\n{hashtag_str}"
            
        except Exception as e:
            print(f"AI caption generation failed: {e}")
            return self._generate_basic_caption(title, key_points, custom_hashtags)
    
    def _generate_basic_caption(self, title, key_points, custom_hashtags=None):
        """Generate basic caption without AI."""
        caption_parts = [
            f"【{title}】",
            "",
        ]
        
        # Add up to 3 key points
        for point in key_points[:3]:
            caption_parts.append(f"✅ {point}")
        
        caption_parts.extend([
            "",
            "---",
            "",
            "💡 この投稿が参考になったら",
            "保存📌してね！",
            "",
            "フォローもお願いします🙏",
            "",
            ".",
            ".",
            ".",
            "",
        ])
        
        # Add hashtags
        all_hashtags = HASHTAGS.copy()
        if custom_hashtags:
            all_hashtags.extend(custom_hashtags)
        
        caption_parts.append(" ".join(all_hashtags[:12]))
        
        return "\n".join(caption_parts)


if __name__ == "__main__":
    # Test caption generation
    generator = CaptionGenerator()
    
    test_slides = [
        {"text": "美容師が知るべき\n生成AI活用術"},
        {"text": "AIに仕事を奪われる\nそう思っていませんか？"},
        {"text": "美容師の技術は\nAIには置き換えられない"},
        {"text": "保存してね！"},
    ]
    
    caption = generator.generate_caption(test_slides)
    print("Generated caption:")
    print(caption)
