# 📊 Manual de Utilização - Relatório de Vendas SGR

## 🎯 Visão Geral

O **Relatório de Vendas SGR** é uma ferramenta completa e interativa para análise de desempenho comercial. Desenvolvido com interface moderna e intuitiva, este módulo oferece recursos avançados de filtragem, visualização de dados, rankings de performance e análises de métricas comerciais em tempo real.

### 💡 Principais Recursos

✅ **Filtros Inteligentes** - Sistema avançado de filtros personalizáveis
✅ **Rankings Dinâmicos** - Vendedores e Produtos mais performáticos
✅ **Métricas em Tempo Real** - Acompanhamento instantâneo de resultados
✅ **Análise de Mix de Produtos** - Composição Equipamentos vs Acessórios
✅ **Análises Avançadas** - Insights aprofundados de performance
✅ **Exportação de Dados** - Relatórios em formato Excel/CSV

---

## 🏗️ Estrutura do Sistema

### 📋 Seções Principais

O sistema está organizado em **cinco seções principais**, cada uma com funcionalidades específicas:

| Seção | Ícone | Função Principal |
|-------|-------|------------------|
| **Informações de Atualização** | 🔄 | Monitoramento de sincronização de dados |
| **Filtros e Configuração** | 🔍 | Definição de parâmetros de consulta |
| **Resumo Executivo** | 📊 | Visão panorâmica das métricas |
| **Dados Detalhados** | 📋 | Visualização tabular dos registros |
| **Análise Avançada** | 📈 | Rankings e insights aprofundados |

---

## 🚀 Guia de Utilização Passo a Passo

### 1️⃣ Informações de Atualização 🔄

> **Localização**: Expandível no topo da tela
> **Função**: Monitorar a sincronização de dados com o sistema principal

#### 📊 Métricas Exibidas

| Métrica | Descrição | Exemplo |
|---------|-----------|---------|
| 📅 **Data** | Data da última atualização | 15/10/2025 |
| ⏰ **Hora** | Horário da última sincronização | 14:30:15 |
| 📆 **Período** | Intervalo dos dados processados | 01/10 - 15/10 |
| ➕ **Inseridos** | Novos registros adicionados | 127 |
| 🔄 **Atualizados** | Registros modificados | 45 |

#### 🎯 Como Utilizar

1. Clique no expandir **"🔄 Informações de Atualização"**
2. Visualize as métricas de sincronização
3. Verifique se os dados estão atualizados
4. Certifique-se que o período está correto

> 💡 **Dica**: Sempre verifique esta seção antes de gerar relatórios importantes!

---

### 2️⃣ Filtros e Configuração 🔍

> **Localização**: Seção central principal (sempre visível)
> **Função**: Definir parâmetros de consulta para análise personalizada

Esta é a seção mais importante do sistema, onde você define **EXATAMENTE** quais dados deseja analisar.

#### 📅 Filtros de Período (Obrigatórios)

##### **Data Inicial** 📆

- **Formato**: DD/MM/AAAA
- **Valor Padrão**: Primeiro dia do mês atual (01/10/2025)
- **Limite Máximo**: Data atual
- **Validação**: Não pode ser posterior à data final
- **Exemplo**: Para analisar o mês de setembro, use 01/09/2025

##### **Data Final** 📅

- **Formato**: DD/MM/AAAA
- **Valor Padrão**: Data atual
- **Limite Máximo**: Data atual (não permite datas futuras)
- **Validação**: Não pode ser anterior à data inicial
- **Exemplo**: Para analisar até hoje, use a data atual

> ⚠️ **Atenção**: As datas inicial e final são **OBRIGATÓRIAS**. O sistema não permite consultas sem período definido!

#### 👤 Filtro de Vendedores (Opcional)

- **Tipo**: Seleção múltipla (pode escolher vários vendedores)
- **Opções**: Lista dinâmica de vendedores ativos no sistema
- **Comportamento Padrão**:
  - ✅ **Vazio** = Todos os vendedores (recomendado para visão geral)
  - ✅ **Selecionado** = Apenas vendedores específicos
- **Interface**: Dropdown com busca integrada (digite para filtrar)
- **Exemplo de Uso**:
  - Para análise geral: deixe vazio
  - Para avaliação individual: selecione um vendedor
  - Para comparar equipe: selecione múltiplos vendedores

