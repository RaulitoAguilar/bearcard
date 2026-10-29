import { api } from './api.js';
import { initStudy } from './study.js';
import { initImport } from './import.js';
import { loadHistory } from './history.js';

const select = document.getElementById('topic-select');

async function loadTopics() {
  const topics = await api.topics();
  select.innerHTML = topics.map((t) => `<option>${t}</option>`).join('');
}

initStudy(() => select.value, loadHistory);
initImport(loadTopics);
loadTopics();
loadHistory();
