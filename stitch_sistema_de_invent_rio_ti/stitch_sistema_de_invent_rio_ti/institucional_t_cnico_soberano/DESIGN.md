---
name: Institucional Técnico Soberano
colors:
  surface: '#f8f9ff'
  surface-dim: '#ccdbf4'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e6eeff'
  surface-container-high: '#dde9ff'
  surface-container-highest: '#d5e3fd'
  on-surface: '#0d1c2f'
  on-surface-variant: '#43474d'
  inverse-surface: '#233144'
  inverse-on-surface: '#ebf1ff'
  outline: '#74777e'
  outline-variant: '#c3c6ce'
  surface-tint: '#49607c'
  primary: '#001428'
  on-primary: '#ffffff'
  primary-container: '#0f2942'
  on-primary-container: '#7991af'
  inverse-primary: '#b0c9e8'
  secondary: '#4059aa'
  on-secondary: '#ffffff'
  secondary-container: '#8fa7fe'
  on-secondary-container: '#1d3989'
  tertiary: '#001524'
  on-tertiary: '#ffffff'
  tertiary-container: '#002a44'
  on-tertiary-container: '#2e95da'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d1e4ff'
  primary-fixed-dim: '#b0c9e8'
  on-primary-fixed: '#011d35'
  on-primary-fixed-variant: '#314863'
  secondary-fixed: '#dce1ff'
  secondary-fixed-dim: '#b6c4ff'
  on-secondary-fixed: '#00164e'
  on-secondary-fixed-variant: '#264191'
  tertiary-fixed: '#cce5ff'
  tertiary-fixed-dim: '#93ccff'
  on-tertiary-fixed: '#001d31'
  on-tertiary-fixed-variant: '#004b73'
  background: '#f8f9ff'
  on-background: '#0d1c2f'
  surface-variant: '#d5e3fd'
typography:
  display:
    fontFamily: Public Sans
    fontSize: 2rem
    fontWeight: '700'
    lineHeight: 2.5rem
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Public Sans
    fontSize: 1.5rem
    fontWeight: '600'
    lineHeight: 2rem
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: Public Sans
    fontSize: 1.25rem
    fontWeight: '600'
    lineHeight: 1.75rem
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Public Sans
    fontSize: 1.125rem
    fontWeight: '600'
    lineHeight: 1.5rem
  headline-sm:
    fontFamily: Public Sans
    fontSize: 1rem
    fontWeight: '600'
    lineHeight: 1.375rem
  body-lg:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: '400'
    lineHeight: 1.5rem
  body-md:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '400'
    lineHeight: 1.25rem
  body-sm:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '400'
    lineHeight: 1rem
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 0.8125rem
    fontWeight: '500'
    lineHeight: 1.125rem
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 0.6875rem
    fontWeight: '500'
    lineHeight: 0.875rem
  label-md:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '600'
    lineHeight: 1rem
    letterSpacing: 0.04em
  label-sm:
    fontFamily: Inter
    fontSize: 0.6875rem
    fontWeight: '500'
    lineHeight: 0.875rem
    letterSpacing: 0.02em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
---

## Brand & Style

O design system estabelece uma linguagem visual estrita, austera e de alta precisão para a governança de infraestrutura de tecnologia e inventário patrimonial público. 

### Personalidade e Atributos da Marca
- **Institucional e Confiável:** Comunica integridade de dados, conformidade e rigor regulatório sem recorrer a linguagens burocráticas obsoletas.
- **Técnico e Direto:** Projetado para operadores de rede, administradores de sistemas e gestores de patrimônio que demandam varredura rápida de telas densas.
- **Racional e Objetivo:** Reduz ruído decorativo ao mínimo; cada pixel, linha ou cor carrega significado funcional imediato.

### Movimento de Design
Adota-se uma abordagem **Corporate / Modern Utilitarian** focada em dados de alta densidade:
- Uso primário de linhas estruturais finas e superfícies neutras em vez de sombras pesadas ou efeitos ornamentais.
- Estruturação tabular arquitetada para leitura scan-friendly de endereços IPv4/IPv6, máscaras CIDR, VLANs, números de tombo e números de série.
- Contraste semântico pontual calibrado para leitura ergonômica durante longas jornadas de trabalho técnico.

## Colors

A matriz cromática baseia-se em fundamentos institucionais com ênfase na distinção imediata de estados de topologia e auditoria de hardware.

