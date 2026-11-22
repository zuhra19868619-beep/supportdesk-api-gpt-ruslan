from django.db.models import Count
from rest_framework import generics,viewsets,exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category,Ticket
from .serializers import CategorySerializer,TicketSerializer,CommentSerializer
class CategoryList(generics.ListAPIView):
 queryset=Category.objects.all().order_by("name")
 serializer_class=CategorySerializer
 pagination_class=None
class TicketViewSet(viewsets.ModelViewSet):
 serializer_class=TicketSerializer
 http_method_names=["get","post","patch","delete","head","options"]
 filterset_fields=["status","category"]
 search_fields=["title"]
 ordering_fields=["created_at"]
 ordering=["-created_at"]
 def get_queryset(self):
  qs=Ticket.objects.select_related("author","category","assigned_to")
  return qs if self.request.user.is_staff else qs.filter(author=self.request.user)
 def perform_create(self,serializer):serializer.save(author=self.request.user)
 def perform_destroy(self,obj):
  if obj.author_id!=self.request.user.id or obj.status!=Ticket.Status.NEW:
   raise exceptions.PermissionDenied("Удалить может только автор нового обращения.")
  obj.delete()
 @action(detail=True,methods=["get","post"])
 def comments(self,request,pk=None):
  ticket=self.get_object()
  if request.method=="GET":
   return Response(CommentSerializer(ticket.comments.select_related("author"),many=True).data)
  serializer=CommentSerializer(data=request.data)
  serializer.is_valid(raise_exception=True)
  serializer.save(ticket=ticket,author=request.user)
  return Response(serializer.data,status=201)
class StatsView(generics.GenericAPIView):
 def get(self,request):
  qs=Ticket.objects.all() if request.user.is_staff else Ticket.objects.filter(author=request.user)
  return Response({"total":qs.count(),"by_status":dict(qs.values_list("status").annotate(count=Count("id")))})
