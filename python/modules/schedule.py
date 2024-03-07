import sched
import time
from datetime import timedelta
from python.model.FileSystemNodeModel import *


class FileOrganizerScheduler:
    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def organize_files_weekly(self, path):
        # Schedule the organization task to run weekly
        now = datetime.now()
        next_week = now + timedelta(weeks=1)
        delta = next_week - now
        seconds_until_next_week = delta.total_seconds()
        self.scheduler.enter(seconds_until_next_week, 1, self.organize_files_weekly, (path,))
        print(f"Next organization scheduled for: {next_week}")
        # Start the scheduler
        self.scheduler.run()


if __name__ == "__main__":
    # scheduler = FileOrganizerScheduler()
    # # Specify the file path to be organized
    # file_path_schedule = "/home/evelynchelsea/test music"
    # # dir_node = organise.dir_node
    # # Call the organise function
    # cache = FileSystemCache()
    # dir_node = Directory("/home/evelynchelsea/test music", cache, 'test_music', None)
    # organise(dir_node)
    pass