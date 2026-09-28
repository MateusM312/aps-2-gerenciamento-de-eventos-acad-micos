/* =========================================================
   Configuração
   Se o front for servido pela própria FastAPI (StaticFiles),
   troque para API_BASE = "" (string vazia) e use caminhos relativos.
   ========================================================= */
const API_BASE = "http://127.0.0.1:8000";

const CATEGORIAS = ["Palestra", "Workshop", "Minicurso", "Seminário", "Competição"];

/* =========================================================
   Estado em memória
   ========================================================= */
const state = {
  eventos: [],
  participantes: [],
  eventoSelecionadoId: null,
  participanteSelecionadoId: null,
};

/* =========================================================
   Helpers de rede
   ========================================================= */
async function apiRequest(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  let body = null;
  const text = await res.text();
  if (text) {
    try { body = JSON.parse(text); } catch { body = text; }
  }

  if (!res.ok) {
    const detail = (body && body.detail) ? body.detail : `Erro ${res.status}`;
    throw new Error(detail);
  }
  return body;
}

async function checkApiStatus() {
  const dot = document.getElementById("apiDot");
  const text = document.getElementById("apiStatusText");
  try {
    await apiRequest("/eventos/");
    dot.className = "dot ok";
    text.textContent = "conectado à API";
  } catch (e) {
    dot.className = "dot fail";
    text.textContent = "sem conexão com a API — verifique se o uvicorn está rodando";
  }
}

/* =========================================================
   Toast
   ========================================================= */
let toastTimer = null;
function showToast(message, isError = false) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.toggle("is-error", isError);
  toast.classList.add("is-visible");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("is-visible"), 3200);
}

/* =========================================================
   Tabs
   ========================================================= */
document.querySelectorAll(".tab").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => {
      b.classList.remove("is-active");
      b.setAttribute("aria-selected", "false");
    });
    btn.classList.add("is-active");
    btn.setAttribute("aria-selected", "true");

    const target = btn.dataset.tab;
    document.querySelectorAll(".panel").forEach((p) => {
      p.classList.toggle("is-hidden", p.dataset.panel !== target);
    });
  });
});

/* =========================================================
   Modais — abrir / fechar
   ========================================================= */
function openModal(id) { document.getElementById(id).classList.add("is-open"); }
function closeModal(id) { document.getElementById(id).classList.remove("is-open"); }

document.querySelectorAll("[data-close]").forEach((el) => {
  el.addEventListener("click", () => closeModal(el.dataset.close));
});
document.querySelectorAll(".modal-backdrop").forEach((bg) => {
  bg.addEventListener("click", (e) => {
    if (e.target === bg) bg.classList.remove("is-open");
  });
});

/* =========================================================
   EVENTOS — carregar e listar
   ========================================================= */
async function loadEventos() {
  const lista = document.getElementById("listaEventos");
  try {
    state.eventos = await apiRequest("/eventos/") || [];
    renderEventos();
  } catch (e) {
    lista.innerHTML = `<li class="empty-state">Não foi possível carregar os eventos.<br>${e.message}</li>`;
  }
}

function renderEventos() {
  const lista = document.getElementById("listaEventos");
  const termo = document.getElementById("filtroEventos").value.trim().toLowerCase();

  const filtrados = state.eventos.filter((ev) =>
    ev.titulo.toLowerCase().includes(termo) || ev.categoria.toLowerCase().includes(termo)
  );

  if (filtrados.length === 0) {
    lista.innerHTML = `<li class="empty-state">Nenhum evento encontrado.</li>`;
    return;
  }

  lista.innerHTML = "";
  filtrados
    .slice()
    .sort((a, b) => (a.data || "").localeCompare(b.data || ""))
    .forEach((ev) => {
      const li = document.createElement("li");
      li.className = "card" + (ev.id === state.eventoSelecionadoId ? " is-selected" : "");
      li.innerHTML = `
        <div class="card__top">
          <div>
            <p class="card__title">${escapeHtml(ev.titulo)}</p>
            <p class="card__meta">${formatarData(ev.data)} · ${ev.horario || ""}</p>
          </div>
          <span class="tag">${escapeHtml(ev.categoria)}</span>
        </div>
        <div class="card__foot">
          <span>📍 ${escapeHtml(ev.local)}</span>
          <span>🎟️ ${ev.capacidade} vagas</span>
        </div>
      `;
      li.addEventListener("click", () => selectEvento(ev.id));
      lista.appendChild(li);
    });
}

document.getElementById("filtroEventos").addEventListener("input", renderEventos);

