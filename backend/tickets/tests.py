from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category,Ticket
class TicketSecurityTests(APITestCase):
 def setUp(self):
  self.a=User.objects.create_user(username="alice",password="pass12345")
  self.b=User.objects.create_user(username="bob",password="pass12345")
  self.manager=User.objects.create_user(username="manager",password="pass12345",is_staff=True)
  self.category=Category.objects.create(name="Technical")
  self.ticket=Ticket.objects.create(title="Secret",description="Private",category=self.category,author=self.a)
 def test_other_user_cannot_read_or_comment(self):
  self.client.force_authenticate(self.b)
  for url in [f"/api/tickets/{self.ticket.id}/",f"/api/tickets/{self.ticket.id}/comments/"]:
   self.assertEqual(self.client.get(url).status_code,404)
  self.assertEqual(self.client.post(f"/api/tickets/{self.ticket.id}/comments/",{"text":"hello"}).status_code,404)
 def test_user_cannot_change_status(self):
  self.client.force_authenticate(self.a)
  self.assertEqual(self.client.patch(f"/api/tickets/{self.ticket.id}/",{"status":"resolved"}).status_code,400)
 def test_manager_can_change_status(self):
  self.client.force_authenticate(self.manager)
  self.assertEqual(self.client.patch(f"/api/tickets/{self.ticket.id}/",{"status":"resolved"}).status_code,200)
 def test_delete_only_new_own_ticket(self):
  self.client.force_authenticate(self.a)
  self.ticket.status="in_progress"
  self.ticket.save()
  self.assertEqual(self.client.delete(f"/api/tickets/{self.ticket.id}/").status_code,403)
