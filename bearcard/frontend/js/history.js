import { api } from './api.js';

export async function loadHistory() {
  const rows = await api.history();
  document.getElementById('history-body').innerHTML = rows.map((r) =>
    `<tr><td>${esc(r.topic)}</td><td>${esc(r.question)}</td>
     <td class="${r.correct ? 'hit' : 'miss'}">${r.correct ? 'Acierto' : 'Error'}</td>
     <td>${(r.time_ms / 1000).toFixed(1)} s</td></tr>`).join('');
}
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
