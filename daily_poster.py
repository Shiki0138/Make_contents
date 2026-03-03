#!/usr/bin/env python3
"""
Daily Instagram Auto-Poster

Runs daily to post the next unposted content from output/.
When stock runs out, generates new content using carousel_generator.

Usage:
    python daily_poster.py              # Post next content
    python daily_poster.py --dry-run    # Test without posting
    python daily_poster.py --status     # Show posting status
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOG_FILE = os.path.join(BASE_DIR, "posted_log.json")
POSTER_SCRIPT = os.path.join(BASE_DIR, "instagram_poster.py")
FB_POSTER_SCRIPT = os.path.join(BASE_DIR, "facebook_poster.py")
GENERATOR_SCRIPT = os.path.join(BASE_DIR, "carousel_generator.py")
PYTHON = os.path.join(BASE_DIR, "venv", "bin", "python3")
LOG_DIR = os.path.join(BASE_DIR, "logs")

JST = timezone(timedelta(hours=9))

# Posting order — series-based, naturally grouped
POSTING_ORDER = [
    # E series: カウンセリングの科学
    "e3_question_order",
    "e4_visual_anchor",
    "e5_silence",
    # F series: 口コミが生まれる瞬間
    "f1_word_of_mouth",
    "f2_photo_moment",
    "f3_referral",
    "f4_google_review",
    # G series: 新規→リピーター初期設計
    "g1_first_impression",
    "g2_name_recall",
    "g3_coupon_trap",
    "g4_follow_up_dm",
    "g5_homework",
    # H series: スタッフ教育の行動科学
    "h1_training_science",
    "h2_feedback_timing",
    # Standalone
    "hp_cost",
]

# Generator functions for auto-generation when stock runs out
# Maps output folder name → carousel_generator function name
GENERATOR_MAP = {
    # A series
    "a1_decision_fatigue": "generate_a1",
    "a2_status_quo_bias": "generate_a2",
    "a3_anchoring": "generate_a3",
    "a4_peak_end": "generate_a4",
    "a5_social_proof": "generate_a5",
    # B series
    "b1_self_efficacy": "generate_b1",
    "b2_specificity": "generate_b2",
    "b3_conclusion_first": "generate_b3",
    "b4_checklist": "generate_b4",
    "b5_reproducibility": "generate_b5",
    # C series
    "c1_memory_design": "generate_c1",
    "c2_booking_timing": "generate_c2",
    "c3_customer_notes": "generate_c3",
    "c4_visit_interval": "generate_c4",
    # D series
    "d1_contrast_effect": "generate_d1",
    "d2_pine_bamboo_plum": "generate_d2",
    "d3_bundling": "generate_d3",
    "d4_cross_sell": "generate_d4",
    # Day series (older content)
    "day1": "generate_day1",
    "day2": "generate_day2",
    "day3": "generate_day3",
    "day4": "generate_day4",
    "day5": "generate_day5",
    "day6": "generate_day6",
    "day7": "generate_day7",
    "day8": "generate_day8",
    "day9": "generate_day9",
    "day10": "generate_day10",
    "day11": "generate_day11",
    "day12": "generate_day12",
    "day13": "generate_day13",
    "day14": "generate_day14",
    "day15": "generate_day15",
}

# Order for auto-generation (when stock runs out)
GENERATION_ORDER = [
    "a1_decision_fatigue",
    "a2_status_quo_bias",
    "a3_anchoring",
    "a4_peak_end",
    "a5_social_proof",
    "b1_self_efficacy",
    "b2_specificity",
    "b3_conclusion_first",
    "b4_checklist",
    "b5_reproducibility",
    "c1_memory_design",
    "c2_booking_timing",
    "c3_customer_notes",
    "c4_visit_interval",
    "d1_contrast_effect",
    "d2_pine_bamboo_plum",
    "d3_bundling",
    "d4_cross_sell",
]


# ---------------------------------------------------------------------------
# Log management
# ---------------------------------------------------------------------------


def load_log() -> dict:
    """Load posting log."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"posted": [], "generated": []}


def save_log(log: dict):
    """Save posting log."""
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def get_posted_folders(log: dict) -> set:
    """Get set of already-posted folder names."""
    return {entry["folder"] for entry in log["posted"]}


def add_post_record(log: dict, folder: str, media_id: str | None = None):
    """Add a post record to the log."""
    log["posted"].append({
        "folder": folder,
        "posted_at": datetime.now(JST).isoformat(),
        "media_id": media_id or "dry-run",
    })
    save_log(log)


# ---------------------------------------------------------------------------
# Stock management
# ---------------------------------------------------------------------------


