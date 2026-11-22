from django.contrib.auth.models import User
from rest_framework import serializers
class RegisterSerializer(serializers.ModelSerializer):
 password=serializers.CharField(write_only=True,min_length=8)
 class Meta:
  model=User
  fields=["id","username","email","password"]
 def create(self,data):
  return User.objects.create_user(**data)
class MeSerializer(serializers.ModelSerializer):
 is_manager=serializers.BooleanField(source="is_staff",read_only=True)
 class Meta:
  model=User
  fields=["id","username","email","is_manager"]
