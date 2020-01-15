###########################################################################################
# A couple of functions to test Weak References, which are used to track objecs without
# creating a reference. They are added to a weakref table, and, when no longer being 
# used, removed from the table and a callback is triggered
###########################################################################################

import weakref, gc

###########################################################################################
# A couple dummy classes so that weak references can be tested
###########################################################################################
class weakRefTester1:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return str(self.value)

class weakRefTester2(list):
   pass


###########################################################################################
# Method testing Weak References by initializing a class variable through regular class
# instantiation. Using the weakref module, it then creates a dictionary whose key has a 
# weak reference to its value. Deleting the object shows that the reference to it in the 
# second print statement throws an exception as the object has been removed
#
# Uncommenting out the lines of code that are commented out shows no exception being thrown
# as the strong reference to the data is maintained 
###########################################################################################
def testWeakRefTester1():
    try:
        test = weakRefTester1(10)

        # create a weak reference to test through a dictionary reference
        weakRefDict = weakref.WeakValueDictionary()
        weakRefDict['key'] = test
        print("Referencing value in WeekValueDictionary prior to deletion: weakRefDict[key]=",weakRefDict['key'])

        # create a "strong" reference to test through a dictionary reference
        #strongRefDict = {}
        #strongRefDict['key'] = test
        #print("strongRefDict[ky]=",strongRefDict['key'])

        del test
        gc.collect()
        print("weakRefDict[key]=",weakRefDict['key'])
        #print("strongRefDict[key]=",strongRefDict['key'])

    except KeyError as err:
        print("Referencing value in WeekValueDictionary after deletion: Key error in WeakRefTester: Value was Garbage Collected {0}".format(err))
    except Exception as exc:
        print("Unknown error in WeakRefTester: {0}".format(exc))


###########################################################################################
# Method testing Weak References, Weak Proxies and Reference Counts
###########################################################################################
def testWeakRefTester2():
    # create a weakRefTester2 object called newList
    newList = weakRefTester2('WeakRefTester') 
    print("New List Object:", newList)

    # create a weak reference to newList
    weakRef = weakref.ref(newList, refCallback)

    # get a reference to the list referenced by the weak reference
    newWeakList = weakRef()

    # create a proxy to newList which uses a weak reference
    newProxy = weakref.proxy(newList, proxyCallBack)
    print("Weak reference to New List Object:", newWeakList)
    print('The object using a proxy: ' + str(newProxy))
    if newList is newWeakList:
        print("Original NewList is now a weak reference")
    
    print('The Weak reference count is: ' + str(weakref.getweakrefcount(newList)))
    del newList, newWeakList
    print("The weak reference is: " + str(weakRef()))
    

def refCallback(weakRef):
    print('deleting weak reference')

def proxyCallBack(weakProxy):
    print('deleting weak proxy')

