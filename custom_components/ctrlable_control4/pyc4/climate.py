from __future__ import annotations
_F='SET_SETPOINT_HEAT'
_E='CELSIUS'
_D='FAHRENHEIT'
_C='SET_SETPOINT_COOL'
_B='MODE'
_A=None
from.import C4Entity
class C4Climate(C4Entity):
	async def get_hvac_state(A):return await A.director.get_item_variable_value(A.item_id,'HVAC_STATE')
	async def get_fan_state(A):return await A.director.get_item_variable_value(A.item_id,'FAN_STATE')
	async def get_hvac_mode(A):return await A.director.get_item_variable_value(A.item_id,'HVAC_MODE')
	async def get_hvac_modes(A):
		B=await A.director.get_item_variable_value(A.item_id,'HVAC_MODES_LIST')
		if B is _A:return
		return[A.strip()for A in B.split(',')if A.strip()]
	async def get_fan_mode(A):return await A.director.get_item_variable_value(A.item_id,'FAN_MODE')
	async def get_fan_modes(A):
		B=await A.director.get_item_variable_value(A.item_id,'FAN_MODES_LIST')
		if B is _A:return
		return[A.strip()for A in B.split(',')if A.strip()]
	async def get_hold_mode(A):return await A.director.get_item_variable_value(A.item_id,'HOLD_MODE')
	async def get_hold_modes(A):
		B=await A.director.get_item_variable_value(A.item_id,'HOLD_MODES_LIST')
		if B is _A:return
		return[A.strip()for A in B.split(',')if A.strip()]
	async def get_cool_setpoint_f(A):
		B=await A.director.get_item_variable_value(A.item_id,'COOL_SETPOINT_F')
		if B is _A:return
		return float(B)
	async def get_cool_setpoint_c(A):
		B=await A.director.get_item_variable_value(A.item_id,'COOL_SETPOINT_C')
		if B is _A:return
		return float(B)
	async def get_heat_setpoint_f(A):
		B=await A.director.get_item_variable_value(A.item_id,'HEAT_SETPOINT_F')
		if B is _A:return
		return float(B)
	async def get_heat_setpoint_c(A):
		B=await A.director.get_item_variable_value(A.item_id,'HEAT_SETPOINT_C')
		if B is _A:return
		return float(B)
	async def get_humidity(A):
		B=await A.director.get_item_variable_value(A.item_id,'HUMIDITY')
		if B is _A:return
		return float(B)
	async def get_current_temperature_f(A):
		B=await A.director.get_item_variable_value(A.item_id,'TEMPERATURE_F')
		if B is _A:return
		return float(B)
	async def get_current_temperature_c(A):
		B=await A.director.get_item_variable_value(A.item_id,'TEMPERATURE_C')
		if B is _A:return
		return float(B)
	async def set_cool_setpoint_f(A,temp):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",_C,{_D:temp})
	async def set_cool_setpoint_c(A,temp):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",_C,{_E:temp})
	async def set_heat_setpoint_f(A,temp):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",_F,{_D:temp})
	async def set_heat_setpoint_c(A,temp):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",_F,{_E:temp})
	async def set_hvac_mode(A,mode):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'SET_MODE_HVAC',{_B:mode})
	async def set_fan_mode(A,mode):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'SET_MODE_FAN',{_B:mode})
	async def set_preset(A,preset):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'SET_PRESET',{'NAME':preset})
	async def set_hold_mode(A,mode):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'SET_MODE_HOLD',{_B:mode})