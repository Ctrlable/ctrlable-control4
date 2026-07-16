from __future__ import annotations
_B='Undefined'
_A='value'
from contextlib import asynccontextmanager
from typing import Any,AsyncGenerator
import aiohttp,asyncio,json
from.error_handling import check_response_for_error
class C4Director:
	def __init__(A,ip,director_bearer_token,session_no_verify_ssl=None):B=director_bearer_token;A.base_url=f"https://{ip}";A.headers={'Authorization':f"Bearer {B}"};A.director_bearer_token=B;A.session=session_no_verify_ssl
	@asynccontextmanager
	async def _get_session(self):
		if self.session is not None:yield self.session
		else:
			async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))as A:yield A
	async def send_get_request(A,uri):
		async with A._get_session()as C:
			async with asyncio.timeout(10):
				async with C.get(A.base_url+uri,headers=A.headers)as D:B=await D.text();check_response_for_error(B);return B
	async def send_post_request(A,uri,command,params,is_async=True):
		C={'async':is_async,'command':command,'tParams':params}
		async with A._get_session()as D:
			async with asyncio.timeout(10):
				async with D.post(A.base_url+uri,headers=A.headers,json=C)as E:B=await E.text();check_response_for_error(B);return B
	async def get_all_items_by_category(A,category):B=await A.send_get_request(f"/api/v1/categories/{category}");C=json.loads(B);return C
	async def get_all_item_info(A):B=await A.send_get_request('/api/v1/items');C=json.loads(B);return C
	async def get_item_info(A,item_id):B=await A.send_get_request(f"/api/v1/items/{item_id}");C=json.loads(B);return C
	async def get_item_setup(A,item_id):B=await A.send_post_request(f"/api/v1/items/{item_id}/commands",'GET_SETUP',{},False);C=json.loads(B);return C
	async def get_item_variables(A,item_id):B=await A.send_get_request(f"/api/v1/items/{item_id}/variables");C=json.loads(B);return C
	async def get_item_variable_value(F,item_id,var_name):
		D=item_id;A=var_name
		if isinstance(A,(tuple,list,set)):A=','.join(A)
		B=await F.send_get_request(f"/api/v1/items/{D}/variables?varnames={A}")
		if B=='[]':raise ValueError(f"Empty response received from Director! The variable {A} doesn't seem to exist for item {D}.")
		C=json.loads(B)
		if not isinstance(C,list)or not C:raise ValueError(f"Invalid response format from Director for variable {A}: {B}")
		E=C[0].get(_A)
		if E==_B:return
		return E
	async def get_all_item_variable_value(E,var_name):
		A=var_name
		if isinstance(A,(tuple,list,set)):A=','.join(A)
		B=await E.send_get_request(f"/api/v1/items/variables?varnames={A}")
		if B=='[]':raise ValueError(f"Empty response received from Director! The variable {A} doesn't seem to exist for any items.")
		C=json.loads(B)
		for D in C:
			if D.get(_A)==_B:D[_A]=None
		return C
	async def get_item_commands(A,item_id):B=await A.send_get_request(f"/api/v1/items/{item_id}/commands");C=json.loads(B);return C
	async def get_item_network(A,item_id):B=await A.send_get_request(f"/api/v1/items/{item_id}/network");C=json.loads(B);return C
	async def get_item_bindings(A,item_id):B=await A.send_get_request(f"/api/v1/items/{item_id}/bindings");C=json.loads(B);return C
	async def get_ui_configuration(A):B=await A.send_get_request('/api/v1/agents/ui_configuration');C=json.loads(B);return C