> 💡 **Dica Profissional**: Use este filtro para avaliar performance individual ou comparar vendedores!

#### 📊 Filtro de Situação (Opcional)

- **Tipo**: Seleção múltipla
- **Opções Disponíveis**:
  - 🔵 **Em andamento** - Vendas em processamento
  - ✅ **Finalizada** - Vendas concluídas
  - ⏸️ **Pendente** - Aguardando ação
  - ❌ **Cancelada** - Vendas canceladas
- **Comportamento Padrão**: Vazio = Todas as situações
- **Recomendação**: Selecione "Finalizada" para análises de faturamento real

> 💡 **Quando usar cada filtro**:
> - **Todas**: Visão completa do pipeline de vendas
> - **Finalizada**: Análise de vendas confirmadas
> - **Em andamento**: Acompanhamento de vendas em processo
> - **Cancelada**: Análise de perda de vendas

---

#### 🎯 Botões de Ação

##### 🔍 **Aplicar Filtros** (Botão Principal)

- **Função**: Executa consulta personalizada com os filtros definidos
- **Cor**: Azul (botão primário)
- **Validações Automáticas**:
  - ✅ Verifica se datas foram preenchidas
  - ✅ Valida se data inicial ≤ data final
  - ✅ Alerta se período > 365 dias (performance)
  - ✅ Confirma disponibilidade de dados

**Fluxo de Execução**:
1. Sistema valida os filtros
2. Exibe mensagem de "Carregando dados..."
3. Busca dados no banco de dados
4. Calcula métricas automaticamente
5. Exibe resultados na tela

> ⏱️ **Tempo de processamento**: 2-10 segundos (depende do período)

##### 📅 **Dados do Mês Atual** (Botão Secundário)

- **Função**: Carregamento rápido do período corrente
- **Comportamento**:
  - ✅ Ignora todos os filtros personalizados
  - ✅ Carrega automaticamente de 01/10 até hoje
  - ✅ Inclui todos os vendedores
  - ✅ Inclui todas as situações
- **Quando usar**:
  - Análise rápida do mês corrente
  - Acompanhamento diário de vendas
  - Verificação de performance atual

> 🚀 **Atalho Rápido**: Use este botão para análises diárias!

---

#### ⚠️ Sistema de Validações

O sistema possui validações inteligentes para garantir qualidade dos dados:

| Situação | Tipo de Alerta | Ação do Sistema |
|----------|----------------|-----------------|
| **Data inicial > Data final** | ❌ Erro Crítico | Bloqueia consulta |
| **Período > 365 dias** | ⚠️ Aviso de Performance | Continua com alerta |
| **Campos obrigatórios vazios** | ❌ Erro de Validação | Bloqueia consulta |
| **Nenhum dado encontrado** | ℹ️ Informação | Exibe mensagem informativa |
| **Erro de conexão** | ❌ Erro de Sistema | Exibe detalhes do erro |

---

### 3️⃣ Resumo Executivo 📊

> **Exibição**: Automática após carregamento de dados
> **Função**: Visão panorâmica das métricas comerciais em cards visuais

Esta seção apresenta os **KPIs (Key Performance Indicators)** mais importantes do seu negócio.

#### 💰 Primeira Linha - Métricas Financeiras

##### 💵 **Total Entradas**

- **O que é**: Valores já recebidos (vencimento ≤ hoje)
- **Cálculo**: Soma dos pagamentos com data de vencimento passada ou atual
- **Formato**: R$ 0.000,00
- **Exemplo**: R$ 45.230,50
- **Importância**: Mostra o dinheiro que já está no caixa

##### 📅 **Total Parcelado**

- **O que é**: Valores a receber (vencimento > hoje)
- **Cálculo**: Soma dos pagamentos com data de vencimento futura
- **Formato**: R$ 0.000,00
- **Exemplo**: R$ 23.450,00
- **Importância**: Mostra o fluxo de caixa futuro

##### 💰 **Valor Total**

- **O que é**: Faturamento total do período
- **Cálculo**: Total Entradas + Total Parcelado
- **Formato**: R$ 0.000,00
- **Exemplo**: R$ 68.680,50
- **Importância**: Indica a performance geral de vendas

> 💡 **Análise Rápida**: Se Total Entradas for muito menor que Total Parcelado, pode indicar muitas vendas parceladas.