/* =========================================================
   EVENTOS — detalhe + inscrições
   ========================================================= */
async function selectEvento(id) {
  state.eventoSelecionadoId = id;
  renderEventos();

  const detalhe = document.getElementById("detalheEvento");
  detalhe.innerHTML = `<div class="empty-detail"><p>Carregando evento…</p></div>`;

  try {
    const ev = await apiRequest(`/eventos/${id}`);
    const inscritos = await apiRequest(`/eventos/${id}/inscricoes`).catch(() => []);
    renderDetalheEvento(ev, inscritos || []);
  } catch (e) {
    detalhe.innerHTML = `<div class="empty-detail"><p>Não foi possível carregar este evento.</p><p>${e.message}</p></div>`;
  }
}

function renderDetalheEvento(ev, inscritos) {
  const detalhe = document.getElementById("detalheEvento");
  const vagasRestantes = ev.capacidade - inscritos.length;
  const tagVagas = vagasRestantes <= 0
    ? `<span class="tag tag--cheio">Sem vagas</span>`
    : `<span class="tag tag--vagas">${vagasRestantes} vaga${vagasRestantes === 1 ? "" : "s"} restante${vagasRestantes === 1 ? "" : "s"}</span>`;

  const opcoesParticipantes = state.participantes
    .filter((p) => !inscritos.some((i) => i.id === p.id))
    .map((p) => `<option value="${p.id}">${escapeHtml(p.nome)} — ${escapeHtml(p.curso)}</option>`)
    .join("");

  detalhe.innerHTML = `
    <div class="detail-head">
      <div>
        <h3>${escapeHtml(ev.titulo)}</h3>
        <span class="tag">${escapeHtml(ev.categoria)}</span>
        ${tagVagas}
      </div>
      <div class="detail-actions">
        <button class="btn btn--ghost btn--sm" id="btnEditarEvento">Editar</button>
        <button class="btn btn--danger btn--sm" id="btnExcluirEvento">Excluir</button>
      </div>
    </div>

    <div class="detail-grid">
      <div class="detail-field"><label>Data</label><div>${formatarData(ev.data)}</div></div>
      <div class="detail-field"><label>Horário</label><div>${ev.horario}</div></div>
      <div class="detail-field"><label>Local</label><div>${escapeHtml(ev.local)}</div></div>
      <div class="detail-field"><label>Capacidade</label><div>${ev.capacidade} pessoas</div></div>
    </div>

    <p class="detail-desc">${escapeHtml(ev.descricao)}</p>

    <h4 class="section-title">Participantes inscritos (${inscritos.length})</h4>
    <ul class="inscritos-list" id="listaInscritos">
      ${inscritos.length === 0
        ? `<li class="empty-state">Ninguém inscrito ainda.</li>`
        : inscritos.map((p) => `
            <li class="inscrito-row">
              <span>${escapeHtml(p.nome)} <span class="curso">— ${escapeHtml(p.curso)}</span></span>
            </li>`).join("")}
    </ul>

    <div class="inscrever-row">
      <select id="selectParticipanteInscrever" ${vagasRestantes <= 0 ? "disabled" : ""}>
        <option value="" disabled selected>
          ${vagasRestantes <= 0 ? "Evento sem vagas" : "Selecionar participante…"}
        </option>
        ${opcoesParticipantes}
      </select>
      <button class="btn btn--primary btn--sm" id="btnInscrever" ${vagasRestantes <= 0 ? "disabled" : ""}>
        Inscrever
      </button>
    </div>
  `;

  document.getElementById("btnEditarEvento").addEventListener("click", () => openEventoModal(ev));
  document.getElementById("btnExcluirEvento").addEventListener("click", () => excluirEvento(ev.id));
  document.getElementById("btnInscrever").addEventListener("click", () => inscreverParticipante(ev.id));
}

async function inscreverParticipante(eventoId) {
  const select = document.getElementById("selectParticipanteInscrever");
  const participanteId = select.value;
  if (!participanteId) {
    showToast("Selecione um participante primeiro.", true);
    return;
  }
  try {
    await apiRequest(`/eventos/${eventoId}/inscricoes/${participanteId}`, { method: "POST" });
    showToast("Inscrição realizada com sucesso.");
    selectEvento(eventoId);
  } catch (e) {
    showToast(e.message, true);
  }
}

