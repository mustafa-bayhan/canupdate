from unicodedata import name
from django.shortcuts import render
from .models import *
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.views.generic.edit import UpdateView
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.decorators import login_required
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation
import requests
# Create your views here.

# Create your views here.
def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        print('aaaaaaaaaaaaaaaaaaaaaa')
        print(translation.activate(language))
        response = HttpResponseRedirect("/")
    return response


def recaptcha_check(recaptcha_response): #2
    verify_url = 'https://www.google.com/recaptcha/api/siteverify' #3
    value = { #4
        'secret': '6Ldp3UUlAAAAAM5SqtI9w0eOBnTikXyNNQAoFUtM',
        'response': recaptcha_response
    }
    response = requests.post(verify_url, value) #5
    result = response.json() #6
    if result['success'] is True: #7
        return True
    else: #8
        return {'status': result['success'], 'reason': result['error-codes']} #


def home(request):
    if request.LANGUAGE_CODE == 'en-us':
        return redirect('/en')
    
    context=dict()
    context['postsh']=Post.objects.filter(Q(completed__iexact='completed')).order_by('-read','-id').distinct()[0:4]
    context['portfolioh']=Portfolio.objects.all().order_by('-publishing_date','-id').distinct()[0:6]
    context['posts']=Post.objects.filter(Q(completed__iexact='completed')).order_by('-read','-id').distinct()[0:3]
    context['portfolio']=Portfolio.objects.all().order_by('-publishing_date','-id').distinct()[0:3]
    resume=Resume.objects.all().order_by('-publishing_date','-id').distinct()
    if len(resume)!=0:
        context['resume']=resume[0]
        
    if request.method=="POST":
        recaptcha_response = request.POST.get('g-recaptcha-response') #8
        recaptcha_response_result = recaptcha_check(recaptcha_response) #9
        
        username=request.POST.get('name')
        mail=request.POST.get('email')
        number=request.POST.get('phone')
        comment=request.POST.get('message')
        if recaptcha_response_result is True:
            make_comment = Connection.objects.create(name=username,mail=mail, telefon=number, content=comment)
            make_comment.save()
            return redirect(request.META['HTTP_REFERER'])
        
        else:
           
            context['name1']=username
            context['comment1']=comment
            context['mail1']=mail
            context['number1']=number
            context['error'] = 'Robot olmadığınızı doğrulayınız!'
            return render(request,'index.html',context)
    
    return render(request,'index.html',context)

def contact(request):
    if request.LANGUAGE_CODE == 'en-us':
        return redirect('/en/contact')
    
    context9=dict()
    context9['postsh']=Post.objects.filter(Q(completed__iexact='completed')).order_by('-read','-id').distinct()[0:4]
    context9['portfolioh']=Portfolio.objects.all().order_by('-publishing_date','-id').distinct()[0:6]
    
    if request.method=="POST":
        recaptcha_response = request.POST.get('g-recaptcha-response') #8
        recaptcha_response_result = recaptcha_check(recaptcha_response) #9
        
        username=request.POST.get('name')
        mail=request.POST.get('email')
        number=request.POST.get('phone')
        comment=request.POST.get('message')
        if recaptcha_response_result is True:
            make_comment = Connection.objects.create(name=username,mail=mail, telefon=number, content=comment)
            make_comment.save()
            return redirect(request.META['HTTP_REFERER'])
        
        else:
           
            context9['name1']=username
            context9['comment1']=comment
            context9['mail1']=mail
            context9['number1']=number
            context9['error'] = 'Robot olmadığınızı doğrulayınız!'
            return render(request,'contact.html',context9)
    
        
        
    return render(request,'contact.html',context9)

def about(request):
    if request.LANGUAGE_CODE == 'en-us':
        return redirect('/en/about')
    
    context1=dict()
    context1['postsh']=Post.objects.filter(Q(completed__iexact='completed')).order_by('-read','-id').distinct()[0:4]
    context1['portfolioh']=Portfolio.objects.all().order_by('-publishing_date','-id').distinct()[0:6]
    
    resume=Resume.objects.all().order_by('-publishing_date','-id').distinct()
    if len(resume)!=0:
        context1['resume']=resume[0]
    
    
    return render(request,'about.html',context1)


