// ChatGPT image queue ("pump"), pasted into a chatgpt.com tab via Claude in Chrome (javascript_tool).
// Not loadable with eval (chatgpt.com CSP) — paste the whole file, then load references + queue through file inputs:
//
//   1. Open a NEW chat (fresh chat = no drift from earlier images). Paste this file.
//   2. __addPicker('refs')  -> file_upload references/style_ref_master.jpg (+ character sheets) into it
//      __addPicker('queue') -> file_upload batches/<queue>.json ([{name, text}], each text is a FULL prompt)
//   3. __startPump()   — every message re-attaches ALL refs (window.__REFS) and sends the next prompt.
//
// Completion is detected from the image LIBRARY feed (/backend-api/my/recent/image_gen) — /backend-api/conversation
// returns 429 when polled. Items are matched by conversation id + created_at > last send time.
// Status:  JSON.stringify({idx: B2.idx, log: B2.log.slice(-4)})     Stop:  __stopPump()
// Download: await __dlResults('prefix')  -> ~/Downloads/prefix_bundle.bin ; locally: python3 scripts/unbundle_strips.py prefix
// Gotchas (2026-10-11..15):
//  - a new chat first shows a temporary 'local-chatgpt:…' id that never matches the library -> only accept real UUIDs
//    (13 images were wasted before this guard);
//  - reference upload sometimes shows "Upload failed": rebuild fresh File objects from ArrayBuffers every send, remove
//    the failed chip and retry;
//  - the composer can hold a leftover draft — send() clears it; a stuck "Stop" button is clicked first;
//  - background tabs throttle setTimeout chains: use setInterval polling and start runs manually, not on a schedule;
//  - the Chrome tab group can disappear: reopen the chat URL; finished images are still in the library.

const W = (ms) => new Promise(r => setTimeout(r, ms));
// the visible composer form — after 'New chat' (SPA) ChatGPT keeps hidden old composer forms; always target the visible one
window.__form = () => { const eds=[...document.querySelectorAll('[contenteditable="true"]')].filter(e=>e.offsetParent); const ed=eds[eds.length-1]; return ed ? ed.closest('form') : null; };
window.__addPicker = (kind) => {
  const q = document.createElement('input'); q.type = 'file'; q.multiple = kind === 'refs'; q.id = '__pick_' + kind;
  q.style.cssText = 'position:fixed;top:4px;left:4px;z-index:99999'; q.setAttribute('aria-label', kind === 'refs' ? 'PICKREFS' : 'PICKQUEUE');   // findable for file_upload
  q.onchange = async () => {
    if (kind === 'refs') window.__REFS = await Promise.all([...q.files].map(async f => ({name: f.name, type: f.type, buf: await f.arrayBuffer()})));
    else window.__Q = JSON.parse(await q.files[0].text());
  };
  document.body.appendChild(q); return '#__pick_' + kind;
};

async function attach() {
  const refs = window.__REFS || []; if (!refs.length) return 'no refs';
  for (let tryN = 0; tryN < 3; tryN++) {
    const inp = (window.__form() || document).querySelector('input[type=file][accept*=image]');   // the LIVE composer's input (SPA new chats leave stale forms behind)
    if (!inp) return 'no input';
    const dt = new DataTransfer();
    refs.forEach(r => dt.items.add(new File([r.buf.slice(0)], r.name, {type: r.type || 'image/png'})));
    inp.files = dt.files; inp.dispatchEvent(new Event('change', {bubbles: true}));
    await W(6000);
    // VERIFY, never assume (2026-10-18: ChatGPT's "limit for file attachments" banner made every upload silently drop and
    // a whole batch went out WITHOUT the style ref / character sheet). Count the attachment chips the composer shows.
    if (/limit for file attachments/i.test(document.body.innerText)) return 'attach FAILED: attachment limit';
    const chips = (window.__form() || document).querySelectorAll('button[aria-label^="Remove"], [data-testid*="attachment"]').length;
    if (chips >= refs.length && !/upload failed/i.test(document.body.innerText.slice(-4000))) return 'attached ok';
    document.querySelectorAll('button[aria-label^="Remove"]').forEach(b => b.click()); await W(2000);
  }
  return 'attach FAILED';
}

