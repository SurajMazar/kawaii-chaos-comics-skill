// One-image-per-topic sender (2026-10-21). Paste into a fresh chatgpt.com tab.
// 1) adds a PICKQ file input: upload a job JSON [{name, text}]  2) attach the ref image with the composer's "Attach photos" input
// 3) await __send1('<outName>')  -> refuses without an attachment chip, sends, checks the conversation record holds the image,
//    waits until generation is DONE (ChatGPT may make 2 images per prompt — takes the LAST), downloads <outName>_bundle.bin.
//    __edit1('<outName>', text) sends a follow-up edit in the same chat the same way.
(() => {
  const i = document.createElement('input'); i.type = 'file'; i.id = '__pick_q'; i.setAttribute('aria-label', 'PICKQ');
  i.style.cssText = 'position:fixed;top:4px;left:4px;z-index:99999';
  i.onchange = async () => { window.__JOB = JSON.parse(await i.files[0].text())[0]; };
  document.body.appendChild(i);
  const W = ms => new Promise(r => setTimeout(r, ms));
  const send = async (text, needAttach) => {
    if (needAttach && document.querySelectorAll('button[aria-label^="Remove"]').length < 1) return 'no attachment';
    const e = [...document.querySelectorAll('[contenteditable="true"]')].filter(x => x.offsetParent).pop(); e.focus();
    document.execCommand('selectAll', false); document.execCommand('delete', false); document.execCommand('insertText', false, text);
    let b = null;
    for (let k = 0; k < 20 && !b; k++) { await W(1000); b = document.querySelector('#composer-submit-button, button[data-testid="send-button"], form button[aria-label="Send"], button[aria-label="Send prompt"]'); if (b && b.disabled) b = null; }
    if (!b) return 'no send button'; b.click(); return 'sent';
  };
  const waitDl = async (outName, t0) => {
    const cid = location.pathname.split('/c/')[1]; const tok = (await (await fetch('/api/auth/session')).json()).accessToken; const H = {headers: {Authorization: 'Bearer ' + tok}};
    let last = null, lastT = 0;
    while (Date.now() - t0 < 12 * 60000) {
      await W(15000); const q = await fetch('/backend-api/my/recent/image_gen?limit=20', H); if (!q.ok) continue;
      const it = (await q.json()).items.filter(x => x.conversation_id === cid && x.created_at * 1000 > t0 - 5000);
      const busy = !!document.querySelector('button[data-testid="stop-button"], button[aria-label*="Stop"]');
      if (it.length) { if (!last || it[0].id !== last.id) { last = it[0]; lastT = Date.now(); } if (!busy && Date.now() - lastT > 40000) break; }
    }
    if (!last) { window.__DLR = 'no image'; return; }
    const d = await (await fetch('/backend-api/files/download/' + last.asset_pointer.replace(/^.*:\/\//, '') + '?conversation_id=' + cid, H)).json();
    const bl = await (await fetch(d.download_url)).blob(); const me = [{name: outName + '.png', size: bl.size}]; const en = new TextEncoder().encode(JSON.stringify(me));
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([String(en.length).padStart(10, '0'), en, bl])); a.download = outName + '_bundle.bin'; document.body.appendChild(a); a.click(); a.remove();
    window.__DLR = 'ok';
  };
  window.__send1 = async (outName) => {
    await W(2000); if (!window.__JOB) return 'no job';
    const t0 = Date.now(); const r = await send(window.__JOB.text, true); if (r !== 'sent') return r;
    await W(9000); const cid = location.pathname.split('/c/')[1];
    const tok = (await (await fetch('/api/auth/session')).json()).accessToken;
    const cv = await (await fetch('/backend-api/conversation/' + cid, {headers: {Authorization: 'Bearer ' + tok}})).json();
    const us = Object.values(cv.mapping || {}).map(n => n.message).filter(m => m && m.author && m.author.role === 'user');
    const prov = ((us[0] && us[0].content && us[0].content.parts) || []).filter(p => typeof p === 'object' && p.content_type === 'image_asset_pointer').length;
    window.__DLR = 'waiting'; waitDl(outName, t0);
    return JSON.stringify({cid, refsInRecord: prov});
  };
  window.__edit1 = async (outName, text) => { const t0 = Date.now(); const r = await send(text, false); if (r !== 'sent') return r; window.__DLR = 'waiting'; waitDl(outName, t0); return 'sent edit'; };
  return 'send1 ready';
})();