def get_available_stock() -> list[str]:
    """Get list of output folders that have slide images."""
    if not os.path.isdir(OUTPUT_DIR):
        return []

    folders = []
    for name in sorted(os.listdir(OUTPUT_DIR)):
        folder_path = os.path.join(OUTPUT_DIR, name)
        if not os.path.isdir(folder_path):
            continue
        # Check if folder has slide images
        slides = [f for f in os.listdir(folder_path) if f.startswith("slide_") and f.endswith(".png")]
        if len(slides) >= 2:
            folders.append(name)
    return folders


def get_next_to_post(log: dict) -> str | None:
    """Get the next folder to post, following POSTING_ORDER first."""
    posted = get_posted_folders(log)
    available = set(get_available_stock())

    # First: follow the defined posting order
    for folder in POSTING_ORDER:
        if folder not in posted and folder in available:
            return folder

    # Then: any other available folder not yet posted
    for folder in sorted(available):
        if folder not in posted:
            return folder

    return None


# ---------------------------------------------------------------------------
# Content generation
# ---------------------------------------------------------------------------


def generate_next_content(log: dict) -> str | None:
    """Generate the next content using carousel_generator."""
    generated = set(log.get("generated", []))
    available = set(get_available_stock())

    for folder_name in GENERATION_ORDER:
        if folder_name not in generated and folder_name not in available:
            func_name = GENERATOR_MAP.get(folder_name)
            if not func_name:
                continue

            print(f"🔧 Generating content: {folder_name} ({func_name})")

            try:
                result = subprocess.run(
                    [PYTHON, "-c", f"from carousel_generator import {func_name}; {func_name}()"],
                    cwd=BASE_DIR,
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if result.returncode == 0:
                    print(f"  ✅ Generated: {folder_name}")
                    log.setdefault("generated", []).append(folder_name)
                    save_log(log)
                    return folder_name
                else:
                    print(f"  ❌ Generation failed: {result.stderr[:200]}")
                    return None
            except subprocess.TimeoutExpired:
                print("  ❌ Generation timed out")
                return None

    print("⚠️  No more content to generate!")
    return None


# ---------------------------------------------------------------------------
# Token auto-refresh
# ---------------------------------------------------------------------------

REFRESH_THRESHOLD_DAYS = 7


def check_and_refresh_token():
    """Check token expiry and refresh if ≤ 7 days remain."""
    token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
    app_id = os.environ.get("META_APP_ID")
    app_secret = os.environ.get("META_APP_SECRET")

    if not all([token, app_id, app_secret]):
        print("⚠️  Token refresh skipped (missing META_APP_ID or META_APP_SECRET)")
        return

    # Debug token to check expiry
    try:
        resp = requests.get(
            f"https://graph.facebook.com/v22.0/debug_token",
            params={"input_token": token, "access_token": token},
            timeout=15,
        )
        data = resp.json().get("data", {})
        expires_at = data.get("expires_at", 0)

        if expires_at == 0:
            print("⚠️  Token has no expiry (permanent token)")
            return

        remaining = expires_at - datetime.now(timezone.utc).timestamp()
        remaining_days = remaining / 86400

        print(f"🔑 Token expires in {remaining_days:.1f} days")

        if remaining_days > REFRESH_THRESHOLD_DAYS:
            return  # Still valid, no refresh needed

        if remaining_days <= 0:
            print("❌ Token has already expired! Manual re-auth required.")
            return

    except Exception as e:
        print(f"⚠️  Token check failed: {e}")
        return

    # Refresh the token
    print("🔄 Refreshing token...")
    try:
        resp = requests.get(
            "https://graph.facebook.com/v22.0/oauth/access_token",
            params={
                "grant_type": "fb_exchange_token",
                "client_id": app_id,
                "client_secret": app_secret,
                "fb_exchange_token": token,
            },
            timeout=15,
        )
        result = resp.json()

        if "access_token" not in result:
            print(f"❌ Token refresh failed: {result.get('error', {}).get('message', 'Unknown')}")
            return

        new_token = result["access_token"]
        new_expires = result.get("expires_in", 0) / 86400

        # Update .env file
        env_path = os.path.join(BASE_DIR, ".env")
        with open(env_path, "r") as f:
            content = f.read()

        content = re.sub(
            r"INSTAGRAM_ACCESS_TOKEN=.*",
            f"INSTAGRAM_ACCESS_TOKEN={new_token}",
            content,
        )

        with open(env_path, "w") as f:
            f.write(content)

        # Update current process env
        os.environ["INSTAGRAM_ACCESS_TOKEN"] = new_token

        print(f"✅ Token refreshed! New expiry: {new_expires:.0f} days")

    except Exception as e:
        print(f"❌ Token refresh error: {e}")


# ---------------------------------------------------------------------------
# Posting
# ---------------------------------------------------------------------------


def post_folder(folder: str, dry_run: bool = False) -> str | None:
    """Post a folder's content to Instagram."""
    folder_path = os.path.join(OUTPUT_DIR, folder)

    cmd = [PYTHON, POSTER_SCRIPT, folder_path]
    if dry_run:
        cmd.append("--dry-run")

    print(f"\n📱 Posting: {folder}")
    result = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True, timeout=300)

    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        print(f"❌ Posting failed (exit code {result.returncode})")
        return None

    # Extract media ID from output
    for line in result.stdout.split("\n"):
        if "Media ID:" in line:
            media_id = line.split("Media ID:")[-1].strip()
            return media_id

    return "dry-run" if dry_run else "unknown"


