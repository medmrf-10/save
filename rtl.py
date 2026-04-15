#!/usr/bin/env python3
"""
RTL Support for Antigravity v9.0 — Force RTL
==============================================
Force RTL for ALL lines in .md files regardless of language:
- .md files → ALL lines RTL (Arabic, English, whatever)
- Non-.md files → LTR (default)

NO per-line detection, NO language checking.
Everything in markdown is RTL. Period.

Usage:
  python3 rtl.py
  sudo cp /tmp/workbench.desktop.main.{js,css} \
    /Applications/Antigravity.app/Contents/Resources/app/out/vs/workbench/
"""

import subprocess

BACKUP_JS  = '/Users/med10/med/plugins/workbench.desktop.main.js.backup'
BACKUP_CSS = '/Users/med10/med/plugins/workbench.desktop.main.css.backup'
JS_TMP  = '/tmp/workbench.desktop.main.js'
CSS_TMP = '/tmp/workbench.desktop.main.css'
JS_DEST  = '/Applications/Antigravity.app/Contents/Resources/app/out/vs/workbench/workbench.desktop.main.js'
CSS_DEST = '/Applications/Antigravity.app/Contents/Resources/app/out/vs/workbench/workbench.desktop.main.css'

print("📖 قراءة النسخ الاحتياطية النظيفة...")
with open(BACKUP_JS, 'r') as f:
    js = f.read()
print(f"  JS: {len(js):,} chars ✅")

with open(BACKUP_CSS, 'r') as f:
    css = f.read()
print(f"  CSS: {len(css):,} chars ✅")

errors = []

# ==============================================================
# MOD 1: P() — Auto-detect direction from line content
# ==============================================================
print("\n🔧 [1/3] تعديل P() — إجبار RTL لكل الأسطر ...")

OLD_P = 'return i>0?IL.RTL:IL.LTR}getTextDirection'

# Force RTL logic:
# 1. Decorations override everything (original behavior)
# 2. For .md files: ALL lines → RTL (no language detection)
# 3. For non-.md files: LTR

NEW_P = (
    'if(i>0)return IL.RTL;if(i<0)return IL.LTR;'
    'if(typeof window==="undefined"||!window._rtlDefault)return IL.LTR;'
    'return IL.RTL'
    '}getTextDirection'
)

count = js.count(OLD_P)
if count == 1:
    js = js.replace(OLD_P, NEW_P)
    print("  ✅ P() — كل الأسطر RTL في ملفات .md")
else:
    errors.append(f"P() pattern: {count} (expected 1)")
    print(f"  ❌ {errors[-1]}")

# ==============================================================
# MOD 2: XLl — padding-inline-start for RTL wrap
# ==============================================================
print("\n🔧 [2/3] تعديل XLl (التفاف الأسطر) ...")

OLD_XLl = 'appendString("px; padding-left: ")'
NEW_XLl = 'appendString("px; padding-inline-start: ")'

text_indent_pos = js.find('text-indent: -')
if text_indent_pos != -1:
    xll_pos = js.find(OLD_XLl, text_indent_pos)
    if xll_pos != -1 and xll_pos - text_indent_pos < 200:
        js = js[:xll_pos] + NEW_XLl + js[xll_pos + len(OLD_XLl):]
        print("  ✅ XLl — padding-inline-start")
    else:
        errors.append("XLl: padding-left not near text-indent")
        print(f"  ❌ {errors[-1]}")
else:
    errors.append("XLl: text-indent not found")
    print(f"  ❌ {errors[-1]}")

# ==============================================================
# MOD 3: Minimal control script (just file detection!)
# ==============================================================
print("\n🔧 [3/3] سكريبت كشف الملف (مبسّط!) ...")

SCRIPT = r"""
;/* RTL_V90 */(function(){
/* RTL v9.0 — Force RTL + Cmd+; toggle per file */
window._rtlDefault=false;
var _ov={};
function _gf(){
  var el=document.querySelector('.tab.active .label-name span');
  if(!el)el=document.querySelector('.tab.active .label-name');
  return el?el.textContent.replace(/[●•*◌]/g,'').trim():''
}
function sync(){
  var f=_gf(),l=f.toLowerCase();
  var isMd=(l.endsWith('.md')||l.endsWith('.markdown')||l.endsWith('.mdx'));
  window._rtlDefault=(f in _ov)?_ov[f]:isMd
}
document.addEventListener('keydown',function(e){
  if((e.metaKey||e.ctrlKey)&&e.key===';'){
    e.preventDefault();e.stopPropagation();
    var f=_gf();if(!f)return;
    window._rtlDefault=!window._rtlDefault;
    _ov[f]=window._rtlDefault;
    var msg=window._rtlDefault?'↘ RTL':'↙ LTR';
    var n=document.createElement('div');
    n.textContent=msg;
    n.style.cssText='position:fixed;top:20px;right:20px;z-index:99999;background:#007acc;color:#fff;padding:10px 20px;border-radius:8px;font-size:16px;font-weight:bold;transition:opacity 0.5s;pointer-events:none;font-family:system-ui';
    document.body.appendChild(n);
    setTimeout(function(){n.style.opacity='0'},1500);
    setTimeout(function(){n.remove()},2000);
    console.log('🔄 RTL toggle:',msg,'for',f)
  }
},true);
setTimeout(function(){
  setInterval(sync,300);sync();
  console.log('🔄 RTL v9.0 — Cmd+; to toggle direction')
},2000)
})();
"""

