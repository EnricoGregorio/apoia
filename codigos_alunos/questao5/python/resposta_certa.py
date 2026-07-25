valor_compra = 200.0

if valor_compra > 150.0:
	valor_com_desconto = valor_compra - valor_compra * 0.10
	print("Compra com desconto: ", valor_com_desconto)
else:
	print("Valor normal: ", valor_compra)