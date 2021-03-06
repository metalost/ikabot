#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import getpass
import ikabot.config as config
from ikabot.web.sesion import *
from ikabot.helpers.pedirInfo import read
from ikabot.helpers.gui import banner

def getSesion():
	banner()
	html = normal_get('https://es.ikariam.gameforge.com/?').text
	servidores = re.findall(r'<a href="(?:https:)?//(\w{2})\.ikariam\.gameforge\.com/\?kid=[\d\w-]*" target="_top" rel="nofollow" class="mmoflag mmo_\w{2}">(.+)</a>', html)
	i = 0
	for server in servidores:
		i += 1
		print('({:d}) {}'.format(i, server[1]))
	servidor = read(msg='Servidor:', min=1, max=len(servidores))
	srv = servidores[servidor - 1][0]
	config.infoUser = 'Servidor:{}'.format(servidores[servidor-1][1])
	banner()
	if srv != 'es':
		html = normal_get('https://{}.ikariam.gameforge.com/?'.format(srv)).text
	html = re.search(r'registerServer[\s\S]*registerServerServerInfo', html).group()
	mundos = re.findall(r'mobileUrl="s(\d{1,3})-\w{2}\.ikariam\.gameforge\.com"(?:\s*cookieName="")?\s*>\s*([\w\s]+?)\s*</option>', html)
	i = 0
	for mundo in mundos:
		i += 1
		print('({:d}) {}'.format(i, mundo[1]))
	mundo = read(msg='Mundo:', min=1, max=len(mundos))
	mundo = mundos[mundo - 1]
	config.infoUser += ', Mundo:{}'.format(mundo[1])
	urlBase = 'https://s{}-{}.ikariam.gameforge.com/index.php?'.format(mundo[0], srv)
	uni_url = 's{}-{}.ikariam.gameforge.com'.format(mundo[0], srv)
	banner()
	usuario = read(msg='Usuario:')
	password = getpass.getpass('Contraseña:')
	headers = {'Host': uni_url, 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, br', 'Content-Type':'application/x-www-form-urlencoded', 'Referer': urlBase}
	payload = {'uni_url': uni_url, 'name': usuario, 'password': password, 'pwat_uid': '', 'pwat_checksum': '' ,'startPageShown' : '1' , 'detectedDevice' : '1' , 'kid':''}
	config.infoUser += ', Jugador:{}'.format(usuario)
	return Sesion(urlBase, payload, headers)
