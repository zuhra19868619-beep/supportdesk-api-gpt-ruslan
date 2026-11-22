from django.db import models
from django.conf import settings
class Category(models.Model):
 name=models.CharField(max_length=100,unique=True)
 def __str__(self):return self.name
class Ticket(models.Model):
 class Status(models.TextChoices):
  NEW="new","Новое"
  IN_PROGRESS="in_progress","В работе"
  RESOLVED="resolved","Решено"
 title=models.CharField(max_length=200)
 description=models.TextField()
 category=models.ForeignKey(Category,on_delete=models.PROTECT)
 status=models.CharField(max_length=20,choices=Status.choices,default=Status.NEW)
 author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="tickets")
 assigned_to=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="assigned_tickets",limit_choices_to={"is_staff":True})
 created_at=models.DateTimeField(auto_now_add=True)
 updated_at=models.DateTimeField(auto_now=True)
 class Meta:ordering=["-created_at"]
class Comment(models.Model):
 ticket=models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name="comments")
 author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
 text=models.TextField()
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta:ordering=["created_at"]
