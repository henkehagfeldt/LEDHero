def func():
    x = 5
    dell(x)
    print("X is: " + str(x) )
    del x 
    print("X is: " + str(x) )

def dell(x):
    print("deleting: " + str(x))
    del x

func()