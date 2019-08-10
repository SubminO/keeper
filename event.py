import socket
import os

from flask_login import login_required

from front import application
from front.lib.handlers import route
# from front.lib import navdata
from . import websocket

@websocket.route('/tdata_free')
def get_track_data_free(ws):
	"""
	основной метод отдачи данных по транспорту
	"""
	client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	sock_path = application.config.get("EGTS_DATA_SOCK")
	chunk_size = application.config.get("EGTS_DATA_CHUNK_SIZE")

	try:
		client.connect(sock_path)
	except socket.error as msg:
		print("socket connecton error", msg)
		return

	try:
		while ws.connected:
			data = client.recv(chunk_size)
			if data:
				json = data.decode("utf-8").replace("][", ",")
				ws.send(route.get_info(json))
			else:
				break
	finally:
		client.close()


@websocket.route('/tdata_full')
@login_required
def get_track_data_full(ws):
	"""
	основной метод отдачи данных по транспорту
	"""
	ws.send("PONG")