async function excluirEvento(id) {
  if (!confirm("Excluir este evento? Essa ação não pode ser desfeita.")) return;
  try {
    await apiRequest(`/eventos/${id}`, { method: "DELETE" });
    showToast("Evento removido.");
    state.eventoSelecionadoId = null;
    document.getElementById("detalheEvento").innerHTML =
      `<div class="empty-detail"><p>Selecione um evento na lista para ver os detalhes,</p><p>ou cadastre um novo evento.</p></div>`;
    await loadEventos();
  } catch (e) {
    showToast(e.message, true);
  }
}

/* =========================================================
   EVENTOS — modal de criação/edição
   ========================================================= */
function openEventoModal(ev = null) {
  const form = document.getElementById("formEvento");
  form.reset();
  document.getElementById("eventoErro").textContent = "";

  document.getElementById("modalEventoTitulo").textContent = ev ? "Editar evento" : "Novo evento";
  document.getElementById("eventoId").value = ev ? ev.id : "";
  document.getElementById("eventoTitulo").value = ev ? ev.titulo : "";
  document.getElementById("eventoDescricao").value = ev ? ev.descricao : "";
  document.getElementById("eventoData").value = ev ? ev.data : "";
  document.getElementById("eventoHorario").value = ev ? ev.horario : "";
  document.getElementById("eventoLocal").value = ev ? ev.local : "";
  document.getElementById("eventoCapacidade").value = ev ? ev.capacidade : "";
  document.getElementById("eventoCategoria").value = ev ? ev.categoria : "";

  openModal("modalEventoBackdrop");
}

document.getElementById("btnNovoEvento").addEventListener("click", () => openEventoModal());

document.getElementById("formEvento").addEventListener("submit", async (e) => {
  e.preventDefault();
  const erroEl = document.getElementById("eventoErro");
  const btn = document.getElementById("eventoSalvarBtn");
  erroEl.textContent = "";

  const id = document.getElementById("eventoId").value;
  const payload = {
    titulo: document.getElementById("eventoTitulo").value.trim(),
    descricao: document.getElementById("eventoDescricao").value.trim(),
    data: document.getElementById("eventoData").value,
    horario: document.getElementById("eventoHorario").value,
    local: document.getElementById("eventoLocal").value.trim(),
    capacidade: Number(document.getElementById("eventoCapacidade").value),
    categoria: document.getElementById("eventoCategoria").value,
  };

  btn.disabled = true;
  try {
    if (id) {
      await apiRequest(`/eventos/${id}`, { method: "PUT", body: JSON.stringify(payload) });
      showToast("Evento atualizado.");
    } else {
      await apiRequest(`/eventos/`, { method: "POST", body: JSON.stringify(payload) });
      showToast("Evento cadastrado.");
    }
    closeModal("modalEventoBackdrop");
    await loadEventos();
    if (id) selectEvento(Number(id));
  } catch (e2) {
    erroEl.textContent = e2.message;
  } finally {
    btn.disabled = false;
  }
});

/* =========================================================
   PARTICIPANTES — carregar e listar
   ========================================================= */
async function loadParticipantes() {
  const lista = document.getElementById("listaParticipantes");
  try {
    state.participantes = await apiRequest("/participantes/") || [];
    renderParticipantes();
  } catch (e) {
    lista.innerHTML = `<li class="empty-state">Não foi possível carregar os participantes.<br>${e.message}</li>`;
  }
}

function renderParticipantes() {
  const lista = document.getElementById("listaParticipantes");
  const termo = document.getElementById("filtroParticipantes").value.trim().toLowerCase();

  const filtrados = state.participantes.filter((p) =>
    p.nome.toLowerCase().includes(termo) ||
    p.curso.toLowerCase().includes(termo) ||
    p.email.toLowerCase().includes(termo)
  );

  if (filtrados.length === 0) {
    lista.innerHTML = `<li class="empty-state">Nenhum participante encontrado.</li>`;
    return;
  }

  lista.innerHTML = "";
  filtrados.forEach((p) => {
    const li = document.createElement("li");
    li.className = "card" + (p.id === state.participanteSelecionadoId ? " is-selected" : "");
    li.innerHTML = `
      <div class="card__top">
        <div>
          <p class="card__title">${escapeHtml(p.nome)}</p>
          <p class="card__meta">${escapeHtml(p.curso)}</p>
        </div>
        <span class="tag">${escapeHtml(p.email)}</span>
      </div>
    `;
    li.addEventListener("click", () => selectParticipante(p.id));
    lista.appendChild(li);
  });
}

document.getElementById("filtroParticipantes").addEventListener("input", renderParticipantes);

