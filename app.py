import streamlit as st
import os
import json
import base64
import random

st.set_page_config(
    page_title="Discourse Assessment Protocol",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── API Key ──────────────────────────────────────────────────────────────────
api_key = ""
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")

# ── Section II task list ─────────────────────────────────────────────────────
SECTION2_TASKS = [
    "II-A1 — Cookie Theft",
    "II-A2 — Broken Window",
    "II-B1 — Cat Rescue",
    "II-B2 — Refused Umbrella",
]

# Shuffle once per session; stable across reruns, fresh per participant
if "task_order" not in st.session_state:
    order = SECTION2_TASKS.copy()
    random.shuffle(order)
    st.session_state.task_order = order

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Protocol Navigator")

    rcol, bcol = st.columns([5, 1])
    with rcol:
        st.caption("Section II order is randomized per session.")
    with bcol:
        if st.button("🔀", help="Re-randomize for a new participant"):
            order = SECTION2_TASKS.copy()
            random.shuffle(order)
            st.session_state.task_order = order
            st.rerun()

    task = st.radio(
        "Select task",
        ["I — First Encounter"] + st.session_state.task_order,
    )

    st.divider()
    st.subheader("⚙️ Configuration")
    if not api_key:
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            placeholder="sk-ant-...",
            help="Required for Section I only.",
        )
        if api_key:
            st.success("Key entered ✓")
    else:
        st.success("API key loaded ✓")

    st.divider()
    st.caption(
        "**Browser:** Chrome or Edge required\n\n"
        "**Images:** Place stimulus files in an `images/` folder next to `app.py`"
    )
    with st.expander("Expected image filenames"):
        st.code(
            "images/cookie_theft.jpg\n"
            "images/broken_window_1.jpg\n"
            "images/broken_window_2.jpg\n"
            "images/broken_window_3.jpg\n"
            "images/broken_window_4.jpg\n"
            "images/cat_rescue.jpg\n"
            "images/refused_umbrella_1.jpg\n"
            "images/refused_umbrella_2.jpg\n"
            "images/refused_umbrella_3.jpg\n"
            "images/refused_umbrella_4.jpg",
            language="text",
        )


