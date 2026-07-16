from __future__ import annotations
_A=None
from.import C4Entity
class C4Blind(C4Entity):
	async def get_battery_level(A):
		B=await A.director.get_item_variable_value(A.item_id,'Battery Level')
		if B is _A:return
		return int(B)
	async def get_closing(A):
		B=await A.director.get_item_variable_value(A.item_id,'Closing')
		if B is _A:return
		return bool(B)
	async def get_fully_closed(A):
		B=await A.director.get_item_variable_value(A.item_id,'Fully Closed')
		if B is _A:return
		return bool(B)
	async def get_fully_open(A):
		B=await A.director.get_item_variable_value(A.item_id,'Fully Open')
		if B is _A:return
		return bool(B)
	async def get_level(A):
		B=await A.director.get_item_variable_value(A.item_id,'Level')
		if B is _A:return
		return int(B)
	async def get_open(A):
		B=await A.director.get_item_variable_value(A.item_id,'Open')
		if B is _A:return
		return bool(B)
	async def get_opening(A):
		B=await A.director.get_item_variable_value(A.item_id,'Opening')
		if B is _A:return
		return bool(B)
	async def get_stopped(A):
		B=await A.director.get_item_variable_value(A.item_id,'Stopped')
		if B is _A:return
		return bool(B)
	async def get_target_level(A):
		B=await A.director.get_item_variable_value(A.item_id,'Target Level')
		if B is _A:return
		return int(B)
	async def open(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'SET_LEVEL_TARGET:LEVEL_TARGET_OPEN',{})
	async def close(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'SET_LEVEL_TARGET:LEVEL_TARGET_CLOSED',{})
	async def set_level_target(A,level):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'SET_LEVEL_TARGET',{'LEVEL_TARGET':level})
	async def stop(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'STOP',{})
	async def toggle(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'TOGGLE',{})