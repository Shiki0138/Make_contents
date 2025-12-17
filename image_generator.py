"""
Instagram Image Generator Module

Generates 8 Instagram carousel images with consistent styling.
Uses IPAex Mincho font with yellow underline highlights.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import re
from config import BRAND_COLORS, IMAGE_SIZE, MARGIN_PERCENT, FONT_SIZES

class ImageGenerator:
    def __init__(self, font_path="fonts/ipaexm.ttf"):
        self.font_path = font_path
        self.image_size = IMAGE_SIZE
        self.margin = int(IMAGE_SIZE[0] * MARGIN_PERCENT)
        self.content_width = IMAGE_SIZE[0] - (2 * self.margin)
        
        # Load fonts
        self.fonts = {}
        for name, size in FONT_SIZES.items():
            try:
                self.fonts[name] = ImageFont.truetype(font_path, size)
            except Exception as e:
                print(f"Warning: Could not load font {font_path}: {e}")
                self.fonts[name] = ImageFont.load_default()
    
    def create_image(self, text_content, slide_type="body", highlights=None, emphasis_lines=None):
        """
        Create a single Instagram image.
        
        Args:
            text_content: Text to display (can include \n for line breaks)
            slide_type: "title", "body", "cta" - affects font size
            highlights: List of text phrases to highlight with yellow underline
            emphasis_lines: List of line indices (0-based) to make larger/bolder
        """
        # Create white background
        img = Image.new('RGB', self.image_size, BRAND_COLORS["background"])
        draw = ImageDraw.Draw(img)
        
        # Select font based on slide type
        if slide_type == "title":
            font = self.fonts["title"]
        elif slide_type == "cta":
            font = self.fonts["heading"]
        else:
            font = self.fonts["body"]
        
        emphasis_font = self.fonts["emphasis"]
        highlights = highlights or []
        emphasis_lines = emphasis_lines or []
        
        # Split text into lines
        lines = text_content.strip().split('\n')
        
        # Calculate line heights and total text height
        line_data = []
        total_height = 0
        line_spacing = 20
        
        for i, line in enumerate(lines):
            if i in emphasis_lines:
                current_font = emphasis_font
            elif slide_type == "title":
                current_font = self.fonts["title"]
            else:
                current_font = font
            
            # Get text bounding box
            bbox = draw.textbbox((0, 0), line, font=current_font)
            line_height = bbox[3] - bbox[1]
            line_width = bbox[2] - bbox[0]
            
            line_data.append({
                "text": line,
                "font": current_font,
                "height": line_height,
                "width": line_width,
                "is_emphasis": i in emphasis_lines
            })
            
            total_height += line_height + line_spacing
        
        total_height -= line_spacing  # Remove last spacing
        
        # Calculate starting Y position (vertically centered)
        start_y = (self.image_size[1] - total_height) // 2
        
        # Draw each line
        current_y = start_y
        for i, line_info in enumerate(line_data):
            text = line_info["text"]
            current_font = line_info["font"]
            line_width = line_info["width"]
            line_height = line_info["height"]
            
            # Center horizontally
            x = (self.image_size[0] - line_width) // 2
            
            # Determine text color
            text_color = BRAND_COLORS["primary"] if line_info["is_emphasis"] else BRAND_COLORS["text"]
            
            # Draw the text
            draw.text((x, current_y), text, font=current_font, fill=text_color)
            
            # Check if this line should have yellow underline
            for highlight in highlights:
                if highlight in text:
                    # Find highlight position
                    highlight_start = text.find(highlight)
                    
                    # Calculate highlight x position
                    prefix = text[:highlight_start]
                    prefix_bbox = draw.textbbox((0, 0), prefix, font=current_font)
                    prefix_width = prefix_bbox[2] - prefix_bbox[0]
                    
                    highlight_bbox = draw.textbbox((0, 0), highlight, font=current_font)
                    highlight_width = highlight_bbox[2] - highlight_bbox[0]
                    
                    # Draw yellow underline
                    underline_y = current_y + line_height + 5
                    underline_start_x = x + prefix_width
                    underline_end_x = underline_start_x + highlight_width
                    
                    # Draw thick underline
                    for offset in range(8):
                        draw.line(
                            [(underline_start_x, underline_y + offset), 
                             (underline_end_x, underline_y + offset)],
                            fill=BRAND_COLORS["highlight"],
                            width=1
                        )
            
            current_y += line_height + line_spacing
        
        return img
    
    def generate_carousel(self, slides, output_dir="output"):
        """
        Generate all 8 carousel images.
        
        Args:
            slides: List of dicts with keys:
                - text: Content text
                - type: "title", "body", "cta"
                - highlights: Optional list of phrases to highlight
                - emphasis_lines: Optional list of line indices to emphasize
            output_dir: Directory to save images
        
        Returns:
            List of saved file paths
        """
        os.makedirs(output_dir, exist_ok=True)
        saved_paths = []
        
        for i, slide in enumerate(slides):
            img = self.create_image(
                text_content=slide.get("text", ""),
                slide_type=slide.get("type", "body"),
                highlights=slide.get("highlights", []),
                emphasis_lines=slide.get("emphasis_lines", [])
            )
            
            filename = f"slide_{i+1:02d}.png"
            filepath = os.path.join(output_dir, filename)
            img.save(filepath, "PNG", quality=95)
            saved_paths.append(filepath)
            print(f"Saved: {filepath}")
        
        return saved_paths


def test_generator():
    """Test the image generator with sample content."""
    generator = ImageGenerator()
    
    test_slides = [
        {
            "text": "美容師が知るべき\n生成AI活用術",
            "type": "title",
            "highlights": [],
            "emphasis_lines": []
        },
        {
            "text": "「AIに仕事を奪われる」\n\nそう思っていませんか？",
            "type": "body",
            "highlights": ["AIに仕事を奪われる"],
            "emphasis_lines": []
        },
        {
            "text": "美容師の技術や接客は\nAIには置き換えられない\n\nでも、集客や発信は\nAIで効率化できる",
            "type": "body",
            "highlights": [],
            "emphasis_lines": [0, 1]
        },
    ]
    
    generator.generate_carousel(test_slides, "test_output")


if __name__ == "__main__":
    test_generator()
