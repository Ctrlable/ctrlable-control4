from __future__ import annotations
_B=False
_A=None
from functools import cached_property
import logging
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import ATTR_TARGET_TEMP_HIGH,ATTR_TARGET_TEMP_LOW,FAN_AUTO,FAN_DIFFUSE,FAN_ON,ClimateEntityFeature,HVACAction,HVACMode
from homeassistant.const import ATTR_TEMPERATURE,UnitOfTemperature,PRECISION_WHOLE
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from.pyc4.climate import C4Climate
from.import Control4Entity,get_items_of_category,filter_selected
from.const import CONF_DIRECTOR,CONTROL4_ENTITY_TYPE,DOMAIN
from.director_utils import director_get_entry_variables
_LOGGER=logging.getLogger(__name__)
CONTROL4_CATEGORY='comfort'
CONTROL4_PROXY={'control4_thermostat_proxy','thermostatV2'}
CONTROL4_HVAC_MODE_OFF='Off'
CONTROL4_HVAC_MODE_HEAT='Heat'
CONTROL4_HVAC_MODE_COOL='Cool'
CONTROL4_HVAC_MODE_HEAT_COOL='Auto'
CONTROL4_HVAC_MODE_AUX_HEAT='Emergency Heat'
CONTROL4_FAN_MODE_ON='On'
CONTROL4_FAN_MODE_AUTO='Auto'
CONTROL4_FAN_MODE_DIFFUSE='Circulate'
MIN_TEMP_RANGE=2
CONTROL4_HVAC_MODES={HVACMode.OFF:CONTROL4_HVAC_MODE_OFF,HVACMode.HEAT:CONTROL4_HVAC_MODE_HEAT,HVACMode.COOL:CONTROL4_HVAC_MODE_COOL,HVACMode.HEAT_COOL:CONTROL4_HVAC_MODE_HEAT_COOL}
HVAC_MODES={CONTROL4_HVAC_MODE_OFF:HVACMode.OFF,CONTROL4_HVAC_MODE_HEAT:HVACMode.HEAT,CONTROL4_HVAC_MODE_AUX_HEAT:HVACMode.HEAT,CONTROL4_HVAC_MODE_COOL:HVACMode.COOL,CONTROL4_HVAC_MODE_HEAT_COOL:HVACMode.HEAT_COOL}
CONTROL4_FAN_MODES={FAN_ON:CONTROL4_FAN_MODE_ON,FAN_AUTO:CONTROL4_FAN_MODE_AUTO,FAN_DIFFUSE:CONTROL4_FAN_MODE_DIFFUSE}
FAN_MODES={CONTROL4_FAN_MODE_ON:FAN_ON,CONTROL4_FAN_MODE_AUTO:FAN_AUTO,CONTROL4_FAN_MODE_DIFFUSE:FAN_DIFFUSE}
ATTR_HUMIDITY='HUMIDITY'
ATTR_TEMPERATURE_F='TEMPERATURE_F'
ATTR_TEMPERATURE_C='TEMPERATURE_C'
ATTR_FAN_MODE='FAN_MODE'
ATTR_FAN_STATE='FAN_STATE'
ATTR_FAN_MODES_LIST='FAN_MODES_LIST'
ATTR_HVAC_STATE='HVAC_STATE'
ATTR_HVAC_MODE='HVAC_MODE'
ATTR_HVAC_MODES_LIST='HVAC_MODES_LIST'
ATTR_HOLD_MODE='HOLD_MODE'
ATTR_HOLD_MODES_LIST='HOLD_MODES_LIST'
ATTR_SETPOINT_HEAT_F='SETPOINT_HEAT_F'
ATTR_HEAT_SETPOINT_F='HEAT_SETPOINT_F'
ATTR_SETPOINT_HEAT_C='SETPOINT_HEAT_C'
ATTR_HEAT_SETPOINT_C='HEAT_SETPOINT_C'
ATTR_SETPOINT_COOL_F='SETPOINT_COOL_F'
ATTR_COOL_SETPOINT_F='COOL_SETPOINT_F'
ATTR_SETPOINT_COOL_C='SETPOINT_COOL_C'
ATTR_COOL_SETPOINT_C='COOL_SETPOINT_C'
ATTR_SCALE='SCALE'
SETUP_HAS_HUMIDITY='has_humidity'
SETUP_CURRENT_TEMP_RES_F='current_temperature_resolution_f'
SETUP_CURRENT_TEMP_RES_C='current_temperature_resolution_c'
SETUP_SETPOINT_HEAT_RES_F='setpoint_heat_resolution_f'
SETUP_SETPOINT_COOL_RES_F='setpoint_cool_resolution_f'
SETUP_SETPOINT_HEAT_RES_C='setpoint_heat_resolution_c'
SETUP_SETPOINT_COOL_RES_C='setpoint_cool_resolution_c'
SETUP_SETPOINT_DEADBAND_F='setpoint_heatcool_deadband_f'
SETUP_SETPOINT_DEADBAND_C='setpoint_heatcool_deadband_c'
async def async_setup_entry(hass,entry,async_add_entities):
	O='name';D=hass;B=entry;F=D.data[DOMAIN][B.entry_id];P=F[CONF_DIRECTOR];G=await get_items_of_category(D,B,CONTROL4_CATEGORY);H=[]
	for A in G:
		try:
			if A['type']==CONTROL4_ENTITY_TYPE and A['proxy']in CONTROL4_PROXY:
				I=A[O];_LOGGER.debug('Climate Setup Name: %s',str(I));E=A['id'];Q=A['roomName'];J=A['parentId'];K=_A;L=_A;M=_A
				for C in G:
					if C['id']==J:K=C['manufacturer'];L=C[O];M=C['model']
				N=await P.get_item_setup(E);_LOGGER.debug('Climate Setup: %s',str(N))
			else:continue
		except KeyError:_LOGGER.exception('Unknown device properties received from Control4: %s',A);continue
		R=await director_get_entry_variables(D,B,E);H.append(Control4Climate(F,B,I,E,L,K,M,J,Q,R,N.get('thermostat_setup')))
	async_add_entities(filter_selected(B,H),True)
