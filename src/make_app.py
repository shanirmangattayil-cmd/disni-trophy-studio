"""Builds the phone-app version of Disni Trophy Studio from the artifact source."""
import json, re, sys
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, 'disni_src.html')
s = open(SRC).read()

def rep(a, b, cnt=1):
    global s
    n = s.count(a)
    assert n == cnt, (n, a[:90])
    s = s.replace(a, b)

def sub(pat, b):
    global s
    s2, n = re.subn(pat, lambda m: b, s, count=1, flags=re.S)
    assert n == 1, pat[:70]
    s = s2

REPO = 'shanirmangattayil-cmd/disni-trophy-studio'

# ---------- document shell ----------
rep('<title>Disni Trophy Studio</title>\n<meta name="claude:viewport-fit-sides" content="cover">',
'''<!doctype html><html lang="ml"><head><meta charset="utf-8">
<meta name="disni-web-version" content="__WEBVER__">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#7a0716">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<title>Disni Trophies</title>''')
rep('<style>\n/* Layout:', '<style>\n:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font-size:14px}img{max-width:100%}[hidden]{display:none!important}*{-webkit-tap-highlight-color:transparent}\n/* Layout:')
rep('</style>\n\n<div class="wrap">', '''</style></head><body>

<div class="wrap">''')
s = s.rstrip() + '\n</body></html>\n'

# ---------- cover + owner ----------
rep('''  <header class="brand">
    <img id="logo" alt="Disni logo">
    <div><h1>Disni Trophies</h1><small>Design Studio</small></div>
  </header>''', '''  <div class="updbar" id="updBar" hidden><span>പുതിയ version ready</span><button class="btn sm primary" id="updBtn">Update</button></div>
  <header class="cover">
    <img class="cover-logo logo-img" alt="Disni logo">
    <div class="cover-t"><h1>Disni Trophies</h1><small>Design Studio</small></div>
    <div class="owner"><img class="owner-img" alt="Owner Befil"><span class="owner-l">Owner</span><b>Befil</b></div>
  </header>''')
rep("document.getElementById('logo').src = IMG.logo;", "document.querySelectorAll('.logo-img').forEach(i=>i.src=IMG.logo); document.querySelectorAll('.owner-img').forEach(i=>i.src=IMG.owner);")
rep('@media (prefers-reduced-motion:reduce)', '''/* app: cover, owner, auth, update bar */
.cover{position:relative;display:flex;align-items:center;gap:14px;margin:12px 0 16px;padding:16px 14px;border-radius:22px;overflow:hidden;border:1px solid var(--line-2);
  background:repeating-conic-gradient(from 0deg at 22% 50%,rgba(255,214,120,.10) 0deg 5deg,transparent 5deg 12deg),radial-gradient(120% 140% at 20% 50%,#e01a3a,#8c0a1d 55%,#4a0914);box-shadow:0 14px 34px rgba(0,0,0,.35)}
.cover-logo{width:86px;height:86px;border-radius:50%;flex:none;box-shadow:0 0 0 2px var(--gold),0 0 0 6px rgba(246,206,116,.18),0 10px 26px rgba(0,0,0,.45)}
.cover-t{min-width:0;flex:1}
.cover h1{margin:0;font-family:var(--f-brand);font-weight:800;font-size:28px;line-height:.95;letter-spacing:.03em;text-transform:uppercase;font-style:italic;background:var(--gold-grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.cover small{display:block;color:var(--gold-hi);opacity:.85;font-size:11px;letter-spacing:.24em;text-transform:uppercase;margin-top:5px}
.owner{position:absolute;top:10px;right:10px;display:flex;flex-direction:column;align-items:center;gap:1px}
.owner img{width:50px;height:50px;border-radius:50%;box-shadow:0 0 0 2px var(--gold),0 6px 14px rgba(0,0,0,.45)}
.owner-l{font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-hi);margin-top:4px}
.owner b{font-family:var(--f-brand);font-size:15px;line-height:1;color:#fff;letter-spacing:.04em}
@media (max-width:380px){.cover-logo{width:70px;height:70px}.cover h1{font-size:23px}.owner img{width:42px;height:42px}}
.cover .cover-t{padding-right:64px}
.updbar{display:flex;align-items:center;gap:10px;justify-content:space-between;margin-top:10px;padding:8px 10px 8px 14px;border-radius:14px;background:rgba(37,211,102,.12);border:1px solid rgba(37,211,102,.5);font-weight:700;font-size:13.5px}
.auth{position:fixed;inset:0;z-index:80;overflow:auto;display:flex;align-items:flex-start;justify-content:center;
  background:repeating-conic-gradient(from 0deg at 50% 26%,rgba(255,214,120,.08) 0deg 5deg,transparent 5deg 12deg),radial-gradient(120% 80% at 50% 20%,#d0142f,#7a0716 50%,#3a0610);
  padding:calc(36px + env(safe-area-inset-top,0px)) max(20px,env(safe-area-inset-left,0px)) 30px max(20px,env(safe-area-inset-right,0px))}
.auth .box{width:100%;max-width:400px;display:flex;flex-direction:column;align-items:center;gap:14px}
.auth .big{width:140px;height:140px;border-radius:50%;box-shadow:0 0 0 3px var(--gold),0 0 0 10px rgba(246,206,116,.15),0 20px 50px rgba(0,0,0,.5)}
.auth h1{margin:6px 0 0;font-family:var(--f-brand);font-weight:800;font-size:36px;font-style:italic;text-transform:uppercase;letter-spacing:.03em;background:var(--gold-grad);-webkit-background-clip:text;background-clip:text;color:transparent;line-height:1}
.auth .tag2{color:var(--gold-hi);font-size:11.5px;letter-spacing:.26em;text-transform:uppercase;margin-top:-6px}
.auth form{width:100%;display:flex;flex-direction:column;gap:12px;background:rgba(43,4,12,.55);border:1px solid var(--line-2);border-radius:20px;padding:16px;backdrop-filter:blur(6px)}
.auth .seg{grid-template-columns:1fr 1fr;margin:0}
.auth .msg{min-height:18px;font-size:13px;color:var(--gold-hi);text-align:center}
.auth .owner-row{display:flex;align-items:center;gap:10px;margin-top:4px}
.auth .owner-row img{width:42px;height:42px;border-radius:50%;box-shadow:0 0 0 2px var(--gold)}
.auth .owner-row small{display:block;font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-hi)}
.auth .owner-row b{font-family:var(--f-brand);font-size:17px}
.acct{display:flex;align-items:center;gap:10px;background:var(--well);border:1px solid var(--line);border-radius:14px;padding:9px 10px;margin-bottom:6px}
.acct .t{flex:1;min-width:0}.acct .t b{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.acct small{color:var(--muted)}
.bgbtn{display:flex;align-items:center;gap:10px;width:100%;border:1px solid var(--gold);background:linear-gradient(180deg,rgba(246,206,116,.16),rgba(246,206,116,.04));border-radius:12px;padding:10px 12px;text-align:left}
.bgbtn svg{width:24px;height:24px;color:var(--gold);flex:none}
.bgbtn b{display:block;font-size:14px}.bgbtn small{color:var(--muted);font-size:12px}
@media (prefers-reduced-motion:reduce)''')

