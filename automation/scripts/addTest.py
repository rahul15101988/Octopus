#!/usr/bin/python -tt

""""
created on 17th March 2018
@author: Abhishek Chattopadhyay
FName: addTest
"""

from __future__ import print_function
import os
import sys
import subprocess
import datetime
import time
import xml.etree.ElementTree as ET

BASEDIR		=	'.'
_template	=	BASEDIR +	'/xml/templates/testtemplate.xml'
optDir		=	BASEDIR +	'/xml/options/'
testDir		=	BASEDIR	+	'/Tests/tbd/'
tempDir		=	BASEDIR +	'/Tests/temp/'
runningDir	=	BASEDIR	+	'/Tests/running/'
completedDir=	BASEDIR	+	'/Tests/completed/'
scheduledDir=	BASEDIR	+	'/Tests/scheduled/'
debug		=	False

def Print(level,statement):
	global debug
	if debug:
		print (level+':',statement)

def inputMsg(msg1, msg2):
	if type(msg1) is int:
		msg1 = str(msg1)
	if type(msg2) is int:
		msg2 = str(msg2)
	return '['+msg1+'] '+msg2

def getInp(item,tag, msg):
	inp = raw_input(inputMsg(item[tag],msg))
	if inp != '':
		item[tag] = inp
	else:
		Print('INFO: ', 'using old value:')
		
