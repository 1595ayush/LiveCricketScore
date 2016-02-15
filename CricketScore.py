__author__ = "Ayush"

import urllib2
import json
import dbus
from time import sleep

#Live feed API
link = "http://cricscore-api.appspot.com/csa" 

#Notifications
bus = dbus.SessionBus()
notifications = bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
interface = dbus.Interface(notifications, 'org.freedesktop.Notifications')
id = 4856
timeout = 1000

#Request for URl Score
def urlopenlink(link):	
	f = urllib2.urlopen(link)
	myfile = f.read()
	parsed = json.loads(myfile)
	return parsed

#Show ongoing matched and to accept choice from the user
def takeChoice(parsed):
	print "List of ongoing matches"
	for index in range(len(parsed)):
		print str(index+1)+". "+parsed[index]['t1']+" vs "+parsed[index]['t2']  
	option = input("Enter the choice : ")
	return option


parsed=urlopenlink(link)
choice = takeChoice(parsed)

#To show score every minute
if(choice>=1 and choice<=len(parsed)):
	openlink = link+"?id="+str(parsed[choice-1]["id"])
	while True:
		parsed=urlopenlink(openlink)
		a= json.dumps(parsed,indent=4,sort_keys=True)	
		de = parsed[0]["de"]
		si = parsed[0]["si"]
		score = si.split(" v ")	
		interface.Notify(score[0]+'\n'+score[1],id,'',de,score[0]+'\n'+score[1],'','',timeout)#Display Notification
		sleep(60)#Thread sleep
else: 
	print("Sorry incorrect option. Try again\n")
	takeChoice(parsed)	#Re-ask for choice
	
	