---

#### 📈 Segunda Linha - Métricas Operacionais

##### 🛒 **Total de Vendas**

- **O que é**: Quantidade de transações realizadas
- **Cálculo**: Contagem de registros únicos de vendas
- **Formato**: 0.000 vendas
- **Exemplo**: 234 vendas
- **Importância**: Mostra o volume de operações

##### 💳 **Ticket Médio**

- **O que é**: Valor médio por transação
- **Cálculo**: Valor Total ÷ Quantidade de Vendas
- **Formato**: R$ 0.000,00
- **Exemplo**: R$ 293,51
- **Importância**: Indica o poder de compra médio

> 📊 **Meta ideal**: Ticket médio crescente indica melhor mix de produtos ou upselling efetivo.

##### 📊 **Margem Média**

- **O que é**: Rentabilidade percentual média
- **Cálculo**: ((Valor Total - Custo Total) ÷ Valor Total) × 100
- **Formato**: 00,00%
- **Exemplo**: 35,50%
- **Observação**: Exibe "N/A" se dados de custo não disponíveis
- **Importância**: Mostra a lucratividade das vendas

> 💰 **Interpretação**:
> - Margem < 20%: Atenção, lucratividade baixa
> - Margem 20-40%: Saudável para varejo
> - Margem > 40%: Excelente rentabilidade

---

#### 📦 Terceira Linha - Métrica de Produtos

> **Nova Funcionalidade!** Análise de composição de vendas por tipo de produto

Esta seção apresenta a **distribuição de vendas entre Equipamentos e Acessórios**, permitindo análise estratégica do mix de produtos.

##### 🏋️ **Equipamentos**

- **O que é**: Valor total de vendas de equipamentos fitness
- **Classificação**: Todos os produtos **exceto** grupos "PEÇA DE REPOSIÇÃO" e "ACESSÓRIOS"
- **Grupos incluídos**: CARDIO, INFINITY FREE WEIGHT, NEW BLACK, GOLD, NEW PREMIUM, UNIQUE, INFINITY, ENERGY, PRODUTOS SEM GRUPO
- **Formato**: Percentual (%) + Valor monetário (R$)
- **Exemplo**:
  - **90.3%** - Representa 90,3% do faturamento total
  - **R$ 11.725.890,25** - Valor absoluto vendido em equipamentos
- **Importância**: Mostra participação dos produtos principais no faturamento

##### 🔧 **Acessórios**

- **O que é**: Valor total de vendas de acessórios e peças
- **Classificação**: Produtos dos grupos "PEÇA DE REPOSIÇÃO" e "ACESSÓRIOS"
- **Formato**: Percentual (%) + Valor monetário (R$)
- **Exemplo**:
  - **9.7%** - Representa 9,7% do faturamento total
  - **R$ 1.255.562,18** - Valor absoluto vendido em acessórios
- **Importância**: Mostra participação de produtos complementares

---

##### 🎯 **Cálculo Inteligente - Valor Proporcional**

> **Tecnologia Avançada**: O sistema utiliza cálculo proporcional para garantir precisão absoluta

**Como funciona**:

1. **Para cada produto de cada venda**:
   - Calcula a proporção do produto dentro daquela venda específica
   - Exemplo: Produto representa 80% do valor dos produtos da venda

2. **Aplica ao valor real da venda**:
   - Multiplica a proporção pelo `ValorTotal` da venda
   - Isso respeita descontos/acréscimos aplicados no nível da venda

3. **Garante precisão**:
   - ✅ **Equipamentos + Acessórios = Valor Total** (sempre)
   - ✅ Reflete valores reais faturados
   - ✅ Considera todos os ajustes comerciais

**Exemplo Prático**:

```
Venda com ValorTotal = R$ 1.000,00

Produtos registrados:
- Equipamento A: R$ 800,00
- Acessório B: R$ 300,00
- Soma produtos: R$ 1.100,00 (antes dos descontos da venda)

Cálculo proporcional:
- Proporção Equipamento: 800 ÷ 1.100 = 72,73%
- Proporção Acessório: 300 ÷ 1.100 = 27,27%

Valores ajustados:
- Equipamento A ajustado: 1.000 × 0,7273 = R$ 727,30
- Acessório B ajustado: 1.000 × 0,2727 = R$ 272,70
- Soma final: R$ 1.000,00 ✅ (bate exatamente com ValorTotal)
```

