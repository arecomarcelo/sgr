
# 🐍💻 **Comandos de Desenvolvimento Python & Django**

---

## 🧪 **Ambiente Virtual (venv)**

### 🪟 Windows
- 📦 **Criar:** 
```bash
python -m venv venv
```

- ✅ **Ativar:** 
```bash
.venv\Scripts\activate
```

- ❎ **Desativar:** 
```bash
deactivate
```

- 🔄 **Atualizar pip:**
```bash
python.exe -m pip install --upgrade pip
```

### 🐧 Linux
```bash
sudo apt update
python3 -m venv venv
```

- ✅ **Ativar:**
```bash
source venv/bin/activate
```

- ❎ **Desativar:**
```bash
deactivate
```

- 🔄 **Atualizar pip:**
```bash
pip install --upgrade pip
```

---

## 📦 **Requirements (Dependências)**

- 🔄 **Atualizar dependências:**
```bash
pip freeze
```

- 📄 **Gerar arquivo de dependências:**
```bash
pip freeze > requirements.txt
```

- ⬇️ **Instalar dependências:**
```bash
pip install -r requirements.txt
```

- 📋 **Listar dependências instaladas:**
```bash
pip list
```

---

## 🌐 **Comandos Django**

### 🪟 Windows
- 📥 **Instalar Django:**
```bash
pip install django

```

- 🚧 **Iniciar projeto:**
```bash
django-admin startproject app .
```

- 🧩 **Criar app:**
```bash
python manage.py startapp nome_app
```

- 👤 **Criar superusuário:**
```bash
python manage.py createsuperuser
```

- 🛠️ **Criar migrações:**
```bash
python manage.py makemigrations
```

- 🧱 **Aplicar migrações:**
```bash
python manage.py migrate
```

- 🕵️ **Listar migrações:**
```bash
python manage.py showmigrations
```

### 🐧 Linux
- 📥 **Instalar Django:**
```bash
pip install django
```

- 🚧 **Iniciar projeto:**
```bash
django-admin startproject app .
```

- 🧩 **Criar app:**
```bash
python3 manage.py startapp nome_app
```

- 👤 **Criar superusuário:**
```bash
python3 manage.py createsuperuser
```

- 🛠️ **Criar migrações:**
```bash
python3 manage.py makemigrations
```

- 🧱 **Aplicar migrações:**
```bash
python3 manage.py migrate
```

- 🕵️ **Listar migrações:**
```bash
python3 manage.py showmigrations
```
---

## ▶️ **Rodar Servidor:**

##### 🪟 Windows
```bash
python manage.py runserver
```

##### 🐧 Linux
```bash
python3 manage.py runserver
```

##### 🚀 Streamlit
```bash
streamlit run app.py
```
---
## 🌳 **GIT**

- 🙍‍♂️ **Configurar nome de usuário:**  
  ```bash
  git config --global user.name "arecomarcelo"
  ```

- 📧 **Configurar e-mail:**  
  ```bash
  git config --global user.email "marcelo.areco@hotmail.com"
  ```
---

## 🚀 **Deploy da Aplicação**

### 💻 Local
- 📄 Atualizar requirements.txt
```bash
pip freeze > requirements.txt
```

- 🔄 Organizer imports *isort*:
```bash
isort .
```

- 🎨 Organizar Código *blue*:
```bash
blue .
```
- 📏 Verificar *flake8*:
```bash
flake8
```

- 💾 Fazer commit das alterações

### 🌍 VPS
- 🔐 Acessar via SSH:
```bash
ssh root@195.200.1.244
```

- 📁 Entrar no diretório:
```bash
cd /var/www/sga/
```

- ⛔ Parar servidor NGINX:
```bash
sudo systemctl stop nginx
```

- 🔍 Verificar status:
```bash
sudo systemctl status nginx
```

- 🔓 Desmascarar NGINX:
```bash
sudo systemctl unmask nginx
```

- 🔄 Reiniciar NGINX:
```bash
sudo /etc/init.d/nginx restart
```

- ⬇️ Atualizar app via GIT:
```bash
git pull
```

- ✅ Ativar venv:
```bash
source venv/bin/activate
```

- 📦 Instalar dependências:
```bash
pip install -r requirements.txt
```
---

# 👥 Autor

- **Marcelo Areco** - Desenvolvedor
  - Email: [marcelo.areco.ti@gmail.com ](mailto:marcelo.areco.ti@gmail.com)
  - GitHub: [@arecomarcelo](https://github.com/arecomarcelo)

📄 Licença: HauxTech©