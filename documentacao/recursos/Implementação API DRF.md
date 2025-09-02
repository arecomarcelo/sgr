# 🚀 Guia de Implementação - API Modelo

Guia passo a passo para implementação da API de gestão de clientes usando Django REST Framework.

## 📑 Índice

1. [Configuração do Ambiente](#-configuracao-do-ambiente)
2. [Criação do Projeto](#-criação-do-projeto)
3. [Estrutura de Pastas](#-estrutura-de-pastas)
4. [Configurações Iniciais](#-configurações-iniciais)
5. [Implementação dos Componentes](#-implementação-dos-componentes)
6. [Configuração da Autenticação](#-configuração-da-autenticação)
7. [Documentação da API](#-documentação-da-api)
8. [Testes](#-testes)
9. [Notas Importantes](#-notas-importantes)

## 🔮 Configuração do Ambiente

### Criar e ativar ambiente virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar no Linux/Mac
source venv/bin/activate

# Ativar no Windows
.\venv\Scripts\activate
```

### Instalar Dependências

```bash
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-filter
pip install django-rql
pip install drf-spectacular
pip install psycopg2-binary

# Gerar requirements.txt
pip freeze > requirements.txt
```

## 🎯 Criação do Projeto

Criar projeto Django

```bash
django-admin startproject app
mv app api_modelo  # Linux/Mac
# ou
ren app api_modelo  # Windows
cd api_modelo
```

## 📂 Estrutura de Pastas

### Criar Pastas

Na raiz do projeto (api_nome)

```bash
mkdir -p app/domain/models
mkdir -p app/domain/repositories
mkdir -p app/domain/services
mkdir -p app/infrastructure/persistence
mkdir -p app/infrastructure/auth
mkdir -p app/infrastructure/docs
mkdir -p app/presentation/api/v1
mkdir -p app/presentation/serializers
mkdir -p app/presentation/viewsets
mkdir -p app/presentation/pagination
```

### Criar Arquivos __init__.py

#### Linux

```bash
touch app/domain/models/__init__.py
touch app/domain/repositories/__init__.py
touch app/domain/services/__init__.py
touch app/infrastructure/auth/__init__.py
touch app/infrastructure/docs/__init__.py
touch app/infrastructure/persistence/__init__.py
touch app/presentation/api/v1/__init__.py
touch app/presentation/serializers/__init__.py
touch app/presentation/viewsets/__init__.py
touch app/presentation/pagination/__init__.py
```

#### Windows

```bash
type nul > app/domain/models/__init__.py
type nul > app/domain/repositories/__init__.py
type nul > app/domain/services/__init__.py
type nul > app/infrastructure/auth/__init__.py
type nul > app/infrastructure/docs/__init__.py
type nul > app/infrastructure/persistence/__init__.py
type nul > app/presentation/api/v1/__init__.py
type nul > app/presentation/serializers/__init__.py
type nul > app/presentation/viewsets/__init__.py
type nul > app/presentation/pagination/__init__.py
```

### Estrutura das Pastas e Arquivos Criados

```bash
api_modelo/
├── app/
│   ├── domain/
│   │   ├── models/
│   │   │   └── __init__.py
│   │   ├── repositories/
│   │   │   └── __init__.py
│   │   └── services/
│   │       └── __init__.py
│   ├── infrastructure/
│   │   ├── auth/
│   │   │   └── __init__.py
│   │   ├── docs/
│   │   │   └── __init__.py
│   │   └── persistence/
│   │       └── __init__.py
│   └── presentation/
│       ├── api/
│       │   └── v1/
│       │       └── __init__.py
│       ├── serializers/
│       │   └── __init__.py
│       ├── viewsets/
│       │   └── __init__.py
│       └── pagination/
│           └── __init__.py
├── manage.py
└── requirements.txt
```

### Verificação da Estrutura Criada

```bash
# No Linux/Mac
tree

# No Windows (se tiver tree instalado)
tree /F
```

Esta estrutura segue o ***Padrão de Arquitetura em Camadas***:

- ***Domain***: Regras de Negócio e Modelos
- ***Infrastructure***: Configurações e Implementações Técnicas
- ***Presentation***: Interface com o Usuário (API)

## ⚙️ Configurações Iniciais

### Configurar settings.py

```python
# app/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'rest_framework_simplejwt',
    # Local apps
    'app',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sga',
        'USER': 'postgres',
        'PASSWORD': 'sua-senha',
        'HOST': '195.200.1.244',
        'PORT': '5432',
    }
}

# DRF Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'app.presentation.pagination.custom_pagination.CustomPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}
```

# 🛠️ Implementação dos ComponentesCriar Custom Pagination

```python
# app/presentation/pagination/custom_pagination.py

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'code': 200,
            'status': 'success',
            'meta': {
                'total_registros': self.page.paginator.count,
                'total_paginas': self.page.paginator.num_pages,
                'total_registros_pagina': len(data),
                'pagina_atual': self.page.number,
                'limite_por_pagina': self.page_size,
                'pagina_anterior': self.page.previous_page_number() if self.page.has_previous() else None,
                'url_anterior': self.get_previous_link(),
                'proxima_pagina': self.page.next_page_number() if self.page.has_next() else None,
                'proxima_url': self.get_next_link(),
            },
            'data': data
        })
```

2. Implementar Base Repository

```python
# app/domain/repositories/base.py

from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """Interface base para todos os repositories"""
  
    def get_all(self) -> List[T]:
        raise NotImplementedError
  
    def get_by_id(self, id: int) -> Optional[T]:
        raise NotImplementedError
  
    def get_by_pessoa_tipo_id(self, pessoa_tipo_id: int) -> List[T]:
        raise NotImplementedError
```

3. Implementar Repositories

```python
# Implementar em arquivos separados:
# - app/domain/repositories/cliente_repository.py

# - app/domain/repositories/telefone_repository.py
# - app/domain/repositories/endereco_repository.py
```

4. Implementar Serializers

```python
# Implementar em arquivos separados:
# - app/presentation/serializers/cliente_serializer.py
# - app/presentation/serializers/telefone_serializer.py
# - app/presentation/serializers/endereco_serializer.py
```

5. Implementar ViewSets

```python
# Implementar em arquivos separados:
# - app/presentation/viewsets/cliente_viewset.py
# - app/presentation/viewsets/telefone_viewset.py
# - app/presentation/viewsets/endereco_viewset.py
```

# 🔐 Configuração da Autenticação

Configurar JWT

```python
# app/infrastructure/auth/jwt_config.py

from datetime import timedelta

JWT_SETTINGS = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': None,  # Será substituída pela SECRET_KEY
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

# 📚 Documentação da API

Configurar Swagger/Spectacular

```python
# app/infrastructure/docs/swagger_config.py

SPECTACULAR_SETTINGS = {
    'TITLE': 'API Modelo',
    'DESCRIPTION': '''
    # API Modelo

    ## Paginação
    Por padrão, todos os endpoints que retornam listas são paginados.
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
}
```

Configurar URLs

```python
# app/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# ... configuração das rotas ...

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

# ✅ Testes

1. Executar migrações

```bash
python manage.py migrate
```

2. Criar superusuário

```bash
python manage.py createsuperuser
```

3. Iniciar servidor

```bash
python manage.py runserver
```

4. Testar Autenticação

```bash
# Obter token
curl -X POST http://localhost:8000/api/token/ \
    -H "Content-Type: application/json" \
    -d '{"username": "seu_usuario", "password": "sua_senha"}'

# Testar endpoint com token
curl http://localhost:8000/api/v1/clientes/ \
    -H "Authorization: Bearer seu_token_aqui"
```

5. Acessar Documentação
   Swagger UI: ``http://localhost:8000/api/swagger/``
   ReDoc: ``http://localhost:8000/api/redoc/``

# 📝 Notas Importantes

1. Paginação
   - Padrão: /api/v1/clientes/
   - Sem paginação: /api/v1/clientes/?paginate=false
   - Parâmetros: page, page_size
2. Autenticação
   - Todos os endpoints requerem autenticação JWT
   - Token válido por 60 minutos
   - Refresh token válido por 24 horas
3. Filtros
   - Disponíveis em todos os endpoints
   - Exemplo: /api/v1/clientes/?Nome=João