---

##### 📊 **Como Interpretar os Resultados**

**Análise de Mix de Produtos**:

| Cenário | Interpretação | Ação Recomendada |
|---------|---------------|------------------|
| **Equipamentos > 85%** | ✅ Foco em produtos principais | Continue estratégia, cross-sell acessórios |
| **Equipamentos 70-85%** | ✅ Mix equilibrado | Excelente, mantenha equilíbrio |
| **Equipamentos < 70%** | ⚠️ Alta venda de acessórios | Verifique estoque de equipamentos |
| **Acessórios > 30%** | ⚠️ Possível falta de equipamentos | Revisar disponibilidade de produtos principais |
| **Acessórios < 5%** | ⚠️ Baixa venda complementar | Incentive cross-selling |

**Estratégias Comerciais**:

1. **🎯 Cross-Selling**: Se acessórios < 10%, treine equipe para oferecer complementos
2. **📦 Gestão de Estoque**: Mantenha proporção de estoque similar à proporção de vendas
3. **💰 Margem**: Acessórios geralmente têm margem maior, balanceie o mix
4. **🎁 Combos**: Crie pacotes que equilibrem equipamentos + acessórios

**Análise Temporal**:

- **Tendência crescente de equipamentos**: Mercado aquecido, investimento em fitness
- **Tendência crescente de acessórios**: Clientes comprando complementos (bom sinal de satisfação)
- **Variação sazonal**: Normal ter mais acessórios próximo a datas comemorativas

> 💡 **Dica Estratégica**: Use esta métrica mensalmente para ajustar mix de produtos, negociações com fornecedores e estratégias de marketing!

---

### 4️⃣ Dados Detalhados 📋

> **Exibição**: Automática após carregamento
> **Função**: Visualização tabular completa dos registros

Esta seção exibe **TODAS** as vendas do período filtrado em formato de tabela interativa.

#### 🗂️ Colunas da Tabela

| Coluna | Descrição | Formato | Exemplo |
|---------|-----------|---------|---------|
| 👤 **Cliente** | Nome do cliente | Texto | João Silva |
| 🤝 **Vendedor** | Nome do vendedor | Texto | Maria Santos |
| 📦 **Valor Produtos** | Valor bruto dos produtos | R$ 0.000,00 | R$ 1.250,00 |
| 💸 **Desconto** | Valor do desconto aplicado | R$ 0.000,00 | R$ 125,00 |
| 💰 **Valor Total** | Valor líquido da venda | R$ 0.000,00 | R$ 1.125,00 |
| 📅 **Data** | Data da transação | DD/MM/AAAA | 15/10/2025 |

---

#### 🎨 Funcionalidades da Tabela

##### 🔄 **Ordenação de Colunas**

- **Como usar**: Clique no cabeçalho da coluna desejada
- **Comportamento**:
  - 1º clique: Ordem crescente (↑)
  - 2º clique: Ordem decrescente (↓)
  - 3º clique: Remove ordenação
- **Indicação Visual**: Seta no cabeçalho mostra direção
- **Exemplo de Uso**:
  - Ordene por "Valor Total" para ver maiores vendas
  - Ordene por "Data" para ver cronologia
  - Ordene por "Vendedor" para agrupar por pessoa

##### 🔍 **Busca Interna**

- **Localização**: Campo de busca acima da tabela
- **Função**: Filtro em tempo real (tipo e aparecem resultados)
- **Abrangência**: Busca em TODAS as colunas visíveis
- **Exemplo de Uso**:
  - Digite "Maria" para ver vendas dela
  - Digite "1000" para ver vendas acima deste valor
  - Digite "15/10" para ver vendas desta data

> 💡 **Dica**: Use a busca para encontrar rapidamente clientes ou valores específicos!

##### 📄 **Paginação**

- **Registros por página**: 50 (configurável)
- **Navegação**: Botões ◀ Anterior | Próxima ▶
- **Indicador**: Mostra "Página X de Y" e "Total de registros: Z"
- **Comportamento**: Mantém filtros e ordenação ao mudar página

##### 📥 **Download dos Dados**

