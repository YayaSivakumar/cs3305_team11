import sched
import time
from datetime import timedelta
from python.model.FileSystemNodeModel import *
from python.modules.organise import organise
import threading


class FileOrganizerScheduler:
    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.thread = None
        self.stop_requested = False
        self.next_organisation = ''
        self.next_organisation_event = None

    def start(self, dir_node):
        if self.thread is None or not self.thread.is_alive():
            # Schedule the first task immediately and start the scheduler in a background thread
            self.scheduler.enter(0, 1, self.organize_files_weekly, argument=(dir_node,))
            self.thread = threading.Thread(target=self.scheduler.run)
            self.thread.start()

        # Start the scheduler
        self.scheduler.run()
        return self.next_organisation

    def stop(self):
        self.stop_requested = True  # set the flag to request stop
        if self.thread is not None:
            self.scheduler.cancel(self.next_organisation_event)  # cancel the next event

    def organize_files_weekly(self, dir_node):
        if self.stop_requested:
            self.stop_requested = False
            return ''

        # perform the organization
        organise(dir_node)

        # Calculate next week's time
        next_week = datetime.now() + timedelta(weeks=1)
        seconds_until_next_week = (next_week - datetime.now()).total_seconds()
        self.next_organisation = next_week.strftime('%Y-%m-%d %H:%M:%S')

        # Schedule the next organization
        self.next_organisation_event = self.scheduler.enter(seconds_until_next_week, 1, self.organize_files_weekly, argument=(dir_node,))


if __name__ == "__main__":
    pass