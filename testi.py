import re

podatek = re.finditer(r'(?P<krneki>[^я]*)', 'aaasdfsdfsdfsdegdsf')


for tabela in podatek:
	print(tabela.group('krneki'))
	print(tabela)