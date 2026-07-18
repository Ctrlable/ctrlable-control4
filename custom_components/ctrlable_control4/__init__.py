from __future__ import annotations
_F='parent item id'
_E='item id'
_D='OnDataToUI'
_C='evtName'
_B=False
_A=True
import asyncio,logging
from functools import cached_property
from typing import Any
import random
from aiohttp import client_exceptions
from.pyc4.account import C4Account
from.pyc4.director import C4Director
from.pyc4.error_handling import BadCredentials,InvalidCategory
from.pyc4.websocket import C4Websocket
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST,CONF_PASSWORD,CONF_TOKEN,CONF_USERNAME,Platform,CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed,ConfigEntryNotReady
from homeassistant.helpers import aiohttp_client,device_registry as dr,entity_registry as er
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.update_coordinator import CoordinatorEntity,DataUpdateCoordinator
from.const import CONF_ACCOUNT,CONF_ALARM_ARM_STATES,CONF_ALARM_AWAY_MODE,CONF_ALARM_CUSTOM_BYPASS_MODE,CONF_ALARM_HOME_MODE,CONF_ALARM_NIGHT_MODE,CONF_ALARM_VACATION_MODE,CONF_CANCEL_TOKEN_REFRESH_CALLBACK,CONF_CONFIG_LISTENER,CONF_CONTROLLER_UNIQUE_ID,CONF_LICENSE_TASK,CONF_DIRECTOR,CONF_DIRECTOR_ALL_ITEMS,CONF_DIRECTOR_MODEL,CONF_DIRECTOR_SW_VERSION,CONF_WEBSOCKET,CONF_UI_CONFIGURATION,DEFAULT_ALARM_AWAY_MODE,DEFAULT_ALARM_CUSTOM_BYPASS_MODE,DEFAULT_ALARM_HOME_MODE,DEFAULT_ALARM_NIGHT_MODE,DEFAULT_ALARM_VACATION_MODE,DEFAULT_SCAN_INTERVAL,DOMAIN,RETRY_BACKOFF_MAX_SEC,SCHEDULE_REFRESH_ADVANCE_SEC
from.devices import async_snapshot_devices
from.director_utils import director_get_entry_variables
from.keypad import async_setup_keypads
from.license import async_enforce_license
_LOGGER=logging.getLogger(__name__)
PLATFORMS=[Platform.LIGHT,Platform.ALARM_CONTROL_PANEL,Platform.BINARY_SENSOR,Platform.EVENT,Platform.LOCK,Platform.MEDIA_PLAYER,Platform.SENSOR,Platform.SWITCH,Platform.FAN,Platform.CLIMATE,Platform.COVER]
async def async_setup_entry(hass,entry):
	C=hass;B=entry;C.data.setdefault(DOMAIN,{});A=C.data[DOMAIN].setdefault(B.entry_id,{});E=B.data;await async_enforce_license(C,B);await refresh_tokens(C,B);A[CONF_CONTROLLER_UNIQUE_ID]=E[CONF_CONTROLLER_UNIQUE_ID]
	try:F=(await A[CONF_ACCOUNT].get_account_controllers())['href']
	except(client_exceptions.ClientError,asyncio.TimeoutError)as D:raise ConfigEntryNotReady(D)from D
	try:A[CONF_DIRECTOR_SW_VERSION]=await A[CONF_ACCOUNT].get_controller_os_version(F)
	except(client_exceptions.ClientError,asyncio.TimeoutError)as D:raise ConfigEntryNotReady(D)from D
	K,G,H=A[CONF_CONTROLLER_UNIQUE_ID].split('_',3);A[CONF_DIRECTOR_MODEL]=G.upper();I=dr.async_get(C);I.async_get_or_create(config_entry_id=B.entry_id,identifiers={(DOMAIN,A[CONF_CONTROLLER_UNIQUE_ID])},connections={(dr.CONNECTION_NETWORK_MAC,H)},manufacturer='Control4',name=A[CONF_CONTROLLER_UNIQUE_ID],model=A[CONF_DIRECTOR_MODEL],sw_version=A[CONF_DIRECTOR_SW_VERSION])
	try:J=await A[CONF_DIRECTOR].get_all_item_info()
	except(client_exceptions.ClientError,asyncio.TimeoutError)as D:raise ConfigEntryNotReady(D)from D
	A[CONF_DIRECTOR_ALL_ITEMS]=J;A[CONF_UI_CONFIGURATION]=await A[CONF_DIRECTOR].get_ui_configuration();A[CONF_SCAN_INTERVAL]=B.options.get(CONF_SCAN_INTERVAL,DEFAULT_SCAN_INTERVAL);A[CONF_ALARM_AWAY_MODE]=B.options.get(CONF_ALARM_AWAY_MODE,DEFAULT_ALARM_AWAY_MODE);A[CONF_ALARM_HOME_MODE]=B.options.get(CONF_ALARM_HOME_MODE,DEFAULT_ALARM_HOME_MODE);A[CONF_ALARM_NIGHT_MODE]=B.options.get(CONF_ALARM_NIGHT_MODE,DEFAULT_ALARM_NIGHT_MODE);A[CONF_ALARM_CUSTOM_BYPASS_MODE]=B.options.get(CONF_ALARM_CUSTOM_BYPASS_MODE,DEFAULT_ALARM_CUSTOM_BYPASS_MODE);A[CONF_ALARM_VACATION_MODE]=B.options.get(CONF_ALARM_VACATION_MODE,DEFAULT_ALARM_VACATION_MODE);A[CONF_ALARM_ARM_STATES]={DEFAULT_ALARM_AWAY_MODE,DEFAULT_ALARM_HOME_MODE,DEFAULT_ALARM_NIGHT_MODE,DEFAULT_ALARM_CUSTOM_BYPASS_MODE,DEFAULT_ALARM_VACATION_MODE};A[CONF_CONFIG_LISTENER]=B.add_update_listener(update_listener);await async_setup_keypads(C);await C.config_entries.async_forward_entry_setups(B,PLATFORMS);await async_snapshot_devices(C,B);_prune_deselected(C,B);return _A
