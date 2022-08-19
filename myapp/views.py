from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import login as ulogin,authenticate,logout
from .models import Recipe,Category,Reviews,UserDetail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.



def register(request):
    if request.method == "POST":
        uname = request.POST['username']
        upass = request.POST['password']
        emailid = request.POST['email']
        user = User.objects.create_user(username=uname,password=upass,email=emailid)
        user = UserDetail(user=user)
        user.save()
        return redirect('login')
        registered=True
    else:
        registered=False

    return render(request,'register.html',{'registered':registered})

def login(request):
    if request.method == "POST":
        uname = request.POST['username']
        upass = request.POST['password']
        print(uname,upass)
        user = authenticate(username=uname,password=upass)
        print(user)
        if user is not None:
            ulogin(request,user)
            return redirect('addrecipe')
        else:
            return render(request,'login.html',{'loginerror':'Invalid Username/Password'})
    else:
        return render(request,'login.html')

def profile(request):
    user = User.objects.get(id=request.user.id)
    obj = UserDetail.objects.get(user=request.user.id)
    if request.method == 'POST':
        user_info = request.POST.get('info')
        user_fname = request.POST.get('fname')
        user_lname = request.POST.get('lname')
        user_image = request.FILES.get('image')
        user_city = request.POST.get('city')
        user_phone = request.POST.get('phone')

        obj = UserDetail.objects.get(user=request.user.id)
        obj.user_info = user_info
        obj.user_fname = user_fname
        obj.user_lname = user_lname
        if user_image:
            obj.user_image = user_image
        obj.user_city = user_city
        obj.user_phone = user_phone
        obj.save()
        return render(request, 'profilepage.html',{'user':user,'user1':obj})
    else:

        return render(request,'profilepage.html',{'user':user,'user1':obj})

def changepassword(request):
    if request.method == 'POST':
        id=request.user.id;
        data=User.objects.get(pk=id)
        password = request.POST.get('new_pass')
        confirm_password = request.POST.get('cpass')
        if password != confirm_password:
            print('ggg')
            return render(request, 'changepass.html',{'error':'Password and Confirm password does not match'})
        else:
            print('fff')
            data.set_password(request.POST.get('new_pass'))
            data.save()
            return redirect('login')
    else:
        return render(request, 'changepass.html')


def signout(request):
    logout(request)
    return  redirect('login')

