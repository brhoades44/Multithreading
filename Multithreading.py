###########################################################################################
# Bruce Rhoades - Weak References and Multithreading Code Samples
###########################################################################################

from multiprocessing import Pool

import threading
import time
import MultiThreadTester
import WeakRefTester

COUNT = 50000000
###########################################################################################
# A heavy computational operation to see differences between single thread, multi thread
# and multi process approaches
###########################################################################################
def countdown(n):
    while n>0:
        n -= 1
        
###########################################################################################
# Testing a heavy computational operation a few different ways - One using a single thread
# one using multiple threads and another using multiple processes
# Shows that Multithread actually slows down the operation for CPU Bound problems like this
# Single threaded performance is better, with MultiProcess better yet as multi-cpu support
# of computers are utilized, although more code is needed to support this so the added
# complexity needs to be considered
###########################################################################################
def testMultiThreading10VsMultiProcessingVsSingleThread():
    if __name__ == '__main__':
        print("Implementing lengthy, CPU-Bound Operation...")
        testCPUIntenseSingleThread()
        testCPUIntenseOpMultiThread()
        testCPUIntenseOpMultiProcess()

###########################################################################################
#  Testing a heavy computational operation via a single thread/process
###########################################################################################
def testCPUIntenseSingleThread():
    start = time.time()
    countdown(COUNT)
    end = time.time()
    print('Single Process Time taken in seconds -', end - start)

###########################################################################################
#  Testing a heavy computational operation via multiple thread
###########################################################################################
def testCPUIntenseOpMultiThread():
    t1 = threading.Thread(target=countdown, args=(COUNT//2,))
    t2 = threading.Thread(target=countdown, args=(COUNT//2,))

    start = time.time()
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    end = time.time()
    print('Multi Thread Time taken in seconds -', end - start)

###########################################################################################
#  Testing a heavy computational operation via multiple processes
###########################################################################################
def testCPUIntenseOpMultiProcess():
    if __name__ == '__main__':
        pool = Pool(processes=2)
        start = time.time()
        r1 = pool.apply_async(countdown, [COUNT//2])
        r2 = pool.apply_async(countdown, [COUNT//2])
        pool.close()
        pool.join()
        end = time.time()
        print('Multi Process Time taken in seconds -', end - start)

###########################################################################################
# Function to query a process selection from the user until a valid response is given
###########################################################################################
def getProcessSelection():
    processSelection = ''
    while (processSelection != 'q'):
        print("""\n        1.) Weak Reference - Dictionary
        2.) Weak Reference - Weak References, Proxies and Reference Counts
        3.) Threading - Threading with Inheritance
        4.) Threading - Daemon Threads
        5.) Threading - List of Threads
        6.) Threading - List of Threads with ThreadPoolExecutor
        7.) Threading - Race Conditions (not thread safe)
        8.) Threading - Race Conditions (using Locks)
        9.) Threading - RLock
        10.) Threading - Producer/Consumer Scenario
        11.) Threading - Producer/Consumer with Queue Scenario
        12.) CPU Bound Operation - Comparing Single Thread vs Multi Thread vs Multi Process""")
        processSelection = input("\nOutput from last menu selection may require you to scroll above the menu.\nPlease make a selection from the above choices. Please Enter a Value Between 1 and 12 (or q to quit): ")
        if(processSelection not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']):
            if(processSelection != 'q'):
                print("\nINVALID SELECTION!\n")
            continue
        else:
            break

    return processSelection

######################################################
# Main
######################################################
if(__name__ == "__main__"):
    #intro()
    processSelection = ''
    while(processSelection != 'q'):
        processSelection = getProcessSelection()
        print('\n')
        if(processSelection != 'q'):
            if(processSelection == '1'):
                WeakRefTester.testWeakRefTester1()
            elif(processSelection == '2'):
                WeakRefTester.testWeakRefTester2()
            elif(processSelection == '3'):
                MultiThreadTester.testMultithreading1ThreadInheritance()
            elif(processSelection == '4'):
                MultiThreadTester.testMultithreading2DaemonThreads(True)
                print('Application Terminating to show Thread 1 not finishing if it is a Daemon Thread')
                processSelection = 'q'
            elif(processSelection == '5'):
                MultiThreadTester.testMultithreading3ListOfThreads()
            elif(processSelection == '6'):
                MultiThreadTester.testMultithreading4ThreadPoolExecutor()
            elif(processSelection == '7'):
                MultiThreadTester.testMultiThreading5RaceConditions(False)
            elif(processSelection == '8'):
                MultiThreadTester.testMultiThreading6RaceConditions()
            elif(processSelection == '9'):
                MultiThreadTester.testMultiThreading7RLock()
            elif(processSelection == '10'):
                MultiThreadTester.testMultiThreading8ProducerConsumer()
            elif(processSelection == '11'):
                MultiThreadTester.testMultiThreading9ProducerConsumerQueues()
            else:
                testMultiThreading10VsMultiProcessingVsSingleThread()

###########################################################################################
# Other multithreading considerations
#
# The Python Global Interpreter Lock or GIL, in simple words, is a mutex (or a lock) that 
# allows only one thread to hold the control of the Python interpreter.
#
# This means that only one thread can be in a state of execution at any point in time. The 
# impact of the GIL isn’t visible to developers who execute single-threaded programs, but it 
# can be a performance bottleneck in CPU-bound and multi-threaded code.
#
# The GIL (Global Interpreter Lock) does not have much impact on the performance of 
# I/O-bound multi-threaded programs as the lock is shared between threads while they are
#  waiting for I/O.
#
# But a program whose threads are entirely CPU-bound, e.g., a program that processes an 
# image in parts using threads, would not only become single threaded due to the lock but 
# will also see an increase in execution time, in comparison to a scenario where it was written 
# to be entirely single-threaded.
# This increase is the result of acquire and release overheads added by the lock.
#
# What about the programs where some threads are I/O-bound and some are CPU-bound?
# Python’s GIL was known to starve the I/O-bound threads by not giving them a chance to 
# acquire the GIL from CPU-bound threads. This was because of a mechanism built into Python 
# that forced threads to release the GIL after a fixed interval of continuous use and if 
# nobody else acquired the GIL, the same thread could continue its use.
#
# Using multiple processes can be a better approach for CPU intensive operations as the 
# 10th example above illustrates. But multiple processes are heavier than multiple 
# threads so scaling can be an issue
#
# In conclusion, the GIL can be an issue when using CPU-bound multi-threading or 
# writing C extenstions
#
# I/O Bound Process - Speeding up a program involves overlapping the times spent 
# waiting for these devices.
#
# CPU Bound Process - Speeding up a program involves finding ways to do more 
# computations in the same amount of time.
###########################################################################################

###########################################################################################
# More about multiprocessing
#
# With multiprocessing, Python creates new processes. A process here can be thought of as 
# almost a completely different program, though technically they’re usually defined as a 
# collection of resources where the resources include memory, file handles and things like 
# that. One way to think about it is that each process runs in its own Python interpreter.
# Different processes run on a different core in the processor, so they are actually
# running at the same time. There are some complications that arise from doing this, but 
# Python does a pretty good job of smoothing them over most of the time.
###########################################################################################

