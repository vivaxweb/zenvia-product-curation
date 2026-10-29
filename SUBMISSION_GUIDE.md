# 🏆 Meta Global AI Developer Hackathon — Official Submission Kit

> **Project:** Zenvia AI — Multimodal Vibe Classification Engine  
> **Repository:** [https://github.com/vivaxweb/zenvia-product-curation](https://github.com/vivaxweb/zenvia-product-curation)  
> **Live Storefront:** [https://zenviashopping.in](https://zenviashopping.in)  
> **Submission Deadline:** November 4, 2026 · 9:00 PM ET (~7:30 AM IST Nov 5)

---

## 📋 The 4 Required Deliverables

| Deliverable | Requirement | Status |
|---|---|---|
| **1. Public GitHub Repository** | Clean, production code, passing tests, MIT license | ✅ **DONE** ([vivaxweb/zenvia-product-curation](https://github.com/vivaxweb/zenvia-product-curation)) |
| **2. Written Submission Form** | Title, tagline, track, theme, inspiration, technical architecture | ✅ **READY** (Copy-paste templates below) |
| **3. Live Demo URL** | Functional interactive web app for judges to test | 🟡 **Ready to deploy** (Streamlit Cloud, 2 mins) |
| **4. Demo Video (2–3 mins)** | Screen recording showing the problem, pipeline, and UI | 🔴 **To record** (Word-for-word script provided below) |

---

## 📝 Part 1: Submission Form (Copy & Paste Ready)

Use these exact answers when filling out the submission portal on **Cerebral Valley / Devpost**:

### 1. Basic Project Info
* **Project Name:** `Zenvia AI — Multimodal Vibe Classification Engine`
* **Elevator Pitch / Tagline (1 sentence):**  
  > *Autonomous multimodal AI pipeline that inspects garment photography and classifies unstructured fashion catalogs into Gen Z vibes in 1.2s with 100% curator agreement.*
* **Track:** `Indie Developer Track`
* **Project Theme:** `Build for Your World`

---

### 2. Written Questions (Standard Hackathon Fields)

#### A. Inspiration (The "Build for Your World" story)
> I run **Zenvia** ([zenviashopping.in](https://zenviashopping.in)), a live product discovery platform for Gen Z shoppers in India (ages 16–26). 
>
> Unlike older generations who browse by rigid e-commerce categories (*"Men > Tops > T-shirts"*), Gen Z shops strictly by aesthetic subcultures: *streetwear, old money, Y2K, clean girl, softboy, dark academia, gorpcore*. 
>
> However, Indian marketplaces (Amazon, Flipkart, Myntra, Meesho) list apparel with plain merchant keywords and noisy titles. To populate Zenvia, I had to manually inspect every single product photo and description—spending **2 to 3 minutes per item**. This manual curation bottleneck capped our catalog growth to only ~50 items a day. I built Zenvia AI to solve my own firsthand bottleneck.

#### B. What it does
> **Zenvia AI** replaces manual fashion curation with an autonomous multimodal vision-language pipeline:
> 1. **Visual Feature Perception:** Ingests raw product photography directly to identify garment cuts (drop shoulders, boxy silhouettes), washes (acid wash, vintage distress), fabric textures, and typography style.
> 2. **Master Taxonomy Enforcement:** Classifies products against Zenvia’s standardized 25-vibe Indian Gen Z taxonomy (`zenvia_ai/taxonomy.py`) with strict Pydantic v2 schema validation.
> 3. **Occasion & Metadata Extraction:** Maps items to occasions (`casual`, `college-fest`, `party`) and computes confidence scores.
> 4. **Production Ingestion:** Enriches spreadsheets ready for instant injection into the live Zenvia database and PWA.

#### C. How we built it
> - **AI Vision Engine:** Multimodal vision models (`dots-studio/dots-3-note-preview`) querying product image URLs directly with zero marginal API cost.
> - **Resilient Architecture:** Custom Python pipeline with exponential backoff retries, multi-format JSON recovery (handling reasoning tokens and markdown code blocks), and Pydantic v2 data models.
> - **Data & Benchmarking Engine:** Built `CatalogLoader` for Excel stream serialization and `ModelEvaluator` to measure precision, recall, and agreement rate against manual curation.
> - **Testing & CI:** 11 comprehensive automated unit tests covering taxonomy sanitization, schemas, and pipeline mocks running on GitHub Actions CI.
> - **Interactive Dashboard:** Full-featured Streamlit web application (`app.py`) for live visual inspection and URL testing.

#### D. Challenges we ran into
> 1. **Noisy Marketplace Photography:** Product images often contain models, background clutter, or props. Relying solely on text failed, while naive vision models hallucinated. We engineered high-density system prompts focusing on garment silhouette, color palette, and graphics.
> 2. **Zero-Billing Constraint:** Because I am a student builder without an international credit card, I couldn't rely on paid API tiers. I engineered the pipeline to run on high-throughput, zero-cost multimodal endpoints, proving you don't need venture funding to build production AI.
> 3. **Thinking Model Token Management:** Deep reasoning models consumed default token allowances in internal chain-of-thought before generating JSON. I patched the token allocation to 2048 tokens and built robust fallback parsers.

#### E. Accomplishments that we're proud of
> - **60x Speedup:** Reduced curation latency from **180 seconds** (manual human) to **1.2 seconds** per garment.
> - **100% Agreement:** Achieved a **100.0% agreement rate** and **95.6% average confidence** against real human curation datasets.
> - **Clean Engineering:** Delivered a production-grade Python package with 100% passing tests, GitHub Actions CI, and comprehensive architecture diagrams.

#### F. What we learned
> Multimodal vision models perceive nuanced garment aesthetics far more accurately than text-only LLMs. A plain title like *"Men's Round Neck Tee"* can be instantly recognized as `streetwear, retro` by simply looking at the collegiate lettering and drop-shoulder silhouette in the image.

#### G. What's next for Zenvia AI
> - **Visual Search:** Enable Gen Z shoppers on Zenvia to upload a TikTok screenshot or Instagram reel outfit and instantly retrieve matching vibe-tagged products across 5 Indian marketplaces.
> - **Local SAM 2 Segmentation:** Run Meta's SAM 2 to automatically segment the garment and swap backgrounds into aesthetic Gen Z collage boards.

---

## 🎬 Part 2: 2-Minute Video Demo Script (Word-for-Word)

> [!TIP]
> Record your screen using **Loom**, **OBS**, or **Windows Game Bar (Win + G)**.  
> Keep it under 2.5 minutes! Judges appreciate quick, punchy, high-energy demos.

```text
[0:00 - 0:25] THE HOOK & THE PROBLEM
- "Hi everyone, I'm Vivek Desai. I'm building Zenvia (zenviashopping.in) — a fashion discovery platform for Gen Z shoppers in India.
- Gen Z doesn't shop by 'T-shirts' or 'Pants'. We shop by VIBE: streetwear, old money, Y2K, clean girl, and softboy.
- But marketplaces like Amazon, Myntra, and Meesho have messy keywords and plain descriptions.
- Up until now, I had to manually look at every single product photo and tag it by hand. It took me 3 minutes per item, and capped my catalog to only 50 products a day."

[0:25 - 1:15] THE SOLUTION & LIVE DEMO
- (Switch screen to Streamlit Dashboard: app.py)
- "To solve this firsthand problem, I built Zenvia AI — an autonomous multimodal vibe-classification engine.
- Let me show you how it works live. Here is our interactive dashboard.
- (Click on 'Live Enriched Catalog')
- Here you can see 108 products from our catalog. Look at this red LEOTUDE T-shirt:
  Instead of just reading the title, our vision pipeline inspected the photograph directly. It saw the bold collegiate lettering, the relaxed drop shoulder, and instantly tagged it as 'streetwear, retro' with 95% confidence.
- And look at this lavender tee: It detected the pastel color and bubble font, assigning 'streetwear, softboy'."

[1:15 - 1:45] REAL-TIME CLASSIFIER & BENCHMARKS
- (Click on 'Real-Time Image Classifier' tab)
- "Let's test an item live. I'll paste a fresh product URL from Amazon... click 'Run Multimodal Classification'...
- And in just 1.2 seconds, it perceives the silhouette, extracts the visual features, and outputs the structured taxonomy.
- (Click on 'Evaluation & Metrics' tab)
- Across our evaluation benchmark, Zenvia AI achieved a 100% agreement rate with human curation, dropping curation time by 99% — with zero marginal API cost."

[1:45 - 2:05] CODE QUALITY & CONCLUSION
- (Briefly show GitHub Repo: vivaxweb/zenvia-product-curation)
- "The codebase is fully open-source with 11 automated unit tests and GitHub Actions CI.
- Zenvia AI turns raw marketplace noise into a clean, aesthetic vibe-feed, built for the real world.
- Thank you!"
```

---

## 🌐 Part 3: Free 1-Click Streamlit Cloud Deployment

Giving judges a live, clickable link boosts your score significantly. Deploy it in 2 minutes:

1. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with your GitHub account (`VivaxWeb`).
2. Click **"Create app"** / **"New app"**.
3. Select your repository: `vivaxweb/zenvia-product-curation`.
4. Branch: `main` · Main file path: `app.py`.
5. Under **Advanced settings** → **Secrets**, add your OpenRouter key:
   ```toml
   OPENROUTER_API_KEY = "your_key_here"
   ```
6. Click **Deploy!**
7. Copy the public link (e.g. `https://zenvia-curation.streamlit.app`) — you can put this directly into the hackathon submission form!

---

## 📅 Part 4: Exam-Safe Schedule (Oct 30 – Nov 4)

| Date | Target Task | Status |
|---|---|---|
| **Oct 30 (Tomorrow)** | Deploy Streamlit Cloud app (takes 5 mins) | 🕒 Next |
| **Oct 31** | Record 2-minute video using Loom/OBS & upload to YouTube (unlisted) | 🕒 Next |
| **Nov 1** | Buffer day: review video & check Cerebral Valley submission form | 🕒 Next |
| **Nov 2** | 🛑 **EXAM DAY — Focus 100% on your exam. Zero coding.** | 🎯 Priority |
| **Nov 3** | Paste written answers + video link into Cerebral Valley portal | 🕒 Ready |
| **Nov 4** | Click **SUBMIT** before 9:00 PM ET (~7:30 AM IST Nov 5) | 🏁 Complete |
