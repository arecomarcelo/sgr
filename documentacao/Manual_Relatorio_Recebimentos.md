# 💰 Manual de Utilização - Relatório de Recebimentos SGR

## 🎯 Visão Geral

O **Relatório de Recebimentos SGR** é uma ferramenta completa e interativa para análise e acompanhamento de contas a receber. Desenvolvido com interface moderna e intuitiva, este módulo oferece recursos avançados de filtragem, visualização de dados e métricas financeiras em tempo real.

### 💡 Principais Recursos

✅ **Filtros Inteligentes** - Sistema avançado de filtros por período
✅ **Métricas em Tempo Real** - Acompanhamento instantâneo de valores
✅ **Tabela Interativa** - Visualização com ordenação e busca
✅ **Exportação de Dados** - Relatórios em formato Excel/CSV formatados
✅ **Carregamento Automático** - Dados do mês atual ao acessar

---

## 🏗️ Estrutura do Sistema

### 📋 Seções Principais

O sistema está organizado em **três seções principais**, cada uma com funcionalidades específicas:

| Seção | Ícone | Função Principal |
|-------|-------|------------------|
| **Filtros e Configuração** | 🔍 | Definição de parâmetros de consulta |
| **Métricas de Recebimento** | 📊 | Visão panorâmica dos valores |
| **Dados Detalhados** | 📋 | Visualização tabular dos registros |

---

## 🚀 Guia de Utilização Passo a Passo

### 1️⃣ Carregamento Automático 🔄

> **Comportamento Inicial**: Ao acessar o módulo, o sistema carrega automaticamente os dados do mês atual

#### 📊 O que acontece automaticamente?

1. Sistema identifica o primeiro dia do mês atual
2. Busca todos os recebimentos até a data de hoje
3. Calcula métricas automaticamente
4. Exibe dados na tabela

> 💡 **Dica**: Você não precisa fazer nada na primeira vez - os dados já estarão carregados!

---

### 2️⃣ Filtros e Configuração 🔍

> **Localização**: Seção central principal (sempre visível)
> **Função**: Definir parâmetros de consulta para análise personalizada

Esta é a seção principal do sistema, onde você define **EXATAMENTE** quais dados deseja analisar.

#### 📅 Filtros de Período (Obrigatórios)

##### **Data Inicial** 📆

- **Formato**: DD/MM/AAAA
- **Valor Padrão**: Primeiro dia do mês atual
- **Validação**: Não pode ser posterior à data final
- **Exemplo**: Para analisar o mês de dezembro, use 01/12/2025

##### **Data Final** 📅

- **Formato**: DD/MM/AAAA
- **Valor Padrão**: Data atual
- **Validação**: Não pode ser anterior à data inicial
- **Exemplo**: Para analisar até hoje, use a data atual

> ⚠️ **Atenção**: As datas inicial e final são **OBRIGATÓRIAS**. O sistema não permite consultas sem período definido!

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
  - ✅ Carrega automaticamente de 01/mês até hoje
  - ✅ Inclui todos os recebimentos do período
- **Quando usar**:
  - Análise rápida do mês corrente
  - Acompanhamento diário de recebimentos
  - Verificação de valores a receber

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

### 3️⃣ Métricas de Recebimento 📊

> **Exibição**: Automática após carregamento de dados
> **Função**: Visão panorâmica dos valores em cards visuais

Esta seção apresenta os **KPIs (Key Performance Indicators)** mais importantes dos seus recebimentos.

#### 📊 Cards de Métricas

##### 📅 **Período Filtrado**

- **O que é**: Intervalo de datas da consulta atual
- **Formato**: DD/MM/AAAA a DD/MM/AAAA
- **Exemplo**: 01/12/2025 a 15/12/2025
- **Importância**: Confirma o período analisado

##### 📋 **Total de Recebimentos**

- **O que é**: Quantidade de registros no período
- **Cálculo**: Contagem de parcelas/títulos
- **Formato**: 0.000
- **Exemplo**: 234 recebimentos
- **Importância**: Mostra o volume de operações

##### 💰 **Valor Total**

- **O que é**: Soma de todos os valores a receber
- **Cálculo**: Soma dos valores de todas as parcelas
- **Formato**: R$ 0.000,00
- **Exemplo**: R$ 601.539,43
- **Importância**: Indica o montante total a receber

> 💡 **Análise Rápida**: Compare o Valor Total com meses anteriores para identificar tendências!

---

### 4️⃣ Dados Detalhados 📋

