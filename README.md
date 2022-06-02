# Projeto Shark Tank

É uma plataforma de investimentos, onde o empreendedor expõe seu plano de negócios com objetivo de encontrar investidores.

O empreendedor poderá cadastrar suas idéias e acessá-las a qualquer momento, mas só poderá deixar uma delas elegíveis a receber investimento.

O investidor poderá visualizar as idéias abertas para receber investimento e injetar parte ou todo o valor indicado para o desenvolvimento do projeto, que será concluído quando atingir 100% do valor recebido e liberará ao empreendedor eleger outra ideia para captar investimentos.

## Lista de endpoints:

- **users**:
    
    
    | CHAVES | VALORES | OBRIGATORIEDADE | ROTAS |
    | --- | --- | --- | --- |
    | name | string, max(255) | X | POST, PATCH |
    | email | string, email, max(255) | X | POST, PATCH |
    | password | string, max(255) | X | POST, PATCH |
    | phone | string, max(14), unique | X | POST, PATCH |
    | is_inv | boolean, default=False |  | POST, PATCH |
    | is_superuser | boolean, default=False |  | POST, PATCH |
    - create - POST - /api/users/
        
        rota não autenticada
        
        Serão criadas contas tipo investidor (is_inv=true) ou empreendedor (is_inv=false)
        
        Requisição correta → Insere novo usuário no DB  
        
        ```json
        {
        	"name": "Pedro Silva",
        	"email": "psilva@email.com",
        	"password": "123456",
          "phone": "(11)98585-5858",
          "is_inv" : false
        }
        ```
        
        ```json
        **RESPONSE 201 - CREATED**
        
        {
        	"name": "Pedro Silva",
        	"email": "psilva@email.com",
          "phone": "(11)98585-5858",
          "is_inv" : false
        }
        ```
        
        Requisição incorreta → faltando um mais campos obrigatórios:
        
        ```python
        **RESPONSE 400 - BAD REQUEST**
        
        {
          "name": [
            "This field is required."
          ],
          "email": [
            "This field is required."
          ],
          "password": [
            "This field is required."
          ]
        }
        ```
        
        Requisição incorreta → email fora do formato padrão:
        
        ```python
        **RESPONSE 400 - BAD REQUEST**
        
        {
          "email": [
            "Enter a valid email address."
          ]
        }
        ```
        
        Requisição incorreta → Email já existente
        
        ```json
        **RESPONSE 422 - Unprocessable Entity**
        
        { "error": "email has already been used" }
        ```
        
        Requisição incorreta →quando o tipo de dado não é válido
        
        ```json
        {
        	"name": ["Pedro Silva"],
        	"email": "psilva@email.com",
        	"password": "123456",
          "phone": "(11)98585-5858",
          "is_inv" : false
        }
        ```
        
        ```json
        **RESPONSE 400 - Bad Request**
        {
          "name": [
            "Not a valid string."
          ]
        }
        ```
        
    - read all - GET - /api/users/
        
        rota autenticada com token
        
        Permite uso de paginação
        
        /api/users/?page=1&per_page=20/
        
        O usuário, se não for admin, só poderá ver sua própria conta.
        
        Não tem Json de envio.
        
        Retorna:
        
        ```json
        **RESPONSE 200 - OK**
        [
          {
            "user_id": "1",
            "name": "Pedro Silva",
            "email": "psilva@email.com",
            "phone": "(11)985855858",
            "is_inv" : false
          },
          {
            "user_id": "2",
            "name": "Maria Silva",
            "email": "msilva@email.com",
            "phone": "(11)974744747",
            "is_inv" : true
          },
        ]
        ```
        
    - read one - GET - /api/users/:id/
        
        rota autenticada com token
        
        Não tem Json de envio.
        
        O usuário, se não for admin, só poderá ver sua própria conta.
        
        Requisição correta:
        
        ```json
        **RESPONSE 200 - OK**
        {
          "user_id": "1",
          "name": "Pedro Silva",
          "email": "psilva@email.com",
          "phone": "(11)985855858",
          "is_inv" : false
        }
        ```
        
        Requisição correta → mas não está logado
        
        ```json
        **RESPONSE 401 - Unauthorized**
        
        {
          "detail": "Authentication credentials were not provided."
        }
        ```
        
        Requisição correta →  id não pertence ao usuário e a requisição não veio de um admin
        
        ```json
        **RESPONSE 401 - Unauthorized**
        
        {
          "detail": "Authentication credentials allow access."
        }
        ```
        
        Requisição correta → id não existe
        
        ```json
        **RESPONSE 404 - Not Found**
        
        {
          "message": "User does not exist"
        }
        ```
        
    - update - PATCH - /api/users/:id/
        
        rota autenticada com token
        
        O usuário, se não for admin, só poderá alterar sua própria conta
        
        Json de envio
        
        ```json
        {
        	"name": "Pedro José Silva",
        	"email": "psilva@email.com",
        	"password": "123456",
          "phone": "(11)985855858",
          "is_inv": false
        }
        ```
        
        Requisição correta
        
        ```json
        **RESPONSE 200 - Ok**
        
        {
        	"name": "Pedro Silva Mendes",
          "phone": "(11)98585-5888",
          "is_inv": true
        }
        ```
        
        Requisição correta → id não existe
        
        ```json
        **RESPONSE 404 - Not Found**
        
        {
          "message": "User does not exist"
        }
        ```
        
        Requisição correta → id não pertence ao usuário e a requisição não veio de um admin
        
        ```json
        **RESPONSE 422 - Unprocessable Entity**
        
        {
        	"message": "Unauthorized change another user"
        }
        ```
        
        Requisição correta → Email já existente
        
        ```json
        **RESPONSE 422 - Unprocessable Entity**
        
        { "message": "email has already been used" }
        ```
        
        Requisição correta → tentou alterar ‘is_inv’ mas não é um admin
        
        ```json
        **RESPONSE 422 - Unprocessable Entity**
        
        {
        	"message": "changing its type is not allowed, look for an administrator"
        }
        ```
        
        Requisição incorreta →quando o tipo de dado não é válido
        
        ```json
        {
        	"name": ["Pedro Silva"],
        	"email": "psilva@email.com",
        	"password": "123456",
          "phone": "(11)98585-5858",
          "is_inv" : false
        }
        ```
        
        ```json
        **RESPONSE 400 - Bad Request**
        {
          "name": [
            "Not a valid string."
          ]
        }
        ```
        
    - delete - DELETE - /api/users/:id/
        
        rota autenticada com token
        
        Requisição correta → tentou excluir sua própria conta, ou sendo admin a conta de outro user
        
        ```json
        **RESPONSE 200 - Ok**
        
        {}
        ```
        
        Requisição correta → tentou excluir outro user mas não é um admin
        
        ```json
        **RESPONSE 422 - Unprocessable Entity**
        
        {
        	"message": "Unauthorized delete another user"
        }
        ```
        
        Requisição correta → id não existe
        
        ```json
        **RESPONSE 404 - Not Found**
        
        {
          "message": "User does not exist"
        }
        ```
        
        ```json
        {}
        ```
        
    