async def async_unload_entry(hass,entry):
	B=hass;A=entry;D=await B.config_entries.async_unload_platforms(A,PLATFORMS);C=B.data[DOMAIN][A.entry_id];E=C.get(CONF_LICENSE_TASK)
	if E is not None:E.cancel()
	_LOGGER.debug('Disconnecting C4Websocket for config entry unload');await C[CONF_WEBSOCKET].sio_disconnect();_LOGGER.debug('Cancelling scheduled token refresh for config entry unload');C[CONF_CANCEL_TOKEN_REFRESH_CALLBACK]()
	if D:B.data[DOMAIN].pop(A.entry_id);_LOGGER.debug('Unloaded entry for %s',A.entry_id)
	return D
async def update_listener(hass,config_entry):_LOGGER.debug('Config entry was updated, rerunning setup');await hass.config_entries.async_reload(config_entry.entry_id)
def is_item_selected(entry,item_id):
	from.const import CONF_IMPORT_ALL as B,CONF_SELECTED_ITEMS as C;A=entry.options
	if A.get(B,_A):return _A
	try:D={int(A)for A in A.get(C)or[]}
	except(TypeError,ValueError):return _A
	try:return int(item_id)in D
	except(TypeError,ValueError):return _B
def filter_selected(entry,entities):return[A for A in entities if is_item_selected(entry,getattr(A,'_idx',None))]
def _prune_deselected(hass,entry):
	C=hass;A=entry;from.const import CONF_IMPORT_ALL as K
	if A.options.get(K,_A):return
	L=C.data[DOMAIN][A.entry_id];M=L.get(CONF_CONTROLLER_UNIQUE_ID);D=er.async_get(C);G=dr.async_get(C)
	for E in er.async_entries_for_config_entry(D,A.entry_id):
		H=E.unique_id or''
		if H.startswith('c4kp_'):continue
		F=''
		for I in H:
			if I.isdigit():F+=I
			else:break
		if not F:continue
		if not is_item_selected(A,F):_LOGGER.debug('Pruning deselected entity %s',E.entity_id);D.async_remove(E.entity_id)
	for B in dr.async_entries_for_config_entry(G,A.entry_id):
		J={A[1]for A in B.identifiers if A[0]==DOMAIN}
		if M in J:continue
		if any(A.startswith('keypad_')for A in J):continue
		if not er.async_entries_for_device(D,B.id,include_disabled_entities=_A):_LOGGER.debug('Pruning now-empty Control4 device %s',B.id);G.async_remove_device(B.id)
