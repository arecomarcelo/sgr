# Roteiro de Ajustes - Ranking de Vendedores (Novo Layout dos Cards)

## Objetivo
Atualizar os cards do Ranking de Vendedores para o novo layout, substituindo o gauge e badge percentual por:
- Nome curto do vendedor (campo "Curto" da tabela Vendedores)
- Valor de vendas do mesmo período filtrado no ano anterior
- Percentual meta batida: `vendas_atuais / (vendas_ano_anterior * (1 + Percentual/100)) * 100`

---

## Pré-requisitos
- O campo `"Curto"` deve existir na tabela `"Vendedores"` no banco de dados PostgreSQL
- O campo `"Percentual"` deve existir na tabela `"Vendedores"` (valor percentual, ex: 10 para 10%)

---

## Ajuste 1: Repositório - Novo método para buscar dados dos vendedores

**Arquivo:** `infrastructure/database/repositories_vendas.py`
**Classe:** `VendaRepository`
**Ação:** Adicionar o método abaixo (antes do método `get_situacoes_disponiveis`)

```python
def get_vendedores_com_nome_curto(self) -> dict:
    """Obtém mapeamento de nome completo para dados do vendedor (nome curto e percentual)"""
    try:
        query = 'SELECT "Nome", "Curto", "Percentual" FROM "Vendedores" ORDER BY "Nome"'

        with connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()

            resultado = {}
            for row in data:
                nome_completo = row[0]
                nome_curto = row[1] if row[1] else nome_completo
                percentual = float(row[2]) if row[2] else 0.0
                resultado[nome_completo] = {
                    "curto": nome_curto,
                    "percentual": percentual,
                }

        return resultado

    except Exception as e:
        logger.error(f"Error fetching short names: {str(e)}")
        return {}
```

**Status:** ✅ Aplicado

---

## Ajuste 2: Função `_render_vendedores_com_fotos()` - Novos dados para os cards

**Arquivo:** `app.py`
**Função:** `_render_vendedores_com_fotos(vendas_por_vendedor)`

### 2.1 - REMOVER o bloco de cálculo de gauge

**Localizar e REMOVER:**
```python
# Calcular vendas do mês atual para os gauges
# IMPORTANTE: Os gauges sempre usam o mês atual, independente dos filtros
# Realizado: 01 do mês atual até hoje
# Meta: 01 do mesmo mês do ano anterior até o mesmo dia
vendedores_nomes = [v["nome"] for v in vendedores_tabela]
vendas_realizadas_gauge, vendas_meta_gauge = _calcular_vendas_mes_atual_para_gauge(
    vendedores_nomes
)
```

### 2.2 - ADICIONAR busca de dados e cálculo de vendas do ano anterior

**Inserir no lugar do bloco removido (após `vendedores_tabela`):**
```python
# Buscar nomes curtos e percentuais do banco de dados
dados_vendedores = vendas_service.venda_repository.get_vendedores_com_nome_curto()

# Obter datas do filtro aplicado (ou calcular mês atual)
from dateutil.relativedelta import relativedelta

data_inicio = st.session_state.get("data_inicio_filtro")
data_fim = st.session_state.get("data_fim_filtro")

if not data_inicio or not data_fim:
    hoje = datetime.now()
    data_inicio = datetime(hoje.year, hoje.month, 1).date()
    data_fim = hoje.date()

# Calcular ano anterior para exibição
ano_anterior = (data_inicio - relativedelta(years=1)).year

# Calcular vendas do mesmo período no ano anterior
vendedores_nomes = [v["nome"] for v in vendedores_tabela]
vendas_anteriores = _calcular_vendas_periodo_anterior(
    data_inicio, data_fim, vendedores_nomes
)
```

### 2.3 - SUBSTITUIR o bloco de criação do `vendas_dict`

**Localizar e SUBSTITUIR de:**
```python
vendas_dict = {}
total_geral = 0

if vendas_por_vendedor is not None and not vendas_por_vendedor.empty:
    total_geral = float(vendas_por_vendedor["total_valor"].sum())
    for _, row in vendas_por_vendedor.iterrows():
        vendas_dict[row["VendedorNome"]] = {
            "total_valor": float(row["total_valor"]),
            "percentual": (
                (float(row["total_valor"]) / total_geral * 100)
                if total_geral > 0
                else 0
            ),
        }
```

**Para:**
```python
vendas_dict = {}

if vendas_por_vendedor is not None and not vendas_por_vendedor.empty:
    for _, row in vendas_por_vendedor.iterrows():
        vendas_dict[row["VendedorNome"]] = {
            "total_valor": float(row["total_valor"]),
        }
```

### 2.4 - SUBSTITUIR o bloco de preparação dos vendedores

**Localizar e SUBSTITUIR o bloco `vendedores_completos` por:**
```python
vendedores_completos = []
for vendedor in vendedores_tabela:
    nome = vendedor["nome"]
    dados_vend = dados_vendedores.get(nome, {})
    nome_curto = dados_vend.get("curto", nome)
    percentual_meta = dados_vend.get("percentual", 0.0)
    vendas_ant = vendas_anteriores.get(nome, 0.0)

    total_valor = vendas_dict[nome]["total_valor"] if nome in vendas_dict else 0.0

    vendedores_completos.append(
        {
            "nome": nome,
            "nome_curto": nome_curto,
            "foto": vendedor["foto"],
            "total_valor": total_valor,
            "vendas_ano_anterior": vendas_ant,
            "percentual_meta": percentual_meta,
            "ano_anterior": ano_anterior,
        }
    )
```

