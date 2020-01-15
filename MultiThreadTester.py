###########################################################################################
# Bruce Rhoades - Several Methods to test MultiThreading 
#
# There is a lot of code here, but broken down into distinct pieces and used with the script 
# Multithreading.py. The distinct pieces are numbered below. The code starts with some 
# classes used by some of the "distinct pieces", then functions that implement the numbered
# items below follow those classes. Finally, items 8 and 9 are at the bottom. They both start
# with Pipeline classes followed by supporting functions to illustrate those two items.
# 
# Cheers!
#
# 1.) Threading with Inheritance
# 2.) Daemon Threads
# 3.) List of threads 
# 4.) List of threads with ThreadPoolExecutor
# 5.) Race conditions that are not thread safe
# 6.) Locks to address the issue of race conditions
# 7.) RLock
# 8.) Producer/Consumer scenario
# 9.) Producer/Consumer with Queue scenario
############################################################################################

###########################################################################################
# Other Multithreading concepts not illustrated here are Semaphors, Timers and Barriers
# 
# Semaphors: Manages internal counters that decrement when a call is made to acquire() and 
# increment for each call to release(). If the counter goes below zero, it will block and 
# wait for a call to release(). A good example for semaphor use is when a pool of connections
# is needed and wanted to limit that pool size to a specific number
#
# Timers are used to start a function after a specified time has elapsed.
#
# Barriers are used to keep a fixed number of threads in sync. Each thread calls wait() on
# the barrier. They remain blocked until the specified number of threads are waiting
# and then are all released at the same time (although really they are scheduled by the os
# and run one at a time). One use for a Barrier is to allow a pool of threads to initialize
# themselvess. The threads waiting after they are initialized will ensure none of the 
# threads start running before all the threads have been initialized
###########################################################################################

import concurrent.futures
import logging
import queue
import random
import threading
import time
import ZipADeeDooDah as zaddd
import XKCDPassword as xkcdp

###########################################################################################
# The classes below are used in the Threading sample code that follows them
###########################################################################################


###########################################################################################
# Class To test Race Conditions - Showing a shared resource (dbValue) not protected with 
# multithreading synchronization techniques. dbValue does not get written back properly in
# a multithreading environment (i.e., can retain a value of 1 if updated in more than one
# thread)
###########################################################################################
class FakeDatabase:
    def __init__(self):
        self.dbValue = 0

    # simulate reading a value from a db, updating it and 
    # then writing it back
    def update(self, threadName):
        readDBValue = self.dbValue
        readDBValue += 1
        logging.info("Thread %s: Increasing value by %d", threadName, readDBValue)

        # pause current thread and allow other threads to run
        time.sleep(0.1)
        self.dbValue = readDBValue
        logging.info("Thread %s: finishing update", threadName)


###########################################################################################
# Testing updating with lock to allow for safe dbValue updating in a multithreading
# environment
###########################################################################################
class FakeDatabaseWithLock:
    def __init__(self):
        self.dbValue = 0
        self._lock = threading.Lock()

    # update the database using a lock
    def update(self, threadName):
        logging.info("Thread %s: starting update", threadName)
        logging.debug("Thread %s: about to lock", threadName)

        # lock functions as a context manager, so lock released at end of the with code block
        with self._lock:
            logging.debug("Thread %s: has lock", threadName)
            readDBValue = self.dbValue
            readDBValue += 1
            logging.info("Thread %s: Updating with value %d", threadName, readDBValue)
            time.sleep(0.1)
            self.dbValue = readDBValue
            logging.debug("Thread %s: about to release lock", threadName)

        logging.debug("Thread %s: after release", threadName)
        logging.info("Thread %s: finishing update", threadName)
        

