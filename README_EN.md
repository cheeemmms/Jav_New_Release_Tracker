# JAV New Release Tracker (JRT)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Ready-brightgreen)]()
[![GitHub stars](https://img.shields.io/github/stars/cheeemmms/Jav_New_Release_Tracker?style=flat)](https://github.com/cheeemmms/Jav_New_Release_Tracker/stargazers)

> 🇨🇳 [中文版](README.md) | 🇬🇧 English

Automatically scrape new releases for your favorite actresses, generate Markdown reports, and preview them in batches in your browser.

> 🤖 This project was entirely written by AI.

---

## ⚠️ Disclaimer

- **This project is for personal learning of Python programming and web automation techniques only.**
- Users are responsible for complying with the target website's `robots.txt` and terms of service.
- Please control scraping frequency responsibly. The program includes built-in random delays of 3-7 seconds. Do not modify these to excessively short intervals.
- Any legal risks or liabilities arising from the use of this project are borne solely by the user.
- The author assumes no responsibility for any misuse.

---

## Features

- **Incremental Scraping** — Only fetches new releases based on your last run date or a manually entered date
- **Precision Targeting** — Directly visits actress profile pages via UID, no site-wide search
- **Smart Filtering** — Automatically excludes VR content
- **Aggregated Reports** — Generates Markdown files organized by actress
- **Batched Preview** — Opens links in your browser in batches of 20
- **State Memory** — Automatically records the current date after each successful run

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────┐
│  1. Launch → Shows last run date                         │
│  2. Choose: Use last date / Enter a new date             │
│  3. Browser opens automatically → Scrapes each actress    │
│  4. Generates Markdown report (outputs/Updates_*.md)     │
│  5. Opens new release links in browser batches           │
│  6. Saves current date → Done                           │
└─────────────────────────────────────────────────────────┘
```

---

## Beginner's Setup Guide

If you're new to Python projects, follow these steps:

### Step 1: Install Python

1. Open your browser and visit https://www.python.org/downloads/
2. Click the yellow **Download Python** button to download the latest installer
3. **Important**: During installation, make sure to check **"Add Python to PATH"** at the bottom, then click Install Now

   ```
   ┌──────────────────────────────────┐
   │  ☑ Add Python to PATH  ← MUST CHECK │
   │  [Install Now]                   │
   └──────────────────────────────────┘
   ```

4. Verify the installation:

   - Press `Win + R`, type `cmd`, and press Enter to open Command Prompt
   - Type the following command. It should display a Python version (e.g., `Python 3.12.x`):

   ```bash
   python --version
   ```

### Step 2: Download the Project

**Option A (Recommended): Clone with Git**

```bash
git clone https://github.com/cheeemmms/Jav_New_Release_Tracker.git
cd Jav_New_Release_Tracker
```

**Option B: Download ZIP**

1. Open https://github.com/cheeemmms/Jav_New_Release_Tracker
2. Click the green **Code** button → **Download ZIP**
3. Extract to your preferred directory (e.g., `D:\Jav_New_Release_Tracker`)
4. In the extracted folder's address bar, type `cmd` and press Enter to open Command Prompt

### Step 3: Install Dependencies

In the project directory (Command Prompt), run:

```bash
pip install -r requirements.txt
```

If you see an error saying `pip` is not recognized:

```bash
python -m pip install -r requirements.txt
```

### Step 4: Install the Browser

```bash
playwright install chromium
```

This downloads a standalone Chromium browser (~150MB) used by the program. You only need to do this once.

### Step 5: Verify Your Environment

Run this command to confirm everything is ready:

```bash
python -c "import yaml, arrow, rich, bs4, playwright; print('Environment ready!')"
```

Seeing `Environment ready!` means you're all set.

---

## Configuration Guide

### Config File Location

All configuration is in `config/config.yaml`. Open it with any text editor (Notepad, VS Code, etc.).

### How to Find an Actress UID

1. Open the target website (e.g., `https://www.javbus.com`)
2. Search for an actress name and click through to her profile page
3. Look at the browser address bar. The URL format is:

   ```
   https://www.javbus.com/star/xxxx
                            ↑
                      This is the UID
   ```

   | Example | Page URL | UID (put in config) |
   |---------|----------|---------------------|
   | Yua Mikami | `javbus.com/star/12xc` | `12xc` |
   | Eimi Fukada | `javbus.com/star/ok12` | `ok12` |

   Just grab the part after `/star/` in the URL.

### Configuring Your Actress List

Edit `config/config.yaml`:

```yaml
settings:
  proxy: "http://127.0.0.1:7890"   # Proxy address, see below
  batch_size: 20                   # Links per browser batch
  headless: false                  # Hide browser? (recommend false)
  start_date: ""                   # Fixed start date, skips interactive prompt (optional)

stars:
  - { name: "Yua Mikami", id: "12xc" }
  - { name: "Eimi Fukada", id: "ok12" }
  - { name: "Your Actress", id: "her-uid" }
```

- `name`: Any display name, used in reports
- `id`: The UID extracted from her profile URL
- To add more actresses, copy the `{ name: "...", id: "..." }` line

#### Fixed Start Date

Set `start_date` in `settings` to skip the date selection prompt each run:

```yaml
settings:
  start_date: "2026-05-01"
```

- When set, the program **skips** the interactive date selection
- Leave empty `""` or omit to restore interactive mode

### Proxy Settings

If access requires a proxy, common defaults:

| Proxy Tool | Default Address |
|------------|----------------|
| Clash / Clash Verge | `http://127.0.0.1:7890` |
| V2Ray / v2rayN | `http://127.0.0.1:10809` |
| SSR | `http://127.0.0.1:1080` |

**No proxy needed**: Set `proxy` to an empty string:

```yaml
settings:
  proxy: ""
```

### About Headless Mode

- `headless: false` — **Recommended**. The browser window is visible so you can manually complete any CAPTCHA challenges.
- `headless: true` — Runs in the background with no visible window. Good for daily use once everything is confirmed working.

---

## Running the Program

From the project directory:

```bash
python src/main.py
```

### First Run

```
+--------------------------------------------------+
| JAV New Release Tracker                           |
+--------------------------------------------------+
[INFO] Loading config...
[INFO] First run — please enter a start date
Enter start date (YYYY-MM-DD): 2026-01-01

Entering 2026-01-01 will scrape all releases published after that date.
On subsequent runs, the program remembers where it left off.
```

### Subsequent Runs

```
Last run date: 2026-05-01, please choose:
  1. Use last date (2026-05-01)
  2. Enter a new date
Enter number:
```

Choose `1` to incrementally scrape only new releases since May 1st.

### Output

The program generates a Markdown report in the `outputs/` directory:

```
outputs/
└── Updates_20260502.md
```

Sample report:

```markdown
# JAV Update Report (2026-05-02)

## Yua Mikami
1. **Release Title One**
   - Date: 2026-05-01
   - Link: [https://www.javbus.com/...](...)

## Eimi Fukada
> No new releases
```

The program then opens new release links in your browser in batches of 20, asking for confirmation between batches.

---

## FAQ

<details>
<summary><b>Q: "No module named 'xxx'"</b></summary>

Dependencies are not fully installed. Re-run:
```bash
pip install -r requirements.txt
```
</details>

<details>
<summary><b>Q: "playwright browser not installed"</b></summary>

Run:
```bash
playwright install chromium
```
</details>

<details>
<summary><b>Q: Browser crashes or page fails to load</b></summary>

1. Check your proxy: make sure the proxy app is running and the port is correct
2. Set `headless: false` to observe what's happening in the browser window
3. If a Cloudflare challenge appears, complete it manually in the visible browser window
</details>

<details>
<summary><b>Q: Will the program crash if one actress fails?</b></summary>

No. Errors for individual actress pages are caught, and the program skips to the next one.
</details>

<details>
<summary><b>Q: How do I change the batch size?</b></summary>

Edit `batch_size` in `config/config.yaml` (default: 20).
</details>

<details>
<summary><b>Q: How do I reset the state (re-scrape everything)?</b></summary>

Edit `config/state.json` and set `last_run_date` to a very early date, or simply delete the file.
</details>

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Browser Automation | Playwright + playwright-stealth |
| HTML Parsing | BeautifulSoup4 |
| Terminal UI | Rich |
| Config Format | YAML |
| State Persistence | JSON |

---

## Project Structure

```
Jav_New_Release_Tracker/
├── config/
│   ├── config.yaml          # Actress list, proxy, batch size
│   └── state.json           # Run state (auto-maintained)
├── src/
│   ├── main.py              # Entry point — orchestrates the workflow
│   ├── scraper/
│   │   ├── engine.py        # Browser engine (Playwright + Stealth)
│   │   └── parser.py        # Page parsing (BeautifulSoup)
│   ├── output/
│   │   ├── md_generator.py  # Markdown report generation
│   │   └── browser_opener.py# Batch browser opener
│   └── utils/
│       ├── logger.py        # Rich terminal logging
│       └── config_loader.py # YAML/JSON I/O
├── outputs/                 # Generated reports
├── requirements.txt
└── .gitignore
```

---

## Personalization

### Adding Your Own Bookmarks

You can place your own `favorites_*.html` browser bookmark files (e.g., exported from Chrome) in the project root directory. Git is configured to automatically ignore these files — they will never be committed to the repository.

---

## Roadmap

- [ ] Support excluding "compilation" or "trailer" tags
- [ ] Embed cover images in Markdown
- [ ] Auto-detect magnet link availability

---

## License

MIT