def blog(request):
    if request.LANGUAGE_CODE == 'en-us':
        return redirect('/en/articles')
    context2=dict()
    posts=Post.objects.filter(Q(completed__iexact='completed')).distinct()
    query=request.GET.get('q')
    search=request.GET.get('search')
    context2['postsh']=Post.objects.filter(Q(completed__iexact='completed')).order_by('-read','-id').distinct()[0:4]
    context2['portfolioh']=Portfolio.objects.all().order_by('-publishing_date','-id').distinct()[0:6]
    
    if query:
        posts= posts.filter(
             Q(category__name__exact=query)
        ).distinct()
        context2['temizle'] = ('temizle')
        
    if search:
        posts= posts.filter(
            Q(title__icontains=search)|Q(category__name__icontains=search)|Q(body__icontains=search)
        ).distinct()  
        context2['temizle'] = ('temizle') 
  
    paginator = Paginator(posts, 6) 
    context2['filter_count']=paginator.count
    page_num = request.GET.get('page')
    page=paginator.get_page(page_num)
    
    context2['count']=paginator.count
    context2['page'] = page  
    page_number=page.number

    if page_number !=None:
        fark=int(paginator.num_pages) - int(page_number)
       
        if fark >= 2:
            context2['last'] = ('last')
            if fark > 2:
                context2['last_three'] = ('last_three')
                
            
        if int(page_number) >= 3:
            context2['first'] = ('first')
            
            if int(page_number) > 3:
                context2['three_dot'] = ('three_dot')
            
    else:

        
        if paginator.num_pages-1 >= 2:
            context2['last_true'] = ('last')
            if paginator.num_pages-1 >2:
                
                context2['last_three'] = ('last_three')


    context2['posts'] = posts
    context2['categories']=Category.objects.all()
    context2['tags'] = Category.objects.all()
    context2['recent'] = Category.objects.all()
    context2['recent']=Post.objects.all().filter(Q(completed__iexact='completed')).order_by('-read').distinct()[:5]
    return render(request,'articles.html',context2)


def blog_single(request, slug):
    
    context3={}
    context3['postsh']=Post.objects.filter(Q(completed__iexact='completed')).order_by('-read','-id').distinct()[0:4]
    context3['portfolioh']=Portfolio.objects.all().order_by('-publishing_date','-id').distinct()[0:6]
    post11=get_object_or_404(Post, slug=slug)
    if request.LANGUAGE_CODE == 'en-us':
        return redirect('/en/{}'.format(post11.get_absolute_url()))
    
    query2=request.POST.get('parent_id')

    
   
    read = post11.read
    read += 1
    degıs = Post.objects.filter(slug=slug).update(read=read)
    context3['post11'] = post11
    context3['recent']=Post.objects.all().filter(Q(completed__iexact='completed')).order_by('-read').distinct()[:5]
    context3['tags'] = Category.objects.all()
    context3['parent'] = Comment.objects.filter(Q(parent_comment__id__iexact=None),Q(post__id__iexact=post11.id)).order_by('-created_date','-id').distinct()
    context3['inner'] = Comment.objects.filter(~Q(parent_comment__id__iexact=None))
    if request.method=="POST" and query2 == None:
        recaptcha_response = request.POST.get('g-recaptcha-response') #8
        recaptcha_response_result = recaptcha_check(recaptcha_response) #9
        username=request.POST.get('name')
        comment=request.POST.get('message')
        if recaptcha_response_result is True:
            
            
            newcomment = Comment.objects.create(name=username,content=comment, post=post11)
            newcomment.save()
            return HttpResponseRedirect(post11.get_absolute_url())
        
        else:
           
            context3['name1']=username
            context3['message1']=comment
            context3['error'] = 'Robot olmadığınızı doğrulayınız!'
            return render(request,'article-single.html',context3)
    
    
    if query2:
        recaptcha_response = request.POST.get('g-recaptcha-response') #8
        recaptcha_response_result = recaptcha_check(recaptcha_response) #9
        
        username=request.POST.get('name_reply')
        comment=request.POST.get('message_reply')
        if recaptcha_response_result is True:
            the_parent = Comment.objects.get(pk=int(query2))
            newcomment = Comment.objects.create(parent_comment = the_parent, name=username,content=comment, post=post11)
            newcomment.save()
            return HttpResponseRedirect(post11.get_absolute_url())
        
        else:
            context3['name2']=username
            context3['message2']=comment
            context3['error2'] = 'Robot olmadığınızı doğrulayınız!'
            return render(request,'article-single.html',context3)
            
        
        
    return render(request, 'article-single.html', context3)





def portfolio(request):
    if request.LANGUAGE_CODE == 'en-us':
        return redirect('/en/projects')
    context4=dict()
    context4['postsh']=Post.objects.filter(Q(completed__iexact='completed')).order_by('-read','-id').distinct()[0:4]
    context4['portfolioh']=Portfolio.objects.all().order_by('-publishing_date','-id').distinct()[0:6]
    portfolio=Portfolio.objects.all().order_by('-publishing_date','-id')
    paginator = Paginator(portfolio, 30) # bir sayfada kaç tane görünmesi gerek
    context4['filter_count']=paginator.count
    page_num = request.GET.get('page')
    page=paginator.get_page(page_num)
    
    context4['count']=paginator.count
    context4['page'] = page  
    page_number=page.number
    
    context4['portfolio']=Portfolio.objects.all().order_by('-publishing_date','-id').distinct()

    if page_number !=None:
        fark=int(paginator.num_pages) - int(page_number)
        if fark >= 2:
            context4['last'] = ('last')
            if fark > 2:
                context4['last_three'] = ('last_three')
                
            
        if int(page_number) >= 3:
            context4['first'] = ('first')
            
            if int(page_number) > 3:
                context4['three_dot'] = ('three_dot')
            
    else:

        
        if paginator.num_pages-1 >= 2:
            context4['last_true'] = ('last')
            if paginator.num_pages-1 >2:
                
                context4['last_three'] = ('last_three')
                
    return render(request,'projects.html', context4)


















