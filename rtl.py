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
  sudo cp /tmp/jetskiAgent.main.js \
    /Applications/Antigravity.app/Contents/Resources/app/out/jetskiAgent/main.js
"""

import os
import subprocess

BACKUP_JS  = '/Users/kamel/k/save/plugins_backup/workbench.desktop.main.js.backup'
BACKUP_CSS = '/Users/kamel/k/save/plugins_backup/workbench.desktop.main.css.backup'
JS_TMP  = '/tmp/workbench.desktop.main.js'
# Paths
VSCODE_DIR = '/Applications/Antigravity.app/Contents/Resources/app/out/vs/workbench'
JS_DEST = os.path.join(VSCODE_DIR, 'workbench.desktop.main.js')
CSS_DEST = os.path.join(VSCODE_DIR, 'workbench.desktop.main.css')
MGR_JS_DEST = '/Applications/Antigravity.app/Contents/Resources/app/out/jetskiAgent/main.js'

JS_BACKUP = '/Users/kamel/k/save/plugins_backup/workbench.desktop.main.js.backup'
CSS_BACKUP = '/Users/kamel/k/save/plugins_backup/workbench.desktop.main.css.backup'
MGR_JS_BACKUP = '/Users/kamel/k/save/plugins_backup/jetskiAgent.main.js.backup'

JS_TMP = '/tmp/workbench.desktop.main.js'
CSS_TMP = '/tmp/workbench.desktop.main.css'
MGR_JS_TMP = '/tmp/jetskiAgent.main.js'

print("📖 قراءة النسخ الاحتياطية النظيفة...")
with open(JS_BACKUP, 'r') as f: js = f.read()
with open(CSS_BACKUP, 'r') as f: css = f.read()
with open(MGR_JS_BACKUP, 'r') as f: mgr_js = f.read()

print(f"  Workbench JS: {len(js):,} chars ✅")
print(f"  Workbench CSS: {len(css):,} chars ✅")
print(f"  Manager JS: {len(mgr_js):,} chars ✅")

errors = []

# ==============================================================
# MOD 1: True Native Bidi (Line-by-Line Direction)
# ==============================================================
print("\n🔧 [1/2] تعديل P() — الكشف الذكي عن الاتجاه (Native Bidi) ...")
OLD_P = 'return i>0?V6.RTL:V6.LTR}getTextDirection'
NEW_P = (
    'if(i>0)return V6.RTL;if(i<0)return V6.LTR;'
    'if(typeof window==="undefined"||!window._rtlDefault)return V6.LTR;'
    'var l=this.q.getLineContent(t);var ar=/[\\u0600-\\u06FF]/.test(l);return ar?V6.RTL:V6.LTR;'
    '}getTextDirection'
)

count_p = js.count(OLD_P)
if count_p == 1:
    js = js.replace(OLD_P, NEW_P)
    print("  ✅ P() — تم تفعيل الكشف الذكي (عربي=RTL، إنجليزي=LTR)")
else:
    errors.append(f"P() pattern: {count_p} (expected 1)")
    print(f"  ❌ {errors[-1]}")

# ==============================================================
# MOD 2: SCRIPT INJECTION (Add antigravity-rtl class to workbench)
# ==============================================================
print("\n🔧 [2/2] سكريبت إضافة كلاس الـ RTL ...")
SCRIPT = """
/* RTL INJECT V10 */
;(function(){
function _gf(){
  var e=document.querySelector('.monaco-editor.focused');if(!e)return null;
  var d=e.querySelector('.monaco-scrollable-element');
  return d?d.getAttribute('data-uri'):null;
}
var _ov={};
function sync(){
  var ed=document.querySelectorAll('.monaco-editor');
  for(var i=0;i<ed.length;i++){
    var d=ed[i].querySelector('.monaco-scrollable-element');
    var u=d?d.getAttribute('data-uri'):null;
    var isMd=u&&u.endsWith('.md');
    if(isMd){
      ed[i].classList.add('antigravity-rtl');
    }else{
      ed[i].classList.remove('antigravity-rtl');
    }
  }
}
function injectWebviews(){
  var w=document.querySelectorAll('webview');
  for(var i=0;i<w.length;i++){
    try{
      w[i].executeJavaScript("if(!document.getElementById('_rtl_inj')){var s=document.createElement('style');s.id='_rtl_inj';s.textContent='.interactive-session{direction:rtl;text-align:right} .interactive-item-container{direction:rtl;text-align:right} .interactive-item-container .header{direction:rtl;flex-direction:row-reverse} .interactive-item-container .value, .interactive-item-container .value .rendered-markdown, .interactive-item-container .value .rendered-markdown p, .interactive-item-container .value .rendered-markdown li, .interactive-item-container .value .rendered-markdown h1, .interactive-item-container .value .rendered-markdown h2, .interactive-item-container .value .rendered-markdown h3, .interactive-item-container .value .rendered-markdown h4, .interactive-item-container .value .rendered-markdown blockquote, .interactive-item-container .value .rendered-markdown ul, .interactive-item-container .value .rendered-markdown ol{direction:rtl;text-align:right;unicode-bidi:plaintext} .chat-input-container{direction:rtl;text-align:right} .interactive-input-part{direction:rtl}';document.head.appendChild(s);}");
    }catch(e){}
  }
}
setTimeout(function(){
  setInterval(sync,300);sync();
  setInterval(injectWebviews,1000);injectWebviews();
  console.log('🔄 RTL v10.0 — True Native Bidi')
},2000)
})();
"""
js += '\n' + SCRIPT
print("  ✅ سكريبت إضافة كلاس الـ RTL")

# ==============================================================
# CSS
# ==============================================================
RTL_CSS = """
/* ===== RTL v10.0 — True Native Bidi ===== */

