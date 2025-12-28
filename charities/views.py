from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


User = get_user_model()

from accounts.permissions import IsCharityOwner, IsBenefactor
from charities.models import Task,Benefactor,Charity
from charities.serializers import (
    TaskSerializer, CharitySerializer, BenefactorSerializer
)
from accounts.serializers import UserSerializer

class BenefactorRegistration(generics.CreateAPIView):
    queryset = Benefactor.objects.all()
    serializer_class = BenefactorSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors})
     
    


class CharityRegistration(generics.CreateAPIView):
    queryset = Charity.objects.all()
    serializer_class = CharitySerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors})


class Tasks(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all_related_tasks_to_user(self.request.user)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsCharityOwner]

        return [permission() for permission in self.permission_classes]

    def filter_queryset(self, queryset):
        filter_lookups = {}
        for name, value in Task.filtering_lookups:
            param = self.request.GET.get(value)
            if param:
                filter_lookups[name] = param

        exclude_lookups = {}
        for name, value in Task.excluding_lookups:
            param = self.request.GET.get(value)
            if param:
                exclude_lookups[name] = param

        return queryset.filter(**filter_lookups).exclude(**exclude_lookups)

  
    def list(self, request, *args, **kwargs):
        user_id = request.user.id

       
        query_string = "&".join(
            [f"{k}={v}" for k, v in sorted(request.GET.items())]
        )

        cache_key = f"tasks:user:{user_id}:qs:{query_string}"

        cached_data = cache.get(cache_key)
        if cached_data is not None:
            print("✅ TASKS FROM REDIS")
            return Response(cached_data)

        print("❌ TASKS FROM DATABASE")

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

   
        cache.set(cache_key, serializer.data, timeout=300)

        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        data = {
            **request.data,
            "charity_id": request.user.charity.id
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

 
        cache.delete_pattern(f"tasks:user:{request.user.id}:*")

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskRequest(APIView):
    permission_classes = (IsBenefactor,)

    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        if task.state != "P":
            return Response(data={'detail':'This task is not pending.'},status=status.HTTP_404_NOT_FOUND)
        
        
        task.assign_to_benefactor(request.user.benefactor)
        #task_serializer = TaskSerializer(instance=task)
        #data = task_serializer.data
        return Response(data={'detail': 'Request sent.'} , status=status.HTTP_200_OK)

class TaskResponse(APIView):
    permission_classes = (IsCharityOwner,)

    def post(self, request , task_id):
        task = get_object_or_404(Task, pk=task_id)
        task_response = request.data.get('response')
        if not (task_response == 'A' or  task_response == 'R'):
            return Response(data={'detail': 'Required field ("A" for accepted / "R" for rejected)'},status=status.HTTP_400_BAD_REQUEST)
        if task.state != 'W':
            return Response(data={'detail': 'This task is not waiting.'},status=status.HTTP_404_NOT_FOUND)
        if task_response == 'A':
            task.state = 'A'
            task.save()
            return Response(data={'detail': 'Response sent.'},status=status.HTTP_200_OK)
        if task_response == 'R':
            task.state = 'P'
            task.assigned_benefactor = None
            task.save()
            return Response(data={'detail': 'Response sent.'},status=status.HTTP_200_OK)

class DoneTask(APIView):
    permission_classes = (IsCharityOwner,)
    def post(self, request , task_id):
        task = get_object_or_404(Task, pk=task_id)
        if task.state != 'A':
            return Response(data={'detail': 'Task is not assigned yet.'},status=status.HTTP_404_NOT_FOUND)
        
        if task.state == 'A':
            task.state = 'D'
            task.save()
            return Response(data={'detail': 'Task has been done successfully.'},status=status.HTTP_200_OK)




    
class UserCharityFieldsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch all users and charities
        user = User.objects.get(id=request.user.id)
        charity = Charity.objects.get(id=request.user.charity.id)

        # Serialize the data
        user_data = UserSerializer(user).data
        charity_data = CharitySerializer(charity).data

        # Return the serialized data
        return Response({
            'user': user_data,
            'charity': charity_data
        })
    
    def put(self, request, *args, **kwargs):
        user = request.user
        charity = Charity.objects.get(user=user)

        # Update user fields
        user.first_name = request.data.get('firstname', user.first_name)
        user.last_name = request.data.get('lastname', user.last_name)
        user.email = request.data.get('email', user.email)
        user.phone = request.data.get('phone', user.phone)
        user.address = request.data.get('address', user.address)
        user.description = request.data.get('description', user.description)
        user.gender = request.data.get('gender', user.gender)
        user.age = request.data.get('age', user.age)
        user.save()

        # Update charity fields
        charity.reg_number = request.data.get('regnumber', charity.reg_number)
        charity.name = request.data.get('charityname', charity.name)
        charity.save()

        return Response({'message': 'Data updated successfully'}, status=status.HTTP_200_OK)
    

class UserBenefactorFieldsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch all users and charities
        user = User.objects.get(id=request.user.id)
        benefactor = Benefactor.objects.get(id=request.user.benefactor.id)

        # Serialize the data
        user_data = UserSerializer(user).data
        benefactor_data = BenefactorSerializer(benefactor).data

        # Return the serialized data
        return Response({
            'user': user_data,
            'benefactor': benefactor_data
        })

    def put(self, request, *args, **kwargs):
        user = request.user
        benefactor = Benefactor.objects.get(user=user)

        # Update user fields
        user.first_name = request.data.get('firstname', user.first_name)
        user.last_name = request.data.get('lastname', user.last_name)
        user.email = request.data.get('email', user.email)
        user.phone = request.data.get('phone', user.phone)
        user.address = request.data.get('address', user.address)
        user.description = request.data.get('description', user.description)
        user.gender = request.data.get('gender', user.gender)
        user.age = request.data.get('age', user.age)
        user.save()

        # Update benefactor fields
        benefactor.experience = request.data.get('experience', benefactor.experience)
        benefactor.free_time_per_week = request.data.get('freeTime', benefactor.free_time_per_week)
        benefactor.save()

        return Response({'message': 'Data updated successfully'}, status=status.HTTP_200_OK)
