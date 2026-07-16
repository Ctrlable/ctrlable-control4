from __future__ import annotations
_A='RelayState'
import logging
from.pyc4.relay import C4Relay
from homeassistant.components.lock import LockEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from.import Control4Entity,get_items_of_category,filter_selected
from.const import CONF_DIRECTOR,CONTROL4_ENTITY_TYPE,DOMAIN
from.director_utils import director_get_entry_variables
_LOGGER=logging.getLogger(__name__)
CONTROL4_CATEGORY='locks'
async def async_setup_entry(hass,entry,async_add_entities):
	O='name';F=None;E='id';D=hass;B=entry;P=D.data[DOMAIN][B.entry_id];G=await get_items_of_category(D,B,CONTROL4_CATEGORY);H=[]
	for A in G:
		try:
			if A['type']==CONTROL4_ENTITY_TYPE and A[E]:
				Q=str(A[O]);I=A[E];R=A['roomName'];J=A['parentId'];K=F;L=F;M=F
				for C in G:
					if C[E]==J:K=C['manufacturer'];L=C[O];M=C['model']
			else:continue
		except KeyError:_LOGGER.exception('Unknown device properties received from Control4: %s',A);continue
		N=await director_get_entry_variables(D,B,I)
		if _A in N:H.append(Control4Lock(P,B,Q,I,L,K,M,J,R,N))
	async_add_entities(filter_selected(B,H),True)
class Control4Lock(Control4Entity,LockEntity):
	def create_api_object(A):return C4Relay(A.entry_data[CONF_DIRECTOR],A._idx)
	async def _update_callback(A,device,message):
		F=False;E='relay_state';B=message
		if B is F:A._attr_available=F
		elif B['evtName']=='OnDataToUI':
			A._attr_available=True;C=B['data']
			if E in C:
				D=C[E].pop('current_state')
				if D=='CLOSED':A._extra_state_attributes[_A]=1
				elif D=='OPENED':A._extra_state_attributes[_A]=0
				else:_LOGGER.error('Unkonwn relay state %s',D)
				await A._data_to_extra_state_attributes(C[E])
		_LOGGER.debug('Message for device %s',device);A.async_write_ha_state()
	@property
	def is_locked(self):
		if _A in self._extra_state_attributes:return self._extra_state_attributes[_A]==0
	async def async_lock(A,**C):B=A.create_api_object();await B.open()
	async def async_unlock(A,**C):B=A.create_api_object();await B.close()