### Estrutura de Cores
- **Primária (`#0F2942`):** Azul profundo institucional. Utilizado em barras de topo institucionais, botões primários de ação e tipografia de máximo contraste hierárquico.
- **Secundária (`#1E3A8A`):** Azul naval de suporte técnico. Empregado em cabeçalhos de tabelas, seções de navegação lateral ativa e agrupamentos lógicos de rede.
- **Terciária (`#0284C7`):** Cerúleo funcional para estados operacionais dinâmicos (DHCP, pool alocado, rotas ativas e hiperlinks contextuais).
- **Neutra (`#334155`):** Ardósia de alta legibilidade para texto corrido, ícones auxiliares e rótulos de dados técnicos.

### Superfícies e Fundos
- `surface-canvas`: `#F8FAFC` (fundo neutro suave para reduzir estresse ocular).
- `surface-card`: `#FFFFFF` (placas de dados, tabelas e janelas modais).
- `surface-subtle`: `#F1F5F9` (zebrado de tabelas, campos desabilitados e cabeçalhos de coluna).
- `border-default`: `#E2E8F0` (delimitadores de células e contornos estruturais).
- `border-strong`: `#CBD5E1` (divisões de módulos e inputs em foco passivo).

### Acentos Semânticos de Rede e Patrimônio
- **Operante / Ativo / Online:** `#10B981` (fundo com 12% de opacidade `#ECFDF5`, texto `#065F46`).
- **Dinâmico / DHCP / Em Uso:** `#0284C7` (fundo `#F0F9FF`, texto `#075985`).
- **Alerta / Manutenção / Reserva:** `#F59E0B` (fundo `#FFFBEB`, texto `#92400E`).
- **Crítico / Offline / Conflito / Baixa:** `#EF4444` (fundo `#FEF2F2`, texto `#991B1B`).

## Typography

A hierarquia tipográfica resolve a dualidade entre textos administrativos institucionais e valores técnicos tabulares (IPs, MAC addresses, números de patrimônio e hashes).

### Famílias Tipográficas
- **Títulos e Estrutura Institucional (Public Sans):** Confere tom sóbrio, oficial e legível em diferentes resoluções de monitores governamentais.
- **Corpo e Interface (Inter):** Altura-x balanceada e geometria neutra para máxima eficiência em formulários complexos e tabelas de alta densidade.
- **Dados Técnicos (JetBrains Mono):** Elementar para exibição de blocos CIDR (`10.200.0.0/16`), endereços IPv6, portas físicas (`Eth0/1`) e tombos patrimoniais (`BR-2024-TI-0891`), assegurando alinhamento vertical estrito sem saltos ópticos.

### Regras de Aplicação
- Valores numéricos em tabelas devem utilizar numerais tabulares (`font-feature-settings: "tnum"`).
- Textos de status em badges usam caixa-alta reduzida com leve tracking positivo para visualização rápida.

## Layout & Spacing

O layout opera sob uma lógica de densidade balanceada, desenhado especificamente para telas de monitoramento de infraestrutura (dashboards, listagens de switches e ranges de subnet).

### Grade e Estrutura
- **Modelo:** Grade fluida baseada em 12 colunas para módulos de métricas e inventário, com barra lateral de navegação fixa em desktop (`240px` compacta / `64px` colapsada).
- **Ritmo Compacto:** Base de 4px / 8px ajustada com `space-md` em `0.75rem (12px)` para acomodar volumes elevados de linhas sem estourar o viewport.

### Adaptação por Dispositivo
- **Desktop (>= 1280px):** Layout amplo com margens de `2rem`, exibição simultânea de árvore de rede, filtros laterais e tabela com até 10 colunas visíveis.
- **Tablet / Notebook compacto (768px - 1279px):** Margens em `1.5rem`, recolhimento automático da barra de navegação para ícones com tooltips, agrupamento de ações em menus suspensos.
- **Mobile (< 768px):** Margens em `1rem`, conversão de linhas de tabela para visualização em cards de patrimônio com dados essenciais e sanfona de detalhes técnicos.

## Elevation & Depth

A tridimensionalidade é minimalista e estrutural, priorizando o alinhamento plano com delimitações sutis para evitar fadiga visual e preservar a clareza técnica.

