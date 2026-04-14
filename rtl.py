#!/usr/bin/env python3
"""
RTL Support for Antigravity v8.2 — The Radical Solution
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
print("\n🔧 [1/4] تعديل P() — الكشف التلقائي ...")

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
print("\n🔧 [2/4] تعديل XLl (التفاف الأسطر) ...")

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
# MOD 3: Fix arrow keys — remove RTL direction swap
# ==============================================================
print("\n🔧 [3/4] إصلاح الأسهم المعكوسة ...")

OLD_ARROW_L = 'o?G0.moveRight(t.cursorConfig,t,s.viewState,i,n):G0.moveLeft(t.cursorConfig,t,s.viewState,i,n)'
NEW_ARROW_L = 'G0.moveLeft(t.cursorConfig,t,s.viewState,i,n)'

OLD_ARROW_R = 'o?G0.moveLeft(t.cursorConfig,t,s.viewState,i,n):G0.moveRight(t.cursorConfig,t,s.viewState,i,n)'
NEW_ARROW_R = 'G0.moveRight(t.cursorConfig,t,s.viewState,i,n)'

for label, old, new in [("سهم يسار", OLD_ARROW_L, NEW_ARROW_L), ("سهم يمين", OLD_ARROW_R, NEW_ARROW_R)]:
    c = js.count(old)
    if c == 1:
        js = js.replace(old, new)
        print(f"  ✅ {label}")
    else:
        errors.append(f"{label}: {c} (expected 1)")
        print(f"  ❌ {errors[-1]}")

# ==============================================================
# MOD 4: Minimal control script (just file detection!)
# ==============================================================
print("\n🔧 [4/4] سكريبت كشف الملف (مبسّط!) ...")

SCRIPT = r"""
;/* RTL_V82 */(function(){
/* RTL v8.2 — Auto-detect. Just set _rtlDefault based on file type.
 * P() handles everything else by reading line content. */
window._rtlDefault=false;
function sync(){
  var el=document.querySelector('.tab.active .label-name span')||document.querySelector('.tab.active .label-name');
  var l=el?el.textContent.replace(/[●•*◌]/g,'').trim().toLowerCase():'';
  var isM=(l.endsWith('.md')||l.endsWith('.markdown')||l.endsWith('.mdx'));
  var isA=(l==='chat'||l==='composer'||l==='ai'||l==='manager'||l==='ai manager');
  var isV=!!document.querySelector('.chat-widget, .composer-editor, .interactive-input');
  if(isM||isA||isV)window._rtlDefault=true;
  else if(l&&!isM)window._rtlDefault=false;
}
setTimeout(function(){
  setInterval(sync,300);sync();
  console.log('🔄 RTL v8.2 — auto-detect direction per line')
},2000)
})();
"""

js += '\n' + SCRIPT
print("  ✅ سكريبت مبسّط (كشف الملف فقط — 10 أسطر!)")

# ==============================================================
# CSS
# ==============================================================
RTL_CSS = """
/* ===== RTL v8.2 ===== */
.view-line[dir="rtl"]{text-align:right}
.view-line[dir="rtl"]>span>span[style*="unicode-bidi"]{unicode-bidi:normal!important}

/* Chat & AI RTL */
.interactive-item-container .rendered-markdown, .interactive-item-container .rendered-markdown p, .interactive-item-container .rendered-markdown li, .interactive-item-container .rendered-markdown h1, .interactive-item-container .rendered-markdown h2, .interactive-item-container .rendered-markdown h3, .interactive-item-container .rendered-markdown h4, .interactive-item-container .rendered-markdown blockquote, .interactive-item-container .rendered-markdown ul, .interactive-item-container .rendered-markdown ol, .chat-widget .rendered-markdown, .chat-widget .rendered-markdown p, .chat-widget .rendered-markdown li, .chat-widget .rendered-markdown h1, .chat-widget .rendered-markdown h2, .chat-widget .rendered-markdown h3, .chat-widget .rendered-markdown h4, .chat-widget .rendered-markdown blockquote, .chat-widget .rendered-markdown ul, .chat-widget .rendered-markdown ol, .composer-editor .rendered-markdown, .composer-editor .rendered-markdown p, .composer-editor .rendered-markdown li, .composer-editor .rendered-markdown h1, .composer-editor .rendered-markdown h2, .composer-editor .rendered-markdown h3, .composer-editor .rendered-markdown h4, .composer-editor .rendered-markdown blockquote, .composer-editor .rendered-markdown ul, .composer-editor .rendered-markdown ol { direction: rtl; text-align: right; unicode-bidi: plaintext; }
.interactive-item-container .rendered-markdown pre, .interactive-item-container .rendered-markdown code, .chat-widget .rendered-markdown pre, .chat-widget .rendered-markdown code, .composer-editor .rendered-markdown pre, .composer-editor .rendered-markdown code, .interactive-input pre, .interactive-input code { direction: ltr; text-align: left; unicode-bidi: normal; }
.chat-widget textarea, .chat-widget input, .composer-editor textarea, .composer-editor input, .interactive-input textarea, .interactive-input input { unicode-bidi: plaintext !important; }
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
print("🎉 RTL v8.2 — الحل الجذري")
print("=" * 50)
print("✨ كل سطر يكتشف اتجاهه تلقائياً من محتواه!")
print("📌 حرف عربي أول → RTL")
print("📌 حرف لاتيني أول → LTR")
print("📌 سطر فاضي → RTL (في .md)")
print("📌 بدون Cmd+;, بدون وراثة, بدون تخزين!")
print("📌 الأسهم تتحرك بصرياً")
print("\n⚠️  Cmd+Q ثم أعد فتح Antigravity!")