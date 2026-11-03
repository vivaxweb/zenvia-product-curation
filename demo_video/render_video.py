"""
Automated High-Definition Video Demo Producer for Zenvia AI
Captures pixel-perfect 1080p screen interactions synchronized with neural voiceover.
"""

import os
import sys
import json
import time
import subprocess
from playwright.sync_api import sync_playwright

FFMPEG = r"C:\Users\ADMIN\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
DEMO_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_VIDEO_DIR = os.path.join(DEMO_DIR, "raw_recordings")
MANIFEST_PATH = os.path.join(DEMO_DIR, "audio_manifest.json")
FINAL_MP4 = os.path.join(DEMO_DIR, "zenvia_ai_hackathon_demo.mp4")

os.makedirs(RAW_VIDEO_DIR, exist_ok=True)

def smooth_scroll(page, target_y, steps=25, delay=0.03):
    current_y = page.evaluate("window.scrollY")
    diff = target_y - current_y
    for i in range(1, steps + 1):
        y = current_y + (diff * (i / steps))
        page.evaluate(f"window.scrollTo(0, {y})")
        time.sleep(delay)

def record_session():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = {item["id"]: item["duration"] for item in json.load(f)}

    print("Loaded audio durations:", manifest)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--font-render-hinting=none", "--force-device-scale-factor=1"]
        )
        context = browser.new_context(
            record_video_dir=RAW_VIDEO_DIR,
            record_video_size={"width": 1920, "height": 1080},
            viewport={"width": 1920, "height": 1080},
        )
        page = context.new_page()

        # ── SCENE 1: HOOK & FIRSTHAND PROBLEM ──
        s1_start = time.time()
        s1_target = manifest.get("scene1_intro", 37.7)
        print(f"Recording Scene 1 (Target: {s1_target:.2f}s)...")

        page.goto("http://localhost:8501", wait_until="networkidle")
        page.wait_for_timeout(3500)

        # Hover on top profile bar
        page.hover(".top-profile-bar")
        page.wait_for_timeout(2000)

        # Smooth scroll through hero banner
        smooth_scroll(page, 280, steps=30, delay=0.04)
        page.wait_for_timeout(3000)
        smooth_scroll(page, 0, steps=25, delay=0.04)

        # Pad remaining time
        elapsed = time.time() - s1_start
        if elapsed < s1_target:
            page.wait_for_timeout(int((s1_target - elapsed) * 1000))

        # ── SCENE 2: CATALOG SHOWCASE ──
        s2_start = time.time()
        s2_target = manifest.get("scene2_showcase", 41.2)
        print(f"Recording Scene 2 (Target: {s2_target:.2f}s)...")

        # Stat boxes hover
        page.hover(".stat-grid")
        page.wait_for_timeout(2500)

        # Scroll to first product (LEOTUDE Red Tee)
        smooth_scroll(page, 620, steps=30, delay=0.04)
        page.wait_for_timeout(4000)

        # Scroll to second product (Blazer)
        smooth_scroll(page, 1150, steps=35, delay=0.04)
        page.wait_for_timeout(5000)

        # Scroll back up to filter bar
        smooth_scroll(page, 320, steps=30, delay=0.04)
        page.wait_for_timeout(3000)

        elapsed = time.time() - s2_start
        if elapsed < s2_target:
            page.wait_for_timeout(int((s2_target - elapsed) * 1000))

        # ── SCENE 3: BATCH CATALOG STUDIO ──
        s3_start = time.time()
        s3_target = manifest.get("scene3_batch_studio", 38.2)
        print(f"Recording Scene 3 (Target: {s3_target:.2f}s)...")

        # Navigate to Batch Studio
        page.locator("p:has-text('Batch Catalog Studio')").first.click()
        page.wait_for_timeout(3000)

        # Click Load Demo Feed
        load_btn = page.locator("button:has-text('Load Demo Feed')")
        if load_btn.count() > 0:
            load_btn.first.click()
            page.wait_for_timeout(3000)

        # Scroll down to run button
        smooth_scroll(page, 450, steps=25, delay=0.04)
        page.wait_for_timeout(2000)

        # Click Start Autonomous Multimodal Tagging
        run_btn = page.locator("button:has-text('Start Autonomous Multimodal Tagging')")
        if run_btn.count() > 0:
            run_btn.first.click()
            page.wait_for_timeout(8000)

        # Scroll down to see generated value and download button
        smooth_scroll(page, 750, steps=25, delay=0.04)
        page.wait_for_timeout(4000)

        elapsed = time.time() - s3_start
        if elapsed < s3_target:
            page.wait_for_timeout(int((s3_target - elapsed) * 1000))

        # ── SCENE 4: REAL-TIME PLAYGROUND & BENCHMARKS ──
        s4_start = time.time()
        s4_target = manifest.get("scene4_playground_benchmarks", 27.8)
        print(f"Recording Scene 4 (Target: {s4_target:.2f}s)...")

        # Navigate to Playground
        page.locator("p:has-text('Real-Time Vision Playground')").first.click()
        page.wait_for_timeout(2500)

        # Click preset button
        preset_btn = page.locator("button:has-text('Streetwear Drop Shoulder Tee')")
        if preset_btn.count() > 0:
            preset_btn.first.click()
            page.wait_for_timeout(2000)

        # Scroll down to see preset fields
        smooth_scroll(page, 300, steps=20, delay=0.04)
        page.wait_for_timeout(3000)

        # Navigate to Benchmark & Precision Studio
        page.locator("p:has-text('Benchmark & Precision Studio')").first.click()
        page.wait_for_timeout(2500)

        # Scroll down to Head-to-Head Table
        smooth_scroll(page, 380, steps=25, delay=0.04)
        page.wait_for_timeout(4000)

        elapsed = time.time() - s4_start
        if elapsed < s4_target:
            page.wait_for_timeout(int((s4_target - elapsed) * 1000))

        # ── SCENE 5: FOUNDER STORY & CODE QUALITY ──
        s5_start = time.time()
        s5_target = manifest.get("scene5_code_outro", 17.6)
        print(f"Recording Scene 5 (Target: {s5_target:.2f}s)...")

        page.locator("p:has-text('Founder Story')").first.click()
        page.wait_for_timeout(2500)

        smooth_scroll(page, 350, steps=25, delay=0.04)
        page.wait_for_timeout(4000)

        # Scroll to footer
        smooth_scroll(page, 750, steps=25, delay=0.04)
        page.wait_for_timeout(3000)

        elapsed = time.time() - s5_start
        if elapsed < s5_target:
            page.wait_for_timeout(int((s5_target - elapsed) * 1000))

        # Close page & context to finalize webm recording
        video_obj = page.video
        context.close()
        browser.close()

        raw_video_path = video_obj.path()
        print("Raw video recorded to:", raw_video_path)
        return raw_video_path

def merge_video_and_audio(raw_video_path):
    full_audio_path = os.path.join(DEMO_DIR, "full_voiceover.mp3")
    print(f"Merging raw video {raw_video_path} with {full_audio_path}...")

    # FFmpeg command to merge, sync length, and encode to MP4
    cmd = [
        FFMPEG, "-y",
        "-i", raw_video_path,
        "-i", full_audio_path,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "19",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        FINAL_MP4
    ]
    subprocess.run(cmd, check=True)
    print(f"SUCCESS! Finalized hackathon demo video created at:\n{FINAL_MP4}")

    # Check file size
    size_mb = os.path.getsize(FINAL_MP4) / (1024 * 1024)
    print(f"Final video size: {size_mb:.2f} MB")

if __name__ == "__main__":
    raw_path = record_session()
    merge_video_and_audio(raw_path)
