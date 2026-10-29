import { api } from './api.js';
const $ = (id) => document.getElementById(id);

export function initImport(onChange) {
  $('form-card').onsubmit = async (e) => {
    e.preventDefault();
    await api.addCard(Object.fromEntries(new FormData(e.target)));
    e.target.reset(); $('import-msg').textContent = 'Tarjeta guardada.'; onChange();
  };
  $('csv-file').onchange = async (e) => {
    const res = await api.importCsv(e.target.files[0]);
    $('import-msg').textContent = `${res.imported} tarjetas importadas.`; onChange();
  };
}
