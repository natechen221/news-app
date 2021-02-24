from django.db import models
import django.utils.timezone as timezone
from django.contrib.auth.models import User

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    username = models.CharField(max_length=50)
    birthdate = models.DateField(null = True)

    # Email = models.EmailField(max_length=254)
    profile_picture = models.ImageField(upload_to='', blank = True, null = True)
    favorite_category = models.ManyToManyField(
        'ArticleCategory',
        blank = True,
        related_name = 'user_Category'
    )

    def __str__(self):
        return str(self.id)

    def course_list(self):
        return ','.join([i.CourseName for i in self.courses.all()])

class Article(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    content = models.TextField("Content")
    date= models.DateField(default = timezone.now)
    category = models.ForeignKey(
        'ArticleCategory',
        null = True,
        blank = True,
        on_delete=models.SET_NULL,
    )
    article_pictures = models.ImageField(upload_to='', blank = True, null = True)
    liked = models.ManyToManyField(User, blank = True)

    def __str__(self):
        return str(self.id)

    def course_list(self):
        return ','.join([i.CourseName for i in self.courses.all()])

    @property
    def num_likes(self):
        return self.liked.count()

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

class ArticleCategory(models.Model):
    name = models.CharField(max_length=50)
    articles = models.ManyToManyField('Article',blank = True)
    
    def size(self):
        return self.articles.all().count()

    def __str__(self):
        return self.name


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(Parent=None)
        return qs

    def filter_by_instance(self,instance):
        content_type =ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id = obj_id).filter(parent = None)
        return qs

#Comments Database
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null = True)
    object_id = models.PositiveIntegerField(null = True)
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    content = models.TextField()
    timestamp = models.DateField(auto_now_add=True, null = True)

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return str(self.user.usename)

    def __str__(self):
        return str(self.user.username)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike','Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    value = models.CharField(choices = LIKE_CHOICES, default = 'Like', max_length = 10)

    def __str__(self):
        return str(self.article)