class Control4Climate(Control4Entity,ClimateEntity):
	def __init__(A,entry_data,entry,name,idx,device_name,device_manufacturer,device_model,device_id,device_area,device_attributes,thermostat_setup):
		B=thermostat_setup;super().__init__(entry_data,entry,name,idx,device_name,device_manufacturer,device_model,device_id,device_area,device_attributes)
		if isinstance(B,dict):A._thermostat_setup=B
		else:A._thermostat_setup={}
		A._aux_heat_active=_B
	def create_api_object(A):return C4Climate(A.entry_data[CONF_DIRECTOR],A._idx)
	@property
	def current_humidity(self):
		if self._thermostat_setup.get(SETUP_HAS_HUMIDITY,_B)is _B:return
		return self._extra_state_attributes.get(ATTR_HUMIDITY)
	@property
	def current_temperature(self):
		A=self
		if A.temperature_unit==UnitOfTemperature.FAHRENHEIT:return A._extra_state_attributes.get(ATTR_TEMPERATURE_F)
		return A._extra_state_attributes.get(ATTR_TEMPERATURE_C)
	@property
	def fan_mode(self):
		A=self._extra_state_attributes.get(ATTR_FAN_MODE)
		if A in FAN_MODES:return FAN_MODES[A]
	@property
	def fan_modes(self):
		A=self._extra_state_attributes.get(ATTR_FAN_MODES_LIST)
		if A:B=A.split(',');return[FAN_MODES[A]for A in B if A in FAN_MODES]
		return list(FAN_MODES.values())
	@property
	def preset_modes(self):
		A=self._extra_state_attributes.get(ATTR_HOLD_MODES_LIST)
		if A:return A.split(',')
	@property
	def preset_mode(self):return self._extra_state_attributes.get(ATTR_HOLD_MODE)
	@property
	def hvac_action(self):
		A=self._extra_state_attributes.get(ATTR_HVAC_STATE,'')
		if'Cool'in A:return HVACAction.COOLING
		if'Heat'in A:return HVACAction.HEATING
		B=self._extra_state_attributes.get(ATTR_FAN_STATE,'')
		if'on'in B.lower():return HVACAction.FAN
		return HVACAction.OFF
	@property
	def hvac_mode(self):
		A=self._extra_state_attributes.get(ATTR_HVAC_MODE,'')
		if A==''or A not in HVAC_MODES:return HVACMode.OFF
		return HVAC_MODES[A]
	@property
	def hvac_modes(self):
		A=[];C=self._extra_state_attributes.get(ATTR_HVAC_MODES_LIST,'');D=C.split(',')if C else[];_LOGGER.debug('c4modes = %s',C)
		for B in D:
			_LOGGER.debug('a_c4mode = %s',B)
			if B in HVAC_MODES and HVAC_MODES[B]not in A:A.append(HVAC_MODES[B])
		if len(A)==0:A.append(HVACMode.OFF)
		return A
	def _get_heat_setpoint(A):
		if A.temperature_unit==UnitOfTemperature.FAHRENHEIT:
			if ATTR_SETPOINT_HEAT_F in A._extra_state_attributes:return A._extra_state_attributes.get(ATTR_SETPOINT_HEAT_F)
			if ATTR_HEAT_SETPOINT_F in A._extra_state_attributes:return A._extra_state_attributes.get(ATTR_HEAT_SETPOINT_F)
		else:
			if ATTR_SETPOINT_HEAT_C in A._extra_state_attributes:return A._extra_state_attributes.get(ATTR_SETPOINT_HEAT_C)
			if ATTR_HEAT_SETPOINT_C in A._extra_state_attributes:return A._extra_state_attributes.get(ATTR_HEAT_SETPOINT_C)
	def _get_cool_setpoint(A):
		if A.temperature_unit==UnitOfTemperature.FAHRENHEIT:
			if ATTR_SETPOINT_COOL_F in A._extra_state_attributes:return A._extra_state_attributes.get(ATTR_SETPOINT_COOL_F)
			if ATTR_COOL_SETPOINT_F in A._extra_state_attributes:return A._extra_state_attributes.get(ATTR_COOL_SETPOINT_F)
		else:
			if ATTR_SETPOINT_COOL_C in A._extra_state_attributes:return A._extra_state_attributes.get(ATTR_SETPOINT_COOL_C)
			if ATTR_COOL_SETPOINT_C in A._extra_state_attributes:return A._extra_state_attributes.get(ATTR_COOL_SETPOINT_C)
	@property
	def target_temperature(self):
		A=self
		if A.hvac_mode==HVACMode.HEAT:return A._get_heat_setpoint()
		if A.hvac_mode==HVACMode.COOL:return A._get_cool_setpoint()
	@property
	def target_temperature_high(self):
		if self.hvac_mode!=HVACMode.HEAT_COOL:return
		return self._get_cool_setpoint()
	@property
	def target_temperature_low(self):
		if self.hvac_mode!=HVACMode.HEAT_COOL:return
		return self._get_heat_setpoint()
	@property
	def temperature_unit(self):
		A=self._extra_state_attributes.get(ATTR_SCALE,'')
		if'f'in A.lower():return UnitOfTemperature.FAHRENHEIT
		return UnitOfTemperature.CELSIUS
	@property
	def precision(self):
		A=self
		if isinstance(A._thermostat_setup,dict):
			if A.temperature_unit==UnitOfTemperature.FAHRENHEIT:
				B=A._thermostat_setup.get(SETUP_CURRENT_TEMP_RES_F)
				if B is not _A:return B
			if A.temperature_unit==UnitOfTemperature.CELSIUS:
				B=A._thermostat_setup.get(SETUP_CURRENT_TEMP_RES_C)
				if B is not _A:return B
		return PRECISION_WHOLE
	@property
	def target_temperature_step(self):
		A=self
		if isinstance(A._thermostat_setup,dict):
			if A.temperature_unit==UnitOfTemperature.FAHRENHEIT:
				B=A._thermostat_setup.get(SETUP_SETPOINT_HEAT_RES_F)or A._thermostat_setup.get(SETUP_SETPOINT_COOL_RES_F)
				if B is not _A:return B
			if A.temperature_unit==UnitOfTemperature.CELSIUS:
				B=A._thermostat_setup.get(SETUP_SETPOINT_HEAT_RES_C)or A._thermostat_setup.get(SETUP_SETPOINT_COOL_RES_C)
				if B is not _A:return B
		return PRECISION_WHOLE
	@cached_property
	def supported_features(self):A=ClimateEntityFeature.TARGET_TEMPERATURE|ClimateEntityFeature.FAN_MODE|ClimateEntityFeature.TARGET_TEMPERATURE_RANGE|ClimateEntityFeature.PRESET_MODE;return A
	async def async_set_hvac_mode(C,hvac_mode):
		A=hvac_mode;B=C.create_api_object();_LOGGER.debug('set new hvac mode: %s',A)
		if A==HVACMode.HEAT:
			if C._aux_heat_active:_LOGGER.debug('set hvac mode with aux: %s',A);await B.set_hvac_mode(CONTROL4_HVAC_MODE_AUX_HEAT)
			else:await B.set_hvac_mode(CONTROL4_HVAC_MODE_HEAT)
		elif A in CONTROL4_HVAC_MODES:await B.set_hvac_mode(CONTROL4_HVAC_MODES[A])
		else:_LOGGER.exception('Request for unsupported hvac mode received:: %s',A)
	async def async_set_fan_mode(B,fan_mode):
		A=fan_mode;C=B.create_api_object()
		if A in CONTROL4_FAN_MODES:await C.set_fan_mode(CONTROL4_FAN_MODES[A])
		else:_LOGGER.exception('Request for unsupported fan mode received:: %s',A)
	async def async_set_preset_mode(A,preset_mode):B=A.create_api_object();await B.set_hold_mode(preset_mode)
	async def _set_cool_setpoint(B,temp):
		A=temp;C=B.create_api_object()
		if B.target_temperature_step>=1:A=int(A)
		if B.temperature_unit==UnitOfTemperature.FAHRENHEIT:await C.set_cool_setpoint_f(A)
		else:await C.set_cool_setpoint_c(A)
	async def _set_heat_setpoint(B,temp):
		A=temp;C=B.create_api_object()
		if B.target_temperature_step>=1:A=int(A)
		if B.temperature_unit==UnitOfTemperature.FAHRENHEIT:await C.set_heat_setpoint_f(A)
		else:await C.set_heat_setpoint_c(A)
	def _get_setpoint_deadband(A):
		if isinstance(A._thermostat_setup,dict):
			if A.temperature_unit==UnitOfTemperature.FAHRENHEIT:
				B=A._thermostat_setup.get(SETUP_SETPOINT_DEADBAND_F)
				if B is not _A:return B
			if A.temperature_unit==UnitOfTemperature.CELSIUS:
				B=A._thermostat_setup.get(SETUP_SETPOINT_DEADBAND_C)
				if B is not _A:return B
		return MIN_TEMP_RANGE
	async def async_set_temperature(A,**E):
		C=E.get(ATTR_TARGET_TEMP_LOW);B=E.get(ATTR_TARGET_TEMP_HIGH);D=E.get(ATTR_TEMPERATURE)
		if A.hvac_mode==HVACMode.HEAT_COOL:
			if C and B:
				if B-C<A._get_setpoint_deadband():
					if abs(B-A.target_temperature_high)<.01:B=C+A._get_setpoint_deadband()
					else:C=B-A._get_setpoint_deadband()
				await A._set_heat_setpoint(C);await A._set_cool_setpoint(B)
		elif A.hvac_mode==HVACMode.COOL and D:await A._set_cool_setpoint(D)
		elif A.hvac_mode==HVACMode.HEAT and D:await A._set_heat_setpoint(D)
	async def async_turn_aux_heat_on(A):
		A._aux_heat_active=True
		if A.hvac_mode==HVACMode.HEAT:await A.async_set_hvac_mode(HVACMode.HEAT)
	async def async_turn_aux_heat_off(A):
		A._aux_heat_active=_B
		if A.hvac_mode==HVACMode.HEAT:await A.async_set_hvac_mode(HVACMode.HEAT)