from django.core.management.base import BaseCommand
from tickets.models import Category
class Command(BaseCommand):
 def handle(self,*args,**kwargs):
  for name in ["Техническая проблема","Аккаунт","Другое"]:
   Category.objects.get_or_create(name=name)
  self.stdout.write("Categories ready")
