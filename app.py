import streamlit as st
import os
import json

st.set_page_config(
    page_title="Discourse Assessment — First Encounter",
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

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")

    if not api_key:
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            placeholder="sk-ant-...",
            help="Your key is injected server-side and used only for Anthropic API calls.",
        )
        if api_key:
            st.success("Key entered ✓")
    else:
        st.success("API key loaded from environment ✓")

    st.divider()

    st.subheader("📋 Protocol Info")
    st.markdown(
        """
| Field | Value |
|-------|-------|
| Section | I — First Encounter |
| Duration | ~5 min |
| Browser | Chrome / Edge |
| Input mode | Voice only |
"""
    )

    st.divider()
    st.caption(
        "The AI partner has no prepared questions. "
        "Allow the participant to initiate topics and lead the conversation."
    )

# ── Page header ──────────────────────────────────────────────────────────────
st.title("🎙️ Discourse Assessment")
st.write("**Section I: First Encounter** — Voice-only protocol")

if not api_key:
    st.info("Enter your Anthropic API key in the sidebar to begin the session.")
    st.stop()

# ── Embedded HTML voice chatbot ───────────────────────────────────────────────
# API_KEY_PLACEHOLDER is replaced by the Python-side key so it never
# appears in source committed to version control.
CHATBOT_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.0.0/dist/tabler-icons.min.css">
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: transparent;
  color: #1e293b;
  font-size: 14px;
}

.screen { display: none; }
.screen.on {
  display: flex; flex-direction: column; align-items: center;
  padding: 16px 16px 12px;
  animation: up .2s ease;
}
@keyframes up { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:translateY(0); } }

/* ── INTRO ── */
.intro-logo {
  width: 58px; height: 58px; border-radius: 50%;
  background: #f0f9ff; border: 1px solid rgba(14,165,233,.25);
  display: flex; align-items: center; justify-content: center;
  font-size: 24px; color: #0ea5e9;
  margin-bottom: 12px;
}

