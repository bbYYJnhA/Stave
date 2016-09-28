#from utils import *
import re
import orodja
import datetime
import os
datum = datetime.datetime.today().isoformat()[:10] + '/'

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

def pripravi_bwin(potdatoteke = datum):    
    reg_sportnika = re.compile(r'<td class="option  option_(.*?)" >'
    r'[^я]*?<span class="option-name">(?P<sportnik>.*?) \((?P<drzava>.*?)\)</span>'
    r'[^я]*?<span class="odds">(?P<kvota>.*?)</span>')
    reg_dogodka = re.compile(r'.*<a class="league-link" href=".*" >(?P<dogodek>.*.)\n* *- (?P<drzava>.*)</a>')
        #r'.*<a class="league-link" href=".*" >(?P<dogodek>.*.\n.*)</a>')
    reg_datumi = re.compile(r'(?P<vse><h2 class="event-group-level3">[^Я]*?  *.* - (?P<datum>.*)[^Я]*?<div class="ui-widget-content-body)')
    
    ###############################################################
    #Tole je preveč. Treba je iti korak za korakom.               #
    ###############################################################
    #reg_datumi = re.compile(r'<h2 class="event-group-level3">[^Я]*?  *.* - (?P<datum>.*)[^Я]*?</h2>'
    #                        r'[^Я]*?<a class="league-link" href="(.*)[^Я]*? - (?P<kategorija>.*)</a>'
    #                        r'[^Я]*?<h6 class="event-info">[^Я]*? *(?P<kraj>.*)[^Я]*?<td class="option  option_'
    #                        r'(.*?)" >'
    #                        r'[^я]*?<span class="option-name">(?P<sportnik>.*?).\((?P<drzava>.*?)\)</span>'
    #                        r'[^я]*?<span class="odds">(?P<kvota>.*?)</span>'
    #                        r'[^я]*</html>')

    reg_celatabela = re.compile(
        r'<a class="league-link" href=".*" >(?P<dogodek>[^Я]*?)</a>[^я]*?<span class="option-name">'
        r'(?P<sportnik>.*?) \((?P<drzava>.*?)\)</span>[^Я]*?<span class="odds">(?P<kvota>.*)'
        r'</span>[^я]*?(<a class="league-link" href=|<div class="ui-widget-content" id="sport-footer">)'
        )
    
    igralci_surovo = []
    dogodki = []
    igralci = []
    kategorije = []
    
    for html_datoteka in orodja.datoteke('zajete-strani/' + potdatoteke + '/bwin/'):
        datoteka = 'zajete-strani/' + potdatoteke + '/' + html_datoteka
        csvDat = 'csv-datoteke/'+ html_datoteka[13:-5]
        for ujemanje in re.finditer(reg_datumi, orodja.vsebina_datoteke(html_datoteka)):
            #print(uredi_datum(ujemanje.group('vse'), ujemanje.group('datum')))
            #print(ujemanje.groupdict())
            if uredi_datum(ujemanje.group('vse'), ujemanje.group('datum')) != {}:
                kategorije += [uredi_datum(ujemanje.group('vse'), ujemanje.group('datum'))]
        orodja.zapisi_tabelo(kategorije, ['datum', 'kategorija'], csvDat +  '/kategorije.csv')
        
        for ujemanje in re.finditer(reg_celatabela, orodja.vsebina_datoteke(html_datoteka)):
            igralci += [ujemanje.groupdict()]
        orodja.zapisi_tabelo(igralci, ['dogodek', 'kvota', 'drzava','sportnik'], csvDat +  '/sportniki.csv')
        for ujemanje in re.finditer(reg_dogodka, orodja.vsebina_datoteke(html_datoteka)):
            dogodki += [ujemanje.groupdict()]
        orodja.zapisi_tabelo(dogodki, ['dogodek', 'drzava'], csvDat +  '/dogodki.csv')
#        
        for ujemanje in re.finditer(reg_sportnika, orodja.vsebina_datoteke(html_datoteka)):
            #print(ujemanje.groupdict())            
            igralci_surovo += [ujemanje.groupdict()]
        orodja.zapisi_tabelo(igralci_surovo, ['sportnik', 'drzava', 'kvota'], csvDat +  '/sportniki_surovo.csv')


def uredi_datum(datum, ze):
    podatki = datum
    reg_datumi = re.compile(r'<h2 class="event-group-level3">[^Я]*?  *.* - (?P<datum>.*)[^Я]*?<div class="ui-widget-content-body')
    reg_kategorija = re.compile(r'<h6 class="game">(?P<kategorija>.*?)</h6>')
    slovar = {}
    for kat in re.finditer(reg_kategorija, podatki):
        try:
            a = slovar['datum'].add(kat.group('kategorija'))
            slovar['datum'] = ze
            slovar['kategorija'] = kat.group('kategorija')
        except:
            slovar['datum'] = ze
            slovar['kategorija'] = kat.group('kategorija')
    #podatki = [kat.group('kategorija') for kat in re.finditer(reg_kategorija, podatki['datum'])]
    return slovar
    #print(podatki)
    #regx_sportnika=re.compile(r'')	
    #podatki['sportniki'] = {
    #        sportnik.group('id'): sportnik.group('ime')
    #        for sportnik in re.finditer(regex_sportnika, podatki['sportniki'])	
    #    }
    #    return podatki['id'], podatki


#pripravi_bwin('2016-01-16')
#pripravi_bwin('2016-01-17')
#pripravi_bwin('2016-01-18')
#pripravi_bwin('2016-01-20')
#pripravi_bwin('2016-01-21')
#pripravi_bwin('2016-01-22')

