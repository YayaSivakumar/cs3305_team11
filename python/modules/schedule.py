import sched
import time
from datetime import timedelta
from python.model.FileSystemNodeModel import *
from python.modules.organise import organise
import threading


class FileOrganizerScheduler:
    def __init__(self):
        # Initialize the scheduler object with time functions
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.thread = None  # Initialize the thread object for running the scheduler in the background
        self.stop_requested = False # Flag to indicate if the scheduler should stop
        self.next_organisation = ''  # Stores the next organization time
        self.next_organisation_event = None  # Stores the event for the next organization

    def start(self, dir_node):
        # Check if there's no active thread or if the existing thread is not alive
        if self.thread is None or not self.thread.is_alive():
            # Schedule the first task immediately and start the scheduler in a background thread
            self.scheduler.enter(0, 1, self.organize_files_weekly, argument=(dir_node,))
            self.thread = threading.Thread(target=self.scheduler.run)
            self.thread.start()

        # Start the scheduler
        self.scheduler.run()
        return self.next_organisation   # Return the next organization time

    def stop(self):
        # Set the flag to request stopping the scheduler
        self.stop_requested = True  # set the flag to request stop
        if self.thread is not None:
            self.scheduler.cancel(self.next_organisation_event)  # cancel the next event

    def organize_files_weekly(self, dir_node):
        # Check if a stop has been requested
        if self.stop_requested:
            self.stop_requested = False # Reset the stop request flag
            return ''  # Exit the function

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