# ---------- sign-in screen ----------
rep('<div id="sheetRoot"></div>', '''<div id="sheetRoot"></div>

<div class="auth" id="auth" hidden>
  <div class="box">
    <img class="big logo-img" alt="Disni logo">
    <h1>Disni Trophies</h1>
    <div class="tag2">Design Studio</div>
    <form id="authForm" autocomplete="on">
      <div class="seg" id="authSeg"><button type="button" data-m="in" aria-selected="true">Sign in</button><button type="button" data-m="up">Create account</button></div>
      <label class="f" id="aNameWrap" hidden>പേര് · Name <input class="inp" id="aName" autocomplete="name" placeholder="ഉദാ: Befil"></label>
      <label class="f">Email <input class="inp" id="aEmail" type="email" autocomplete="email" inputmode="email" placeholder="name@gmail.com" required></label>
      <label class="f">Password <input class="inp" id="aPass" type="password" autocomplete="current-password" placeholder="കുറഞ്ഞത് 4 അക്ഷരം" required></label>
      <button class="btn primary" id="aGo" type="submit">Sign in</button>
      <div class="msg" id="aMsg"></div>
      <button class="btn ghost sm" type="button" id="aForgot">Password മറന്നോ?</button>
    </form>
    <div class="owner-row"><img class="owner-img" alt=""><div><small>Owner</small><b>Befil</b></div></div>
  </div>
</div>''')

# ---------- account box in Saved tab ----------
rep('''    <p class="eyebrow">Library</p>
    <h2>Saved Designs</h2>''', '''    <div class="acct"><span class="avatar" id="acctAv">D</span><div class="t"><b id="acctName"></b><small id="acctEmail"></small></div><button class="btn sm" id="signOut">Sign out</button></div>
    <p class="eyebrow" style="margin-top:16px">Library</p>
    <h2>Saved Designs</h2>''')