def addrecipe(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title=request.POST.get('title')
        details=request.POST.get('details')
        preptime=request.POST.get('preptime')
        cooktime=request.POST.get('cooktime')
        ingredient=request.POST.get('ingredients')
        nutfacts=request.POST.get('nutfacts')
        directions=request.POST.get('directions')
        servings=request.POST.get('servings')
        type=request.POST.get('type')
        catid=request.POST.get('category')
        image1=request.FILES['image1']
        image2=request.FILES['image2']
        image3=request.FILES['image3']
        image4=request.FILES['image4']
        obj=Recipe(rec_title=title,rec_details=details,rec_type=type,rec_preptime=preptime,rec_cooktime=cooktime,rec_ingredients=ingredient,rec_nutfacts=nutfacts,rec_directions=directions,rec_servings=servings,rec_img1=image1,rec_img2=image2,rec_img3=image3,rec_img4=image4,rec_catid=Category.objects.get(pk=catid),user_id=User.objects.get(pk=request.user.id))
        obj.save()
        return render(request,"postrecipe.html",{'categories':categories})
    else:
        return render(request,"postrecipe.html",{'categories':categories})


def index(request):
    recipes=Recipe.objects.all().order_by('-id')
    p = Paginator(recipes, 9)  # creating a paginator object
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    return render(request,'home.html',{'recipes':page_obj})
"""
def index(request):
    recipes=Recipe.objects.all().order_by('-id')
    return render(request,'home.html',{'recipes':recipes})
"""
def recipebycat(request,id):
    recipes=Recipe.objects.filter(rec_catid=id)
    count=recipes.count()
    if count>0:
        return render(request,'recipebycat.html',{'recipes':recipes})
    else:
        return render(request, 'recipebycat.html', {'recipes': recipes,'norecords':'No Recipes in this category '})

def detail(request,id):
    recipe=Recipe.objects.get(pk=id)
    ingredients=recipe.rec_ingredients
    inglist=ingredients.split(",")
    directions=recipe.rec_directions
    dirlist=directions.split("Step")
    nutfacts = recipe.rec_nutfacts
    nutlist = nutfacts.split(":")

    #relatedrecipes
    catid=recipe.rec_catid #show recipe cat id fetch
    relatedrecipes=Recipe.objects.filter(rec_catid=catid)

    #fetchreviews
    reviews=Reviews.objects.filter(recipe_id=id)
    allreviews = []
    for i in reviews:
        reviewsdata={}
        print(i.user_id,'ggg')
        uobj = UserDetail.objects.get(user=i.user_id)
        #print(uobj.user_image)
        reviewsdata['user_id']=i.user_id
        reviewsdata['posteddate']=i.posteddate
        reviewsdata['review']=i.review
        reviewsdata['rating']=i.rating
        reviewsdata['image']=uobj.user_image
        allreviews.append(reviewsdata)



    categories=Category.objects.all()
    return render(request,'recipedetail.html',{'recipe':recipe,'reviews':allreviews,'relatedrecipes':relatedrecipes,'inglist':inglist,'dirlist':dirlist,'nutlist':nutlist,'categories':categories})

def postreview(request,id):
    recipe = Recipe.objects.get(pk=id)
    if request.method == 'POST':
        review=request.POST.get('review')
        rate=request.POST.get('rating')
        obj=Reviews(review=review,rating=rate,user_id=User.objects.get(pk=request.user.id),recipe_id=Recipe.objects.get(pk=id))
        obj.save()
        return redirect("detail",id)
    else:
        return render(request,"recipedetail.html",{'recipe':recipe})


def editrecipe(request,id):
    if request.method == 'POST':
        title = request.POST.get('title')
        details = request.POST.get('details')
        preptime = request.POST.get('preptime')
        cooktime = request.POST.get('cooktime')
        ingredient = request.POST.get('ingredients')
        nutfacts = request.POST.get('nutfacts')
        directions = request.POST.get('directions')
        servings = request.POST.get('servings')
        type = request.POST.get('type')
        catid = request.POST.get('category')
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')
        obj = Recipe.objects.get(pk=id)
        obj.rec_title = title
        obj.rec_details = details
        obj.rec_preptime = preptime
        obj.rec_cooktime = cooktime
        obj.rec_ingredient = ingredient
        obj.rec_nutfacts = nutfacts
        obj.rec_directions = directions
        obj.rec_servings = servings
        obj.rec_type = type
        obj.rec_img1 = request.FILES.get('image1')
        obj.rec_img2 = request.FILES.get('image2')
        obj.rec_img3 = request.FILES.get('image3')
        obj.rec_img4 = request.FILES.get('image4')
        obj.category = Category.objects.get(pk=catid)
        obj.save()
       # return render(request, 'editrecipe.html', {'recipe': recipe, 'categories': categories})
        return  redirect('myrecipes')
    else:
        categories=Category.objects.all()
        recipe=Recipe.objects.get(pk=id)
        return render(request, 'editrecipe.html',{'recipe':recipe,'categories':categories})

def delrecipe(request,id):
    recipe=Recipe.objects.get(pk=id)
    recipe.delete()
    return redirect('myrecipes')
def myrecipes(request):
    userid=request.user.id
    recipes=Recipe.objects.filter(user_id=userid)
    return render(request,'myrecipes.html',{'recipes':recipes})

def news(request):
    from newsapi import NewsApiClient

    newsapi = NewsApiClient(api_key='6381055e63cf4bac97aead362e4e8ba3')
    top_headlines = newsapi.get_top_headlines(language='en',country='in')
    articles=top_headlines['articles']
    desc=[]
    title=[]
    article_img=[]
    url=[]
    for i in range(len(articles)):
        title.append(articles[i]['title'])
        desc.append(articles[i]['description'])
        article_img.append(articles[i]['urlToImage'])
        url.append(articles[i]['url'])
    news=zip(title,desc,article_img,url)

    return render(request,'news.html',{'news',news})


def search_recipes(request):
    if request.method == 'POST':
        search_txt=request.POST.get('search')
        if search_txt == "":
            return render(request, 'search.html',{'recipes': {}})
        elif search_txt:
            recipes = Recipe.objects.filter(rec_title__icontains=search_txt)
            return render(request, 'search.html', {'recipes':recipes})
    else:
        return render(request,'search.html',{'recipes':{}})