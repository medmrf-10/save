#!/usr/bin/env python3
"""
RTL Support for Antigravity v8.3 — Chat + Manager RTL
=========================================================
Auto-detect direction per line based on content:
- First Arabic char → RTL
- First Latin char → LTR
- Empty/neutral → RTL (default for .md)

NO per-line map, NO Cmd+;, NO Enter inheritance, NO localStorage.
Just works.

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
print("\n🔧 [1/3] تعديل P() — الكشف التلقائي ...")

OLD_P = 'return i>0?IL.RTL:IL.LTR}getTextDirection'

# Auto-detect logic:
# 1. Decorations override everything (original behavior)
# 2. For .md files: scan line content for first strong directional char
#    - Arabic/Hebrew → RTL
#    - Latin → LTR  
#    - Empty/neutral-only → RTL (default for .md)
# 3. For non-.md files: LTR
# Uses this.m.getViewLineData(t).content to get the actual line content

NEW_P = (
    'if(i>0)return IL.RTL;if(i<0)return IL.LTR;'
    'if(typeof window==="undefined"||!window._rtlDefault)return IL.LTR;'
    'try{'
    'var _c=this.m.getViewLineData(t).content;'
    'for(var _j=0;_j<_c.length;_j++){'
    'var _h=_c.charCodeAt(_j);'
    'if(_h>=0x600&&_h<=0x6FF||_h>=0x750&&_h<=0x77F||_h>=0x8A0&&_h<=0x8FF'
    '||_h>=0xFB50&&_h<=0xFDFF||_h>=0xFE70&&_h<=0xFEFF||_h>=0x590&&_h<=0x5FF)'
    'return IL.RTL;'
    'if(_h>=0x41&&_h<=0x5A||_h>=0x61&&_h<=0x7A)return IL.LTR'
    '}'
    'return IL.RTL'
    '}catch(_x){return IL.RTL}'
    '}getTextDirection'
)

count = js.count(OLD_P)
if count == 1:
    js = js.replace(OLD_P, NEW_P)
    print("  ✅ P() — كشف تلقائي من محتوى السطر")
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
;/* RTL_V83_CHAT */(function(){
/* RTL v8.3 — Auto-detect for editor + Chat/Manager RTL support.
 * P() handles editor lines. This script handles chat inputs. */
window._rtlDefault=false;
function sync(){
  var el=document.querySelector('.tab.active .label-name span');
  if(!el)el=document.querySelector('.tab.active .label-name');
  var f=el?el.textContent.replace(/[●•*◌]/g,'').trim():'';
  var l=f.toLowerCase();
  window._rtlDefault=(l.endsWith('.md')||l.endsWith('.markdown')||l.endsWith('.mdx'))
}
/* MutationObserver: set dir="auto" on chat input textareas & contenteditable */
function patchChatInputs(){
  var sels=[
    '.interactive-input-editor textarea',
    '.chat-input-container textarea',
    '.inline-chat-input textarea',
    '.chat-edit-input-container textarea',
    '.interactive-input-editor [contenteditable]',
    '.chat-input-container [contenteditable]',
    '.inline-chat-input [contenteditable]'
  ];
  sels.forEach(function(s){
    document.querySelectorAll(s).forEach(function(el){
      if(el.getAttribute('dir')!=='auto') el.setAttribute('dir','auto');
    })
  });
  /* Also patch .view-lines inside chat editors */
  var chatEditors=[
    '.interactive-input-editor .view-lines',
    '.chat-input-container .view-lines',
    '.inline-chat-input .view-lines',
    '.chat-edit-input-container .view-lines'
  ];
  chatEditors.forEach(function(s){
    document.querySelectorAll(s).forEach(function(el){
      if(el.style.direction!=='auto'){
        el.style.direction='auto';
        el.style.unicodeBidi='plaintext';
      }
    })
  });
}
setTimeout(function(){
  setInterval(sync,300);sync();
  /* Patch existing + watch for new chat inputs */
  patchChatInputs();
  var obs=new MutationObserver(function(){patchChatInputs()});
  obs.observe(document.body,{childList:true,subtree:true});
  console.log('🔄 RTL v8.3 — auto-detect for editor + chat/manager')
},2000)
})();
"""

js += '\n' + SCRIPT
print("  ✅ سكريبت مبسّط (كشف الملف فقط — 10 أسطر!)")

