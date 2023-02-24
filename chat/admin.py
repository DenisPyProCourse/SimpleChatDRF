from django.contrib import admin
from .models import Thread, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


class ThreadsInline(admin.TabularInline):
    model = Thread.participants.through
    max_num = 2
    extra = 0


class ThreadAdmin(admin.ModelAdmin):
    inlines = [
        ThreadsInline, MessageInline,
    ]

    def get_message(self, obj):
        """
        Providing of Message ids to admin panel.
        """
        thread = Thread.objects.get(id=obj.id)
        messg_lst = [messg.id for messg in thread.messages.all()]
        if messg_lst:
            return messg_lst
        else:
            return 'No messages'

    def get_participant_names(self, obj):
        return ", ".join([participant.username for participant in obj.participants.all()])

    get_participant_names.short_description = 'Participants'
    get_message.short_description = 'messages id'
    fields = ('id', 'created', 'get_message')
    readonly_fields = ('id', 'created', 'get_message')
    exclude = ('participants',)
    list_display = ('id', 'get_participant_names', 'get_message', 'created')
    list_filter = ('created',)
    search_fields = ('participants__username',)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'text', 'thread', 'created', 'is_read')
    list_filter = ('thread', 'is_read')
    search_fields = ('sender__username', 'sender__email', 'text')


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)
