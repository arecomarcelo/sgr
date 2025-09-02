# CLAUDE.md

Este arquivo fornece orientações para o Claude Code (claude.ai/code) ao trabalhar com código neste repositório.

## Visão Geral do Projeto

SGR (Sistema de Gestão de Recursos) é uma aplicação de gestão empresarial construída com:
- **Frontend**: Streamlit (framework web Python)
- **Backend**: Django (ORM e configurações)
- **Banco de Dados**: PostgreSQL (hospedado em 195.200.1.244)
- **Arquitetura**: Padrão Service-Repository com estrutura modular

## Estrutura Principal da Aplicação

### Componentes Principais
- `app.py` - Ponto de entrada principal da aplicação Streamlit com roteamento de módulos
- `service.py` - Camada de lógica de negócio (DataService, UserService)
- `repository.py` - Camada de acesso a dados com conexões de banco
- `modules.py` - Sistema de menu de navegação
- `login.py` - Tela de autenticação
- Arquivos de módulos: `vendas.py`, `clientes.py`, `boletos.py`, `extratos.py`, `estoque.py`

### Integração Django
- Django é usado principalmente para modelos ORM e configuração de banco de dados
- Configurações em `app/settings.py` (configuração básica Django com SQLite padrão)
- Autenticação usa sistema auth do Django com hash de senhas

### Configuração do Banco de Dados
A aplicação conecta a um banco PostgreSQL:
```python
DB_CONFIG = {
    'dbname': 'sga',
    'user': 'postgres', 
    'password': 'Zyxelpar100448',
    'host': '195.200.1.244',
    'port': '5432'
}
```

## Comandos Comuns de Desenvolvimento

### Configuração do Ambiente
```bash
# Ativar ambiente virtual (Linux)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Executando a Aplicação
```bash
# Iniciar aplicação Streamlit
streamlit run app.py

# Comandos de gerenciamento Django (se necessário)
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

### Ferramentas de Qualidade de Código (da documentação)
```bash
# Organizar imports
isort .

# Formatar código
blue .

# Verificar estilo
flake8
```

### Gerenciamento de Dependências
```bash
# Atualizar requirements.txt
pip freeze > requirements.txt
```

## Padrões de Arquitetura

### Padrão Service-Repository
- **Camada Repository**: Acesso direto ao banco de dados (`repository.py`)
- **Camada Service**: Lógica de negócio (`service.py`)
- **Camada Presentation**: Módulos Streamlit (vendas, clientes, etc.)

### Estrutura dos Módulos
Cada módulo de negócio segue este padrão:
```python
def main(key="nome_modulo"):
    # Interface Streamlit específica do módulo
    # Usa DataService para operações de dados
```

### Acesso ao Banco de Dados
- Usa tanto SQLAlchemy quanto psycopg2 para diferentes operações
- Classes Repository lidam com operações específicas de entidades
- DataService orquestra interações entre repositories

## Dependências Principais
- `streamlit` - Framework web
- `django` - ORM e autenticação
- `pandas` - Manipulação de dados
- `plotly` - Visualização de dados
- `psycopg2-binary` - Adaptador PostgreSQL
- `sqlalchemy` - Toolkit de banco de dados

## Notas de Desenvolvimento

### Segurança do Banco de Dados
As credenciais do banco estão atualmente hardcoded na camada de serviço. Considere usar variáveis de ambiente para deployments de produção.

### Configuração Streamlit
Configuração de página definida em `app.py` com:
- Título da página: "SGR"
- Layout amplo
- Sidebar expandida

### Fluxo de Autenticação
1. Tela de login valida contra tabela auth_user do Django
2. Permissões do usuário buscadas do sistema auth Django
3. Estado da sessão gerencia status de login

### Navegação entre Módulos
A aplicação principal roteia para diferentes módulos baseado na seleção da sidebar:
- Estoque
- Cobrança
- Financeiro
- Vendas
- Relatório de Clientes

## Diretrizes de Codificação

- **Princípios Fundamentais**:
  01) Sempre revise suas alterações de modo a não alterar ou prejudicar a execução já implementada
  02) Sempre responder em Português do Brasil
  03) Sempre retornar o código completo, jamais abrevie o código
  04) Sempre Listar o nomes dos arquivos alterado
  05) Sempre finalize suas resposta com uma linha em Branco *** FINALIZADO ***
  06) Ao finalizar uma Interação, armazene no arquivo Historico.md (crie se não existir):
    1) Dia (somente na primeira interação do Dia) e a cada nova interação Hora da Tarefa
    2) O que foi pedido
    3) Detalhamento da Solução ou Implementação
    4) Lista de Arquivos Alterados ou Criados
    5) Utilize emojis para tornar clara a compreensão
    6) Utilize UTF-8 e o Fuso Horário Local
 07) **MODELOS**: Os modelos já existem no banco de dados e NÃO devem gerar migrações
 08) **NOVOS MODELOS**: Quando um modelo não existir, será informado como "Novo Modelo" na descrição