- **Botão**: "📥 Download" no canto superior direito
- **Formato**: CSV (Excel compatível)
- **Nomenclatura**: `vendas_detalhadas_DDMMAAAA.csv`
- **Conteúdo**: Dados filtrados atualmente exibidos
- **Separador**: Vírgula (,) - compatível com Excel Brasil
- **Codificação**: UTF-8

**Como usar no Excel**:
1. Clique em "📥 Download"
2. Abra o arquivo no Excel
3. Se necessário: Dados > Texto para Colunas
4. Faça análises adicionais (tabelas dinâmicas, gráficos, etc.)

---

### 5️⃣ Análise Avançada 📈

> **Localização**: Expandível na parte inferior
> **Função**: Insights aprofundados de performance com rankings

Esta é a seção mais poderosa do sistema, apresentando análises estratégicas para tomada de decisão.

---

#### 🏆 Ranking de Vendedores

> **Nova Funcionalidade!** Análise completa de performance da equipe comercial

##### 📊 **Visualização do Ranking**

O sistema exibe os **Top 10 Vendedores** ordenados por valor de vendas, com três colunas principais:

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| 👤 **Vendedor** | Nome completo | Maria Santos |
| 💰 **Total Valor** | Faturamento do vendedor | R$ 125.450,00 |
| 📦 **Quantidade** | Número de vendas | 87 vendas |

##### 🎯 **Resumo Estatístico**

Ao lado do ranking, são exibidas métricas do melhor vendedor:

- **🏆 Vendedor Mais Produtivo**: Nome do 1º colocado
- **💰 Maior Valor**: Faturamento individual do líder

##### 📈 **Como Interpretar**

**Análise de Performance**:
- ✅ **Consistência**: Vendedor com muitas vendas E alto valor = performance consistente
- ⚠️ **Alto Ticket**: Poucas vendas mas valor alto = especialista em vendas grandes
- ⚠️ **Volume**: Muitas vendas mas valor médio baixo = oportunidade de upselling

**Identificação de Padrões**:
1. **Concentração**: Se 20% dos vendedores geram 80% do faturamento, há desequilíbrio
2. **Oportunidades**: Vendedores com muitas vendas mas ticket baixo podem melhorar
3. **Treinamento**: Vendedores com baixa performance podem precisar capacitação

> 💡 **Dica Gerencial**: Use este ranking para definir metas, bonificações e planos de treinamento!

---

#### 📦 Ranking de Produtos

> **Nova Funcionalidade!** Análise dos produtos mais vendidos e rentáveis

##### 📊 **Visualização do Ranking**

O sistema exibe os **Top 10 Produtos** mais vendidos, ordenados por valor total:

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| 📦 **Produto** | Nome do produto | Tênis Esportivo Nike Air |
| 🔢 **Quantidade** | Unidades vendidas | 156 unidades |
| 💰 **Valor Total** | Faturamento do produto | R$ 34.580,00 |

##### 🎯 **Resumo do Produto Líder**

- **🏆 Produto Mais Vendido**: Nome do 1º colocado
- **💰 Valor Total**: Faturamento individual do produto líder

##### 📈 **Como Interpretar**

**Análise de Mix de Produtos**:
- ✅ **Carro-chefe**: Produto com maior faturamento = principal gerador de receita
- ✅ **Volume Alto**: Muitas unidades vendidas = produto popular
- ⚠️ **Ticket Alto**: Poucas unidades mas valor alto = produto premium

**Gestão de Estoque Estratégica**:
1. **Prioridade**: Produtos no top 10 devem ter estoque garantido
2. **Promoções**: Produtos não listados podem precisar de ações promocionais
3. **Margem**: Cruze com dados de margem para identificar produtos mais rentáveis

**Decisões Comerciais**:
- 🔄 **Reposição**: Produtos top devem ter reposição prioritária
- 📢 **Marketing**: Invista em divulgação dos produtos mais vendidos
- 🎯 **Negociação**: Use volume para negociar melhores preços com fornecedores

> 💡 **Estratégia de Vendas**: Treine a equipe para fazer upselling com produtos do ranking!

---

#### 📈 Tendência por Período

##### 📊 **Análise Temporal**

O sistema agrupa as vendas por período (dia, semana ou mês) mostrando:

- **📅 Período**: Data ou intervalo
- **💰 Valor Total**: Faturamento do período
- **📦 Quantidade**: Número de vendas
- **💳 Ticket Médio**: Valor médio por venda

