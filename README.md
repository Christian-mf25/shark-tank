# <b>FIND & INVEST

## URLBASE = localhost:300

### Rotas que não necessitam de autenticação

## Criar Conta
`POST - /api/users/ - formato da requisição`

```JSON
{
	"name": "Pedro Silva",
	"email": "psilva@email.com",
	"password": "123456",
    "phone": "(11)98585-5858",
    "is_inv" : false
}
```








## Login
`POST - /api/login/ - formato da requisição`
```JSON
{
	"email": "psilva@email.com",
	"password": "123456"
}
```
`Formato da resposta - status 200`
```JSON
{
	"token": "3c68840fc0b20dfa350804b689c1fedfeea438ff"
}
```

Caso usuário não esteja cadastrado<br>
`Formato da resposta - status 401`
```JSON
{
	"message": "Invalid password or e-mail address"
}
```
Caso email ou senham estejam incorretos<br>
`Formato da resposta - status 401`
```JSON
{
	"message": "Invalid password or e-mail address"
}
```
Caso requisição seja diferente de string<br>
`Formato da requisição`
```JSON
{
	"email": ["psilva@email.com"],
	"password": "123456"
}
```
`Formato da resposta - status 400`
```JSON
{
	"email": [
		"Not a valid string."
	]
}
```
Caso requisição esteja em branco<br>
`Formato da requisição`
```JSON
{
	"email": "psilva@email.com",
	"password": ""
}
```
`Formato da resposta - status 400`
```JSON
{
	"password": [
		"This field may not be blank."
	]
}
```
Caso requisição falte uma ou mais chaves<br>
`Formato da requisição`
```JSON
{
	"email": "psilva@email.com"
}
```
`Formato da resposta - status 400`
```JSON
{
	"password": [
		"This field is required."
	]
}
```