def post_folder_facebook(folder: str, dry_run: bool = False) -> str | None:
    """Post a folder's content to Facebook Page."""
    if os.environ.get("FACEBOOK_POSTING_ENABLED", "").lower() != "true":
        return None

    if not os.environ.get("FACEBOOK_PAGE_ID"):
        print("\n⏭️  Facebook posting skipped (no FACEBOOK_PAGE_ID)")
        return None

    folder_path = os.path.join(OUTPUT_DIR, folder)
    cmd = [PYTHON, FB_POSTER_SCRIPT, folder_path]
    if dry_run:
        cmd.append("--dry-run")

    print(f"\n📘 Posting to Facebook: {folder}")
    try:
        result = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True, timeout=300)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            print(f"⚠️  Facebook posting failed (exit code {result.returncode})")
            return None
        for line in result.stdout.split("\n"):
            if "Post ID:" in line:
                return line.split("Post ID:")[-1].strip()
        return "dry-run" if dry_run else "unknown"
    except Exception as e:
        print(f"⚠️  Facebook posting error: {e}")
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def show_status():
    """Show current posting status."""
    log = load_log()
    posted = get_posted_folders(log)
    stock = get_available_stock()
    unposted = [f for f in stock if f not in posted]

    print("=" * 50)
    print("📊 Instagram Auto-Poster Status")
    print("=" * 50)
    print(f"\n📁 Total stock:    {len(stock)} folders")
    print(f"✅ Posted:         {len(posted)} folders")
    print(f"📦 Remaining:      {len(unposted)} folders")

    if unposted:
        next_folder = get_next_to_post(log)
        print(f"\n⏭️  Next to post:   {next_folder}")

    print("\n── Posted History ──")
    for entry in log["posted"][-10:]:
        print(f"  {entry['posted_at'][:16]}  {entry['folder']}")

    if unposted:
        print("\n── Remaining Stock ──")
        for f in unposted[:10]:
            print(f"  📦 {f}")

    print()


def run(dry_run: bool = False):
    """Main execution: find next content and post it."""
    os.makedirs(LOG_DIR, exist_ok=True)

    # Log this run
    timestamp = datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(LOG_DIR, f"daily_{datetime.now(JST).strftime('%Y%m%d')}.log")

    print(f"\n{'='*50}")
    print(f"🕐 Daily Poster — {timestamp}")
    print(f"{'='*50}")

    # Auto-refresh token if needed
    check_and_refresh_token()

    log = load_log()

    # Find next folder to post
    next_folder = get_next_to_post(log)

    if not next_folder:
        print("\n📭 No stock available. Generating new content...")
        generated = generate_next_content(log)
        if generated:
            next_folder = generated
        else:
            msg = f"[{timestamp}] ❌ No content to post and generation failed"
            print(msg)
            with open(log_file, "a") as f:
                f.write(msg + "\n")
            return

    # Post to Instagram
    media_id = post_folder(next_folder, dry_run=dry_run)

    # Post to Facebook (independent — failure doesn't affect IG)
    fb_post_id = post_folder_facebook(next_folder, dry_run=dry_run)

    if media_id:
        add_post_record(log, next_folder, media_id)
        msg = f"[{timestamp}] ✅ Posted: {next_folder} (IG: {media_id})"
        if fb_post_id:
            msg += f" (FB: {fb_post_id})"
    else:
        msg = f"[{timestamp}] ❌ Failed to post: {next_folder}"

    print(msg)
    with open(log_file, "a") as f:
        f.write(msg + "\n")


def main():
    parser = argparse.ArgumentParser(description="Daily Instagram Auto-Poster")
    parser.add_argument("--dry-run", action="store_true", help="Test without actually posting")
    parser.add_argument("--status", action="store_true", help="Show posting status")
    args = parser.parse_args()

    if args.status:
        show_status()
    else:
        run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
