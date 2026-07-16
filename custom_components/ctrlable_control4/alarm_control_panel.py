from __future__ import annotations
_H='PARTITION_STATE'
_G='TROUBLE_TEXT'
_F='DISPLAY_TEXT'
_E='zone_state'
_D=True
_C='id'
_B='text'
_A=None
from functools import cached_property
import logging
from.pyc4.alarm import C4SecurityPanel
import voluptuous
from homeassistant.components.alarm_control_panel import AlarmControlPanelEntity
from homeassistant.components.alarm_control_panel.const import AlarmControlPanelEntityFeature,AlarmControlPanelState,CodeFormat
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv,entity_platform
from.import Control4Entity,get_items_of_category,filter_selected
from.const import CONF_ALARM_ARM_STATES,CONF_ALARM_AWAY_MODE,CONF_ALARM_CUSTOM_BYPASS_MODE,CONF_ALARM_HOME_MODE,CONF_ALARM_NIGHT_MODE,CONF_ALARM_VACATION_MODE,CONF_DIRECTOR,CONTROL4_ENTITY_TYPE,DEFAULT_ALARM_AWAY_MODE,DEFAULT_ALARM_CUSTOM_BYPASS_MODE,DEFAULT_ALARM_HOME_MODE,DEFAULT_ALARM_NIGHT_MODE,DEFAULT_ALARM_VACATION_MODE,DOMAIN
from.director_utils import director_get_entry_variables
_LOGGER=logging.getLogger(__name__)
CONTROL4_CATEGORY='security'
CONTROL4_ARMED_AWAY_VAR='AWAY_STATE'
CONTROL4_ARMED_HOME_VAR='HOME_STATE'
CONTROL4_DISARMED_VAR='DISARMED_STATE'
CONTROL4_ALARM_STATE_VAR='ALARM_STATE'
CONTROL4_DISPLAY_TEXT_VAR=_F
CONTROL4_TROUBLE_TEXT_VAR=_G
CONTROL4_PARTITION_STATE_VAR=_H
CONTROL4_DELAY_TIME_REMAINING_VAR='DELAY_TIME_REMAINING'
CONTROL4_OPEN_ZONE_COUNT_VAR='OPEN_ZONE_COUNT'
CONTROL4_ALARM_TYPE_VAR='ALARM_TYPE'
CONTROL4_ARMED_TYPE_VAR='ARMED_TYPE'
CONTROL4_LAST_EMERGENCY_VAR='LAST_EMERGENCY'
CONTROL4_LAST_ARM_FAILURE_VAR='LAST_ARM_FAILED'
CONTROL4_EXIT_DELAY_STATE='EXIT_DELAY'
CONTROL4_ENTRY_DELAY_STATE='ENTRY_DELAY'
CONTROL4_ARMED_STATE='ARMED'
CONTROL4_DISARMED_NOT_READY_STATE='DISARMED_NOT_READY'
CONTROL4_DISARMED_READY_STATE='DISARMED_READY'
CONTROL4_PARTITION_STATE_DATA_MAPPING={'state':_H,'trouble':_G,_B:_F}
async def async_setup_entry(hass,entry,async_add_entities):
	T='name';S='arm_states';R='send_alarm_keystrokes';G='capabilities';E=hass;B=entry;H=entity_platform.current_platform.get()
	if H is not _A:H.async_register_entity_service(R,{voluptuous.Required('keystrokes'):cv.string},R)
	F=E.data[DOMAIN][B.entry_id];I=await get_items_of_category(E,B,CONTROL4_CATEGORY);J=[];K=F[CONF_DIRECTOR]
	for A in I:
		try:
			if A['type']==CONTROL4_ENTITY_TYPE and A[_C]:
				if G in A and S in A[G]:F[CONF_ALARM_ARM_STATES].update(A[G][S].split(','))
				L=str(A[T]);C=A[_C];U=A['roomName'];M=A['parentId'];N=_A;O=_A;P=_A
				try:V=await K.get_item_setup(C);Q=V.get('setup',{}).get('enabled',_D)
				except(KeyError,TypeError):_LOGGER.debug('No setup info available for device %s, defaulting to enabled',L);Q=_D
				for D in I:
					if D[_C]==M:N=D.get('manufacturer');O=D.get(T);P=D.get('model')
			else:continue
		except KeyError as W:_LOGGER.debug('Unknown device properties received from Control4: %s %s',W,A);continue
		X=await director_get_entry_variables(E,B,C);Y=C4SecurityPanel(K,C);Z=await Y.get_emergency_types();J.append(Control4AlarmControlPanel(F,B,L,C,O,N,P,M,U,X,Q,Z))
	async_add_entities(filter_selected(B,J),_D)
