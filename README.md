# 🐉 Dragon Lineage Visualizer

**Dragon Lineage Visualizer** is a web-based tool that helps you explore the descendants tree of your dragons on Flight Rising, without clicking endlessly through offspring pages.

Curious about where your dragons' descendants ended up? Whether they’ve:
- Started their own clans,
- Raised families of their own,
- Or sworn service to the elemental gods...

This tool fetches that information for you and visualizes it in an interactive, easy-to-read **lineage tree**.

---

## ✨ Features
- 🔍 **Enter a Dragon ID** to view their full offspring tree.
- 🧭 **See multiple generations** of descendants at a glance.
- ⚔️ **Exclude exalted dragons** to focus on those still active in lairs.
- 🕸️ **Interactive tree layout** built with D3.js for visual clarity.

---

## ⚙️ How It Works
- The app scrapes the public offspring data from Flight Rising based on the provided dragon ID.
- It constructs a hierarchical tree of descendants up to a chosen number of generations.
- The tree is rendered using D3.js with clear parent-child relationships and optional filters.

---

## 📁 Project Structure
dragon_lineage_visualizer/
├── backend/ # Scraping and data-processing logic
├── static/ # Static assets (JSON output, CSS, JS)
│ └── data/ # Cached dragon tree data
├── templates/ # HTML templates for the frontend
└── server.py # Flask app entry point


🚀 Getting Started
Clone the repo.

Install dependencies: pip install -r requirements.txt

Run the app: python server.py

Open your browser to http://localhost:8000