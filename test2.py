import re
import orodja
   
   
   
reg_datumi = re.compile(r'<h2 class="event-group-level3">[^Я]*?  *.* - (?P<datum>.*)[^Я]*?<div class="ui-widget-content-body')
reg_dogodka = re.compile(r'.*<a class="league-link" href=".*" >(?P<dogodek>.*.)\n* *- (?P<drzava>.*)</a>')

#<h2 class="event-group-level3">[^Я]*?  *.* - (?P<datum>.*)[^Я]*?(<a class="league-link" href=|<div class="ui-widget-content" id="sport-footer">)

for ujemanje in re.finditer(reg_datumi, orodja.vsebina_datoteke('zajete-strani/2016-01-16/bwin/alpine-skiing.html')):
    print(ujemanje.groupdict())
