from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers

from chat.models import Thread, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User list.
    """
    class Meta:
        model = User
        fields = ['id', 'username']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message list/create.
    """
    class Meta:
        model = Message
        fields = ['id', 'thread', 'sender', 'is_read', 'text', 'created']
        read_only_fields = ['id', 'thread', 'sender', 'is_read', 'created']


    def create(self, validated_data):
        """
        Check that sender is request.user and that user is a participant of Thread.
        Take pk of thread from POST request.
        Return a validated data for create()
        """
        validated_data['sender'] = self.context['request'].user
        thread = Thread.objects.get(id=self.context['request'].parser_context.get('kwargs')['pk_thread'])
        if validated_data['sender'] not in thread.participants.all():
            raise serializers.ValidationError("You're not the member of this thread")
        validated_data['thread'] = thread
        return super().create(validated_data)

class DetailUserSerializer(serializers.ModelSerializer):
    """
    Serializer for showing unread messages of each user.
    """
    unread_messages = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = User
        fields = ['id', 'username', 'unread_messages']

    def get_unread_messages(self, obj):
        """
        I've used here User model from self.instance object. And then I get a queryset of objects where user is a
        participant of related to these messages Thread + user is not a sender + messages are not read yet.
        Then I sent 'messages' to Serializer and order it in reverse order.
        """
        user = self.instance
        messages = Message.objects.filter(Q(thread__participants=user) & ~Q(sender_id=user) & Q(is_read=False))
        return MessageSerializer(instance=messages.order_by('-created'), many=True).data

    def to_representation(self, instance):
        """
        Representation view of messages fields
        """
        data = super().to_representation(instance)
        messages_representation = data['unread_messages']
        data['unread_messages'] = messages_representation

        return data


class ThreadSerializer(serializers.ModelSerializer):
    """
    Serializer for Thread List/Create/Delete
    """
    messages = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Thread
        fields = ['id', 'participants', 'updated', 'created', 'messages']
        read_only_fields = ['id', 'updated', 'created']

    def validate_participants(self, attrs):
        """
        Validation for the quantity of participants and presence of request.user in new Thread.
        """
        if len(attrs) != 2:
            raise serializers.ValidationError("A thread can only have two participants.")
        if self.context['request'].user not in attrs:
            raise serializers.ValidationError("You should choose yourself to create a thread")
        return attrs

    def get_messages(self, obj):
        """
        I've got here the last message to display it in Thread List/Detail.
        """
        return MessageSerializer(instance=obj.messages.order_by('-created').first()).data

    def to_representation(self, instance):
        """
        If last message for Thread exists I show it.
        """
        data = super().to_representation(instance)
        messages_representation = data.pop('messages')
        if messages_representation.get('thread'):
            data['messages'] = messages_representation
        return data

    def create(self, validated_data):
        """
        I've checked here if the Thread with provided 2 participants exists. If yes you'll be redirected to this Thread.
        If no the Thread will be created.
        """
        participant = validated_data.pop('participants')
        participants = [User.objects.get(id=member.id).id for member in participant]
        thread = Thread.objects.filter(participants=participants[0]).filter(participants=participants[1])
        if thread.exists():
            return thread.first()
        else:
            thread = Thread.objects.create()
            thread.participants.set(participants)
            return thread


class UserRegistrSerializer(serializers.ModelSerializer):
    """
    Serializer for User registration view.
    """
    password2 = serializers.CharField()
    email = serializers.CharField(required=True, max_length=50)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({password: "Password doesn't match"})
        user.set_password(password)
        user.save()
        return user