###########################################################################################
# Using RLock to make multiple updates with the same lock
# If a regular lock is used, the changeValues1And2 function would block as that function 
# "acquires" the lock, but the changeValue1() and changeValue2() functions also try to 
# acquire the lock but the changeValues1And2 function have not "released" the lock
###########################################################################################
class RLockTester:
    def __init__(self):
        self.value1 = 1
        self.value2 = 2
        self.lock = threading.RLock()

    def changeValue1(self):
        with self.lock:
            self.value1 = self.value1 + 1

    def changeValue2(self):
        with self.lock:
            self.value2 = self.value2 + self.value1

    def changeValues1And2(self):
        # changeValue1 and changeValue2 are thread safe
        # Using a regular lock would block the logic in
        # the calls to changeValue1 and changeValue2
        with self.lock:
            self.changeValue1()
            self.changeValue2()
            print("Using RLock to update 2 values, each of which also uses RLock (regular lock would block):", self.value1, self.value2)


###########################################################################################
# Functions (prefixed with "test") implementing the 9 "Distinct Pieces" Start here
###########################################################################################

###########################################################################################
# The sample below shows threading using a class (ZipADeeDooDah) that inherits from the 
# thread class
# 
# Method to test threading by starting a lengthy process in one thread and then continue
# with a shorter process in the main thread.  Threads perform separate and independent 
# operations - one to unzip a password-protected folder with many files containing music 
# sheets and another to unzip a folder containing files containing words to be randomly 
# selected for a passphrase
# 
# Lengthy process will start with output - Start Extracting MusicSheets.zip
# Lengthy process will end with output - End Extracting MusicSheets.zip
# Shorter process will start with output - Start generation of Passphrase from word files
# Shorter process will end with output - End of generation of Passphrase from word files
###########################################################################################
def testMultithreading1ThreadInheritance():
    unzipMusicSheets = zaddd.ZipADeeDooDah()
    print("New Thread Starting...")
    unzipMusicSheets.start()
    print("Main Thread Starting Next Operation...")
    xkcdp.XKCDPassword.generatePassphraseFromWordFiles()
    print("Joining New Thread to Main")
    unzipMusicSheets.join()

###########################################################################################
#  The function below is used by a few of the threading examples that follow
############################################################################################
def threadFunction(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)


###########################################################################################
# Similar to testMultithreading1 but here assigning the thread function instead of 
# deriving from the Thread class. Can uncomment out the thread.join() line for the main 
# thread to join the one created which will wait for the threadFunction to complete
# before proceeding
#
# param isDaemon, when true, will create a daemon thread which will shut down when the
# program ends. Hence, if the thread is not joined to the main thread, the thread
# will not complete and its logging of Thread finishing will not be output
###########################################################################################
def testMultithreading2DaemonThreads(isDaemon=False):
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    thread = threading.Thread(target=threadFunction, args=(1,), daemon=isDaemon)
    logging.info("Main    : before running thread")
    thread.start()
    logging.info("Main    : wait for the thread to finish")
    #thread.join()
    logging.info("Main    : all done")


###########################################################################################
# Creates a list of threads and starts them. Iterates the list and joins the threads to 
# the main thread. Execution of the threads is indeterminate - they can complete in an
# unpredictable order before they are joined or if the join takes place before they are 
# complete then a thread will wait for another to finish
###########################################################################################
def testMultithreading3ListOfThreads():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    print("The ordering of the threads completing is unpredictable")
    threads = []
    for index in range(3):
        logging.info("Main    : create and start thread %d.", index)
        thread = threading.Thread(target=threadFunction, args=(index,))
        threads.append(thread)
        thread.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)


###########################################################################################
# Recommended version of testMultithreading3 using ThreadPoolExecutor and an executor
# Scheduling of threads determined by Operating system
###########################################################################################
def testMultithreading4ThreadPoolExecutor():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    # The end of the with block causes ThreadPoolExecutor to do a join on each 
    # of the threads in a pool - map allows for iterating over the range of 3 values
    print("The ordering of the threads completing is unpredictable")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(threadFunction, range(3))

