from datetime import date
from task import Task
class Alorithim:
    def __init__(self, tasks: list[Task]):
        self.tasks = tasks
        self.lowest = self.tasks[0]
        self.greatest =  self.tasks[0]
        self.maxima()
        self.impossible = []
        self.today = date.today()
        self.days = self.greatest.date_text - date.today()
        self.schedule = [[0 for i in range(3)] for j in range (self.days)]
    def mainloop(self):
        while len(self.tasks) != 0:
            if self.possible():
                self.scheduler()
                
    def maxima (self):
        if len (self.tasks) == 0:
            pass
        else:
            for task in self.tasks:
                if task.date_text < self.lowest.date_text:
                    self.lowest = task 
                if task.date_text > self.greatest.date_text:
                    self.greatest = task

    def possible(self):
        self.maxima()
        current = self.lowest
        if current.date_text < self.today:
            self.impossible.append(current)
            return False
        else:
            distance = current.date_text - self.today
            days = distance.days
            if len(current.availability) == 3 and (3 * days) < current.duration_text or len(current.availability) == 2 and (2 * days) < current.duration_text or len(current.availability) == 1 and days < current.duration_text:
                self.impossible.append(current)
                self.tasks.remove(current)
                self.maxima()
                return False
            else:
                return True
            
    def scheduler(self):
        distance = self.lowest.date_text - self.today
        days = distance.days
        combinations = [["Morning", "Afternoon", "Evening"], ["Morning", "Evening"], ["Evening", "Afternoon"], ["Morning", "Afternoon"],
                         ["Morning"], ["Afternoon"], ["Evening"]]
        availability = None
        if self.lowest.availability == None:
            availability = ["Morning", "Afternoon", "Evening"]
        else:
            for x in combinations:
                if set(x) == set(self.lowest.availability):
                    availability = x
        for index, x in enumerate(self.schedule):
            if self.lowest.duration_text == 0:
                self.tasks.remove(self.lowest)
                break
            if index > days:
                self.impossible.append(self.lowest)
                self.tasks.remove(self.lowest)
                break
            if  "Morning" in availability and x[0] == 0:
                self.schedule[index][0] = self.lowest.task_text
                self.lowest.duration_text -= 1
            if "Afternoon" in availability and x[1] == 0:
                self.schedule[index][1] = self.lowest.task_text
                self.lowest.duration_text -= 1
            if "Evening" in availability and x[2] == 0:
                self.schedule[index][2] = self.lowest.task_text
                self.lowest.duration_text -= 1
    
                
