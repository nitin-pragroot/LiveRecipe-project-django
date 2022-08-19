from django.utils import timezone

#import CHOICES as CHOICES
from django.db import models
from django.contrib.auth.models import User


CHOICES1 = (
    ('Chinese','Chinese'),
    ('Afghani','Afghani'),
    ('Indian','Indian'),
    ('Dubai','Dubai'),

)
# Create your models here.
class Category(models.Model):
    cat_name=models.CharField(max_length=50)
    cat_img=models.ImageField(upload_to="cat_images/",default="",blank="True",null="True")
    def __str__(self):
        return self.cat_name


class Recipe(models.Model):
    rec_title=models.CharField(max_length=200)
    rec_details=models.TextField()
    rec_img1=models.ImageField(upload_to="images/",default="",null="True",blank="True")
    rec_img2=models.ImageField(upload_to="images/",default="",null="True",blank="True")
    rec_img3=models.ImageField(upload_to="images/",default="",null="True",blank="True")
    rec_img4=models.ImageField(upload_to="images/",default="",null="True",blank="True")
    rec_preptime = models.CharField(max_length=100)
    rec_cooktime = models.CharField(max_length=100)
    rec_ingredients = models.CharField(max_length=500,null="True",blank="True")
    rec_directions = models.CharField(max_length=1000,null="True",blank="True")
    rec_nutfacts = models.CharField(max_length=500,null="True",blank="True")
    rec_servings = models.IntegerField()
    rec_type = models.CharField()
    rec_type=models.CharField(choices=CHOICES1,max_length=50)
    rec_posteddate = models.DateTimeField(default=timezone.now)
    rec_catid=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)


    def __str__(self):
        return self.rec_title



class Reviews(models.Model):
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=100,blank=True, null=True)
    rating = models.IntegerField(blank=True,null=True)
    posteddate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.review

class UserDetail(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    user_info = models.CharField(max_length=500, null=True, blank=True)
    user_fname = models.CharField(max_length=100, null=True, blank=True)
    user_lname = models.CharField(max_length=100, null=True, blank=True)
    user_image = models.ImageField(upload_to='images/', null=True, blank=True,default="images/profile.jfif")
    user_city = models.CharField(max_length=100, null=True, blank=True)
    user_phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.user)