############################################################################################
# Method to test racing conditions. Using useLock as False shows the racing condition of 
# a (simulated) database update functioning incorrectly in a multithreaded envrionment. 
#
# Using useLock as True updates the db correctly in a multithreaded environment
# useDebug as True will enable more detailed logging in the case of useLock=True
###########################################################################################
def testMultiThreading5RaceConditions(useLock=True, useDebug=False):
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    if(useDebug == True):
        logging.getLogger().setLevel(logging.DEBUG)

    if(useLock == True):
        database = FakeDatabaseWithLock()
    else:
        database = FakeDatabase()

    logging.info("Testing update. Starting value is %d.", database.dbValue)

    # using submit to execute the database.update function in its own thread
    # creating two threads in this case but updating the database with the 
    # update instance method of the same database object
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.update, index)
    logging.info("Testing update. Ending value is %d.", database.dbValue)


###########################################################################################
# Tests multithreading with race conditions using a Lock for proper multithreading access
# to a protected db resource. 
#
# Can set useDebug to False to turn off more detailed logging
###########################################################################################
def testMultiThreading6RaceConditions():
    testMultiThreading5RaceConditions(useDebug=True)

###########################################################################################
# Using RLock to make multiple updates with the same lock
# See RLockTester for more information
###########################################################################################
def testMultiThreading7RLock():
    rlockTester = RLockTester()
    rlockTester.changeValues1And2()


ENDPRODUCING = object()

###########################################################################################
# The code below addresses items 8 and 9 of the "distinct pieces." 
# Supporting code for item #8 is the pipeline class below followed by implementing functions
# Supporting code for item #9 follows that code with another pipeline class followed by 
# its implementors
###########################################################################################

###########################################################################################
# Class to mimic a pipeline between producer and consumer. This approach works for a limited
# amount of data but is not a great producer-consumer solution because it only allows a 
# single value into a pipeline at a time. See class PipelineWithQueue for an approach that
# supports multiple values in a pipeline
#
# Typical flow is below. Process can run in an iterative fashion x number of times
# 
# 1.) Init: Consumer lock is locked
# 2a.) Producer gets a message where setMessage will lock the Producer
# 2b.) Consumer can try to read, but its lock is blocked in step #1
# 3.) Producer locks to prevent other "producing", sets the message
# 4.) Producer then releases getLock to allow consumer to read
# 5a.) Consumer can then proceed - i.e., "have getLock" executes
# 5b.) Calls to setMessage will be blocked until getMessage releases the producer lock
###########################################################################################
class Pipeline:
    def __init__(self):
        self.message = 0
        self.producerLock = threading.Lock()
        self.consumerLock = threading.Lock()

        # Initial state is unlocked, so lock the consumer
        self.consumerLock.acquire()

    # mimic consuming a message from a data source (i.e., network)
    def getMessage(self, name):
        logging.debug("%s:about to acquire getlock", name)

        # set the consumer lock and get the message. This will block until
        # a setMessage releses the consumer lock 
        self.consumerLock.acquire()
        logging.debug("%s:have getlock", name)

        # Save the message to save the data in the message in case when the producer lock
        # is released, the message is overwritten before this function returns!!
        message = self.message
        logging.debug("%s:about to release setlock", name)

        # release producer lock to allow producer to add messages
        self.producerLock.release()
        logging.debug("%s:setlock released", name)
        return message

    # mimic producing a message to a data source (i.e., network)
    def setMessage(self, message, name):
        logging.debug("%s:about to acquire setlock", name)

        # set the producer lock and set the message. This will block until
        # a getMessage releases the producer lock
        self.producerLock.acquire()
        logging.debug("%s:have setlock", name)
        self.message = message
        logging.debug("%s:about to release getlock", name)

        # unlock the consumer lock to allow consumer to read the value 
        self.consumerLock.release()
        logging.debug("%s:getlock released", name)
        

