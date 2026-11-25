# API de Exoplanetas - Trabalho Final

API desenvolvida em Python com Django REST Framework conectada a um banco MySQL (XAMPP) contendo dados de 5.250 exoplanetas catalogados.

---

# Instalação e execução em desenvolvimento

## Pré-requisitos

Antes de começar, confirme que o computador tem:

| Requisito | Versão | Como conferir |
|---|---|---|
| Python | 3.12 ou mais recente | `python --version` |
| XAMPP (MySQL/MariaDB) | MariaDB 10.11 ou mais recente | Página inicial do phpMyAdmin, em "Servidor de banco de dados" |
| Conexão com a internet | | Necessária para instalar as dependências e para carregar a tela do Swagger |

> Se a versão do MariaDB for mais antiga que a 10.11, veja a seção [Solução de problemas](#solução-de-problemas).

## 1. Banco de dados (MySQL)

1. Abra o **XAMPP Control Panel** e clique em **Start** nos módulos **Apache** e **MySQL** (o Apache é necessário para o phpMyAdmin).
2. No navegador, acesse [http://localhost/phpmyadmin](http://localhost/phpmyadmin).
3. Clique na aba **Importar**.
4. Em **Arquivo a importar**, selecione o arquivo [database/db_exoplanetas.sql](./database/db_exoplanetas.sql).
5. Clique em **Importar** (ou **Executar**) no final da página.

O script cria o banco `db_exoplanetas` e a tabela `planetas` com os 5.250 registros. Não é preciso criar o banco antes, o próprio script faz isso.

A API se conecta ao banco com o usuário padrão do XAMPP (`root`, sem senha). Esses dados ficam em `setup/settings.py`, na seção `DATABASES`.

> O script começa apagando a tabela `planetas` se ela já existir. Ou seja, importar de novo restaura a base original.

## 2. Criação do ambiente virtual (Windows)

Abra o **PowerShell** na pasta do projeto (`final-ds-APIs`) e rode os comandos abaixo, um de cada vez:

```powershell
# 1. Cria o ambiente virtual (apenas na primeira vez)
python -m venv venv

# 2. Libera a execução de scripts no PowerShell (apenas na primeira vez)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 3. Ativa o ambiente virtual
.\venv\Scripts\Activate.ps1

# 4. Instala as dependências do projeto
pip install -r requirements.txt

# 5. Cria as tabelas internas do Django (admin, autenticação e sessões)
python manage.py migrate
```

Quando o ambiente virtual está ativo, aparece `(venv)` no começo da linha do PowerShell.

> A tabela `planetas` é criada pelo arquivo `.sql` (o model usa `managed = False`), por isso o `migrate` não cria nem altera essa tabela.

**Dependências instaladas pelo `requirements.txt`:**
- `Django`: framework web
- `djangorestframework`: criação da API REST
- `mysqlclient`: conexão com o MySQL/MariaDB
- `drf-spectacular`: documentação Swagger

## 3. Executar a aplicação

Ainda na mesma janela do PowerShell, com o `(venv)` ativo:

```powershell
python manage.py runserver
```

O servidor fica rodando enquanto a janela estiver aberta. Para parar, use `Ctrl + C`.

Se fechar a janela, abra o PowerShell de novo na pasta do projeto e rode os dois comandos abaixo para subir a aplicação novamente:

```powershell
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

## 4. Consultando a API

Com o servidor rodando, acesse pelo navegador:

- **API:** [http://127.0.0.1:8000/api/planetas/](http://127.0.0.1:8000/api/planetas/)
- **Documentação Swagger** (lista todos os endpoints e permite testá-los pelo botão "Try it out"): [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **Admin do Django:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) (exige criar um usuário com `python manage.py createsuperuser`)

---

## Endpoints Disponíveis (10 Endpoints)

### CRUD Padrão e Detalhe (5 Endpoints)
- `GET /api/planetas/` - Lista todos os planetas (com paginação, 20 por página; use `?page=2` para navegar).
- `POST /api/planetas/` - Cadastra um novo planeta.
- `GET /api/planetas/<id>/` - Exibe detalhes de um planeta específico.
- `PUT / PATCH /api/planetas/<id>/` - Atualiza um planeta.
- `DELETE /api/planetas/<id>/` - Remove um planeta.

### Endpoints Personalizados (5 Endpoints)
- `GET /api/planetas/por-tipo/?tipo=<Gigante Gasoso>` - Filtra por tipo de planeta (paginado).
- `GET /api/planetas/mais-proximos/` - Retorna os 20 planetas mais próximos da Terra, ordenados por menor distância.
- `GET /api/planetas/por-metodo/?metodo=<Transito>` - Filtra pelo método científico de descoberta (paginado).
- `GET /api/planetas/recentes/?ano=<2015>` - Filtra planetas descobertos a partir de um ano (paginado).
- `GET /api/planetas/estatisticas/` - Retorna um resumo analítico da base: total de planetas, distância média, anos da descoberta mais antiga e mais recente, e totais por tipo e por método.

Os endpoints com parâmetro obrigatório retornam **400** com uma mensagem de erro quando o parâmetro não é informado ou é inválido (ex: `?ano=abc`).

### Exemplos para testar no navegador
- [http://127.0.0.1:8000/api/planetas/por-tipo/?tipo=Terrestre](http://127.0.0.1:8000/api/planetas/por-tipo/?tipo=Terrestre)
- [http://127.0.0.1:8000/api/planetas/mais-proximos/](http://127.0.0.1:8000/api/planetas/mais-proximos/)
- [http://127.0.0.1:8000/api/planetas/por-metodo/?metodo=Transito](http://127.0.0.1:8000/api/planetas/por-metodo/?metodo=Transito)
- [http://127.0.0.1:8000/api/planetas/recentes/?ano=2015](http://127.0.0.1:8000/api/planetas/recentes/?ano=2015)
- [http://127.0.0.1:8000/api/planetas/estatisticas/](http://127.0.0.1:8000/api/planetas/estatisticas/)

---

## Parâmetros para Testes

### Tipos de Planeta válidos:
- `Gigante Gasoso`
- `Super-Terra`
- `Tipo Netuno`
- `Terrestre`
- `Desconhecido`

### Métodos de Descoberta válidos (exemplos):
- `Velocidade Radial`
- `Transito`
- `Imagem Direta`
- `Astrometria`
- `Microlentes Gravitacionais`

---

## Solução de problemas

**`Activate.ps1 não pode ser carregado porque a execução de scripts foi desabilitada`**
Rode `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` e tente ativar o ambiente de novo. Outra opção é usar o Prompt de Comando (cmd) e ativar com `venv\Scripts\activate`.

**`MariaDB 10.11 or later is required (found 10.x.x)`**
O Django 6.1 exige o MariaDB 10.11 ou mais recente, e algumas versões do XAMPP trazem um MariaDB mais antigo. Para resolver, atualize o MariaDB do XAMPP para a versão 10.11 ou mais recente (ou instale uma versão mais nova do XAMPP) e importe o `database/db_exoplanetas.sql` novamente.

**`Can't connect to MySQL server on '127.0.0.1'`**
O MySQL não está rodando. Abra o XAMPP Control Panel e clique em **Start** no módulo **MySQL**.

**`Unknown database 'db_exoplanetas'`**
O banco ainda não foi importado. Siga o passo [1. Banco de dados (MySQL)](#1-banco-de-dados-mysql).

**Erro ao instalar o `mysqlclient`**
Confira se o Python é 3.12 ou mais recente e atualize o pip com `python -m pip install --upgrade pip` antes de rodar o `pip install -r requirements.txt` de novo.

**A página do Swagger (`/api/docs/`) abre em branco**
A tela do Swagger carrega os arquivos de estilo pela internet. Confira a conexão. A API continua funcionando normalmente em `/api/planetas/`.