- **login**:
    - Login  POST - /api/login/
        
        
        | CHAVES | VALORES | OBRIGATORIEDADE |
        | --- | --- | --- |
        | email | string, email, max(255) | X |
        | password | string, max(255) | X |
        
        Requisição correta:
        
        ```json
        {
        	"email": "psilva@email.com",
        	"password": "123456"
        }
        ```
        
        Retorno → Gera um token de acesso:
        
        ```json
        **RESPONSE 200 - OK**
        
        {
        	"token": "3c68840fc0b20dfa350804b689c1fedfeea438ff"
        }
        ```
        
        Requisição incorreta → e-mail/senha não registrados:
        
        ```json
        **RESPONSE 401 - UNAUTHORIZED**
        
        {
        	"message": "Invalid password or e-mail address"
        }
        ```
        
        Requisição incorreta → e-mail e senha não compatíveis:
        
        ```json
        **RESPONSE 401 - UNAUTHORIZED**
        
        {
        	"message": "Invalid password or e-mail address"
        }
        ```
        
        Requisição incorreta → requisição com valores diferente de string:
        
        ```json
        {
        	"email": ["psilva@email.com"],
        	"password": "123456"
        }
        ```
        
        Retorno → retorna nome da chave errada e informa valor correto:
        
        ```json
        RESPONSE 400 - BAD REQUEST
        
        {
        	"email": [
        		"Not a valid string."
        	]
        }
        ```
        
        Requisição incorreta → requisição com campo em branco:
        
        ```json
        {
        	"email": "psilva@email.com",
        	"password": ""
        }
        ```
        
        Retorno → retorna nome da chave errada e informa que está em branco:
        
        ```json
        RESPONSE 400 - BAD REQUEST
        
        {
        	"password": [
        		"This field may not be blank."
        	]
        }
        ```
        
        Requisição incorreta → Faltando uma ou mais chaves 
        
        ```json
        {
        	"email": "psilva@email.com"
        }
        ```
        
        Retorno → retorna nome da chave e mensagem informando que é obrigatória:
        
        ```json
        RESPONSE 400 - BAD REQUEST
        
        {
        	"password": [
        		"This field is required."
        	]
        }
        ```
        
