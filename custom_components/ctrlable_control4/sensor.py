from __future__ import annotations
_B='light_v2'
_A=None
from dataclasses import dataclass
import logging
from typing import Any,Callable
from homeassistant.components.sensor import SensorEntity,SensorDeviceClass,SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from.import Control4Entity,filter_selected
from.const import DOMAIN,CONTROL4_ENTITY_TYPE,CONF_DIRECTOR_ALL_ITEMS
from.director_utils import director_get_entry_variables
_LOGGER=logging.getLogger(__name__)
@dataclass
class _SensorMap:key:str;name_suffix:str;unit:str|_A;device_class:SensorDeviceClass|_A;state_class:SensorStateClass|_A;value_fn:Callable[[Any],Any]|_A=_A;proxies:set[str]|_A=_A
SENSORS=[_SensorMap(key='CURRENT_POWER',name_suffix='Power',unit='W',device_class=SensorDeviceClass.POWER,state_class=SensorStateClass.MEASUREMENT,proxies={_B}),_SensorMap(key='ENERGY_USED_TODAY',name_suffix='Energy Today',unit='Wh',device_class=SensorDeviceClass.ENERGY,state_class=SensorStateClass.TOTAL_INCREASING,proxies={_B}),_SensorMap(key='ENERGY_USED',name_suffix='Energy',unit='Wh',device_class=SensorDeviceClass.ENERGY,state_class=SensorStateClass.TOTAL,proxies={_B})]
async def async_setup_entry(hass,entry,async_add_entities):
	F='id';C=entry;G=hass.data[DOMAIN][C.entry_id];H=G[CONF_DIRECTOR_ALL_ITEMS];E=[]
	for A in H:
		try:
			if A['type']!=CONTROL4_ENTITY_TYPE or not A.get(F):continue
			I=A[F];O=A['roomName'];J=A['parentId'];K=_A;L=_A;M=_A
			for D in H:
				if D[F]==J:K=D['manufacturer'];L=D['name'];M=D['model']
			N=await director_get_entry_variables(hass,C,I)
			for B in SENSORS:
				if B.key in N and(B.proxies and A.get('proxy')in B.proxies):E.append(Control4AttrSensor(entry_data=G,entry=C,name=B.name_suffix,idx=I,device_name=L,device_manufacturer=K,device_model=M,device_id=J,device_area=O,device_attributes=N,sensor_map=B))
		except Exception:_LOGGER.debug('Skipping invalid light item: %s',A,exc_info=True);continue
	if E:async_add_entities(filter_selected(C,E),True)
class Control4AttrSensor(Control4Entity,SensorEntity):
	_attr_has_entity_name=True;_attr_should_poll=False
	def __init__(A,entry_data,entry,name,idx,device_name,device_manufacturer,device_model,device_id,device_area,device_attributes,sensor_map):B=sensor_map;super().__init__(entry_data,entry,name,idx,device_name,device_manufacturer,device_model,device_id,device_area,device_attributes);A._sm=B;A._attr_unique_id=f"{idx}-{B.key.lower()}";A._attr_native_unit_of_measurement=B.unit;A._attr_device_class=B.device_class;A._attr_state_class=B.state_class;A._attr_entity_registry_visible_default=False
	async def async_added_to_hass(A):await super().async_added_to_hass()
	@property
	def available(self):return super().available and self._sm.key in self.extra_state_attributes
	@property
	def native_value(self):
		A=self;C=A.extra_state_attributes.get(A._sm.key)
		if C is _A:return
		try:B=float(C)
		except(TypeError,ValueError):return
		if A._sm.value_fn:B=A._sm.value_fn(B)
		return B