# ==============================================================
# CSS
# ==============================================================
RTL_CSS = """
/* ===== RTL v8.3 — Chat + Manager + Auto-detect ===== */
.view-line[dir="rtl"]{text-align:right}
.view-line[dir="rtl"]>span>span[style*="unicode-bidi"]{unicode-bidi:normal!important}

/* === Chat Response/Request RTL (Auto-detect per paragraph) === */
.interactive-item-container .rendered-markdown,
.interactive-item-container .rendered-markdown p,
.interactive-item-container .rendered-markdown li,
.interactive-item-container .rendered-markdown h1,
.interactive-item-container .rendered-markdown h2,
.interactive-item-container .rendered-markdown h3,
.interactive-item-container .rendered-markdown h4,
.interactive-item-container .rendered-markdown h5,
.interactive-item-container .rendered-markdown h6,
.interactive-item-container .rendered-markdown blockquote,
.interactive-item-container .rendered-markdown ul,
.interactive-item-container .rendered-markdown ol,
.interactive-item-container .rendered-markdown td,
.interactive-item-container .rendered-markdown th,
.chat-widget .rendered-markdown,
.chat-widget .rendered-markdown p,
.chat-widget .rendered-markdown li,
.chat-widget .rendered-markdown h1,
.chat-widget .rendered-markdown h2,
.chat-widget .rendered-markdown h3,
.chat-widget .rendered-markdown h4,
.chat-widget .rendered-markdown h5,
.chat-widget .rendered-markdown h6,
.chat-widget .rendered-markdown blockquote,
.chat-widget .rendered-markdown ul,
.chat-widget .rendered-markdown ol,
.chat-widget .rendered-markdown td,
.chat-widget .rendered-markdown th{direction:auto;text-align:start;unicode-bidi:plaintext}

/* === Chat Input RTL (typing area) === */
.interactive-input-editor .view-lines,
.interactive-input-editor .view-line,
.chat-input-container .monaco-editor .view-lines,
.chat-input-container .monaco-editor .view-line,
.chat-edit-input-container .monaco-editor .view-lines,
.chat-edit-input-container .monaco-editor .view-line{direction:auto;unicode-bidi:plaintext;text-align:start}

/* === Inline Chat RTL === */
.inline-chat-widget .rendered-markdown,
.inline-chat-widget .rendered-markdown p,
.inline-chat-widget .rendered-markdown li,
.inline-chat-widget .rendered-markdown h1,
.inline-chat-widget .rendered-markdown h2,
.inline-chat-widget .rendered-markdown h3,
.inline-chat-widget .rendered-markdown h4,
.inline-chat-input .monaco-editor .view-lines,
.inline-chat-input .monaco-editor .view-line{direction:auto;unicode-bidi:plaintext;text-align:start}

/* === Extension/Settings/Manager Editor RTL === */
.extension-editor .rendered-markdown,
.extension-editor .rendered-markdown p,
.extension-editor .rendered-markdown li,
.extension-editor .rendered-markdown h1,
.extension-editor .rendered-markdown h2,
.extension-editor .rendered-markdown h3,
.extension-editor .rendered-markdown h4,
.settings-editor .rendered-markdown,
.settings-editor .rendered-markdown p,
.settings-editor .rendered-markdown li{direction:auto;unicode-bidi:plaintext;text-align:start}

/* === Interactive Session (Notebook-style) === */
.interactive-session .rendered-markdown,
.interactive-session .rendered-markdown p,
.interactive-session .rendered-markdown li,
.interactive-request .rendered-markdown,
.interactive-request .rendered-markdown p,
.interactive-response .rendered-markdown,
.interactive-response .rendered-markdown p{direction:auto;unicode-bidi:plaintext;text-align:start}

/* === Keep code blocks LTR everywhere === */
.rendered-markdown pre,
.rendered-markdown code,
.interactive-item-container .rendered-markdown pre,
.interactive-item-container .rendered-markdown code,
.chat-widget .rendered-markdown pre,
.chat-widget .rendered-markdown code,
.inline-chat-widget .rendered-markdown pre,
.inline-chat-widget .rendered-markdown code,
.extension-editor .rendered-markdown pre,
.extension-editor .rendered-markdown code{direction:ltr!important;text-align:left!important;unicode-bidi:normal!important}
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
print("🎉 RTL v8.3 — Chat + Manager + المحرر")
print("=" * 50)
print("✨ كل سطر يكتشف اتجاهه تلقائياً من محتواه!")
print("📌 حرف عربي أول → RTL")
print("📌 حرف لاتيني أول → LTR")
print("📌 Chat Input + Responses — unicode-bidi:plaintext")
print("📌 Inline Chat + Manager Editor — مدعوم")
print("📌 Code blocks — دائماً LTR")
print("\n⚠️  Cmd+Q ثم أعد فتح Antigravity!")