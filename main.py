from config import JellyfinSettings
import math
 
def main():
    print(62.5%60)
main()


def get_duration(ticks):
    time_seconds = ticks / 10_000_000
    if time_seconds < 60:
        seconds = time_seconds
        return {
            "seconds" : seconds
        }
    elif time_seconds > 60 and time_seconds < 60*60:
        minutes = time_seconds // 60
        seconds = time_seconds % 60
        return {
            "seconds" : seconds,
            "minutes" : minutes
        }        
    else:
        hours = time_seconds // 60**2
        minutes = (time_seconds - hours*60**2) // 60
        seconds = (time_seconds - hours*60**2) // 60
        return {
            "seconds" : seconds,
            "minutes" : minutes,
            "hours" : hours
        }        


print(get_duration(53687389999))



 