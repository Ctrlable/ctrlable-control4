from __future__ import annotations
_C='capabilities'
_B='UserCode'
_A=None
from.import C4Entity
from.director import C4Director
class C4SecurityPanel(C4Entity):
	async def get_arm_state(A):
		B=await A.director.get_item_variable_value(A.item_id,'DISARMED_STATE');C=await A.director.get_item_variable_value(A.item_id,'HOME_STATE');D=await A.director.get_item_variable_value(A.item_id,'AWAY_STATE')
		try:
			if B is not _A and int(B)==1:return'DISARMED'
			elif C is not _A and int(C)==1:return'ARMED_HOME'
			elif D is not _A and int(D)==1:return'ARMED_AWAY'
		except(ValueError,TypeError):pass
	async def get_alarm_state(A):
		B=await A.director.get_item_variable_value(A.item_id,'ALARM_STATE')
		if B is _A:return
		return bool(B)
	async def get_display_text(A):B=await A.director.get_item_variable_value(A.item_id,'DISPLAY_TEXT');return B
	async def get_trouble_text(A):B=await A.director.get_item_variable_value(A.item_id,'TROUBLE_TEXT');return B
	async def get_partition_state(A):B=await A.director.get_item_variable_value(A.item_id,'PARTITION_STATE');return B
	async def get_delay_time_total(A):B=await A.director.get_item_variable_value(A.item_id,'DELAY_TIME_TOTAL');return int(B)if B is not _A else _A
	async def get_delay_time_remaining(A):B=await A.director.get_item_variable_value(A.item_id,'DELAY_TIME_REMAINING');return int(B)if B is not _A else _A
	async def get_open_zone_count(A):B=await A.director.get_item_variable_value(A.item_id,'OPEN_ZONE_COUNT');return int(B)if B is not _A else _A
	async def get_alarm_type(A):B=await A.director.get_item_variable_value(A.item_id,'ALARM_TYPE');return B
	async def get_armed_type(A):B=await A.director.get_item_variable_value(A.item_id,'ARMED_TYPE');return B
	async def get_last_emergency(A):B=await A.director.get_item_variable_value(A.item_id,'LAST_EMERGENCY');return B
	async def get_last_arm_failure(A):B=await A.director.get_item_variable_value(A.item_id,'LAST_ARM_FAILED');return B
	async def set_arm(B,usercode,mode):A=usercode;A=str(A);await B.director.send_post_request(f"/api/v1/items/{B.item_id}/commands",'PARTITION_ARM',{'ArmType':mode,_B:A})
	async def set_disarm(B,usercode):A=usercode;A=str(A);await B.director.send_post_request(f"/api/v1/items/{B.item_id}/commands",'PARTITION_DISARM',{_B:A})
	async def get_emergency_types(D):
		A=[];B=await D.director.get_item_info(D.item_id)
		if not B or not isinstance(B,list)or len(B)==0:return A
		C=B[0].get(_C,{})
		if C.get('has_fire'):A.append('Fire')
		if C.get('has_medical'):A.append('Medical')
		if C.get('has_panic'):A.append('Panic')
		if C.get('has_police'):A.append('Police')
		return A
	async def get_arm_types(B):
		A=await B.director.get_item_info(B.item_id)
		if not A or not isinstance(A,list)or len(A)==0:return[]
		D=A[0].get(_C,{});C=D.get('arm_types','')
		if not C:return[]
		return[A.strip()for A in C.split(',')if A.strip()]
	async def trigger_emergency(A,emergency_type):await A.director.send_post_request(f"/api/v1/items/{A.item_id}/commands",'EXECUTE_EMERGENCY',{'EmergencyType':emergency_type})
	async def send_key_press(B,key):A=key;A=str(A);await B.director.send_post_request(f"/api/v1/items/{B.item_id}/commands",'KEY_PRESS',{'KeyName':A})
class C4ContactSensor:
	def __init__(A,director,item_id):A.director=director;A.item_id=item_id
	async def get_contact_state(A):
		B=await A.director.get_item_variable_value(A.item_id,'ContactState')
		if B is _A:return
		return bool(B)