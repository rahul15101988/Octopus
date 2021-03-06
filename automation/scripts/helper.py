#!/user/bin/python -tt

import os
import xml.etree.ElementTree as ET
import requests

BASEDIR 		= '.'
TestXmlFilePath = BASEDIR + '/Tests/tbd/'
xmlext 			= '.xml'
urlHeader 		= 'http://10.223.1.88/Carmel-Versions/SVN/Builds/prod/'
buildStream		= ''
buildVer		= '8.7.5'
buildSubdir 	= 'trunk'
buildSuffix		= '.bin'
delem 			= '/'

#url = urlHeader + buildVer + delem + buildSubdir + delem

def getTestXml(file):
	print( TestXmlFilePath + file + xmlext)
	return (file)
	#return (TestXmlFilePath + file + xmlext)

def isavailable(file):
	if os.path.isfile(file):
		return True
	return False

def getopts(argv):
	opts = {}
	while argv:
		if argv[0][0] == '-': # found a "-name value" pair.
			opts[argv[0]] = argv[1] # add key and value to the dictionary
		argv = argv[1:] #  reduce the arg list, copyit from 1
	# all the arguments that we know of must be initialized
	if '-r' not in opts or opts['-r'] not in  ['Yes','yes','Yes']:
		opts['-r'] = False
	elif opts['-r'] in ['YES','yes']:
		opts['-r'] = True

	return opts

def printusage():
	print ('Try: ./runTest.sh -f <testname> -r <yes/no>')

def getXmlElem(file):
	tree = ET.parse(file)
	root = tree.getroot()
	elements = {}	
	elements['id']				=	root.attrib['id']
	elements['DURATION_H']		=	root.find('DURATION_H').text
	elements['DURATION_M']		=	root.find('DURATION_M').text
	elements['DURATION_S']		=	root.find('DURATION_S').text
	elements['RATE']			=	root.find('RATE').text
	elements['RECURRENCE']		=	root.find('RECURRENCE').text
	elements['SCHEDULE_TIME']	=	root.find('SCHEDULE_TIME').text
	elements['SCHEDULE_DATE']	=	root.find('SCHEDULE_DATE').text
	elements['SCHEDULE_POLICY']	=	root.find('SCHEDULE_POLICY').text
	elements['RMX_IP']			=	root.find('RMX_IP').text
	elements['RMX_BUILD']		=	root.find('RMX_BUILD').text
	elements['RELEASE']			=	root.find('RELEASE').text
	elements['RMX_TYPE']		=	root.find('RMX_TYPE').text
	elements['RMX_USER']		=	root.find('RMX_USER').text
	elements['RMX_PASS']		=	root.find('RMX_PASS').text
	elements['RMX_SU_PASS']		=	root.find('RMX_SU_PASS').text
	elements['DMA_IP']			=	root.find('DMA_IP').text
	elements['SIPP_PRIMARY']	=	root.find('SIPP_PRIMARY').text
	elements['SIPP_PRI_USR']	=	root.find('SIPP_PRI_USR').text
	elements['SIPP_PRI_PASS']	=	root.find('SIPP_PRI_PASS').text
	elements['SIPP_SECONDARY'] 	= 	root.find('SIPP_SECONDARY').text
	elements['SIPP_SEC_USR']	=	root.find('SIPP_SEC_USR').text
	elements['SIPP_SEC_PASS']	=	root.find('SIPP_SEC_PASS').text
	elements['CPS']				=	root.find('CPS').text
	elements['VIDEO_TYPE']		=	root.find('VIDEO_TYPE').text
	elements['PROTOCOL']		=	root.find('PROTOCOL').text
	elements['FR']				=	root.find('FR').text
	elements['HOLDTIME']		=	root.find('HOLDTIME').text
	elements['ON_FAIL_RESTART']	=	root.find('ON_FAIL_RESTART').text
	elements['EMAILTO']			=	root.find('EMAILTO').text
	elements['MONITOR_DELAY']	=	root.find('MONITOR_DELAY').text
	elements['LOADING']			=	root.find('LOADING').text
	elements['MAX_PORTS']		=	root.find('MAX_PORTS').text
	#print (elements)
	return elements

def getDownloadPath(RmxBuild,RmxType):
	global buildStream 
	global url
	buildStream = '.'.join(RmxBuild.split('_')[1].split('.')[:3])
	if RmxType.lower() in ['rmx4000','rmx2000']:
		url = urlHeader + buildStream + delem + buildSubdir + delem + RmxBuild + delem + RmxBuild + '.bin'
	elif RmxType.lower() == 'ninja':
		url = urlHeader + buildStream + delem + buildSubdir + delem + RmxBuild + delem + 'RPCS1800_'+ RmxBuild + '.bin'
	return url

def getExactBuildName(RmxBuild,RmxType):
	if RmxType.lower() == 'ninja':
		return 'RPCS1800_' + RmxBuild +'.bin'
	elif RmxType.lower() in ['rmx4000', 'rmx2000']:
		return RmxBuild + '.bin'
	else:
		raise ValueError('Some issue with identification of rmx build:[HELPER]')

def buildavailable(build):
	global url
	global buildStream
	# the build input would be in format RMX_8.7.5.351
	buildStream = '.'.join(build.split('_')[1].split('.')[:3])
	url = urlHeader + buildStream + delem + buildSubdir + delem + build + delem +'BL_names.txt'
	resp = requests.get(url)
	if resp.status_code == 200:
		buildName = resp.text.split('\n')[0].split('=')[1].strip(' ')
		if buildName == build:
			return True
	#else:
	#	raise ValueError ('ERROR: Couldnt contact jenkins')
	return False

def getLatestBuild(codeLineup):
	os.system('clear')
	os.system('cls')
	global url
	url = urlHeader + codeLineup + delem +	buildSubdir + delem + 'last/BL_names.txt'
	resp = requests.get(url)
	if resp.status_code == 200:
		buildName = resp.text.split('\n')[0].split('=')[1].strip(' ')
		return buildName
	else:
		return 'INVALID'
		