async def get_items_of_category(hass,entry,category):
	A=category;_LOGGER.debug('Getting items of category: %s',A);B=hass.data[DOMAIN][entry.entry_id][CONF_DIRECTOR]
	try:C=await B.get_all_items_by_category(A);return C
	except InvalidCategory as D:_LOGGER.warning('Category %s does not exist on this Control4 system,                         entities from this domain will not be setup.',A,exc_info=_A);return[]
async def refresh_tokens(hass,entry):
	E=entry;C=hass;D=E.data;L=aiohttp_client.async_get_clientsession(C);F=C4Account(D[CONF_USERNAME],D[CONF_PASSWORD],L)
	try:await F.get_account_bearer_token()
	except(client_exceptions.ClientError,asyncio.TimeoutError)as A:raise ConfigEntryNotReady(A)from A
	except BadCredentials as A:raise ConfigEntryAuthFailed(A)from A
	M=D[CONF_CONTROLLER_UNIQUE_ID]
	try:G=await F.get_director_bearer_token(M)
	except(client_exceptions.ClientError,asyncio.TimeoutError)as A:raise ConfigEntryNotReady(A)from A
	H=aiohttp_client.async_get_clientsession(C,verify_ssl=_B);I=C4Director(D[CONF_HOST],G[CONF_TOKEN],H);_LOGGER.debug('Saving new account and director tokens in hass data');B=C.data[DOMAIN][E.entry_id];B[CONF_ACCOUNT]=F;B[CONF_DIRECTOR]=I
	if not(CONF_WEBSOCKET in B and isinstance(B[CONF_WEBSOCKET],C4Websocket)):_LOGGER.debug('First time setup, creating new C4Websocket object');J=C4WebsocketConnectionTracker(C,E);N=C4Websocket(D[CONF_HOST],H,J.connect_callback,J.disconnect_callback);B[CONF_WEBSOCKET]=N;logging.getLogger('socketio.client').setLevel(logging.WARNING);logging.getLogger('engineio.client').setLevel(logging.WARNING);logging.getLogger('charset_normalizer').setLevel(logging.ERROR)
	_LOGGER.debug('Starting new WebSocket connection')
	try:await B[CONF_WEBSOCKET].sio_connect(I.director_bearer_token)
	except Exception as A:raise ConfigEntryNotReady(A)from A
	K=max(G['validSeconds']-SCHEDULE_REFRESH_ADVANCE_SEC,SCHEDULE_REFRESH_ADVANCE_SEC);_LOGGER.debug('Registering next token refresh in %s seconds',K);O=RefreshTokensObject(C,E);B[CONF_CANCEL_TOKEN_REFRESH_CALLBACK]=async_call_later(hass=C,delay=K,action=O.refresh_tokens)
class C4WebsocketConnectionTracker:
	def __init__(A,hass,entry):A.hass=hass;A.entry=entry;A._was_disconnected=_B
	async def connect_callback(A):
		if not A._was_disconnected:return
		_LOGGER.info('Websocket connection to Control4 reestablished');C=A.hass.data[DOMAIN][A.entry.entry_id][CONF_WEBSOCKET].item_callbacks
		for(B,D)in C.items():E=await director_get_entry_variables(A.hass,A.entry,B);F={_C:_D,'iddevice':B,'data':E};await D(B,F)
		A._was_disconnected=_B
	async def disconnect_callback(A):
		_LOGGER.warning('Websocket connection to Control4 lost, attempting reconnection');A._was_disconnected=_A;B=A.hass.data[DOMAIN][A.entry.entry_id][CONF_WEBSOCKET].item_callbacks
		for(C,D)in B.items():await D(C,_B)
class RefreshTokensObject:
	def __init__(A,hass,entry):A.hass=hass;A.entry=entry;A.retries=0
	async def refresh_tokens(A,datetime):return await A._refresh_token_with_retry()
	async def _refresh_token_with_retry(A):
		try:await refresh_tokens(A.hass,A.entry)
		except ConfigEntryNotReady:A._schedule_refresh_retry()
	def _schedule_refresh_retry(A):A.retries+=1;B=random.uniform(0,min(2**A.retries,RETRY_BACKOFF_MAX_SEC));_LOGGER.warning('Token refresh failed, trying again in %s seconds',B);C=A.hass.data[DOMAIN][A.entry.entry_id];C[CONF_CANCEL_TOKEN_REFRESH_CALLBACK]=async_call_later(hass=A.hass,delay=B,action=A.refresh_tokens)
