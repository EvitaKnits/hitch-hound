from django.db import models


class Project(models.Model):
    """ This model represents a Project, which is assigned issues """
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
