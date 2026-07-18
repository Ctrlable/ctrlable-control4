from __future__ import annotations
_D='other'
_C='room'
_B='name'
_A='domain'
from typing import Any
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr,entity_registry as er
from homeassistant.helpers.storage import Store
_STORAGE_VERSION=1
def _store(hass,entry):return Store(hass,_STORAGE_VERSION,f"ctrlable_control4_devices_{entry.entry_id}")
async def async_snapshot_devices(hass,entry):
	F=entry;C=hass;K=er.async_get(C);L=dr.async_get(C);G=_store(C,F);D=await G.async_load()or{};H=False
	for A in er.async_entries_for_config_entry(K,F.entry_id):
		B=A.unique_id or''
		if not B.isdigit():continue
		M=A.entity_id.split('.',1)[0]if A.entity_id else _D;N=A.original_name or A.name or A.entity_id or B;I=''
		if A.device_id:
			E=L.async_get(A.device_id)
			if E is not None:I=E.name_by_user or E.name or''
		J={_A:M,_B:N,_C:I}
		if D.get(B)!=J:D[B]=J;H=True
	if H:await G.async_save(D)
async def async_device_catalog(hass,entry):
	F=await _store(hass,entry).async_load()or{};B=[];C=set()
	for(D,A)in F.items():E=A.get(_A)or _D if isinstance(A,dict)else _D;C.add(E);B.append({'id':str(D),_B:(A.get(_B)if isinstance(A,dict)else None)or str(D),_C:(A.get(_C)if isinstance(A,dict)else'')or'',_A:E})
	B.sort(key=lambda e:(e[_A],e[_C],e[_B].lower()));return B,sorted(C)