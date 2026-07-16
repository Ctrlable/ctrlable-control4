from __future__ import annotations
import logging
from typing import Any
from homeassistant.components.cover import CoverEntity,CoverEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from.pyc4.blind import C4Blind
from.import Control4Entity,filter_selected
from.const import CONF_DIRECTOR,CONF_DIRECTOR_ALL_ITEMS,CONTROL4_ENTITY_TYPE,DOMAIN
from.director_utils import director_get_entry_variables
_LOGGER=logging.getLogger(__name__)
_COVER_PROXY_SUBSTRINGS='shade','blind','windowcover','curtain','drap'
async def async_setup_entry(hass,entry,async_add_entities):
	N='name';E=None;D='id';B=entry;F=hass.data[DOMAIN][B.entry_id];G=F[CONF_DIRECTOR_ALL_ITEMS];O={A.get(D):A for A in G if D in A}
	def P(proxy_value):
		A=proxy_value
		if not A or not isinstance(A,str):return False
		B=A.lower();return any(A in B for A in _COVER_PROXY_SUBSTRINGS)
	Q=[A for A in G if A.get('type')==CONTROL4_ENTITY_TYPE and A.get(D)and P(A.get('proxy'))];H=[]
	for A in Q:
		try:
			R=str(A[N]);I=A[D];S=A.get('roomName');J=A['parentId'];K=E;L=E;M=E;C=O.get(J)
			if C:K=C.get('manufacturer');L=C.get(N);M=C.get('model')
		except KeyError:_LOGGER.exception('Unknown device properties received from Control4: %s',A);continue
		T=await director_get_entry_variables(hass,B,I);H.append(Control4Cover(F,B,R,I,L,K,M,J,S,T))
	async_add_entities(filter_selected(B,H),True)
class Control4Cover(Control4Entity,CoverEntity):
	_attr_assumed_state=True;_attr_supported_features=CoverEntityFeature.OPEN|CoverEntityFeature.CLOSE|CoverEntityFeature.STOP
	def create_api_object(A):return C4Blind(A.entry_data[CONF_DIRECTOR],A._idx)
	async def async_added_to_hass(A):await super().async_added_to_hass()
	@property
	def current_cover_position(self):0
	@property
	def is_closed(self):0
	async def async_open_cover(A,**C):B=A.create_api_object();await B.open()
	async def async_close_cover(A,**C):B=A.create_api_object();await B.close()
	async def async_set_cover_position(A,**B):0
	async def async_stop_cover(A,**C):B=A.create_api_object();await B.stop()