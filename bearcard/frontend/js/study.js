import { api } from './api.js';
const $ = (id) => document.getElementById(id);
let queue = [], current = null, shownAt = 0;

export function initStudy(getTopic, onAnswered) {
  const show = (reveal) => {
    $('card-answer').hidden = !reveal;
    $('btn-reveal').hidden = reveal || !current;
    $('btn-hit').hidden = $('btn-miss').hidden = !reveal;
  };
  const next = () => {
    current = queue.shift();
    $('card').hidden = !current;
    if (!current) { $('study-meta').textContent = 'Sesión terminada.'; show(false); return; }
    $('card-question').textContent = current.question;
    $('card-answer').textContent = current.answer;
    $('study-meta').textContent = `Riesgo de error: ${Math.round(current.risk * 100)}% (${current.source})`;
    shownAt = Date.now(); show(false);
  };
  const answer = async (ok) => {
    await api.answer(current.id, ok, Date.now() - shownAt);
    onAnswered(); next();
  };
  $('btn-start').onclick = async () => { queue = await api.session(getTopic()); next(); };
  $('btn-reveal').onclick = () => show(true);
  $('btn-hit').onclick = () => answer(true);
  $('btn-miss').onclick = () => answer(false);
}
