from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import mixins
from rest_framework import generics
from api.models import Chore
from api.serializers import ChoreSerializer
from api.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User


class ChoreList(APIView):
    """
    List all chores, or create a new chore.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request, format=None):
        chores = Chore.objects.all()
        serializer = ChoreSerializer(chores, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ChoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner = self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ChoreDetail(APIView):
    """
    Retrieve, update or delete a chore.
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_object(self, pk):
        try:
            return Chore.objects.get(pk=pk)
        except Chore.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        chore = self.get_object(pk)
        serializer = ChoreSerializer(chore)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        chore = self.get_object(pk)
        serializer = ChoreSerializer(chore, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        chore = self.get_object(pk)
        chore.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssignChore(APIView):
    """
    Assign a Chore
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Chore.objects.get(pk=pk)
        except Chore.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        chore = self.get_object(pk)
        if chore.assigned is True:
            return Response('is already assigned')
        else:
            seri = ChoreSerializer(chore)
            serializer = ChoreSerializer(chore, data=seri.data)

            if serializer.is_valid():
                serializer.save(assigned_to=self.request.user, assigned=True)
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RemoveAllAssignments(APIView):
    def put(self, request, format=None):
        queryset = Chore.objects.all()
        seri = ChoreSerializer(queryset, many=True)
        serializer = ChoreSerializer(queryset, many=True, data=seri.data)
        if serializer.is_valid():
            serializer.save(assigned_to=None, assigned=False)
        return Response(serializer.data)

class DeleteAllChores(APIView):

    def delete(self, request, format=None):
        Chore.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

