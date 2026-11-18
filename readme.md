# API de Exoplanetas - Trabalho Final

API desenvolvida em Python com Django REST Framework conectada a um banco MySQL (XAMPP) contendo dados de exoplanetas catalogados.

## Como Executar
1. Certifique-se de que o MySQL e o Apache estão rodando no XAMPP.
2. Ative o ambiente virtual: `venv\Scripts\activate`
3. Inicie o servidor: `python manage.py runserver`
4. Acesse em: `http://127.0.0.1:8000/api/planetas/`

---

## Endpoints Disponíveis (10 Endpoints)

### CRUD Padrão e Detalhe (5 Endpoints)
- `GET /api/planetas/` — Lista todos os planetas (com paginação).
- `POST /api/planetas/` — Cadastra um novo planeta.
- `GET /api/planetas/<id>/` — Exibe detalhes de um planeta específico.
- `PUT / PATCH /api/planetas/<id>/` — Atualiza um planeta.
- `DELETE /api/planetas/<id>/` — Remove um planeta.

### Endpoints Personalizados (5 Endpoints)
- `GET /api/planetas/por-tipo/?tipo=<Gigante Gasoso>` — Filtra por tipo de planeta.
- `GET /api/planetas/mais-proximos/` — Retorna os planetas ordenados por menor distância da Terra.
- `GET /api/planetas/por-metodo/?metodo=<Transito>` — Filtra pelo método científico de descoberta.
- `GET /api/planetas/recentes/?ano=<2015>` — Filtra planetas descobertos a partir de um ano.
- `GET /api/planetas/estatisticas/` — Retorna um resumo analítico da base.

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