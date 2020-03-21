from django.shortcuts import render


def view(request, ch_id):
    return render(request, 'chat.html', dict(
        room_name=ch_id,
    ))