> **Exibição**: Automática após carregamento
> **Função**: Visualização tabular completa dos registros

Esta seção exibe **TODOS** os recebimentos do período filtrado em formato de tabela interativa.

#### 🗂️ Colunas da Tabela

| Coluna | Descrição | Formato | Exemplo |
|--------|-----------|---------|---------|
| 📅 **Vencimento** | Data de vencimento da parcela | DD/MM/AAAA | 15/12/2025 |
| 💰 **Valor** | Valor da parcela | R$ 0.000,00 | R$ 1.250,00 |
| 💳 **Forma de Pagamento** | Método de pagamento | Texto | Boleto Bancário |
| 👤 **Cliente** | Nome do cliente | Texto | João Silva |

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
  - Ordene por "Valor" para ver maiores recebimentos
  - Ordene por "Vencimento" para ver cronologia
  - Ordene por "Cliente" para agrupar por pessoa

##### 🔍 **Busca Interna (Filtro Flutuante)**

- **Localização**: Campo de busca abaixo de cada cabeçalho
- **Função**: Filtro em tempo real (digite e aparecem resultados)
- **Abrangência**: Cada coluna tem seu próprio filtro
- **Exemplo de Uso**:
  - Digite "Maria" no filtro de Cliente para ver recebimentos dela
  - Digite "Boleto" no filtro de Forma de Pagamento
  - Digite "1000" no filtro de Valor para ver valores específicos

> 💡 **Dica**: Use os filtros para encontrar rapidamente clientes ou valores específicos!

##### 📥 **Download dos Dados**

Dois formatos de exportação disponíveis:

###### 📄 **Download CSV**

- **Formato**: CSV (compatível com Excel)
- **Nomenclatura**: `recebimentos_DDMMAAAA_HHMMSS.csv`
- **Conteúdo**: Dados atualmente exibidos
- **Separador**: Vírgula (,)
- **Codificação**: UTF-8

###### 📊 **Download Excel**

- **Formato**: XLSX (Excel nativo)
- **Nomenclatura**: `recebimentos_DDMMAAAA_HHMMSS.xlsx`
- **Formatação Especial**:
  - 📌 Título estilizado no topo
  - 🎨 Cabeçalhos coloridos (azul)
  - 💰 Valores monetários formatados (R$)
  - 📅 Datas formatadas (DD/MM/AAAA)
  - 📊 Linha de totais automática
  - 🔒 Cabeçalho congelado para facilitar navegação
  - 🦓 Formatação zebra (linhas alternadas)

**Como usar no Excel**:
1. Clique em "📊 Download Excel"
2. Abra o arquivo no Excel
3. O arquivo já vem formatado e pronto para uso
4. Faça análises adicionais (tabelas dinâmicas, gráficos, etc.)

---

## 🎓 Guia de Melhores Práticas

### 📊 Para Análise Eficiente

#### 🌅 **Análise Matinal** (Recomendado Diariamente)
1. Acesse o módulo de Recebimentos
2. Dados do mês já estarão carregados
3. Verifique o **Valor Total** a receber
4. Analise vencimentos do dia
5. Exporte para controle se necessário

#### 📈 **Análise Semanal** (Segunda-feira)
1. Defina filtro de **7 dias** futuros
2. Verifique recebimentos da semana
3. Identifique clientes com valores altos
4. Planeje cobranças se necessário

#### 📆 **Análise Mensal** (Início do mês)
1. Filtre o **mês anterior completo**
2. Analise o total recebido
3. Compare com projeção/meta
4. Gere relatório Excel para arquivo

---

### 🔍 Estratégias de Filtros

#### 🎯 **Para Visão Geral do Mês**
```
📅 Período: Mês atual
```
**Objetivo**: Ver todos os recebimentos do mês

#### 📦 **Para Análise de Período Específico**
```
📅 Período: Defina datas personalizadas
```
**Objetivo**: Analisar intervalo específico

#### 💰 **Para Fluxo de Caixa**
```
📅 Período: Próximos 30 dias
```
**Objetivo**: Planejar entrada de recursos

---

### 📈 Interpretação de Métricas

#### 📊 **Análise de Volume**

| Faixa de Registros | Interpretação | Ação |
|-------------------|---------------|------|
| **> 500 registros** | Alto volume | Considere filtros mais específicos |
| **100-500 registros** | Volume normal | Análise padrão |
| **< 100 registros** | Baixo volume | Verifique período |

#### 💰 **Análise de Valores**

