from __future__ import annotations
from.import C4Entity
class C4Relay(C4Entity):
	async def get_relay_state(A):
		B=await A.director.get_item_variable_value(A.item_id,'RelayState')
		if B is None:return
		return int(B)
	async def get_relay_state_verified(A):
		B=await A.director.get_item_variable_value(A.item_id,'StateVerified')
		if B is None:return
		return bool(B)
	async def open(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'OPEN',{})
	async def close(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'CLOSE',{})
	async def toggle(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'TOGGLE',{})