/* =========================================================
   PARTICIPANTES — detalhe
   ========================================================= */
async function selectParticipante(id) {
  state.participanteSelecionadoId = id;
  renderParticipantes();

  const detalhe = document.getElementById("detalheParticipante");
  detalhe.innerHTML = `<div class="empty-detail"><p>Carregando participante…</p></div>`;

  try {
    const p = await apiRequest(`/participantes/${id}`);
    renderDetalheParticipante(p);
  } catch (e) {
    detalhe.innerHTML = `<div class="empty-detail"><p>Não foi possível carregar este participante.</p><p>${e.message}</p></div>`;
  }
}

function renderDetalheParticipante(p) {
  const detalhe = document.getElementById("detalheParticipante");
  detalhe.innerHTML = `
    <div class="detail-head">
      <div>
        <h3>${escapeHtml(p.nome)}</h3>
        <span class="tag">${escapeHtml(p.curso)}</span>
      </div>
      <div class="detail-actions">
        <button class="btn btn--ghost btn--sm" id="btnEditarParticipante">Editar</button>
        <button class="btn btn--danger btn--sm" id="btnExcluirParticipante">Excluir</button>
      </div>
    </div>
    <div class="detail-grid">
      <div class="detail-field"><label>E-mail</label><div>${escapeHtml(p.email)}</div></div>
      <div class="detail-field"><label>Curso</label><div>${escapeHtml(p.curso)}</div></div>
    </div>
  `;
  document.getElementById("btnEditarParticipante").addEventListener("click", () => openParticipanteModal(p));
  document.getElementById("btnExcluirParticipante").addEventListener("click", () => excluirParticipante(p.id));
}

async function excluirParticipante(id) {
  if (!confirm("Excluir este participante? Essa ação não pode ser desfeita.")) return;
  try {
    await apiRequest(`/participantes/${id}`, { method: "DELETE" });
    showToast("Participante removido.");
    state.participanteSelecionadoId = null;
    document.getElementById("detalheParticipante").innerHTML =
      `<div class="empty-detail"><p>Selecione um participante na lista para ver os detalhes,</p><p>ou cadastre um novo participante.</p></div>`;
    await loadParticipantes();
  } catch (e) {
    showToast(e.message, true);
  }
}

/* =========================================================
   PARTICIPANTES — modal de criação/edição
   ========================================================= */
function openParticipanteModal(p = null) {
  const form = document.getElementById("formParticipante");
  form.reset();
  document.getElementById("participanteErro").textContent = "";

  document.getElementById("modalParticipanteTitulo").textContent = p ? "Editar participante" : "Novo participante";
  document.getElementById("participanteId").value = p ? p.id : "";
  document.getElementById("participanteNome").value = p ? p.nome : "";
  document.getElementById("participanteEmail").value = p ? p.email : "";
  document.getElementById("participanteCurso").value = p ? p.curso : "";

  openModal("modalParticipanteBackdrop");
}

document.getElementById("btnNovoParticipante").addEventListener("click", () => openParticipanteModal());

document.getElementById("formParticipante").addEventListener("submit", async (e) => {
  e.preventDefault();
  const erroEl = document.getElementById("participanteErro");
  const btn = document.getElementById("participanteSalvarBtn");
  erroEl.textContent = "";

  const id = document.getElementById("participanteId").value;
  const payload = {
    nome: document.getElementById("participanteNome").value.trim(),
    email: document.getElementById("participanteEmail").value.trim(),
    curso: document.getElementById("participanteCurso").value.trim(),
  };

  btn.disabled = true;
  try {
    if (id) {
      await apiRequest(`/participantes/${id}`, { method: "PUT", body: JSON.stringify(payload) });
      showToast("Participante atualizado.");
    } else {
      await apiRequest(`/participantes/`, { method: "POST", body: JSON.stringify(payload) });
      showToast("Participante cadastrado.");
    }
    closeModal("modalParticipanteBackdrop");
    await loadParticipantes();
    if (id) selectParticipante(Number(id));
  } catch (e2) {
    erroEl.textContent = e2.message;
  } finally {
    btn.disabled = false;
  }
});

/* =========================================================
   Utilitários
   ========================================================= */
function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function formatarData(iso) {
  if (!iso) return "";
  const [ano, mes, dia] = iso.split("-");
  if (!ano || !mes || !dia) return iso;
  return `${dia}/${mes}/${ano}`;
}

/* =========================================================
   Boot
   ========================================================= */
(async function init() {
  checkApiStatus();
  await loadParticipantes();
  await loadEventos();
})();