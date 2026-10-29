const j = (r) => r.json();
export const api = {
  topics: () => fetch('/api/topics').then(j),
  session: (topic) => fetch(`/api/session?topic=${encodeURIComponent(topic)}`).then(j),
  answer: (card_id, correct, time_ms) =>
    fetch('/api/answer', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ card_id, correct, time_ms }) }).then(j),
  addCard: (card) =>
    fetch('/api/cards', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(card) }).then(j),
  importCsv: (file) => {
    const fd = new FormData(); fd.append('file', file);
    return fetch('/api/import', { method: 'POST', body: fd }).then(j);
  },
  history: () => fetch('/api/history').then(j),
};
