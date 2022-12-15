from bluepy import btle
import struct

MAC_array = ['E5:F9:D5:9B:E4:5F', 'E5:5E:FE:D4:4E:EC', 'D9:30:A3:82:87:F1', 'EB:FD:D3:79:6A:50']
pos_x = [0, 900, 900, 0]
pos_y = [900, 900, 0, 0]
pos_z = [0, 0, 0, 0]

count = 0
for MAC in MAC_array:
	dev = btle.Peripheral(MAC)
	
	locuuid = btle.UUID("680c21d9-c946-4c1f-9c11-baa1c21329e7")
	panuuid = btle.UUID("80f9d8bc-3bff-45bb-a181-2d6a37991208")
	opuuid = btle.UUID("3f0afd88-7770-46b0-b5e7-9fc099598964")
	posuuid = btle.UUID("f0f26c9b-2c8c-49ac-ab60-fe03def1b40c")
	
	locService = dev.getServiceByUUID(locuuid)
	
	if count == 0:
		opcode = struct.pack(">H", 0b1101110110000000)
	else :
		opcode = struct.pack(">H", 0b1101110100000000)
		
	poscode = struct.pack("<iiib", pos_x[count], pos_y[count], pos_z[count], 100)
	panid = struct.pack(">H", 1)
		
	try:
		ch = locService.getCharacteristics(opuuid)[0]
		dev.writeCharacteristic(ch.valHandle, opcode)
		ch1 = locService.getCharacteristics(posuuid)[0]
		dev.writeCharacteristic(ch1.valHandle, poscode)
		ch2 = locService.getCharacteristics(panuuid)[0]
		dev.writeCharacteristic(ch2.valHandle, poscode)
		# dev.writeCharacteristic(28, poscode)
	finally:
		dev.disconnect()
		print((MAC), 'is disconnected')
	count = count + 1
