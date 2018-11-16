import requests
url_imagen = "http://www.fcv.org/img/app/capercio.jpg"
nombre_local_imagen = "Captura.ppm"
imagen = requests.get(url_imagen).content
with open(nombre_local_imagen, 'wb') as handler:
	handler.write(imagen)