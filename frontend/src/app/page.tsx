const areas = ['TI', 'Suprimentos', 'Administrativo', 'RH']

export default function Home() {
  return (
    <div className="app-shell">
      <aside className="sidebar" aria-label="Navegação principal">
        <div className="brand">
          <span className="brand-mark">GM</span>
          <div>
            <strong>Gestão de Materiais</strong>
            <small>Plataforma corporativa</small>
          </div>
        </div>
        <nav className="nav-list">
          {['Visão geral', 'Materiais', 'Estoque', 'Solicitações', 'Compras', 'Relatórios'].map((item, index) => (
            <a className={`nav-item${index === 0 ? ' active' : ''}`} href={`#${item.toLowerCase()}`} key={item}>{item}</a>
          ))}
        </nav>
        <div className="sidebar-footer"><span className="status-dot" /> Fundação do produto em andamento</div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div><p className="eyebrow">Workspace / Plataforma</p><h1>Visão geral</h1></div>
          <div className="user-chip"><span className="avatar">AD</span><span>Administrador</span></div>
        </header>

        <section className="intro-card">
          <div>
            <p className="eyebrow accent">Primeiro marco</p>
            <h2>Uma base única para controlar materiais com segurança.</h2>
            <p className="intro-copy">O produto começa com identidade, áreas e permissões. Em seguida, evolui para estoque, solicitações, compras, recebimento, entregas e custódia de ativos.</p>
          </div>
          <div className="architecture-badge"><strong>Next.js + Django</strong><span>PostgreSQL · Python · IA preparada</span></div>
        </section>

        <section className="section-block" aria-labelledby="areas-title">
          <div className="section-heading"><div><p className="eyebrow">Estrutura organizacional</p><h2 id="areas-title">Áreas preparadas</h2></div><span className="counter-badge">{areas.length} áreas iniciais</span></div>
          <div className="area-grid">{areas.map((area, index) => <article className="area-card" key={area}><span className="area-index">0{index + 1}</span><h3>{area}</h3><p>Acesso por escopo, perfil e permissão.</p><span className="planned">Próxima configuração</span></article>)}</div>
        </section>

        <section className="section-block" aria-labelledby="principles-title">
          <div className="section-heading"><div><p className="eyebrow">Diretrizes</p><h2 id="principles-title">Princípios de operação</h2></div></div>
          <div className="principles-grid"><div><strong>Rastreabilidade</strong><span>Histórico completo de ações e movimentações.</span></div><div><strong>Menor privilégio</strong><span>Cada usuário acessa apenas o que precisa.</span></div><div><strong>Estoque íntegro</strong><span>Saldo calculado por movimentações auditáveis.</span></div></div>
        </section>
      </main>
    </div>
  )
}
