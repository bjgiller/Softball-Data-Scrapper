from django.utils import timezone
from main.models import Completed

class DB_RPI_Interface:
    def __init__(self):
        self.g = None

    def get_incompleted(self):
        return Completed.objects.filter(completed=False)

    def create_single_completed(self,date,completed):
        self._add_to_db(team,date,completed,True)

    def _add_to_db(self,date,completed,override):
        exists = Completed.objects.filter(team_name=team).exists()

        #overriding
        if override and exists:
                self.g = Completed.objects.get(date=date)
                self.g.date = date
                self.g.completed = completed
                self.g.save()
        #adding
        else:
            self.g = Completed(date=date,completed=completed)
            self.g.save()

    def clear_table(self):
        for i in Completed.objects.all():
            i.delete()
