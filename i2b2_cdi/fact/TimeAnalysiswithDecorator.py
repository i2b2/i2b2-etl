from time import time
functionName=[]
timeTaken=[]
def total_time(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        filename = "/usr/src/app/tmp/timeAnalysis.csv"
        functionName.append(func.__name__)
        timeTaken.append(t2-t1)
        with open(filename,'a') as file:
            file.write(f'{func.__name__!r},{(t2-t1):.4f}')
            file.write("\n")
        return result
    return wrap_func
