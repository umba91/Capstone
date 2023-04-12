from django.db import models

class Banner(models.Model):
    img = models.CharField(max_length=200)
    alt_text = models.CharField(max_length=300)

class Species(models.Model):
    title = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = "bug_imgs/")

    def __str__(self):
        return self.title

class Color(models.Model):
    title = models.CharField(max_length = 100)

    def __str__(self):
        return self.title

class Size(models.Model):
    title = models.CharField(max_length = 100)

    def __str__(self):
        return self.title
    
# Bug Model
class Bug(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="bug_imgs/")
    description = models.TextField()
    facts = models.TextField()
    factnum = models.IntegerField()
    species = models.ForeignKey(Species,on_delete=models.CASCADE)
    status = models.BooleanField(default=True) #can't see on frontend

    def __str__(self):
        return self.title
    
class BugAttribute(models.Model):
    bug = models.ForeignKey(Bug,on_delete=models.CASCADE)
    species = models.ForeignKey(Species,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    size = models.ForeignKey(Size,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