# ---------- per-account storage ----------
rep("    async get(k){ const db=await open(); if(!db) return mem[k];", "    async get(k){ k=NS+k; const db=await open(); if(!db) return mem[k];")
rep("    async set(k,v){ mem[k]=v; const db=await open();", "    async set(k,v){ if(['models','designs','contacts'].includes(k)) scheduleBackup(); k=NS+k; mem[k]=v; const db=await open();")
rep("const store = (() => {", "let NS='';\nconst store = (() => {")

# ---------- boot: wait for sign-in ----------
sub(r"/\* ---------- boot ---------- \*/\n\(async\(\)=>\{\n  models = sampleModels\(\); renderModels\(\);(.*?)\n\}\)\(\);",
r'''/* ---------- boot ---------- */
async function loadUser(){
  models = sampleModels(); designs=[]; contacts=[]; cur=null; renderModels();\g<1>
  go('models');
}''')
s = s.replace(r'\g<1>', '')  # safety
# re-insert the original body (re.sub with lambda kept literal \g<1>) -> do it properly
m = re.search(r"async function loadUser\(\)\{\n  models = sampleModels\(\); designs=\[\]; contacts=\[\]; cur=null; renderModels\(\);\n  go\('models'\);\n\}", s)
orig = open(SRC).read()
body = re.search(r"/\* ---------- boot ---------- \*/\n\(async\(\)=>\{\n  models = sampleModels\(\); renderModels\(\);(.*?)\n\}\)\(\);", orig, re.S).group(1)
s = s[:m.start()] + "async function loadUser(){\n  models = sampleModels(); designs=[]; contacts=[]; cur=null; renderModels();" + body + "\n  go('models');\n}" + s[m.end():]

