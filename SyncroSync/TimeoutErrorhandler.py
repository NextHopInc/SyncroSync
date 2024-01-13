import time 

def timeOutError(): 
    total_mins = 60
    while(total_mins):
        mins , secs = divmod(total_mins,60)
        timer = '{:02d}:{:02d}'.format(mins,secs)
        print(timer,end='\r')
        time.sleep(1)
        total_mins-=1
    print("Timer Done")
    return 0 