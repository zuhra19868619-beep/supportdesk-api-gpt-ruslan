from rest_framework import serializers
from .models import Category,Ticket,Comment
class CategorySerializer(serializers.ModelSerializer):
 class Meta:
  model=Category
  fields=["id","name"]
class CommentSerializer(serializers.ModelSerializer):
 author_name=serializers.CharField(source="author.username",read_only=True)
 class Meta:
  model=Comment
  fields=["id","author","author_name","text","created_at"]
  read_only_fields=["author","created_at"]
class TicketSerializer(serializers.ModelSerializer):
 author_name=serializers.CharField(source="author.username",read_only=True)
 category_name=serializers.CharField(source="category.name",read_only=True)
 class Meta:
  model=Ticket
  fields=["id","title","description","category","category_name","status","author","author_name","assigned_to","created_at","updated_at"]
  read_only_fields=["author","created_at","updated_at"]
 def validate(self,attrs):
  user=self.context["request"].user
  if not user.is_staff:
   if "status" in attrs and (self.instance is None or attrs["status"]!=self.instance.status):
    raise serializers.ValidationError({"status":"Только менеджер может изменять статус."})
   if "assigned_to" in attrs:
    raise serializers.ValidationError({"assigned_to":"Только менеджер назначает ответственного."})
   if self.instance and self.instance.status!=Ticket.Status.NEW:
    raise serializers.ValidationError("Редактировать можно только новое обращение.")
  assigned=attrs.get("assigned_to")
  if assigned and not assigned.is_staff:
   raise serializers.ValidationError({"assigned_to":"Ответственный должен быть менеджером."})
  return attrs