# ── Image helpers ─────────────────────────────────────────────────────────────
def img_src(path):
    """Return base64 data-URL if file exists, else None."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        ext = path.rsplit(".", 1)[-1].lower()
        mime = "jpeg" if ext in ("jpg", "jpeg") else ext
        return f"data:image/{mime};base64,{data}"
    return None


def single_img_html(path, label):
    src = img_src(path)
    if src:
        return (
            f'<div style="border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;margin-bottom:14px">'
            f'<img src="{src}" style="width:100%;display:block">'
            f'<div style="background:#f8fafc;padding:5px 12px;font-size:11px;color:#64748b">{label}</div>'
            f"</div>"
        )
    return (
        f'<div style="background:#f1f5f9;border:2px dashed #e2e8f0;border-radius:10px;'
        f'padding:40px 20px;text-align:center;color:#94a3b8;margin-bottom:14px">'
        f'<div style="font-size:36px">🖼️</div>'
        f'<div style="font-size:13px;font-weight:500;margin-top:8px">{label}</div>'
        f'<div style="font-size:11px;margin-top:4px;color:#cbd5e1">Place {os.path.basename(path)} in images/</div>'
        f"</div>"
    )


def multi_img_html(paths_labels):
    cols = len(paths_labels)
    items = ""
    for path, label in paths_labels:
        src = img_src(path)
        if src:
            inner = f'<img src="{src}" style="width:100%;border-radius:6px;display:block">'
        else:
            inner = (
                f'<div style="background:#f1f5f9;border:2px dashed #e2e8f0;border-radius:6px;'
                f'aspect-ratio:4/3;display:flex;align-items:center;justify-content:center;'
                f'flex-direction:column;color:#94a3b8;font-size:11px;gap:4px">'
                f'<span style="font-size:22px">🖼️</span>{label}</div>'
            )
        items += (
            f'<div style="text-align:center">{inner}'
            f'<div style="font-size:10px;color:#94a3b8;margin-top:3px">{label}</div></div>'
        )
    return (
        f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:8px;margin-bottom:14px">'
        + items
        + "</div>"
    )


# ── Section I HTML ────────────────────────────────────────────────────────────
SECTION1_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.0.0/dist/tabler-icons.min.css">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:transparent;color:#1e293b;font-size:14px;}
.screen{display:none;} .screen.on{display:flex;flex-direction:column;align-items:center;padding:16px 16px 12px;animation:up .2s ease;}
@keyframes up{from{opacity:0;transform:translateY(6px);}to{opacity:1;transform:translateY(0);}}
.intro-logo{width:58px;height:58px;border-radius:50%;background:#f0f9ff;border:1px solid rgba(14,165,233,.25);display:flex;align-items:center;justify-content:center;font-size:24px;color:#0ea5e9;margin-bottom:12px;}
h1{font-size:20px;font-weight:600;color:#1e293b;margin-bottom:5px;text-align:center;}
.badge{display:inline-block;background:#f0f9ff;color:#0369a1;border:1px solid rgba(14,165,233,.3);padding:3px 12px;border-radius:50px;font-size:12px;font-weight:600;margin-bottom:12px;}
.sub{font-size:13px;color:#64748b;text-align:center;line-height:1.6;margin-bottom:14px;}
.info-box{width:100%;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:12px 16px;margin-bottom:20px;}
.info-box .lbl{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:#94a3b8;margin-bottom:5px;}
.info-box p{font-size:12px;color:#64748b;line-height:1.6;}
button{background:#f0f9ff;color:#0369a1;border:1px solid rgba(14,165,233,.4);padding:9px 28px;border-radius:50px;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;transition:background .15s;}
button:hover{background:#e0f2fe;}
.err{display:none;color:#dc2626;font-size:12px;margin-top:10px;text-align:center;}
.sess-hd{width:100%;display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;}
.sess-lbl{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:#94a3b8;}
.timer{font-size:22px;font-weight:600;font-variant-numeric:tabular-nums;color:#1e293b;font-family:'SF Mono',Menlo,monospace;}
.timer.warn{color:#d97706;}
.grid{width:100%;display:grid;grid-template-columns:1fr 60px 1fr;gap:10px;align-items:center;margin-bottom:10px;}
.panel{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:18px 10px;display:flex;flex-direction:column;align-items:center;gap:7px;min-height:162px;justify-content:center;transition:background .25s,border-color .25s;}
.panel.ai-on{background:#f0f9ff;border-color:rgba(14,165,233,.45);}
.panel.pa-on{background:#fffbeb;border-color:rgba(245,158,11,.45);}
.p-ico{width:48px;height:48px;border-radius:50%;background:#f1f5f9;display:flex;align-items:center;justify-content:center;font-size:20px;color:#94a3b8;transition:color .25s,background .25s;}
.panel.ai-on .p-ico{background:#fff;color:#0ea5e9;}
.panel.pa-on .p-ico{background:#fff;color:#d97706;}
.p-name{font-size:12px;font-weight:600;color:#1e293b;}
.p-st{font-size:11px;color:#94a3b8;text-align:center;min-height:14px;transition:color .2s;}
.panel.ai-on .p-st{color:#0284c7;} .panel.pa-on .p-st{color:#b45309;}
.ctr{display:flex;flex-direction:column;align-items:center;justify-content:center;height:162px;gap:8px;}
.wave{display:flex;align-items:center;gap:3px;height:28px;}
.wbar{width:3px;border-radius:2px;background:#e2e8f0;height:4px;}
.wbar:nth-child(1){animation-delay:.00s;} .wbar:nth-child(2){animation-delay:.12s;}
.wbar:nth-child(3){animation-delay:.24s;} .wbar:nth-child(4){animation-delay:.12s;} .wbar:nth-child(5){animation-delay:.00s;}
.wave.ai-wave .wbar{background:#0ea5e9;animation:wv .85s ease-in-out infinite;}
.wave.pa-wave .wbar{background:#f59e0b;animation:wv .60s ease-in-out infinite;}
@keyframes wv{0%,100%{height:4px;}50%{height:24px;}}
.spin{display:none;width:20px;height:20px;border:2px solid #e2e8f0;border-top-color:#0ea5e9;border-radius:50%;animation:rot .7s linear infinite;}
@keyframes rot{to{transform:rotate(360deg);}}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.2;}}
.status-p{width:100%;text-align:center;font-size:12px;color:#94a3b8;min-height:15px;margin-bottom:6px;}
.irow{min-height:26px;display:flex;align-items:center;justify-content:center;margin-bottom:12px;}
.ipill{display:none;background:#f8fafc;border:1px solid #e2e8f0;border-radius:50px;padding:3px 11px;font-size:11px;color:#64748b;font-style:italic;max-width:100%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.btn-end{color:#64748b;border-color:#e2e8f0;} .btn-end:hover{background:#f1f5f9;}
.end-logo{width:58px;height:58px;border-radius:50%;background:#f0fdf4;border:1px solid rgba(34,197,94,.3);display:flex;align-items:center;justify-content:center;font-size:24px;color:#16a34a;margin-bottom:12px;}
</style>
</head>
<body>
<div id="app">
  <div id="s-intro" class="screen on" style="justify-content:center;min-height:260px;gap:16px;padding-top:48px;">
    <p style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:#94a3b8;margin:0;">Section I — First Encounter</p>
    <button style="font-size:15px;padding:13px 52px;" onclick="startSession()"><i class="ti ti-player-play"></i>&nbsp; Start Session</button>
    <p class="err" id="err"></p>
  </div>
  <div id="s-sess" class="screen">
    <div class="sess-hd"><span class="sess-lbl">First Encounter</span><div style="display:flex;align-items:center;gap:10px;"><span id="rec-ind" style="display:none;align-items:center;gap:5px;font-size:11px;font-weight:700;color:#dc2626;"><span style="width:8px;height:8px;border-radius:50%;background:#dc2626;animation:blink 1.5s ease-in-out infinite;display:inline-block;"></span>REC</span><span class="timer" id="timer">0:00</span></div></div>
    <div class="grid">
      <div class="panel" id="panel-ai"><div class="p-ico"><i class="ti ti-robot"></i></div><div class="p-name">AI Partner</div><div class="p-st" id="ai-st">Initializing</div></div>
      <div class="ctr"><div class="wave" id="wave"><div class="wbar"></div><div class="wbar"></div><div class="wbar"></div><div class="wbar"></div><div class="wbar"></div></div><div class="spin" id="spin"></div></div>
      <div class="panel" id="panel-pa"><div class="p-ico"><i class="ti ti-microphone"></i></div><div class="p-name">Participant</div><div class="p-st" id="pa-st">Waiting</div></div>
    </div>
    <p class="status-p" id="status"></p>
    <div class="irow"><div class="ipill" id="ipill"></div></div>
    <button class="btn-end" onclick="endSession()">End Session</button>
  </div>
  <div id="s-end" class="screen">
    <div class="end-logo"><i class="ti ti-check"></i></div>
    <h1>Session Complete</h1>
    <p class="sub" style="margin-top:5px;">Download your files before starting a new session.</p>
    <div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin:16px 0 2px;">
      <button onclick="downloadTranscript()" style="background:#f0f9ff;color:#0369a1;border-color:rgba(14,165,233,.4);">
        <i class="ti ti-file-text"></i>&nbsp; Transcript (.txt)
      </button>
      <button id="btn-audio" onclick="downloadAudio()" disabled style="background:#fffbeb;color:#b45309;border-color:rgba(245,158,11,.4);">
        <i class="ti ti-microphone"></i>&nbsp; Recording (.webm)
      </button>
    </div>
    <p id="rec-note" style="font-size:11px;color:#94a3b8;margin-bottom:14px;min-height:16px;text-align:center;"></p>
    <button onclick="resetSession()"><i class="ti ti-refresh"></i>&nbsp; New Session</button>
  </div>
</div>
<script>
const API_KEY=APIKEY_PLACEHOLDER;
const API_URL="https://api.anthropic.com/v1/messages";
const MAX_S=300,SIL_MS=2500,LONG_S=11000;
const OPENING="Hello. I don't think we've met before. So maybe we can start by getting to know each other a little. This isn't an interview, so I don't have a list of questions prepared. We can just chat casually and get to know each other.";
const SYS="You are participating in the First Encounter section of a clinical discourse assessment. Engage in natural casual conversation as if meeting this person for the first time.\\n\\nRULES:\\n- NOT an interview: no prepared question list\\n- Let the participant lead; follow their topics\\n- VERY SHORT responses: 1-2 sentences max\\n- Be warm, genuine, natural\\n- Never ask more than one question at a time\\n- Respond only with spoken words\\n- Do not reference the assessment";
let phase='idle',hist=[],recog=null,recogOn=false,tid=null,secs=0,silT=null,longT=null,curTx='',voices=[],bugT=null;
let txLog=[],sessStart=null,mediaRec=null,recChunks=[],recStream=null;
const $=id=>document.getElementById(id);
function qShow(id){document.querySelectorAll('.screen').forEach(s=>s.classList.remove('on'));$(id).classList.add('on');}
function setPanel(who,active){const el=$(who==='ai'?'panel-ai':'panel-pa');el.className='panel'+(active?' '+(who==='ai'?'ai-on':'pa-on'):'');const st=$(who==='ai'?'ai-st':'pa-st');if(who==='ai')st.textContent=active?'Speaking\u2026':(phase==='processing'?'Thinking\u2026':'Listening');else st.textContent=active?'Speaking\u2026':'Your turn';}
function setWave(m){const w=$('wave'),sp=$('spin');w.style.display='flex';sp.style.display='none';w.className='wave'+(m==='ai'?' ai-wave':m==='pa'?' pa-wave':'');if(m==='proc'){w.style.display='none';sp.style.display='block';}}
function setStatus(t){$('status').textContent=t;}
function setInterim(t){const el=$('ipill');if(t){el.textContent=t;el.style.display='block';}else{el.style.display='none';el.textContent='';}}
function startTimer(){secs=0;tid=setInterval(()=>{secs++;const el=$('timer');el.textContent=Math.floor(secs/60)+':'+String(secs%60).padStart(2,'0');el.className='timer'+(secs>=MAX_S-30?' warn':'');if(secs>=MAX_S)endSession();},1000);}
function loadVoices(){voices=window.speechSynthesis.getVoices();}
function pickVoice(){const p=['Samantha','Karen','Moira','Google US English Female','Microsoft Aria','Aria','Zira'];for(const n of p){const v=voices.find(v=>v.name.includes(n));if(v)return v;}return voices.find(v=>v.lang&&v.lang.startsWith('en'))||null;}
function speak(text,done){clearInterval(bugT);window.speechSynthesis.cancel();phase='speaking';setPanel('ai',true);setPanel('pa',false);setWave('ai');setStatus('AI partner is speaking\u2026');const utt=new SpeechSynthesisUtterance(text);utt.rate=0.92;utt.pitch=1.0;utt.volume=1.0;const v=pickVoice();if(v)utt.voice=v;utt.onstart=()=>{bugT=setInterval(()=>{window.speechSynthesis.pause();window.speechSynthesis.resume();},9000);};utt.onend=()=>{clearInterval(bugT);setPanel('ai',false);setWave(null);if(done)done();};utt.onerror=()=>{clearInterval(bugT);setPanel('ai',false);setWave(null);if(done)done();};window.speechSynthesis.speak(utt);}
function initSTT(){const SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR)return false;recog=new SR();recog.continuous=true;recog.interimResults=true;recog.lang='en-US';recog.onstart=()=>{recogOn=true;phase='listening';setPanel('pa',false);setWave('pa');setStatus('Listening for participant\u2026');$('pa-st').textContent='Listening\u2026';};recog.onresult=evt=>{let interim='';for(let i=evt.resultIndex;i<evt.results.length;i++){const t=evt.results[i][0].transcript;if(evt.results[i].isFinal){curTx+=t+' ';clearTimeout(silT);clearTimeout(longT);setPanel('pa',true);silT=setTimeout(()=>{if(curTx.trim()&&phase==='listening'){stopSTT();processTurn(curTx.trim());}},SIL_MS);longT=setTimeout(()=>{if(phase==='listening')setStatus('Take your time\u2026');},LONG_S);}else{interim=t;}}setInterim(interim||'');if(interim)setPanel('pa',true);};recog.onend=()=>{recogOn=false;if(phase==='listening'&&!curTx.trim())setTimeout(()=>{if(phase==='listening')safeStart();},600);};recog.onerror=e=>{recogOn=false;if(e.error==='not-allowed'){setStatus('Mic denied \u2014 allow access and reload.');return;}if(phase==='listening')setTimeout(()=>{if(phase==='listening')safeStart();},1000);};return true;}
function safeStart(){if(recogOn)return;try{recog.start();}catch(_){}}
function stopSTT(){clearTimeout(silT);clearTimeout(longT);try{recog.stop();}catch(_){}recogOn=false;setInterim('');}
function listenForParticipant(){curTx='';setInterim('');phase='listening';setPanel('pa',false);setWave(null);setStatus("Participant's turn\u2026");longT=setTimeout(()=>{if(phase==='listening')setStatus('Take your time\u2026');},LONG_S);safeStart();}
async function processTurn(text){if(phase==='ended')return;phase='processing';setPanel('ai',false);setPanel('pa',false);setWave('proc');setStatus('Processing\u2026');$('ai-st').textContent='Thinking\u2026';logTx('Participant',text);hist.push({role:'user',content:text});try{const res=await fetch(API_URL,{method:'POST',headers:{'Content-Type':'application/json','x-api-key':API_KEY,'anthropic-version':'2023-06-01','anthropic-dangerous-direct-browser-access':'true'},body:JSON.stringify({model:'claude-sonnet-4-6',max_tokens:180,system:SYS,messages:hist})});const data=await res.json();if(data?.content?.[0]?.text){const reply=data.content[0].text.trim();hist.push({role:'assistant',content:reply});logTx('AI',reply);speak(reply,()=>{if(phase!=='ended')listenForParticipant();});}else{if(phase!=='ended')listenForParticipant();}}catch(err){setStatus('Connection issue \u2014 resuming\u2026');setTimeout(()=>{if(phase!=='ended')listenForParticipant();},2000);}}
function logTx(who,text){if(!sessStart)return;const e=Math.floor((Date.now()-sessStart)/1000);txLog.push({t:Math.floor(e/60)+':'+String(e%60).padStart(2,'0'),who,text});}
function dlTranscript(){if(!txLog.length)return;const d=new Date();let o='DISCOURSE ASSESSMENT — SECTION I: FIRST ENCOUNTER\n';o+='Date: '+d.toLocaleDateString()+'   Time: '+d.toLocaleTimeString()+'\n';o+='─'.repeat(52)+'\n\n';for(const e of txLog)o+='['+e.t+']  '+e.who+':\n'+e.text+'\n\n';const b=new Blob([o],{type:'text/plain'});const u=URL.createObjectURL(b);const a=document.createElement('a');a.href=u;a.download='transcript_'+d.toISOString().slice(0,10)+'.txt';document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(u);}
function downloadTranscript(){dlTranscript();}
async function startRec(){try{recStream=await navigator.mediaDevices.getUserMedia({audio:true,video:false});const mt=MediaRecorder.isTypeSupported('audio/webm;codecs=opus')?'audio/webm;codecs=opus':'audio/webm';mediaRec=new MediaRecorder(recStream,{mimeType:mt});recChunks=[];mediaRec.ondataavailable=e=>{if(e.data.size>0)recChunks.push(e.data);};mediaRec.onstop=()=>{const b=$('btn-audio');if(b)b.disabled=false;};mediaRec.start(1000);const ri=$('rec-ind');if(ri)ri.style.display='flex';}catch(err){const n=$('rec-note');if(n)n.textContent='Audio recording was unavailable in this session.';}}
function stopRec(){if(mediaRec&&mediaRec.state!=='inactive')mediaRec.stop();if(recStream)recStream.getTracks().forEach(t=>t.stop());}
function downloadAudio(){if(!recChunks.length)return;const b=new Blob(recChunks,{type:'audio/webm'});const u=URL.createObjectURL(b);const a=document.createElement('a');a.href=u;a.download='recording_'+new Date().toISOString().slice(0,10)+'.webm';document.body.appendChild(a);a.click();document.body.removeChild(a);URL.revokeObjectURL(u);}
function startSession(){if(!initSTT()){const el=$('err');el.textContent='Speech recognition not supported. Use Chrome or Edge.';el.style.display='block';return;}$('panel-ai').className='panel';$('panel-pa').className='panel';$('ai-st').textContent='Initializing';$('pa-st').textContent='Waiting';setWave(null);setStatus('Preparing session\u2026');setInterim('');txLog=[];recChunks=[];sessStart=Date.now();startRec();logTx('AI',OPENING);hist=[{role:'assistant',content:OPENING}];qShow('s-sess');startTimer();speak(OPENING,()=>{if(phase!=='ended')listenForParticipant();});}
function endSession(){phase='ended';stopSTT();stopRec();clearInterval(tid);clearInterval(bugT);window.speechSynthesis.cancel();qShow('s-end');}
function resetSession(){phase='idle';hist=[];txLog=[];secs=0;curTx='';$('timer').textContent='0:00';$('timer').className='timer';qShow('s-intro');}
if(typeof speechSynthesis!=='undefined'){speechSynthesis.addEventListener('voiceschanged',loadVoices);loadVoices();}
</script>
</body>
</html>"""

