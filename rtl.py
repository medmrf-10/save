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
 * P() handles editor lines. This script handles chat inputs + responses. */
window._rtlDefault=false;
function sync(){
  var el=document.querySelector('.tab.active .label-name span');
  if(!el)el=document.querySelector('.tab.active .label-name');
  var f=el?el.textContent.replace(/[●•*◌]/g,'').trim():'';
  var l=f.toLowerCase();
  window._rtlDefault=(l.endsWith('.md')||l.endsWith('.markdown')||l.endsWith('.mdx'))
}
/* Patch chat inputs with dir="auto" HTML attribute (valid!) */
function patchChatInputs(){
  /* 1. Set dir="auto" on textareas and contenteditable (HTML attr IS valid) */
  var inputSels=[
    '.interactive-input-editor textarea',
    '.chat-input-container textarea',
    '.inline-chat-input textarea',
    '.chat-edit-input-container textarea',
    '.interactive-input-editor [contenteditable]',
    '.chat-input-container [contenteditable]',
    '.inline-chat-input [contenteditable]'
  ];
  inputSels.forEach(function(s){
    document.querySelectorAll(s).forEach(function(el){
      if(el.getAttribute('dir')!=='auto') el.setAttribute('dir','auto');
    })
  });
  /* 2. Patch view-lines inside chat input editors */
  var chatEditors=[
    '.interactive-input-editor .view-lines',
    '.interactive-input-editor .view-line',
    '.chat-input-container .view-lines',
    '.chat-input-container .view-line',
    '.inline-chat-input .view-lines',
    '.inline-chat-input .view-line',
    '.chat-edit-input-container .view-lines',
    '.chat-edit-input-container .view-line'
  ];
  chatEditors.forEach(function(s){
    document.querySelectorAll(s).forEach(function(el){
      if(!el.style.unicodeBidi||el.style.unicodeBidi!=='plaintext'){
        el.style.unicodeBidi='plaintext';
        el.style.textAlign='start';
      }
    })
  });
  /* 3. Patch chat response markdown with dir="auto" */
  var mdSels=[
    'chat-markdown-part',
    'chat-tool-invocation-part .rendered-markdown',
    'chat-terminal-content-part .rendered-markdown',
    '.interactive-item-container .rendered-markdown',
    '.chat-widget .rendered-markdown',
    '.inline-chat-widget .rendered-markdown',
    '.extension-editor .rendered-markdown'
  ];
  mdSels.forEach(function(s){
    document.querySelectorAll(s).forEach(function(el){
      if(el.getAttribute('dir')!=='auto') el.setAttribute('dir','auto');
      /* Also patch child paragraphs */
      el.querySelectorAll('p,li,h1,h2,h3,h4,blockquote,ul,ol,td,th').forEach(function(child){
        if(child.getAttribute('dir')!=='auto') child.setAttribute('dir','auto');
      });
    })
  });
}
setTimeout(function(){
  setInterval(sync,300);sync();
  /* Patch existing + watch for new chat elements */
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
/* NOTE: chat-markdown-part is a CUSTOM ELEMENT (tag), not a class!
   Use tag selector without dot. Also !important to override Tailwind. */
.view-line[dir="rtl"]{text-align:right}
.view-line[dir="rtl"]>span>span[style*="unicode-bidi"]{unicode-bidi:normal!important}

/* === Chat Response/Request RTL (Auto-detect per paragraph) === */
/* chat-markdown-part is a custom HTML element <chat-markdown-part> */
chat-markdown-part,
chat-markdown-part p,
chat-markdown-part li,
chat-markdown-part h1,
chat-markdown-part h2,
chat-markdown-part h3,
chat-markdown-part h4,
chat-markdown-part h5,
chat-markdown-part h6,
chat-markdown-part blockquote,
chat-markdown-part ul,
chat-markdown-part ol,
chat-markdown-part td,
chat-markdown-part th,
.interactive-item-container .rendered-markdown,
.interactive-item-container .rendered-markdown p,
.interactive-item-container .rendered-markdown li,
.interactive-item-container .rendered-markdown h1,
.interactive-item-container .rendered-markdown h2,
.interactive-item-container .rendered-markdown h3,
.interactive-item-container .rendered-markdown h4,
.interactive-item-container .rendered-markdown blockquote,
.interactive-item-container .rendered-markdown ul,
.interactive-item-container .rendered-markdown ol,
.chat-widget .rendered-markdown,
.chat-widget .rendered-markdown p,
.chat-widget .rendered-markdown li,
.chat-widget .rendered-markdown h1,
.chat-widget .rendered-markdown h2,
.chat-widget .rendered-markdown h3,
.chat-widget .rendered-markdown h4,
.chat-widget .rendered-markdown blockquote,
.chat-widget .rendered-markdown ul,
.chat-widget .rendered-markdown ol{unicode-bidi:plaintext!important;text-align:start!important}

/* === Chat Input RTL (typing area) === */
.interactive-input-editor .view-lines,
.interactive-input-editor .view-line,
.interactive-input-editor .view-line span,
.chat-input-container .monaco-editor .view-lines,
.chat-input-container .monaco-editor .view-line,
.chat-edit-input-container .monaco-editor .view-lines,
.chat-edit-input-container .monaco-editor .view-line{unicode-bidi:plaintext!important;text-align:start!important}

/* === Inline Chat RTL === */
.inline-chat-widget .rendered-markdown,
.inline-chat-widget .rendered-markdown p,
.inline-chat-widget .rendered-markdown li,
.inline-chat-input .monaco-editor .view-lines,
.inline-chat-input .monaco-editor .view-line{unicode-bidi:plaintext!important;text-align:start!important}

/* === Extension/Settings/Manager Editor RTL === */
.extension-editor .rendered-markdown,
.extension-editor .rendered-markdown p,
.extension-editor .rendered-markdown li,
.settings-editor .rendered-markdown,
.settings-editor .rendered-markdown p,
.settings-editor .rendered-markdown li{unicode-bidi:plaintext!important;text-align:start!important}

/* === Interactive Session (Notebook-style) === */
.interactive-session .rendered-markdown,
.interactive-session .rendered-markdown p,
.interactive-request .rendered-markdown,
.interactive-request .rendered-markdown p,
.interactive-response .rendered-markdown,
.interactive-response .rendered-markdown p{unicode-bidi:plaintext!important;text-align:start!important}

/* === Other chat custom elements === */
chat-tool-invocation-part .rendered-markdown,
chat-tool-invocation-part .rendered-markdown p,
chat-terminal-content-part .rendered-markdown,
chat-terminal-content-part .rendered-markdown p{unicode-bidi:plaintext!important;text-align:start!important}

/* === Keep code blocks LTR everywhere === */
chat-markdown-part pre,
chat-markdown-part code,
.rendered-markdown pre,
.rendered-markdown code,
chat-tool-invocation-part pre,
chat-tool-invocation-part code,
chat-terminal-content-part pre,
chat-terminal-content-part code{direction:ltr!important;text-align:left!important;unicode-bidi:normal!important}
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