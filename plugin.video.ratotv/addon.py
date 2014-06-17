#!/usr/bin/env python
# -- coding: utf-8 --
# Copyright 2013 enen92 e Pedrock
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################
from __future__ import division
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcvfs,xbmc,xbmcaddon,HTMLParser,json,os,time,datetime,binascii
from t0mm0.common.addon import Addon

h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.ratotv'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder+'/resources/img/'
addon = Addon(addon_id)
datapath = addon.get_profile()
ADDON = selfAddon

base_url = 'http://www.ratotv.net/'
escolher_qualidade = xbmcgui.Dialog().select
mensagemok = xbmcgui.Dialog().ok
progresso = xbmcgui.DialogProgress()
tmdb_base_url = 'http://d3gtl9l2a4fn1j.cloudfront.net/t/p/w1280'
fanart_rato_tv = addonfolder + '/fanart.jpg'
setting_limpar_metadata = "limpar-metadata"

######################################################################################################
#                                               MENUS                                                #
######################################################################################################

def Menu_principal():
	login_sucessful = check_login()
	if login_sucessful == True:
		addDir_reg_menu('Filmes','url',1,artfolder+'filmes.jpg',True)
		addDir_reg_menu('Séries',base_url,8,artfolder+'series.jpg',True)
		addDir_reg_menu('Pedidos',"http://www.ratotv.net/requests/page/1/",33,artfolder+'contactar.jpg',True)
		addDir_reg_menu('Pesquisar','url',4,artfolder+'pesquisa.jpg',True)
		addDir_reg_menu('','','',addonfolder+'logo.png',False)
		addDir_reg_menu('Favoritos','http://www.ratotv.net/favorites/page/1/',15,artfolder+'favoritos.jpg',True)
		addDir_reg_menu('Séries subscritas',base_url + 'index.php?cstart=1&do=cat&category=tvshows',45,artfolder+'series.jpg',True)
		addDir_reg_menu('Séries a seguir',base_url + 'index.php?cstart=1&do=cat&category=tvshows',26,artfolder+'series.jpg',True)
		addDir_reg_menu('Géneros','url',5,artfolder+'categorias.jpg',True)
		addDir_reg_menu('Ano','url',42,artfolder+'pesquisa.jpg',True)
		addDir_reg_menu('Definições','url',9,artfolder+'definicoes.jpg',True)
		addDir_reg_menu('','','',addonfolder+'logo.png',False)
		mensagens_conta()
		#if selfAddon.getSetting(setting_limpar_metadata) == "true": limpar_pasta_metadata()
		menu_view()
	if selfAddon.getSetting('novos-episodios') == "true": verificar_novos()
	else:
		addDir_reg_menu('Alterar Definições','url',9,artfolder+'definicoes.jpg',False)
		addDir_reg_menu('Tentar Novamente','url',None,artfolder+'refresh.jpg',True)
		menu_view()

def Menu_principal_series():
    addDir_reg_menu('Todas as séries',base_url + 'index.php?cstart=1&do=cat&category=tvshows',2,artfolder+'series.jpg',True)
    addDir_reg_menu('Séries a seguir',base_url + 'index.php?cstart=1&do=cat&category=tvshows',26,artfolder+'series.jpg',True)
    addDir_reg_menu('Séries subscritas',base_url + 'index.php?cstart=1&do=cat&category=tvshows',45,artfolder+'series.jpg',True)
    addDir_reg_menu('Séries mais recentes',base_url,6,artfolder+'series-mais.jpg',True)
    addDir_reg_menu('Séries mais populares',base_url,6,artfolder+'series-mais.jpg',True)
    addDir_reg_menu('Séries mais vistas',base_url,6,artfolder+'series-mais.jpg',True)
    addDir_reg_menu('Séries mais votadas',base_url,6,artfolder+'series-mais.jpg',True)
    menu_view()

def Menu_principal_filmes():
    addDir_reg_menu('Todos os filmes',base_url + 'movies/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Filmes mais recentes',base_url,6,artfolder+'filmes-mais.jpg',True)
    addDir_reg_menu('Filmes mais populares',base_url,6,artfolder+'filmes-mais.jpg',True)
    addDir_reg_menu('Filmes mais vistos',base_url,6,artfolder+'filmes-mais.jpg',True)
    addDir_reg_menu('Filmes mais votados',base_url,6,artfolder+'filmes-mais.jpg',True)
    menu_view()

