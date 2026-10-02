"use client";

import { useEffect, useMemo, useState } from "react";
import { createId, loadData, resetData, saveData, type AppData } from "@/lib/store";
import { loginWithApi } from "@/lib/auth";
import type { SectorCode, SessionUser } from "@/lib/session";

type Section = "overview" | "materials" | "stock" | "requests" | "purchases" | "reports";
const nav: { id: Section; label: string; icon: string }[] = [
  { id: "overview", label: "Visão geral", icon: "⌂" },
  { id: "materials", label: "Materiais", icon: "▦" },
  { id: "stock", label: "Estoque", icon: "▣" },
  { id: "requests", label: "Solicitações", icon: "↗" },
  { id: "purchases", label: "Compras", icon: "▤" },
  { id: "reports", label: "Relatórios", icon: "◒" },
];

const statusLabels: Record<string, string> = {
  pending_approval: "Aguardando aprovação", approved: "Aprovada", in_separation: "Em separação",
  draft: "Rascunho", rejected: "Rejeitada", delivered: "Entregue", completed: "Finalizada",
};


const sectorAccounts: Record<SectorCode, { label: string; email: string; password: string; role: string; description: string }> = {
  TI: { label: "Tecnologia da Informação", email: "ti@acme.demo", password: "Demo@123", role: "Gestor de TI", description: "Ativos, equipamentos e suporte" },
  RH: { label: "Recursos Humanos", email: "rh@acme.demo", password: "Demo@123", role: "Gestor de RH", description: "Pessoas, onboarding e desligamentos" },
  ADM: { label: "Administrativo", email: "adm@acme.demo", password: "Demo@123", role: "Gestor Administrativo", description: "Materiais de uso geral e serviços" },
  COMPRAS: { label: "Compras", email: "compras@acme.demo", password: "Demo@123", role: "Comprador", description: "Fornecedores, cotações e pedidos" },
};

export default function Home() {
  const [session, setSession] = useState<SessionUser | null>(() => {
    if (typeof window === "undefined") return null;
    try { return JSON.parse(window.localStorage.getItem("gestao-materiais:session:v1") ?? "null") as SessionUser | null; } catch { return null; }
  });
  if (!session) return <LoginScreen onLogin={(user) => { window.localStorage.setItem("gestao-materiais:session:v1", JSON.stringify(user)); setSession(user); }} />;
  return <Dashboard session={session} onLogout={() => { window.localStorage.removeItem("gestao-materiais:session:v1"); setSession(null); }} />;
}

function LoginScreen({ onLogin }: { onLogin: (user: SessionUser) => void }) {
  const [sector, setSector] = useState<SectorCode>("TI");
  const [email, setEmail] = useState(sectorAccounts.TI.email);
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const account = sectorAccounts[sector];
  function changeSector(next: SectorCode) { setSector(next); setEmail(sectorAccounts[next].email); setPassword(""); setError(""); }
  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); setError(""); setLoading(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      if (apiUrl) {
        const user = await loginWithApi(apiUrl, email.trim().toLowerCase(), password);
        if (user.sector !== sector) throw new Error("Este usuário não pertence ao setor selecionado.");
        onLogin(user);
      } else {
        if (email.trim().toLowerCase() !== account.email || password !== account.password) throw new Error("E-mail, setor ou senha inválidos.");
        onLogin({ id: `demo-${sector.toLowerCase()}`, name: account.label, email: account.email, role: account.role, sector });
      }
    } catch (loginError) { setError(loginError instanceof Error ? loginError.message : "Não foi possível entrar."); } finally { setLoading(false); }
  }
  return <main className="login-page"><section className="login-panel"><div className="login-brand"><span className="brand-mark">GM</span><div><strong>Gestão de Materiais</strong><small>Controle operacional corporativo</small></div></div><div className="login-copy"><p className="eyebrow accent">Acesso por setor</p><h1>Entre para continuar a operação.</h1><p>Escolha seu setor. O sistema aplicará o escopo, as permissões e as próximas ações disponíveis para o seu perfil.</p></div><div className="sector-grid">{(Object.keys(sectorAccounts) as SectorCode[]).map((code) => <button type="button" className={`sector-card${sector === code ? " selected" : ""}`} onClick={() => changeSector(code)} key={code}><strong>{code}</strong><span>{sectorAccounts[code].label}</span><small>{sectorAccounts[code].description}</small></button>)}</div><form className="login-form" onSubmit={submit}><label>E-mail<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} autoComplete="username" required /></label><label>Senha<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} autoComplete="current-password" placeholder="Senha do ambiente" required /></label>{error && <p className="form-error" role="alert">{error}</p>}<button className="primary-button login-button" type="submit" disabled={loading}>{loading ? "Autenticando..." : `Entrar como ${sector}`}</button></form><p className="demo-hint">{process.env.NEXT_PUBLIC_API_URL ? "Autenticação via API Django" : <>Ambiente de demonstração · senha dos setores: <strong>Demo@123</strong></>}</p></section></main>;
}

