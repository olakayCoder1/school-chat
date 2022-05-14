from . import consumers

from django.urls import re_path


websocket_urlpatterns = [
    re_path(r'chat/group/(?P<room_name>\w+)/$', consumers.GroupMessageConsumer.as_asgi()),
    re_path(r'chat/direct/(?P<username>\w+)/$', consumers.DirectMessageConsumer.as_asgi()),
]