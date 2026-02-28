#!/usr/bin/env python3
"""
Facebook Page Auto-Poster

Posts carousel images to a Facebook Page via Graph API.
Uses the same output folders as instagram_poster.py.

Usage:
    python facebook_poster.py output/folder_name
    python facebook_poster.py output/folder_name --dry-run
"""

import argparse
import glob
import os
import sys
import time

import requests
from dotenv import load_dotenv

load_dotenv()

GRAPH_API_VERSION = "v22.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"


class FacebookPoster:
    """Post images to a Facebook Page via Graph API."""

    def __init__(self, page_id: str, user_access_token: str):
        if not page_id or not user_access_token:
            raise ValueError("FACEBOOK_PAGE_ID and INSTAGRAM_ACCESS_TOKEN required")
        self.page_id = page_id
        self.user_token = user_access_token
        self.page_token = self._get_page_token()

    def _get_page_token(self) -> str:
        """Get Page Access Token from User Access Token."""
        resp = requests.get(
            f"{GRAPH_API_BASE}/{self.page_id}",
            params={
                "fields": "access_token",
                "access_token": self.user_token,
            },
            timeout=15,
        )
        data = resp.json()
        if "access_token" not in data:
            error = data.get("error", {}).get("message", "Unknown error")
            raise RuntimeError(f"Failed to get page token: {error}")
        return data["access_token"]

    def upload_photo(self, image_path: str) -> str:
        """Upload a photo to the page (unpublished)."""
        with open(image_path, "rb") as f:
            resp = requests.post(
                f"{GRAPH_API_BASE}/{self.page_id}/photos",
                data={
                    "published": "false",
                    "access_token": self.page_token,
                },
                files={"source": f},
                timeout=60,
            )

        result = resp.json()
        if "id" not in result:
            error = result.get("error", {}).get("message", "Unknown error")
            raise RuntimeError(f"Photo upload failed: {error}")

        photo_id = result["id"]
        print(f"  📷 Uploaded: {os.path.basename(image_path)} → {photo_id}")
        return photo_id

    def create_post(
        self, photo_ids: list[str], message: str, dry_run: bool = False
    ) -> str | None:
        """Create a post with multiple photos."""
        attached_media = [{"media_fbid": pid} for pid in photo_ids]

        if dry_run:
            print(f"\n🏁 Dry-run: would post {len(photo_ids)} photos")
            print(f"   Message: {message[:100]}...")
            return None

        import json

        resp = requests.post(
            f"{GRAPH_API_BASE}/{self.page_id}/feed",
            data={
                "message": message,
                "attached_media": json.dumps(attached_media),
                "access_token": self.page_token,
            },
            timeout=30,
        )

        result = resp.json()
        if "id" not in result:
            error = result.get("error", {}).get("message", "Unknown error")
            raise RuntimeError(f"Post creation failed: {error}")

        post_id = result["id"]
        print(f"  🚀 Published! Post ID: {post_id}")
        return post_id

    def post_carousel(
        self, image_paths: list[str], caption: str, dry_run: bool = False
    ) -> str | None:
        """Full workflow: upload photos → create post."""
        print(f"\n📤 Uploading {len(image_paths)} photos to Facebook...")
        photo_ids = []
        for i, path in enumerate(image_paths, 1):
            print(f"  [{i}/{len(image_paths)}]", end=" ")
            pid = self.upload_photo(path)
            photo_ids.append(pid)
            time.sleep(0.5)

        print("\n📝 Creating post...")
        post_id = self.create_post(photo_ids, caption, dry_run=dry_run)

        return post_id


def post_from_output(
    output_dir: str,
    caption_override: str | None = None,
    dry_run: bool = False,
) -> str | None:
    """Post output folder contents to Facebook Page."""
    if not os.path.isdir(output_dir):
        print(f"❌ Directory not found: {output_dir}")
        sys.exit(1)

    image_paths = sorted(glob.glob(os.path.join(output_dir, "slide_*.png")))
    if not image_paths:
        print(f"❌ No slide_*.png found in {output_dir}")
        sys.exit(1)

    print(f"📁 Found {len(image_paths)} images in {output_dir}")

    # Read caption
    if caption_override:
        caption = caption_override
    else:
        caption_path = os.path.join(output_dir, "caption.txt")
        if os.path.exists(caption_path):
            with open(caption_path, "r", encoding="utf-8") as f:
                caption = f.read().strip()
        else:
            caption = ""

    # Credentials
    page_id = os.environ.get("FACEBOOK_PAGE_ID")
    user_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")

    if not page_id:
        print("❌ Missing FACEBOOK_PAGE_ID in .env")
        sys.exit(1)
    if not user_token:
        print("❌ Missing INSTAGRAM_ACCESS_TOKEN in .env")
        sys.exit(1)

    poster = FacebookPoster(page_id=page_id, user_access_token=user_token)
    post_id = poster.post_carousel(image_paths, caption, dry_run=dry_run)

    print("\n" + "=" * 50)
    if dry_run:
        print("✅ Dry-run complete!")
    else:
        print("✅ Posted to Facebook Page!")
        print(f"   Post ID: {post_id}")
    print("=" * 50)

    return post_id


def main():
    parser = argparse.ArgumentParser(description="Post to Facebook Page")
    parser.add_argument("output_dir", help="Path to output folder")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--caption", "-c", help="Override caption")
    args = parser.parse_args()

    print("=" * 50)
    print("📘 Facebook Page Auto-Poster")
    print("=" * 50)

    post_from_output(args.output_dir, args.caption, args.dry_run)


if __name__ == "__main__":
    main()