function Dashboard({ session, onLogout }: { session: SessionUser; onLogout: () => void }) {
  const [data, setData] = useState<AppData>(() => loadData());
  const [section, setSection] = useState<Section>("overview");
  const [search, setSearch] = useState("");
  const [showRequest, setShowRequest] = useState(false);
  const [notice, setNotice] = useState("");

  useEffect(() => { saveData(data); }, [data]);
  useEffect(() => { if (!notice) return; const timer = setTimeout(() => setNotice(""), 3500); return () => clearTimeout(timer); }, [notice]);

  const available = data.stockBalances.reduce((sum, item) => sum + item.onHand - item.reserved, 0);
  const lowStock = data.stockBalances.filter((balance) => {
    const material = data.materials.find((item) => item.id === balance.materialId);
    return material && balance.onHand - balance.reserved <= material.minimumStock;
  });
  const filteredMaterials = useMemo(() => data.materials.filter((material) => `${material.name} ${material.sku}`.toLowerCase().includes(search.toLowerCase())), [data.materials, search]);
  const title = nav.find((item) => item.id === section)?.label ?? "Visão geral";

  function createRequest(title: string, materialId: string, quantity: number) {
    const request = { id: createId("req"), code: `REQ-${1000 + data.requests.length + 1}`, title, requesterId: "user-requester", areaId: "area-adm", status: "pending_approval", createdAt: new Date().toISOString(), items: [{ materialId, quantity }] };
    setData((current) => ({ ...current, requests: [request, ...current.requests] }));
    setShowRequest(false); setNotice("Solicitação criada e enviada para aprovação."); setSection("requests");
  }

  function resetDemo() { setData(resetData()); setNotice("Dados de demonstração restaurados."); }

  return (
    <div className="app-shell">
      <aside className="sidebar" aria-label="Navegação principal">
        <div className="brand"><span className="brand-mark">GM</span><div><strong>Gestão de Materiais</strong><small>Plataforma corporativa</small></div></div>
        <nav className="nav-list">{nav.map((item) => <button className={`nav-item${section === item.id ? " active" : ""}`} onClick={() => setSection(item.id)} key={item.id}><span>{item.icon}</span>{item.label}</button>)}</nav>
        <div className="sidebar-footer"><span className="status-dot" /> Ambiente de demonstração<br /><small>Persistência local ativa</small></div>
      </aside>
      <main className="main-content">
        <header className="topbar"><div><p className="eyebrow">Workspace / {session.sector}</p><h1>{title}</h1></div><div className="top-actions"><button className="secondary-button" onClick={resetDemo}>Restaurar demo</button><div className="user-chip"><span className="avatar">{session.sector.slice(0, 2)}</span><span>{session.name} <small>{session.role}</small></span></div><button className="logout-button" onClick={onLogout}>Sair</button></div></header>
        {notice && <div className="toast" role="status">✓ {notice}</div>}
        {section === "overview" && <Overview data={data} available={available} lowStock={lowStock.length} onNew={() => setShowRequest(true)} onNavigate={setSection} />}
        {section === "materials" && <Materials data={data} materials={filteredMaterials} search={search} setSearch={setSearch} />}
        {section === "stock" && <Stock data={data} lowStock={lowStock.map((item) => item.materialId)} />}
        {section === "requests" && <Requests data={data} onNew={() => setShowRequest(true)} />}
        {section === "purchases" && <Placeholder title="Compras" description="Fornecedores, cotações e pedidos entram nesta visão. A estrutura inicial já está preparada para o próximo módulo." />}
        {section === "reports" && <Reports data={data} available={available} />}
      </main>
      {showRequest && <RequestModal data={data} onClose={() => setShowRequest(false)} onCreate={createRequest} />}
    </div>
  );
}