- **ideas**:
    
    
    | CHAVES | VALORES | OBRIGATORIEDADE | ROTAS |
    | --- | --- | --- | --- |
    | name | string, max(255) | X | POST, PATCH |
    | value | integer | X | POST, PATCH |
    | value | integer | X | POST, PATCH |
    | is_activated | boolean, default=true |  | PATCH |
    
    - create - POST - /api/idea/
        
        rota autenticada com token
        
        Apenas empreendedor poderá criar uma ideia para investimentos
        
        Json de envio
        
        ```json
        {
        	"name":"mecânica",
        	"description":"mecânica de carros em geral, ..."
        	"value":15000
        }
        ```
        
        Resposta requisição correta
        
        ```json
        **RESPONSE 201 - CREATED**
        
        {
        	"id": "7233c63b-2e65-4e51-9f34-07b8de4c6668"
        	"name":"mecânica",
        	"description":"mecânica de carros em geral, ..."
        	"value":15000,
        	"amount_collected": 0,
        	"is_active": true,
        	"finished": false,
        	"created_at": "23/05/2022",
        	"deadline": "23/10/2022",
        	"user": {
        		"name": "Evan",
        		"email": "ent1@mail.com"
        	},
        	"is_deleted":false
        }
        ```
        
        Requisição faltando campo obrigatório
        
        ```json
        **RESPONSE 400 - BAD REQUEST**
        
        {
          "name": [
            "This field is required."
          ],
          "description": [
            "This field is required."
          ],
          "value": [
            "This field is required."
          ]
        }
        ```
        
        Requisição caso usuário já tenha uma ideia ativa
        
        ```json
        **RESPONSE 201 - CREATED**
        
        {
        	"id": "fc5a80ec-56bc-4d04-8af8-8445edb6d2d5"
        	"name":"mecânica",
        	"description":"mecânica de carros em geral, ..."
        	"value":15000,
        	"amount_collected": 0,
        	"is_active": false,
        	"finished": false,
        	"created_at": "23/05/2022",
        	"deadline": "23/08/2022",
        	"user_id": {
        		"name": "Evan",
        		"email": "ent1@mail.com"
        	},
        	"id_deleted":false
        }
        ```
        
    - read all - GET -/api/ideas/ (INVESTOR)
        
        rota autenticada com token
        
        Apenas investidores poderão visualizar todas as ideias ativas, disponíveis para investimento
        
        ```json
        **RESPONSE 200 - OK**
        
        [
        	{
        		"id": "999bb5f3-a80e-4e78-8764-64ca948071f5",
        		"name": "mecânica",
        		"description": "mecânica de carros em geral, experiência de 30 anos no mercado como empregado, procuro oportunidade para abrir meu próprio negócio",
        		"value": 15000,
        		"amount_collected": 15000,
        		"finished": true,
        		"is_activated": true,
        		"created_at": "20/05/2022",
        		"deadline": "18/08/2022",
        		"user": {
        			"name": "ent",
        			"email": "ent1@mail.com"
        		},
        		"id_deleted":false
        	},
        	{
        		"id": "d75292df-db7f-48cb-9178-a5373a19c809",
        		"name": "padaria",
        		"description": "Padaria locaizada em bairro nobre da cidade, ótimo potencial de clientela, concorrência mais próxima a 10km",
        		"value": 15550,
        		"amount_collected": 15550,
        		"finished": true,
        		"is_activated": true,
        		"created_at": "20/05/2022",
        		"deadline": "18/08/2022",
        		"user": {
        			"name": "ent2",
        			"email": "ent2@mail.com"
        		},
        		"id_deleted":false
        	}
        ]
        ```
        
    - read all - GET -/api/ideas/ (ADMINISTRADOR)
        
        rota autenticada com token
        
        Administradores poderáo visualizar todas as ideis ativas/inativas/deletadas
        
        ```json
        **RESPONSE 200 - OK**
        
        [
        	{
        		"id": "999bb5f3-a80e-4e78-8764-64ca948071f5",
        		"name": "mecânica",
        		"description": "mecânica de carros em geral, experiência de 30 anos no mercado como empregado, procuro oportunidade para abrir meu próprio negócio",
        		"value": 15000,
        		"amount_collected": 15000,
        		"finished": true,
        		"is_activated": false,
        		"created_at": "20/05/2022",
        		"deadline": "18/08/2022",
        		"user": {
        			"name": "ent",
        			"email": "ent1@mail.com"
        		},
        		"id_deleted":true
        	},
        	{
        		"id": "d75292df-db7f-48cb-9178-a5373a19c809",
        		"name": "padaria",
        		"description": "Padaria locaizada em bairro nobre da cidade, ótimo potencial de clientela, concorrência mais próxima a 10km",
        		"value": 15550,
        		"amount_collected": 15550,
        		"finished": true,
        		"is_activated": true,
        		"created_at": "20/05/2022",
        		"deadline": "18/08/2022",
        		"user": {
        			"name": "ent2",
        			"email": "ent2@mail.com"
        		},
        		"id_deleted":false
        	}
        ]
        ```
        
    - read one - GET -/api/idea/:id/ (INVESTOR)
        
        rota autenticada com token
        
        Apenas investidores poderão visualizar por id as ideias ativas disponíveis para investimento
        
        ROTA
        
        URL/api/idea/7233c63b-2e65-4e51-9f34-07b8de4c6668/
        
        ```json
        **RESPONSE 200 - OK**
        {
        	"id": "7233c63b-2e65-4e51-9f34-07b8de4c6668",
        	"name": "padaria",
        	"description": "Padaria locaizada em bairro nobre da cidade, ótimo potencial de clientela, concorrência mais próxima a 10km",
        	"value": 15550,
        	"amount_collected": 0,
        	"finished": false,
        	"is_activated": true,
        	"created_at": "20/05/2022",
        	"deadline": "24/05/2022",
        	"user": {
        		"name": "ent2",
        		"email": "ent2@mail.com"
        	},
        	"id_deleted":false
        }
        ```
        
    - read all - GET -/api/ideas/owner/ (ENTREPRENEUR)
        
        rota autenticada com token
        
        empresário poderá visualizar suas ideias
        
        ROTA
        
        URL/api/ideas/
        
        ```json
        **RESPONSE 200 - OK**
        [
        	{
        		"id": "01338794-6f58-4079-8108-37685cf72ffa",
        		"name": "mecânica do Evan",
        		"description": "mecânica de carros em geral, profissional com experiência de 30 anos no mercado como empregado, procuro oportunidade para abrir meu próprio negócio",
        		"value": 15000,
        		"amount_collected": 0,
        		"finished": false,
        		"created_at": "30/05/2022",
        		"deadline": "31/05/2022",
        		"is_activated": true,
        		"user": {
        			"name": "Evan",
        			"email": "ent1@mail.com"
        		},
        		"id_deleted":false
        	},
        	{
        		"id": "cb973a01-0d5f-4e19-b64d-9e0625cba5a6",
        		"name": "mecânica do Evan (Filial)",
        		"description": "mecânica de carros em geral, profissional com experiência de 30 anos no mercado como empregado, procuro oportunidade para abrir meu próprio negócio",
        		"value": 20000,
        		"amount_collected": 0,
        		"finished": false,
        		"created_at": "30/05/2022",
        		"deadline": "31/05/2022",
        		"is_activated": false,
        		"user": {
        			"name": "Evan",
        			"email": "ent1@mail.com"
        		},
        		"id_deleted":false
        	}
        ]
        ```
        
    - read one - GET -/api/idea/owner/:id/ (ENTREPRENEUR)
        
        rota autenticada com token
        
        empresário poderá visualizar sua ideia pelo id
        
        ROTA
        
        URL/api/idea/7233c63b-2e65-4e51-9f34-07b8de4c6668/
        
        ```json
        **RESPONSE 200 - OK
        {
        	"idea": {
        		"id": "8701be61-1482-45b6-bb11-62bc555365c6",
        		"name": "padaria pão de mel",
        		"description": "Padaria locaizada em bairro nobre da cidade, ótimo potencial de clientela, concorrência mais próxima a 10km",
        		"value": 15550,
        		"amount_collected": 2000,
        		"finished": false,
        		"created_at": "26/05/2022",
        		"deadline": "27/05/2022",
        		"is_activated": true,
        		"user_id": {
        			"name": "Everaldo",
        			"email": "ent2@mail.com"
        		},**
        		"id_deleted":false
        	**},
        	"investors": [
        		{
        			"user": {
        				"name": "Adolfo",
        				"email": "inv2@mail.com"
        			},
        			"value": 1000
        		},
        		{
        			"user": {
        				"name": "Adolfo",
        				"email": "inv2@mail.com"
        			},
        			"value": 1000
        		}
        	]
        }**
        ```
        
        Caso token esteja incorreto
        
        ```json
        **RESPONSE 401 - UNAUTHORIZED**
        {
        	"detail": "Invalid token."
        }
        ```
        
        Caso id não exista
        
        ```json
        **RESPONSE 404 - NOT FOUND
        {
        	"error": "Proposal not found"
        }**
        ```
        
    - update - PATCH -/api/idea/:id/
        
        Rota autenticada com token
        
        Apenas empreendedores podem alterar as informações de suas respectivas ideias
        
        Requisição correta
        
        ```json
        {
        	"name":"mecânica",
        	"description":"mecânica de carros em geral, ..."
        	"value":18000,
        	"is_activated": true,
        }
        ```
        
        Resposta 
        
        ```json
        **RESPONSE 200 - OK**
        
        {
        		"id": "999bb5f3-a80e-4e78-8764-64ca948071f5",
        		"name": "mecânica",
        		"description": "mecânica de carros em geral, experiência de 30 anos no mercado como empregado, procuro oportunidade para abrir meu próprio negócio",
        		"value": 18000,
        		"amount_collected": 18000,
        		"finished": false,
        		"is_active": true,
        		"created_at": "20/05/2022",
        		"deadline": "18/08/2022",
        		"user": {
        			"id": "66848116-681f-4ee2-856c-282fcf2753b2",
        			"name": "ent",
        			"email": "ent1@mail.com",
        			"phone": "9999999999"
        		},
        		"id_deleted":false
        ```
        
        Resposta se usuário não for dono da ideia
        
        ```json
        **RESPONSE 422 - UNPROCESSABLE ENTITY
        
        {"error": "This idea does not belong to you"}**
        ```
        
        Requisição para mudar **is_activaded** para **false**
        
        ```json
        {
        		"is_activated":false
        }
        ```
        
        Resposta caso ideia possua algum investimento 
        
        ```json
        **RESPONSE 401 - UNAUTHORIZED**
        {
        	**"error": "This proposal have investments. Can't be deactivated"**
        }
        ```
        
        Requisição para mudar **is_activated** para true
        
        ```json
        {
        	**"is_activated":true**
        }
        ```
        
        Resposta caso já exista outra ideia ativa
        
        ```json
        **RESPONSE 401 - UNAUTHORIZED**
        {
        	**"message": "Already have an active proposal"**
        }
        ```
        
    - delete - DELETE - /api/idea/:id/
        
        rota autenticada com token
        
        Apenas empreendedores poderão deletar suas respectivas ideias, porem ideia não será deletada, será alterado o is_deletede para true, assim a ideia fica registrada no banco de dados para futuras pesquisas de investimentos
        
        ROTA
        
        URL/api/idea/7233c63b-2e65-4e51-9f34-07b8de4c6668/
        
        Caso id e token estejam corretos e idea não tenha nenhum investimento 
        
        ```json
        **RESPONSE 204 - NO CONTENT**
        ```
        
        Caso id e token estejam corretos mas idea tem investimentos
        
        ```json
        **RESPONSE 401 - UNAUTHORIZED**
        {	
        	**"error": "This proposal have investments. Can't be deleted"**
        { 
        ```
        
        Caso id esteja incorreto
        
        ```json
        **RESPONSE 404 - FOT FOUND**
        {
        	**"error": "Idea does not exists"**
        }
        ```
        
        Caso  idea_id seja de outro empreendedor
        
        ```json
        **RESPONSE 401 - UNAUTHORIZED
        {
        	"error": "You can't perform this action"
        }**
        ```
        