class userTest:
		def __init__(self,elements):
			self.tcEdit = False
			self.foundPath = ''
			self.user =	elements
			self.codeLineup = ''
			self.getInput()
			return
		
		def getInput(self):	#function gets inputs from the user and returns a dict of inputs	
				print ('INFO','provide test case inputs, hit enter to auto-generate')
				now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
				self.user['id'] = now
				
				msg = 'Name your test case:(HINT: Must be unique add yyyy-mm-dd at the end): '	
				inp	=	raw_input(msg)
				if inp != '':
					if self.validateName(inp):
						self.tcEdit = True
						self.user = helper.getXmlElem(self.foundPath+inp+'.xml')
					else:
						self.user['id'] = inp
				else:
					self.user['id']	= now
					print ('INFO: AUTOGENERATED: Test Name: ', str(now)+'.xml')
					
				getInp (self.user,'SCHEDULE_TIME','Schedule Time: [enter 0 to immediately schedule]')
				getInp (self.user,'SCHEDULE_DATE','Schedule Date:(HINT: DD-MM-YYYY): ')
				if self.user['SCHEDULE_DATE'] == 'TODAY':
					self.user['SCHEDULE_DATE'] = datetime.datetime.now().strftime("%d-%m-%Y")

				getInp (self.user,'SCHEDULE_POLICY','Schedule Policy: ')
				
				if int(self.user['SCHEDULE_TIME']) == 0:
					self.user['SCHEDULE_POLICY']	= 'IMMEDIATE'
					print ('INFO: Test case schedule is: ',self.user['SCHEDULE_POLICY'])

				getInp (self.user, 'RECURRENCE','Recurrence:(HINT: [yes/no]): ')
				getInp (self.user, 'DURATION_H','Duration:(HINT: in hours): ')

				self.user['DURATION_M']		=	0 # not allowed now
				self.user['DURATION_S']		=	0 # not allowed now

				getInp (self.user,'RMX_IP',"RMX IP: ")
				getInp (self.user,'RMX_TYPE',"Rmx Type: ")
				
				#	get the build lineup
				#self.codeLineup = raw_input("Pick your code line (8.7.5, 8.7.4, 8.5.13, 8.5.21): ")
				getInp (self.user,'RELEASE','(8.7.5, 8.7.4, 8.5.13, 8.5.21)')
				self.user['RMX_BUILD'] = helper.getLatestBuild(self.user['RELEASE'])
				 
				getInp (self.user,'RMX_BUILD', 'Rmx Build: ')
				getInp (self.user,'DMA_IP', "DMA IP: ")
				getInp (self.user,'CPS',"Calls Per Second: ")
				getInp (self.user,'PROTOCOL',"Protocol: ")
				getInp (self.user,'FR',"Failure Rate:(HINT:% failure to monitor): ")
				getInp (self.user,'SIPP_PRIMARY',"primary Sipp IP: ")
				getInp (self.user,'SIPP_PRI_USR',"primary Sipp ssh user: ")
				getInp (self.user,'SIPP_PRI_PASS',"primary Sipp ssh password: ")
				if (self.user['RMX_TYPE']).lower() == 'rmx4000':
					getInp (self.user,'SIPP_SECONDARY',"secondary Sipp IP: ")
					getInp (self.user,'SIPP_SEC_USR',"secondary Sipp ssh user: ")
					getInp (self.user,'SIPP_SEC_PASS',"secondary Sipp ssh passowrd: ")

				advancedConfig = False

				print ('INFO: Based on your inputs further parameters are autocalculated:')
				print ('RMX ssh User: ', self.user['RMX_USER'])
				print ('RMX ssh password: ', self.user['RMX_PASS'])
				print ('RMX su password: ', self.user['RMX_SU_PASS'])
				print ('Video Type: ', self.user['VIDEO_TYPE'])

				# calculate rate & loading factor
				if self.user['CPS'] == '2':
					self.user['RATE'] = 2000
					self.user['LOADING'] = 75
				elif self.user['CPS'] ==	'5':
					self.user['RATE'] = 5000
					self.user['LOADING'] = 60
				print ('RATE: ', self.user['RATE'])
				print ('LOADING %: ', self.user['LOADING'])

				# calculate ports & monitor delay
				if (self.user['RMX_TYPE']).lower() == 'rmx4000':
					self.user['MAX_PORTS'] = 400
					self.user['MONITOR_DELAY'] = 15
				elif (self.user['RMX_TYPE']).lower() == 'rmx2000':
					self.user['MAX_PORTS'] = 200
					self.user['MONITOR_DELAY'] = 15
				elif (self.user['RMX_TYPE']).lower() == 'ninja':
					self.user['MAX_PORTS'] = 100
					self.user['MONITOR_DELAY'] = 10
				print ('MAX PORTS: ', self.user['MAX_PORTS'])
				print ('Monitor Delay: ', self.user['MONITOR_DELAY'])

				#	calculate hold time
				#	Calculation of media quality multiplier (1 for HD, 2 for CIF and SD, 3 for AUDIO ONLY
				if self.user['VIDEO_TYPE'] in ['CIF','SD']:
					MQFactor = 	2
				elif self.user['VIDEO_TYPE'] == 'HD':
					MQFactor = 1
				else:
					MQFactor = 3
				
				# the hold time is derived by ((MQFactor * Loading Factor * Ports)/(Rate))*10   this value would be in mil secs
				# rate is in thousand calls factor
				# loading factor is actually a percentage : So multiplicative facor becomes 10
				print (MQFactor, self.user['LOADING'], self.user['MAX_PORTS'], self.user['RATE'])
				print (type(MQFactor), type(self.user['LOADING']), type(self.user['MAX_PORTS']), type(self.user['RATE']))
				holdTime = (MQFactor * self.user['LOADING'] * self.user['MAX_PORTS'] * 10 )/(self.user['RATE'])
				self.user['HOLDTIME'] = holdTime
				print ('HoldTime: ', self.user['HOLDTIME'])


				advancedConfig = raw_input ('If you want to Overwrite the autocalculated parameters enter (YES)')

				if advancedConfig == 'YES':
					getInp (self.user,'RMX_USER','Rmx ssh user name: ')
					getInp (self.user,'RMX_PASS','Rmx ssh password: ')
					getInp (self.user,'RMX_SU_PASS','Rmx super user password:')
					getInp (self.user,'VIDEO_TYPE',"Video Type: ")
					getInp (self.user,'LOADING','%age loading of RMX: ')
					getInp (self.user,'RATE',"Rate: ")
					getInp (self.user,'HOLDTIME',"Hold Time: ")
					getInp (self.user,'MONITOR_DELAY',"Monitor delay:(HINT: This is the time in minute the failure rate checked would wait feore starting to monitor your sipp load stats): ")
					getInp (self.user,'ON_FAIL_RESTART','On Fail Restart? (yes/ no): ') 		# not allowed now
					getInp (self.user,'EMAILTO','email: ')	# not allowed now

				Print ('INFO',self.user)
				#return self.user

		def validateName(self,name):
		#	Check name of test case for uniqueness
			paths = [testDir, scheduledDir, completedDir, tempDir]
			for path in paths:
				if name+'.xml' in os.listdir(path):
					self.foundPath =  path
					print('INFO: ', 'You are editing an existing tc')
					return True

			if name in os.listdir(runningDir):
				raise ValueError('ERROR: This test case is running, cant edit')
			return False

		def validate(self):	#	function validates all the inputs by user
			result	=	True
			print ('Let me quickly check the inputs')
			print ('INFO: ','Checking build: ', end='')
			if helper.buildavailable(self.user['RMX_BUILD']):
				print ('Build choice is fine')
			else:
				result = result & False
				
			'''command = 'ping -c 4 '
			errors = ['100% packet loss','unknown','unreachable']
			print ('INFO: Checking if I can reach RMX IP: ',self.user['RMX_IP'], end='')
			output = subprocess.Popen(
				[command + self.user['RMX_IP']],
				shell=True,
				stdout=subprocess.PIPE).communicate()[0]
			print (output)
			#if ("Destination host unreachable" in output) or ('unknown' in output):
			print ([i for i in errors if i in output])
			if [i for i in errors if i in output.decode('utf-8')]:
				print ("{} is offline".format(self.user['RMX_IP']))
				result = result & False
			else:
				print (' : RMX Rechable')
				
			print ('INFO: Checking if I can reach the SIPP machine: ',self.user['SIPP_PRIMARY'] )
			output = subprocess.Popen(
					[command + self.user['SIPP_PRIMARY']],
					shell=True,
					stdout=subprocess.PIPE,
					).communicate()[0]
			if "Destination host unreachable" in output.decode('utf-8') or 'unknown' in output.decode('utf-8'):
				print ("{} is offline".format(self.user['SIPP_PRIMARY']))
				result = result & False
			else:
				print  (' : SIPP Rechable')

			if (self.user['RMX_TYPE']).lower() == 'rmx4000':
				print ('INFO: Checking is I can reach the 2nd SIPP machine:', self.user['SIPP_SECONDARY'])
				output = subprocess.Popen([command + self.user['SIPP_SECONDARY']],stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
				if "Destination host unreachable" in output.decode('utf-8') or 'unknown' in output.decode('utf-8'):
					print ("{} is offline".format(self.user['SIPP_SECONDARY']))
					result = result & False
				else:
					print ('SIPP Rechable')
			'''
			if result == True:
				print ('All Good adding test case now')
			else:
				print ('one or more errors')
			return result
				
		def addTest(self,isValid):	#	function adds the test case to the be scheduled
			if isValid:
				testFile = testDir + self.user['id'] + '.xml'
			else:	#	If the validation fails then save the file in a temp dir
				testFile = tempDir + self.user['id'] + '.xml'
			print (testFile)

			root	=	ET.Element('TEST')

			for key in self.user.keys():			#	Create the test XML
				#print (key, self.user[key])
				if key == 'id':					#	id tag it's a root element
					root.attrib[key]	=	self.user['id']
				if type(self.user[key]) is int:
						self.user[key] = str(self.user[key])
				ET.SubElement(root, key).text	=	self.user[key]
	
			tree	=	ET.ElementTree(root)	
			
			if 	self.tcEdit:
				fileToRemove = self.foundPath + self.user['id'] + '.xml'
				os.remove(fileToRemove)
				print ('INFO: ','Removed file: ', fileToRemove)
			
			tree.write(testFile)	# write the pirmary test xml
			print ('INFO: ', 'New test case added, filename: ', testFile)
		
		def addToXmlDB():
			pass
			
			
def main(elements):
	print ('Add A TestCase to Execute')
	Print ('INFO',elements)
	test = userTest(elements)
	test.addTest(test.validate())
		
			
if __name__ == '__main__':
	sys.dont_write_bytecode = True
	import helper
	main(helper.getXmlElem(_template))
	sys.exit(0)
	
