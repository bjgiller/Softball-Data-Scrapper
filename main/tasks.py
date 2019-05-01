from background_task import background,tasks
from main.webtargets import Past
import datetime
import time
from main.dbgame import DB_Game_Interface

@background(schedule=10)
def daily():
    #print(i)
    print("Day:",datetime.datetime.now().day,",Month:",datetime.datetime.now().month,",Year:",datetime.datetime.now().year,",Hour:",datetime.datetime.now().hour,",Min: ",datetime.datetime.now().minute,"Sec: ",datetime.datetime.now().second)
    #time.sleep(1)
    #ws = Past(23,3,2019,None,24,3,2019)
