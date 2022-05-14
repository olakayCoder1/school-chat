from django.http import JsonResponse
from django.shortcuts import  render , get_object_or_404
from .models import Messages , Threads , CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
# Create your views here.




@login_required
def index(request):
    print(CustomUser)
    groups = Threads.objects.filter(thread_type='group')
    users = CustomUser.objects.all().exclude(id=request.user.id)
    context = { 'users': users, 'groups': groups}
    return render(request, 'chat/general.html', context)





#group chat view
@login_required
def group_chat(request, room_name):
    name = room_name
    group_link = f'/chat/group/about/{room_name}/'
    #retrieve all messages with the current thread name
    try :
        thread= Threads.objects.get(name=name)
        past_messages = Messages.objects.filter(thread_name= thread.id)

    except :
        print('in exception block')
        #create new group with the current thread name if does not exist
        Threads.objects.create(name=name, thread_type='group' , created_by=request.user)
        thread= Threads.objects.get(name=name)
        past_messages = Messages.objects.filter(thread_name= thread.id)

    groups = Threads.objects.filter(thread_type='group')
    users = CustomUser.objects.all().exclude(id=request.user.id)


    context={ 
        'room_name': room_name ,#setting room_name to actual room_name arg
        'username': request.user.username,
        'past_messages' : past_messages,
        'group_link': group_link,
        'groups': groups,
        'users': users
    }
    return render(request, 'chat/group_chat.html', context)



#direct chat view 
@login_required
def direct_chat(request,username):
    user = get_user_model()
    other_user = get_object_or_404(user ,username=username)
    other_user_id = other_user.id
    #get the user to be messaged
    if other_user_id > request.user.id :
        try:
            thread_name = f'chat_{other_user_id}{request.user.id}'
            thread_name_id = Threads.objects.get(name=thread_name).id
        except:
            name = f'chat_{other_user_id}{request.user.id}'
            Threads.objects.create(name=name, thread_type='direct')
            thread_name_id = Threads.objects.get(name=thread_name).id
    else :
        try:
            thread_name = f'chat_{request.user.id}{other_user_id}'
            thread_name_id = Threads.objects.get(name=thread_name).id
        except:
            name = f'chat_{request.user.id}{other_user_id}'
            Threads.objects.create(name=name, thread_type='direct')
            thread_name_id = Threads.objects.get(name=thread_name).id
    
    past_messages = Messages.objects.filter(thread_name=thread_name_id)
    users = CustomUser.objects.all().exclude(id=request.user.id)

    groups = Threads.objects.filter(thread_type='group')

    friend = user.objects.get(username=username)
    context = {'friend': friend.id, 'friend_name': friend.username ,'groups':groups, 'past_messages': past_messages, 'users': users}
    return render(request,'chat/direct_chat.html', context)

@login_required
def group_about(request, room_name):

    thread_name = f'chat_{room_name}_group'
    room_object = Threads.objects.get(name=thread_name)

    context = {
        'room': room_object,
        'name': room_name
    }
    return render(request, 'chat/about-group.html', context)

@login_required
def create_group(request,name):
    res = f'{name} group created'
    data = { 'res': res}
    return JsonResponse(data=data, safe=True)