class Control4AlarmControlPanel(Control4Entity,AlarmControlPanelEntity):
	def __init__(A,entry_data,entry,name,idx,device_name,device_manufacturer,device_model,device_id,device_area,device_attributes,is_enabled,emergency_types):super().__init__(entry_data,entry,name,idx,device_name,device_manufacturer,device_model,device_id,device_area,device_attributes);A._is_enabled=is_enabled;A._emergency_types=emergency_types;A._extra_state_attributes[_E]={}
	async def _update_callback(B,device,message):
		H='devicecommand';G='partition_state';F=False;C=message;_LOGGER.debug(C)
		if C is F:B._attr_available=F
		elif C['evtName']=='OnDataToUI':
			B._attr_available=_D;A=C['data']
			if G in A:
				A=A[G]
				for(D,E)in A.items():
					if D in CONTROL4_PARTITION_STATE_DATA_MAPPING:B._extra_state_attributes[CONTROL4_PARTITION_STATE_DATA_MAPPING[D]]=E
					else:B._extra_state_attributes[D.upper()]=E
			elif _B in A:B._extra_state_attributes[CONTROL4_PARTITION_STATE_DATA_MAPPING[_B]]=A[_B]
			elif _E in A:A=A[_E];B._extra_state_attributes[_E][A[_C]]=A
			elif H in A:A=A[H]['params'];await B._data_to_extra_state_attributes(A)
			else:await B._data_to_extra_state_attributes(A)
		_LOGGER.debug('Message for device %s',device);B.async_write_ha_state()
	def create_api_object(A):return C4SecurityPanel(A.entry_data[CONF_DIRECTOR],A._idx)
	@cached_property
	def entity_registry_enabled_default(self):return self._is_enabled
	@cached_property
	def code_format(self):return CodeFormat.NUMBER
	@cached_property
	def supported_features(self):
		B=self;A=AlarmControlPanelEntityFeature(0)
		if not B.entry_data[CONF_ALARM_AWAY_MODE]==DEFAULT_ALARM_AWAY_MODE:A|=AlarmControlPanelEntityFeature.ARM_AWAY
		if not B.entry_data[CONF_ALARM_HOME_MODE]==DEFAULT_ALARM_HOME_MODE:A|=AlarmControlPanelEntityFeature.ARM_HOME
		if not B.entry_data[CONF_ALARM_NIGHT_MODE]==DEFAULT_ALARM_NIGHT_MODE:A|=AlarmControlPanelEntityFeature.ARM_NIGHT
		if not B.entry_data[CONF_ALARM_CUSTOM_BYPASS_MODE]==DEFAULT_ALARM_CUSTOM_BYPASS_MODE:A|=AlarmControlPanelEntityFeature.ARM_CUSTOM_BYPASS
		if not B.entry_data[CONF_ALARM_VACATION_MODE]==DEFAULT_ALARM_VACATION_MODE:A|=AlarmControlPanelEntityFeature.ARM_VACATION
		if B._emergency_types:A|=AlarmControlPanelEntityFeature.TRIGGER
		return A
	@property
	def alarm_state(self):
		A=self;B=A.extra_state_attributes.get(CONTROL4_PARTITION_STATE_VAR)
		if B==CONTROL4_EXIT_DELAY_STATE:return AlarmControlPanelState.ARMING
		if B==CONTROL4_ENTRY_DELAY_STATE:return AlarmControlPanelState.PENDING
		if B==CONTROL4_DISARMED_NOT_READY_STATE or B==CONTROL4_DISARMED_READY_STATE:return AlarmControlPanelState.DISARMED
		if B==CONTROL4_ARMED_STATE:
			C=A.extra_state_attributes.get(CONTROL4_ARMED_TYPE_VAR)
			if C==A.entry_data[CONF_ALARM_AWAY_MODE]:return AlarmControlPanelState.ARMED_AWAY
			if C==A.entry_data[CONF_ALARM_HOME_MODE]:return AlarmControlPanelState.ARMED_HOME
			if C==A.entry_data[CONF_ALARM_NIGHT_MODE]:return AlarmControlPanelState.ARMED_NIGHT
			if C==A.entry_data[CONF_ALARM_CUSTOM_BYPASS_MODE]:return AlarmControlPanelState.ARMED_CUSTOM_BYPASS
			if C==A.entry_data[CONF_ALARM_VACATION_MODE]:return AlarmControlPanelState.ARMED_VACATION
		D=A.extra_state_attributes.get(CONTROL4_ALARM_TYPE_VAR)
		if D:return AlarmControlPanelState.TRIGGERED
	async def async_alarm_arm_away(A,code=_A):B=A.create_api_object();await B.set_arm(code or'',A.entry_data[CONF_ALARM_AWAY_MODE])
	async def async_alarm_arm_home(A,code=_A):B=A.create_api_object();await B.set_arm(code or'',A.entry_data[CONF_ALARM_HOME_MODE])
	async def async_alarm_arm_night(A,code=_A):B=A.create_api_object();await B.set_arm(code or'',A.entry_data[CONF_ALARM_NIGHT_MODE])
	async def async_alarm_arm_custom_bypass(A,code=_A):B=A.create_api_object();await B.set_arm(code or'',A.entry_data[CONF_ALARM_CUSTOM_BYPASS_MODE])
	async def async_alarm_arm_vacation(A,code=_A):B=A.create_api_object();await B.set_arm(code or'',A.entry_data[CONF_ALARM_VACATION_MODE])
	async def async_alarm_disarm(A,code=_A):B=A.create_api_object();await B.set_disarm(code or'')
	async def async_alarm_trigger(A,code=_A):
		if not A._emergency_types:return
		B=A.create_api_object();C=['Police','Fire','Medical','Panic'];D=next((B for B in C if B in A._emergency_types),A._emergency_types[0]);await B.trigger_emergency(D)
	async def send_alarm_keystrokes(A,keystrokes):
		B=A.create_api_object()
		for C in keystrokes:await B.send_key_press(C)