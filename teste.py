from re import fullmatch

digitos9 = '5511973758356' #celular com 9 digitos
digitos8 = '(48)99848-1774'  #celular com 8 digitos

padrao = "(\(?\d{2}\)?)?(\d{4,5}\-\d{4})"

teste_1 = fullmatch(padrao, digitos9)
teste_2 = fullmatch(padrao, digitos8)

if teste_1:
	print("teste 1 passou")

if teste_2:
	print("teste 2 passou")

