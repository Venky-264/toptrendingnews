from django.shortcuts import render,redirect
from Home.models import Register
import random
from django.contrib import messages
import requests
import json



from django.core.mail import EmailMessage

# Create your views here.
def Homepage(request):
    return render(request,'Home/index.html')

def Login(request):
    return render(request,'Home/login.html')

def register(request):
    if request.method == 'POST':
        usermail=request.POST['mail']
        userpassword=request.POST['password']
        userinterest=request.POST['interest']
        id=Register.objects.all().count()+1
        flag=Register.objects.filter(email=usermail).count()
        if(flag!=1):
            tomail=[]
            tomail.append(usermail)
            otp=str(random.randint(1000,9999))
            email = EmailMessage('Otp for the Toptrends','otp for the toptrends news website is '+otp,'venkymeragana@gmail.com',tomail)
            email.send()
            request.session['email'] = usermail
            request.session['password'] = userpassword
            request.session['interest'] = userinterest
            request.session['gen_otp'] = otp
            return redirect('verification/')
        else:
            messages.error(request, 'User already exists')
            return redirect('/')

def verification(request):
    return render(request,'Home/authenticate.html')

def validate(request):
    if request.method == 'POST':
        user_otp=request.POST['otp']
        gen_otp=request.session.get('gen_otp')
        if user_otp==gen_otp:
            email = request.session.get('email')
            password = request.session.get('password')
            interest = request.session.get('interest')
            id=Register.objects.all().count()+1
            Register(id,email,password,interest).save()
            del request.session['email']
            del request.session['password']
            del request.session['interest']
            del request.session['gen_otp']
            url='/news/interest={}'.format(interest)
            return redirect(url)
        else:
            messages.error(request, 'Invalid otp')
            return redirect('/register/verification/')

def News(request,interest):
    url="https://newsapi.org/v2/everything"
    parameters={'q':interest,'sortBy':'publishedAt','apiKey':'66ef098b7ea94f7b93abbb860ac554c0'}
    res=requests.get(url,params=parameters)
    textdata=res.text
    data=json.loads(textdata)
    status=data['status']
    totalresults=data['totalResults']
    articles=data['articles']
    return render(request,'Home/user_news.html',{'status':status,'totalarticles':totalresults,'articles':articles})

def interests(request):
    return render(request,'Home/search.html')

def yourinterests(request):
    if(request.method=='POST'):
        interest=request.POST['topic']
        url="https://newsapi.org/v2/everything"
        parameters={'q':interest,'sortBy':'publishedAt','apiKey':'66ef098b7ea94f7b93abbb860ac554c0'}
        res=requests.get(url,params=parameters)
        textdata=res.text
        data=json.loads(textdata)
        status=data['status']
        totalresults=data['totalResults']
        articles=data['articles']
        return render(request,'Home/yourinterest.html',{'status':status,'totalarticles':totalresults,'articles':articles})

def validateuser(request):
    if request.method=='POST':
        usermail=request.POST['mail']
        userpassword=request.POST['password']
        flag=Register.objects.filter(email=usermail,password=userpassword).count()
        if(flag==1):
            row=Register.objects.filter(email=usermail,password=userpassword)
            for i in row:
                userinterest=i.interest
            url='/news/interest={}'.format(userinterest)
            return redirect(url)
        else:
            messages.error(request, 'invalid username or password')
            return redirect('/login')