s = s.replace("</script>\n</body></html>", r'''
/* ---------- app platform: phone bridge, accounts, backup, updates ---------- */
const NATIVE = window.DisniNative || null;
const REPO = '__REPO__';
const APK_URL = `https://github.com/${REPO}/releases/latest/download/Disni-Trophies.apk`;

function blobToB64(blob){ return new Promise(res=>{ const r=new FileReader(); r.onload=()=>res(String(r.result).split(',')[1]); r.readAsDataURL(blob); }); }

// accounts (kept on this phone; each email has its own models, designs and contacts)
let USER=null;
const accounts = ()=>{ try{ return JSON.parse(localStorage.getItem('disni-accounts')||'{}'); }catch(e){ return {}; } };
async function hashPw(email,pw,salt){
  const txt=salt+'|'+email+'|'+pw;
  if(window.crypto&&crypto.subtle){ const h=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(txt)); return [...new Uint8Array(h)].map(b=>b.toString(16).padStart(2,'0')).join(''); }
  let h=5381; for(const c of txt) h=((h<<5)+h+c.charCodeAt(0))|0; return 'x'+(h>>>0).toString(16);
}
let authMode='in';
function setAuthMode(m){ authMode=m; document.querySelectorAll('#authSeg button').forEach(b=>b.setAttribute('aria-selected',b.dataset.m===m));
  $('aNameWrap').hidden = m!=='up'; $('aGo').textContent = m==='up'?'Account ഉണ്ടാക്കൂ':'Sign in'; $('aPass').autocomplete = m==='up'?'new-password':'current-password'; $('aMsg').textContent=''; }
$('authSeg').onclick=e=>{ const b=e.target.closest('button'); if(b) setAuthMode(b.dataset.m); };
$('aForgot').onclick=()=>{ $('aMsg').textContent='Account ഈ phone-ൽ ആണ്. Password മറന്നാൽ പുതിയ account ഉണ്ടാക്കി "Backup restore" വഴി data തിരികെ ചേർക്കൂ (Download › Disni Trophies-ൽ backup ഉണ്ട്).'; };
$('authForm').addEventListener('submit',async e=>{
  e.preventDefault();
  const email=$('aEmail').value.trim().toLowerCase(), pw=$('aPass').value, name=$('aName').value.trim();
  if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)){ $('aMsg').textContent='ശരിയായ email നൽകൂ'; return; }
  if(pw.length<4){ $('aMsg').textContent='Password കുറഞ്ഞത് 4 അക്ഷരം വേണം'; return; }
  const acc=accounts();
  if(authMode==='up'){
    if(acc[email]){ $('aMsg').textContent='ഈ email-ന് account ഉണ്ട് — Sign in ചെയ്യൂ'; setAuthMode('in'); return; }
    const salt=Math.random().toString(36).slice(2); acc[email]={salt,hash:await hashPw(email,pw,salt),name:name||email.split('@')[0],created:Date.now()};
    try{ localStorage.setItem('disni-accounts',JSON.stringify(acc)); }catch(err){}
  } else {
    const a=acc[email];
    if(!a){ $('aMsg').textContent='ഈ email-ന് account ഇല്ല — "Create account" അമർത്തൂ'; return; }
    if(await hashPw(email,pw,a.salt)!==a.hash){ $('aMsg').textContent='Password തെറ്റാണ്'; return; }
  }
  signIn(email);
});
function signIn(email){
  USER=email; NS=email+':'; try{ localStorage.setItem('disni-session',email); }catch(e){}
  const a=accounts()[email]||{}; $('acctName').textContent=a.name||email; $('acctEmail').textContent=email; $('acctAv').textContent=(a.name||email)[0].toUpperCase();
  $('auth').hidden=true; $('aPass').value='';
  loadUser();
}
$('signOut').onclick=()=>{ try{ localStorage.removeItem('disni-session'); }catch(e){} USER=null; NS=''; $('auth').hidden=false; setAuthMode('in'); window.scrollTo(0,0); };

// automatic backup to Download/Disni Trophies (phone app)
let backupT=null;
function scheduleBackup(){ if(!NATIVE||!USER) return; clearTimeout(backupT); backupT=setTimeout(()=>{
  try{ NATIVE.saveText(`disni-backup-${USER.replace(/[^\w.@-]/g,'_')}.json`, JSON.stringify({app:'disni-studio',v:2,user:USER,saved:new Date().toISOString(),models,designs,contacts})); }catch(e){}
},2500); }

// saving files: phone app -> Pictures/Download "Disni Trophies"; browser -> normal download
saveFile = async function(filename,data,previewURL){
  if(NATIVE){
    const ok = /\.png$/i.test(filename) ? NATIVE.saveImage(filename, await blobToB64(data)) : NATIVE.saveText(filename, typeof data==='string'?data:await data.text());
    toast(ok ? (/\.png$/i.test(filename)?'Gallery › Pictures › Disni Trophies-ൽ save ചെയ്തു':'Download › Disni Trophies-ൽ save ചെയ്തു') : 'Save ചെയ്യാൻ പറ്റിയില്ല');
    return ok;
  }
  const blob = data instanceof Blob ? data : new Blob([data],{type:'application/json'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=filename; document.body.appendChild(a); a.click(); setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},4000);
  toast('Download ചെയ്തു'); return true;
};

// voice: phone app uses Android speech input (any language)
let voiceTarget=null, voiceBtn=null;
window.disniVoice = t=>{ if(voiceBtn) voiceBtn.classList.remove('on'); if(t&&voiceTarget){ const base=voiceTarget.value.trim(); voiceTarget.value=(base?base+' ':'')+t; voiceTarget.dispatchEvent(new Event('input',{bubbles:true})); toast('Voice ചേർത്തു'); } else if(t===null) toast('ഒന്നും കേട്ടില്ല — വീണ്ടും mic അമർത്തൂ'); voiceTarget=null; };
if(NATIVE){ const webListen=listen; listen = function(btn){ voiceTarget=$(btn.dataset.for); voiceBtn=btn; if(!voiceTarget) return; btn.classList.add('on'); NATIVE.voice(speechLang); }; }

// WhatsApp: phone app sends the design image + message straight into the chat
let waApp=null;
function designB64(){ return printCanvas().toDataURL('image/png').split(',')[1]; }
async function nativeShare(num){
  await Promise.all(cur.layers.filter(l=>l.type==='image').map(l=>{ const im=getImg(l.src); return im.decode?im.decode().catch(()=>{}):null; }));
  const msg=$('sMsg')?$('sMsg').value:'';
  const apps=(NATIVE.waApps()||'').split(',').filter(Boolean);
  const app = waApp && apps.includes(waApp) ? waApp : (apps[0]||'');
  if(!NATIVE.shareWhatsApp(app,num||'',msg,fileName(),designB64())) toast('WhatsApp തുറക്കാൻ പറ്റിയില്ല');
}
window.disniContact = j=>{ if(!j) return; try{ const c=JSON.parse(j); const n=normNum(c.num); if(n.length<11){ toast('ഈ contact-ന് ശരിയായ number ഇല്ല'); return; }
  addContact(c.name,n); if($('sNum')){ $('sNum').value=c.num; $('sName').value=c.name; $('sNum').dispatchEvent(new Event('input')); } renderContacts(); toast(c.name+' ചേർത്തു'); }catch(e){} };
const webSendSheet = sendSheet;
sendSheet = function(){
  webSendSheet();
  if(!NATIVE) return;
  const sheet=document.querySelector('#sheetRoot .sheet'); if(!sheet) return;
  const steps=sheet.querySelectorAll('.step');
  steps[1].hidden=true; steps[3].hidden=true;            // image goes with the message automatically
  steps[2].querySelector('.n').textContent='2';
  const apps=(NATIVE.waApps()||'').split(',').filter(Boolean);
  const body=steps[2].querySelector('.body');
  const tools=document.createElement('div'); tools.className='fields'; tools.style.gap='8px';
  tools.innerHTML = (apps.length>1?`<div class="chips" id="waApps">${apps.map(a=>`<button class="chip h" data-a="${a}" aria-pressed="${a===(waApp||apps[0])}">${a==='w4b'?'WhatsApp Business':'WhatsApp'}</button>`).join('')}</div>`:'')+
    (apps.length?'':'<p style="color:var(--danger)">ഈ phone-ൽ WhatsApp കാണുന്നില്ല — share list തുറക്കും.</p>')+
    `<button class="btn" id="sPhoneContact" type="button"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/></svg>Phone contacts-ൽ നിന്ന് തിരഞ്ഞെടുക്കൂ</button>`;
  body.insertBefore(tools, body.children[1]);
  body.querySelector('h3').textContent='ആർക്ക് അയക്കണം? (design image ഒപ്പം പോകും)';
  sheet.querySelector('#sPick').textContent='WhatsApp-ൽ contact / group തിരഞ്ഞെടുക്കൂ';
  $('sPhoneContact').onclick=()=>NATIVE.pickContact();
  const wa=sheet.querySelector('#waApps'); if(wa) wa.onclick=e=>{ const b=e.target.closest('button'); if(!b) return; waApp=b.dataset.a; wa.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',x===b)); };
  sheet.addEventListener('click',e=>{ const a=e.target.closest('a[href^="https://wa.me"]'); if(!a) return; e.preventDefault(); e.stopImmediatePropagation();
    const m=a.getAttribute('href').match(/wa\.me\/(\d*)/); const num=m?m[1]:'';
    if(a.id==='sGoNum'){ const n=normNum($('sNum').value); if(n.length<11){ toast('ശരിയായ number നൽകൂ'); return; } if($('sKeep').checked) addContact($('sName').value.trim(),n); nativeShare(n); return; }
    nativeShare(num); }, true);
};

// other links open outside the app
if(NATIVE) document.addEventListener('click',e=>{ const a=e.target.closest('a[target="_blank"]'); if(a&&!a.getAttribute('href').startsWith('#')&&!e.defaultPrevented){ e.preventDefault(); NATIVE.open(a.href); } });

// Android back button
window.disniBack = ()=>{
  const sheets=document.querySelectorAll('.sheet-bg'); if(sheets.length){ const last=sheets[sheets.length-1]; if(last.parentElement===$('sheetRoot')) $('sheetRoot').innerHTML=''; else last.remove(); return true; }
  if(!$('auth').hidden) return false;
  if(sel){ sel=null; draw(); return true; }
  if(view!=='models'){ go('models'); return true; }
  return false;
};

// update check (phone app)
let updMode='apk';
if(NATIVE){ fetch(`https://raw.githubusercontent.com/${REPO}/main/release/version.txt?t=${Date.now()}`).then(r=>r.ok?r.text():'').then(t=>{ const v=parseInt(t,10); if(v&&v>NATIVE.versionCode()&&updMode==='apk'){ $('updBar').querySelector('span').textContent='പുതിയ app version ready'; $('updBar').hidden=false; } }).catch(()=>{}); }
// new screens downloaded in the background (no reinstall): reload to use them
window.disniWebUpdated = ()=>{ updMode='web'; $('updBar').querySelector('span').textContent='പുതിയ മാറ്റങ്ങൾ വന്നു'; $('updBar').hidden=false; };
$('updBtn').onclick=()=>{ if(updMode==='web'||!NATIVE){ persistCur(); setTimeout(()=>location.reload(),150); } else NATIVE.open(APK_URL); };

// Auto background without Claude: pick by the award words
if(!window.claude){ $('bgAuto').hidden=false; $('bgAuto').onclick=()=>{
  const t=[cur.fields.head,cur.fields.det,cur.fields.by].join(' ').toLowerCase(); let k='silver';
  if(/first|1st|winner|champion|ഒന്നാം|gold/.test(t)) k='rays'; else if(/second|2nd|രണ്ടാം/.test(t)) k='silver'; else if(/third|3rd|മൂന്നാം/.test(t)) k='swoosh';
  else if(/visa|honou?r|felicitat|retire|ആദരം|ആദരവ്|vip/.test(t)) k='royalframe'; else if(/best|excellen|star|topper/.test(t)) k='stars';
  else if(/school|class|fest|kalolsavam|cultural|teen|kids|madrasa|മദ്രസ/.test(t)) k='swoosh'; else if(/birthday|celebrat|party/.test(t)) k='confetti'; else if(/achiev|service|award/.test(t)) k='laurel';
  $('bgSw').querySelector(`[data-b="${k}"]`)?.click(); const n=$('bgAutoNote'); n.hidden=false; n.textContent=`${BGS[k].name}: award-ലെ വാക്കുകൾ നോക്കി തിരഞ്ഞെടുത്തു`; }; }

/* ---------- automatic trophy shape (on-phone AI: tap-to-select object) ---------- */
let isegP=null;
function getISeg(){
  if(isegP) return isegP;
  isegP=(async()=>{
    const V='https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14';
    const vision=await import(V+'/vision_bundle.mjs');
    const files=await vision.FilesetResolver.forVisionTasks(V+'/wasm');
    return vision.InteractiveSegmenter.createFromOptions(files,{baseOptions:{modelAssetPath:'https://storage.googleapis.com/mediapipe-models/interactive_segmenter/magic_touch/float32/1/magic_touch.tflite'},outputCategoryMask:false,outputConfidenceMasks:true});
  })();
  isegP.catch(()=>{ isegP=null; });
  return isegP;
}
async function maskAt(src,pt){
  const seg=await getISeg();
  const im=new Image(); im.src=src; await im.decode();
  const sc=Math.min(1,1024/Math.max(im.naturalWidth,im.naturalHeight));
  const c=document.createElement('canvas'); c.width=Math.round(im.naturalWidth*sc); c.height=Math.round(im.naturalHeight*sc); c.getContext('2d').drawImage(im,0,0,c.width,c.height);
  const res=seg.segment(c,{keypoint:{x:pt.x,y:pt.y}});
  const masks=res.confidenceMasks||[]; let best=null, bv=-1;
  for(const m of masks){ const a=m.getAsFloat32Array(); const v=a[Math.min(m.height-1,Math.floor(pt.y*m.height))*m.width+Math.min(m.width-1,Math.floor(pt.x*m.width))]; if(v>bv){ bv=v; best={w:m.width,h:m.height,a:Float32Array.from(a)}; } }
  try{ res.close&&res.close(); }catch(e){}
  if(!best) throw {code:'none'};
  return best;
}
// connected region around the tap -> outline by casting rays from its centre (good for plates, shields, arches, figures)
function regionAt(m,pt){
  const {w,h,a}=m, inside=new Uint8Array(w*h); for(let i=0;i<a.length;i++) inside[i]=a[i]>0.5?1:0;
  let sx=Math.floor(pt.x*w), sy=Math.floor(pt.y*h);
  if(!inside[sy*w+sx]){ let found=false; for(let r=1;r<40&&!found;r++) for(let dy=-r;dy<=r&&!found;dy++) for(let dx=-r;dx<=r;dx++){ const x=sx+dx,y=sy+dy; if(x>=0&&y>=0&&x<w&&y<h&&inside[y*w+x]){ sx=x;sy=y;found=true;break; } } if(!found) return null; }
  const comp=new Uint8Array(w*h), st=[sy*w+sx]; comp[sy*w+sx]=1; let n=0,cx=0,cy=0;
  while(st.length){ const i=st.pop(), x=i%w, y=(i-x)/w; n++; cx+=x; cy+=y;
    if(x>0&&inside[i-1]&&!comp[i-1]){comp[i-1]=1;st.push(i-1);} if(x<w-1&&inside[i+1]&&!comp[i+1]){comp[i+1]=1;st.push(i+1);}
    if(y>0&&inside[i-w]&&!comp[i-w]){comp[i-w]=1;st.push(i-w);} if(y<h-1&&inside[i+w]&&!comp[i+w]){comp[i+w]=1;st.push(i+w);} }
  if(n<200) return null;
  return {comp,w,h,n,cx:cx/n,cy:cy/n};
}
function outlineOf(R){
  const {comp,w,h,cx,cy}=R, pts=[], N=180, maxR=Math.hypot(w,h);
  for(let k=0;k<N;k++){ const t=k/N*Math.PI*2, dx=Math.cos(t), dy=Math.sin(t); let last=0, miss=0;
    for(let r=0;r<maxR;r+=1){ const x=Math.round(cx+dx*r), y=Math.round(cy+dy*r); if(x<0||y<0||x>=w||y>=h) break;
      if(comp[y*w+x]){ last=r; miss=0; } else if(++miss>6) break; }
    pts.push([(cx+dx*last)/w,(cy+dy*last)/h]); }
  return pts;
}
function longAxis(R){
  const {comp,w,h,cx,cy}=R; let sxx=0,syy=0,sxy=0,n=0;
  for(let i=0;i<comp.length;i++) if(comp[i]){ const x=i%w-cx, y=(i-i%w)/w-cy; sxx+=x*x; syy+=y*y; sxy+=x*y; n++; }
  const th=0.5*Math.atan2(2*sxy,sxx-syy), ux=Math.cos(th), uy=Math.sin(th); let mn=1e9,mx=-1e9;
  for(let i=0;i<comp.length;i++) if(comp[i]){ const x=i%w-cx, y=(i-i%w)/w-cy, p=x*ux+y*uy; if(p<mn)mn=p; if(p>mx)mx=p; }
  return {a:[(cx+ux*mn)/w,(cy+uy*mn)/h], b:[(cx+ux*mx)/w,(cy+uy*mx)/h]};
}
if(!window.claude){
  autoDetect = async function(src, pt, want){
    const p = pt || {x:.5,y:.45};
    const m = await maskAt(src,p); const R = regionAt(m,p); if(!R) return {};
    return want==='ref' ? {ref:longAxis(R)} : {plate:outlineOf(R)};
  };
}

/* ---------- background remover for people photos ---------- */
let segP=null;
function getSegmenter(){
  if(segP) return segP;
  segP=(async()=>{
    const V='https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14';
    const vision=await import(V+'/vision_bundle.mjs');
    const files=await vision.FilesetResolver.forVisionTasks(V+'/wasm');
    return vision.ImageSegmenter.createFromOptions(files,{baseOptions:{modelAssetPath:'https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite'},runningMode:'IMAGE',outputConfidenceMasks:true,outputCategoryMask:false});
  })();
  segP.catch(()=>{ segP=null; });
  return segP;
}
async function removeBg(src){
  const seg=await getSegmenter();
  const im=new Image(); im.src=src; await im.decode();
  const max=1200, sc=Math.min(1,max/Math.max(im.naturalWidth,im.naturalHeight));
  const c=document.createElement('canvas'); c.width=Math.round(im.naturalWidth*sc); c.height=Math.round(im.naturalHeight*sc);
  const x=c.getContext('2d'); x.drawImage(im,0,0,c.width,c.height);
  const res=seg.segment(c); const bgMask=res.confidenceMasks[0]; const mw=bgMask.width, mh=bgMask.height; const bg=bgMask.getAsFloat32Array();
  const mc=document.createElement('canvas'); mc.width=mw; mc.height=mh; const mx=mc.getContext('2d'); const md=mx.createImageData(mw,mh);
  for(let i=0;i<bg.length;i++){ let a=1-bg[i]; a=Math.min(1,Math.max(0,(a-0.35)/0.3)); a=a*a*(3-2*a); md.data[i*4+3]=Math.round(a*255); }
  mx.putImageData(md,0,0); try{ res.close&&res.close(); }catch(e){}
  x.globalCompositeOperation='destination-in'; x.imageSmoothingQuality='high'; x.filter='blur(1px)'; x.drawImage(mc,0,0,c.width,c.height); x.filter='none';
  return c.toDataURL('image/png');
}
''' + "</script>\n</body></html>")
s = s.replace('__REPO__', REPO)
import time
s = s.replace('__WEBVER__', str(int(time.time())))