function Overview({ data, available, lowStock, onNew, onNavigate }: { data: AppData; available: number; lowStock: number; onNew: () => void; onNavigate: (section: Section) => void }) {
  const pending = data.requests.filter((request) => request.status === "pending_approval").length;
  return <>
    <section className="hero"><div><p className="eyebrow accent">Operação em tempo real</p><h2>Controle tudo que entra, sai e precisa de atenção.</h2><p className="intro-copy">Base inicial pronta para explorar o ciclo de materiais. Os dados são carregados do JSON versionado e alterações desta sessão ficam persistidas no navegador.</p><div className="hero-actions"><button className="primary-button" onClick={onNew}>+ Nova solicitação</button><button className="link-button" onClick={() => onNavigate("materials")}>Ver catálogo →</button></div></div><div className="architecture-badge"><strong>Ambiente demo</strong><span>JSON + localStorage</span><small>Troque por API quando publicar o backend.</small></div></section>
    <section className="metrics-grid"><Metric label="Itens disponíveis" value={available.toString()} detail="em todos os almoxarifados" tone="green" /><Metric label="Aguardando ação" value={pending.toString()} detail="solicitações pendentes" tone="amber" /><Metric label="Estoque baixo" value={lowStock.toString()} detail="itens abaixo do mínimo" tone="red" /><Metric label="Materiais ativos" value={data.materials.length.toString()} detail="no catálogo" tone="blue" /></section>
    <div className="content-grid"><section className="panel"><div className="panel-heading"><div><p className="eyebrow">Fluxo operacional</p><h2>Solicitações recentes</h2></div><button className="text-button" onClick={() => onNavigate("requests")}>Ver todas</button></div><div className="request-list">{data.requests.slice(0, 4).map((request) => <RequestRow data={data} request={request} key={request.id} />)}</div></section><section className="panel attention"><div className="panel-heading"><div><p className="eyebrow">Monitoramento</p><h2>Pontos de atenção</h2></div></div>{lowStock > 0 ? <div className="attention-item"><span className="attention-icon">!</span><div><strong>{lowStock} {lowStock === 1 ? "item precisa" : "itens precisam"} de reposição</strong><span>Revise o estoque mínimo e abra uma compra.</span></div></div> : <Empty text="Nenhum alerta no momento" />}</section></div>
  </>;
}

function Metric({ label, value, detail, tone }: { label: string; value: string; detail: string; tone: string }) { return <article className={`metric metric-${tone}`}><span>{label}</span><strong>{value}</strong><small>{detail}</small></article>; }
function RequestRow({ data, request }: { data: AppData; request: AppData["requests"][number] }) { const requester = data.users.find((user) => user.id === request.requesterId)?.name ?? "Usuário"; return <div className="request-row"><div className="request-mark">{request.code.slice(-2)}</div><div className="request-main"><strong>{request.title}</strong><span>{request.code} · {requester}</span></div><Status value={request.status} /></div>; }
function Status({ value }: { value: string }) { return <span className={`status status-${value}`}>{statusLabels[value] ?? value}</span>; }

