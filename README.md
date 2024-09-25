# Django REST API para empréstimos e pagamentos

Esse é um projeto Django para permitir usuários gerenciarem seus empréstimos e pagamentos. A autenticação no projeto é feita utilizando JWT, e garante que apenas usuários autenticados possam ver os empréstimos e pagamentos, e apenas os seus. Todas as rotas disponíveis na api, entretanto, podem ser vistas pela rota /api/, a única que não requer autenticação.

## Funcionalidades
- Autenticação por JWT
- Empréstimos: criar, listar empréstimos, e verificar informações de um empréstimo (incluindo saldo devedor)
- Pagamentos: criar, listar pagamentos, e verificar informações de um pagamento
- Separação por usuário (um usuário não consegue ver informações de outro, e nem criar pagamentos para empréstimo de outro)
- Teste cobrindo as funcionalidades mencionadas, e também o cálculo correto do saldo devedor
- Scripts de exemplo para utilização da API

## Setup da API

É necessário ter o python 3.10+ por ter compatibilidade com o Django 5.1.1. Também é sugerido a utilização de virtual environments para o projeto.

Clone o projeto utilizando
```bash
git clone https://github.com/lorenzosc/matera.git
cd matera
```

E crie o ambiente com
```bash
python -m venv env
source env/bin/activate  # Para Windows: env\Scripts\activate
```

Instale as dependencias do projeto
```bash
pip install -r requirements.txt
```

Prepare o banco de dados
```bash
cd loan
python manage.py migrate
```

Por fim, para ligar o servidor local
```bash
python manage.py runserver
```

A API estará hosteada em http://localhost:8000/, e suas rotas já poderão ser vistas (inclusive pelo navegador) utilizando http://localhost:8000/api

## API Endpoints

### 1. Autenticação

- **Gere JWT**:  
  `POST /api/token/`

  Request Body:
  ```json
  {
      "username": "seu_usuário",
      "password": "sua_senha"
  }
- **Refresh JWT**:
  `POST /api/token/refresh/`

  Request Body:

    ```json
    {
        "refresh": "sua_token_refresh"
    }
    ```
### 2. Empréstimos
- **Criar empréstimos**:
    `POST /api/loans/`

    Request Body:

    ```json
    {
        "value": "loan_value",
        "interest_rate": "loan_interest_rate",
        "request_date": "2024-05-30T00:00:00Z",
        "ip_address": "192.168.0.1",
        "bank": "Your Bank",
        "client": "Client Name"
    }
    ```
- **Obter detalhes de empréstimo** (incluindo pagamentos e saldo devedor):
    `GET /api/loans/{id}/`

    - O saldo devedor é apresentado como `still_due`

- **Listar Empréstimos do usuário**:
    `GET /api/loans/`

### 3. Pagamentos
- **Criar pagamentos**:
    `POST /api/payments/`

    Request Body:
    ```json
    {
        "date": "2024-09-21T00:00:00Z",
        "value": 500,
        "loan": "loan_id"
    }
    ```
- **Obter Pagamentos**:
    `GET /api/payments/{id}`

- **Listar Pagamentos**:
    `GET /api/payments/`

## Testes da API

Os testes podem ser rodados utilizando
```bash
python manage.py test
```
E dentro deles há testes para verificar
- Se um usuário só consegue ver seus próprios empréstimos
- Se ele consegue ver e criar empréstimos e pagamentos
- Se ele consegue não consegue criar empréstimo para pagamentos de outros usuários
- Se ele não consegue acessar empréstimos de outros usuários
- Se alguém não autenticado não consegue acessar empréstimos
- Se um empréstimo pago no dia apresenta saldo devedor 0
- Se o cálculo do juros está sendo aplicado corretamente

## Exemplos

Para rodar os exemplos, é necessário criar um usuário, e sugere-se a criação com as credenciais já registradas nos scripts de exemplo

Para entrar na shell do Django
```bash
python manage.py shell
```

E então crie o usuário
```python
from django.contrib.auth.models import User
user = User.objects.create_user(username='testuser', password='testpassword')
user.email = 'test@email.com'
user.save()
exit()
```

Após isso, é necessário ligar a API com o comando
```bash
python manage.py runserver
```

E então o script [get_token.py](example/get_token.py) pode ser utilizado para gerar uma access token e um refresh token. Essa refresh token deve ser colocada no arquivo [refresh_token.py](example/refresh_token.py), e então esse script pode ser utilizado para renovar e refazer automaticamente a access token em [access_token.py](example/access_token.py). Uma vez feito isso, os outros 4 scripts podem ser utilizados.

Para criar um pagamento com [insert_payment.py](example/insert_payment.py), é necessário editar o loan_id dentro do arquivo para se referir a um empréstimo existente. O mesmo vale para ver um empréstimo com [view_loan.py](example/view_loan.py). As informações de data podem ser alteradas caso seja de interesse inserir pagamentos e empréstimos com dados diferentes.