# saveFile / sendSheet / listen must be reassignable
rep("async function saveFile(filename,data,previewURL){", "var saveFile = async function(filename,data,previewURL){")
s = re.sub(r"(var saveFile = async function\(filename,data,previewURL\)\{.*?\n\})", lambda m: m.group(1)+';', s, count=1, flags=re.S)
rep("function sendSheet(){", "var sendSheet = function(){")
s = re.sub(r"(var sendSheet = function\(\)\{.*?\n\})\n\n/\* ---------- backup", lambda m: m.group(1)+';\n\n/* ---------- backup', s, count=1, flags=re.S)
rep("function listen(btn){", "var listen = function(btn){")
s = re.sub(r"(var listen = function\(btn\)\{.*?\n\})", lambda m: m.group(1)+';', s, count=1, flags=re.S)

# ---------- photo panel: background remove + round fill ----------
rep('''      <div id="imgCtl">
        <div class="lbl" style="margin-bottom:6px">FRAME</div>''', '''      <div id="imgCtl">
        <button class="bgbtn" id="rmBg" type="button"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/><path d="M2 3l20 18" stroke-dasharray="2 2"/></svg><span><b id="rmBgT">Background remove ചെയ്യൂ</b><small id="rmBgS">ആളെ മാത്രം എടുത്ത് round frame-ൽ വൃത്തിയായി വയ്ക്കും</small></span></button>
        <div class="lbl" style="margin:12px 0 6px">BEHIND PERSON</div>
        <div class="sw" id="fillSw"></div>
        <div class="lbl" style="margin:12px 0 6px">FRAME</div>''')
