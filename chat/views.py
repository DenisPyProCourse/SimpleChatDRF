from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from rest_framework import generics, mixins, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from chat.models import Thread, Message
from chat.serializers import ThreadSerializer, UserSerializer, MessageSerializer, DetailUserSerializer, \
    UserRegistrSerializer


class ThreadAPIList(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
       ViewSet for Threads. I've deleted Update mixin due to task logic because it's nothing to amend in Threads.
       List: get_queryset() is returning the queryset of Threads for logged in user in which user takes part.
       Create: create() will redirect us to the existed Thread or will create a new one and also redirect us to it.
       Retrieve/Delete: Thread details page allows us to delete this Thread.
       If User isn't a participant - he can't see a details.
    """

    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self, *args, **kwargs):
        """
        I show only threads in which request.user is participated.
        """
        return Thread.objects.filter(participants=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        If Thread exists - redirect to it
        """
        response = super(ThreadAPIList, self).create(request, *args, **kwargs)
        thread = response.data['id']
        return HttpResponseRedirect(redirect_to=f'{thread}/')


class MessageApiList(generics.ListCreateAPIView):
    """
    We got the list of messages for definite Thread and also can create the message there.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        I've used Thread pk from POST to got the queryset of messages from this Thread.
        """
        pk = self.request.parser_context.get('kwargs')['pk_thread']
        return Message.objects.filter(thread_id=pk)


class DetailMessageApi(generics.RetrieveUpdateAPIView):
    """
    If reciever will open this page message.is_read will get True.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        """
        Implementation of changing is_read from False to True if reciever open it.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance.sender != request.user:
            instance.is_read = True
            instance.save()
        return Response(serializer.data)


class UserAPIDetail(generics.RetrieveAPIView):
    """
    Show User details and unread messages for this User.
    Is request.user != details user - request.user can't read the details.
    """
    queryset = User.objects.all()
    serializer_class = DetailUserSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        """
        If request.user != instance.user he can't see the user details
        """
        instance = self.get_object()
        if instance != request.user:
            return Response('Not allow for you')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserAPIList(generics.ListAPIView):
    """
    List of Users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class RegistrUserView(CreateAPIView):
    """
    Base registration view
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)
