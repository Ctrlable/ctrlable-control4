from __future__ import annotations
_A=None
import json
from typing import Any
from.import C4Entity
class C4Room(C4Entity):
	async def is_room_hidden(A):
		B=await A.director.get_item_variable_value(A.item_id,'ROOM_HIDDEN')
		if B is _A:return
		return int(B)!=0
	async def is_on(A):
		B=await A.director.get_item_variable_value(A.item_id,'POWER_STATE')
		if B is _A:return
		return int(B)!=0
	async def set_room_off(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'ROOM_OFF',{})
	async def _set_source(A,source_id,audio_only):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'SELECT_AUDIO_DEVICE'if audio_only else'SELECT_VIDEO_DEVICE',{'deviceid':source_id})
	async def set_audio_source(A,source_id):await A._set_source(source_id,audio_only=True)
	async def set_video_and_audio_source(A,source_id):await A._set_source(source_id,audio_only=False)
	async def get_volume(A):
		B=await A.director.get_item_variable_value(A.item_id,'CURRENT_VOLUME')
		if B is _A:return
		return int(B)
	async def is_muted(A):
		B=await A.director.get_item_variable_value(A.item_id,'IS_MUTED')
		if B is _A:return
		return int(B)!=0
	async def set_mute_on(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'MUTE_ON',{})
	async def set_mute_off(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'MUTE_OFF',{})
	async def toggle_mute(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'MUTE_TOGGLE',{})
	async def set_volume(A,volume):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'SET_VOLUME_LEVEL',{'LEVEL':volume})
	async def set_increment_volume(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'PULSE_VOL_UP',{})
	async def set_decrement_volume(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'PULSE_VOL_DOWN',{})
	async def set_play(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'PLAY',{})
	async def set_pause(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'PAUSE',{})
	async def set_stop(A):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'STOP',{})
	async def get_audio_devices(A):B=await A.director.send_get_request(f"/api/v1/locations/rooms/{A.item_id}/audio_devices");C=json.loads(B);return C
	async def get_video_devices(A):B=await A.director.send_get_request(f"/api/v1/locations/rooms/{A.item_id}/video_devices");C=json.loads(B);return C