### Hierarquia de Camadas
- **Camada Base (L0 - Fundo):** `#F8FAFC`, neutro e uniforme.
- **Camada Plana (L1 - Painéis e Cartões):** `#FFFFFF` sobrepostos diretamente na base, delimitados exclusivamente por borda sólida de `1px` em `#E2E8F0`. Sem projeção de sombra por padrão.
- **Camada Funcional (L2 - Menus de Contexto e Dropdowns):** Sombra suave e precisa: `0px 4px 8px -2px rgba(15, 41, 66, 0.08), 0px 2px 4px -1px rgba(15, 41, 66, 0.04)`.
- **Camada de Foco (L3 - Modais e Gavetas de Inspeção de IP/Ativo):** Sombra profunda ancorada no tom primário: `0px 12px 24px -4px rgba(15, 41, 66, 0.16)`.
- **Destaque de Foco Acessível:** Todos os controles interativos utilizam um anel duplo de foco (`ring-2 ring-offset-2 ring-[#0284C7]`) para total conformidade com diretrizes governamentais de acessibilidade (eMAG / WCAG 2.1 AA).

## Shapes

O sistema utiliza a classificação de cantos **Soft (1)**, garantindo um visual sóbrio, contemporâneo e estritamente institucional.

### Aplicação Geométrica
- **Controles (Inputs, Botões, Selects):** Raio de `0.25rem (4px)`. Oferece rigidez e estabilidade geométrica para formulários densos de cadastro patrimonial.
- **Painéis, Modais e Cards de Métrica:** Raio de `0.5rem (8px)` (`rounded-lg`), suavizando levemente as esquinas dos contêineres principais sem perder o caráter analítico.
- **Badges de Status IPAM e Tags:** Raio de `0.25rem (4px)` com padding horizontal contido, mantendo o formato de etiqueta de leitura técnica rápida.

## Components

### Botões
- **Primário:** Fundo `#0F2942`, texto `#FFFFFF`, sem sombra. No hover: `#1E3A8A`. Altura padrão de `36px` (`padding: 0 12px`).
- **Secundário/Neutro:** Fundo `#FFFFFF`, borda `1px solid #CBD5E1`, texto `#334155`. No hover: `#F1F5F9`.
- **Destrutivo (Baixa/Exclusão):** Fundo `#FEF2F2`, borda `1px solid #FCA5A5`, texto `#991B1B`. No hover: fundo `#FEE2E2`.

### Badges e Chips de Status
- Estrutura: Altura de `22px`, fonte `code-sm` (`JetBrains Mono`, `0.6875rem`), peso semibold, raio de `4px`.
- **Ativo / Online:** Fundo `#ECFDF5`, borda `1px solid #A7F3D0`, texto `#065F46`, com ponto indicador verde circular de `6px`.
- **Alocado / DHCP:** Fundo `#F0F9FF`, borda `1px solid #BAE6FD`, texto `#075985`.
- **Reserva / Em Manutenção:** Fundo `#FFFBEB`, borda `1px solid #FDE68A`, texto `#92400E`.
- **Conflito / Offline / Baixado:** Fundo `#FEF2F2`, borda `1px solid #FECACA`, texto `#991B1B`.

### Tabelas de Ativos e IPAM (Core)
- **Densidade:** Linhas com altura de `40px` (modo compacto) e `48px` (modo confortável).
- **Cabeçalho:** Fundo `#F1F5F9`, tipografia `label-md` em `#334155`, delimitado por borda inferior de `2px solid #CBD5E1`.
- **Células Técnicas:** Colunas de Endereço IP, MAC, Máscara e Tombamento utilizam a tipografia `code-md` alinhada à esquerda com numerais tabulares.

### Campos de Entrada (Inputs de Formulário)
- Altura de `36px`, fundo `#FFFFFF`, borda `1px solid #CBD5E1`, texto `#0F2942`, tipografia `body-md`.
- Campos formatados para IPv4/IPv6 possuem prefixo fixo ou segmentação em bloco monoespaçado para validação imediata de sintaxe.

### Cards de Métricas e Capacidade de Subnet
- Cartões com fundo `#FFFFFF`, borda `1px solid #E2E8F0`, padding de `16px`.
- Estrutura interna: Rótulo superior institucional em `label-sm` (`#64748B`), número mestre em `display` (`#0F2942`) e barra de progresso linear fina (`height: 6px`) indicando alocação de IPs do bloco (ex: 82% utilizado em azul cerúleo e restante em cinza ardósia claro).

### Seletores, Checkboxes e Radio Buttons
- Caixas de marcação com `16x16px`, borda `1px solid #94A3B8`, raio de `3px`. Quando ativas: preenchimento `#0F2942` com ícone branco nítido.