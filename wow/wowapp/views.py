from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from wowapp.models import Product,Cart,Orders
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def home(request):
    context={}
    p=Product.objects.filter(is_active=True)
    context['products']=p
    return render(request,'homepage.html',context)


def description(request,pid):
    context={}
    context['products']=Product.objects.filter(id=pid)
    return render(request,'description.html',context)

def about(request):
    return render(request,'about.html')

def base(request):
    return render(request,'base.html')

def cart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    context={}
    context['products']=c
    s=0
    for x in c:
        s=s+x.pid.price*x.qty
    context['total']=s
    return render(request,'cart.html',context)

def addCart(request,pid):
    context={}
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid)
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        q=Cart.objects.filter(q1 & q2)
        n=len(q)
        if n==1:
            return redirect('/cart')
        else:    
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()  
            return redirect('/home',context)
    else:
        return redirect('/login')

def updateqty(request,qty,cid):
        context={}
        c=Cart.objects.filter(id=cid)
        if qty=='1':
           t=c[0].qty+1
           c.update(qty=t)
        
        else:
           if c[0].qty>1:
                t=c[0].qty-1
                c.update(qty=t)
        s=0
        for x in c:
            s=s+x.pid.price*x.qty
        context['amnt']=s
        return redirect('/cart',context)
    
def order(request):
    context={}
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(100000,999999)
    for x in c:
        o=Orders.objects.create(orderId=oid,qty=x.qty,pid=x.pid,uid=x.uid)
        o.save()
        x.delete()
    order=Orders.objects.filter(uid=request.user.id)
    s=0
    for x in order:
            s=s+x.pid.price*x.qty
    context['total']=s
    context['products']=order
    return render(request,'order.html',context)

def remove(request,pid):
    p=Cart.objects.filter(id=pid)
    p.delete()
    return redirect('/cart')

def makepayment(request):
    order=Orders.objects.filter(uid=request.user.id)
    s=0
    for x in order:
            s=s+x.pid.price*x.qty
            oid=x.orderId
    # context['total']=s
    client = razorpay.Client(auth=("rzp_test_XzkkGuSvrCCQWh", "R1vQhHxFwKHPjXO442rh352G"))
    data = { "amount": s*100, "currency": "INR", "receipt": "oid"}
    payment = client.order.create(data=data)
    context ={}
    context['data']= payment
    return render(request,'pay.html',context)

def login_user(request):
    context={}
    if request.method=='POST':
        un=request.POST['uname']
        p=request.POST['pwd']
        if un=='' or p=='':
            context['error']="fileds cannot be empty!!"
            return render(request,'login.html',context)
        else:
            a=authenticate(username=un,password=p)
            if a is not None:
                login(request,a)
                return redirect('/home')
            else:
                context['error']="invalid username or password"
                return render(request,'login.html',context)        
    else:
        return render(request,'login.html')
    
def register(request):
    context={}
    if request.method=='POST':
        un=request.POST['uname']
        p=request.POST['pwd']
        cp=request.POST['cpwd']
        if un=='' or p=='' or cp=='':
            context['error']="fileds cannot be empty!!"
            return render(request,'register.html',context)
        elif p!=cp:
            context['error']="password and confirm password does not match!!"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(username=un,email=un,password=p)
                u.set_password(p)
                u.save()
                context={}
                context['success']="user created successfully!!!"
                return render(request,'register.html',context)
            except Exception:
                context['error']="user already exist!!"
                return render(request,'register.html',context)
    else:    
        return render(request,'register.html')    

def logout_user(request):
    logout(request)
    return redirect('/home')


def sendUserMail(request):
    uemail=request.user.email
    subject = 'welcome to WoW Store'
    message = 'Hi, your order placed successfully.'
    email_from = "mullaibrahim140@gmail.com"
    recipient_list = [uemail]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('/home')