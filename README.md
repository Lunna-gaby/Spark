# ReservaEdu 🎓

Sistema de reservas de equipamentos pedagógicos desenvolvido para facilitar o controle e o empréstimo de equipamentos da escola.

## 🛠️ Tecnologias utilizadas

- Python
- Django
- HTML
- CSS
- JavaScript
- SQLite

## 💻 1. O que precisa instalar?

Antes de executar o sistema, instale:

1. **Python** — baixe em https://www.python.org/downloads/
2. **Git** — baixe em https://git-scm.com/downloads
3. **Visual Studio Code (opcional)** — https://code.visualstudio.com/

Durante a instalação do Python no Windows, marque a opção **Add Python to PATH**.

Para conferir se o Python e o Git foram instalados, abra o PowerShell e execute:

```powershell
python --version
git --version
```

## 📥 2. Baixar o projeto

Abra o PowerShell e execute:

```powershell
git clone https://github.com/Lunna-gaby/Spark.git
cd Spark
```

## 🐍 3. Criar o ambiente virtual

Dentro da pasta do projeto, execute:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação, será necessário ajustar a política de execução ou ativar o ambiente por outro terminal.

## 📦 4. Instalar as dependências

Com o ambiente virtual ativado, instale o Django:

```powershell
python -m pip install django
```

Caso o projeto tenha outras dependências, instale também as dependências listadas no arquivo de configuração do projeto.

## 🗄️ 5. Preparar o banco de dados

Se o arquivo `manage.py` estiver na pasta principal do projeto, execute:

```powershell
python manage.py migrate
```

Para criar um usuário administrador:

```powershell
python manage.py createsuperuser
```

Siga as instruções exibidas no terminal.

## 🚀 6. Executar o sistema

Na pasta principal do projeto, execute:

```powershell
python manage.py runserver 8001
```

Depois, abra o navegador e acesse:

http://127.0.0.1:8001/

Para acessar a tela de login, utilize:

http://127.0.0.1:8001/login/

**Importante:** mantenha o terminal aberto enquanto estiver utilizando o sistema. Para encerrar o servidor, pressione `Ctrl + C`.

## 🔐 7. Acesso ao sistema

As funcionalidades disponíveis dependem do tipo de usuário e das permissões configuradas no sistema.

- **Aluno:** consultar equipamentos e realizar reservas.
- **Direção:** acessar o painel administrativo e gerenciar as solicitações de reserva.

## ⚠️ Observações

- O banco de dados local pode ser diferente do banco utilizado em uma hospedagem.
- Não compartilhe senhas ou credenciais de acesso.
- Para utilizar o sistema em outro computador, configure o ambiente e o banco de dados nesse computador.
- A implantação no Cloudflare ainda precisa ser corrigida e validada.

## 👩‍💻 Projeto

**Nome:** ReservaEdu  
**Objetivo:** facilitar a organização e o controle das reservas de equipamentos pedagógicos da escola.