###########################################################################################
# Method to mimic Reading messages from a network and place them into a Pipeline
###########################################################################################
def producer(pipeline):
    # Mimic we're getting a message from the network.
    for index in range(10):
        message = random.randint(1, 101)
        logging.info("Producer got message: %s", message)
        pipeline.setMessage(message, "Producer")

    # Send a EndProducing message to tell consumer we're done
    pipeline.setMessage(ENDPRODUCING, "Producer")

###########################################################################################
# Mehthod to mimic Reading message from a pipeline populated by the producer
###########################################################################################
def consumer(pipeline):
    # Mimic a number in the database.
    message = 0
    while message is not ENDPRODUCING:
        message = pipeline.getMessage("Consumer")
        if message is not ENDPRODUCING:
            logging.info("Consumer storing message: %s", message)


###########################################################################################
# Method to spawn two threads: One to mimic reading data from a network and put it into a
# Pipeline. And another to mimic reading data from a pipeline and writing it to a db
# More information on the data flow can be found in comments for the Pipeline class
###########################################################################################
def testMultiThreading8ProducerConsumer():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)

    print("Limitation here is a single item in a pipeline at a time")
    pipeline = Pipeline()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)


###########################################################################################
# Class to mimic a pipeline between producer and consumer. Uses a queue to allow processing
# of multiple messages at a time
#
# Queues are frequently used in multithreading envrionments, so locking code is located
# within the Queue class itself so it is thread safe
#
# Note that this class just extends the Queue class with logging. Queue class can be used
# directly
###########################################################################################
class PipelineWithQueue(queue.Queue):
    def __init__(self):
        super().__init__(maxsize=10)

    # mimic consuming a message from a data source (i.e., network)
    def getMessage(self, name):
        logging.debug("%s:about to get from queue", name)
        value = self.get()
        logging.debug("%s:got %d from queue", name, value)
        return value

    # mimic producing a message to a data source (i.e., network)
    def setMessage(self, value, name):
        logging.debug("%s:about to add %d to queue", name, value)

        # put will block until there are less than maxsize elements
        self.put(value)
        logging.debug("%s:added %d to queue", name, value)


###########################################################################################
# Method to mimic Reading messages from a network and place them into a Pipeline
# Uses an event instead of a counter
###########################################################################################
def producerWithEvent(pipeline, event):
    # Mimic getting a number from the network.
    while not event.is_set():
        message = random.randint(1, 101)
        logging.info("Producer got message: %s", message)
        pipeline.setMessage(message, "Producer")

    logging.info("Producer received EXIT event. Exiting")


###########################################################################################
# Mehthod to mimic Reading message from a pipeline populated by the producer
# Uses event instead of ENDPRODUCING indicator
###########################################################################################
def consumerWithEvent(pipeline, event):
    # Mimic saving a number in the database
    # We need to check pipleline.empty() as well here because the event may have been
    # triggered after the producer checked the event.is_set() but before the pipeline 
    # calls setMessage. If the queue is completely full, the producer can still call 
    # setMessage() which will wait until there is room on the queue for the new message
    # The consumer would have already exited so no room on the queue will exist and thus
    # the producer will not exit
    while not event.is_set() or not pipeline.empty():
        message = pipeline.getMessage("Consumer")
        logging.info(
            "Consumer storing message: %s  (queue size=%s)",
            message,
            pipeline.qsize(),
        )

    logging.info("Consumer received EXIT event. Exiting")


###########################################################################################
# Method to spawn two threads: One to mimic reading data from a network and put it into a
# Pipeline. And another to mimic reading data from a pipeline and mimic writing it to a db
#
# Test using an event with a pipeline
###########################################################################################
def testMultiThreading9ProducerConsumerQueues():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    #logging.getLogger().setLevel(logging.DEBUG)

    # using PipelineWithQueue class here for logging. Can also use Queue class directly
    pipeline = PipelineWithQueue()
    event = threading.Event()
    print("Allows for multiple items in a pipeline at a time")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producerWithEvent, pipeline, event)
        executor.submit(consumerWithEvent, pipeline, event)

        time.sleep(0.1)
        logging.info("Main: about to set event")
        event.set()