rep("$('frameChips').innerHTML", r'''var FILLS={none:null,gold:['#fff3c4','#e3b043','#a8701a'],red:['#ff5a6e','#c8102e','#6e0616'],white:['#ffffff','#f1f1f4','#d9dbe2'],blue:['#7fb0ff','#2347a8','#0c1c4d'],silver:['#ffffff','#d6d9df','#9aa0aa']};
$('fillSw').innerHTML=Object.entries(FILLS).map(([k,c])=>`<button data-f="${k}" aria-label="${k}" style="background:${c?`radial-gradient(circle at 40% 35%,${c[0]},${c[1]} 55%,${c[2]})`:'transparent'}">${c?'':'<span style="color:var(--muted)">×</span>'}</button>`).join('');
$('fillSw').onclick=e=>{ const b=e.target.closest('button'); const L=selLayer(); if(b&&L&&L.type==='image'){ L.fill=b.dataset.f==='none'?null:b.dataset.f; if(L.fill&&L.frame==='none') L.frame='circle'; commit(); } };
$('rmBg').onclick=async()=>{
  const L=selLayer(); if(!L||L.type!=='image') return;
  if(L.origSrc){ L.src=L.origSrc; delete L.origSrc; L.fill=null; commit(); return; }
  const t=$('rmBgT'), sm=$('rmBgS'); t.textContent='Background മാറ്റുന്നു…'; sm.textContent='ആദ്യ തവണ കുറച്ച് സെക്കൻഡ് എടുക്കും (internet വേണം)'; $('rmBg').disabled=true;
  try{ const out=await removeBg(L.src); L.origSrc=L.src; L.src=out; L.frame='circle'; L.fill=L.fill||'gold'; L.ring=L.ring&&L.ring!=='none'?L.ring:'#e8c26a'; commit(); toast('Background remove ചെയ്തു'); }
  catch(err){ toast('ഇപ്പോൾ പറ്റിയില്ല — internet ഉണ്ടോ എന്ന് നോക്കി വീണ്ടും ശ്രമിക്കൂ'); }
  $('rmBg').disabled=false; syncPanels();
};
$('frameChips').innerHTML''')
rep("  if(isI){ $('iSize').value=L.w;", '''  if(isI){ $('rmBgT').textContent=L.origSrc?'Original photo തിരികെ':'Background remove ചെയ്യൂ'; $('rmBgS').textContent=L.origSrc?'Background ഉള്ള പഴയ photo വേണമെങ്കിൽ':'ആളെ മാത്രം എടുത്ത് round frame-ൽ വൃത്തിയായി വയ്ക്കും';
    document.querySelectorAll('#fillSw button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.f===(L.fill||'none')));
    $('iSize').value=L.w;''')
