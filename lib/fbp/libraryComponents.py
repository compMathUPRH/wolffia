
class FBP_CONSTANTS:
	END_TOKEN             = "FBP_END_TOKEN"
	BEACON_SIGNAL         = "FBP_BEACON_SIGNAL"

FBP_NO_WRAP_FUNCTIONS = ["split", "collate", "wolffiaState",  "beacon"]

def beacon(out):
	while out.empty():
		print "beacon sending signal"
		out.put(BEACON_SIGNAL)

def split(values, queueList):
	print "entro a splitter"
	value = values.get()
	while value != FBP_CONSTANTS.END_TOKEN:
		for queue in queueList:
			queue.put(value)
		value = values.get()

	for queue in queueList:
		queue.put(FBP_CONSTANTS.END_TOKEN)


def collate(queueList, out):
	print "entro a lumper"
	while True:
		values = []
		for queue in queueList:
			value = queue.get()
			if value == FBP_CONSTANTS.END_TOKEN: 
				out.put(FBP_CONSTANTS.END_TOKEN)
				return
			values.append(value[0])
		out.put(values)
		#print "lumper->", values

	# falta consumir colas

def wolffiaState(inQ, outQ):
	inItem = inQ.get()
	while inItem != FBP_CONSTANTS.END_TOKEN:
		print "wolffiaState recibio"
		outQ.put([inItem])
		inItem = inQ.get()
	print "wolffiaState termino"
	outQ.put(FBP_CONSTANTS.END_TOKEN)