| Situação | Interpretação | Recomendação |
|----------|---------------|--------------|
| **Valor crescente** | ✅ Vendas em alta | Continue estratégia |
| **Valor estável** | ⚠️ Mercado equilibrado | Busque crescimento |
| **Valor decrescente** | ❌ Atenção | Reveja estratégia comercial |

---

## 🚨 Solução de Problemas

### ❌ Problemas Comuns e Soluções

#### **"❌ Nenhum dado encontrado"**

**Possíveis Causas**:
- Período sem recebimentos
- Filtros muito restritivos

**Soluções**:
1. Amplie o período de datas
2. Use o botão "📅 Dados do Mês Atual" para teste
3. Verifique se o período selecionado está correto

---

#### **"❌ Erro de conectividade" ou "Erro no health check"**

**Possíveis Causas**:
- Problema de rede
- Servidor de banco de dados offline

**Soluções**:
1. Verifique sua conexão com internet
2. Aguarde alguns minutos e tente novamente
3. Entre em contato com TI/Suporte

---

#### **"⚠️ Performance lenta" ou carregamento demorado**

**Possíveis Causas**:
- Período muito extenso (> 6 meses)
- Grande volume de registros

**Soluções**:
1. Reduza o intervalo de datas (máx. 3 meses)
2. Exporte dados e analise offline
3. Execute fora do horário comercial

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
| **Recebimento** | Parcela ou título a receber | Boleto de R$ 1.000 |
| **Vencimento** | Data limite para pagamento | 15/12/2025 |
| **Forma de Pagamento** | Método de cobrança | Boleto, Cartão, PIX |
| **KPI** | Indicador-chave de performance | Métricas principais |
| **Health Check** | Verificação de saúde do sistema | Sistema funcionando? |
| **Filtro Flutuante** | Busca em tempo real por coluna | Digite para filtrar |

---

## 🎯 Casos de Uso Práticos

### 📊 Caso 1: Acompanhamento Diário

**Objetivo**: Verificar recebimentos do dia

**Passo a Passo**:
1. Acesse o módulo de Recebimentos
2. Dados do mês já estarão carregados
3. Use o filtro flutuante na coluna "Vencimento"
4. Digite a data de hoje
5. Visualize recebimentos do dia
6. Tome ações de cobrança se necessário

---

### 📦 Caso 2: Exportação para Arquivo

**Objetivo**: Gerar relatório mensal para arquivo

**Passo a Passo**:
1. Use "📅 Dados do Mês Atual" ou defina período
2. Verifique se os dados estão corretos
3. Clique em "📊 Download Excel"
4. Arquivo será baixado formatado
5. Salve em pasta de arquivo mensal
6. Use para relatórios gerenciais

---

### 💰 Caso 3: Planejamento de Fluxo de Caixa

**Objetivo**: Projetar entradas dos próximos dias

**Passo a Passo**:
1. Defina Data Inicial: Hoje
2. Defina Data Final: 30 dias à frente
3. Clique em "🔍 Aplicar Filtros"
4. Analise o **Valor Total** a receber
5. Ordene por Vencimento para ver cronologia
6. Exporte para análise detalhada

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
- [ ] Acessar módulo de Recebimentos
- [ ] Verificar valor total a receber no mês
- [ ] Analisar vencimentos do dia
- [ ] Identificar valores importantes

### 🌆 Tarde (15h-16h)
- [ ] Atualizar dados se necessário
- [ ] Verificar novos lançamentos
- [ ] Tomar ações de cobrança pendentes

### 🌙 Final do Dia (17h-18h)
- [ ] Gerar relatório do dia se necessário
- [ ] Exportar dados importantes
- [ ] Planejar cobranças para amanhã

---

## 🎓 Certificação de Leitura

Ao finalizar este manual, você estará apto a:

✅ Navegar com eficiência pelo Relatório de Recebimentos

✅ Aplicar filtros personalizados corretamente

✅ Interpretar métricas financeiras

✅ Utilizar a tabela interativa com ordenação e busca

✅ Exportar dados em CSV e Excel formatado

✅ Solucionar problemas comuns

✅ Tomar decisões baseadas em dados

---

## 📖 Histórico de Atualizações

### Versão 1.0 - Janeiro 2026
- ✨ Versão inicial do manual
- 📊 Guia completo de utilização
- 📥 Documentação de exportação
- 🎯 Casos de uso práticos

---

📧 **Dúvidas?** Entre em contato: [ti@oficialsport.com.br](mailto:ti@oficialsport.com.br)

---

**SGR** | **Transformando dados em decisões** | **2026** 🚀