/* === Editor RTL === */
.monaco-editor.antigravity-rtl .view-line[dir="rtl"] {
    text-align: right !important;
}
.monaco-editor.antigravity-rtl .view-line[dir="ltr"] {
    text-align: left !important;
}

/* === Fix: kill text-indent overflow on RTL wrapped lines === */
.view-line[dir="rtl"]>div[style*="text-indent"]{text-indent:0px!important}

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
.antigravity-agent-side-panel *:not(pre):not(code):not(.codicon):not(.monaco-tokenized-source):not(.monaco-tokenized-source *){direction:rtl!important;text-align:right!important;unicode-bidi:plaintext!important}
/* Override Tailwind text-align utilities inside agent panel */
.antigravity-agent-side-panel .text-left,
.antigravity-agent-side-panel .text-center,
.antigravity-agent-side-panel .text-start{text-align:right!important}
.antigravity-agent-side-panel .flex-row{flex-direction:row-reverse!important}

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

if errors:
    print(f"\n⛔ {len(errors)} أخطاء:")
    for e in errors:
        print(f"   • {e}")
    exit(1)

# ==============================================================
# Manager RTL
# ==============================================================
print("\n🔧 [3/3] Manager RTL — حقن CSS عبر JS ...")
MGR_RTL_SCRIPT = r"""
;/* MGR_RTL_V1 */(function(){
var s=document.createElement('style');
s.id='_mgr_rtl';
s.textContent='.leading-relaxed p,.leading-relaxed li,.leading-relaxed h1,.leading-relaxed h2,.leading-relaxed h3,.leading-relaxed h4,.leading-relaxed h5,.leading-relaxed h6,.leading-relaxed blockquote,.leading-relaxed td,.leading-relaxed th{unicode-bidi:plaintext!important;text-align:start!important}.leading-relaxed.select-text{unicode-bidi:plaintext!important;text-align:start!important}.leading-relaxed pre,.leading-relaxed code{direction:ltr!important;text-align:left!important;unicode-bidi:normal!important}textarea,[contenteditable]{unicode-bidi:plaintext!important}';
document.head.appendChild(s);
console.log('🔄 Manager RTL v1 — injected');
})();
"""
mgr_js += '\n' + MGR_RTL_SCRIPT
print("  ✅ Manager RTL CSS injected via JS")

# ==============================================================
# Save & Copy
# ==============================================================
print("\n💾 حفظ ...")
with open(JS_TMP, 'w') as f: f.write(js)
with open(CSS_TMP, 'w') as f: f.write(css)
with open(MGR_JS_TMP, 'w') as f: f.write(mgr_js)
print(f"  JS → {JS_TMP} ({len(js):,})")
print(f"  CSS → {CSS_TMP} ({len(css):,})")
print(f"  Manager JS → {MGR_JS_TMP} ({len(mgr_js):,})")

print("\n📦 نسخ ...")
ok = True
for src, dst in [(JS_TMP, JS_DEST), (CSS_TMP, CSS_DEST), (MGR_JS_TMP, MGR_JS_DEST)]:
    try: subprocess.run(['cp', src, dst], check=True)
    except: ok = False

if not ok:
    print(f"\n👉 sudo cp {JS_TMP} '{JS_DEST}' && sudo cp {CSS_TMP} '{CSS_DEST}' && sudo cp {MGR_JS_TMP} '{MGR_JS_DEST}'")

print("\n" + "=" * 50)
print("🎉 RTL v10.0 — True Native Bidi")
print("=" * 50)
print("✨ الأسطر العربية RTL / الأسطر الإنجليزية LTR")
print("📌 إحداثيات الماوس تعمل بنسبة 100%")
print("📌 الروابط تعمل بشكل طبيعي!")
print("\n⚠️  Cmd+Q ثم أعد فتح Antigravity!")