##### 🎯 **Identificação de Padrões**

**Sazonalidade**:
- Identifique dias da semana com mais vendas
- Reconheça períodos de alta e baixa demanda
- Planeje ações promocionais em períodos fracos

**Tendências**:
- Vendas crescentes = estratégia funcionando
- Vendas decrescentes = necessário ação corretiva
- Vendas estáveis = mercado maduro

---

## 🎓 Guia de Melhores Práticas

### 📊 Para Análise Eficiente

#### 🌅 **Análise Matinal** (Recomendado Diariamente)
1. Clique em **"📅 Dados do Mês Atual"**
2. Verifique o **Total de Vendas** do dia anterior
3. Analise o **Ranking de Vendedores** atualizado
4. Compare com a meta do mês

#### 📈 **Análise Semanal** (Segunda-feira)
1. Defina filtro de **7 dias** (segunda a domingo)
2. Exporte dados para análise detalhada
3. Compare com semana anterior
4. Identifique oportunidades de melhoria

#### 📆 **Análise Mensal** (Início do mês)
1. Filtre o **mês anterior completo**
2. Analise **Ranking de Vendedores** mensal
3. Revise **Ranking de Produtos** para reposição
4. Gere relatório executivo para diretoria

---

### 🔍 Estratégias de Filtros

#### 🎯 **Para Avaliação de Vendedor**
```
📅 Período: Último mês
👤 Vendedor: [Selecione um específico]
📊 Situação: Finalizada
```
**Objetivo**: Avaliar performance individual real

#### 📦 **Para Análise de Produtos**
```
📅 Período: Últimos 3 meses
👤 Vendedor: [Todos]
📊 Situação: Finalizada
```
**Objetivo**: Identificar tendências de produtos

#### 💰 **Para Análise Financeira**
```
📅 Período: Mês atual
👤 Vendedor: [Todos]
📊 Situação: [Todas]
```
**Objetivo**: Visão completa do pipeline financeiro

---

### 📈 Interpretação de Métricas

#### 💳 **Ticket Médio Ideal**

| Faixa | Interpretação | Ação |
|-------|---------------|------|
| **Crescente** | ✅ Upselling funcionando | Continue estratégia |
| **Estável** | ⚠️ Zona de conforto | Teste novos produtos |
| **Decrescente** | ❌ Problema | Reveja mix e promoções |

#### 📊 **Proporção Entrada/Parcelado**

| Proporção | Situação | Interpretação |
|-----------|----------|---------------|
| **70/30** | ✅ Ideal | Boa liquidez |
| **50/50** | ⚠️ Atenção | Fluxo balanceado |
| **30/70** | ❌ Crítico | Muito parcelado |

#### 🏆 **Concentração de Vendedores**

| Cenário | Interpretação | Ação Necessária |
|---------|---------------|-----------------|
| **Top 3 = 80%** | ❌ Muito concentrado | Desenvolver outros |
| **Top 5 = 70%** | ⚠️ Desequilibrado | Treinar equipe |
| **Top 10 = 60%** | ✅ Bem distribuído | Manter estratégia |

---

## 🚨 Solução de Problemas

### ❌ Problemas Comuns e Soluções

#### **"❌ Nenhum dado encontrado"**

**Possíveis Causas**:
- Filtros muito restritivos (vendedor específico sem vendas)
- Período sem movimento comercial
- Situação selecionada sem registros

**Soluções**:
1. Remova filtros de vendedor e situação
2. Amplie o período de datas
3. Use o botão "📅 Dados do Mês Atual" para teste
4. Verifique se o período selecionado está correto

---

#### **"❌ Erro de conectividade" ou "Erro no health check"**

**Possíveis Causas**:
- Problema de rede
- Servidor de banco de dados offline
- Credenciais de acesso incorretas

**Soluções**:
1. Verifique sua conexão com internet
2. Aguarde alguns minutos e tente novamente
3. Entre em contato com TI/Suporte
4. Verifique status no menu "Sistema"

---

#### **"⚠️ Performance lenta" ou carregamento demorado**

**Possíveis Causas**:
- Período muito extenso (> 6 meses)
- Grande volume de registros
- Horário de pico do sistema

