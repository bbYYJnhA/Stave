import re
import orodja
import datetime
import os
datum = 'zajete-strani/' + datetime.datetime.today().isoformat()[:10] + '/'

def zajemi_bwin():
	if not os.path.exists(datum):
		os.makedirs(datum)
	orodja.shrani('https://sports.bwin.com/en/sports', datum + 'bwin.html')
	izraz = r'href="(?P<link>/en/sports/(?P<id>[0-9]+)/.*/(?P<sport>.*))" title=".*">\s*<span class="sporticon"'
	#print(izraz)
	regex_url_filma = re.compile(izraz)
	#print(regex_url_filma)
	#print(orodja.vsebina_datoteke(datum + 'bwin.html'))
	for sport in re.finditer(regex_url_filma, orodja.vsebina_datoteke(datum + 'bwin.html')):
		url = 'https://sports.bwin.com{}'.format(sport.group('link'))
		ime_datoteke = datum + 'bwin/{}.html'.format(sport.group('sport'))
		print(url)
		orodja.shrani(url, ime_datoteke)

#zajemi_bwin()

def pripravi_bwin(potdatoteke = datum):
	regex_celatabela = re.compile(
		r'(?P<vse>.*<a class="league-link" href=".*" >(?P<ime_dogodka>.*.)\n *- (?P<drzava>.*)</a>'
		r'[^я]*?<span class="option-name">(?P<igralec>.*)</span>\n *<span class="odds">(?P<kvota>.*)</span>'
		r'[^я]*?(<a class="league-link" href=|<div class="ui-widget-content" id="sport-footer">))'
		)
	regex_celatabela1 = re.compile(
		r'(?P<vse>.*<a class="league-link" href=".*" >(?P<ime_dogodka>.*.)\n *- (?P<drzava>.*)</a>'
		r'[^я]*?<span class="option-name">(?P<igralec>.*)</span>\n *<span class="odds">(?P<kvota>.*)</span>'
		r'[^я]*?(<a class="league-link" href=|<div class="ui-widget-content" id="sport-footer">))'
		)
	regex_dogodka1 = re.compile(
		r'.*<h6 class="game">(?P<dogodek>.*)</h6>'
		r'[^я]<h6 class="game">'
		#r'.*<a class="league-link" href=".*" >(?P<dogodek>.*.\n.*)</a>'
		)
	regex_dogodka1 = re.compile(
		r'.*<a class="league-link" href=".*" >(?P<dogodek>.*.)\n* *- (?P<drzava>.*)</a>'
		r''
		#r'.*<a class="league-link" href=".*" >(?P<dogodek>.*.\n.*)</a>'
		)
	
	regex_sporta = re.compile(
		r'<button type="submit" class="no-uniform option-button fav-button">\n* *<span class="option-name">'
		r'(?P<ime>.*)</span>\n* *<span class="odds">(?P<kvota>.*)</span>')



	dogodek, igralec = {}, {}
	drzava, kvota = set(), []
	podatki_dogodkov = {}
	j = 1
	i = 1
	kvot = 0

	print(orodja.datoteke(potdatoteke + '/bwin/'))
	for html_datoteka in orodja.datoteke(potdatoteke + '/bwin/'):
		#print(orodja.vsebina_datoteke(html_datoteka))
		for tabela in re.finditer(regex_celatabela, orodja.vsebina_datoteke(html_datoteka)):
			print('***')
			#print(tabela)
			for podatki in re.finditer(regex_celatabela, tabela.group('vse')):				
				#for dogodek in re.finditer(regex_dogodka, tabela.group('vse')):
				#dogodek = podatki.group('dogodek')
				dogodek = tabela.group('ime_dogodka')
				igralec = tabela.group('igralec')
				print(dogodek)
				print(podatki)
				print(igralec + tabela.group('kvota'))
				podatki_dogodka = podatki_dogodkov.get(dogodek, {})
				podatki_dogodka[tabela.group('igralec')] = tabela.group('kvota')
				podatki_dogodkov[dogodek] = podatki_dogodka
				#drzava.add(podatki.group('drzava'))
				#print(podatki.group('dogodek') + ' -- ' + podatki.group('igralec') + ' -- ' + podatki.group('kvota'))



	#for html_datoteka in orodja.datoteke(potdatoteke + '/bwin/'):
	#	print(html_datoteka)
	#	for ime in re.finditer(regex_dogodka, orodja.vsebina_datoteke(html_datoteka)):
	#		if ime.group('drzava') == 'Slovenia':
	#			pass
				#print(ime.group('dogodek') + ' ' + ime.group('drzava')  + ' ' + html_datoteka)
	#		j += 1



	for html_datoteka in orodja.datoteke(potdatoteke + '/bwin/'):
		for ime in re.finditer(regex_sporta, orodja.vsebina_datoteke(html_datoteka)):
			#print(ime.group('ime') + '  '  + ime.group('kvota') + ' ' + datum[14:-1])
			i += 1
			kvot += float(ime.group('kvota'))
	orodja.zapisi_tabelo(igralec.values(), ['igralec', 'kvota'], 'csv-datoteke/dogodki.csv')
	print(drzava)
	print(igralec)
	return (i, j, kvot/i)
	
	
pripravi_bwin('zajete-strani/2016-01-16')

drzave = {}
def get_id_drzave(niz):
	if niz in drzave:
		return drzave[niz]
	else:
		drzave[niz] = len(drzave)

def uredi_sport(sport):
	podatki = sport.groupdict()

	regex_dogodka = re.compile(
	r'.*<a class="league-link" href=".*" >(?P<dogodek>.*.)\n *- (?P<drzava>.*)</a>'
	r''
	#r'.*<a class="league-link" href=".*" >(?P<dogodek>.*.\n.*)</a>'
	)
	podatki['dogodek'] = {
        	dogodek.group('id'): dogodek.group('ime')
        	for
        	dogodek in re.finditer(regex_dogodka, podatki['dogodki'])	
	}
	regx_sportnika=re.compile(r'')	
	podatki['sportniki'] = {
        	sportnik.group('id'): sportnik.group('ime')
        	for
        	sportnik in re.finditer(regex_sportnika, podatki['sportniki'])	
	}
	return podatki['id'], podatki





