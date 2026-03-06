#!/usr/bin/env python3
"""
Instagram Auto-Poster

Uploads carousel images to imgbb for public hosting,
then publishes them as a carousel post via Instagram Graph API.

Usage:
    python instagram_poster.py output/folder_name
    python instagram_poster.py output/folder_name --dry-run
    python instagram_poster.py output/folder_name --caption "Custom caption"
"""

import argparse
import base64
import glob
import json
import os
import sys
import time

import requests
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GRAPH_API_VERSION = "v22.0"
GRAPH_API_BASE = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

# imgbb upload endpoint
IMGBB_UPLOAD_URL = "https://api.imgbb.com/1/upload"

# Polling config for container status check
PUBLISH_POLL_INTERVAL = 3  # seconds
PUBLISH_POLL_MAX_ATTEMPTS = 20


# ---------------------------------------------------------------------------
# Image Uploader (catbox.moe primary, imgbb fallback)
# ---------------------------------------------------------------------------

CATBOX_UPLOAD_URL = "https://catbox.moe/user/api.php"
IMGBB_UPLOAD_URL = "https://api.imgbb.com/1/upload"


class ImageUploader:
    """Upload local images to a public host and return URLs.

    Primary:  catbox.moe  (no API key, reliable with Meta Graph API)
    Fallback: imgbb       (requires IMGBB_API_KEY)
    """

    def __init__(self, api_key: str | None = None):
        self.imgbb_api_key = api_key

    # -- catbox.moe (primary) -----------------------------------------------

    def _upload_catbox(self, image_path: str) -> str:
        """Upload via catbox.moe — no API key required."""
        with open(image_path, "rb") as f:
            resp = requests.post(
                CATBOX_UPLOAD_URL,
                data={"reqtype": "fileupload"},
                files={"fileToUpload": (os.path.basename(image_path), f, "image/png")},
                timeout=60,
            )
        resp.raise_for_status()
        url = resp.text.strip()
        if not url.startswith("https://"):
            raise RuntimeError(f"catbox upload failed: {url}")
        return url

    # -- imgbb (fallback) ---------------------------------------------------

    def _upload_imgbb(self, image_path: str) -> str:
        """Upload via imgbb — requires API key."""
        if not self.imgbb_api_key:
            raise RuntimeError("IMGBB_API_KEY is required for fallback upload")

        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "key": self.imgbb_api_key,
            "image": image_data,
            "name": os.path.splitext(os.path.basename(image_path))[0],
        }
        resp = requests.post(IMGBB_UPLOAD_URL, data=payload, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        if not result.get("success"):
            raise RuntimeError(f"imgbb upload failed: {result}")
        return result["data"]["url"]

    # -- public API ---------------------------------------------------------

    def upload_image(self, image_path: str) -> str:
        """Upload a single image, trying catbox first then imgbb."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        try:
            url = self._upload_catbox(image_path)
        except Exception as e:
            print(f"  ⚠️  catbox.moe failed ({e}), trying imgbb...")
            url = self._upload_imgbb(image_path)

        print(f"  ✅ Uploaded: {os.path.basename(image_path)} → {url}")
        return url

    def upload_images(self, image_paths: list[str]) -> list[str]:
        """Upload multiple images and return their public URLs (ordered)."""
        urls = []
        for i, path in enumerate(image_paths, 1):
            print(f"  📤 Uploading image {i}/{len(image_paths)}...")
            url = self.upload_image(path)
            urls.append(url)
            if i < len(image_paths):
                time.sleep(0.5)
        return urls


# ---------------------------------------------------------------------------
# Instagram Poster (Graph API)
# ---------------------------------------------------------------------------


class InstagramPoster:
    """Publish carousel posts to Instagram via Graph API."""

    def __init__(self, user_id: str, access_token: str):
        if not user_id or not access_token:
            raise ValueError(
                "INSTAGRAM_USER_ID and INSTAGRAM_ACCESS_TOKEN are required"
            )
        self.user_id = user_id
        self.access_token = access_token

    MAX_RETRIES = 3
    RETRY_BASE_DELAY = 5  # seconds

    def _post(self, endpoint: str, params: dict) -> dict:
        """Make a POST request to Graph API with retry on server errors."""
        params["access_token"] = self.access_token
        url = f"{GRAPH_API_BASE}/{endpoint}"

        last_error = None
        for attempt in range(1, self.MAX_RETRIES + 1):
            resp = requests.post(url, data=params, timeout=60)

            if resp.status_code == 200:
                return resp.json()

            error_detail = resp.json().get("error", {}).get("message", resp.text)
            last_error = f"Graph API error ({resp.status_code}): {error_detail}"

            # Retry only on 500-series (server) errors
            if resp.status_code >= 500 and attempt < self.MAX_RETRIES:
                delay = self.RETRY_BASE_DELAY * (2 ** (attempt - 1))
                print(
                    f"  ⚠️  Server error (attempt {attempt}/{self.MAX_RETRIES}), "
                    f"retrying in {delay}s..."
                )
                time.sleep(delay)
                continue

            # Client errors (4xx) or final attempt — fail immediately
            raise RuntimeError(last_error)

        raise RuntimeError(last_error)

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        """Make a GET request to Graph API."""
        params = params or {}
        params["access_token"] = self.access_token
        url = f"{GRAPH_API_BASE}/{endpoint}"
        resp = requests.get(url, params=params, timeout=30)
        return resp.json()

    def create_media_container(self, image_url: str) -> str:
        """Create a single image container (as carousel item)."""
        result = self._post(
            f"{self.user_id}/media",
            {
                "image_url": image_url,
                "is_carousel_item": "true",
            },
        )
        container_id = result["id"]
        print(f"  📦 Container created: {container_id}")
        return container_id

    def create_carousel_container(
        self, children_ids: list[str], caption: str
    ) -> str:
        """Create a carousel container referencing child containers."""
        result = self._post(
            f"{self.user_id}/media",
            {
                "media_type": "CAROUSEL",
                "children": ",".join(children_ids),
                "caption": caption,
            },
        )
        carousel_id = result["id"]
        print(f"  🎠 Carousel container created: {carousel_id}")
        return carousel_id

    def wait_for_container(self, container_id: str) -> bool:
        """Poll until the container is ready for publishing."""
        for attempt in range(PUBLISH_POLL_MAX_ATTEMPTS):
            status_resp = self._get(
                container_id, {"fields": "status_code,status"}
            )
            status_code = status_resp.get("status_code")

            if status_code == "FINISHED":
                return True
            elif status_code == "ERROR":
                error = status_resp.get("status", "Unknown error")
                raise RuntimeError(f"Container processing failed: {error}")

            print(
                f"  ⏳ Container status: {status_code} "
                f"(attempt {attempt + 1}/{PUBLISH_POLL_MAX_ATTEMPTS})"
            )
            time.sleep(PUBLISH_POLL_INTERVAL)

        raise TimeoutError("Container did not become ready in time")

    def publish(self, container_id: str) -> str:
        """Publish a prepared container."""
        result = self._post(
            f"{self.user_id}/media_publish",
            {"creation_id": container_id},
        )
        media_id = result["id"]
        print(f"  🚀 Published! Media ID: {media_id}")
        return media_id

    def post_carousel(
        self, image_urls: list[str], caption: str, dry_run: bool = False
    ) -> str | None:
        """Full workflow: create item containers → carousel → publish."""

        if len(image_urls) < 2:
            raise ValueError("Carousel requires at least 2 images")
        if len(image_urls) > 10:
            raise ValueError("Carousel supports at most 10 images")

        print(f"\n📦 Creating {len(image_urls)} media containers...")
        children_ids = []
        for i, url in enumerate(image_urls, 1):
            print(f"  [{i}/{len(image_urls)}]", end=" ")
            cid = self.create_media_container(url)
            children_ids.append(cid)
            time.sleep(1)  # Rate limit safety

        print("\n🎠 Creating carousel container...")
        carousel_id = self.create_carousel_container(children_ids, caption)

        if dry_run:
            print("\n🏁 Dry-run complete. Carousel NOT published.")
            print(f"   Carousel container ID: {carousel_id}")
            return None

        print("\n⏳ Waiting for container to be ready...")
        self.wait_for_container(carousel_id)

        print("\n🚀 Publishing...")
        media_id = self.publish(carousel_id)
        return media_id


# ---------------------------------------------------------------------------
# Main: post from output directory
# ---------------------------------------------------------------------------


def post_from_output(
    output_dir: str,
    caption_override: str | None = None,
    dry_run: bool = False,
) -> str | None:
    """
    Read slides + caption from an output directory and post to Instagram.

    Args:
        output_dir: Path to the output folder (e.g. output/e2_yes_set)
        caption_override: Optional caption text (overrides caption.txt)
        dry_run: If True, create containers but do not publish.

    Returns:
        Media ID of the published post, or None if dry-run.
    """

    # ── Validate output directory ──────────────────────────────
    if not os.path.isdir(output_dir):
        print(f"❌ Directory not found: {output_dir}")
        sys.exit(1)

    # ── Discover slide images ──────────────────────────────────
    image_paths = sorted(glob.glob(os.path.join(output_dir, "slide_*.png")))
    if not image_paths:
        print(f"❌ No slide_*.png images found in {output_dir}")
        sys.exit(1)

    print(f"📁 Found {len(image_paths)} images in {output_dir}")

    # ── Read caption ───────────────────────────────────────────
    if caption_override:
        caption = caption_override
    else:
        caption_path = os.path.join(output_dir, "caption.txt")
        if os.path.exists(caption_path):
            with open(caption_path, "r", encoding="utf-8") as f:
                caption = f.read().strip()
            print(f"📝 Caption loaded from {caption_path}")
        else:
            caption = ""
            print("⚠️  No caption.txt found — posting without caption")

    # ── Load credentials ───────────────────────────────────────
    imgbb_key = os.environ.get("IMGBB_API_KEY")  # optional fallback
    ig_user_id = os.environ.get("INSTAGRAM_USER_ID")
    ig_token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")

    missing = []
    if not ig_user_id:
        missing.append("INSTAGRAM_USER_ID")
    if not ig_token:
        missing.append("INSTAGRAM_ACCESS_TOKEN")

    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        print("   Set them in .env or export them.")
        sys.exit(1)

    # ── Upload images ──────────────────────────────────────────
    print("\n📤 Uploading images...")
    uploader = ImageUploader(api_key=imgbb_key)
    image_urls = uploader.upload_images(image_paths)

    # ── Post to Instagram ──────────────────────────────────────
    poster = InstagramPoster(user_id=ig_user_id, access_token=ig_token)
    media_id = poster.post_carousel(image_urls, caption, dry_run=dry_run)

    # ── Summary ────────────────────────────────────────────────
    print("\n" + "=" * 50)
    if dry_run:
        print("✅ Dry-run complete!")
    else:
        print("✅ Successfully posted to Instagram!")
        print(f"   Media ID: {media_id}")
        print(f"   https://www.instagram.com/p/{media_id}/")
    print("=" * 50)

    return media_id


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Post generated carousel images to Instagram",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python instagram_poster.py output/e2_yes_set
  python instagram_poster.py output/e2_yes_set --dry-run
  python instagram_poster.py output/e2_yes_set --caption "Custom caption here"
        """,
    )

    parser.add_argument(
        "output_dir",
        help="Path to the output folder containing slide_*.png and caption.txt",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Create containers but do not publish (test mode)",
    )
    parser.add_argument(
        "--caption",
        "-c",
        help="Override caption text (instead of reading caption.txt)",
    )

    args = parser.parse_args()

    print("=" * 50)
    print("📱 Instagram Auto-Poster")
    print("=" * 50)

    post_from_output(
        output_dir=args.output_dir,
        caption_override=args.caption,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
