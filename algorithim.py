from datetime import date
from task import Task


class Alorithim:
    def __init__(self, tasks: list[Task]):
        self.tasks = list(tasks)
        self.impossible = []
        self.today = date.today()
        self._normalize_tasks()
        self.lowest = None
        self.greatest = None
        self.maxima()
        if self.greatest is None:
            self.days = 0
            self.schedule = []
        else:
            self.days = max(0, (self.greatest.date_text - self.today).days)
            self.schedule = [[0 for _ in range(3)] for _ in range(self.days + 1)]

    def mainloop(self):
        while len(self.tasks) != 0:
            if self.possible():
                self.scheduler()

    def maxima(self):
        if not self.tasks:
            self.lowest = None
            self.greatest = None
            return
        self.lowest = self.tasks[0]
        self.greatest = self.tasks[0]
        for task in self.tasks[1:]:
            if task.date_text < self.lowest.date_text:
                self.lowest = task
            if task.date_text > self.greatest.date_text:
                self.greatest = task

    def _normalize_tasks(self):
        normalized = []
        for task in self.tasks:
            due = task.date_text
            if isinstance(due, str):
                try:
                    due = date.fromisoformat(due)
                except ValueError:
                    due = None
            if isinstance(due, date):
                task.date_text = due
            else:
                due = None

            duration = task.duration_text
            if isinstance(duration, str):
                duration = int(duration) if duration.isdigit() else None
            else:
                try:
                    duration = int(duration)
                except (TypeError, ValueError):
                    duration = None
            if duration is not None:
                task.duration_text = duration

            if due is None or duration is None:
                self.impossible.append(task)
            else:
                normalized.append(task)
        self.tasks = normalized

    def _normalized_availability(self, availability):
        slots = ["Morning", "Afternoon", "Evening"]
        if not availability:
            return slots
        available_set = set(availability)
        return [slot for slot in slots if slot in available_set]

    def possible(self):
        if not self.tasks:
            return False
        self.maxima()
        current = self.lowest
        if current is None:
            return False
        if current.date_text < self.today:
            self.impossible.append(current)
            self.tasks.remove(current)
            return False
        if current.duration_text <= 0:
            self.tasks.remove(current)
            return False
        days = (current.date_text - self.today).days + 1
        availability = self._normalized_availability(current.availability)
        slots_per_day = len(availability)
        if slots_per_day == 0 or (slots_per_day * days) < current.duration_text:
            self.impossible.append(current)
            self.tasks.remove(current)
            self.maxima()
            return False
        return True

    def scheduler(self):
        days = (self.lowest.date_text - self.today).days
        availability = self._normalized_availability(self.lowest.availability)
        for index, x in enumerate(self.schedule):
            if self.lowest.duration_text <= 0:
                self.tasks.remove(self.lowest)
                break
            if index > days:
                break
            if "Morning" in availability and x[0] == 0:
                self.schedule[index][0] = self.lowest.task_text
                self.lowest.duration_text -= 1
            if "Afternoon" in availability and x[1] == 0:
                self.schedule[index][1] = self.lowest.task_text
                self.lowest.duration_text -= 1
            if "Evening" in availability and x[2] == 0:
                self.schedule[index][2] = self.lowest.task_text
                self.lowest.duration_text -= 1
        if self.lowest in self.tasks and self.lowest.duration_text > 0:
            self.impossible.append(self.lowest)
            self.tasks.remove(self.lowest)
