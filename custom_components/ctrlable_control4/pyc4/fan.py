from __future__ import annotations
from.import C4Entity
class C4Fan(C4Entity):
	async def get_state(A):
		B=await A.director.get_item_variable_value(A.item_id,'IS_ON')
		if B is None:return
		return bool(B)
	async def get_speed(A):
		B=await A.director.get_item_variable_value(A.item_id,'CURRENT_SPEED')
		if B is None:return
		return int(B)
	async def set_speed(A,speed):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'SET_SPEED',{'SPEED':speed})
	async def set_preset(A,preset):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'DESIGNATE_PRESET',{'PRESET':preset})