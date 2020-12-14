import sys
import os
import time
import logging
import LPD
import postReq
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
 

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        for img in os.listdir(folderToWatch):
            name = str(folderToWatch+img)
            plate_number = LPD.getPlateNumber(name)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            data = {
                'plate_number': plate_number,
                'current_time': current_time
            }
            #postReq.sendPlate(self, data)
    

folderToWatch = '.'
observer = Observer()
event_handler = Handler()
observer.schedule(event_handler, folderToWatch, recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()