function Materials({ data, materials, search, setSearch }: { data: AppData; materials: AppData["materials"]; search: string; setSearch: (value: string) => void }) { return <section className="panel page-panel"><div className="panel-heading"><div><p className="eyebrow">Catálogo por organização</p><h2>Materiais</h2></div><span className="counter-badge">{materials.length} de {data.materials.length}</span></div><input className="search" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Buscar por nome ou SKU..." aria-label="Buscar materiais" /><div className="table-wrap"><table><thead><tr><th>Material</th><th>Categoria</th><th>Tipo</th><th>Estoque mínimo</th><th>Status</th></tr></thead><tbody>{materials.map((material) => <tr key={material.id}><td><strong>{material.name}</strong><small>{material.sku}</small></td><td>{data.categories.find((category) => category.id === material.categoryId)?.name}</td><td>{material.kind === "asset" ? "Ativo" : "Consumível"}</td><td>{material.minimumStock} {material.unit}</td><td><span className="dot-label"><i className="green-dot" /> Ativo</span></td></tr>)}</tbody></table></div></section>; }

function Stock({ data, lowStock }: { data: AppData; lowStock: string[] }) { return <section className="panel page-panel"><div className="panel-heading"><div><p className="eyebrow">Saldos e disponibilidade</p><h2>Estoque</h2></div><span className="counter-badge">{data.stockBalances.length} saldos controlados</span></div><div className="table-wrap"><table><thead><tr><th>Material</th><th>Almoxarifado</th><th>Físico</th><th>Reservado</th><th>Disponível</th><th>Situação</th></tr></thead><tbody>{data.stockBalances.map((balance) => { const material = data.materials.find((item) => item.id === balance.materialId)!; const warehouse = data.warehouses.find((item) => item.id === balance.warehouseId); const available = balance.onHand - balance.reserved; return <tr key={balance.id}><td><strong>{material.name}</strong><small>{material.sku}</small></td><td>{warehouse?.name}</td><td>{balance.onHand} {material.unit}</td><td>{balance.reserved} {material.unit}</td><td><strong>{available} {material.unit}</strong></td><td>{lowStock.includes(material.id) ? <Status value="pending_approval" /> : <span className="dot-label"><i className="green-dot" /> Normal</span>}</td></tr>; })}</tbody></table></div></section>; }

function Requests({ data, onNew }: { data: AppData; onNew: () => void }) { return <section className="panel page-panel"><div className="panel-heading"><div><p className="eyebrow">Fluxo de aprovação e atendimento</p><h2>Solicitações</h2></div><button className="primary-button small-button" onClick={onNew}>+ Nova solicitação</button></div><div className="request-list full-list">{data.requests.map((request) => <RequestRow data={data} request={request} key={request.id} />)}</div></section>; }
function Reports({ data, available }: { data: AppData; available: number }) { const consumed = data.movements.filter((movement) => movement.kind === "issue").reduce((sum, movement) => sum + movement.quantity, 0); return <section className="panel page-panel"><div className="panel-heading"><div><p className="eyebrow">Indicadores operacionais</p><h2>Relatórios</h2></div></div><div className="report-grid"><div><span>Saldo disponível total</span><strong>{available}</strong><small>unidades controladas</small></div><div><span>Movimentações registradas</span><strong>{data.movements.length}</strong><small>livro de estoque</small></div><div><span>Consumo registrado</span><strong>{consumed}</strong><small>unidades baixadas</small></div></div><div className="info-banner">Os relatórios respeitam a organização selecionada. A persistência definitiva deve ser conectada à API Django antes da produção.</div></section>; }
function Placeholder({ title, description }: { title: string; description: string }) { return <section className="panel empty-page"><div className="empty-illustration">▤</div><p className="eyebrow">Próximo módulo</p><h2>{title}</h2><p>{description}</p><span className="planned">Estrutura de dados preparada no roadmap</span></section>; }
function Empty({ text }: { text: string }) { return <div className="empty-state">{text}</div>; }

function RequestModal({ data, onClose, onCreate }: { data: AppData; onClose: () => void; onCreate: (title: string, materialId: string, quantity: number) => void }) { const [title, setTitle] = useState(""); const [materialId, setMaterialId] = useState(data.materials[0]?.id ?? ""); const [quantity, setQuantity] = useState(1); const canSubmit = title.trim().length > 3 && quantity > 0; return <div className="modal-backdrop" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}><div className="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title"><div className="modal-heading"><div><p className="eyebrow">Nova operação</p><h2 id="modal-title">Criar solicitação</h2></div><button className="close-button" onClick={onClose} aria-label="Fechar">×</button></div><label>Título da solicitação<input value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Ex.: Kit de integração" autoFocus /></label><label>Material<select value={materialId} onChange={(event) => setMaterialId(event.target.value)}>{data.materials.map((material) => <option value={material.id} key={material.id}>{material.name} ({material.sku})</option>)}</select></label><label>Quantidade<input type="number" min="1" value={quantity} onChange={(event) => setQuantity(Number(event.target.value))} /></label><div className="modal-actions"><button className="secondary-button" onClick={onClose}>Cancelar</button><button className="primary-button" disabled={!canSubmit} onClick={() => onCreate(title.trim(), materialId, quantity)}>Enviar para aprovação</button></div></div></div>; }