# render the fill behind the cut-out person
rep("    ctx.save(); ctx.clip();\n    if(im&&im.complete&&im.naturalWidth){ const s=Math.max(w/im.naturalWidth,h/im.naturalHeight);",
"""    ctx.save(); ctx.clip();
    if(L.fill&&typeof FILLS!=='undefined'&&FILLS[L.fill]){ const f=FILLS[L.fill]; const g=ctx.createRadialGradient(x+w*.4,y+h*.35,0,x+w/2,y+h/2,Math.max(w,h)*.7); g.addColorStop(0,f[0]); g.addColorStop(.55,f[1]); g.addColorStop(1,f[2]); ctx.fillStyle=g; ctx.fillRect(x,y,w,h); }
    if(im&&im.complete&&im.naturalWidth){ const s=Math.max(w/im.naturalWidth,h/im.naturalHeight);""")
# a freshly added person photo: offer background removal right away
rep("  if(cur.layers.some(l=>l.type==='text')) applyTemplate(); sel=L.id; commit(); toast('Photo ചേർത്തു'); };",
    "  if(cur.layers.some(l=>l.type==='text')) applyTemplate(); sel=L.id; showPanel('photo'); commit(); toast('Photo ചേർത്തു — Background remove അമർത്താം'); };")

# start: show sign-in or resume session
s = s.replace("</script>\n</body></html>", r'''
(function start(){ let e=null; try{ e=localStorage.getItem('disni-session'); }catch(err){}
  if(e && accounts()[e]) signIn(e); else { $('auth').hidden=false; setAuthMode(Object.keys(accounts()).length?'in':'up'); } })();
</script>
</body></html>''', 1)

imgs = json.load(open(os.path.join(HERE, 'images.json')))
s = s.replace('__IMGS__', json.dumps(imgs))
for out in ('app/src/main/assets/index.html', 'web/app/index.html'):
    open(os.path.join(ROOT, out), 'w').write(s)
print('ok', len(s))
