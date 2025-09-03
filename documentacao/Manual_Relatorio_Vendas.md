# 📊 Manual de Utilização - Relatório de Vendas SGR

## 🔍 Visão Geral

O **Relatório de Vendas SGR** é uma ferramenta completa e interativa para análise de desempenho comercial, desenvolvida com interface moderna e intuitiva. Este módulo oferece recursos avançados de filtragem, visualização de dados e análise de métricas comerciais.

---

## 🏗️ Estrutura do Sistema

### 📋 Seções Principais

O sistema está organizado em **cinco seções principais**, cada uma com funcionalidades específicas:

1. **🔄 Informações de Atualização**
2. **🔍 Filtros e Configuração**
3. **📊 Resumo Executivo**
4. **📋 Dados Detalhados**
5. **📈 Análise Avançada**

---

## 🚀 Guia de Utilização Detalhado

### 1. 🔄 Seção de Informações de Atualização

> **Localização**: Expandível no topo da tela
> **Função**: Monitoramento da sincronização de dados

#### 📊 Métricas Exibidas:

| Métrica | Descrição | Exemplo |
|---------|-----------|---------|
| **Data** | Data da última atualização | 03/09/2025 |
| **Hora** | Horário da última sincronização | 14:30:15 |
| **Período** | Intervalo dos dados processados | 01/09 - 03/09 |
| **Inseridos** | Novos registros adicionados | 127 |
| **Atualizados** | Registros modificados | 45 |

#### ⚙️ Como Utilizar:
1. **Clique** no expandir "🔄 Informações de Atualização"
2. **Visualize** as métricas de sincronização
3. **Verifique** se os dados estão atualizados

---

### 2. 🔍 Seção de Filtros e Configuração

> **Localização**: Seção central principal
> **Função**: Definição de parâmetros de consulta

#### 📅 Filtros de Período

##### **Data Inicial**
- **Formato**: DD/MM/AAAA
- **Valor Padrão**: Primeiro dia do mês atual
- **Limite Máximo**: Data atual
- **Validação**: Não pode ser posterior à data final

##### **Data Final**
- **Formato**: DD/MM/AAAA
- **Valor Padrão**: Data atual
- **Limite Máximo**: Data atual
- **Validação**: Não pode ser anterior à data inicial

#### 👤 Filtros de Vendedores

- **Tipo**: Seleção múltipla
- **Opções**: Lista dinâmica de vendedores ativos
- **Comportamento**: Vazio = Todos os vendedores
- **Interface**: Dropdown com busca integrada

#### 📊 Filtros de Situação

- **Tipo**: Seleção múltipla
- **Opções**: Lista de situações de vendas disponíveis
- **Comportamento**: Vazio = Todas as situações
- **Critério Padrão**: "Em andamento"

#### 🎯 Botões de Ação

##### **🔍 Aplicar Filtros**
- **Função**: Executa consulta personalizada
- **Validações**: 
  - Datas obrigatórias
  - Intervalo de datas válido
  - Aviso para períodos > 365 dias

##### **📅 Dados do Mês Atual**
- **Função**: Carregamento rápido do período corrente
- **Comportamento**: Ignora filtros personalizados
- **Período**: 1º dia do mês até data atual

#### ⚠️ Validações e Alertas

| Situação | Alerta | Ação |
|----------|--------|------|
| Data inicial > Data final | ❌ Erro crítico | Bloqueio da consulta |
| Período > 365 dias | ⚠️ Aviso de performance | Continua execução |
| Campos obrigatórios vazios | ❌ Erro de validação | Bloqueio da consulta |

---

### 3. 📊 Seção Resumo Executivo

> **Exibição**: Automática após carregamento de dados
> **Função**: Visão panorâmica das métricas comerciais

#### 💰 Primeira Linha - Métricas Financeiras

##### **Total Entradas**
- **Descrição**: Valores já recebidos (vencimento ≤ hoje)
- **Cálculo**: Soma dos pagamentos com data de vencimento passada
- **Formato**: R$ 0.000,00

##### **Total Parcelado**
- **Descrição**: Valores a receber (vencimento > hoje)
- **Cálculo**: Soma dos pagamentos com data de vencimento futura
- **Formato**: R$ 0.000,00

##### **Valor Total**
- **Descrição**: Faturamento total do período
- **Cálculo**: Soma de todos os valores de vendas
- **Formato**: R$ 0.000,00

#### 📈 Segunda Linha - Métricas Operacionais

##### **Total de Vendas**
- **Descrição**: Quantidade de transações
- **Cálculo**: Contagem de registros únicos
- **Formato**: 0.000 vendas

##### **Ticket Médio**
- **Descrição**: Valor médio por transação
- **Cálculo**: Valor Total ÷ Quantidade de Vendas
- **Formato**: R$ 0.000,00

##### **Margem Média**
- **Descrição**: Rentabilidade percentual média
- **Cálculo**: ((Valor Total - Custo Total) ÷ Valor Total) × 100
- **Formato**: 00,00%
- **Observação**: Exibe "N/A" se dados de custo indisponíveis

