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


class AuthenticationFlowTests(APITestCase):
 def test_register_login_refresh_and_me(self):
  response=self.client.post("/api/auth/register/",{"username":"new_customer","email":"customer@example.com","password":"strongpass123"},format="json")
  self.assertEqual(response.status_code,201,response.data)
  response=self.client.post("/api/auth/token/",{"username":"new_customer","password":"strongpass123"},format="json")
  self.assertEqual(response.status_code,200,response.data)
  self.assertIn("access",response.data)
  self.assertIn("refresh",response.data)
  refreshed=self.client.post("/api/auth/token/refresh/",{"refresh":response.data["refresh"]},format="json")
  self.assertEqual(refreshed.status_code,200,refreshed.data)
  self.client.credentials(HTTP_AUTHORIZATION="Bearer "+refreshed.data["access"])
  me=self.client.get("/api/auth/me/")
  self.assertEqual(me.status_code,200,me.data)
  self.assertEqual(me.data["username"],"new_customer")
  self.assertFalse(me.data["is_manager"])
 def test_manager_role_is_server_controlled(self):
  manager=User.objects.create_user(username="support_manager",password="strongpass123",is_staff=True)
  response=self.client.post("/api/auth/token/",{"username":"support_manager","password":"strongpass123"},format="json")
  self.assertEqual(response.status_code,200,response.data)
  self.client.credentials(HTTP_AUTHORIZATION="Bearer "+response.data["access"])
  me=self.client.get("/api/auth/me/")
  self.assertTrue(me.data["is_manager"])
 def test_wrong_password_rejected(self):
  User.objects.create_user(username="customer",password="strongpass123")
  response=self.client.post("/api/auth/token/",{"username":"customer","password":"wrongpass"},format="json")
  self.assertEqual(response.status_code,401)
 def test_unauthenticated_tickets_rejected(self):
  self.assertEqual(self.client.get("/api/tickets/").status_code,401)
