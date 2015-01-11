#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import shutil
import sys

#ordner1 = "/Users/user1/Documents/python/BackUpSync/tmp1"
#ordner1 = "c:\temp1"
#ordner2 = "/Users/user1/Documents/python/BackUpSync/tmp2"
#ordner2 = "c:\temp2"

def copyLargeFile(src, dest, buffer_size):
    with open(src, 'rb') as fsrc:
        with open(dest, 'wb') as fdest:
            shutil.copyfileobj(fsrc, fdest, buffer_size)

def copyFile(src1, dest2):
	if os.path.getsize(src1)>50000000:
		try:
			copyLargeFile(src1, dest2, buffer_size=10000000)
			return 1
		except shutil.Error as e:
			print(src1 + ' Error1: %s' % e)
		# eg. source or destination doesn't exist
		except IOError as e:
			print(src1 + ' Error2: %s' % e.strerror)
	else:
		try:
			#print dest2[:dest2.rfind(slash)]
			shutil.copy2(src1, dest2[:dest2.rfind(slash)])
			return 1
		# eg. src and dest are the same file
		except shutil.Error as e:
			print(src1 + ' Error3: %s' % e)
		# eg. source or destination doesn't exist
   		except IOError as e:
			print(src1 + ' Error4: %s' % e.strerror)
	return 0

def CopyOrdner(ord1):
	j=0
	if ordner1[:len(ordner2)]!=ordner2[:len(ordner1)]:
		ord2 = ordner2 + ord1[len(ordner1):]
		if os.path.isdir(ord2)==False:
			try:
				os.mkdir(ord2)
			except OSError, e:
				print 'Error5: ' + e.strerror + " " + ord2 
		if os.path.isdir(ord2)==True:
			for item in os.listdir(ord1):
				#print item
				if os.path.isdir(ord1 + slash + item)==False:
					flg=0
					try:
						if os.path.getsize(ord1 + slash + item)!=os.path.getsize(ord2 + slash + item):
							print "update: " + ord2 + slash + item
							flg=1
					except:
						print "copy: " + ord2 + slash + item
						flg=1
					if flg==1:
						try:
							j = j + copyFile(ord1 + slash + item, ord2 + slash + item)
						except:
							try:
								if os.path.getsize(ord1 + slash + item)!=os.path.getsize(ord2 + slash + item):
									j = j + copyFile(ord1 + slash + item, ord2 + slash + item)
							except:
								print "Error: " + ord2 + slash + item			
				else:
					j=j+CopyOrdner(ord1 + slash + item)
	return j

def SyncOrdner(ord1):
	j=0
	if ordner1[:len(ordner2)]!=ordner2[:len(ordner1)]:
		ord2 = ordner2 + ord1[len(ordner1):]
		if os.path.isdir(ord2)==False:
			try:
				os.mkdir(ord2)
			except OSError, e:
				print 'Error5: ' + e.strerror + " " + ord2
		if os.path.isdir(ord2)==True:
			for item in os.listdir(ord2):
				if os.path.isfile(ord1 + slash + item)==False and os.path.isdir(ord2 + slash + item)==False:
					print "delete: " + ord2 + slash + item
					try: 
						os.remove(ord2 + slash + item)
					except OSError, e:
						print 'Error6: ' + e.strerror + " " + ord2 + slash + item
				if os.path.isdir(ord1 + slash + item)==False and os.path.isdir(ord2 + slash + item)==True:
					print "delete tree: " + ord2 + slash + item
					try:
						shutil.rmtree(ord2 + slash + item)
					except OSError, e:
						print 'Error7: ' + e.strerror + " " + ord2 + slash + item 
			for item in os.listdir(ord1):
				#print item
				if os.path.isdir(ord1 + slash + item)==False:
					flg=0
					try:
						if os.path.getsize(ord1 + slash + item)!=os.path.getsize(ord2 + slash + item):
							print "update: " + ord2 + slash + item
							flg=1
					except:
						print "copy: " + ord2 + slash + item
						flg=1
					if flg==1:
						try:
							j = j + copyFile(ord1 + slash + item, ord2 + slash + item)
						except:
							try:
								if os.path.getsize(ord1 + slash + item)!=os.path.getsize(ord2 + slash + item):
									j = j + copyFile(ord1 + slash + item, ord2 + slash + item)
							except:
								print "Error: " + ord2 + slash + item			
				else:
					j = j + SyncOrdner(ord1 + slash + item)
	return j

if len(sys.argv)==4 and os.path.isdir(sys.argv[2]) and os.path.isdir(sys.argv[3]):
	befehl=sys.argv[1]
	ordner1=sys.argv[2]
	ordner2=sys.argv[3]
	if ordner1.find("/")>-1:
		slash = "/"
	else:
		slash = "\\"
	if ordner1.rfind(slash) + 1==len(ordner1):
		ordner1=ordner1[:len(ordner1)-1]
	if ordner2.rfind(slash) + 1==len(ordner2):
		ordner2=ordner2[:len(ordner2)-1]
	print befehl + " " + ordner1 + " > " + ordner2 
	print("wait a moment")
	if befehl=="dircopy":		
		print CopyOrdner(ordner1), "files are copied"
	elif befehl=="dirsync":
		print SyncOrdner(ordner1), "files are synced"
	else:
		print "no command: " + befehl 
		print "use:"
		print "dircopy - to tree copy" 
		print "dirsync - to tree sync, !!! this command does delete all fils and directories at destination, that there are not at source..." 
