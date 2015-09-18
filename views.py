from django.http import Http404
from django.contrib.auth.models import User
from django.db.models.query_utils import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import mixins
from rest_framework import generics

from api.models import Chore
from api.serializers import ChoreSerializer
from api.permissions import IsOwnerOrReadOnly
from rest_auth.permissions import IsAccountActivated

import datetime


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
            serializer.save(owner=self.request.user)
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

class CategorizedChoreList(APIView):
    """
    return a dictionary of four lists: all assigned chores, all
    unassigned chores, all expired chores, and all completed
    chores (in that order).
    """

    def get(self, request, format=None):

        #first we gather all chores with appropriate boolean values
        #into separate lists using Queries
        assigned_chores = ChoreSerializer(Chore.objects.filter(Q(assigned=True)), many=True).data
        unassigned_chores = ChoreSerializer(Chore.objects.filter(Q(assigned=False)), many=True).data
        expired_chores = ChoreSerializer(Chore.objects.filter(Q(expired=True)), many=True).data
        completed_chores = ChoreSerializer(Chore.objects.filter(Q(completed=True)), many=True).data

        #now initialize the dictionary with the above lists
        categorized_chores = {'Assigned Chores': assigned_chores,
                               'Unassigned Chores': unassigned_chores,
                               'Expired Chores': expired_chores,
                               'Completed Chores': completed_chores}

        return Response(categorized_chores)

class AssignChore(APIView):
    """
    Assign a Chore
    """

    permission_classes = (permissions.IsAuthenticated, IsAccountActivated)

    def get_object(self, pk):
        try:
            return Chore.objects.get(pk=pk)
        except Chore.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        chore = self.get_object(pk)
        if chore.assigned is True:
            return Response('"'+chore.name+'"'+' is already assigned', status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            seri = ChoreSerializer(chore)
            serializer = ChoreSerializer(chore, data=seri.data)

            if serializer.is_valid():
                serializer.save(assigned_to=self.request.user, assigned=True)
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteChore(APIView):
    """
	Complete a chore
	"""

    permission_classes = (permissions.IsAuthenticated, IsAccountActivated)

    def get_object(self, pk):
        try:
            return Chore.objects.get(pk=pk)
        except Chore.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        chore = self.get_object(pk)
        if chore.assigned is True and chore.completed is True:
            return Response('"'+chore.name+'"'+' is already completed', status=status.HTTP_412_PRECONDITION_FAILED)
        elif chore.assigned is False:
            return Response('"'+chore.name+'"'+' is not assigned', status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            seri = ChoreSerializer(chore)
            serializer = ChoreSerializer(chore, data=seri.data)

            if serializer.is_valid():
                serializer.save(completed=True)
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpireChore(APIView):
    """
    Mark a chore as expired
    """

    today_as_weekday = datetime.date.today().weekday()  # returns an integer, 0 for Monday - 6 for Sunday
    Days = {'Monday': 0, 'monday': 0,
        'Tuesday': 1, 'tuesday': 1,
        'Wednesday': 2, 'wednesday': 2,
        'Thursday': 3, 'thursday': 3,
        'Friday': 4, 'friday': 4,
        'Saturday': 5, 'saturday': 5,
        'Sunday': 6, 'sunday': 6}


    def get_object(self, pk):
        try:
            return Chore.objects.get(pk=pk)
        except Chore.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        chore = self.get_object(pk=pk)
        if chore.assigned is False:
            return Response('"'+chore.name+'"'+' is not assigned', status=status.HTTP_412_PRECONDITION_FAILED)
        if chore.expired is True:
            return Response('"'+chore.name+'"'+' is already expired', status=status.HTTP_412_PRECONDITION_FAILED)
        elif chore.assigned is True and self.Days[chore.due_day] >= self.today_as_weekday:
            return Response('The due day for '+'"'+chore.name+'"'+' has not passed', status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            seri = ChoreSerializer(chore)
            serializer = ChoreSerializer(chore, data=seri.data)

            if serializer.is_valid():
                serializer.save(expired=True)
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClaimChore(APIView):
    """
    Claim an expired chore
    """

    permission_classes = (permissions.IsAuthenticated, IsAccountActivated)

    def get_object(self, pk):
        try:
            return Chore.objects.get(pk=pk)
        except Chore.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        chore = self.get_object(pk)
        if chore.assigned is False:
            return Response('"'+chore.name+'"'+' is not assigned', status=status.HTTP_412_PRECONDITION_FAILED)
        elif chore.assigned is True and chore.expired is False:
            return Response('"'+chore.name+'"'+' has not yet expired', status=status.HTTP_412_PRECONDITION_FAILED)
        elif chore.assigned is True and chore.expired is True and chore.claimed is True:
            return Response('"'+chore.name+'"'+' is already claimed', status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            seri = ChoreSerializer(chore)
            serializer = ChoreSerializer(chore, data=seri.data)

            if serializer.is_valid():
                serializer.save(claimed=True, claimed_by=self.request.user)
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