js += '\n' + SCRIPT
print("  ✅ سكريبت مبسّط (كشف الملف فقط — 10 أسطر!)")

# ==============================================================
# CSS
# ==============================================================
RTL_CSS = """
/* ===== RTL v9.0 — Force RTL ===== */

/* === Editor RTL === */
.view-line[dir="rtl"]{text-align:right}
.view-line[dir="rtl"]>span>span[style*="unicode-bidi"]{unicode-bidi:normal!important}

/* === Chat Panel RTL (interactive-session) === */
.interactive-session{direction:rtl;text-align:right}
.interactive-item-container{direction:rtl;text-align:right}
.interactive-item-container .header{direction:rtl;flex-direction:row-reverse}
.interactive-item-container .value,
.interactive-item-container .value .rendered-markdown,
.interactive-item-container .value .rendered-markdown p,
.interactive-item-container .value .rendered-markdown li,
.interactive-item-container .value .rendered-markdown h1,
.interactive-item-container .value .rendered-markdown h2,
.interactive-item-container .value .rendered-markdown h3,
.interactive-item-container .value .rendered-markdown h4,
.interactive-item-container .value .rendered-markdown blockquote,
.interactive-item-container .value .rendered-markdown ul,
.interactive-item-container .value .rendered-markdown ol{direction:rtl;text-align:right;unicode-bidi:plaintext}

/* Chat input */
.interactive-session .chat-input-container{direction:rtl;text-align:right}
.interactive-input-part{direction:rtl}

/* === Agent Manager RTL === */
.antigravity-agent-side-panel{direction:rtl!important;text-align:right!important}
.antigravity-agent-side-panel *:not(pre):not(code):not(.codicon):not(.monaco-tokenized-source):not(.monaco-tokenized-source *){unicode-bidi:plaintext}
.antigravity-agent-side-panel p,
.antigravity-agent-side-panel li,
.antigravity-agent-side-panel h1,
.antigravity-agent-side-panel h2,
.antigravity-agent-side-panel h3,
.antigravity-agent-side-panel h4,
.antigravity-agent-side-panel blockquote,
.antigravity-agent-side-panel span:not(.codicon){direction:rtl;text-align:right}

/* === Jetski / Full-screen view RTL === */
.jetski-full-screen-view{direction:rtl!important;text-align:right!important}
.jetski-full-screen-view p,
.jetski-full-screen-view li,
.jetski-full-screen-view h1,
.jetski-full-screen-view h2,
.jetski-full-screen-view h3,
.jetski-full-screen-view h4,
.jetski-full-screen-view blockquote{direction:rtl;text-align:right;unicode-bidi:plaintext}
.jetski-custom-editor-pane{direction:rtl!important;text-align:right!important}

/* === Chat widget (inline chat) RTL === */
.chat-widget .rendered-markdown,
.chat-widget .rendered-markdown p,
.chat-widget .rendered-markdown li,
.chat-widget .rendered-markdown h1,
.chat-widget .rendered-markdown h2,
.chat-widget .rendered-markdown h3,
.chat-widget .rendered-markdown h4,
.chat-widget .rendered-markdown blockquote,
.chat-widget .rendered-markdown ul,
.chat-widget .rendered-markdown ol{direction:rtl;text-align:right;unicode-bidi:plaintext}

/* === EXCLUDE code blocks from RTL (stay LTR) === */
.interactive-item-container .rendered-markdown pre,
.interactive-item-container .rendered-markdown code,
.chat-widget .rendered-markdown pre,
.chat-widget .rendered-markdown code,
.antigravity-agent-side-panel pre,
.antigravity-agent-side-panel code,
.antigravity-agent-side-panel .monaco-tokenized-source,
.jetski-full-screen-view pre,
.jetski-full-screen-view code,
.jetski-custom-editor-pane pre,
.jetski-custom-editor-pane code{direction:ltr!important;text-align:left!important;unicode-bidi:normal!important}
"""

css += '\n' + RTL_CSS
print("  ✅ CSS")

# ==============================================================
# Error check
# ==============================================================
if errors:
    print(f"\n⛔ {len(errors)} أخطاء:")
    for e in errors:
        print(f"   • {e}")
    exit(1)

# ==============================================================
# Save & Copy
# ==============================================================
print("\n💾 حفظ ...")
with open(JS_TMP, 'w') as f:
    f.write(js)
with open(CSS_TMP, 'w') as f:
    f.write(css)
print(f"  JS → {JS_TMP} ({len(js):,})")
print(f"  CSS → {CSS_TMP} ({len(css):,})")

print("\n📦 نسخ ...")
ok = True
for src, dst in [(JS_TMP, JS_DEST), (CSS_TMP, CSS_DEST)]:
    try:
        subprocess.run(['cp', src, dst], check=True)
    except:
        ok = False

if not ok:
    print(f"\n👉 sudo cp {JS_TMP} '{JS_DEST}' && sudo cp {CSS_TMP} '{CSS_DEST}'")

print("\n" + "=" * 50)
print("🎉 RTL v9.0 — كل شي RTL")
print("=" * 50)
print("✨ كل الأسطر في .md ملفات RTL بغض النظر عن اللغة!")
print("📌 ملف .md → كل الأسطر RTL")
print("📌 عربي، إنجليزي، مخلوط — كله RTL")
print("📌 Chat + Manager → RTL كمان")
print("📌 بدون كشف تلقائي، بدون تعقيد!")
print("\n⚠️  Cmd+Q ثم أعد فتح Antigravity!")