**Status:** ✅ Aplicado

---

## Ajuste 3: Função `_render_card_vendedor()` - Novo layout do card

**Arquivo:** `app.py`
**Função:** `_render_card_vendedor(col, vendedor, get_image_base64, format_currency)`
**Ação:** SUBSTITUIR a função inteira por:

```python
def _render_card_vendedor(col, vendedor, get_image_base64, format_currency):
    """Renderiza um card individual do vendedor com novo layout"""
    with col:
        # Buscar foto do vendedor
        foto_path_jpg = f"fotos/{vendedor['foto']}.jpg"
        foto_path_png = f"fotos/{vendedor['foto']}.png"

        # Usar JPG se existir, senão PNG
        foto_path = foto_path_jpg if os.path.exists(foto_path_jpg) else foto_path_png
        image_b64 = get_image_base64(foto_path)

        # Calcular percentual: vendas atuais / (vendas ano anterior + percentual crescimento)
        vendas_ant = vendedor.get("vendas_ano_anterior", 0.0)
        percentual_meta = vendedor.get("percentual_meta", 0.0)
        # Meta = vendas_ano_anterior * (1 + Percentual/100)
        meta = vendas_ant * (1 + percentual_meta / 100) if vendas_ant > 0 else 0
        percentual = (vendedor["total_valor"] / meta * 100) if meta > 0 else 0
        ano_anterior = vendedor.get("ano_anterior", "")

        # Foto ou avatar com iniciais
        if image_b64:
            foto_html = f'<img src="{image_b64}" style="width: 80px; height: 80px; margin-bottom: 12px; object-fit: cover;">'
        else:
            iniciais = "".join(
                [nome[0] for nome in vendedor["nome"].split()[:2]]
            ).upper()
            foto_html = f"""<div style="
                width: 80px;
                height: 80px;
                border-radius: 50%;
                background: linear-gradient(135deg, #1E88E5, #1565C0);
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                font-weight: 700;
                margin: 0 auto 12px auto;
                border: 3px solid #1E88E5;
            ">{iniciais}</div>"""

        st.markdown(
            f"""
        <div style='
            background: #ffffff;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 6px 16px rgba(30, 136, 229, 0.2);
            font-family: Roboto, sans-serif;
            margin-bottom: 20px;
            border: 2px solid #E3F2FD;
        '>
            {foto_html}
            <div style='font-size: 0.95rem; color: #1E88E5; font-weight: 600; margin-bottom: 8px;'>
                {vendedor.get('nome_curto', vendedor['nome'])}
            </div>
            <div style='font-size: 1.2rem; font-weight: 700; color: #1565C0; margin-bottom: 8px;'>
                {format_currency(vendedor['total_valor'])}
            </div>
            <div style='font-size: 0.75rem; color: #555; margin-bottom: 6px;'>
                Mês de {ano_anterior}= {format_currency(vendas_ant)}
            </div>
            <div style='font-size: 0.8rem; font-weight: 600; color: #333;'>
                {percentual:.1f}% meta do mês batida
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
```

**Status:** ✅ Aplicado

---

## Resumo das Alterações

| # | Arquivo | Ação | Descrição | Status |
|---|---------|------|-----------|--------|
| 1 | `repositories_vendas.py` | Adicionar método | `get_vendedores_com_nome_curto()` com Nome, Curto e Percentual | ✅ Aplicado |
| 2 | `app.py` - `_render_vendedores_com_fotos()` | Substituir lógica | Nomes curtos + percentual + vendas ano anterior | ✅ Aplicado |
| 3 | `app.py` - `_render_card_vendedor()` | Substituir função | Novo layout com fórmula de meta | ✅ Aplicado |

## Fórmula do Percentual Meta Batida
```
Meta = vendas_ano_anterior × (1 + Percentual/100)
% meta batida = (vendas_atuais / Meta) × 100
```

Onde:
- `vendas_atuais` = Valor vendido no período selecionado
- `vendas_ano_anterior` = Valor vendido no mesmo período do ano anterior
- `Percentual` = Campo "Percentual" da tabela Vendedores (ex: 10 para 10%)

## Dependências
- Função `_calcular_vendas_periodo_anterior()` já deve existir no `app.py`
- Variável `vendas_service` com acesso a `venda_repository`
- Biblioteca `dateutil` (`pip install python-dateutil`)

## Novo Layout do Card
```
┌─────────────────────┐
│       [FOTO]        │
│                     │
│    Nome Curto       │
│                     │
│  R$ 549.233,18      │  ← Vendas período atual (azul)
│                     │
│ Mês de 2025=        │  ← Vendas mesmo período ano anterior
│ R$1.432.232,00      │
│                     │
│ 34.8% meta do mês   │  ← vendas_atuais / (vendas_anterior × 1.10) × 100
│      batida         │
└─────────────────────┘
```

---

## ✅ Conclusão

**Todas as alterações foram aplicadas com sucesso e registradas no Commit 138.**

| Item | Status |
|------|--------|
| Ajuste 1 - Repositório `get_vendedores_com_nome_curto()` | ✅ Aplicado |
| Ajuste 2 - Função `_render_vendedores_com_fotos()` | ✅ Aplicado |
| Ajuste 3 - Função `_render_card_vendedor()` | ✅ Aplicado |
| **Commit** | **138** |
| **Data** | **13/02/2026** |