# ── Section II HTML template ──────────────────────────────────────────────────
SECTION2_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.0.0/dist/tabler-icons.min.css">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:transparent;color:#1e293b;}
.card{background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;}
.card-head{display:flex;justify-content:space-between;align-items:center;padding:9px 14px;background:#f8fafc;border-bottom:1px solid #e2e8f0;}
.task-lbl{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.7px;color:#64748b;}
.timer{font-size:20px;font-weight:600;font-variant-numeric:tabular-nums;color:#1e293b;font-family:'SF Mono',Menlo,monospace;}
.timer.warn{color:#d97706;}
.card-body{padding:12px 14px;}
.status-row{display:flex;align-items:flex-start;gap:10px;min-height:56px;margin-bottom:10px;}
.s-icon{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;background:#f1f5f9;color:#94a3b8;transition:background .2s,color .2s;}
.s-icon.ai{background:#f0f9ff;color:#0ea5e9;}
.s-icon.pa{background:#fffbeb;color:#d97706;}
.s-icon.ok{background:#f0fdf4;color:#16a34a;}
.s-icon.err{background:#fef2f2;color:#dc2626;}
.s-text{flex:1;}
.s-lbl{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.7px;color:#94a3b8;margin-bottom:2px;}
.s-prompt{font-size:12px;color:#1e293b;line-height:1.55;}
.info-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;}
.utt{font-size:12px;color:#64748b;}
.wave{display:flex;align-items:center;gap:2px;height:20px;}
.wbar{width:3px;border-radius:2px;background:#e2e8f0;height:4px;}
.wbar:nth-child(1){animation-delay:.00s;}.wbar:nth-child(2){animation-delay:.10s;}
.wbar:nth-child(3){animation-delay:.20s;}.wbar:nth-child(4){animation-delay:.10s;}.wbar:nth-child(5){animation-delay:.00s;}
.wave.ai .wbar{background:#0ea5e9;animation:wv .85s ease-in-out infinite;}
.wave.pa .wbar{background:#f59e0b;animation:wv .65s ease-in-out infinite;}
@keyframes wv{0%,100%{height:4px;}50%{height:18px;}}
.btn-row{display:flex;gap:6px;flex-wrap:wrap;}
button{padding:7px 13px;border-radius:50px;font-size:12px;font-weight:600;border:1px solid #e2e8f0;background:#f8fafc;color:#475569;cursor:pointer;font-family:inherit;transition:background .15s;white-space:nowrap;display:inline-flex;align-items:center;gap:4px;}
button:hover:not(:disabled){background:#f1f5f9;}
button:disabled{opacity:.4;cursor:not-allowed;}
.b-start{background:#f0f9ff;color:#0369a1;border-color:rgba(14,165,233,.35);}
.b-start:hover:not(:disabled){background:#e0f2fe;}
.b-end{background:#f0fdf4;color:#15803d;border-color:rgba(34,197,94,.35);}
.b-end:hover:not(:disabled){background:#dcfce7;}
</style>
</head>
<body>
<div class="card">
  <div class="card-head">
    <span class="task-lbl" id="task-lbl">--</span>
    <span class="timer" id="timer">3:00</span>
  </div>
  <div class="card-body">
    <div class="status-row">
      <div class="s-icon" id="s-icon"><i class="ti ti-player-play"></i></div>
      <div class="s-text">
        <div class="s-lbl" id="s-lbl">Ready</div>
        <div class="s-prompt" id="s-prompt">Press Start Task to begin.</div>
      </div>
    </div>
    <div class="info-row">
      <span class="utt" id="utt">Utterances: 0</span>
      <div class="wave" id="wave"><div class="wbar"></div><div class="wbar"></div><div class="wbar"></div><div class="wbar"></div><div class="wbar"></div></div>
    </div>
    <div class="btn-row">
      <button class="b-start" id="b-start" onclick="startTask()"><i class="ti ti-player-play"></i> Start Task</button>
      <button id="b-p2" onclick="giveP2()" style="display:none" disabled><i class="ti ti-message"></i> 2nd Prompt</button>
      <button id="b-p3" onclick="giveP3()" style="display:none" disabled><i class="ti ti-message-2"></i> 3rd Prompt</button>
      <button id="b-panel" onclick="nextPanel()" style="display:none" disabled><i class="ti ti-arrow-right"></i> Next Panel</button>
      <button class="b-end" id="b-end" onclick="endTask()" disabled><i class="ti ti-check"></i> End Task</button>
    </div>
  </div>
</div>
<script>
const CFG = TASKCFG_PLACEHOLDER;
const MAX_S = CFG.duration || 180;
const NR_MS = (CFG.no_response_timeout || 10) * 1000;
let phase='idle', uttCount=0, panelIdx=0, taskSecs=MAX_S;
let taskInt=null, nrTimer=null, bugT=null;
let stt=null, sttOn=false, voices=[];
const $=id=>document.getElementById(id);

function setIcon(cls,icon){const el=$('s-icon');el.className='s-icon '+cls;el.innerHTML='<i class="ti ti-'+icon+'"></i>';}
function setStatus(lbl,prompt,iconCls,iconName){setIcon(iconCls,iconName);$('s-lbl').textContent=lbl;$('s-prompt').textContent=prompt;}
function setWave(m){const w=$('wave');w.className='wave'+(m?' '+m:'');}
function updateTimer(){const m=Math.floor(taskSecs/60),s=String(taskSecs%60).padStart(2,'0');const el=$('timer');el.textContent=m+':'+s;el.className='timer'+(taskSecs<=30?' warn':'');}
function updateUtt(){$('utt').textContent='Utterances: '+uttCount;}

function loadVoices(){voices=window.speechSynthesis.getVoices();}
function pickVoice(){const p=['Samantha','Karen','Moira','Google US English Female','Microsoft Aria','Aria','Zira'];for(const n of p){const v=voices.find(v=>v.name.includes(n));if(v)return v;}return voices.find(v=>v.lang&&v.lang.startsWith('en'))||null;}

function speak(text, done){
  clearInterval(bugT); window.speechSynthesis.cancel();
  phase='speaking'; setWave('ai');
  const utt=new SpeechSynthesisUtterance(text);
  utt.rate=0.92; utt.pitch=1.0; utt.volume=1.0;
  const v=pickVoice(); if(v) utt.voice=v;
  utt.onstart=()=>{bugT=setInterval(()=>{window.speechSynthesis.pause();window.speechSynthesis.resume();},9000);};
  utt.onend=()=>{clearInterval(bugT); setWave(''); if(done) done();};
  utt.onerror=()=>{clearInterval(bugT); setWave(''); if(done) done();};
  window.speechSynthesis.speak(utt);
}

function initSTT(){
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!SR) return false;
  stt=new SR(); stt.continuous=true; stt.interimResults=true; stt.lang='en-US';
  stt.onresult=evt=>{
    for(let i=evt.resultIndex;i<evt.results.length;i++){
      if(evt.results[i].isFinal){uttCount++;updateUtt();clearNR();startNR();setWave('pa');}
      else if(evt.results[i][0].transcript){setWave('pa');}
    }
  };
  stt.onend=()=>{sttOn=false;if(phase==='listening')setTimeout(()=>{if(phase==='listening')safeStart();},500);};
  stt.onerror=e=>{sttOn=false;if(e.error==='not-allowed'){setStatus('Error','Mic denied. Allow access & reload.','err','alert-circle');}else if(phase==='listening')setTimeout(safeStart,1000);};
  return true;
}
function safeStart(){if(sttOn||phase!=='listening')return;try{stt.start();sttOn=true;}catch(_){}}
function stopSTT(){clearNR();try{stt.stop();}catch(_){}sttOn=false;setWave('');}

function startListening(nrPromptText, nrLabel){
  phase='listening'; setWave('');
  safeStart();
  if(nrPromptText){
    clearNR();
    nrTimer=setTimeout(()=>{
      if(phase==='listening'&&uttCount===0){
        playPrompt(nrPromptText, nrLabel||'No-response prompt', null);
      }
    }, NR_MS);
  }
}

function clearNR(){clearTimeout(nrTimer); nrTimer=null;}

function startNR(){
  // After a response, reset no-response timer (for panel context)
  if(CFG.type==='multi'&&CFG.panel_no_response_prompt){
    clearNR();
    nrTimer=setTimeout(()=>{
      if(phase==='listening'){playPrompt(CFG.panel_no_response_prompt,'Panel prompt',null);}
    }, NR_MS);
  }
}

function playPrompt(text, label, onDone){
  stopSTT();
  setStatus(label, text, 'ai', 'volume');
  speak(text, ()=>{
    setStatus('Listening', 'Waiting for participant response\u2026', 'pa', 'microphone');
    startListening(null);
    if(onDone) onDone();
  });
}

function giveP2(){
  if(phase==='done') return;
  const p=CFG.no_response_prompt; if(!p) return;
  $('b-p2').disabled=true;
  playPrompt(p, '2nd prompt');
}

function giveP3(){
  if(phase==='done') return;
  const p=CFG.few_utterances_prompt; if(!p) return;
  $('b-p3').disabled=true;
  playPrompt(p, '3rd prompt');
}

function nextPanel(){
  if(phase==='done'||CFG.type!=='multi') return;
  const panels=CFG.panel_prompts||[];
  if(panelIdx>=panels.length){$('b-panel').disabled=true;return;}
  const prompt=panels[panelIdx]; panelIdx++;
  if(panelIdx>=panels.length) $('b-panel').disabled=true;
  playPrompt(prompt, 'Panel '+(panelIdx+1)+' prompt');
}

function startTask(){
  if(!stt&&!initSTT()){setStatus('Error','Speech recognition not available. Use Chrome/Edge.','err','alert-circle');return;}
  $('b-start').disabled=true;
  $('b-end').disabled=false;
  if(CFG.type==='single'){
    $('b-p2').style.display='inline-flex';
    $('b-p3').style.display='inline-flex';
    $('b-p2').disabled=false;
  } else {
    $('b-panel').style.display='inline-flex';
    $('b-panel').disabled=false;
  }
  taskInt=setInterval(()=>{
    taskSecs--; updateTimer();
    if(taskSecs<=0){
      clearInterval(taskInt);
      if(CFG.type==='single'&&uttCount<(CFG.min_utterances||2)&&CFG.few_utterances_prompt){
        taskSecs=0; updateTimer(); giveP3();
      } else { endTask(); }
    }
  },1000);
  const ip=CFG.initial_prompt;
  setStatus('Initial prompt', ip, 'ai', 'volume');
  speak(ip, ()=>{
    setStatus('Listening', 'Waiting for participant response\u2026', 'pa', 'microphone');
    startListening(CFG.no_response_prompt, '2nd prompt');
  });
}

function endTask(){
  phase='done'; stopSTT(); clearInterval(taskInt); clearInterval(bugT);
  window.speechSynthesis.cancel(); setWave('');
  setStatus('Task Complete','Navigate to the next task in the sidebar.','ok','check');
  $('b-start').disabled=true; $('b-end').disabled=true;
  $('b-p2').disabled=true; $('b-p3').disabled=true; $('b-panel').disabled=true;
  $('timer').className='timer';
}

$('task-lbl').textContent=CFG.task_label||'Task';
updateTimer();
if(typeof speechSynthesis!=='undefined'){speechSynthesis.addEventListener('voiceschanged',loadVoices);loadVoices();}
</script>
</body>
</html>"""

# ── Task configurations ────────────────────────────────────────────────────────
TASK_CONFIGS = {
    "II-A1 — Cookie Theft": {
        "task_label": "II-A1 — Cookie Theft",
        "type": "single",
        "duration": 180,
        "no_response_timeout": 10,
        "min_utterances": 2,
        "initial_prompt": (
            "Here is a picture. "
            "Please tell me everything you see going on in this picture."
        ),
        "no_response_prompt": (
            "Take a look and tell me what's happening in the picture."
        ),
        "few_utterances_prompt": (
            "Anything else you can tell me about the picture?"
        ),
    },
    "II-A2 — Broken Window": {
        "task_label": "II-A2 — Broken Window",
        "type": "multi",
        "duration": 180,
        "no_response_timeout": 10,
        "initial_prompt": (
            "Now I'm going to show you these pictures. "
            "Take a little time to look at these pictures. "
            "They tell a story. "
            "Take a look at all of them, and then I'll ask you to tell me the story "
            "with a beginning, a middle, and an end. "
            "You can look at the pictures as you tell the story."
        ),
        "no_response_prompt": (
            "Take a look at the first picture and tell me what you think is happening."
        ),
        "panel_prompts": [
            "And what happens in the second panel?",
            "And what happens in the third panel?",
            "And what happens in the fourth panel?",
        ],
        "panel_no_response_prompt": "Can you tell me anything about this picture?",
    },
    "II-B1 — Cat Rescue": {
        "task_label": "II-B1 — Cat Rescue",
        "type": "single",
        "duration": 180,
        "no_response_timeout": 10,
        "min_utterances": 2,
        "initial_prompt": (
            "Here is a picture that tells a story. "
            "Look at everything that's happening and then tell me a story about what you see. "
            "Tell me the story with a beginning, a middle, and an end."
        ),
        "no_response_prompt": (
            "Take a look and tell me any part of the story."
        ),
        "few_utterances_prompt": (
            "Anything else you can tell me about the story?"
        ),
    },
    "II-B2 — Refused Umbrella": {
        "task_label": "II-B2 — Refused Umbrella",
        "type": "multi",
        "duration": 180,
        "no_response_timeout": 10,
        "initial_prompt": (
            "Here are some more pictures that tell a story. "
            "Take a look at all of them, and then I'll ask you to tell me the story "
            "with a beginning, a middle, and an end. "
            "Again, you can look at the pictures as you tell the story."
        ),
        "no_response_prompt": (
            "Look at this picture and tell me what you think is happening."
        ),
        "panel_prompts": [
            "And what happens here?",
            "And what happens here?",
            "And what happens here?",
        ],
        "panel_no_response_prompt": "Can you tell me anything about this picture?",
        "end_fallback": "Let's move on to something a little different.",
    },
}

# Image paths
IMAGE_PATHS = {
    "II-A1 — Cookie Theft": [("images/cookie_theft.jpg", "Cookie Theft")],
    "II-A2 — Broken Window": [
        ("images/broken_window_1.jpg", "Panel 1"),
        ("images/broken_window_2.jpg", "Panel 2"),
        ("images/broken_window_3.jpg", "Panel 3"),
        ("images/broken_window_4.jpg", "Panel 4"),
    ],
    "II-B1 — Cat Rescue": [("images/cat_rescue.jpg", "Cat Rescue")],
    "II-B2 — Refused Umbrella": [
        ("images/refused_umbrella_1.jpg", "Panel 1"),
        ("images/refused_umbrella_2.jpg", "Panel 2"),
        ("images/refused_umbrella_3.jpg", "Panel 3"),
        ("images/refused_umbrella_4.jpg", "Panel 4"),
    ],
}

# ── Main routing ──────────────────────────────────────────────────────────────
st.title("Discourse Assessment Protocol")

if task == "I — First Encounter":
    st.write("**Section I: First Encounter** · ~5 minutes · AI-generated responses")
    if not api_key:
        st.warning("Enter your Anthropic API key in the sidebar to begin Section I.")
        st.stop()
    html = SECTION1_HTML.replace("APIKEY_PLACEHOLDER", json.dumps(api_key))
    st.components.v1.html(html, height=530, scrolling=False)

else:
    cfg = TASK_CONFIGS[task]
    images = IMAGE_PATHS[task]

    duration_min = cfg["duration"] // 60
    st.write(f"**Section {task}** · ~{duration_min} minutes · Scripted prompts · No API key needed")

    # ── Image display ──
    if len(images) == 1:
        path, label = images[0]
        st.markdown(single_img_html(path, label), unsafe_allow_html=True)
    else:
        st.markdown(multi_img_html(images), unsafe_allow_html=True)

    # ── Protocol script (collapsible reference for examiner) ──
    with st.expander("📋 Examiner script reference", expanded=False):
        p = cfg
        st.markdown(f"**Initial prompt:**\n> {p['initial_prompt']}")
        st.markdown(f"**If no response in 10 s:**\n> {p['no_response_prompt']}")
        if p.get("few_utterances_prompt"):
            st.markdown(f"**If fewer than 2 utterances:**\n> {p['few_utterances_prompt']}")
        if p.get("panel_prompts"):
            for i, pp in enumerate(p["panel_prompts"], 2):
                st.markdown(f"**Panel {i} prompt:**\n> {pp}")
            st.markdown(f"**Panel no-response:**\n> {p['panel_no_response_prompt']}")
        if p.get("end_fallback"):
            st.markdown(f"**If no response at all:**\n> {p['end_fallback']}")

    # ── Voice control ──
    html = SECTION2_HTML.replace("TASKCFG_PLACEHOLDER", json.dumps(cfg))
    st.components.v1.html(html, height=220, scrolling=False)

st.divider()
st.caption("⚠️ Requires Chrome or Edge for speech recognition and synthesis.")