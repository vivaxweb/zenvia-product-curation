"""
Generate synchronized voiceover segments using Edge-TTS.
"""

import asyncio
import os
import subprocess
import edge_tts

VOICE = "en-US-ChristopherNeural"
FFMPEG = r"C:\Users\ADMIN\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPTS = [
    {
        "id": "scene1_intro",
        "text": (
            "Hi everyone, I'm Vivek Desai. I'm building Zenvia at zenviashopping.in, "
            "a fashion discovery platform for Gen Z shoppers in India. "
            "Gen Z doesn't shop by rigid categories like T-shirts or Pants; we shop by aesthetic vibes: "
            "streetwear, quiet luxury, Y2K, and retro. "
            "But Indian marketplaces like Amazon, Myntra, and Meesho have messy keywords and plain descriptions. "
            "Up until now, I had to manually look at every product photo and tag it by hand, "
            "taking 3 minutes per item, and capping our catalog to only 50 products a day."
        )
    },
    {
        "id": "scene2_showcase",
        "text": (
            "To solve this firsthand problem, I built Zenvia AI, an autonomous multimodal vibe-classification engine. "
            "Look at our live Catalog Showcase. The four metric cards show a 60x curation speedup, "
            "100% precision, and zero marginal API cost. "
            "Instead of just reading plain titles, our vision pipeline inspected the photograph directly. "
            "For this red graphic tee, it perceived the bold collegiate lettering and drop shoulder silhouette, "
            "tagging it as streetwear and retro with 95% confidence. "
            "For this tailored blazer, it recognized the structured suiting and minimal lapels, "
            "assigning quiet luxury and old money."
        )
    },
    {
        "id": "scene3_batch_studio",
        "text": (
            "Real e-commerce operators don't tag one item at a time; they deal with spreadsheets. "
            "In our Batch Catalog Studio, you can upload any supplier Excel or CSV file, or download our blank starter template. "
            "Let's load our demo feed with 10 items, and start autonomous multimodal tagging. "
            "Watch it process live: with every garment, it extracts visual cues, tags subcultures, "
            "and calculates real operational ROI, saving 9 minutes of human labor and 60 rupees in freelance curation fees. "
            "With one click, we can download the enriched Excel spreadsheet ready for our live store."
        )
    },
    {
        "id": "scene4_playground_benchmarks",
        "text": (
            "Judges can also test any custom product URL or try our one-click presets in the Real-Time Playground. "
            "Selecting the Streetwear Drop Shoulder Tee immediately returns the verified taxonomy and visual cues in just 1.2 seconds. "
            "Looking at our empirical benchmarks, Zenvia AI is 60x faster than manual human curation, "
            "achieves 100% subcategory precision, and operates sustainably at zero marginal API cost."
        )
    },
    {
        "id": "scene5_code_outro",
        "text": (
            "The entire codebase is open-source on GitHub at vivaxweb slash zenvia-product-curation, "
            "backed by 11 automated unit tests and continuous integration. "
            "Zenvia AI turns raw marketplace noise into an aesthetic vibe-feed, built for the real world. "
            "Thank you!"
        )
    }
]

def get_audio_duration(file_path: str) -> float:
    cmd = [
        FFMPEG, "-i", file_path,
        "-f", "null", "-"
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in proc.stderr.splitlines():
        if "Duration:" in line:
            # Duration: 00:00:23.45, start: ...
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            hours = float(parts[0])
            mins = float(parts[1])
            secs = float(parts[2])
            return hours * 3600 + mins * 60 + secs
    return 20.0

async def main():
    print("Generating voiceover audio segments...")
    manifest = []
    for item in SCRIPTS:
        mp3_path = os.path.join(OUTPUT_DIR, f"{item['id']}.mp3")
        communicate = edge_tts.Communicate(item["text"], VOICE, rate="+3%")
        await communicate.save(mp3_path)
        dur = get_audio_duration(mp3_path)
        print(f"Generated {item['id']}.mp3 -> Duration: {dur:.2f}s")
        manifest.append({
            "id": item["id"],
            "file": mp3_path,
            "duration": dur,
        })

    # Concatenate all audio segments into single full voiceover track
    concat_list_file = os.path.join(OUTPUT_DIR, "audio_concat.txt")
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for m in manifest:
            # Windows path handling for ffmpeg concat
            f.write(f"file '{m['id']}.mp3'\n")

    full_audio_path = os.path.join(OUTPUT_DIR, "full_voiceover.mp3")
    concat_cmd = [
        FFMPEG, "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_file,
        "-c", "copy", full_audio_path
    ]
    subprocess.run(concat_cmd, check=True)
    total_dur = get_audio_duration(full_audio_path)
    print(f"Total Combined Audio Duration: {total_dur:.2f}s (~{total_dur/60:.2f} mins)")

    # Save manifest json
    manifest_path = os.path.join(OUTPUT_DIR, "audio_manifest.json")
    import json
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
