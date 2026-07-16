from __future__ import annotations
_C='status'
_B=False
_A=None
from typing import Any,Callable
from types import MappingProxyType
import aiohttp,asyncio,socketio_v4 as socketio,logging
from.error_handling import check_response_for_error
_LOGGER=logging.getLogger(__name__)
_NAMESPACE_URI='/api/v1/items/datatoui'
_PROBE_MESSAGE='2probe'
_STATUS_ACK_MESSAGE='2'
class _C4DirectorNamespace(socketio.AsyncClientNamespace):
	def __init__(A,*C,**B):A.url=B.pop('url');A.token=B.pop('token');A.callback=B.pop('callback');A.session=B.pop('session');A.connect_callback=B.pop('connect_callback');A.disconnect_callback=B.pop('disconnect_callback');super().__init__(*C,**B);A.uri=_NAMESPACE_URI;A.subscription_id=_A;A.connected=_B
	async def on_connect(A):
		_LOGGER.debug('Control4 Director socket.io connection established!')
		if A.connect_callback is not _A:await A.connect_callback()
	async def on_disconnect(A):
		A.connected=_B;A.subscription_id=_A;_LOGGER.debug('Control4 Director socket.io disconnected.')
		if A.disconnect_callback is not _A:await A.disconnect_callback()
	async def trigger_event(A,event,*C):
		B=event
		if B=='subscribe':await A.on_subscribe(*C)
		elif B=='connect':await A.on_connect()
		elif B=='disconnect':await A.on_disconnect()
		elif B=='clientId':await A.on_clientId(*C)
		elif B==A.subscription_id:
			D=C[0]
			if _C in D:_LOGGER.debug(f"Status message received from Director: {D[_C]}");await A.emit(_STATUS_ACK_MESSAGE)
			else:await A.callback(C[0])
	async def on_clientId(A,client_id):
		await A.emit(_PROBE_MESSAGE)
		if not A.connected and not A.subscription_id:
			_LOGGER.debug('Fetching subscriptionID from Control4');B=A.session or aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=_B))
			try:
				async with asyncio.timeout(10):
					async with B.get(A.url+A.uri,params={'JWT':A.token,'SubscriptionClient':client_id})as C:
						check_response_for_error(await C.text());E=await C.json();D=E.get('subscriptionId')
						if D is _A:raise ValueError('Failed to get subscription ID from Control4 Director')
						A.connected=True;A.subscription_id=D;await A.emit('startSubscription',A.subscription_id)
			finally:
				if A.session is _A:await B.close()
	async def on_subscribe(A,message):0
class C4Websocket:
	def __init__(A,ip,session_no_verify_ssl=_A,connect_callback=_A,disconnect_callback=_A):A.base_url=f"https://{ip}";A.wss_url=f"wss://{ip}";A.session=session_no_verify_ssl;A.connect_callback=connect_callback;A.disconnect_callback=disconnect_callback;A._item_callbacks=dict();A._sio=_A
	@property
	def item_callbacks(self):return MappingProxyType(self._item_callbacks)
	def add_item_callback(B,item_id,callback):
		C=callback;A=item_id;_LOGGER.debug('Subscribing to updates for item id: %s',A)
		if A not in B._item_callbacks:B._item_callbacks[A]=[]
		if C not in B._item_callbacks[A]:B._item_callbacks[A].append(C)
	def remove_item_callback(A,item_id,callback=_A):
		C=callback;B=item_id
		if B not in A._item_callbacks:return
		if C is _A:del A._item_callbacks[B]
		else:
			try:
				A._item_callbacks[B].remove(C)
				if not A._item_callbacks[B]:del A._item_callbacks[B]
			except ValueError:pass
	async def sio_connect(A,director_bearer_token):
		B=director_bearer_token;await A.sio_disconnect()
		if A.session is not _A:C=aiohttp.ClientSession(connector=A.session.connector,connector_owner=_B);A._sio=socketio.AsyncClient(ssl_verify=True,http_session=C)
		else:A._sio=socketio.AsyncClient(ssl_verify=_B)
		A._sio.register_namespace(_C4DirectorNamespace(token=B,url=A.base_url,callback=A._callback,session=A.session,connect_callback=A.connect_callback,disconnect_callback=A.disconnect_callback));await A._sio.connect(A.wss_url,transports=['websocket'],headers={'JWT':B})
	async def sio_disconnect(A):
		if isinstance(A._sio,socketio.AsyncClient):await A._sio.disconnect()
	async def _callback(B,message):
		A=message
		if _C in A:_LOGGER.debug(f"Subscription {A[_C]}");return
		if isinstance(A,list):
			for C in A:await B._process_message(C)
		else:await B._process_message(A)
	async def _process_message(E,message):
		A=message;_LOGGER.debug(A);B=A.get('iddevice')if isinstance(A,dict)else _A
		if B is _A:_LOGGER.debug('Received message without iddevice field');return
		C=E._item_callbacks.get(B,[])
		if not C:_LOGGER.debug(f"No Callback for device id {B}");return
		for D in C[:]:
			try:
				if isinstance(A,list):
					for F in A:await D(B,F)
				else:await D(B,A)
			except Exception as G:_LOGGER.warning(f"Captured exception during callback: {str(G)}")