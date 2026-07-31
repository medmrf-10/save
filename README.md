# 🔄 RTL Support for Antigravity Editor

> **Auto-detect RTL/LTR direction per line** — Arabic, Hebrew, and other RTL languages just work.

[![Python 3](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![RTL](https://img.shields.io/badge/RTL-Supported-orange.svg)]()

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Auto-detect per line** | Each line detects its direction from content — Arabic char first → RTL, Latin char first → LTR |
| **Markdown optimized** | `.md`, `.markdown`, `.mdx` files default to RTL for empty/neutral lines |
| **Arrow keys fix** | Removes the confusing RTL arrow swap — arrows move visually |
| **Wrap indent fix** | Uses `padding-inline-start` instead of `padding-left` for proper RTL line wrapping |
| **Chat RTL** | CSS rules for RTL in chat widgets and rendered markdown |
| **Zero config** | No keyboard shortcuts, no localStorage, no inheritance — just works |

## 🚀 Quick Start

### Prerequisites

- **Antigravity Editor** installed at `/Applications/Antigravity.app/`
- **Python 3.x**
- Clean backup files in `/Users/med10/med/plugins/`:
  - `workbench.desktop.main.js.backup`
  - `workbench.desktop.main.css.backup`

### Installation

```bash
# 1. Run the patch script
python3 rtl.py

# 2. Copy patched files (requires sudo)
sudo cp /tmp/workbench.desktop.main.js \
  '/Applications/Antigravity.app/Contents/Resources/app/out/vs/workbench/workbench.desktop.main.js'

sudo cp /tmp/workbench.desktop.main.css \
  '/Applications/Antigravity.app/Contents/Resources/app/out/vs/workbench/workbench.desktop.main.css'

# 3. Restart Antigravity (Cmd+Q then reopen)
```

## 🔧 How It Works

The script applies **4 modifications** to the Antigravity editor source:

```
┌─────────────────────────────────────────────────┐
│  MOD 1: P() — Direction Detection               │
│  Scans each line for first strong directional    │
│  character (Arabic/Hebrew → RTL, Latin → LTR)    │
├─────────────────────────────────────────────────┤
│  MOD 2: XLl — Wrap Indentation                  │
│  padding-left → padding-inline-start             │
├─────────────────────────────────────────────────┤
│  MOD 3: Arrow Keys Fix                           │
│  Removes RTL direction swap for arrow movement   │
├─────────────────────────────────────────────────┤
│  MOD 4: File Detection Script                    │
│  Sets _rtlDefault flag based on file extension   │
└─────────────────────────────────────────────────┘
```

### Direction Detection Logic

```
Line Content           → Direction
─────────────────────────────────
"مرحبا بالعالم"         → RTL (first char is Arabic)
"Hello World"           → LTR (first char is Latin)
"# مقدمة"              → LTR (# is neutral, but detected by first strong char)
"  "  (empty/spaces)    → RTL (default for .md files)
```

### Supported Unicode Ranges

| Range | Script |
|-------|--------|
| `U+0600–U+06FF` | Arabic |
| `U+0750–U+077F` | Arabic Supplement |
| `U+08A0–U+08FF` | Arabic Extended-A |
| `U+FB50–U+FDFF` | Arabic Presentation Forms-A |
| `U+FE70–U+FEFF` | Arabic Presentation Forms-B |
| `U+0590–U+05FF` | Hebrew |

## 📁 Project Structure

```
save/
├── rtl.py          # Main patch script — applies all 4 modifications
└── README.md       # This file
```

## ⚠️ Known Issues

- [#1](../../issues/1) — Arrow keys may still feel reversed in some edge cases
- [#2](../../issues/2) — Wiki links in RTL have clickability issues
- [#3](../../issues/3) — Chat and manager editor need additional RTL support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b fix/arrow-keys`)
3. Commit your changes (`git commit -m 'fix: improve arrow key behavior in RTL'`)
4. Push to the branch (`git push origin fix/arrow-keys`)
5. Open a Pull Request

## 📝 Notes

- Always keep clean backups of the original `workbench.desktop.main.js` and `.css` files
- After each Antigravity update, you'll need to re-run the patch
- The script validates each modification and will abort with errors if patterns aren't found

---

<div align="center">

**Made with ❤️ for the Arabic & RTL developer community**

</div>
