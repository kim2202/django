from django.shortcuts import redirect, render
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.


def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect("board:detail", bpk)

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect("board:detail", bpk)

def index(request):
    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw", "")
    pg = request.GET.get("page", 1)
    
    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__contains=kw)
        elif cate == "wri":
            from acc.models import User
            try:
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()
        else:
            b = Board.objects.filter(content__contains=kw)
    else:
        b = Board.objects.all()
    pag = Paginator(b, 5)
    obj = pag.get_page(pg)

    context = {
        "blist" : obj,
        "cate":cate,
        "kw":kw
    }
    return render(request, "board/index.html", context)


def dreply(request, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if request.user == r.replyer:
        r.delete()
    else: # 19일 에러메세지
        pass 
    return redirect("board:detail", bpk)

def creply(request, bpk):
    b = Board.objects.get(id=bpk)
    c = request.POST.get("com")
    Reply(b=b, replyer=request.user, comment=c, pubdate=timezone.now()).save()
    return redirect("board:detail", bpk)


def update(request, bpk):
    b = Board.objects.get(id=bpk)
    if request.user != b.writer:
        # 19일차 메세지 작성할 곳!!
        return redirect("board:index")
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        b.subject = s
        b.content = c
        b.save()
        return redirect("board:detail", bpk)
    context = {
        "b": b
    }
    return render(request, "board/update.html", context)

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        b = Board(subject=s, writer=request.user, content=c, pubdate=timezone.now())
        b.save()
        return redirect("board:detail", b.id)
    return render(request, "board/create.html")

def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if request.user == b.writer:
        b.delete()
    else:
        pass # 19 일차 메세지 수업시에 해줄곳!!
    return redirect("board:index")


def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "b" : b,
        "rlist" : r
    }
    return render(request, "board/detail.html", context)

