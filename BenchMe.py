#!/usr/bin/env python
# ------------------------------------------------------------------------
# The MIT License (MIT)
# Copyright (c) 2015 Hassan Alsaffar <hassan_alsaffar@outlook.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -------------------------------------------------------------------------
# SELinux Performance Tests and Measurements Benchmarking Tool 
# Tests: File Copy, PIPE Throughput, Pipe-based Context Switching, 
#	     Process Creation, EXECL, and Shell Scripts
#--------------------------------------------------------------------------

# ###################################
#            I M P O R T 
# ###################################
from subprocess import Popen, call, PIPE
from time import time
from os import system, unlink, mkfifo, close, path, fork, _exit, waitpid, execl, wait, remove, setpgrp
from multiprocessing import Process

# ###################################
#          F U N C T I O N
# ###################################

#1. FileCopy Test:
# ----------------
def fileCopyTest(fileSizeList):

   testResults = { "500b": [], "1K": [], "4K":[]}
   
   for i in fileSizeList:
	
        #loop for 10 seconds 
	duration = time() + 10
	copyTestCtr = 0 
	
        while time() < duration: 
		
		copyTest = Popen(["dd",    #use dd command
                          "if=/dev/zero",  #input file
               	          "of=./fileCopy%s.dat" % i, #output file
                       	  "bs=%s" % i,	   #size of output file
	                  "count=1",	   #num of blocks to read
                          "oflag=dsync"],   #Use synchronized I/O for data and metadata
               	           stderr=PIPE)

		#Get the stdout and stderr of the command run
		(out, err) = copyTest.communicate()
		lastLine = err.split("\n")
		testResults[i].append(lastLine[2])

		#Remove the file that was copied! So when the copy occurs again, it doesn't overwrite the old file and affect the results
		remove('./fileCopy%s.dat' % i)
		
		copyTestCtr += 1

   return testResults
		
#2 PIPE Test: 
#------------
def pipeTest():
	
	testResults = ""
	
	tempFile = Popen(["dd",    	   #use dd command
					  "if=/dev/zero",  #input file
					  "of=./temp.dat", #output file
					  "bs=500B",       #size of output file
					  "count=1",       #num of blocks to read
					  "oflag=dsync"],  #Use synchronized I/O for data and metadata
					   stderr=PIPE)

        #PIPE Command used: cat temp.dat | cpipe -vr -vw -vt 
        pipeTestPart1 = Popen(["cat", "temp.dat"], stderr=PIPE, stdout=PIPE)
		pipeTestPart2 = Popen(["cpipe", "-vr", "-vw", "-vt"], stdin=pipeTestPart1.stdout, stderr=PIPE, stdout=PIPE)
		pipeTestPart1.stdout.close() 
        
        #Get the out of the command run
        (out, err) = pipeTestPart2.communicate()
		testResults = err

	return testResults

#3 PIPE Switching Test (Bid-drectional PIPE): 
#---------------------------------------------
def pipeSwitchTest():

	#
	testResults = ""

	#cat temp.dat > myFIFO and then in another terminal run cat myFIFO | cpipe -vr -vw -vt
	pipeTestPart1 = Popen(["cat", "temp.dat"], stderr=PIPE, stdout=PIPE)
	pipeTestPart2 = Popen(["cat"], stdin=pipeTestPart1.stdout, stderr=PIPE, stdout=PIPE)
	pipeTestPart3 = Popen(["cpipe", "-vr", "-vw", "-vt"], stdin=pipeTestPart2.stdout, stderr=PIPE, stdout=PIPE)

	pipeTestPart1.stdout.close()
	pipeTestPart2.stdout.close()

	(out, err) = pipeTestPart3.communicate()
	testResults = err

	return testResults

#4. Process Creation
def procCreationTest():
	
	testResults = ""
	
	startTime = time()

	#Start Process
	proc = Process(target = system("ping 127.0.0.1 -s 504 -c 1 > /dev/null 2>&1"))
	proc.start()
	proc.join()	

	#Fork Process
    childProcPID = fork()
	
	#Terminates the Child and Parent Process
	if childProcPID == 0:
		_exit(0)

	proc.terminate()
	endTime = time()

	procTime = endTime - startTime

	testResults = "Process started/forked/stopped in %s seconds" % (str(procTime))
	
	return testResults

#5	
def execlTest():	
	testResult = ""
	#startTime = time()
	numOfExeclCmd = 0

    #print "%s time(s) execl commands ran in seconds " % numOfExeclCmd
	duration = time() + 60
	#loop for 60 seconds
	while time() < duration:
		#childProcPID = fork()
		#child_pids.append(childProcPID)
	        #if childProcPID == 0:
	        	#execl("/bin/echo", "temp.dat")
		        #child_pids.append(childProcPID)

		#On Unix, with shell=False (default): In this case, the Popen class uses os.execvp() to execute the child program. 
		#https://docs.python.org/3.1/library/subprocess.html
		proc = Popen(["cat", "temp.dat"], stderr=PIPE, stdout=PIPE, shell=False)

	        #Get the out of the command run
		(out, err) = proc.communicate()
		numOfExeclCmd += 1
		
	testResult = "%s time(s) execl commands ran in 60 seconds " % numOfExeclCmd

	return testResult

#6
def shellScriptTest():
        testResult = ""
        numOfScriptsRan = 0
      
	duration = time() + 60 #time in seconds + 60 sec = 1 min
        #loop for 60 seconds
        while time() < duration:
	        for i in range(8):
			system("./testShellScript.sh > /dev/null 2>&1") #1

		numOfScriptsRan += 1
        testResult = "%s time(s) shell script ran in 60 seconds " % numOfScriptsRan
        return testResult
	
# ###################################
#     M A I N    P R O G R A M
# ###################################
if __name__=='__main__':

	system("clear")

	selinuxModes = {0:"SELinux is in Permissive Mode", 1:"SELinux is in Enforcing Mode"} 

	for mode in selinuxModes:
		Popen(["setenforce", "%s" % mode], stderr=PIPE, stdout=PIPE)
		print "="*70
		print "\t\t%s" % selinuxModes[mode]
		print "="*70

		print "\n#1. File Copy Test:"
		print "-"*20
		fileSizeList = ["500b", "1K", "4K"]
		fileTestResults = fileCopyTest(fileSizeList)
		for test,results in fileTestResults.items():
			print "- %s Test: %s files were copied in 10 seconds)" % (test, len(results))
			
		#2
		print "\n#2. PIPE Throughput:"
		print "-"*20
		pipeTestResult = pipeTest()
		print pipeTestResult

		#3
		print "#3. PIPE Switching Test:"
		print "-"*24
		pipeSwitchTestResult = pipeSwitchTest()
		print pipeSwitchTestResult

		#4 - http://pubs.opengroup.org/onlinepubs/9699919799/functions/wait.html
		print "#4. Process Creation Test:"
		print "-"*26
		procCreationTestResults = procCreationTest()
		print procCreationTestResults

		#5
		print "\n#5. EXECL Test:"
		print "-"*20
		execlTestResult = execlTest()
		print execlTestResult

		#6
		print "\n#6. ShellScrip Test:"
		print "-"*25
		shellScriptResult = shellScriptTest()
		print shellScriptResult