window.__startPump = (Q = window.__Q) => {
  const st = window.B2 = {queue: Q, idx: 0, results: {}, retries: 0, lastSend: 0, log: [], downloaded: {}};
  st.send = async (t) => {
    const s = document.querySelector('button[aria-label="Stop"]'); if (s) { s.click(); await W(2500); }
    const at = await attach();
    if (at !== 'attached ok') { st.log.push('NOT SENT ' + (st.queue[st.idx]?.name) + ': ' + at); st.done = true; st.halted = at; return; }   // never send a prompt without its refs
    const f = window.__form(); const e = f.querySelector('[contenteditable="true"]'); e.focus();
    document.execCommand('selectAll', false); document.execCommand('delete', false); document.execCommand('insertText', false, t);
    let r = 'timeout';
    for (let k = 0; k < 40; k++) {
      await W(1000);
      const b = window.__form().querySelector('#composer-submit-button, button[aria-label="Send prompt"], button[aria-label="Send"], button[type="submit"]');
      if (b && !b.disabled) { b.click(); r = 'ok'; break; }
    }
    st.lastSend = Date.now(); await W(3000);
    st.log.push('sent ' + st.queue[st.idx]?.name + ' ' + at + ' ' + r + ' ' + new Date().toLocaleTimeString());
  };
  const poll = async () => {
    const tok = (await (await fetch('/api/auth/session')).json()).accessToken;
    const r = await fetch('/backend-api/my/recent/image_gen?limit=40', {headers: {Authorization: 'Bearer ' + tok}});
    if (!r.ok) return [];
    return (await r.json()).items.map(i => ({cid: i.conversation_id, t: i.created_at * 1000, ptr: i.asset_pointer, title: i.title}));
  };
  st.timer = setInterval(async () => {
    if (st.done || st.busy) return;
    const c = location.pathname.split('/c/')[1];
    if (!c || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(c)) return;
    st.cid = c; st.busy = true;
    try {
      const mine = (await poll()).filter(i => i.cid === st.cid && i.t > st.lastSend).sort((a, b) => b.t - a.t);
      const name = st.queue[st.idx].name;
      if (mine.length) {
        st.results[name] = mine[0].ptr; st.idx++; st.retries = 0; st.downloaded[name] = 0;
        st.log.push('got ' + name + ' ' + new Date().toLocaleTimeString());
        if (st.idx < st.queue.length) await st.send(st.queue[st.idx].text); else { st.done = true; st.log.push('DONE'); }
      } else if (Date.now() - st.lastSend > 8 * 60000) {
        if (/limit|try again (later|in)/i.test(document.body.innerText.slice(-3000))) { st.log.push('LIMIT? ' + name); st.lastSend = Date.now(); return; }
        if (st.retries < 2) { st.retries++; st.log.push('timeout ' + name); await st.send('Please generate the image for this frame now (one image).'); }
        else { st.results[name] = 'FAILED: timeout'; st.idx++; st.retries = 0; if (st.idx < st.queue.length) await st.send(st.queue[st.idx].text); else st.done = true; }
      }
    } finally { st.busy = false; }
  }, 30000);
  // first message: the new chat has no UUID yet, so send it directly
  st.send(st.queue[0].text);
  return 'started ' + Q.length;
};
window.__stopPump = () => { clearInterval(window.B2?.timer); if (window.B2) window.B2.done = true; return 'stopped'; };

// Downloads every not-yet-downloaded image of this run as one bundle: 10-char byte-length header + JSON [{name,size}] + blobs.
window.__dlResults = async (prefix) => {
  const c = B2.cid || location.pathname.split('/c/')[1];
  const k = (await (await fetch('/api/auth/session')).json()).accessToken, H = {Authorization: 'Bearer ' + k}, bl = [], me = [];
  for (const [n, ptr] of Object.entries(B2.results)) {
    if (B2.downloaded[n] || ptr.startsWith('FAILED')) continue;
    const d = await (await fetch('/backend-api/files/download/' + ptr.replace(/^.*:\/\//, '') + '?conversation_id=' + c, {headers: H})).json();
    const b = await (await fetch(d.download_url)).blob(); bl.push(b); me.push({name: n + '.png', size: b.size}); B2.downloaded[n] = 1;
  }
  if (!bl.length) return 'nothing new';
  const en = new TextEncoder().encode(JSON.stringify(me));
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([String(en.length).padStart(10, '0'), en, ...bl]));
  a.download = prefix + '_bundle.bin'; document.body.appendChild(a); a.click(); a.remove();
  return me.map(x => x.name);
};