class Control4Entity(Entity):
	def __init__(A,entry_data,entry,name,idx,device_name,device_manufacturer,device_model,device_id,device_area,device_attributes):D=device_id;C=entry_data;B=idx;super().__init__();A.entry=entry;A.entry_data=C;A._attr_name=name;A._attr_unique_id=str(B);A._idx=B;A._controller_unique_id=C[CONF_CONTROLLER_UNIQUE_ID];A._device_name=device_name;A._device_manufacturer=device_manufacturer;A._device_model=device_model;A._device_id=D;A._device_area=device_area;A._extra_state_attributes=device_attributes;A._extra_state_attributes[_E]=B;A._extra_state_attributes[_F]=D;A._attr_should_poll=_B
	async def async_added_to_hass(A):await super().async_added_to_hass();await A.hass.async_add_executor_job(A.entry_data[CONF_WEBSOCKET].add_item_callback,A._idx,A._update_callback);_LOGGER.debug('Registering item id %s for callback',A._idx);await A.hass.async_add_executor_job(A.entry_data[CONF_WEBSOCKET].add_item_callback,A._device_id,A._update_callback);_LOGGER.debug('Registering parent device %s of item id %s for callback',A._device_id,A._idx)
	async def async_will_remove_from_hass(A):
		try:_LOGGER.debug('Deregistering callback for item id %s',A._idx);A.entry_data[CONF_WEBSOCKET].remove_item_callback(A._idx,A._update_callback);_LOGGER.debug('Deregistering callback for parent device %s of item id %s',A._device_id,A._idx);A.entry_data[CONF_WEBSOCKET].remove_item_callback(A._device_id,A._update_callback)
		except KeyError:return
	async def _update_callback(A,device,message):
		B=message;_LOGGER.debug(B)
		if B is _B:A._attr_available=_B
		elif B[_C]==_D:A._attr_available=_A;C=B['data'];await A._data_to_extra_state_attributes(C)
		_LOGGER.debug('Message for device %s',device);A.async_write_ha_state()
	async def _data_to_extra_state_attributes(B,data):
		if isinstance(data,dict):
			for(C,A)in data.items():
				if isinstance(A,dict):
					for(D,E)in A.items():B._extra_state_attributes[D]=E
				else:B._extra_state_attributes[C.upper()]=A
	@cached_property
	def device_info(self):A=self;return DeviceInfo(identifiers={(DOMAIN,str(A._device_id))},manufacturer=A._device_manufacturer,model=A._device_model,name=A._device_name,via_device=(DOMAIN,A._controller_unique_id),suggested_area=A._device_area)
	@property
	def extra_state_attributes(self):return self._extra_state_attributes
class Control4CoordinatorEntity(CoordinatorEntity[Any]):
	def __init__(A,entry_data,coordinator,name,idx,device_name,device_manufacturer,device_model,device_id,device_area,device_attributes):D=device_id;C=entry_data;B=idx;super().__init__(coordinator);A.entry_data=C;A._attr_name=name;A._attr_unique_id=str(B);A._idx=B;A._controller_unique_id=C[CONF_CONTROLLER_UNIQUE_ID];A._device_name=device_name;A._device_manufacturer=device_manufacturer;A._device_model=device_model;A._device_id=D;A._device_area=device_area;A._extra_state_attributes=device_attributes;A._extra_state_attributes[_E]=B;A._extra_state_attributes[_F]=D
	@cached_property
	def device_info(self):A=self;return DeviceInfo(identifiers={(DOMAIN,str(A._device_id))},manufacturer=A._device_manufacturer,model=A._device_model,name=A._device_name,via_device=(DOMAIN,A._controller_unique_id),suggested_area=A._device_area)
	@property
	def extra_state_attributes(self):A=self;A._extra_state_attributes.update(A.coordinator.data[A._idx]);return A._extra_state_attributes