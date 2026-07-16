from __future__ import annotations
from homeassistant.components.event import EventEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant,callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from.const import CONF_CONTROLLER_UNIQUE_ID,DOMAIN
from.keypad import SIGNAL_ADD_KEYPAD_EVENT,SIGNAL_KEYPAD_BUTTON,VALID_ACTIONS,known_keypads
async def async_setup_entry(hass,entry,async_add_entities):
	B=entry;A=hass;D=A.data[DOMAIN][B.entry_id][CONF_CONTROLLER_UNIQUE_ID]
	@callback
	def C(keypad):A=keypad;async_add_entities(C4KeypadButtonEvent(D,A,B)for B in A['buttons'])
	for E in known_keypads(A):C(E)
	B.async_on_unload(async_dispatcher_connect(A,SIGNAL_ADD_KEYPAD_EVENT,C))
class C4KeypadButtonEvent(EventEntity):
	_attr_has_entity_name=True;_attr_should_poll=False;_attr_event_types=list(VALID_ACTIONS)
	def __init__(A,controller_unique_id,keypad,button):D=button;C=keypad;B=controller_unique_id;A._keypad_id=C['keypad_id'];A._button=int(D['number']);A._controller_unique_id=B;A._attr_name=D.get('name')or f"Button {A._button}";A._attr_unique_id=f"c4kp_{A._keypad_id}_event_{A._button}";A._attr_device_info=DeviceInfo(identifiers={(DOMAIN,f"keypad_{A._keypad_id}")},manufacturer='Control4',name=C.get('keypad_name')or A._keypad_id,via_device=(DOMAIN,B))
	async def async_added_to_hass(A):await super().async_added_to_hass();A.async_on_remove(async_dispatcher_connect(A.hass,SIGNAL_KEYPAD_BUTTON.format(A._keypad_id,A._button),A._on_action))
	@callback
	def _on_action(self,action):self._trigger_event(action);self.async_write_ha_state()