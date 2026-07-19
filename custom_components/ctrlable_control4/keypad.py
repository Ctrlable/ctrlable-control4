from __future__ import annotations
_K='action'
_J='button_name'
_I='press'
_H='rgb_color'
_G='buttons'
_F='_keypad_registry'
_E='button'
_D='keypad_name'
_C='number'
_B='name'
_A='keypad_id'
import logging
from typing import Any
import voluptuous as vol
from homeassistant.core import HomeAssistant,ServiceCall,callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.storage import Store
from.const import DOMAIN
_LOGGER=logging.getLogger(__name__)
KEYPAD_EVENT='ctrlable_control4_keypad_event'
SIGNAL_ADD_KEYPAD_LED='ctrlable_control4_add_keypad_led'
SIGNAL_ADD_KEYPAD_EVENT='ctrlable_control4_add_keypad_event'
SIGNAL_KEYPAD_BUTTON='ctrlable_control4_keypad_button_{}_{}'
VALID_ACTIONS=_I,'release','hold','hold_release','double_tap','click','triple_tap'
_STORAGE_VERSION=1
_STORAGE_KEY='ctrlable_control4_keypads'
SERVICE_REGISTER_KEYPAD='register_keypad'
SERVICE_KEYPAD_EVENT='keypad_event'
SERVICE_SET_BUTTON_LED='set_button_led'
_BUTTON_SCHEMA=vol.Schema({vol.Required(_C):vol.Coerce(int),vol.Optional(_B):cv.string})
REGISTER_KEYPAD_SCHEMA=vol.Schema({vol.Required(_A):cv.string,vol.Optional(_D):cv.string,vol.Required(_G):vol.All(cv.ensure_list,[_BUTTON_SCHEMA])})
KEYPAD_EVENT_SCHEMA=vol.Schema({vol.Required(_A):cv.string,vol.Required(_E):vol.Coerce(int),vol.Optional(_J):cv.string,vol.Optional(_K,default=_I):vol.In(VALID_ACTIONS)})
SET_BUTTON_LED_SCHEMA=vol.Schema({vol.Required(_A):cv.string,vol.Required(_E):vol.Coerce(int),vol.Required('state'):cv.boolean,vol.Optional(_H):vol.All(cv.ensure_list,[vol.All(vol.Coerce(int),vol.Range(min=0,max=255))],vol.Length(min=3,max=3))})
class KeypadRegistry:
	def __init__(A,hass):A.hass=hass;A._store=Store(hass,_STORAGE_VERSION,_STORAGE_KEY);A.keypads={}
	async def async_load(A):A.keypads=await A._store.async_load()or{}
	async def async_save(A):await A._store.async_save(A.keypads)
	def get(A,keypad_id):return A.keypads.get(keypad_id)
	async def async_upsert(B,keypad_id,keypad_name,buttons):A=keypad_id;C={_A:A,_D:keypad_name or A,_G:[{_C:int(A[_C]),_B:A.get(_B)or f"Button {A[_C]}"}for A in buttons]};B.keypads[A]=C;await B.async_save();return C
def _registry(hass):return hass.data[DOMAIN][_F]
async def async_setup_keypads(hass):
	A=hass;A.data.setdefault(DOMAIN,{})
	if _F in A.data[DOMAIN]:return
	C=KeypadRegistry(A);await C.async_load();A.data[DOMAIN][_F]=C
	async def B(call):D=call;B=await C.async_upsert(D.data[_A],D.data.get(_D,''),D.data[_G]);_LOGGER.info('Registered Control4 keypad %s (%d buttons)',B[_A],len(B[_G]));async_dispatcher_send(A,SIGNAL_ADD_KEYPAD_LED,B);async_dispatcher_send(A,SIGNAL_ADD_KEYPAD_EVENT,B)
	@callback
	def D(call):D=call;B=D.data[_A];E=int(D.data[_E]);F=D.data.get(_K,_I);_LOGGER.debug('keypad_event keypad_id=%s button=%s action=%s',B,E,F);G={_A:B,_D:(C.get(B)or{}).get(_D,B),_E:E,_J:D.data.get(_J),_K:F};A.bus.async_fire(KEYPAD_EVENT,G);async_dispatcher_send(A,SIGNAL_KEYPAD_BUTTON.format(B,E),F)
	async def E(call):
		B=call;E=B.data[_A];F=int(B.data[_E]);C=B.data['state'];G=f"light.ctrlable_c4_kp_{E}_led_{F}";D={'entity_id':G}
		if C and _H in B.data:D[_H]=B.data[_H]
		await A.services.async_call('light','turn_on'if C else'turn_off',D,blocking=False)
	A.services.async_register(DOMAIN,SERVICE_REGISTER_KEYPAD,B,schema=REGISTER_KEYPAD_SCHEMA);A.services.async_register(DOMAIN,SERVICE_KEYPAD_EVENT,D,schema=KEYPAD_EVENT_SCHEMA);A.services.async_register(DOMAIN,SERVICE_SET_BUTTON_LED,E,schema=SET_BUTTON_LED_SCHEMA)
def known_keypads(hass):A=hass.data.get(DOMAIN,{}).get(_F);return list(A.keypads.values())if A else[]
_KEYPAD_PROXIES='keypad_proxy',
_KEYPAD_ENTITY_TYPE=7
def _extract_buttons(commands):
	for A in commands or[]:
		if not isinstance(A,dict)or A.get('command')!='KEYPAD_BUTTON_INFO':continue
		for B in A.get('params',[]):
			if B.get(_B)!='BUTTON_ID'or B.get('type')!='LIST':continue
			C=[]
			for D in B.get('values',[]):
				try:E=int(D['id'])
				except(KeyError,TypeError,ValueError):continue
				C.append({_C:E,_B:(D.get(_B)or f"Button {E}").strip()})
			if C:return C
	return[]
async def async_discover_keypads(hass,entry):
	C=hass;from.const import CONF_DIRECTOR as M,CONF_DIRECTOR_ALL_ITEMS as N;E=C.data[DOMAIN][entry.entry_id];F=C.data[DOMAIN].get(_F);G=E.get(M)
	if F is None or G is None:return 0
	O=E.get(N,[])or[];H=0
	for A in O:
		if not isinstance(A,dict):continue
		if A.get('proxy')not in _KEYPAD_PROXIES:continue
		if A.get('type')!=_KEYPAD_ENTITY_TYPE:continue
		B=A.get('id')
		if not B:continue
		try:P=await G.get_item_commands(B)
		except Exception as Q:_LOGGER.debug('Keypad %s: could not read commands (%s)',B,Q);continue
		D=_extract_buttons(P)
		if not D:continue
		I=(A.get('roomName')or'').strip();J=(A.get(_B)or f"Keypad {B}").strip();K=f"{I} {J}".strip()if I else J;L=await F.async_upsert(str(B),K,D);async_dispatcher_send(C,SIGNAL_ADD_KEYPAD_LED,L);async_dispatcher_send(C,SIGNAL_ADD_KEYPAD_EVENT,L);H+=1;_LOGGER.info("Auto-discovered Control4 keypad %s '%s' (%d buttons)",B,K,len(D))
	return H