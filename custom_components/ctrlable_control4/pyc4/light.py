from __future__ import annotations
_C='SET_COLOR_TARGET'
_B='LIGHT_COLOR_TARGET_MODE'
_A=None
from.import C4Entity
class C4Light(C4Entity):
	async def get_level(A):
		B=await A.director.get_item_variable_value(A.item_id,'LIGHT_LEVEL')
		if B is _A:return
		return int(B)
	async def get_state(A):
		B=await A.director.get_item_variable_value(A.item_id,'LIGHT_STATE')
		if B is _A:return
		return bool(B)
	async def set_level(A,level):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'SET_LEVEL',{'LEVEL':level})
	async def ramp_to_level(A,level,time):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'RAMP_TO_LEVEL',{'LEVEL':level,'TIME':time})
	async def set_color_xy(A,x,y,*,rate=_A):
		B={'LIGHT_COLOR_TARGET_X':float(x),'LIGHT_COLOR_TARGET_Y':float(y),_B:0}
		if rate is not _A:B['RATE']=int(rate)
		await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",_C,B)
	async def set_color_temperature(A,kelvin,*,rate=_A):
		B={'LIGHT_COLOR_TARGET_COLOR_CORRELATED_TEMPERATURE':int(kelvin),_B:1}
		if rate is not _A:B['RATE']=int(rate)
		await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",_C,B)