---

### 4. 📋 Seção Dados Detalhados

> **Exibição**: Automática após carregamento
> **Função**: Visualização tabular dos registros

#### 🗂️ Colunas Exibidas

| Coluna | Descrição | Formato |
|---------|-----------|---------|
| **Cliente** | Nome do cliente | Texto |
| **Vendedor** | Nome do vendedor | Texto |
| **Valor Produtos** | Valor bruto dos produtos | R$ 0.000,00 |
| **Desconto** | Valor do desconto aplicado | R$ 0.000,00 |
| **Valor Total** | Valor líquido da venda | R$ 0.000,00 |
| **Data** | Data da transação | DD/MM/AAAA |

#### 📊 Funcionalidades da Tabela

##### **Ordenação**
- **Como usar**: Clique no cabeçalho da coluna
- **Comportamento**: Alternância crescente/decrescente
- **Indicação**: Seta no cabeçalho

##### **Busca Interna**
- **Localização**: Campo de busca sobre a tabela
- **Função**: Filtro em tempo real
- **Abrangência**: Todas as colunas visíveis

##### **Paginação**
- **Registros por página**: Configurável
- **Navegação**: Botões anterior/próximo
- **Indicador**: "Página X de Y"

##### **📥 Download dos Dados**
- **Formato**: CSV (Excel compatível)
- **Nomenclatura**: vendas_detalhadas_DDMMAAAA.csv
- **Conteúdo**: Dados filtrados atualmente exibidos

---

### 5. 📈 Seção Análise Avançada

> **Localização**: Expandível na parte inferior
> **Função**: Insights aprofundados de performance

#### 🏆 Análise por Vendedores

##### **Top 10 Vendedores - Valor**
- **Critério**: Ordenação por valor total de vendas
- **Colunas Exibidas**:
  - Nome do Vendedor
  - Valor Total (R$)
  - Quantidade de Vendas

##### **📊 Resumo Estatístico**
- **Vendedor Mais Produtivo**: Nome do 1º colocado em valor
- **Maior Valor Individual**: Maior faturamento por vendedor

#### 📈 Análise Temporal

##### **Tendência por Período**
- **Agrupamento**: Por mês, semana ou dia (configurável)
- **Métricas**: Valor total, quantidade, ticket médio
- **Visualização**: Tabela resumo temporal

#### 🎯 Métricas de Performance

- **Distribuição de Vendas**: Análise da distribuição por vendedor
- **Concentração de Resultados**: Identificação de padrões
- **Sazonalidade**: Identificação de tendências temporais

---

## 🚨 Solução de Problemas

### ❌ Problemas Comuns

#### **"Nenhum dado encontrado"**
- **Causa**: Filtros muito restritivos
- **Solução**: Ampliar período ou remover filtros específicos

#### **"Erro de conectividade"**
- **Causa**: Problema de rede ou servidor
- **Solução**: Verificar conexão e tentar novamente

#### **"Performance lenta"**
- **Causa**: Período muito extenso (> 365 dias)
- **Solução**: Reduzir intervalo de datas

### 🔧 Procedimentos de Recuperação

1. **Limpar Cache da Sessão**: Atualizar página (F5)
2. **Verificar Conectividade**: Menu > Status do Sistema
3. **Contatar Suporte**: Em caso de erros persistentes

---

## 📚 Glossário de Termos

| Termo | Definição |
|-------|-----------|
| **Ticket Médio** | Valor médio por transação de venda |
| **Margem** | Percentual de lucro sobre o faturamento |
| **Entrada** | Valores já recebidos (parcelas vencidas) |
| **Parcelado** | Valores a receber (parcelas futuras) |
| **Vendedor Ativo** | Vendedor com permissão no sistema |
| **Situação** | Status atual da venda (Em andamento, Finalizada, etc.) |

---

## 🎓 Dicas de Melhores Práticas

### 📊 Análise Eficiente
1. **Inicie sempre** com dados do mês atual
2. **Use filtros específicos** para análises pontuais  
3. **Exporte dados** para análises externas detalhadas
4. **Monitor regularmente** as informações de atualização

### 🔍 Filtros Estratégicos
1. **Períodos mensais** para análises de rotina
2. **Filtros por vendedor** para avaliações individuais
3. **Situações específicas** para acompanhamento de pipeline

### 📈 Interpretação de Métricas
1. **Compare** ticket médio entre períodos
2. **Analise** a proporção entrada/parcelado
3. **Identifique** padrões de sazonalidade
4. **Monitore** performance por vendedor

---

**📞 Suporte Técnico**  
Em caso de dúvidas ou problemas técnicos:

- **Marcelo Areco** - Desenvolvedor
  - Email: [ti@oficialsport.com.br ](mailto:ti@oficialsport.com.br)
  
---
*Manual atualizado em: Setembro 2025*  
*Versão: 1.0*
📄 Licença: Oficial Sport©