**Soluções**:
1. Reduza o intervalo de datas (máx. 3 meses)
2. Use filtros específicos (vendedor ou situação)
3. Exporte dados e analise offline
4. Execute fora do horário comercial

---

#### **"⚠️ IDs de vendas não disponíveis" no Ranking de Produtos**

**Possíveis Causas**:
- Dados carregados sem ID
- Problema na estrutura dos dados

**Soluções**:
1. Recarregue os dados com "🔍 Aplicar Filtros"
2. Limpe o cache (F5)
3. Se persistir, contate suporte técnico

---

### 🔧 Procedimentos de Recuperação

#### 1️⃣ **Limpeza Básica** (Sempre tente primeiro)
```
1. Pressione F5 para atualizar página
2. Limpe filtros e aplique novamente
3. Use "📅 Dados do Mês Atual" para teste
```

#### 2️⃣ **Limpeza Avançada** (Se persistir)
```
1. Limpe cache do navegador (Ctrl + Shift + Del)
2. Feche e reabra o navegador
3. Faça logout e login novamente
```

#### 3️⃣ **Suporte Técnico** (Último recurso)
```
1. Anote a mensagem de erro exata
2. Tire print da tela
3. Registre data/hora do problema
4. Entre em contato com suporte
```

---

## 📚 Glossário de Termos Técnicos

| Termo | Definição | Exemplo Prático |
|-------|-----------|-----------------|
| **Ticket Médio** | Valor médio por transação de venda | R$ 250,00 por venda |
| **Margem** | Percentual de lucro sobre faturamento | 35% de lucro |
| **Entrada** | Valores já recebidos (parcelas vencidas) | R$ 10.000 em caixa |
| **Parcelado** | Valores a receber (parcelas futuras) | R$ 5.000 a receber |
| **Vendedor Ativo** | Vendedor com permissão no sistema | Com acesso liberado |
| **Situação** | Status atual da venda | Finalizada, Pendente, etc. |
| **KPI** | Indicador-chave de performance | Métricas principais |
| **Pipeline** | Funil de vendas em andamento | Vendas em processo |
| **Upselling** | Venda de produto superior/adicional | Combo ou upgrade |
| **Mix de Produtos** | Variedade de produtos vendidos | Portfólio comercial |
| **Equipamentos** | Produtos fitness principais | Esteiras, musculação, etc |
| **Acessórios** | Produtos complementares e peças | Peças de reposição, complementos |
| **Cálculo Proporcional** | Distribuição de valor por proporção | Ajuste de valores por produto |
| **Valor Proporcional** | Valor ajustado respeitando total da venda | Produto com desconto proporcional |
| **Sazonalidade** | Variação por período do ano | Vendas de natal |
| **Health Check** | Verificação de saúde do sistema | Sistema funcionando? |

---

## 🎯 Casos de Uso Práticos

### 📊 Caso 1: Avaliação de Performance Mensal

**Objetivo**: Avaliar desempenho da equipe no último mês

**Passo a Passo**:
1. Defina Data Inicial: 01/09/2025
2. Defina Data Final: 30/09/2025
3. Vendedores: [Todos]
4. Situação: Finalizada
5. Clique em "🔍 Aplicar Filtros"
6. Analise o **Ranking de Vendedores**
7. Exporte dados para Excel
8. Gere relatório para diretoria

---

### 📦 Caso 2: Reposição de Estoque

**Objetivo**: Identificar produtos para reposição urgente

**Passo a Passo**:
1. Use "📅 Dados do Mês Atual"
2. Expanda "📈 Análise Avançada"
3. Verifique **Ranking de Produtos**
4. Anote os Top 10 produtos
5. Cruze com estoque atual
6. Priorize reposição dos top 5
7. Negocie com fornecedores

---

### 💰 Caso 3: Análise de Fluxo de Caixa

**Objetivo**: Entender entrada de dinheiro

**Passo a Passo**:
1. Filtre últimos 30 dias
2. Situação: [Todas]
3. Verifique **Total Entradas** vs **Total Parcelado**
4. Se parcelado > 60%, planeje ações para entrada imediata
5. Considere promoções "à vista"

---

### 📦 Caso 4: Análise de Mix de Produtos

**Objetivo**: Avaliar composição de vendas e ajustar estratégia comercial