- **investments**:
    - create - POST -/api/investment/
        
        rota autenticada com token
        
        Somente investidores poderão criar um investimento para cada ideia cadastrada
        
        | CHAVES | VALORES | OBRIGATORIEDADE |
        | --- | --- | --- |
        | value | integer | X |
        | idea_id | string, max(255) | X |
        
        Requisição correta com valor que não pague o total→ Insere um investimento
        
        ```json
        {
        	"value": 5000,
        	"idea_id": "7233c63b-2e65-4e51-9f34-07b8de4c6668"
        }
        ```
        
        ```json
        **RESPONSE 201 - CREATED**
        
        {
        	"value": 5000,
        	"idea": {
        		"id": "7233c63b-2e65-4e51-9f34-07b8de4c6668",
        		"name": "padaria",
        		"description": "Padaria locaizada em bairro nobre da cidade, ótimo potencial de clientela, concorrência mais próxima a 10km",
        		"value": 15550,
        		"amount_collected": 5000,
        		"finished": false,
        		"created_at": "20/05/2022",
        		"deadline": "24/05/2022",
        	},
        	"percentage": 32.15
        }
        ```
        
        Requisição correta → com valor que ultrapasse o total
        
        ```json
        **RESPONSE 422 - Unprocessable Entity**
        
        { "message": "value exceeds the investment required" }
        ```
        
        Requisição correta → com valor que pague o total
        
        ```json
        **RESPONSE 201 - CREATED**
        
        {
        	"value": 15550,
        	"idea": {
        		"id": "7233c63b-2e65-4e51-9f34-07b8de4c6668",
        		"name": "padaria",
        		"description": "Padaria locaizada em bairro nobre da cidade, ótimo potencial de clientela, concorrência mais próxima a 10km",
        		"value": 15550,
        		"amount_collected": 15550,
        		"finished": **true**,
        		"created_at": "20/05/2022",
        		"deadline": "24/05/2022",
        	}
        }
        ```
        
        Requisição incorreta → faltando um mais campo obrigatório:
        
        ```json
        **RESPONSE 400 - BAD REQUEST**
        
        {
          "value": [
            "This field is required."
          ],
          "idea_id": [
            "This field is required."
          ]
        }
        ```
        
        Requisição incorreta →quando o tipo de dado não é válido
        
        ```json
        {
        	"value": "Antonio Costa",
        	"idea_id": "123"
        }
        ```
        
        ```json
        **RESPONSE 400 - Bad Request**
        {
          "value": [
            "Not a valid integer."
          ],
        	"idea_id": [
            "Not a valid string."
          ],
        }
        ```
        
    - read all - GET - /api/investment/
        
        rota autenticada com token
        
        Permite uso de paginação
        
        /api/investment/?page=1&per_page=20/
        
        O usuário, se não for admin, só poderá ver seus investimentos.
        
        Não tem Json de envio.
        
        Retorna:
        
        ```json
        **RESPONSE 200 - OK**
        [
          {
          	"value": 5000,
        	  "idea": {
        		  "id": "7233c63b-2e65-4e51-9f34-07b8de4c6668",
          		"name": "padaria",
        	  	"description": "Padaria locaizada em bairro nobre da cidade, ótimo potencial de clientela, concorrência mais próxima a 10km",
        		  "value": 15550,
          		"amount_collected": 15550,
        	  	"finished": true,
        		  "created_at": "20/05/2022",
          		"deadline": "24/05/2022",
        	  }
          },
          {
          	"value": 10000,
        	  "idea": {
        		  "id": "7233c63b-2e65-4e51-9f34-07b8de4d8543",
          		"name": "Loja de Games",
        	  	"description": "Loja de jogos (games) situada no centro da cidade de Sorocaba-SP",
        		  "value": 150000,
          		"amount_collected": 20000,
        	  	"finished": false,
        		  "created_at": "20/05/2022",
          		"deadline": "24/05/2022",
        	  }
          },
        ]
        ```
        
    - read one - GET - /api/investment/:id/
        
        rota autenticada com token
        
        Não tem Json de envio.
        
        O usuário, se não for admin, só poderá ver investimento próprio.
        
        Requisição correta:
        
        ```json
        **RESPONSE 200 - OK**
        {
        	"value": 15550,
        	"idea": {
        		"id": "7233c63b-2e65-4e51-9f34-07b8de4c6668",
        		"name": "padaria",
        		"description": "Padaria locaizada em bairro nobre da cidade, ótimo potencial de clientela, concorrência mais próxima a 10km",
        		"value": 15550,
        		"amount_collected": 15550,
        		"finished": **true**,
        		"created_at": "20/05/2022",
        		"deadline": "24/05/2022",
        	}
        }
        ```
        
        Requisição correta → mas não está logado
        
        ```json
        **RESPONSE 401 - Unauthorized**
        
        {
          "detail": "Authentication credentials were not provided."
        }
        ```
        
        Requisição correta →  id não pertence ao usuário e a requisição não veio de um admin
        
        ```json
        **RESPONSE 401 - Unauthorized**
        
        {
          "detail": "Authentication credentials allow access."
        }
        ```
        
        Requisição correta → id não existe
        
        ```json
        **RESPONSE 404 - Not Found**
        
        {
          "message": "Idea does not exist"
        }
        ```