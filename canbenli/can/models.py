from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField

CHOICES2 = (
    ('completed', 'completed'),
    ('draft', 'draft'),
)
class Connection(models.Model):
    
    name = models.CharField(max_length=100, verbose_name='Ad Soyad',null= True, blank=False)
    content = models.TextField(max_length=500, verbose_name='Yorum',null= True, blank=False)
    created_date = models.DateTimeField(auto_now_add=True,null= True)
    mail=models.EmailField(max_length=100, null= True, blank=False)
    telefon = models.CharField(max_length=12, verbose_name='telefon',null= True, blank=False)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name=models.CharField(null= True,blank=False, max_length=200)
    slug = models.SlugField(max_length=200, default="", null= True, blank=False)

    def __str__(self):
        return self.name


class Post (models.Model):
    title=models.CharField(null= True, max_length=200)
    image = models.ImageField(null=True, upload_to='image/')
    publishing_date =models.DateTimeField(verbose_name='Yayınlanma Tarihi', auto_now_add=True, null= True )
    read = models.IntegerField(default = 0)
    category= models.ForeignKey(Category, null= True, blank=False, on_delete=models.CASCADE)
    completed=models.CharField(choices=CHOICES2,default='completed',max_length=200)
    author=models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, null= True, blank=False,
    )
    body=RichTextField(null= True)
    read_time=models.CharField(null= True, max_length=200)
    slug = models.SlugField(editable=False, unique=True, null= True, blank=False)
    
    def get_unique_slug(self):
        if not self.pk:
            slug = slugify(self.title.replace('ı', 'i'))
            unique_slug = slug
        
            counter = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(slug, counter)
                counter += 1
        
        else:
            unique_slug=self.slug
        return unique_slug
    
    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Post, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_single', kwargs={"slug":self.slug})

    class Meta:
        ordering  = ['-publishing_date', 'id']


class Portfolio (models.Model):
    
    image = models.ImageField(null=True, upload_to='image/')
    name = models.CharField(null= True,blank=False, max_length=300)
    adres= models.CharField(null= True,blank=False, max_length=300)
    publishing_date =models.DateTimeField(verbose_name='Yayınlanma Tarihi', auto_now_add=True, null= True )
    date=models.CharField(null= True,blank=False, max_length=300)
    category=models.CharField(null= True, max_length=200, default="website")
    def __str__(self):
        return self.adres

class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='comments',null= True)
    name = models.CharField(max_length=100, verbose_name='Ad Soyad',null= True)
    content = models.TextField(max_length=500, verbose_name='Yorum',null= True)
    created_date = models.DateTimeField(auto_now_add=True,null= True)
    parent_comment=models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete= models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        ordering  = ['-created_date', 'id']

class Image_for_detail(models.Model):
    image = models.ImageField(null=True, upload_to='image/')
    def __str__(self):
        return self.image.url
    
   
    
class Resume (models.Model):
    
    sayfa_resmi = models.ImageField(null=True, upload_to='image/')
    body=RichTextField(null= True, default = 'portfolio')
    cv_resmi = models.ImageField(null=True, upload_to='image/')
    cv = models.FileField(upload_to ='files/')
    publishing_date =models.DateTimeField(verbose_name='Yayınlanma Tarihi', auto_now_add=True, null= True )
    def __str__(self):
        return 'cv'
