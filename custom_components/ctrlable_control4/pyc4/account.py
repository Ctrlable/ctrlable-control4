from __future__ import annotations
_G='authToken'
_F='The account bearer token is missing. Is your username/password correct?'
_E='Authorization'
_D='osVersion'
_C=' Response: '
_B='token'
_A=None
from contextlib import asynccontextmanager
from typing import Any,AsyncGenerator
import aiohttp,asyncio,json,logging
from.error_handling import check_response_for_error
AUTHENTICATION_ENDPOINT='https://apis.control4.com/authentication/v1/rest'
CONTROLLER_AUTHORIZATION_ENDPOINT='https://apis.control4.com/authentication/v1/rest/authorization'
GET_CONTROLLERS_ENDPOINT='https://apis.control4.com/account/v3/rest/accounts'
APPLICATION_KEY='78f6791373d61bea49fdb9fb8897f1f3af193f11'
_LOGGER=logging.getLogger(__name__)
class C4Account:
	def __init__(A,username,password,session=_A):A.username=username;A.password=password;A.session=session
	@asynccontextmanager
	async def _get_session(self):
		if self.session is not _A:yield self.session
		else:
			async with aiohttp.ClientSession()as A:yield A
	async def _send_account_auth_request(A):
		C='Ctrlable Control4';D={'clientInfo':{'device':{'deviceName':C,'deviceUUID':'0000000000000000','make':'Ctrlable','model':C,'os':'Android',_D:'10'},'userInfo':{'applicationKey':APPLICATION_KEY,'password':A.password,'userName':A.username}}}
		async with A._get_session()as E:
			async with asyncio.timeout(10):
				async with E.post(AUTHENTICATION_ENDPOINT,json=D)as F:B=await F.text();check_response_for_error(B);return B
	async def _send_account_get_request(A,uri):
		try:C={_E:f"Bearer {A.account_bearer_token}"}
		except AttributeError:D=_F;_LOGGER.error(D);raise
		async with A._get_session()as E:
			async with asyncio.timeout(10):
				async with E.get(uri,headers=C)as F:B=await F.text();check_response_for_error(B);return B
	async def _send_controller_auth_request(A,controller_common_name):
		try:C={_E:f"Bearer {A.account_bearer_token}"}
		except AttributeError:D=_F;_LOGGER.error(D);raise
		E={'serviceInfo':{'commonName':controller_common_name,'services':'director'}}
		async with A._get_session()as F:
			async with asyncio.timeout(10):
				async with F.post(CONTROLLER_AUTHORIZATION_ENDPOINT,headers=C,json=E)as G:B=await G.text();check_response_for_error(B);return B
	async def get_account_bearer_token(A):
		B=await A._send_account_auth_request();D=json.loads(B)
		try:C=D[_G][_B];A.account_bearer_token=C;return C
		except KeyError:E='Did not receive an account bearer token. Is your username/password correct?';_LOGGER.error(E+B);raise
	async def get_account_controllers(B):
		A=await B._send_account_get_request(GET_CONTROLLERS_ENDPOINT);C=json.loads(A)
		try:D=C['account'];return D
		except KeyError:E='Did not receive account information from the Control4 API.';_LOGGER.error(E+_C+A);raise
	async def get_controller_info(A,controller_href):B=await A._send_account_get_request(controller_href);C=json.loads(B);return C
	async def get_controller_os_version(B,controller_href):
		A=await B._send_account_get_request(controller_href+'/controller');C=json.loads(A)
		try:D=C[_D];return D
		except KeyError:E='Did not receive OS version from the Control4 API.';_LOGGER.error(E+_C+A);raise
	async def get_director_bearer_token(F,controller_common_name):
		E='validSeconds';A=await F._send_controller_auth_request(controller_common_name);G=json.loads(A)
		try:
			B=G.get(_G,{});C=B.get(_B);D=B.get(E)
			if C is _A or D is _A:raise KeyError('Missing token or validSeconds in authToken')
			return{_B:C,E:D}
		except KeyError:H='Did not receive a director bearer token from the Control4 API.';_LOGGER.error(H+_C+A);raise