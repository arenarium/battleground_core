from RefereeHandler import RefereeHandler
import time

if __name__=="__main__":
	time.sleep(20)
	referee_handler = RefereeHandler()

	print(" [x] Requesting random number for agent 1")
	response_ag1 = referee_handler.call("ag1","move")
	print(" [.] Got %r" % response_ag1)


	print(" [x] Requesting random number for agent 2")
	response_ag2 = referee_handler.call("ag2","move")
	print(" [.] Got %r" % response_ag2)

	if response_ag1 > response_ag2:
	    print ("Agent 1 won")
	elif response_ag1 < response_ag2:
	    print ("Agent 2 won")
	else:
	    print ("tie")