h1 { font-size: 20px; font-weight: 600; color: #1e293b; margin-bottom: 5px; text-align: center; }

.badge {
  display: inline-block;
  background: #f0f9ff; color: #0369a1;
  border: 1px solid rgba(14,165,233,.3);
  padding: 3px 12px; border-radius: 50px;
  font-size: 12px; font-weight: 600;
  margin-bottom: 12px;
}

.sub {
  font-size: 13px; color: #64748b;
  text-align: center; line-height: 1.6;
  margin-bottom: 14px;
}

.info-box {
  width: 100%;
  background: #f8fafc; border: 1px solid #e2e8f0;
  border-radius: 10px; padding: 12px 16px;
  margin-bottom: 20px;
}
.info-box .lbl {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: .8px; color: #94a3b8; margin-bottom: 5px;
}
.info-box p { font-size: 12px; color: #64748b; line-height: 1.6; }

button {
  background: #f0f9ff; color: #0369a1;
  border: 1px solid rgba(14,165,233,.4);
  padding: 9px 28px; border-radius: 50px;
  font-size: 13px; font-weight: 600;
  cursor: pointer; font-family: inherit;
  transition: background .15s;
}
button:hover { background: #e0f2fe; }

.err { display:none; color:#dc2626; font-size:12px; margin-top:10px; text-align:center; }

/* ── SESSION ── */
.sess-hd {
  width: 100%;
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 14px;
}
.sess-lbl {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: .8px; color: #94a3b8;
}
.timer {
  font-size: 22px; font-weight: 600; font-variant-numeric: tabular-nums;
  color: #1e293b; font-family: 'SF Mono', Menlo, monospace;
}
.timer.warn { color: #d97706; }

.grid {
  width: 100%;
  display: grid; grid-template-columns: 1fr 60px 1fr;
  gap: 10px; align-items: center;
  margin-bottom: 10px;
}

.panel {
  background: #fff; border: 1px solid #e2e8f0;
  border-radius: 12px; padding: 18px 10px;
  display: flex; flex-direction: column; align-items: center; gap: 7px;
  min-height: 162px; justify-content: center;
  transition: background .25s, border-color .25s;
}
.panel.ai-on  { background: #f0f9ff; border-color: rgba(14,165,233,.45); }
.panel.pa-on  { background: #fffbeb; border-color: rgba(245,158,11,.45); }

.p-ico {
  width: 48px; height: 48px; border-radius: 50%;
  background: #f1f5f9;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; color: #94a3b8;
  transition: color .25s, background .25s;
}
.panel.ai-on .p-ico { background: #fff; color: #0ea5e9; }
.panel.pa-on .p-ico { background: #fff; color: #d97706; }

.p-name { font-size: 12px; font-weight: 600; color: #1e293b; }
.p-st   { font-size: 11px; color: #94a3b8; text-align: center; min-height: 14px; transition: color .2s; }
.panel.ai-on .p-st { color: #0284c7; }
.panel.pa-on .p-st { color: #b45309; }

.ctr {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  height: 162px; gap: 8px;
}

.wave { display: flex; align-items: center; gap: 3px; height: 28px; }
.wbar { width: 3px; border-radius: 2px; background: #e2e8f0; height: 4px; }
.wbar:nth-child(1) { animation-delay: .00s; }
.wbar:nth-child(2) { animation-delay: .12s; }
.wbar:nth-child(3) { animation-delay: .24s; }
.wbar:nth-child(4) { animation-delay: .12s; }
.wbar:nth-child(5) { animation-delay: .00s; }
.wave.ai-wave .wbar { background:#0ea5e9; animation:wv .85s ease-in-out infinite; }
.wave.pa-wave .wbar { background:#f59e0b; animation:wv .60s ease-in-out infinite; }
@keyframes wv { 0%,100%{height:4px;} 50%{height:24px;} }

.spin {
  display: none; width: 20px; height: 20px;
  border: 2px solid #e2e8f0; border-top-color: #0ea5e9;
  border-radius: 50%; animation: rot .7s linear infinite;
}
@keyframes rot { to { transform:rotate(360deg); } }

.status-p  {
  width:100%; text-align:center; font-size:12px;
  color:#94a3b8; min-height:15px; margin-bottom:6px;
}
.irow { min-height:26px; display:flex; align-items:center; justify-content:center; margin-bottom:12px; }
.ipill {
  display:none;
  background:#f8fafc; border:1px solid #e2e8f0; border-radius:50px;
  padding:3px 11px; font-size:11px; color:#64748b; font-style:italic;
  max-width:100%; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}

.btn-end { color:#64748b; border-color:#e2e8f0; }
.btn-end:hover { background:#f1f5f9; }

/* ── END ── */
.end-logo {
  width: 58px; height: 58px; border-radius: 50%;
  background: #f0fdf4; border: 1px solid rgba(34,197,94,.3);
  display: flex; align-items: center; justify-content: center;
  font-size: 24px; color: #16a34a;
  margin-bottom: 12px;
}
</style>
</head>
<body>
<div id="app">

  <!-- INTRO -->
  <div id="s-intro" class="screen on">
    <div class="intro-logo"><i class="ti ti-microphone"></i></div>
    <h1>Discourse Assessment</h1>
    <span class="badge">Section I — First Encounter</span>
    <p class="sub">Voice-only protocol. No typing required.<br>The AI partner has no prepared questions.</p>
    <div class="info-box">
      <div class="lbl">Protocol Notes</div>
      <p>This is not an interview. Allow the participant to initiate topics and lead the conversation. Duration: approximately 5 minutes.</p>
    </div>
    <button onclick="startSession()">
      <i class="ti ti-player-play"></i>&nbsp; Begin Session
    </button>
    <p class="err" id="err"></p>
  </div>

  <!-- SESSION -->
  <div id="s-sess" class="screen">
    <div class="sess-hd">
      <span class="sess-lbl">First Encounter</span>
      <span class="timer" id="timer">0:00</span>
    </div>
    <div class="grid">
      <div class="panel" id="panel-ai">
        <div class="p-ico"><i class="ti ti-robot"></i></div>
        <div class="p-name">AI Partner</div>
        <div class="p-st" id="ai-st">Initializing</div>
      </div>
      <div class="ctr">
        <div class="wave" id="wave">
          <div class="wbar"></div><div class="wbar"></div><div class="wbar"></div>
          <div class="wbar"></div><div class="wbar"></div>
        </div>
        <div class="spin" id="spin"></div>
      </div>
      <div class="panel" id="panel-pa">
        <div class="p-ico"><i class="ti ti-microphone"></i></div>
        <div class="p-name">Participant</div>
        <div class="p-st" id="pa-st">Waiting</div>
      </div>
    </div>
    <p class="status-p" id="status"></p>
    <div class="irow"><div class="ipill" id="ipill"></div></div>
    <button class="btn-end" onclick="endSession()">End Session</button>
  </div>

  <!-- END -->
  <div id="s-end" class="screen">
    <div class="end-logo"><i class="ti ti-check"></i></div>
    <h1>Session Complete</h1>
    <p class="sub" style="margin-top:5px;">
      The First Encounter task has ended.<br>
      Proceed to the next section of the protocol.
    </p>
    <div style="margin-top:18px;">
      <button onclick="resetSession()">
        <i class="ti ti-refresh"></i>&nbsp; New Session
      </button>
    </div>
  </div>

</div>
<script>
/* ============================================================
   DISCOURSE ASSESSMENT — SECTION I: FIRST ENCOUNTER
   Voice-only chatbot  |  Streamlit-embedded version
   ============================================================ */

const API_KEY  = API_KEY_PLACEHOLDER;
const API_URL  = "https://api.anthropic.com/v1/messages";
const MAX_S    = 300;     // 5-minute session limit
const SIL_MS   = 2500;    // silence before processing turn
const LONG_SIL = 11000;   // silence before "take your time" prompt

const OPENING =
  "Hello. I don't think we've met before. " +
  "So maybe we can start by getting to know each other a little. " +
  "This isn't an interview, so I don't have a list of questions prepared. " +
  "We can just chat casually and get to know each other.";

const SYS =
  "You are participating in the First Encounter section of a clinical discourse assessment. " +
  "Engage in natural casual conversation as if meeting this person for the first time.\\n\\n" +
  "RULES:\\n" +
  "- NOT an interview: you have no prepared question list\\n" +
  "- Let the participant lead; follow their topics\\n" +
  "- Keep responses VERY SHORT: 1 to 2 sentences maximum\\n" +
  "- Be warm, genuine, natural\\n" +
  "- Never ask more than one question at a time\\n" +
  "- Respond only with spoken words: no stage directions, no descriptions\\n" +
  "- Minimal verbal fillers; brief silences are normal\\n" +
  "- Do not reference the assessment";

let phase = 'idle', hist = [], recog = null, recogOn = false;
let tid = null, secs = 0, silT = null, longT = null, curTx = '';
let voices = [], bugT = null;

const $ = id => document.getElementById(id);

function qShow(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('on'));
  $(id).classList.add('on');
}

function setPanel(who, active) {
  const el = $(who === 'ai' ? 'panel-ai' : 'panel-pa');
  el.className = 'panel' + (active ? (' ' + (who === 'ai' ? 'ai-on' : 'pa-on')) : '');
  const st = $(who === 'ai' ? 'ai-st' : 'pa-st');
  if (who === 'ai')
    st.textContent = active ? 'Speaking\u2026' : (phase === 'processing' ? 'Thinking\u2026' : 'Listening');
  else
    st.textContent = active ? 'Speaking\u2026' : 'Your turn';
}

function setWave(m) {
  const w = $('wave'), sp = $('spin');
  w.style.display = 'flex'; sp.style.display = 'none';
  w.className = 'wave' + (m === 'ai' ? ' ai-wave' : m === 'pa' ? ' pa-wave' : '');
  if (m === 'proc') { w.style.display = 'none'; sp.style.display = 'block'; }
}

function setStatus(t) { $('status').textContent = t; }

function setInterim(t) {
  const el = $('ipill');
  if (t) { el.textContent = t; el.style.display = 'block'; }
  else   { el.style.display = 'none'; el.textContent = ''; }
}

/* TIMER */
function startTimer() {
  secs = 0;
  tid = setInterval(() => {
    secs++;
    const el = $('timer');
    el.textContent = Math.floor(secs / 60) + ':' + String(secs % 60).padStart(2, '0');
    el.className = 'timer' + (secs >= MAX_S - 30 ? ' warn' : '');
    if (secs >= MAX_S) endSession();
  }, 1000);
}

/* VOICES */
function loadVoices() { voices = window.speechSynthesis.getVoices(); }
function pickVoice() {
  const pref = ['Samantha', 'Karen', 'Moira', 'Google US English Female',
                'Microsoft Aria', 'Aria Online', 'Zira'];
  for (const n of pref) {
    const v = voices.find(v => v.name.includes(n));
    if (v) return v;
  }
  return voices.find(v => v.lang && v.lang.startsWith('en')) || null;
}

/* TTS */
function speak(text, done) {
  clearInterval(bugT);
  window.speechSynthesis.cancel();
  phase = 'speaking';
  setPanel('ai', true); setPanel('pa', false); setWave('ai');
  setStatus('AI partner is speaking\u2026');

  const utt = new SpeechSynthesisUtterance(text);
  utt.rate = 0.92; utt.pitch = 1.0; utt.volume = 1.0;
  const v = pickVoice(); if (v) utt.voice = v;

  // Chrome TTS pause-after-15s bug workaround
  utt.onstart = () => {
    bugT = setInterval(() => {
      window.speechSynthesis.pause();
      window.speechSynthesis.resume();
    }, 9000);
  };
  utt.onend  = () => { clearInterval(bugT); setPanel('ai', false); setWave(null); if (done) done(); };
  utt.onerror = () => { clearInterval(bugT); setPanel('ai', false); setWave(null); if (done) done(); };

  window.speechSynthesis.speak(utt);
}

/* STT */
function initSTT() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) return false;
  recog = new SR();
  recog.continuous = true; recog.interimResults = true; recog.lang = 'en-US';

  recog.onstart = () => {
    recogOn = true; phase = 'listening';
    setPanel('pa', false); setWave('pa');
    setStatus('Listening for participant\u2026');
    $('pa-st').textContent = 'Listening\u2026';
  };

  recog.onresult = evt => {
    let interim = '';
    for (let i = evt.resultIndex; i < evt.results.length; i++) {
      const t = evt.results[i][0].transcript;
      if (evt.results[i].isFinal) {
        curTx += t + ' ';
        clearTimeout(silT); clearTimeout(longT);
        setPanel('pa', true);
        silT = setTimeout(() => {
          if (curTx.trim() && phase === 'listening') { stopSTT(); processTurn(curTx.trim()); }
        }, SIL_MS);
        longT = setTimeout(() => {
          if (phase === 'listening') setStatus('Take your time\u2026');
        }, LONG_SIL);
      } else {
        interim = t;
      }
    }
    setInterim(interim || '');
    if (interim) setPanel('pa', true);
  };

  recog.onend = () => {
    recogOn = false;
    if (phase === 'listening' && !curTx.trim())
      setTimeout(() => { if (phase === 'listening') safeStart(); }, 600);
  };

  recog.onerror = e => {
    recogOn = false;
    if (e.error === 'not-allowed') {
      setStatus('Microphone permission denied \u2014 allow access and reload.'); return;
    }
    if (phase === 'listening') setTimeout(() => { if (phase === 'listening') safeStart(); }, 1000);
  };

  return true;
}

function safeStart() { if (recogOn) return; try { recog.start(); } catch (_) {} }

function stopSTT() {
  clearTimeout(silT); clearTimeout(longT);
  try { recog.stop(); } catch (_) {}
  recogOn = false; setInterim('');
}

function listenForParticipant() {
  curTx = ''; setInterim(''); phase = 'listening';
  setPanel('pa', false); setWave(null);
  setStatus("Participant's turn\u2026");
  longT = setTimeout(() => {
    if (phase === 'listening') setStatus('Take your time\u2026');
  }, LONG_SIL);
  safeStart();
}

/* API call */
async function processTurn(text) {
  if (phase === 'ended') return;
  phase = 'processing';
  setPanel('ai', false); setPanel('pa', false); setWave('proc');
  setStatus('Processing\u2026'); $('ai-st').textContent = 'Thinking\u2026';
  hist.push({ role: 'user', content: text });

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY,
        'anthropic-version': '2023-06-01',
        'anthropic-dangerous-direct-browser-access': 'true'
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-6',
        max_tokens: 180,
        system: SYS,
        messages: hist
      })
    });

    const data = await res.json();

    if (data?.content?.[0]?.text) {
      const reply = data.content[0].text.trim();
      hist.push({ role: 'assistant', content: reply });
      speak(reply, () => { if (phase !== 'ended') listenForParticipant(); });
    } else {
      if (phase !== 'ended') listenForParticipant();
    }
  } catch (err) {
    setStatus('Connection issue \u2014 resuming\u2026');
    setTimeout(() => { if (phase !== 'ended') listenForParticipant(); }, 2000);
  }
}

/* Session control */
function startSession() {
  if (!initSTT()) {
    const el = $('err');
    el.textContent = 'Speech recognition not supported. Please use Chrome or Edge.';
    el.style.display = 'block'; return;
  }
  $('panel-ai').className = 'panel'; $('panel-pa').className = 'panel';
  $('ai-st').textContent = 'Initializing'; $('pa-st').textContent = 'Waiting';
  setWave(null); setStatus('Preparing session\u2026'); setInterim('');
  hist = [{ role: 'assistant', content: OPENING }];
  qShow('s-sess');
  startTimer();
  speak(OPENING, () => { if (phase !== 'ended') listenForParticipant(); });
}

function endSession() {
  phase = 'ended';
  stopSTT(); clearInterval(tid); clearInterval(bugT);
  window.speechSynthesis.cancel();
  qShow('s-end');
}

function resetSession() {
  phase = 'idle'; hist = []; secs = 0; curTx = '';
  $('timer').textContent = '0:00'; $('timer').className = 'timer';
  qShow('s-intro');
}

/* Init */
if (typeof speechSynthesis !== 'undefined') {
  speechSynthesis.addEventListener('voiceschanged', loadVoices);
  loadVoices();
}
</script>
</body>
</html>"""

# Safely inject the API key as a JSON-encoded JS string
HTML = CHATBOT_HTML.replace("API_KEY_PLACEHOLDER", json.dumps(api_key))

st.components.v1.html(HTML, height=530, scrolling=False)

st.divider()
st.caption(
    "⚠️ **Browser note:** Speech recognition requires Chrome or Edge. "
    "The mic permission prompt appears once, on first session start. "
    "This app is intended for local or controlled internal use."
)
