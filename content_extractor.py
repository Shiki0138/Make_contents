"""
Content Extractor Module

Extracts and summarizes content from:
- YouTube URLs (via transcript)
- Blog URLs (via web scraping)
- Direct text input
"""

import re
import requests
from bs4 import BeautifulSoup

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False
    print("Warning: youtube-transcript-api not installed. YouTube extraction disabled.")

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: openai not installed. AI summarization disabled.")


class ContentExtractor:
    def __init__(self, openai_api_key=None):
        if openai_api_key and OPENAI_AVAILABLE:
            openai.api_key = openai_api_key
        self.openai_available = OPENAI_AVAILABLE and openai_api_key is not None
    
    def extract_youtube_id(self, url):
        """Extract YouTube video ID from URL."""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_youtube_transcript(self, url):
        """Get transcript from YouTube video."""
        if not YOUTUBE_AVAILABLE:
            raise ImportError("youtube-transcript-api is not installed")
        
        video_id = self.extract_youtube_id(url)
        if not video_id:
            raise ValueError(f"Could not extract video ID from URL: {url}")
        
        try:
            # Try Japanese transcript first, then auto-generated
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            try:
                transcript = transcript_list.find_transcript(['ja'])
            except:
                transcript = transcript_list.find_generated_transcript(['ja', 'en'])
            
            transcript_data = transcript.fetch()
            full_text = ' '.join([entry['text'] for entry in transcript_data])
            return full_text
        except Exception as e:
            raise Exception(f"Failed to get transcript: {e}")
    
    def get_blog_content(self, url):
        """Extract main content from blog URL."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            # Try to find main content
            main_content = None
            for selector in ['article', 'main', '.post-content', '.entry-content', '#content']:
                main_content = soup.select_one(selector)
                if main_content:
                    break
            
            if not main_content:
                main_content = soup.body
            
            if main_content:
                text = main_content.get_text(separator='\n', strip=True)
                # Clean up excessive whitespace
                text = re.sub(r'\n{3,}', '\n\n', text)
                return text
            
            return ""
        except Exception as e:
            raise Exception(f"Failed to extract blog content: {e}")
    
    def summarize_for_instagram(self, content, target_audience="美容師"):
        """
        Use AI to create 8-slide Instagram content from source material.
        
        Returns a list of 8 slide dictionaries.
        """
        if not self.openai_available:
            raise ImportError("OpenAI API is not configured")
        
        prompt = f"""
あなたはInstagramコンテンツクリエイターです。以下のコンテンツを、{target_audience}向けの8枚のカルーセル投稿に変換してください。

【ルール】
- 各スライドは50文字以内
- 1行は10-15文字程度で改行
- ターゲットが最後まで閲覧し、保存したくなる内容に
- 明朝体で読みやすいシンプルなデザイン前提

【8枚の構成】
1. タイトル（キャッチーなフック）
2. 問題提起・共感（読者の悩みに寄り添う）
3. 本論ポイント1
4. 本論ポイント2
5. 具体例・事例1
6. 具体例・事例2
7. まとめ・結論
8. CTA（保存・フォロー促し）

【出力形式】
各スライドを以下のJSON形式で出力してください：
```json
[
  {{"slide": 1, "type": "title", "text": "タイトル\\n2行目", "highlight": "強調したいフレーズ", "emphasis_lines": []}},
  ...
]
```

highlight: 黄色アンダーラインを引くフレーズ（なければnull）
emphasis_lines: 太字・大きくする行番号（0始まり、なければ空配列）

【元コンテンツ】
{content[:3000]}
"""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "あなたはInstagramマーケティングの専門家です。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            
            response_text = response.choices[0].message.content
            
            # Extract JSON from response
            json_match = re.search(r'\[[\s\S]*\]', response_text)
            if json_match:
                import json
                slides = json.loads(json_match.group())
                return slides
            else:
                raise ValueError("Could not parse AI response as JSON")
                
        except Exception as e:
            raise Exception(f"AI summarization failed: {e}")
    
    def extract_content(self, source, source_type="auto"):
        """
        Extract content from various sources.
        
        Args:
            source: URL or text content
            source_type: "youtube", "blog", "text", or "auto"
        
        Returns:
            Extracted text content
        """
        if source_type == "auto":
            if "youtube.com" in source or "youtu.be" in source:
                source_type = "youtube"
            elif source.startswith("http"):
                source_type = "blog"
            else:
                source_type = "text"
        
        if source_type == "youtube":
            return self.get_youtube_transcript(source)
        elif source_type == "blog":
            return self.get_blog_content(source)
        else:
            return source


if __name__ == "__main__":
    # Test blog extraction
    extractor = ContentExtractor()
    
    test_url = "https://example.com"
    try:
        content = extractor.get_blog_content(test_url)
        print(f"Extracted {len(content)} characters from blog")
    except Exception as e:
        print(f"Blog extraction test: {e}")