def Menu_categorias_filmes():
    addDir_reg_menu('Acção',base_url + 'tags/Ação/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Animação',base_url + 'tags/Animação/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Aventura',base_url + 'tags/Aventura/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Biografia',base_url + 'tags/Biografia/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Comédia',base_url + 'tags/Comédia/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Crime',base_url + 'tags/Crime/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Desporto',base_url + 'tags/Desporto/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Documentário',base_url + 'tags/Documentário/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Drama',base_url + 'tags/Drama/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Familiar',base_url + 'tags/Familiar/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Fantasia',base_url + 'tags/Fantasia/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Ficção Científica',base_url + 'tags/Ficção+Científica/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Guerra',base_url + 'tags/Guerra/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('História',base_url + 'tags/História/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Mistério',base_url + 'tags/Mistério/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Musical',base_url + 'tags/Musical/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Romance',base_url + 'tags/Romance/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Terror',base_url + 'tags/Terror/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Thriller',base_url + 'tags/Thriller/page/1/',2,artfolder+'filmes.jpg',True)
    addDir_reg_menu('Western',base_url + 'tags/Western/page/1/',2,artfolder+'filmes.jpg',True)
    menu_view()

def alterar_definicoes():
        oldUsername=selfAddon.getSetting('login_name')
        oldPassword=selfAddon.getSetting('login_password')
        selfAddon.openSettings()
        if oldUsername != selfAddon.getSetting('login_name') or oldPassword != selfAddon.getSetting('login_password'):
            addDir_reg_menu('Entrar novamente','url',None,artfolder+'refresh.jpg',True)
            menu_view()
            xbmcplugin.endOfDirectory(int(sys.argv[1]))

def menu_ano():
	addDir_reg_menu('[B][COLOR green]Introduzir ano manualmente[/B][/COLOR]','url',41,artfolder+'pesquisa.jpg',True)
	for i in reversed(xrange(1900,2015)):
		addDir_reg_menu(str(i),base_url + 'tags/' + str(i) + '/page/1/',16,artfolder+'pesquisa.jpg',True)

##################################################################################################################################
#                                                       FUNCOES LISTAGEM                                                         #
##################################################################################################################################

def get_original_title(url):
	try: html_source=post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
	except: html_source = ""
	if html_source:
		match = re.compile("<strong>Título Original: </strong>(.+?)</li>").findall(html_source)
		if match: return match[0]
		else: return "N/A"

def play_video(name,url,iconimage,Sources,srt,seriesName,season,episode):
	sources = eval(Sources)
	infolabels = { "Title": name , "TVShowTitle":originaltitle,"Season":season, "Episode":episode }
	titles = []; url_movie_file=[]
	for movie_file,quality in sources:
		if "http://" in movie_file:
			titles.append('[B]' + quality + '[/B]')
			url_movie_file.append(movie_file)
		else:
    			try:
				titles.append('[B]' + quality + '[/B]')
				decrypted = abrir_url("http://www.ratotv.net/xmbc/zen.php?hash=" + movie_file)
				if "http://" in decrypted:
					url_movie_file.append(decrypted)
				else:
					try:
						data = re.compile('<input.*?name="(.*?)".*?value="(.*?)"').findall(abrir_url(binascii.unhexlify(''.join('68 74 74 70 3A 2F 2F 76 69 64 78 2E 74 6F 2F'.split())) + decrypted + binascii.unhexlify(''.join('2E 68 74 6D 6C'.split()))))
						mydata='['
						for i in xrange(len(data)):
							if i != len(data)-1:
								mydata += "('" + data[i][0] + "','" + data[i][1] + "'),"
							else:
								mydata += "('" + data[i][0] + "','" + data[i][1] + "')"
						mydata += ']';data = eval(mydata);
						handle_wait(11,"RatoTV","Por favor aguarde 11 segundos...",segunda='')
						r = re.compile('file: "(.+?)",').findall(post_page_free(binascii.unhexlify(''.join('68 74 74 70 3A 2F 2F 76 69 64 78 2E 74 6F 2F'.split())) + decrypted + binascii.unhexlify(''.join('2E 68 74 6D 6C'.split())),data))[0]
						url_movie_file.append(r)
					except: print "Erro Vid"; pass
			except: pass
	if len(titles) != 1:
		if selfAddon.getSetting('qualidade-auto') == "false":
			choose=escolher_qualidade('Seleccione a qualidade',titles)
			if choose > -1: linkescolha=player_rato(url_movie_file[choose],srt,name,url,iconimage,infolabels,season,episode)
		else: linkescolha=player_rato(url_movie_file[0],srt,name,url,iconimage,infolabels,season,episode)
	else: player_rato(url_movie_file[0],srt,name,url,iconimage,infolabels,season,episode)

def resolver_externos(hashstring):
	print hashstring
	try: decoded_url = abrir_url("http://www.ratotv.net/xmbc/zen.php?hash=" + hashstring)
	except: ok=mensagemok('RatoTV','Não conseguiu resolver a hash.');decoded_url = ""
	if "http://" in decoded_url:
		return decoded_url
	else:
		if "stri" in decoded_url:
			try:
				data = re.compile('<input type="hidden" name="(.+?)" value="(.+?)">').findall(abrir_url(binascii.unhexlify(''.join('68 74 74 70 3A 2F 2F 73 74 72 65 61 6D 69 6E 2E 74 6F 2F'.split())) + str(decoded_url.replace("stri",""))))
				mydata='['
				for i in xrange(len(data)):
					if i != len(data)-1:
						mydata += "('" + data[i][0] + "','" + data[i][1] + "'),"
					else:
						mydata += "('" + data[i][0] + "','" + data[i][1] + "')"
				mydata += ',("usr_login",""),("referer","")]';data = eval(mydata);
				handle_wait(6,"RatoTV","Por favor aguarde 6 segundos...",segunda='')
				sourcecode = post_page_free(binascii.unhexlify(''.join('68 74 74 70 3A 2F 2F 73 74 72 65 61 6D 69 6E 2E 74 6F 2F'.split())) + str(decoded_url.replace("stri","")),data)
				try: swfurl = re.compile('src: "(.+?)" }').findall(sourcecode)[0];rtmpurl = re.compile('streamer: "(.+?)"').findall(sourcecode)[0];	playpath = re.compile("file:'(.+?)'").findall(sourcecode)[0];rtmpurl = rtmpurl + ' playpath=' + playpath + ' swfUrl='+swfurl
				except:
					try: rtmpurl= re.compile('{file: "(.+?)"}').findall(sourcecode)[1]
					except: pass
				return rtmpurl
			except: ok=mensagemok('RatoTV','Não conseguiu resolver a hash.'); return False
		else:
			try:
				data = re.compile('<input.*?name="(.*?)".*?value="(.*?)"').findall(abrir_url(binascii.unhexlify(''.join('68 74 74 70 3A 2F 2F 76 69 64 78 2E 74 6F 2F'.split())) + decoded_url + binascii.unhexlify(''.join('2E 68 74 6D 6C'.split()))))
				mydata='['
				for i in xrange(len(data)):
					if i != len(data)-1: mydata += "('" + data[i][0] + "','" + data[i][1] + "'),"
					else: mydata += "('" + data[i][0] + "','" + data[i][1] + "')"
				mydata += ']';data = eval(mydata);
				handle_wait(11,"RatoTV","Por favor aguarde 11 segundos...",segunda='')
				decoded = re.compile('file: "(.+?)",').findall(post_page_free(binascii.unhexlify(''.join('68 74 74 70 3A 2F 2F 76 69 64 78 2E 74 6F 2F'.split())) + decoded_url + binascii.unhexlify(''.join('2E 68 74 6D 6C'.split())),data))[0]
				return decoded
			except: ok=mensagemok('RatoTV','Ocorreu um erro a obter o endereço.','Tente novamente')

def rssnumber(html_source):
	opcao = []; rssopcao=[]
	match = re.compile('playlist: "(.+?)"').findall(html_source)
	if match:
		opcao.append("1")
		rssopcao.append(match[0])
	match = re.compile('FlashVars="plugins.+?&proxy.list=(.+?)&').findall(html_source)
	for rssfile in match:
		rssopcao.append(rssfile)
		opcao.append(rssfile[-5])
	return opcao,rssopcao

def stream_qualidade(url,name,iconimage):
	print url
	titles = []; url_movie_file=[]
	try: html_source=post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
	except: ok=mensagemok('RatoTV','Não foi possível abrir a página. Tente novamente \n ou contacte um dos administradores do site.');html_source =""
	opcao,rssopcao = rssnumber(html_source)
	num_opcoes = len(opcao)
	if num_opcoes == 1: opcao = "1"
	elif num_opcoes == 2:
		janela2qualidades()
		opcao = readfile(datapath + "option.txt")
	elif num_opcoes == 3:
		janela3qualidades()
		opcao = readfile(datapath + "option.txt")
	else: ok=mensagemok('RatoTV','Ocorreu um erro. Tente novamente.')
	if opcao == "10": sys.exit(0)
	if selfAddon.getSetting('fonte-auto') == "true":
		try: rss_source = abrir_url(urllib.quote(rssopcao[int(opcao)-1], safe=":/"))
		except:
			try:
				if num_opcoes == 2:
					janela2qualidades("1")
					opcao = readfile(datapath + "option.txt")
				elif num_opcoes == 3:
					janela3qualidades("1")
					opcao = readfile(datapath + "option.txt")			
				rss_source = abrir_url(urllib.quote(rssopcao[int(opcao)-1], safe=":/"))
			except:
				try:
					if num_opcoes == 2:
						janela2qualidades("2")
						opcao = readfile(datapath + "option.txt")
					elif num_opcoes == 3:
						janela3qualidades("2")
						opcao = readfile(datapath + "option.txt")			
					rss_source = abrir_url(urllib.quote(rssopcao[int(opcao)-1], safe=":/"))
				except: ok=mensagemok('RatoTV','Ocorreu um erro. Tente novamente.')
		if opcao == "1":
			try:
				match = re.compile('<jwplayer:source file="(.+?)" label="(.+?)" />').findall(rss_source)
				for movie_file,quality in match:
						titles.append('[B]' + quality + '[/B]')
						url_movie_file.append(movie_file)
			except: ok=mensagemok('RatoTV','Não foi possível abrir a página. Tente novamente ou contacte um dos administradores do site.')
			try:
				subs = re.compile('<jwplayer:track file="../(.+?)" label=".+?').findall(rss_source)
				if len(subs) >= 1: subs = base_url + str(subs[0])
				else: subs = ''
			except: subs = ''
			print titles,url_movie_file,subs
			if selfAddon.getSetting('qualidade-auto') == "false":
				choose=escolher_qualidade('Seleccione a qualidade',titles)
				if choose > -1:
						linkescolha=player_rato(url_movie_file[choose]+ '|host=ratotv.com&referer=' + url,subs,name,url,iconimage,'',None,None)
			else:
				linkescolha=player_rato(url_movie_file[0]+ '|host=ratotv.com&referer=' + url,subs,name,url,iconimage,'',None,None)
		else:
			if rss_source:
				hash_movie = re.compile('<location>ratotv*(.+?)</location>').findall(rss_source)[0].replace("*","")
			else: ok=mensagemok('RatoTV','Não conseguiu obter a hash.')
			try:
				decoded_url = resolver_externos(hash_movie)
			except: ok=mensagemok('RatoTV','Não conseguiu resolver a hash.')
			try:
					subs = re.compile('<captions.files>../(.+?)</captions.files>').findall(rss_source)
					if len(subs) >= 1: subs = base_url + str(subs[0])
					else: subs = ''
			except: subs = ''
			player_rato(decoded_url,subs,name,url,iconimage,'',None,None)				
	else:
		if opcao == "1":
			try: rss_source = abrir_url(urllib.quote(rssopcao[0], safe=":/"))
			except: ok=mensagemok('RatoTV','Não foi possível abrir o feed da opção 1')
			try:
					match = re.compile('<jwplayer:source file="(.+?)" label="(.+?)" />').findall(rss_source)
					for movie_file,quality in match:
							titles.append('[B]' + quality + '[/B]')
							url_movie_file.append(movie_file)
			except: ok=mensagemok('RatoTV','Não foi possível abrir a página. Tente novamente ou contacte um dos administradores do site.')
			try:
				subs = re.compile('<jwplayer:track file="../(.+?)" label=".+?').findall(rss_source)
				if len(subs) >= 1: subs = base_url + str(subs[0])
				else: subs = ''
			except: subs = ''
			print titles,url_movie_file,subs
			if selfAddon.getSetting('qualidade-auto') == "false":
				choose=escolher_qualidade('Seleccione a qualidade',titles)
				if choose > -1: linkescolha=player_rato(url_movie_file[choose]+ '|host=ratotv.com&referer=' + url,subs,name,url,iconimage,'',None,None)
			else: linkescolha=player_rato(url_movie_file[0]+ '|host=ratotv.com&referer=' + url,subs,name,url,iconimage,'',None,None)
		else:
			try:
				rss_escolhido = int(opcao)-1;print rss_escolhido
				rss_source = abrir_url(urllib.quote(rssopcao[rss_escolhido], safe=":/"))
			except: ok=mensagemok('RatoTV','Não foi possível abrir o feed da opção 1')
			print rss_source
			if rss_source: hash_movie = re.compile('<location>ratotv*(.+?)</location>').findall(rss_source)[0].replace("*","")
			else: ok=mensagemok('RatoTV','Não conseguiu obter a hash.')
			try: decoded_url = resolver_externos(hash_movie)
			except: ok=mensagemok('RatoTV','Não conseguiu resolver a hash.')
			try:
					subs = re.compile('<captions.files>../(.+?)</captions.files>').findall(rss_source)
					if len(subs) >= 1: subs = base_url + str(subs[0])
					else: subs = ''
			except: subs = ''
			print subs
			player_rato(decoded_url,subs,name,url,iconimage,'',None,None)

def player_rato(video,subs,name,url,iconimage,infolabels,season,episode):
	match = re.compile('\((.+?)\)').findall(name)
	if match:
		name=name.replace(match[0],'').replace('(','').replace(')','')
		if infolabels == '': infolabels = dict()
		infolabels['Code'] = imdb_id
		infolabels['Year'] = match[0]
	if 'TVShowTitle' in infolabels:
		match = re.compile('\((.+?)\)').findall(infolabels['TVShowTitle'])
		if match: infolabels['TVShowTitle']=infolabels['TVShowTitle'].replace(match[0],'').replace('(','').replace(')','')
	print video,subs,name,iconimage,infolabels
	playlist = xbmc.PlayList(1)
	playlist.clear()
	if originaltitle: name = originaltitle
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	if infolabels: liz.setInfo( type="Video", infoLabels=infolabels )
	liz.setProperty('mimetype', 'video/x-msvideo')
	liz.setProperty('IsPlayable', 'true')
	playlist.add(video,liz)
	player = Player(url=url,season=season,episode=episode)
	player.play(playlist)
	if subs and selfAddon.getSetting('subtitles-active')=='true': player.setSubtitles(urllib.quote(subs, safe=":/"));print 'meti legendas',subs
	while player.playing:
		xbmc.sleep(1000)
		player.track_time()

class Player(xbmc.Player):
    def __init__(self,url,season,episode):
        xbmc.Player.__init__(self)
        self.url=url
        self.season=season
        self.episode=episode
        self.playing = True
        self.time = 0
        self.totalTime = 0
        print 'player criado'
	print 'verificar definicao do trakt'
	try:
		addon_id_trakt = 'script.trakt'
		trakt_addon = xbmcaddon.Addon(id=addon_id_trakt)
		trakt_instalado = True
	except: trakt_instalado = False
	if trakt_instalado == True:
		save(os.path.join(datapath,'trakt.txt'),trakt_addon.getSetting('rate_movie'))
		if trakt_addon.getSetting('rate_movie') == 'true': xbmcaddon.Addon(id='script.trakt').setSetting('rate_movie',"false")

    def onPlayBackStarted(self):
        print 'player Start'
        self.totalTime = self.getTotalTime()

    def onPlayBackStopped(self):
        print 'player Stop'
        self.playing = False
        time = int(self.time)
        print 'self.time/self.totalTime='+str(self.time/self.totalTime)
        if (self.time/self.totalTime > 0.90): 
		adicionar_visto(url,season=season,episode=episode)
		try:
			definition_trakt = readfile(os.path.join(datapath,'trakt.txt'))
			xbmcaddon.Addon(id='script.trakt').setSetting('rate_movie',definition_trakt)
		except: pass
		if selfAddon.getSetting('votar-stopped')=='true':
			try:
				if season: pass
				else: votar_ratotv()
			except: votar_ratotv()
		else:
			try:
				definition_trakt = readfile(os.path.join(datapath,'trakt.txt'))
				xbmcaddon.Addon(id='script.trakt').setSetting('rate_movie',definition_trakt)
			except: pass

    def onPlayBackEnded(self):
        self.onPlayBackStopped()

    def track_time(self):
        try: self.time = self.getTime()
        except: pass



def pesquisa(url):
    keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa')
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        encode=urllib.quote(search)
        url_pesquisa = base_url + '?do=search&subaction=search&search_start=1&story=' + str(encode)
	print url_pesquisa
	listar_pesquisa(urllib.quote_plus(url_pesquisa))

def pesquisa_ano(url):
    keyb = xbmc.Keyboard('', 'Escreva o ano')
    keyb.doModal()
    if (keyb.isConfirmed()):
        search = keyb.getText()
        encode=urllib.quote(search)
	try:
		int(encode)
		inteiro = True
	except:
		inteiro = False
		ok=mensagemok('RatoTV','Por favor coloque um valor inteiro!')
	if inteiro:
        	url_pesquisa = base_url + 'tags/' + str(encode) + '/page/1/'
		print url_pesquisa
		listar_pesquisa(urllib.quote_plus(url_pesquisa))
	else: sys.exit(0)

def filmes_homepage(name,url):
	try: html_source = abrir_url(url)
	except: ok=mensagemok('RatoTV','Não foi possível abrir a página. Tente novamente ou contacte um dos administradores do site.');sys.exit(0)
	if name == 'Filmes mais vistos':
		pasta = False
		mode = 3
		html_source_trunk = re.findall('<div id="viewed">(.*?)<div id="rated">', html_source, re.DOTALL)
	elif name == 'Filmes mais populares':
		pasta = False
		mode = 3
		html_source_trunk = re.findall('<div id="popular">(.*?)<div id="viewed">', html_source, re.DOTALL)
	elif name == 'Filmes mais recentes':
		pasta = False
		mode = 3
		html_source_trunk = re.findall('<div id="new"(.*?)<div id="popular">', html_source, re.DOTALL)
	elif name == 'Filmes mais votados':
		pasta = False
		mode = 3
		html_source_trunk = re.findall('<div id="rated">(.*?)</div></div>', html_source, re.DOTALL)
	elif name == 'Séries mais vistas':
		pasta = True
		mode = 10
		html_source_trunk = re.findall('<div id="viewed2">(.*?)<div id="rated2">', html_source, re.DOTALL)
	elif name == 'Séries mais populares':
		pasta = True
		mode = 10
		html_source_trunk = re.findall('<div id="popular2">(.*?)<div id="viewed2">', html_source, re.DOTALL)
	elif name == 'Séries mais recentes':
		pasta = True
		mode = 10
		html_source_trunk = re.findall('<div id="new2">(.*?)<div id="popular2">', html_source, re.DOTALL)
	elif name == 'Séries mais votadas':
		pasta = True
		mode = 10
		html_source_trunk = re.findall('<div id="rated2">(.*?)</div></div>', html_source, re.DOTALL)
	if html_source:
		match = re.compile('<img src="(.+?)" alt=".+?"/><span>(.+?)</span><a href="(.+?)"').findall(html_source_trunk[0])
		totalit = len(match)
		progresso.create('RatoTV', 'A obter metadata... ')
		progresso.update(0,'A obter metadata...')
		i=0
		for img,titulo,url in match:
			progresso.update(int(i/float(totalit)*100),'A obter metadata...',titulo)
			id_rato = re.compile('.*/(.+?)-.+?html').findall(url)
			userdata_folder = os.path.join(datapath,"media_database")
			txt_file = os.path.join(userdata_folder,id_rato[0] + '.txt')
			if xbmcvfs.exists(txt_file):
				data = readfile(txt_file).split('|')
				name = data[0]
				url = data[1]
				iconimage = data[3]
				infolabels = eval(data[2])
				fanart = urllib.unquote(data[4])
				filme_ou_serie = data[5]
				HD = eval(data[6])
				favorito = eval(data[7])			
			else:
				infolabels,name,url,iconimage,fanart,filme_ou_serie,HD,favorito = obter_info_url(url,True)
			i += 1
			addDir_filme(name + ' (' + str(infolabels["Year"]) + ')',url,mode,iconimage,infolabels,fanart,totalit,pasta,filme_ou_serie,HD,favorito)
		progresso.close()
	moviesandseries_view()
	
#Funcao para devolver informaçao de um filme/serie dado o url
def obter_info_url(url,salvar=False):
	codigo_fonte = post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
	html_source_trunk = re.findall('<div class="shortpost(.*?)Reportar</a></li>', codigo_fonte, re.DOTALL)
	if html_source_trunk:
		infolabels,name,url,iconimage,fanart,filme_ou_serie,HD,favorito = rato_tv_get_media_info(html_source_trunk[0])
		if salvar:
			id_rato = re.compile('.*/(.+?)-.+?html').findall(url)
			userdata_folder = os.path.join(datapath,"media_database")
			if not xbmcvfs.exists(userdata_folder):
				xbmcvfs.mkdir(userdata_folder)
			txt_file = os.path.join(userdata_folder,id_rato[0] + '.txt')
			save(txt_file, name + '|' + url + '|'+str(infolabels)+'|' + iconimage + '|'  + urllib.quote(fanart) + '|' + filme_ou_serie +'|'+str(HD)+'|' + str(favorito))
		return infolabels,name,url,iconimage,fanart,filme_ou_serie,HD,favorito
		
#funcao para limpar metadata
def limpar_pasta_metadata():
	userdata_folder = os.path.join(datapath,"media_database")
	if xbmcvfs.exists(userdata_folder):
		dirs, files = xbmcvfs.listdir(folder)
		for ficheiro in files:
			xbmcvfs.delete(os.path.join(userdata_folder,ficheiro))
		selfAddon.setSetting(setting_limpar_metadata,"false")
	return

def listar_media(url,mode):
    try:
        html_source=post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
        html_source_trunk = re.findall('<div class="shortpost">(.*?)<\/div>\n<\/div>\n<\/div>', html_source, re.DOTALL)
    except:
        ok=mensagemok('RatoTV','Não foi possível abrir a página. Tente novamente ou contacte um dos administradores do site.')
        return
    #print html_source_trunk
    current_page = re.compile('cstart=(.+?)&').findall(url)
    if current_page == []: current_page= re.compile('/page/(.+?)/').findall(url)
    pag_seguinte = re.compile('<div class="next"><a href="(.+?)">').findall(html_source)
    total_paginas = re.compile('.*<a href=".+?">(.+?)</a>\n<div class="next">').findall(html_source)
    if total_paginas == []: total_paginas=re.compile('.*/page/(.+?)/">(.+?)</a> ').findall(html_source)
    totalit = len(html_source_trunk)
    print "numero total de items:" + str(totalit)
    for html_trunk in html_source_trunk:
        try:
            infolabels,name,url,iconimage,fanart,filme_ou_serie,HD,favorito = rato_tv_get_media_info(html_trunk)
            #print "fanart",fanart
            if filme_ou_serie == 'movie': addDir_filme(name + ' ('+infolabels['Year']+')',url,3,iconimage,infolabels,fanart,totalit,False,'movie',HD,favorito)
            elif filme_ou_serie == 'tvshow': addDir_filme(name + ' ('+infolabels['Year']+')',url,10,iconimage,infolabels,fanart,totalit,True,'tvshow',HD,favorito)
        except: pass    	
    print "pagina seguinte",pag_seguinte,"pagina actual",current_page,"total",total_paginas
    try:
        print type(total_paginas[0])
        addDir_reg_menu('[COLOR green]Pag (' + current_page[0] + '/' + total_paginas[0]+ ') | Próxima >>>[/COLOR]',pag_seguinte[0].replace('amp;',''),mode,artfolder+'seta.jpg',True)
    except:
        try: addDir_reg_menu('[COLOR green]Pag (' + current_page[0] + '/' + total_paginas[0][0]+ ') | Próxima >>>[/COLOR]',pag_seguinte[0].replace('amp;',''),mode,artfolder+'seta.jpg',True)
        except:pass
    moviesandseries_view()

def listar_pesquisa(url):
	URLpesquisa = urllib.unquote(url)
	encode = True
	try:
		html_source = post_page(urllib.unquote(url),selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
		html_source_trunk = re.findall('<div class="shortpost">(.*?)<\/div>\n<\/div>\n<\/div>', html_source, re.DOTALL)
		print len(html_source_trunk)
	except:
		ok=mensagemok('RatoTV','Não foi possível abrir a página. Tente novamente ou contacte um dos administradores do site.')
		sys.exit(0)
	current_page = re.compile('id="search_start" value="(.+?)"').findall(html_source)
	if not current_page:
		current_page = [ url.split('/')[-2] ]
		encode = False
	paginas = re.compile('<a.+?list_submit\((.+?)\);').findall(html_source)
	if not paginas:
		paginas = []
		paginas_check = re.compile('href=".+?/page/(.+?)/">(.+?)</a>').findall(html_source)
		for pagurl,paga in paginas_check:
			if pagurl == paga: paginas.append(paga)
	totalit = len(html_source_trunk)
 	if totalit != 0:
		for html_trunk in html_source_trunk:
			try:
				infolabels,name,url,iconimage,fanart,filme_ou_serie,HD,favorito = rato_tv_get_media_info(html_trunk)
				if filme_ou_serie == 'movie': addDir_filme(name + ' ('+str(infolabels['Year'])+')',url,3,iconimage,infolabels,fanart,totalit,False,'movie',HD,favorito)
				elif filme_ou_serie == 'tvshow': addDir_filme(name + ' ('+str(infolabels['Year'])+')',url,10,iconimage,infolabels,fanart,totalit,True,'tvshow',HD,favorito)
			except:pass
		try:
			total_paginas = max(paginas)
			pag_seguinte = paginas[-1]
			if encode: pagina_seguinte = re.sub('search_start=[0-9]+','search_start='+pag_seguinte[0],URLpesquisa).replace('amp;','')
			else: pagina_seguinte = URLpesquisa.replace('/'+current_page[0]+'/','/' + str(int(current_page[0])+1)+'/')
			if int(pag_seguinte) > int(current_page[0]): addDir_reg_menu('[COLOR green]Pag (' + current_page[0] + '/' + total_paginas + ') | Próxima >>>[/COLOR]',pagina_seguinte,16,artfolder+'seta.jpg',True)
			else:pass
		except: pass
		moviesandseries_view()
	else:
		ok=mensagemok('RatoTV','Não existem resultados.')
		sys.exit(0)

def rato_tv_get_media_info(html_trunk):
    print "get media info"
    data_dict = dict([('code',''),('Count', ''),('Title', ''), ('Year', ''),('Rating', ''),('Genre', ''),('Director', ''),('Cast', list()),('Plot', ''),('Trailer', '')])
    match = re.compile('href="(.+?)".+?<img src="(.+?)" alt="(.+?)" />').findall(html_trunk)
    for url_newsid,iconimage,name in match:
	print "Dados obtidos para o item:",url_newsid,iconimage,name
        if iconimage.find('http://') == -1: thumbnail = base_url + iconimage
        else: thumbnail = iconimage
        data_dict['Title'] = name;url = url_newsid
    match = []
    if match == []:
        match = re.compile('href="(.+?)" >(.+?)</a></h3>\n.+?<span class="favorite">.*?</span>\n.+?</div>\n.+?<div class="poster" style=".+?">\n.+?\n.+?img src="(.+?)"').findall(html_trunk)
        for url_newsid,name,iconimage in match:
            if iconimage.find('http://') == -1: thumbnail = base_url + iconimage
            else: thumbnail = iconimage
            data_dict['Title'] = name;url = url_newsid
    else:pass
    match = re.compile('<strong>Título Original: </strong>(.+?)</li>').findall(html_trunk)
    if match != []: titulo_original=match[0]; data_dict['originaltitle']=match[0]
    else: titulo_original = ''
    match = re.compile('<strong>IMDB: </strong><a href="http://www.imdb.com/title/(.+?)/"').findall(html_trunk)
    if match != []:data_dict['code'] = match[0]
    else: data_dict['code'] = ''
    match = re.compile('<strong>Diretor:</strong>.+?>(.+?)</a>').findall(html_trunk)
    for director in match:
        data_dict['Director'] = director
    match = re.compile('rating=(.+?)&votes').findall(html_trunk)
    if match:
        print "Found rating"
        for score in match:
            data_dict['Rating'] = float(score.replace(',','.').replace('<div class="rating1">','').replace('<span>','').replace('</span>','').replace('</div>',''))
    else:
        print "Rating not found"
        match=re.compile('<strong>Pontuação:.+?</strong>(.+?)</li>').findall(html_trunk)
        for score in match:
            data_dict['Rating'] = float(score.replace(',','.').replace('<div class="rating1">','').replace('<span>','').replace('</span>','').replace('</div>',''))
    print "Rating é:",match
    match = re.compile('<a href="http://www.ratotv.net/.+?">(.+?)</a></li>').findall(html_trunk)
    print "Filme ou Série",match
    for categoria in match:
        if categoria == 'Filmes': filme_ou_serie = 'movie'
        elif categoria == 'Séries': filme_ou_serie = 'tvshow'
    match = re.compile('<div id=".+?" style="display:inline;">(.+?)</div>').findall(html_trunk)
    for plot in match:
        try:
            data_dict['Plot'] = h.unescape(plot)
        except: data_dict['Plot'] = 'N/A'
    match = re.compile('<strong>Ano: </strong><a href="(.+?)/tags/(.+?)">(.+?)</a></li>').findall(html_trunk)
    if match:
	data_dict['Year'] = match[0][2]
    else:
    	match = re.compile('<strong>Ano: </strong>(.+?)</li>').findall(html_trunk)
    	for year in match:
        	data_dict['Year'] = year
    match = re.compile('<strong>Atores: </strong>(.+?)</li>').findall(html_trunk)
    if match:
        actor = match[0].replace(" ","").split(",")
        data_dict['Cast'] = actor
    match = re.compile('<strong>Gênero:</strong>(.+?)</li>').findall(html_trunk)
    if match:
        lista_de_genero = match[0].replace(" ","").split(",")
        for genre in lista_de_genero:
            data_dict['Genre'] += genre + ' '
    match = re.compile('<a href="http://www.ratotv.net/xfsearch/.D/">(.D)</a>').findall(html_trunk)
    HD = None
    if match:
        if match[0] == 'HD': HD = True
        elif match[0] == 'SD': HD = False
	else: HD = match[0]
    match = re.compile('<span class="favorite">.+?href="(.+?)"').findall(html_trunk)
    favorito = False
    if match:
        if 'doaction=del' in match[0]: favorito = True
    if filme_ou_serie == 'movie':
        if selfAddon.getSetting('movie-fanart') == 'true' and selfAddon.getSetting('movie-trailer') == 'true':
            fanart,data_dict['Count'] = themoviedb_api().fanart_and_id(titulo_original,data_dict['Year'])
            data_dict['Trailer'] = themoviedb_api().trailer(data_dict['Count'])
        elif selfAddon.getSetting('movie-fanart') == 'true' and selfAddon.getSetting('movie-trailer') == 'false':
            fanart = themoviedb_api().fanart_and_id(titulo_original,data_dict['Year'])[0]
        elif selfAddon.getSetting('movie-fanart') == 'false' and selfAddon.getSetting('movie-trailer') == 'true':
            data_dict['Count'] = themoviedb_api().fanart_and_id(titulo_original,data_dict['Year'])[1]
            data_dict['Trailer'] = themoviedb_api().trailer(data_dict['Count'])
            fanart = fanart_rato_tv
        else:
            fanart = fanart_rato_tv
    elif filme_ou_serie == 'tvshow':
        if selfAddon.getSetting('series-fanart') == 'true':
            data_dict['Count'] = thetvdb_api()._id(titulo_original,data_dict['Year'])
            fanart = thetvdb_api().fanart(data_dict['Count'])
        else:
            fanart = fanart_rato_tv
    if name == '{title}': data_dict['Title'] = data_dict['originaltitle']
    return data_dict,data_dict['Title'],url,thumbnail,fanart,filme_ou_serie,HD,favorito

def series_seasons_get_dictionary(url,name,fanart):
	try: html_source=post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
	except: ok=mensagemok('RatoTV','Não foi possível abrir a página. Tente novamente \n ou contacte um dos administradores do site.'); match = ''
	try:
		#verificar se originaltitle e year estao definidos
		print originaltitle,year
		original_year = True
	except: original_year = False
	if not original_year:
		originaltitle=re.compile('<strong>Título Original: </strong>(.+?)</li>').findall(html_source)[0]
		year = re.compile('<strong>Ano: </strong><a href=".+?">(.+?)</a>').findall(html_source)[0]
	if selfAddon.getSetting('series-season-poster') == 'true':
		id_tvdb = thetvdb_api()._id(originaltitle,year)
		json_code = trakt_api().shows_seasons(id_tvdb)
	serie_dict_temporadas = {}
	match = re.compile('data-list="(.+?)" data-sid=".+?".+?Temporada (.+?) ').findall(html_source)
	for rss,temporada in match:
		if "http://" not in rss:
			rss=base_url + rss
		serie_dict_temporadas[temporada] = []
		serie_dict_temporadas[temporada].append(rss)
        match = re.findall('<object id="flashplayer(.+?)".*?"FlashVars".+?proxy.list=(.+?)&', html_source, re.DOTALL)
	for temporada,rss in match:
		try: serie_dict_temporadas[temporada].append(rss)
		except: serie_dict_temporadas[temporada] = [rss]
	return iconimage,originaltitle,year,serie_dict_temporadas

def series_seasons(url,name,fanart):
	iconimage,originaltitle,year,serie_dict_temporadas = series_seasons_get_dictionary(url,name,fanart)
	for season in sorted(serie_dict_temporadas.iterkeys(),key=int):
		if selfAddon.getSetting('series-season-poster') == 'true':
			try:
				for key in json_code:
					if str(key['season']) == str(season):
						try: iconimage = key['images']['poster']
						except: pass
				addDir_temporada("[B][COLOR green]Temporada[/B][/COLOR] " + str(season),url,str(serie_dict_temporadas),39,iconimage,True,fanart)
			except: addDir_temporada("[B][COLOR green]Temporada[/B][/COLOR] " + str(season),url,str(serie_dict_temporadas),39,iconimage,True,fanart)
		else: addDir_temporada("[B][COLOR green]Temporada[/B][/COLOR] " + str(season),url,str(serie_dict_temporadas),39,iconimage,True,fanart)

###################################################################################
#FUNCOES AUXILIARES                                                               #
###################################################################################

def download_qualidade(url,name,iconimage):
	try:
		print urllib.unquote_plus(params["tipo"])
		tipo = "movie"
	except: tipo = "tvshow"
	if tipo == "movie":
		titles = []; url_movie_file=[]
		try:
			html_source=post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
		except: ok=mensagemok('RatoTV','Não foi possível abrir a página. Tente novamente \n ou contacte um dos administradores do site.');html_source =""
		opcao,rssopcao = rssnumber(html_source)
		num_opcoes = len(opcao)
		if num_opcoes == 1: opcao = "1"
		elif num_opcoes == 2:
			janela2qualidades()
			opcao = readfile(datapath + "option.txt")
		elif num_opcoes == 3:
			janela3qualidades()
			opcao = readfile(datapath + "option.txt")
		else: ok=mensagemok('RatoTV','Ocorreu um erro. Tente novamente.')
		if opcao == "1":
			try:
				rss_source = abrir_url(urllib.quote(rssopcao[0], safe=":/"))
			except: ok=mensagemok('RatoTV','Não foi possível abrir o feed da opção 1')
			try:
	        		match = re.compile('<jwplayer:source file="(.+?)" label="(.+?)" />').findall(rss_source)
	        		for movie_file,quality in match:
	            			titles.append('[B]' + quality + '[/B]')
	            			url_movie_file.append(movie_file)
	    		except: ok=mensagemok('RatoTV','Não foi possível abrir a página. Tente novamente ou contacte um dos administradores do site.')
	    		try:
	        		subs = re.compile('<jwplayer:track file="../(.+?)" label=".+?').findall(rss_source)
	        		if len(subs) >= 1: subs = base_url + str(subs[0])
	        		else: subs = ''
	    		except: subs = ''
	   		print titles,url_movie_file,subs
	    		if selfAddon.getSetting('qualidade-auto') == "false":
	        		choose=escolher_qualidade('Seleccione a qualidade',titles)
	       			if choose > -1: linkescolha=downloader_rato(url_movie_file[choose],subs,name,url,iconimage,'',None,None)
	    		else: linkescolha=downloader_rato(url_movie_file[0],subs,name,url,iconimage,'',None,None)
		else:
			try:
				rss_escolhido = int(opcao)-1;print rss_escolhido
				rss_source = abrir_url(urllib.quote(rssopcao[rss_escolhido], safe=":/"))
			except: ok=mensagemok('RatoTV','Não foi possível abrir o feed da opção 1')
			print rss_source
			if rss_source: hash_movie = re.compile('<location>ratotv*(.+?)</location>').findall(rss_source)[0].replace("*","")
			else: ok=mensagemok('RatoTV','Não conseguiu obter a hash.')
			try: decoded_url = resolver_externos(hash_movie)
			except: ok=mensagemok('RatoTV','Não conseguiu resolver a hash.')
			try:
        			subs = re.compile('<captions.files>../(.+?)</captions.files>').findall(rss_source)
        			if len(subs) >= 1: subs = base_url + str(subs[0])
        			else: subs = ''
    			except: subs = ''
			print subs
			downloader_rato(decoded_url,subs,name,url,iconimage,'',None,None)
	elif tipo == "tvshow": pass

def downloader_rato(video,subs,name,url,iconimage,infolabels,season,episode):
	print subs,video
	progresso.create('Downloader RatoTV', name ,'A obter resposta do servidor...Aguarde.')
	file_name = video.split('/')[-1]
	print "estou aqui"
	if "ratotv" in video:
		print "server do rato"
		request = urllib2.Request(video, headers={"Host" : "ratotv.com","Referer":url})
	else: request = urllib2.Request(video)
	try:
		if episode:
			print "here"
			u = urllib2.urlopen(request,timeout=1000)
			if os.path.exists(ADDON.getSetting('folder') + 'series/'): pass
			else: os.mkdir( ADDON.getSetting('folder') + 'series/' , 0777 );
			folder_name_serie = ADDON.getSetting('folder') + 'series/' + name.replace(':','')
			if os.path.exists(folder_name_serie): pass
			else: os.mkdir( folder_name_serie , 0777 );
			folder_name_serie_temporada = folder_name_serie + "/Season" + str(season)
			if os.path.exists(folder_name_serie_temporada): pass
			else: os.mkdir( folder_name_serie_temporada , 0777 );
			folder_name = folder_name_serie_temporada + '/' + name.replace(':','') + "-Season" + str(season) + "Episode" + str(episode)
			if os.path.exists(folder_name): pass
			else: os.mkdir( folder_name , 0777 );
		else:
			u = urllib2.urlopen(request,timeout=1000)
			if os.path.exists(ADDON.getSetting('folder') + 'filmes/'): pass
			else: os.mkdir( ADDON.getSetting('folder') + 'filmes/' , 0777 );
			folder_name = ADDON.getSetting('folder') + 'filmes/' + name.replace(':','')
			if os.path.exists(folder_name): pass
			else: os.mkdir( folder_name , 0777 );
		legenda = abrir_url(urllib.quote(subs, safe=":/"))
		legenda_filename = subs.split('/')[-1]
		f = open(folder_name + '/' + legenda_filename, 'wb')
		f.write(legenda)
		f.close()
		f = open(folder_name + '/' + file_name, 'wb')
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		file_size_dl = 0
		block_sz = 8192
		while True:
			if progresso.iscanceled() == 0:
				buffer = u.read(block_sz)
				if not buffer:
 					break
					progresso.close()
					print "Parei"
				file_size_dl += len(buffer)
				f.write(buffer)
				progresso.update(int(file_size_dl * 100. / file_size),name,"Downloading...")
			elif progresso.iscanceled() == 1:
				f.close()
				progresso.close()
				print "Downloader dialog fechada"
				break
		f.close()
		progresso.close()
		print "Parei fim de ciclo"
	except:
		progresso.close()
		mensagemok('RatoTV','Não conseguiu obter resposta do servidor. Servers sobrecarregados.')

def check_login():
    if selfAddon.getSetting('login_name') == '' or selfAddon.getSetting('login_password') == '':
        mensagemok('RatoTV','Precisa de definir o seu username e password')
        resultado = False
        return resultado
    else:
        try:
            html_source=post_page(base_url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
            match = re.compile('&user=(.+?)">Perfil').findall(html_source)
        except:
            resultado = False
            mensagemok('RatoTV','Não foi possível abrir a página. Tente novamente \n ou contacte um dos administradores do site.')
            match = ''
            return resultado
            print match
        if match == []:
            match = re.compile('href="http://www.ratotv.net/user/(.+?)/">Perfil').findall(html_source)
            print match
            if match == []:
                    resultado=False
                    mensagemok('RatoTV','Username e/ou Password incorrectos.')
                    return resultado
            else:
                    resultado = True
                    xbmc.executebuiltin("XBMC.Notification(RatoTv," + selfAddon.getSetting('login_name') + " -Sessão iniciada!,'10000',"+addonfolder+"/icon.png)")
                    return resultado
        else:
            resultado = True
            xbmc.executebuiltin("XBMC.Notification(RatoTv," + selfAddon.getSetting('login_name') + " -Sessão iniciada!,'10000',"+addonfolder+"/icon.png)")
            return resultado

def menu_view():
    setting = selfAddon.getSetting('menu-view')
    if setting =="0": xbmc.executebuiltin("Container.SetViewMode(50)")
    elif setting =="1": xbmc.executebuiltin("Container.SetViewMode(51)")
    return

def moviesandseries_view():
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    setting = selfAddon.getSetting('moviesandseries-view')
    if setting == "0": xbmc.executebuiltin("Container.SetViewMode(50)")
    elif setting == "1": xbmc.executebuiltin("Container.SetViewMode(51)")
    elif setting == "2": xbmc.executebuiltin("Container.SetViewMode(500)")
    elif setting == "3": xbmc.executebuiltin("Container.SetViewMode(501)")
    elif setting == "4": xbmc.executebuiltin("Container.SetViewMode(508)")
    elif setting == "5": xbmc.executebuiltin("Container.SetViewMode(504)")
    elif setting == "6": xbmc.executebuiltin("Container.SetViewMode(503)")
    elif setting == "7": xbmc.executebuiltin("Container.SetViewMode(515)")
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    return

def pedidos_view():
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    setting = selfAddon.getSetting('pedidos-view')
    if setting == "0": xbmc.executebuiltin("Container.SetViewMode(50)")
    elif setting == "1": xbmc.executebuiltin("Container.SetViewMode(51)")
    elif setting == "2": xbmc.executebuiltin("Container.SetViewMode(500)")
    elif setting == "3": xbmc.executebuiltin("Container.SetViewMode(501)")
    elif setting == "4": xbmc.executebuiltin("Container.SetViewMode(508)")
    elif setting == "5": xbmc.executebuiltin("Container.SetViewMode(504)")
    elif setting == "6": xbmc.executebuiltin("Container.SetViewMode(503)")
    elif setting == "7": xbmc.executebuiltin("Container.SetViewMode(515)")
    xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
    return

def episodes_view():
    setting = selfAddon.getSetting('episodes-view')
    if setting =="0": xbmc.executebuiltin("Container.SetViewMode(50)")
    elif setting =="1": xbmc.executebuiltin("Container.SetViewMode(51)")
    if setting =="2": xbmc.executebuiltin("Container.SetViewMode(500)")
    return

def comment(url):
    post_id = re.compile('.*/(.+?)-').findall(url)
    if post_id == [] or len(post_id) != 1 : mensagemok('RatoTV','Ocorreu um erro a determinar correctamente o ID do post. Informe os administradores.')
    else:
        print post_id
        print 'urlcomment',url
        keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa')
        keyb.doModal()
        if (keyb.isConfirmed()):
            comentario = keyb.getText()
            if comentario == '': return mensagemok('RatoTV','Não escreveu nenhum comentário.')
            else:
                comentario += "\n.:.Comentário enviado do XBMC.:."
                mydata=[('login_name',selfAddon.getSetting('login_name')),('login_password',selfAddon.getSetting('login_password')),('login','submit'),('subaction','addcomment'),('name',selfAddon.getSetting('login_name')),('post_id',post_id[0]),('comments',comentario)]
                mydata=urllib.urlencode(mydata)
                req=urllib2.Request(url, mydata)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                req.add_header("Content-type", "application/x-www-form-urlencoded")
                req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
                page=urllib2.urlopen(req).read()
                return mensagemok('RatoTV','Comentário enviado com sucesso.')

def ler_comentarios(url,todos_os_comentarios):
    print url
    try:
        html_source=post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
        match=re.findall('<div id=\'comment-id(.*?)<div class="lst-itm">', html_source, re.DOTALL)
    except: match = []
    if match == []: return mensagemok('RatoTV','Não existem comentários ao filme.')
    else:
        for comentario in match:
            autor = re.compile('href="http://www.ratotv.net/user/.+?">(.+?)</a>').findall(comentario)
            data = re.compile('<h5>(.+?)</h5>').findall(comentario)
            texto = re.findall("<div id=\'comm-id.+?\'>(.*?)</div>", comentario, re.DOTALL)
            texto = texto[0].replace('<br />','')
            quote = re.compile('<!--QuoteBegin(.+?)<!--QuoteEBegin-->').findall(texto)
            for quo in quote: texto = texto.replace(quo,'')
            quote = re.compile('<!--QuoteBegin<!--QuoteEBegin-->(.+?)<!--QuoteEnd--></div><!--QuoteEEnd-->').findall(texto)
            for quo in quote: texto = texto.replace(quo,'')
            quote = re.compile('<!--smile:(.+)<!--/smile-->').findall(texto)
            for quo in quote: texto = texto.replace(quo,'')
            quote = re.compile('<span style=(.+)">').findall(texto)
            for quo in quote: texto = texto.replace(quo,'')
            quote = re.compile('<pre>(.+)</pre>').findall(texto)
            for quo in quote: texto = texto.replace(quo,'')
            texto = texto.replace('<pre>','').replace('</pre>','').replace('</span>','').replace('<!--smile:','').replace('<!--/smile-->','').replace('<!--QuoteBegin','').replace('<!--QuoteEBegin-->','').replace('<!--QuoteEnd-->','').replace('</div><!--QuoteEEnd-->','').replace('<b>','').replace('</b>','').replace('&eacute;','').replace('&nbsp;','').replace('<p>','').replace('</p>','').replace('&atilde;','ã').replace('&aacute;','á').replace('&ccedil;','ç')
            todos_os_comentarios = todos_os_comentarios +'[B]' + autor[0] +' em ' + data[0] + '[/B]\n' + texto + '\n-------------------------------------------------------\n\n'
    pag_seguinte = re.compile('href="(.+?)" onclick=".+?">Seguinte</a>').findall(html_source)
    try: ler_comentarios(pag_seguinte[0],todos_os_comentarios)
    except: janela_lateral('Comentários: ',todos_os_comentarios)

def janela_lateral(label,texto):
    xbmc.executebuiltin("ActivateWindow(10147)")
    window = xbmcgui.Window(10147)
    xbmc.sleep(100)
    window.getControl(1).setLabel(label)
    window.getControl(5).setText(texto)

def save(filename,contents):
    fh = open(filename, 'w')
    fh.write(contents)
    fh.close()

def readfile(filename):
	f = open(filename, "r")
	string = f.read()
	return string

def play_trailer(infolabels_trailer):
    print "url trailer é",infolabels_trailer
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(infolabels_trailer)

def votar(url,voto):
	try:
		addon_id_trakt = 'script.trakt'
		trakt_addon = xbmcaddon.Addon(id=addon_id_trakt)
		trakt_instalado = True
	except: trakt_instalado = False
	if trakt_instalado == True:
		if trakt_addon.getSetting('rate_movie') == 'true':
			html_source=post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
        		infolabels,filme_ou_serie = rato_tv_get_media_info(html_source)[0],rato_tv_get_media_info(html_source)[5]
			print infolabels
			data = dict()
			try:
				data["username"] = trakt_addon.getSetting('username')
				data["password"] = trakt_addon.getSetting('password')
				trakt_login_check = True
			except: trakt_login_check = False
			if trakt_login_check == True:
				try: data['imdb_id'] = infolabels['code']
				except: pass
				try: data['title'] = infolabels['originaltitle']
				except: pass
				try: data['year'] = infolabels['Year']
				except: pass
				try: data['rating'] = voto
				except: pass
				print data
				if filme_ou_serie == 'movie': url_json_post="http://api.trakt.tv/rate/movie/353f223c2afc3c2050fcb810810fdb49"
				elif filme_ou_serie == 'tvshow': url_json_post="http://api.trakt.tv/rate/show/353f223c2afc3c2050fcb810810fdb49"
				try: json_post(data,url_json_post)
				except: print "Não conseguiu enviar rate para o trakt"
			else:pass
		else: pass
	try:
		id_ratotv = re.compile('.*/(.+?)-.+?html').findall(url)
		urlfinal= base_url + 'engine/ajax/rating.php?go_rate=' + voto + '&news_id=' + id_ratotv[0]
		print 'Voto:',urlfinal
		post_page(urlfinal,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
		return xbmc.executebuiltin("XBMC.Notification(RatoTv,Obrigado pelo seu voto!,'10000',"+addonfolder+"/icon.png)")
	except: return mensagemok('RatoTV','Não foi possível votar. Tente mais tarde.')

def reportar(url):
	id_ratotv = re.compile('.*/(.+?)-.+?html').findall(url)
	if id_ratotv == [] or len(id_ratotv) != 1 : mensagemok('RatoTV','Ocorreu um erro a determinar correctamente o ID do post. Informe os administradores.')
	else:
		yes= xbmcgui.Dialog().yesno("RatoTv", 'Pretende escolher um dos problemas comuns (pré-definidos)?')
		if yes:
			label = ['Episódios em falta','Qualidade fraca','Filme incompleto','Sem som','Filme não toca','Qualidade não corresponde ao anunciado','Legendas não estão sincronizadas','Sem legendas']; text = ['A série apresenta episódios em falta','O filme/série tem qualidade fraca','Não consegui reproduzir o filme até ao fim. Encontra-se incompleto','O filme/série não tem som','Não consegui reproduzir o filme','A qualidade do filme/série não corresponde à label anunciada.','As legendas do filme/série não estão sincronizadas','Existem vídeos sem legendas']
			choose=escolher_qualidade('Seleccione de entre a lista de problemas',label)
			try:
	        		if choose > -1:
							try:
								url= base_url + 'engine/ajax/complaint.php'
								mydata=[('login_name',selfAddon.getSetting('login_name')),('login_password',selfAddon.getSetting('login_password')),('login','submit'),('id',str(id_ratotv[0])),('action','news'),('text',urllib.unquote_plus(text[choose]))]
								post_page_free(url,mydata)
								mensagemok('RatoTV','Problema reportado com sucesso.')
							except: mensagemok('RatoTV','Ocorreu um problema')
			except: pass
		else:
				keyb = xbmc.Keyboard('RatoTv', 'Reporte o problema encontrado')
				keyb.doModal()
				if (keyb.isConfirmed()):
					comentario = keyb.getText()
					if comentario == '': return mensagemok('','Não escreveu texto.')
					else:
						try:
							url= base_url + 'engine/ajax/complaint.php'
							mydata=[('login_name',selfAddon.getSetting('login_name')),('login_password',selfAddon.getSetting('login_password')),('login','submit'),('id',str(id_ratotv[0])),('action','news'),('text',urllib.unquote_plus(comentario))]
							post_page_free(url,mydata)
							return mensagemok('RatoTV','Problema reportado com sucesso.')
						except: return mensagemok('RatoTV','Ocorreu um problema.')

def mensagem_site(html_source):
    try:
        match = re.compile("'(.+?)'").findall(html_source)
	print match
    except: match = []
    if match != [] and selfAddon.getSetting('mensagem-site') == "true":
	from random import randint
	randomvalue = randint(0,len(match)-1)
        return mensagemok('RatoTV',match[randomvalue])

def get_last_sep(url):
	try: html_source=post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
	except: html_source = ''
	match = re.compile('data-list="(.+?)".+?Temporada (.+?) ').findall(html_source)
	if match:
		last_season_rss = match[-1][0]
		last_season_num = match[-1][-1]
		if "http://" not in last_season_rss: last_season_rss= base_url + last_season_rss
		try:
			rss_source = abrir_url(last_season_rss)
			match = re.compile('<title>.+? (.+?)</title>').findall(rss_source)
			last_available_episode= match[-1]
			return last_season_num,last_available_episode
		except: return ''

def proximo_episodio(url):
	print 'A abrir url...',url
	try: html_source=post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
	except: html_source = ''
	match = re.compile('<strong>Título Original: </strong>(.+?)</li>').findall(html_source)
	if match != []: titulo_original=match[0]
	else: titulo_original = ''
	match = re.compile('<strong>Ano: </strong><a href=".+?">(.+?)</a></li>').findall(html_source)
	if match != []: year=match[0]
	else: year = ''
	print "titulooriginaleyear",titulo_original,year
	id_tvdb = thetvdb_api()._id(titulo_original,year)
	print id_tvdb
	data = trakt_api().next_episode(id_tvdb)
	print len(data["seasons"][0]["episodes"])
	episodios_dict= dict()
	i = 0
	while i < len(data["seasons"][0]["episodes"]):
		episodios_dict[i+1] = data["seasons"][0]["episodes"][i]["first_aired_utc"]
		i += 1
	print episodios_dict
	status = data["status"]
	print 'tempo corrente ',int(time.time())
	i=0
	while i < len(episodios_dict):
		if episodios_dict[i+1] < int(time.time()): pass
		else: break
		i += 1
	if status == 'Ended': mensagemok('RatoTV','A série está completa. Não existem mais episódios ','para esta série.')
	else:
		try:
			next_episode = i+1
			channel = data["network"]
			season = len(data["seasons"])
			print channel,season,i+1
			print "ola"
			mensagemok('RatoTV','Próximo episódio: S' + str(season) + 'E' + str(i+1),'A exibir no canal ' + channel + ' no dia: ' + datetime.datetime.fromtimestamp(int(episodios_dict[i+1])).strftime('%Y-%m-%d'))
		except: mensagemok('RatoTV','Não existe informação para o próximo episódio')


def votar_ratotv():
	ui = JANELA_VOTO('RatingDialog.xml',addonfolder,'Default','')
	ui.doModal()
	del ui

def estatisticas_trakt(url):
	try: html_source=post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
	except: html_source= ''
	if html_source:
		try: infolabels,name,url2,iconimage2,fanart2,filme_ou_serie,HD2,favorito2 = rato_tv_get_media_info(html_source)
		except: pass
		if infolabels['code']:
			if filme_ou_serie == 'movie':
				url_api_trakt_now = 'http://api.trakt.tv/movie/watchingnow.json/' + trakt_api().api_key + '/' + infolabels['code']
				url_api_trakt = 'http://api.trakt.tv/movie/summary.json/' + trakt_api().api_key + '/' + infolabels['code'] + '/extended'
			elif filme_ou_serie == 'tvshow':
				if season and episode:
					print 'Episodio mode'
					url_api_trakt_now = 'http://api.trakt.tv/show/episode/watchingnow.json/' + trakt_api().api_key + '/' + infolabels['code'] + '/' + season + '/' + episode
					url_api_trakt = 'http://api.trakt.tv/show/episode/summary.json/' + trakt_api().api_key + '/' + infolabels['code'] + '/' + season + '/' + episode
				else:
					url_api_trakt_now = 'http://api.trakt.tv/show/watchingnow.json/' + trakt_api().api_key + '/' + infolabels['code']
					url_api_trakt = 'http://api.trakt.tv/show/summary.json/' + trakt_api().api_key + '/' + infolabels['code'] + '/extended'
			else: pass
			texto = ''
			try:
				print url_api_trakt_now
				data = json_get(url_api_trakt_now)
				if len(data) > 0:
					texto += str(len(data)) +' utilizadores a ver neste momento\n\n'
				else: texto += 'Ninguém a assistir neste momento \n\n'
			except: pass
			data = json_get(url_api_trakt)
			try: texto += 'Já viram: ' + str(data['stats']['watchers']) + ' pessoas\n\n'
			except: pass
			try: texto += 'Visto: ' + str(data['stats']['plays']) + ' vezes\n\n'
			except: pass
			try: texto += str(data['ratings']['loved']) + ' gostam (' + str(data['ratings']['percentage']) + '%)\n\n'
			except: pass
			try: texto += str(data['ratings']['hated']) + ' não gostam\n\n'
			except: pass
			try: texto += 'Total de votos: ' +  str(data['ratings']['votes']) + '\n\n'
			except: pass
			try: texto += "Check-in's: " + str(data['stats']['checkins']) + '\n\n'
			except: pass
			try:texto += "Na colecção de " + str(data['stats']['collection']) + ' utilizadores' + '\n\n'
			except: pass
			try: texto += 'Já viram: ' + str(data['episode']['stats']['watchers']) + ' pessoas\n\n'
			except: pass
			try: texto += 'Visto: ' + str(data['episode']['stats']['plays']) + ' vezes\n\n'
			except: pass
			try: texto += str(data['episode']['ratings']['loved']) + ' gostam (' + str(data['episode']['ratings']['percentage']) + '%)\n\n'
			except: pass
			try: texto += str(data['episode']['ratings']['hated']) + ' não gostam\n\n'
			except: pass
			try: texto += 'Total de votos: ' +  str(data['episode']['ratings']['votes']) + '\n\n'
			except: pass
			try: texto += "Check-in's: " + str(data['episode']['stats']['checkins']) + '\n\n'
			except: pass
			try:texto += "Na colecção de " + str(data['episode']['stats']['collection']) + ' utilizadores' + '\n\n'
			except: pass
			return janela_lateral('Estatísticas Trakt.tv: ',texto)
		else: pass
	else:pass


#class 2 qualidades
def janela2qualidades(prioridade=None):
	if selfAddon.getSetting('fonte-auto') == "false":
		ui = qualidades_duas('2qualidades.xml',addonfolder,'Default','')
		ui.doModal()
		del ui
		return
	else:
		if prioridade == "":
			try: save(datapath + "option.txt","")
			except:
				try:
					os.mkdir( datapath , 0777 )
					save(datapath + "option.txt","")
				except: pass
			if selfAddon.getSetting('host1') == "Opção 1": save(datapath + "option.txt","1")
			if selfAddon.getSetting('host1') == "Opção 2" or selfAddon.getSetting('host1') == "Opção 3": save(datapath + "option.txt","2")			
			return
		if prioridade == "1":
			try: save(datapath + "option.txt","")
			except:
				try:
					os.mkdir( datapath , 0777 )
					save(datapath + "option.txt","")
				except: pass
			if selfAddon.getSetting('host2') == "Opção 1": save(datapath + "option.txt","1")
			if selfAddon.getSetting('host2') == "Opção 2" or selfAddon.getSetting('host2') == "Opção 3": save(datapath + "option.txt","2")			
			return
		if prioridade == "2":
			try: save(datapath + "option.txt","")
			except:
				try:
					os.mkdir( datapath , 0777 )
					save(datapath + "option.txt","")
				except: pass
			if selfAddon.getSetting('host3') == "Opção 1": save(datapath + "option.txt","1")
			if selfAddon.getSetting('host3') == "Opção 2" or selfAddon.getSetting('host3') == "Opção 3": save(datapath + "option.txt","2")			
			return
		
class qualidades_duas(xbmcgui.WindowXMLDialog):
    def __init__(self,strXMLname, strFallbackPath, strDefaultName, forceFallback):
	try: save(datapath + "option.txt","")
	except:
		try:
			os.mkdir( datapath , 0777 )
			save(datapath + "option.txt","")
		except: pass

    def onInit(self):
        # Put your List Populating code/ and GUI startup stuff here
        self.getControl(10012).setLabel("Este filme série tem opção 2/3 (provedores externos).")
        self.getControl(10013).setLabel("Por favor escolha esta qualidade em caso de")
        self.getControl(10014).setLabel("sobrecarga dos servidores. Que opção deseja?")
	self.setFocus(self.getControl(11030))

    def onAction(self, action):
	#print action.getId() #importante para saber que acção estou a fazer
    	if action.getId() == 92: self.close()

    def onClick(self, controlID):
        if controlID == 50000: self.close(); save(datapath + "option.txt","10")
	if controlID == 11030: self.close(); save(datapath + "option.txt","1")
        if controlID == 11031: self.close(); save(datapath + "option.txt","2")


#class 3 qualidades
def janela3qualidades(prioridade=None):
	if selfAddon.getSetting('fonte-auto') == "false":
		ui = qualidades('3qualidades.xml',addonfolder,'Default','')
		ui.doModal()
		del ui
		return
	else:
		if prioridade == "":
			try: save(datapath + "option.txt","")
			except:
				try:
					os.mkdir( datapath , 0777 )
					save(datapath + "option.txt","")
				except: pass
			if selfAddon.getSetting('host1') == "Opção 1": save(datapath + "option.txt","1")
			if selfAddon.getSetting('host1') == "Opção 2": save(datapath + "option.txt","2")
			if selfAddon.getSetting('host1') == "Opção 3": save(datapath + "option.txt","3")
			return
		if prioridade == "1":
			try: save(datapath + "option.txt","")
			except:
				try:
					os.mkdir( datapath , 0777 )
					save(datapath + "option.txt","")
				except: pass
			if selfAddon.getSetting('host2') == "Opção 1": save(datapath + "option.txt","1")
			if selfAddon.getSetting('host2') == "Opção 2": save(datapath + "option.txt","2")
			if selfAddon.getSetting('host2') == "Opção 3": save(datapath + "option.txt","3")
			return
		if prioridade == "2":
			try: save(datapath + "option.txt","")
			except:
				try:
					os.mkdir( datapath , 0777 )
					save(datapath + "option.txt","")
				except: pass
			if selfAddon.getSetting('host3') == "Opção 1": save(datapath + "option.txt","1")
			if selfAddon.getSetting('host3') == "Opção 2": save(datapath + "option.txt","2")
			if selfAddon.getSetting('host3') == "Opção 3": save(datapath + "option.txt","3")
			return

class qualidades(xbmcgui.WindowXMLDialog):
    def __init__(self,strXMLname, strFallbackPath, strDefaultName, forceFallback):
	try: save(datapath + "option.txt","")
	except:
		try:
			os.mkdir( datapath , 0777 )
			save(datapath + "option.txt","")
		except: pass

    def onInit(self):
        # Put your List Populating code/ and GUI startup stuff here
        self.getControl(10012).setLabel("Este filme série tem opção 2 e 3 (provedores externos).")
        self.getControl(10013).setLabel("Por favor escolha uma destas duas qualidades em caso de")
        self.getControl(10014).setLabel("sobrecarga dos servidores. Que opção deseja?")
	self.setFocus(self.getControl(11030))

    def onAction(self, action):
	#print action.getId() #importante para saber que acção estou a fazer
    	if action.getId() == 92: self.close()

    def onClick(self, controlID):
        if controlID == 50000: self.close(); save(datapath + "option.txt","10")
	if controlID == 11030: self.close(); save(datapath + "option.txt","1")
        if controlID == 11031: self.close(); save(datapath + "option.txt","2")
        if controlID == 11032: self.close(); save(datapath + "option.txt","3")

#Adapted from Trakt.tv official addon! Thanks
class JANELA_VOTO(xbmcgui.WindowXMLDialog):
    buttons = {11030:1,11031:2,11032:3,11033:4,11034:5,11035:6,11036:7,11037:8,11038:9,11039:10}
    focus_labels = {10030: 1314,10031: 1315,11030: 1315,11031: 1316,11032: 1317,11033: 1318,11034: 1319,11035: 1320,11036: 1321,11037: 1322,11038: 1323,11039: 1314}
    def __init__(self,strXMLname, strFallbackPath, strDefaultName, forceFallback): pass

    def onInit(self):
        # Put your List Populating code/ and GUI startup stuff here
        self.getControl(10012).setLabel(name.upper())
	self.setFocus(self.getControl(11034))

    def onAction(self, action):
	#print action.getId() #importante para saber que acção estou a fazer
    	if action.getId() == 92: self.close()

    def onClick(self, controlID):
        if controlID == 50000: self.close()
	if controlID == 11030: self.close();votar(url,str(1))
        if controlID == 11031: self.close();votar(url,str(2))
        if controlID == 11032: self.close();votar(url,str(3))
        if controlID == 11033: self.close();votar(url,str(4))
        if controlID == 11034: self.close();votar(url,str(5))
        if controlID == 11035: self.close();votar(url,str(6))
        if controlID == 11036: self.close();votar(url,str(7))
        if controlID == 11037: self.close();votar(url,str(8))
        if controlID == 11038: self.close();votar(url,str(9))
        if controlID == 11039: self.close();votar(url,str(10))

    def onFocus(self, controlID):
        if controlID == 11030: self.getControl(10013).setLabel('1')
        if controlID == 11031: self.getControl(10013).setLabel('2')
        if controlID == 11032: self.getControl(10013).setLabel('3')
        if controlID == 11033: self.getControl(10013).setLabel('4')
        if controlID == 11034: self.getControl(10013).setLabel('5')
        if controlID == 11035: self.getControl(10013).setLabel('6')
        if controlID == 11036: self.getControl(10013).setLabel('7')
        if controlID == 11037: self.getControl(10013).setLabel('8')
        if controlID == 11038: self.getControl(10013).setLabel('9')
        if controlID == 11039: self.getControl(10013).setLabel('10')

###########
# PEDIDOS #
###########

def menu_pedidos(url):
	addDir_reg_menu("[B][COLOR green]Pedir outro filme/série?[/COLOR][/B]","rato",13,artfolder+'contactar.jpg',True,fanart=fanart_rato_tv)
	print url
	pag_actual = url.split('/')[-2]
	print "pagina actual",pag_actual
	if int(pag_actual) == 1 and selfAddon.getSetting('mensagem-pedidos') == "true":
		yes= xbmcgui.Dialog().yesno('RatoTV', 'Clique nos filmes/séries para registar o pedido.', "Pode também pedir outros filmes/séries.", "Continuar a apresentar esta mensagem?",'Não', 'Sim')
		if yes == 0:
			print "Não apresentar mais esta mensagem"
			selfAddon.setSetting('mensagem-pedidos',"false")
		else: print "carreguei no um"
	try: html_source = post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
	except: html_source = ''
	html_source_trunk = re.findall('<div class="req-all"(.*?)Tambem Quero', html_source, re.DOTALL)
	print len(html_source_trunk)
	for trunk in html_source_trunk:
		img_titulo = re.compile('src="(.+?)" alt="(.+?)"').findall(trunk)
		pedidos = re.compile('style="cursor: default;">(.+?)</b>').findall(trunk)
		id_pedido = re.compile("javascript:add_request\('(.+?)'\)").findall(trunk)
		try: addDir_reg_menu(img_titulo[0][1] + "[COLOR green] (" + pedidos[0] + " pedidos)[/COLOR]",id_pedido[0],34,"http://ratotv.net" +img_titulo[0][0],False,fanart=fanart_rato_tv)
		except: pass
	match = re.compile('<a href="http://www.ratotv.net/requests/page/.+?/">(.+?)</a>').findall(html_source)
	pag_total = match[-1]
	print "paginas total",pag_total
	print match
	try: addDir_reg_menu("[COLOR green]Página " + str(pag_actual) +"/"+str(pag_total) + " |[B] Seguinte >>[/COLOR][/B]",'http://www.ratotv.net/requests/page/' + str(int(pag_actual)+1) + '/',33,artfolder+'seta.jpg',True,fanart=fanart_rato_tv)
	except: pass
	pedidos_view()

def pedir_serie_menu():
	yes= xbmcgui.Dialog().yesno('RatoTV', '1) Procurar por nome de filme/série.', "2) Introduzir id do imdb.", "Que opção deseja?",'2)', '1)')
	if yes == 0:
		print "Pedidos opcao2"
		keyb = xbmc.Keyboard('', 'Introduza o id do imdb')
		keyb.doModal()
		if (keyb.isConfirmed()):
			comentario = keyb.getText()
			pedir_imdb("http://www.imdb.com/title/" + str(comentario) +"/")
	else:
		keyb = xbmc.Keyboard('', 'Escreva o nome do filme/série.')
		keyb.doModal()
		if (keyb.isConfirmed()):
			comentario = urllib.quote_plus(keyb.getText())
		data = trakt_api().search_movie(comentario)
		if len(data) >=1:
			addDir_reg_menu("[B][COLOR green]Filmes:[/COLOR][/B]","",13,artfolder+'filmes.jpg',False,fanart=fanart_rato_tv)
			for i in xrange(0,len(data)):
				imdb_id = data[i]["imdb_id"]
				titulo = data[i]["title"]
				ano = data[i]["year"]
				poster = data[i]["images"]["poster"]
				fanarttrakt = data[i]["images"]["fanart"]
				if imdb_id:
					try: addDir_reg_menu(titulo + " (" +str(ano)+")",imdb_id,35,poster,False,fanart=fanarttrakt)
					except:pass
		data = trakt_api().search_show(comentario)
		if len(data) >=1:
			addDir_reg_menu("[B][COLOR green]Séries:[/COLOR][/B]","",13,artfolder+'series.jpg',False,fanart=fanart_rato_tv)
			for i in xrange(0,len(data)):
				imdb_id = data[i]["imdb_id"]
				titulo = data[i]["title"]
				ano = data[i]["year"]
				poster = data[i]["images"]["poster"]
				fanarttrakt = data[i]["images"]["fanart"]
				if imdb_id:
					try: addDir_reg_menu(titulo + " (" +str(ano)+")",imdb_id,35,poster,False,fanart=fanarttrakt)
					except:pass
	pedidos_view()


def pedir_imdb(imdb):
	if "http" not in imdb: imdb = "http://www.imdb.com/title/" + imdb + "/"
	mydata=[('login_name',selfAddon.getSetting('login_name')),('login_password',selfAddon.getSetting('login_password')),('film_request','yes'),('req_url',imdb)]
	source = post_page_free("http://www.ratotv.net/engine/ajax/mws-film.ajax.php",mydata)
	print source
	if '"html":' in source: xbmc.executebuiltin("XBMC.Notification(RatoTV,"+"Pedido efectuado com sucesso."+","+"6000"+"," + addonfolder +"/icon.png)")
	elif '"Ja fizeste este pedido!"' in source: mensagemok('RatoTV','Lamentamos mas já fez o pedido anteriormente.')
	else: mensagemok('RatoTV','Não foi possível encontrar o filme/série.','Verifique novamente.')

def pedir_id(url):
	print url
	mydata=[('login_name',selfAddon.getSetting('login_name')),('login_password',selfAddon.getSetting('login_password')),('film_request','yes'),('add_req',str(url))]
	source = post_page_free("http://www.ratotv.net/engine/ajax/mws-film.ajax.php",mydata)
	print "aqui"
	print source
	if '"result":"ok"}' in source: xbmc.executebuiltin("XBMC.Notification(RatoTV,"+"Pedido efectuado com sucesso."+","+"6000"+"," + addonfolder +"/icon.png)")
	elif '"Ja fizeste este pedido!"' in source: mensagemok('RatoTV','Lamentamos mas já fez o pedido anteriormente.')
	else: mensagemok('RatoTV','Não foi possível encontrar o filme/série.','Verifique novamente.')
	xbmc.executebuiltin("XBMC.Container.Refresh")

####################
#Mensagens privadas#
####################

def mensagens_conta():
	try: html_source = post_page("http://www.ratotv.net/index.php?do=pm&folder=inbox",selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
	except: html_source = ""
	#print html_source
	match = re.compile('<a class="pm_list" href="(.+?)">(.+?)</a></td>').findall(html_source)
	cheia = re.compile('A pasta de mensagens privadas está cheia em: (.+?)">').findall(html_source)
	num_msg_unread = 0
	for endereco_msg,sender in match:
		if "<b>" in sender: num_msg_unread += 1
	try: addDir_reg_menu('Mensagens privadas [COLOR green][ [B]'+str(num_msg_unread)+ '[/B] não lida(s) [/COLOR]|[COLOR yellow] '+ cheia[0]+' cheia [/COLOR][COLOR green]][/COLOR]','url',36,artfolder+'definicoes.jpg',True)
	except: pass


def listar_pms():
	try: html_source = post_page("http://www.ratotv.net/index.php?do=pm&folder=inbox",selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
	except: html_source = ""
	match = re.compile('<a class="pm_list" href="(.+?)">(.+?)</a></td>').findall(html_source)
	for endereco_msg,sender in match:
		if "<b>" in sender: addDir_mensagem('[B]' + sender.replace('<b>','').replace('</b>','')+'[/B]',endereco_msg,37,artfolder+'contactar.jpg',False,"nlida")
		else: addDir_mensagem(sender,endereco_msg,37,artfolder+'contactar.jpg',False,"lida")

def ler_pm(url):
    print url
    try: html_source = post_page(url.replace("amp;",""),selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
    except: html_source = ""
    html_trunk = re.findall('<div class="auth">(.*?)>Responder</a>', html_source, re.DOTALL)
    print html_trunk
    print name
    text = "Assunto: "+name+"\n"
    for trunk in html_trunk:
        data_e_sender = re.compile('href=".+?">(.+?)</a> (.+?)</div>').findall(trunk)
        print data_e_sender
        try:
            text += "De: " + data_e_sender[0][0]+ "\n"
            text += "Enviada em: " + data_e_sender[0][1]+ "\n"
        except: pass
        msg = re.findall('</div>(.*?)<div class="pmlinks">', trunk, re.DOTALL)
        print msg
        try: text += "Mensagem: \n" + msg[0].replace('<br />','')+ "\n"
        except: pass
        janela_lateral("Mensagem Privada",text)

def apagar_pm(url):
	print url
	pm_id = ''
	for letra in url:
		if letra.isdigit(): pm_id += letra
	print pm_id
	try: html_source = post_page("http://www.ratotv.net/index.php?do=pm&doaction=readpm&pmid="+pm_id,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
	except: html_source
	if html_source:
		match = re.compile("javascript:confirmDelete\('(.+?)'\)\">Apagar</a>").findall(html_source)
		try:
			html_source = post_page(match[0].replace('amp;',''),selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
			xbmc.executebuiltin("XBMC.Notification(RatoTV,"+"Mensagem eliminada com sucesso!"+","+"6000"+"," + addonfolder +"/icon.png)")
			xbmc.executebuiltin("XBMC.Container.Refresh")
		except: mensagemok('RatoTV','Ocorreu um erro ao apagar a mensagem.')
	else: mensagemok('RatoTV','Ocorreu um erro ao apagar a mensagem.')

#################################################################################
#                                  FAVORITOS e VISTOS                           #
#################################################################################


def add_to_favourites(url):
    print 'Adicionando aos favoritos: url: '+url
    id_ratotv = re.compile('.*/(.+?)-.+?html').findall(url)
    postURL = base_url+'engine/ajax/favorites.php?fav_id='+id_ratotv[0]+'&action=plus&skin=ratotv'
    html_source=post_page(postURL,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
    xbmc.executebuiltin("XBMC.Notification(RatoTV,"+"adicionado aos favoritos"+","+"6000"+"," + addonfolder +"/icon.png)")
    xbmc.executebuiltin("XBMC.Container.Refresh")

def remover_favoritos(url):
    print 'Removendo dos favoritos: url: '+url
    id_ratotv = re.compile('.*/(.+?)-.+?html').findall(url)
    postURL = base_url+'engine/ajax/favorites.php?fav_id='+id_ratotv[0]+'&action=minus&skin=ratotv'
    html_source=post_page(postURL,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
    xbmc.executebuiltin("XBMC.Notification("+"RatoTv"+","+"Removido dos favoritos"+","+"6000"+"," + addonfolder +"/icon.png)")
    xbmc.executebuiltin("XBMC.Container.Refresh")

def listar_favoritos(url):
    listar_media(url,15)
    moviesandseries_view()

def adicionar_seguir(url,name,iconimage):
	seguirpath=os.path.join(datapath,'Seguir')
	print 'A seguir série: '+url
	id_ratotv = re.compile('.*/(.+?)-.+?html').findall(url)[0]
	last_season_num,last_available_episode = get_last_sep(url)
	try: os.makedirs(seguirpath)
	except: pass
	try:
		NewSeguirFile=os.path.join(seguirpath,id_ratotv+'.txt')
		text= '|' + name + '|' + url + '|' + iconimage + '|'+ last_season_num + '|' + last_available_episode +'|'
		if text != '':
			save(NewSeguirFile,text)
			xbmc.executebuiltin("XBMC.Notification(RatoTV,"+"Operação com sucesso!"+","+"6000"+"," + addonfolder +"/icon.png)")
			xbmc.executebuiltin("XBMC.Container.Refresh")
		else: pass
	except: pass

def deixar_seguir(url):
	seguirpath=os.path.join(datapath,'Seguir')
	print 'A deixar de seguir série: '+url
	id_ratotv = re.compile('.*/(.+?)-.+?html').findall(url)[0]
	filename = os.path.join(seguirpath,id_ratotv + '.txt')
	try:
		os.remove(filename)
		xbmc.executebuiltin("XBMC.Notification(RatoTV,"+"Série removida com sucesso!"+","+"6000"+"," + addonfolder +"/icon.png)")
		xbmc.executebuiltin("XBMC.Container.Refresh")
	except: mensagemok('RatoTV','Ocorreu um erro ao remover série. Informe os developpers deste erro!')


###

def verificar_novos():
	text = ''
	seguirpath=os.path.join(datapath,'Seguir')
	try: dircontents=os.listdir(seguirpath)
	except: dircontents=[]
	if dircontents:
		progresso.create('RatoTv', 'A verificar novos episódios nas séries seguidas','')
		i=0
		while i < len(dircontents):
			seriename,texto =verificar_novoepisodio_serie(dircontents[i])
			print "seriename",seriename
			text += texto
			progresso.update(int(((i+1))/(len(dircontents))*100),"A verificar novos episódios nas séries seguidas",seriename)
			print "progresso", int(((i+1))/(len(dircontents))*100)
			i +=1
		if text != '': return janela_lateral('Séries seguidas: ',text)
		else: return xbmc.executebuiltin("XBMC.Notification(RatoTV,"+"Não há novos episódios."+","+"6000"+"," + addonfolder +"/icon.png)")
	else: pass

def verificar_novoepisodio_serie(txt):
	text = ''
	seguirpath=os.path.join(datapath,'Seguir')
	filename = os.path.join(seguirpath,txt)
	print filename
	try:
		string = readfile(filename)
		match = re.compile('\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|').findall(string)
		print 'Ultimo guardado:S' + match[0][3] + 'E' + match[0][4]
		last_season_num,last_available_episode = get_last_sep(match[0][1])
		print 'Ultimos disponíveis:S' + last_season_num + 'E' +last_available_episode
		if last_season_num != match[0][3] or last_available_episode != match[0][4]:
			print 'Fazer update a ' + txt
			text += 'Novo episódio de ' + match[0][0] + ' disponível! Temporada: '+ last_season_num + ' Episódio: ' + last_available_episode + '\n\n'
			textnew = '|' + match[0][0] + '|' + match[0][1] + '|' + match[0][2] + '|' + last_season_num + '|' + last_available_episode + '|'
			save(filename,textnew)
			return match[0][0],text
		else: return match[0][0],''
	except: return match[0][0],''


####

def adicionar_visto(url,season=None,episode=None):
	try:
		addon_id_trakt = 'script.trakt'
		trakt_addon = xbmcaddon.Addon(id=addon_id_trakt)
		trakt_instalado = True
	except: trakt_instalado = False
	if trakt_instalado == True:
		print 'Esta tudo bem até aqui'
		html_source=post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
		infolabels,name,url2,iconimage2,fanart2,filme_ou_serie,HD2,favorito2 = rato_tv_get_media_info(html_source)
		print infolabels,filme_ou_serie
		data = dict()
		try:
			data["username"] = trakt_addon.getSetting('username')
			data["password"] = trakt_addon.getSetting('password')
			trakt_login_check = True
		except: trakt_login_check = False
		if trakt_login_check == True:
			print 'Verifiquei o login'
			if filme_ou_serie == 'movie':
				url_json_post="http://api.trakt.tv/movie/seen/353f223c2afc3c2050fcb810810fdb49"
				data['movies'] = [dict()]
				try: data['movies'][0]['imdb_id'] = infolabels['code']
				except: pass
				try: data['movies'][0]['title'] = infolabels['originaltitle']
				except: pass
				try: data['movies'][0]['year'] = infolabels['Year']
				except: pass
				print 'data final:',data
				try: json_post(data,url_json_post)
				except: print "Não conseguiu marcar visto no trakt"
			elif filme_ou_serie == 'tvshow':
				url_json_post="http://api.trakt.tv/show/episode/seen/353f223c2afc3c2050fcb810810fdb49"
				data["episodes"] = [{"season": season,"episode": episode}]
				try: data['imdb_id'] = infolabels['code']
				except: pass
				try: data['title'] = infolabels['originaltitle']
				except: pass
				try: data['year'] = infolabels['Year']
				except: pass
				print 'data final:',data
				try: json_post(data,url_json_post)
				except: print "Não conseguiu marcar visto no trakt"
		else:pass
	print 'Marcando como visto: url: '+url
	id_ratotv = re.compile('.*/(.+?)-.+?html').findall(url)[0]
	vistospath=os.path.join(datapath,'Vistos')
	try: os.makedirs(vistospath)
	except: pass
	if season and episode: NewVistoFile=os.path.join(vistospath,id_ratotv+'-S'+season+'E'+episode+'.txt')
	else: NewVistoFile=os.path.join(vistospath,id_ratotv+'.txt')
	if not os.path.exists(NewVistoFile):
		save(NewVistoFile,'')
		xbmc.executebuiltin("XBMC.Notification(RatoTV,"+"Marcado como visto"+","+"6000"+"," + addonfolder +"/icon.png)")
		xbmc.executebuiltin("XBMC.Container.Refresh")
	else:
		print 'Aviso - visto ja existe'
		mensagemok('RatoTV','Já estava marcado como visto.')

def remover_visto(url,season=None,episode=None):
    print 'Marcando como não visto: url: '+url
    id_ratotv = re.compile('.*/(.+?)-.+?html').findall(url)[0]
    vistospath=os.path.join(datapath,'Vistos')
    if season and episode: NewVistoFile=os.path.join(vistospath,id_ratotv+'-S'+season+'E'+episode+'.txt')
    else: NewVistoFile=os.path.join(vistospath,id_ratotv+'.txt')
    try:os.remove(NewVistoFile)
    except: mensagemok('RatoTV','Não foi possível marcar como não visto.')
    xbmc.executebuiltin("RatoTv,"+"Marcado como não visto"+","+"6000"+"," + addonfolder +"/icon.png)")
    xbmc.executebuiltin("XBMC.Container.Refresh")

def check_visto(url,season=None,episode=None):
    print 'check_visto url:'+url
    id_ratotv = id_ratotv = re.findall(r'\d+', url)[0]
    vistospath=os.path.join(datapath,'Vistos')
    if season and episode: NewVistoFile=os.path.join(vistospath,id_ratotv+'-S'+str(season)+'E'+str(episode)+'.txt')
    else: NewVistoFile=os.path.join(vistospath,id_ratotv+'.txt')
    if os.path.exists(NewVistoFile): return True
    else: return False

#################################################################################
#FUNCOES API'S - TMDB e FANART.TV                                               #
#################################################################################

#Trakt.tv
class trakt_api:
    api_key = '353f223c2afc3c2050fcb810810fdb49'
    def next_episode(self,tvdbid):
        url_api = 'http://api.trakt.tv/show/summary.json/' + self.api_key + '/' + tvdbid + '/extended'
        try: data = json_get(url_api)
        except: data = ''
        return data

    def search_movie(self,query):
        url_api = 'http://api.trakt.tv/search/movies.json/'+ self.api_key + '?query='+str(query)
        try: data = json_get(url_api)
        except: data = ''
        return data

    def search_show(self,query):
        url_api = 'http://api.trakt.tv/search/shows.json/'+ self.api_key + '?query='+str(query)
        try: data = json_get(url_api)
        except: data = ''
        return data

    def return_watched_movies(self,query):
        url_api = 'http://api.trakt.tv/user/library/movies/watched.json/'+ self.api_key +'/' + str(query)
        try: data = json_get(url_api)
        except: data = ''
        return data

    def return_watched_shows(self,query):
        url_api = 'http://api.trakt.tv/user/library/shows/watched.json/'+ self.api_key +'/' + str(query)
        try: data = json_get(url_api)
        except: data = ''
        return data

    def movie_unwatched(self,coiso):
        data ={ "username": "username","password": "sha1hash","movies": [{"imdb_id": "tt0114746","title": "Twelve Monkeys","year": 1995}]}

    def shows_seasons(self,tvdbid):
	url_api = 'http://api.trakt.tv/show/seasons.json/'+ self.api_key +'/' + str(tvdbid)
        try: data = json_get(url_api)
        except: data = ''
        return data

    def shows_season(self,tvdbid,season):
	url_api = 'http://api.trakt.tv/show/season.json/'+ self.api_key +'/' + str(tvdbid) + '/' + str(season)
        try: data = json_get(url_api)
        except: data = ''
        return data

    def get_showepisode_thumb(self,originaltitle,year,season,episode):
	screen = ''
	id_tvdb = thetvdb_api()._id(originaltitle,int(year))
	json_code = self.shows_season(id_tvdb,int(season))
	for entry in json_code:
		if int(entry['episode']) == int(episode):
			try: screen = entry['screen']
			except: pass
			break
	return screen
	
#THEMOVIEDB

class themoviedb_api:
    api_key = 'efdea87099d474a3fd5e6f83b8bc42a6'
    tmdb_base_url = 'http://d3gtl9l2a4fn1j.cloudfront.net/t/p/w1280'
    def fanart_and_id(self,movie_info_original_title,movie_info_year):
        url_tmdb = 'http://api.themoviedb.org/3/search/movie?api_key=' + self.api_key + '&query=' + urllib.quote_plus(movie_info_original_title) + '&year=' + movie_info_year
        try: data = json_get(url_tmdb)
        except: data = ''
        try: fanart=self.tmdb_base_url + data['results'][0]['backdrop_path']
        except: fanart=fanart_rato_tv
        try: id_tmdb = data['results'][0]['id']
        except: id_tmdb=''
        return fanart,str(id_tmdb)

    def trailer(self,id_tmdb):
        url_tmdb = 'http://api.themoviedb.org/3/movie/' + id_tmdb +'/trailers?api_key=' + self.api_key
        try: data = json_get(url_tmdb)
        except: data = ''
        try: youtube_id = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + str(data['youtube'][0]['source'])
        except: youtube_id= ''
        return str(youtube_id)

#THETVDB
class thetvdb_api:
    def _id(self,series_name,year):
        _id_init = []
        try:
            url = 'http://thetvdb.com/api/GetSeries.php?seriesname=' + urllib.quote(series_name)+'&language=pt'
            print url
            html_source = abrir_url(url)
        except: html_source = ''
        id_and_year = re.findall('<seriesid>(.+?)</seriesid>.*?<FirstAired>(.+?)-.+?-.+?</FirstAired>', html_source, re.DOTALL)
        print id_and_year
        if id_and_year == []:
            _id = re.compile('<seriesid>(.+?)</seriesid>').findall(html_source)
            print _id
            if _id == []: return ''
            else: return _id[0]
        else:
            for serieid,ano in id_and_year:
                if ano == year: _id_init.append(serieid)
                else: pass
            if _id_init == []: return id_and_year[0][0]
            else: return _id_init[0]

    def fanart(self,series_id):
        return 'http://thetvdb.com/banners/fanart/original/' + series_id + '-1.jpg'

#FANART.TV

class fanarttv_api:
    api_key='93981ff0b2619c20c530189775c38c85'
    def _id(self,series_name):
        try:
            url = 'http://thetvdb.com/api/GetSeries.php?seriesname=' + urllib.quote(series_name)
            print url
            html_source = abrir_url(url)
        except: html_source = ''
        match_ids = re.compile('<seriesid>(.+?)</seriesid>').findall(html_source)
        if len(match_ids) >= 1: return match_ids[0]
        else: return ''

    def fanart(self,series_id):
        try:
            url = 'http://api.fanart.tv/webservice/series/' + self.api_key + '/' + series_id + '/xml/'
            html_source = abrir_url(url)
        except: html_source = ''
        fanart_vector = re.compile('<tvthumb id=".+?" url="(.+?)" lang=".+?" likes=".+?"/>').findall(html_source)
        if len(fanart_vector) >= 1: print fanart_vector[0]; return fanart_vector[0]
        else: return ''

    def season_thumbs(self,temporada,series_id):
        try:
            url = 'http://api.fanart.tv/webservice/series/' + self.api_key + '/' + series_id + '/xml/'
            html_source = abrir_url(url)
            thumb_vector = re.compile('<seasonthumb id=".+?" url="(.+?)" lang=".+?" likes=".+?" season="%s"/>'%temporada).findall(html_source)
            if len(thumb_vector) >= 1: return thumb_vector[0]
            else: return ''
        except: return ''

#################################################################################
#FUNCOES REQUEST's HTTP                                                         #
#################################################################################

def abrir_url(url, encoding='utf-8'):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    if encoding != 'utf-8': link = link.decode(encoding).encode('utf-8')
    return link

def json_get(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    data = json.load(urllib2.urlopen(req))
    return data

def json_post(data,url):
	data = json.dumps(data)
	req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
	f = urllib2.urlopen(req)
	response = f.read()
	f.close()

def post_page(url,user,password):
    mydata=[('login_name',user),('login_password',password),('login','submit')]
    mydata=urllib.urlencode(mydata)
    req=urllib2.Request(url, mydata)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    page=urllib2.urlopen(req).read()
    return page

def post_page_free(url,mydata):
	mydata=urllib.urlencode(mydata)
	req=urllib2.Request(url, mydata)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	req.add_header("Content-type", "application/x-www-form-urlencoded")
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	page=urllib2.urlopen(req).read()
	return page

def exists(url):
    try:
        r = urllib2.urlopen(url)
        return True
    except: return False

#Thanks fightnight
def handle_wait(time_to_wait,title,text,segunda=''):
      ret = progresso.create(' '+title)
      secs=0
      percent=0
      increment = int(100 / time_to_wait)
      cancelled = False
      while secs < time_to_wait:
            secs = secs + 1
            percent = increment*secs
            secs_left = str((time_to_wait - secs))
            if segunda=='': remaining_display = "Faltam " +secs_left+ " segundos"
            else: remaining_display=segunda
            progresso.update(percent,text,remaining_display)
            xbmc.sleep(1000)
            if (progresso.iscanceled()):
                  cancelled = True
                  break
      if cancelled == True: return False
      else:
	    progresso.close()
            return True

####Subscricoes

def adicionar_filme_biblioteca(name,url,iconimage):
	current_url = url
	if selfAddon.getSetting('libraryfolder'): pass
	else:
		ok=mensagemok('RatoTV','Não definiu uma pasta para a biblioteca nas definições!','Por favor defina-a e tente novamente.')
		sys.exit(0)
	if not xbmcvfs.exists(os.path.join(selfAddon.getSetting('libraryfolder'),'movies')): xbmcvfs.mkdir(os.path.join(selfAddon.getSetting('libraryfolder'),'movies'))
	id_ratotv = re.compile('.*/(.+?)-.+?html').findall(url)[0]
	try: html_source=post_page(current_url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
	except: html_source = ''
	if html_source:
		html_source_trunk = re.findall('<div class="shortpost(.*?)Reportar</a></li>', html_source, re.DOTALL)
		if html_source_trunk:
			infolabels,name,url,iconimage,fanart,filme_ou_serie,HD,favorito = rato_tv_get_media_info(html_source_trunk[0])
			movie_folder = os.path.join(selfAddon.getSetting('libraryfolder'),'movies',infolabels['originaltitle'] + ' ('+str(infolabels["Year"])+')')
			if not xbmcvfs.exists(movie_folder): xbmcvfs.mkdir(movie_folder)
			strm_contents = 'plugin://plugin.video.ratotv/?url=' + url +'&mode=44&name=' + urllib.quote_plus(infolabels['originaltitle'])
			movie_database_file = os.path.join(movie_folder,id_ratotv+'.txt')
			save(movie_database_file,strm_contents)
			xbmc.executebuiltin("XBMC.Notification(RatoTv,Filme adicionado à biblioteca!,'10000',"+addonfolder+"/icon.png)")
			xbmc.executebuiltin("XBMC.UpdateLibrary(video)")




def procurar_novas_series():
	cancelar = False
	pasta_series_subscritas = os.path.join(datapath,'tvshows-subscriptions')
	if not xbmcvfs.exists(pasta_series_subscritas):
		cancelar = True
	else:
		dirs, files = xbmcvfs.listdir(pasta_series_subscritas)
		if not files:
			cancelar = True
	if cancelar:
		ok=mensagemok('RatoTV','Não tem séries subscritas','Subscreva novas séries ou desactive a procura de novas séries!')
		sys.exit(0)
	else:
		for serie_txt in files:
			serie_file = os.path.join(pasta_series_subscritas,serie_txt)
			serie_file_data = readfile(serie_file)
			name,url,iconimage = serie_file_data.split('|')
			subscrever_serie(name,url,iconimage,True)
	xbmc.executebuiltin("XBMC.UpdateLibrary(video)")
	return
			

def transferir_biblioteca_filmes(name):

	#verifica se a pasta para o download da biblioteca está definida

	if selfAddon.getSetting('libraryfolder'): pass
	else:
		ok=mensagemok('RatoTV','Não definiu uma pasta para a biblioteca nas definições!','Por favor defina-a e tente novamente.')
		sys.exit(0)
	canceled = False
	comando = name
	url_current = base_url + 'movies/page/1/'
	movie_database_folder = os.path.join(datapath,'movie-subscriptions')

	#verifica se ja transferiu a biblioteca anteriormente para o service.py funcionar devidamente e não tornar o xbmc lento	

	if comando == 'novos':
		if not xbmcvfs.exists(movie_database_folder):
			ok=mensagemok('RatoTV','Tem o serviço de procura de novos filmes activo.','Mas nao transferiu a biblioteca...','Saindo.')
			sys.exit(0)

	if not xbmcvfs.exists(movie_database_folder): xbmcvfs.mkdir(movie_database_folder)
	if not xbmcvfs.exists(os.path.join(selfAddon.getSetting('libraryfolder'),'movies')): xbmcvfs.mkdir(os.path.join(selfAddon.getSetting('libraryfolder'),'movies'))
	try: html_source=post_page(url_current,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
	except: html_source = ''
	if html_source:
		current_page= re.compile('/page/(\d+)/').findall(url_current)[0]
		if not current_page: current_page = str(1)
		pag_seguinte = re.compile('<div class="next"><a href="(.+?)">').findall(html_source)[0]
		try: total_paginas = re.compile('.*<a href=".+?">(.+?)</a>\n<div class="next">').findall(html_source)[0]
		except: total_paginas=re.compile('.*/page/(.+?)/">(.+?)</a> ').findall(html_source)[0]
		current_page = int(current_page)
		html_source_trunk = re.findall('<div class="shortpost">(.*?)<\/div>\n<\/div>\n<\/div>', html_source, re.DOTALL)
		if comando == 'todos': progresso.create('RatoTV - Biblioteca XBMC', 'A transferir biblioteca de Filmes...Aguarde...' ,'Página '+str(current_page)+'/'+str(total_paginas))
		i=0
		while int(current_page) < int(total_paginas):
			if comando == 'todos':
				if progresso.iscanceled():
					canceled = True
					progresso.update(100,"Cancelando...")	
					progresso.close()
					break
			if current_page != 1:
				try: html_source=post_page(pag_seguinte,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
				except: html_source = ''
				pag_seguinte = re.compile('<div class="next"><a href="(.+?)">').findall(html_source)[0]
				html_source_trunk = re.findall('<div class="shortpost">(.*?)<\/div>\n<\/div>\n<\/div>', html_source, re.DOTALL)
			for trunk in html_source_trunk:
				infolabels,name,url,iconimage,fanart,filme_ou_serie,HD,favorito = rato_tv_get_media_info(trunk)
				if comando == 'todos': progresso.update(int((float(current_page)/int(total_paginas)*100)),'A transferir biblioteca de Filmes...Aguarde...',infolabels['originaltitle'] + ' (' + infolabels['Year'] +')','Página '+str(current_page)+'/'+str(total_paginas))
				if not xbmcvfs.exists(os.path.join(selfAddon.getSetting('libraryfolder'),'movies',infolabels['originaltitle'] + ' ('+str(infolabels["Year"])+')')): xbmcvfs.mkdir(os.path.join(selfAddon.getSetting('libraryfolder'),'movies',infolabels['originaltitle'] + ' ('+str(infolabels["Year"])+')'))
				strm_filme = os.path.join(selfAddon.getSetting('libraryfolder'),'movies',infolabels['originaltitle'] + ' ('+str(infolabels["Year"])+')',infolabels['originaltitle']+'.strm')
				strm_contents = 'plugin://plugin.video.ratotv/?url=' + url +'&mode=44&name=' + urllib.quote_plus(infolabels['originaltitle'])
				id_ratotv = re.compile('.*/(.+?)-.+?html').findall(url)[0]
				movie_database_file = os.path.join(movie_database_folder,id_ratotv+'.txt')

			#verifica se o filme ja existe na biblioteca para interromper o ciclo caso esteja à procura de filmes novos 
				if comando == 'novos':
					if xbmcvfs.exists(movie_database_file):
						current_page = int(total_paginas)
						break
						
			#salva ficheiro na userdata para saber se item ja foi transferido anteriormente
			
				if not xbmcvfs.exists(movie_database_file): save(movie_database_file,'check')
			#salva stream
			
				save(strm_filme,strm_contents)
				i +=1

			current_page +=1
			if comando == 'todos': progresso.update(int((float(current_page)/int(total_paginas)*100)),'A transferir biblioteca de Filmes...Aguarde...',infolabels['originaltitle'] + ' (' + infolabels['Year'] +')','Página '+str(current_page)+'/'+str(total_paginas))
	if comando == 'todos' and not canceled:
		progresso.update(100,'Tarefa realizada com sucesso')
		progresso.close()
	if not canceled and i >= 1: xbmc.executebuiltin("XBMC.UpdateLibrary(video)")

def listar_series_subseguir(name):
	if name == "subscritas":
		folder = os.path.join(datapath,'tvshows-subscriptions')
		message = 'Não tem séries subscritas.'
	elif name == "seguir":
		folder = os.path.join(datapath,'Seguir')
		message = 'Não está a seguir nenhuma série'
	if not xbmcvfs.exists(folder):xbmcvfs.mkdir(folder)
	dirs, files = xbmcvfs.listdir(folder)
	if len(files) > 0:
		i=0
		progresso.create('RatoTV', 'A obter metadata... ')
		progresso.update(i,'A obter metadata...')
		for ficheiro in files:
			seriefile = os.path.join(datapath,'tvshows-subscriptions',ficheiro)
			serie_data = readfile(seriefile) 
			serie_array = serie_data.split('|')
			id_rato = ficheiro.replace('.txt','')
			media_database_folder = os.path.join(datapath,'media_database')
			txt_file = os.path.join(media_database_folder,id_rato + '.txt')
			if not xbmcvfs.exists(media_database_folder): xbmcvfs.mkdir(media_database_folder)
			if xbmcvfs.exists(txt_file):
				data = readfile(txt_file).split('|')
				name = data[0]
				url = data[1]
				iconimage = data[3]
				infolabels = eval(data[2])
				fanart = urllib.unquote(data[4])
				filme_ou_serie = data[5]
				HD = eval(data[6])
				favorito = eval(data[7])		
			else:
				infolabels,name,url,iconimage,fanart,filme_ou_serie,HD,favorito = obter_info_url(serie_array[1],True)
				progresso.update(int(i/float(len(files))*100),'A obter metadata...',name)
			addDir_filme(name + ' (' + str(infolabels["Year"]) +')',url,mode,iconimage,infolabels,fanart,len(files),True,filme_ou_serie,HD,favorito)
			i += 1
		progresso.close()
		moviesandseries_view()
	else:
		ok=mensagemok('RatoTV',message)
		sys.exit(0)
		
def remover_subscricao_serie(name,url,iconimage):
	id_ratotv = re.compile('.*/(.+?)-.+?html').findall(url)[0]
	txt_serie = os.path.join(datapath,'tvshows-subscriptions',str(id_ratotv) +'.txt')
	xbmcvfs.delete(txt_serie)
	yes= xbmcgui.Dialog().yesno("RatoTv", 'Pretende também remover os ficheiros e actualizar a biblioteca?')
	if yes:
		iconimage,originaltitle,year,serie_dict_temporadas = series_seasons_get_dictionary(url,name,"fanart")
		folder_show = os.path.join(selfAddon.getSetting('libraryfolder'),'tvshows',originaltitle)
		dirs, files = xbmcvfs.listdir(folder_show)
		for directory in dirs:
			directory_apagar = os.path.join(selfAddon.getSetting('libraryfolder'),'tvshows',originaltitle,directory)
			subdirs, subfiles = xbmcvfs.listdir(directory_apagar)
			for subfile in subfiles:
				sub_file = os.path.join(selfAddon.getSetting('libraryfolder'),'tvshows',originaltitle,directory,subfile)
				xbmcvfs.delete(sub_file)
			xbmcvfs.rmdir(directory_apagar)
		for ficheiro in files:
			ficheiro_apagar = os.path.join(selfAddon.getSetting('libraryfolder'),'tvshows',originaltitle,ficheiro)
			xbmcvfs.delete(ficheiro_apagar)
		xbmcvfs.rmdir(folder_show)
		xbmc.executebuiltin("XBMC.CleanLibrary(video)")
	else: pass
	xbmc.executebuiltin("XBMC.Notification(RatoTv,Removida subscrição com sucesso!,'10000',"+addonfolder+"/icon.png)")
	xbmc.executebuiltin("XBMC.Container.Refresh")

def subscrever_serie(name,url,iconimage,daemon=False):
	print "Subscrever series",name,url,iconimage
	id_ratotv = re.compile('.*/(.+?)-.+?html').findall(url)[0]
	if not xbmcvfs.exists(os.path.join(datapath,'tvshows-subscriptions')): xbmcvfs.mkdir(os.path.join(datapath,'tvshows-subscriptions'))
	save(os.path.join(datapath,'tvshows-subscriptions',str(id_ratotv) +'.txt'),name + '|'+url+'|'+iconimage)
	print selfAddon.getSetting('libraryfolder')
	if selfAddon.getSetting('libraryfolder'):
		if not xbmcvfs.exists(os.path.join(selfAddon.getSetting('libraryfolder'),'tvshows')): xbmcvfs.mkdir(os.path.join(selfAddon.getSetting('libraryfolder'),'tvshows'))
		iconimage,originaltitle,year,serie_dict_temporadas = series_seasons_get_dictionary(url,name,"fanart")
		if not xbmcvfs.exists(os.path.join(selfAddon.getSetting('libraryfolder'),'tvshows',originaltitle)): xbmcvfs.mkdir(os.path.join(selfAddon.getSetting('libraryfolder'),'tvshows',originaltitle))
		total_seasons = len(serie_dict_temporadas.keys())
		for season in serie_dict_temporadas.keys():
			if not xbmcvfs.exists(os.path.join(selfAddon.getSetting('libraryfolder'),'tvshows',originaltitle,'Season ' + str(season))): xbmcvfs.mkdir(os.path.join(selfAddon.getSetting('libraryfolder'),'tvshows',originaltitle,'Season ' + str(season)))
			temp,year,episodios_dict = listar_temporadas_get_dictionary(" "+str(int(season)),url,"fanart","iconimage",str(serie_dict_temporadas))
			for episode in episodios_dict.keys():
				string = 'S'+str(season)+'E'+str(episode)
				strm='plugin://plugin.video.ratotv/?url=' + url +'&mode=44&name=' + string
				save(os.path.join(selfAddon.getSetting('libraryfolder'),'tvshows',originaltitle,'Season ' + str(season),originaltitle + ' '+ string+'.strm'),strm)
		if not daemon:
			xbmc.executebuiltin("XBMC.Notification(RatoTv,Série subscrita com sucesso!,'10000',"+addonfolder+"/icon.png)")
			xbmc.executebuiltin("XBMC.UpdateLibrary(video)")
			xbmc.executebuiltin("XBMC.Container.Refresh")	
	else: print "falhou"
	return


def play_from_outside(name,url):
	listitem = xbmcgui.ListItem(name, iconImage="iconimage", thumbnailImage="iconimage")
	xbmcplugin.setResolvedUrl(int(sys.argv[1]),False,listitem)
	try: html_source=post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
	except: print "ERRO FALTA FAZER",sys.exit(0)
	match = re.compile('<img src="/templates/ratotvv2/dleimages/comments-img2.png"/><a href="http://www.ratotv.net/(.+?)/">.+?</a>').findall(html_source)
	if match[0] == 'tvshows':
		proceed = False
		match = re.compile('S(.+?)E(\d+)').findall(name)
		try:
			int(match[0][0])
			int(match[0][1])
			proceed = True
		except: proceed = False
		if proceed:
			iconimage,originaltitle,year,serie_dict_temporadas = series_seasons_get_dictionary(url,name,"fanart")
			temporada = match[0][0]
			episodio = match[0][1]
			total_seasons = len(serie_dict_temporadas.keys())
			proceed = False
			for season in serie_dict_temporadas.keys():
				if int(season) == int(temporada):	
					proceed = True
					break
			if proceed:
				proceed = False
				temp,year,episodios_dict = listar_temporadas_get_dictionary(" "+str(int(temporada)),url,"fanart","iconimage",str(serie_dict_temporadas))
				for episode in episodios_dict.keys():
					if int(episodio) == int(episode):
						proceed = True
						break
				if proceed:
					screen = ''
					if selfAddon.getSetting('series-episode-thumbnails') == 'true': screen = trakt_api().get_showepisode_thumb(originaltitle,year,temporada,episodio)
					if screen: screenthumb = screen
					else: screenthumb = str(episodios_dict[str(int(episodio))]["thumbnail"])
					if "srt" in episodios_dict[str(int(episodio))].keys(): episodios_opcao(str(episodios_dict[str(int(episodio))]["description"]),url,screenthumb,str(episodios_dict[str(int(episodio))]["source"]),str(episodios_dict[str(int(episodio))]["srt"]),originaltitle,temporada,episodio)
					else: episodios_opcao(str(episodios_dict[str(int(episodio))]["description"]),url,screenthumb,str(episodios_dict[str(int(episodio))]["source"]),'',originaltitle,temporada,episodio)
				else: print "nao encontrou o episodio. FALTA MOSTRAR ERRO"
	if match[0] == 'movies':
		print "Movie detectado"
        	html_source_trunk = re.findall('<div class="shortpost(.*?)Adicionar um comentário', html_source, re.DOTALL)
		infolabels,name,url,iconimage,fanart,filme_ou_serie,HD,favorito = rato_tv_get_media_info(html_source_trunk[0])
		stream_qualidade(url,name,iconimage)
	else: print "MENSAGEM DE ERRO FALTA"

def listar_temporadas_get_dictionary(name,url,fanart,iconimage,dicionario):
	try:
		#verificar se originaltitle e year estao definidos
		print originaltitle,year
		original_year = True
	except: original_year = False
	if not original_year:
		try: html_source=post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
		except: ok=mensagemok('RatoTV','Não foi possível abrir a página. Tente novamente \n ou contacte um dos administradores do site.');sys.exit(0)
		if html_source:
			originaltitle=re.compile('<strong>Título Original: </strong>(.+?)</li>').findall(html_source)[0]
			year = re.compile('<strong>Ano: </strong><a href=".+?">(.+?)</a>').findall(html_source)[0]
	temporada = re.compile('.* (\d+)').findall(name)[0]
	dic = eval(dicionario)
	episodios_dict = {}
	for rss in dic[temporada]:
   		try:
          		htmll_source = abrir_url(rss, encoding='iso-8859-1')
            		items = re.findall('<item>(.*?)</item>', htmll_source, re.DOTALL)
   			for item in items:
            			title = re.compile('<title>(.+?)</title>').findall(item)
				title[0]=title[0].replace("Episodio ","").replace("Episódio ","").replace("Epi ","").replace("Epis ","")
            			description = re.compile('<description>(.+?)</description>').findall(item)
            			thumbnail = re.compile('<jwplayer:image>(.+?)</jwplayer:image>').findall(item)
            			sources_1 = re.compile('source file="(.+?)" label="(.+?)"').findall(item)
            			sub = re.compile('<jwplayer:track file="(.+?)"').findall(item)
				try:episodios_dict[title[0]]
				except:episodios_dict[title[0]]={}
				try: episodios_dict[title[0]]["description"]=description[0]
				except:pass
				try: episodios_dict[title[0]]["thumbnail"]=thumbnail[0]
				except: pass
				try: episodios_dict[title[0]]["source"].append(sources_1[0][0])
				except:episodios_dict[title[0]]["source"]=[sources_1[0][0]]
				try:episodios_dict[title[0]]["srt"].append(sub[0])
				except:episodios_dict[title[0]]["srt"]=[sub[0]]
			items = re.findall('<track>(.*?)</track>', htmll_source, re.DOTALL)
			for item in items:
				title = re.compile('<title>(.+?)</title>').findall(item)
				title[0]=title[0].replace("Episodio ","").replace("Episódio ","").replace("Epi ","").replace("Epis ","")
				description = re.compile('<description>(.+?)</description>').findall(item)
				thumbnail = re.compile('<image>(.+?)</image>').findall(item)
				source = re.compile('<location>ratotv(.+?)</location>').findall(item)
				sub = re.compile('<captions.files>(.+?)</captions.files>').findall(item)
 				try:episodios_dict[title[0]]
				except:episodios_dict[title[0]]={}
				try: episodios_dict[title[0]]["description"]
				except:episodios_dict[title[0]]["description"]=description[0]
				try: episodios_dict[title[0]]["thumbnail"]
				except:episodios_dict[title[0]]["thumbnail"]=thumbnail[0]
				try: episodios_dict[title[0]]["source"].append(source[0].replace("*",""))
				except:episodios_dict[title[0]]["source"]=[source[0].replace("*","")]
				try:episodios_dict[title[0]]["srt"].append(sub[0])
				except:episodios_dict[title[0]]["srt"]=[sub[0]]
		except: pass
	return temporada,year,episodios_dict

def listar_temporadas(name,url,fanart,iconimage,dicionario):
	temporada,year,episodios_dict = listar_temporadas_get_dictionary(name,url,fanart,iconimage,dicionario)
	if selfAddon.getSetting('series-episode-thumbnails') == 'true':
		id_tvdb = thetvdb_api()._id(originaltitle,year)
		json_code = trakt_api().shows_season(id_tvdb,temporada)
	for episodio in sorted(episodios_dict.iterkeys(), key=keyfunc):
		screenimage = None
		if selfAddon.getSetting('series-episode-thumbnails') == 'true':
			aval = 0
			for key in json_code:
				if str(key['episode']) == str(episodio):
					try: screenimage = key['images']['screen'];screen_checker = True
					except:screenimage = str(episodios_dict[episodio]["thumbnail"])
				aval +=1
			if aval == len(json_code) and screenimage == None: screenimage = str(episodios_dict[episodio]["thumbnail"])
			else:pass
		else: screenimage = str(episodios_dict[episodio]["thumbnail"])
		if "srt" in episodios_dict[episodio].keys(): addDir_episodio(name,"[B][COLOR green]Episódio " + str(episodio) + "[/B][/COLOR]",str(episodios_dict[episodio]["description"]),url,temporada,episodio,str(episodios_dict[episodio]["source"]),str(episodios_dict[episodio]["srt"]),screenimage,fanart)
		else: addDir_episodio(name,"[B][COLOR green]Episódio " + str(episodio) + "[/B][/COLOR]",str(episodios_dict[episodio]["description"]),url,temporada,episodio,str(episodios_dict[episodio]["source"]),"",screenimage,fanart)
	episodes_view()

def keyfunc(key): return float(key.replace(" e ","."))

def episodios_opcao(name,url,iconimage,sources,srt,originaltitle,season,episode):
	if "COLOR green" in originaltitle: originaltitle = get_original_title(url)
	infolabels = { "Title": name , "TVShowTitle":originaltitle,"Season":season, "Episode":episode }
	source=eval(sources)
	srt=eval(srt)
	num_opcoes = len(source)
	if num_opcoes == 1: opcao = "1"
	elif num_opcoes == 2:
		janela2qualidades()
		opcao = readfile(datapath + "option.txt")
	elif num_opcoes == 3:
		janela3qualidades()
		opcao = readfile(datapath + "option.txt")
	else: ok=mensagemok('RatoTV','Ocorreu um erro. Tente novamente.'); sys.exit(0)
	if opcao == '10': sys.exit(0)
	else:
		if "http" in source[int(opcao)-1]:
			decoded_url = source[int(opcao)-1] + '|host=ratotv.com&referer=' + url
			source[int(opcao)-1] = decoded_url

		else:
			decoded_url = resolver_externos(source[int(opcao)-1])
			source[int(opcao)-1] = decoded_url
		if "../" in srt[int(opcao)-1]: srt[int(opcao)-1] = srt[int(opcao)-1].replace("../",base_url)
		player_rato(source[int(opcao)-1],srt[int(opcao)-1],name,url,iconimage,infolabels,season,episode)

########################################################################################################
#FUNCOES DIRECTORIAS                                                                                   #
########################################################################################################

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

def addLink(name,url,iconimage):
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setProperty('fanart_image', fanart_rato_tv)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    return ok

def addDir_mensagem(name,url,mode,iconimage,folder,lida,fanart=fanart_rato_tv):
	print lida
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	if fanart: u+= '&fanart='+urllib.quote_plus(fanart)
	contextmen = []
	contextmen.append(('Apagar', 'XBMC.RunPlugin(%s?mode=38&url=%s&)' % (sys.argv[0], urllib.quote_plus(url))))
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	if fanart: liz.setProperty('fanart_image', fanart)
	else: liz.setProperty('fanart_image', fanart_rato_tv)
	print u
	liz.addContextMenuItems(contextmen, replaceItems=True)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
	return ok

def addDir_reg_menu(name,url,mode,iconimage,folder,fanart=fanart_rato_tv):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    if fanart: u+= '&fanart='+urllib.quote_plus(fanart)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    if fanart: liz.setProperty('fanart_image', fanart)
    else: liz.setProperty('fanart_image', fanart_rato_tv)
    print u
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
    return ok

def addDir_temporada(name,url,dicionario,mode,iconimage,folder,fanart):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&dicionario="+urllib.quote_plus(dicionario)
    try: u += "&year="+urllib.quote_plus(year)
    except:pass
    if fanart: u+= '&fanart='+urllib.quote_plus(fanart)
    if originaltitle: u+="&originaltitle="+urllib.quote_plus(originaltitle)
###AMELHORAR!
    else:
	try:
		html_source=post_page(url,selfAddon.getSetting('login_name'),selfAddon.getSetting('login_password'))
		match = re.compile('<span>Título Original: </span><span class="fvalue">(.+?)</span>').findall(html_source)[0]
		u+="&originaltitle="+match
	except:pass
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    if fanart: liz.setProperty('fanart_image', fanart)
    else: liz.setProperty('fanart_image', fanart_rato_tv)
    print u
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
    return ok

def addDir_filme(name,url,mode,iconimage,infolabels,fanart,totalit,pasta,tipo,HD,favorito):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&tipo="+urllib.quote_plus(tipo)
    try: u += "&year="+infolabels['Year']
    except: pass
    try: u += "&imdb_id="+infolabels['code']
    except: pass
    try: u += "&originaltitle="+infolabels['originaltitle']
    except: pass
    try: id_ratotv = re.compile('.*/(.+?)-.+?html').findall(url)[0]
    except: id_ratotv = None
    print id_ratotv
    seguirpath=os.path.join(datapath,'Seguir')
    filename = os.path.join(seguirpath,id_ratotv + '.txt')
    if fanart: u+='&fanart='+urllib.quote_plus(fanart)
    ok=True
    if mode == 3: tipo = 'movie'
    elif mode == 10: tipo = 'tvshow'
    else: tipo = ''
    overlay=6
    playcount=0
    contextmen = []
    if ADDON.getSetting('download-activo') == "true" and tipo == 'movie' and ADDON.getSetting('folder') != "Escolha a pasta":
        contextmen.append(('Download', 'XBMC.RunPlugin(%s?mode=31&name=%s&url=%s&iconimage=%s&tipo=%s)' % (sys.argv[0], name, url, iconimage,urllib.quote_plus(tipo))))
    else: pass
    contextmen.append(('Estatísticas Trakt', 'XBMC.RunPlugin(%s?mode=30&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], name, url, iconimage)))
    contextmen.append(('Ver detalhes', 'XBMC.Action(Info)'))
    contextmen.append(('Classificar', 'XBMC.RunPlugin(%s?mode=19&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], name, url, iconimage)))
    contextmen.append(('Reportar problema', 'XBMC.RunPlugin(%s?mode=24&url=%s&)' % (sys.argv[0], url)))
    if "Trailer" in (infolabels) and infolabels["Trailer"] != "":
            contextmen.append(('Ver trailer', 'XBMC.PlayMedia(%s)' % (infolabels["Trailer"])))
    contextmen.append(('Ler Comentários', 'XBMC.RunPlugin(%s?mode=12&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], name, url, iconimage)))
    contextmen.append(('Comentar', 'XBMC.RunPlugin(%s?mode=7&name=%s&url=%s&iconimage=%s)' % (sys.argv[0], name, url, iconimage)))
    if tipo == 'movie':
        visto = check_visto(url)
        try:
            addon_id_trakt = 'script.trakt'
            trakt_addon = xbmcaddon.Addon(id=addon_id_trakt)
            trakt_instalado = True
            trakt_addon.getSetting('username')
        except: trakt_instalado = False
        try:
            if trakt_instalado == True and selfAddon.getSetting("sync-trakt") == "true":
                vistos = trakt_api().return_watched_movies(trakt_addon.getSetting('username'))
                for filme_visto in vistos:
                    if filme_visto["title"] == infolabels['originaltitle'] and str(filme_visto["year"]) == infolabels["Year"]:
                        visto =True
        except: pass
	contextmen.append(('Adicionar à biblioteca', 'XBMC.RunPlugin(%s?mode=49&url=%s&name=%s&iconimage=%s)' % (sys.argv[0], url, name, iconimage)))
    else:
            visto = None
	    if os.path.exists(filename): contextmen.append(('Deixar de seguir série', 'XBMC.RunPlugin(%s?mode=27&url=%s&name=%s&iconimage=%s)' % (sys.argv[0], url, name, iconimage)))
	    else: contextmen.append(('Seguir série', 'XBMC.RunPlugin(%s?mode=25&url=%s&name=%s&iconimage=%s)' % (sys.argv[0], url, name, iconimage)))
	    contextmen.append(('Próximo episódio?', 'XBMC.RunPlugin(%s?mode=28&url=%s&name=%s&iconimage=%s)' % (sys.argv[0], url, name, iconimage)))
	    if not xbmcvfs.exists(os.path.join(datapath,'tvshows-subscriptions',str(id_ratotv)+'.txt')):
	    	contextmen.append(('Subscrever série', 'XBMC.RunPlugin(%s?mode=43&url=%s&name=%s&iconimage=%s)' % (sys.argv[0], url, name, iconimage)))
	    else:
	    	contextmen.append(('Remover subscrição', 'XBMC.RunPlugin(%s?mode=46&url=%s&name=%s&iconimage=%s)' % (sys.argv[0], url, name, iconimage)))
    print visto
    if visto==True:
        contextmen.append(('Marcar como não visto', 'XBMC.RunPlugin(%s?mode=22&url=%s&)' % (sys.argv[0], url)))
        overlay=7
        playcount=1
    elif visto==False: contextmen.append(('Marcar como visto', 'XBMC.RunPlugin(%s?mode=21&url=%s)' % (sys.argv[0], url)))
    if favorito==True: contextmen.append(('Remover dos favoritos', 'XBMC.RunPlugin(%s?mode=17&url=%s)' % (sys.argv[0], url)))
    elif favorito==False: contextmen.append(('Adicionar aos favoritos', 'XBMC.RunPlugin(%s?mode=14&url=%s)' % (sys.argv[0], url)))
    infolabels["overlay"]=overlay
    infolabels["playcount"]=playcount
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    if fanart: liz.setProperty('fanart_image', fanart)
    if HD==True: liz.addStreamInfo('video', { 'Codec': 'h264', 'width': 1280, 'height': 720 })
    elif HD==False:  liz.addStreamInfo('video', { 'Codec': 'h264', 'width': 854, 'height': 480 })
    elif HD=='3D': pass#liz.setProperty('IsStereoscopic',True)
    liz.setInfo( type="Video", infoLabels=infolabels)
    liz.addContextMenuItems(contextmen, replaceItems=True)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=totalit)
    return ok

def addDir_episodio(nomeSerie,title,description,url,temporada,episodio,sources,srt,thumbnail,fanart):
    print nomeSerie,url,season,episode
    if description: episodeName=description
    else: episodeName=title
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=40"+"&iconimage="+urllib.quote_plus(thumbnail)+"&seriesName="+urllib.quote_plus(nomeSerie)+"&name="+urllib.quote_plus(episodeName)+"&sources="+urllib.quote_plus(str(sources))
    try: u+="&originaltitle="+urllib.quote_plus(originaltitle)
    except: u+="&originaltitle="+nomeSerie
    if srt: u+="&srt="+urllib.quote_plus(srt)
    if temporada and episodio: u+='&season='+temporada+'&episode='+episodio
    ok=True
    contextmen = []
    if ADDON.getSetting('download-activo') == "true" and ADDON.getSetting('folder') != "Escolha a pasta":
        contextmen.append(('Download[COLOR red] (Avariado)[/COLOR]', 'XBMC.RunPlugin(%s?mode=31&name=%s&url=%s&iconimage=%s&season=%s&episode=%s&originaltitle=%s&sources=%s&srt=%s)' % (sys.argv[0], name, url, iconimage,temporada,episodio,nomeSerie,urllib.quote_plus(str(sources)),urllib.quote_plus(srt))))
    else: pass
    visto = check_visto(url,temporada,episodio)
    try:
        addon_id_trakt = 'script.trakt'
        trakt_addon = xbmcaddon.Addon(id=addon_id_trakt)
        trakt_instalado = True
        trakt_addon.getSetting('username')
    except: trakt_instalado = False
    try:
        if trakt_instalado == True and selfAddon.getSetting("sync-trakt") == "true":
            vistos = trakt_api().return_watched_shows(trakt_addon.getSetting('username'))
            for serie_name in vistos:
                if serie_name["title"] == originaltitle:
                    print "encontrou",serie_name["title"]
                    print serie_name
                    for season_trakt in serie_name["seasons"]:
                        print "season é",temporada,type(temporada)
                        if season_trakt["season"] == int(temporada): visto = True
    except: pass
    if visto:
        contextmen.append(('Marcar como não visto', 'XBMC.RunPlugin(%s?mode=22&url=%s&season=%s&episode=%s)' % (sys.argv[0], url, temporada, episodio)))
        overlay=7
        playcount=1
    else:
        contextmen.append(('Marcar como visto', 'XBMC.RunPlugin(%s?mode=21&url=%s&season=%s&episode=%s)' % (sys.argv[0], url, temporada, episodio)))
        overlay=6
        playcount=0
    contextmen.append(('Ver detalhes', 'XBMC.Action(Info)')); contextmen.append(('Reportar problema', 'XBMC.RunPlugin(%s?mode=24&url=%s&)' % (sys.argv[0], url)))
    contextmen.append(('Estatísticas Trakt', 'XBMC.RunPlugin(%s?mode=30&name=%s&url=%s&iconimage=%s&season=%s&episode=%s)' % (sys.argv[0], name, url, iconimage,temporada,episodio)))
    if title != [] and description !=[]: titulo = '[COLOR green]' + title + '[/COLOR]' + '-'+ description
    elif title == [] and description !=[]: titulo = description
    elif title !=[] and description == []: titulo = title
    else: titulo = 'N/A'
    liz=xbmcgui.ListItem(titulo, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    if fanart: liz.setProperty('fanart_image', fanart)
    liz.setInfo( type="Video", infoLabels={ "Title": title , "TVShowTitle":name, "Season":temporada, "Episode":episodio, "overlay":overlay, "playcount":playcount} )
    maxRes=720
    if maxRes==1080: liz.addStreamInfo('video', { 'Codec': 'h264', 'width': 1920, 'height': 1080 })
    elif maxRes==720: liz.addStreamInfo('video', { 'Codec': 'h264', 'width': 1280, 'height': 720 })
    elif maxRes==480:  liz.addStreamInfo('video', { 'Codec': 'h264', 'width': 854, 'height': 480 })
    else: liz.addStreamInfo('video', { 'Codec': 'h264', 'width': 640, 'height': 360 })
    liz.addContextMenuItems(contextmen, replaceItems=True)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=1)
    return ok

############################################################################################################
#NAVEGAÇÃO												   #
############################################################################################################

params=get_params()
url=None
name=None
seriesName=None
mode=None
iconimage=None
tipo=None
infolabels_trailer=None
srt=None
season=None
episode=None
fanart=None
imdb_id=None
originaltitle=None
sources=None
dicionario=None
year=None


try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: seriesName=urllib.unquote_plus(params["seriesName"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: tipo=urllib.unquote_plus(params["tipo"])
except: pass
try: infolabels_trailer=urllib.unquote_plus(params["infolabels_trailer"])
except: pass
try: srt=urllib.unquote_plus(params["srt"])
except: pass
try: season=urllib.unquote_plus(params["season"])
except: pass
try: episode=urllib.unquote_plus(params["episode"])
except: pass
try: fanart=urllib.unquote_plus(params["fanart"])
except: pass
try: sources=urllib.unquote_plus(params["sources"])
except: pass
try: imdb_id=urllib.unquote_plus(params["imdb_id"])
except: pass
try: originaltitle=urllib.unquote_plus(params["originaltitle"])
except: pass
try: sources=urllib.unquote_plus(params["sources"])
except: pass
try: subs=urllib.unquote_plus(params["subs"])
except: pass
try: dicionario=urllib.unquote_plus(params["dicionario"])
except: pass
try: year=urllib.unquote_plus(params["year"])
except: pass

print 'mode='+str(mode)
print 'name='+str(name)
print 'imdb_id='+str(imdb_id)
print 'originaltitle='+str(originaltitle)
print 'tipo='+str(tipo)
print 'season='+str(season)
print 'episode='+str(episode)
print 'sources='+str(sources)
print 'srt='+str(srt)
print 'url='+str(url)
print 'dicionario='+str(dicionario)
print 'seriesName='+str(seriesName)
print 'year='+str(year)

###############################################################################################################
# MODOS                                                                                                       #
###############################################################################################################

if mode==None or url==None or len(url)<1:
    print ""
    Menu_principal()
elif mode==1:
    print ""
    Menu_principal_filmes()
elif mode==2: listar_media(url,2)
elif mode==3: stream_qualidade(url,name,iconimage)
elif mode==4: pesquisa(base_url)
elif mode==5: Menu_categorias_filmes()
elif mode==6: filmes_homepage(name,url)
elif mode==7: comment(url)
elif mode==8: Menu_principal_series()
elif mode==9: alterar_definicoes()
elif mode==10: series_seasons(url,name,fanart)
elif mode==11: season_episodes_um(url,name,season,fanart)
elif mode==12: ler_comentarios(url,'')
elif mode==13: pedir_serie_menu()
elif mode==14: add_to_favourites(url)
elif mode==15: listar_favoritos(url)
elif mode==16: listar_pesquisa(url)
elif mode==17: remover_favoritos(url)
elif mode==18: play_trailer(infolabels_trailer)
elif mode==19: votar_ratotv()
elif mode==21: adicionar_visto(url,season,episode)
elif mode==22: remover_visto(url,season,episode)
elif mode==23: play_video(name,url,iconimage,sources,srt,seriesName,season,episode)
elif mode==24: reportar(url)
elif mode==25: adicionar_seguir(url,name,iconimage)
elif mode==26: listar_series_subseguir("seguir")
elif mode==27: deixar_seguir(url)
elif mode==28: proximo_episodio(url)
elif mode==29: pass
elif mode==30: estatisticas_trakt(url)
elif mode==31: download_qualidade(url,name,iconimage)
elif mode==32: season_episodes_dois(url,name,season,fanart)
elif mode==33: menu_pedidos(url)
elif mode==34: pedir_id(url)
elif mode==35: pedir_imdb(url)
elif mode==36: listar_pms()
elif mode==37: ler_pm(url)
elif mode==38: apagar_pm(url)
elif mode==39: listar_temporadas(name,url,fanart,iconimage,dicionario)
elif mode==40: episodios_opcao(name,url,iconimage,sources,srt,originaltitle,season,episode)
elif mode==41: pesquisa_ano(url)
elif mode==42: menu_ano()
elif mode==43: subscrever_serie(name,url,iconimage)
elif mode==44: play_from_outside(name,url)
elif mode==45: listar_series_subseguir("subscritas")
elif mode==46: remover_subscricao_serie(name,url,iconimage)
elif mode==47: transferir_biblioteca_filmes(name)
elif mode==48: procurar_novas_series()
elif mode==49: adicionar_filme_biblioteca(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
