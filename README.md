# 🖨️ Sistema de Gerenciamento Gemeos-pedido  - Gráfica Gêmeos

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&style=for-the-badge)
![Django](https://img.shields.io/badge/Django-4.x-darkgreen?logo=django&style=for-the-badge)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap&style=for-the-badge)
![HTMX](https://img.shields.io/badge/HTMX-1.9-blue?logo=htmx&style=for-the-badge)

---

## 🧭 1. Visão Geral do Projeto

O **Gemeos-pedido** é uma plataforma web completa para a **Gráfica Gêmeos**, projetada para otimizar o gerenciamento de pedidos e fortalecer a presença online da empresa.

O sistema atua em duas frentes principais:

1. **Portal Institucional (Landing Page):**  
   Página inicial moderna e profissional que apresenta os serviços, portfólio e história da gráfica — com foco em atrair e converter novos clientes.

2. **Sistema de Gerenciamento (Dashboard):**  
   Área autenticada onde clientes podem acompanhar pedidos e a equipe da gráfica pode gerenciar o fluxo de produção.

🎯 **Objetivo:** centralizar a comunicação, agilizar pedidos e reforçar a imagem de profissionalismo e qualidade da marca.

---

## 👥 2. Público-Alvo

### 🧍‍♂️ Persona 1: Cliente
**Quem são:** Pequenos empresários, estudantes ou organizadores de eventos que precisam de serviços gráficos.  
**Necessidades:**
- Visualizar serviços e preços.  
- Solicitar orçamentos e enviar arquivos.  
- Acompanhar o status dos pedidos.  
- Ver histórico de pedidos anteriores.


### 👨‍💼 Persona 2: Administrador (Equipe da Gráfica)
**Quem são:** Gerentes e atendentes da Gráfica Gêmeos.  
**Necessidades:**
- Painel para ver e atualizar pedidos.  
- Controle de status e arquivos dos clientes.  
- Gerenciamento de estoque e catálogo.


---

## ⚙️ 3. Escopo e Funcionalidades

### 🌐 Funcionalidades Públicas
- **Landing Page (`home.html`):**
  - Carrossel de produtos.
  - Seções “Serviços”, “Sobre Nós” e “Portfólio”.
- **Autenticação:**
  - Cadastro, Login e Logout.

### 👤 Funcionalidades do Cliente
- **Dashboard de Pedidos:** lista e status visual de todos os pedidos.  
- **Criação de Pedido:** formulário com upload de arquivos.  
- **Detalhe do Pedido:** visualização detalhada e futuro chat.  
- **Perfil:** edição de informações pessoais.

### 🧰 Funcionalidades do Administrador
- **Dashboard do Gerente:** visão geral de todos os pedidos e métricas.  
- **Gerenciamento de Pedidos:** alterar status e acessar arquivos.  
- **Estoque:** controle de materiais (papel, tinta, etc.).

### 🌍 Funcionalidades Globais
- Design responsivo (mobile-first).  
- Alternador de tema (modo claro/escuro com `localStorage`).  
- Sistema de mensagens e alertas (ex: “Pedido criado com sucesso!”).

---

## 💻 4. Configuração do Ambiente

```bash
# 1. Clone o repositório
git clone https://seu-repositorio-aqui.git
cd nome-do-projeto

# 2. Crie e ative o ambiente virtual
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
# Windows (cmd)
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Aplique as migrações
python manage.py migrate

# 5. Crie um superusuário
python manage.py createsuperuser

# 6. Execute o servidor
python manage.py runserver

## 🗺️ 5. Estrutura e Navegação (Sitemap)

| Caminho | Descrição |
|----------|------------|
| `/` | Landing Page |
| `/login/` | Login |
| `/signup/` | Cadastro |
| `/logout/` | Sair |
| `/pedidos/` | Dashboard do Cliente |
| `/pedidos/novo/` | Novo Pedido |
| `/pedidos/<int:pk>/` | Detalhes do Pedido |
| `/perfil/` | Perfil do Usuário |
| `/gerencia/` | Dashboard do Administrador |
| `/estoque/` | Painel de Estoque |
| `/admin/` | Painel Django nativo |

---

## 🎨 6. Design e Experiência do Usuário (UX)

Baseado no **Bootstrap 5.3**, com uma paleta de cores adaptada à identidade visual da **Gráfica Gêmeos**.

### 🎨 Paleta de Cores

| Uso | Variável CSS | Cor |
|------|---------------|------|
| **Primária** | `--bs-primary` | `#f68117` |
| **Secundária** | `--bs-secondary` | `#0910f4` |
| **Sucesso** | `--bs-success` | `#FFAC68` |
| **Perigo** | `--bs-danger` | `#040752` |
| **Aviso** | `--bs-warning` | `#f59e0b` |
| **Fundo (Dark)** | `--bs-body-bg` | `#0f172a` |

### ✍️ Tipografia

- **Corpo:** System UI, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif.  
- **Títulos:** `.fw-bold` para destaque e legibilidade.

### 🧩 Ícones

Utiliza **Bootstrap Icons v1.11.3** para consistência visual em todo o sistema.

---

## 📦 7. Requisitos de Conteúdo

| Tipo | Descrição |
|------|------------|
| **Textos** | Descrições dos serviços e “Sobre Nós”. |
| **Imagens (Carrossel)** | 3 imagens 1920x700 dos principais produtos. |
| **Imagens (Sobre Nós)** | Foto da equipe ou loja. |

---

## 🚀 8. Tecnologias Principais

| Categoria | Tecnologia |
|------------|-------------|
| **Backend** | Django 4.x |
| **Frontend** | Bootstrap 5.3, HTMX 1.9 |
| **Banco de Dados** | SQLite (dev) / PostgreSQL (produção) |
| **Linguagem** | Python 3.10+ |

---

## 🧱 9. Estrutura de Pastas (Exemplo)

```plaintext
Grafica/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── core/                # Configurações e rotas principais
├── clientes/            # App de usuários/clientes
├── pedidos/             # App de pedidos e gestão
├── estoque/             # App de controle de materiais
│
├── static/              # CSS, JS, Imagens
└── templates/           # Templates HTML (Bootstrap)