**Passo a Passo**:
1. Use "📅 Dados do Mês Atual"
2. Visualize as métricas **🏋️ Equipamentos** e **🔧 Acessórios**
3. Anote os percentuais e valores
4. Compare com mês anterior (use filtro personalizado)
5. **Análise**:
   - Se Acessórios < 5%: Treinar equipe em cross-selling
   - Se Acessórios > 30%: Verificar disponibilidade de equipamentos
   - Se Equipamentos < 70%: Revisar estoque de produtos principais
6. **Ação**:
   - Ajustar mix de estoque baseado na proporção de vendas
   - Criar combos que equilibrem equipamentos + acessórios
   - Negociar com fornecedores baseado no volume de cada categoria

**Exemplo Prático**:
```
Resultado encontrado:
- 🏋️ Equipamentos: 92,5% (R$ 845.230,00)
- 🔧 Acessórios: 7,5% (R$ 68.560,00)

Análise:
✅ Boa participação de equipamentos
⚠️ Acessórios abaixo de 10%

Ação:
- Treinar vendedores para oferecer acessórios
- Criar displays de acessórios nas vitrines
- Oferecer desconto em combo equipamento + acessório
```

---

## 📞 Suporte e Contato

### 🆘 Quando Buscar Suporte?

- ❌ Erros persistentes após limpeza de cache
- 🔒 Problemas de acesso ou permissões
- 🐛 Comportamento inesperado do sistema
- 💡 Dúvidas sobre funcionalidades
- 📊 Necessidade de relatórios customizados

### 📧 Canais de Suporte

**Suporte Técnico - TI**

📧 Email: [ti@oficialsport.com.br](mailto:ti@oficialsport.com.br)

👤 Contato: Marcelo Areco

**Informações para Abrir Chamado**:
1. Nome completo e setor
2. Descrição detalhada do problema
3. Print da tela (se possível)
4. Mensagem de erro exata
5. Data e hora do problema
6. Filtros que estava usando

---

## 📋 Checklist de Utilização Diária

Use este checklist para garantir uso eficiente do sistema:

### ☀️ Manhã (9h-10h)
- [ ] Acessar sistema
- [ ] Clicar em "📅 Dados do Mês Atual"
- [ ] Verificar vendas do dia anterior
- [ ] Analisar performance acumulada do mês
- [ ] Verificar ranking de vendedores
- [ ] Conferir mix de produtos (Equipamentos vs Acessórios)

### 🌆 Tarde (15h-16h)
- [ ] Atualizar dados novamente
- [ ] Verificar vendas do dia
- [ ] Analisar desvios da meta
- [ ] Tomar ações corretivas se necessário

### 🌙 Final do Dia (17h-18h)
- [ ] Gerar relatório do dia
- [ ] Exportar dados se necessário
- [ ] Planejar ações para amanhã

---

## 🎓 Certificação de Leitura

Ao finalizar este manual, você estará apto a:

✅ Navegar com eficiência pelo Relatório de Vendas

✅ Aplicar filtros personalizados corretamente

✅ Interpretar métricas e KPIs comerciais

✅ Analisar rankings de vendedores e produtos

✅ Identificar oportunidades de melhoria

✅ Exportar e manipular dados

✅ Solucionar problemas comuns

✅ Tomar decisões baseadas em dados

---

## 📖 Histórico de Atualizações

| Versão | Data | Alterações |
|--------|------|------------|
| **1.0** | Setembro 2025 | Versão inicial do manual |
| **2.0** | Outubro 2025 | ✨ Adicionado Ranking de Vendedores<br/>✨ Adicionado Ranking de Produtos<br/>📝 Seção de filtros expandida<br/>🎯 Casos de uso práticos<br/>📊 Interpretação de métricas<br/>🎓 Checklist de utilização |
| **2.1** | 30 Outubro 2025 | ✨ **Nova Métrica de Produtos**<br/>🏋️ Card de Equipamentos com % e valor<br/>🔧 Card de Acessórios com % e valor<br/>🎯 Cálculo inteligente por valor proporcional<br/>✅ Garantia de soma exata com Valor Total<br/>📊 Guia completo de interpretação de mix<br/>🎨 Tamanhos de fonte padronizados nos cards |

---


📧 **Dúvidas?** Entre em contato: [ti@oficialsport.com.br](mailto:ti@oficialsport.com.br)

---

**SGR** | **Transformando dados em decisões** | **2025** 🚀
