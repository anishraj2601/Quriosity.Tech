from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
# hello errors 


class topic(models.Model):
  title=models.CharField(unique=True,max_length=100,null=False,blank=False)
  short_title=models.CharField(unique=True,max_length=50,null=True,blank=True)
  priority = models.IntegerField(unique=True,null=False,blank=False)
  slug=models.CharField(unique=True,max_length=200,null=True,blank=True)
  img= models.URLField(max_length=200,null=True,blank=True)
  icon=models.CharField(max_length=50,null=True,blank=True)
  problems_count = models.IntegerField(default=0,blank=False)
  STATUS = (
    (True, 'Yes'),
    (False, 'No')
  )
  active = models.BooleanField(choices=STATUS,default=False, blank=False)
  # last_modified_data = models.DateField(auto_now=True)
  # last_modified_time = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)
  last_updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    # template = 'ID - {0.id} ---> {0.title}({0.problems_count}) ---> ACTIVE - {0.active}'
    template = '{0.title}'
    return template.format(self)


class problem(models.Model):
  topic = models.ManyToManyField(topic, verbose_name=_("all topics"))
  title=models.CharField(unique=True,max_length=100,null=False,blank=False)
  short_title=models.CharField(unique=True,max_length=50,null=True,blank=True)
  TAG_STATUS = (
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Hard', 'Hard')
  )
  tag=models.CharField(choices=TAG_STATUS,max_length=20,null=True,blank=True)
  priority = models.IntegerField(null=False,blank=False)
  slug=models.CharField(unique=True,max_length=200,null=True,blank=True)
  problem_url=models.URLField(max_length=250,null=False,blank=False)
  solution_url=models.URLField(max_length=250,null=False,blank=False)
  # change the feild of video from url to char with default as '#'
  # video_url=models.URLField(max_length=200,null=True,blank=True)
  video_url=models.CharField(max_length=250,default='#',null=True,blank=True)
  liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')
  disliked = models.ManyToManyField(User, default=None, blank=True, related_name='disliked')
  STATUS = (
    (True, 'Yes'),
    (False, 'No')
  )
  completed = models.ManyToManyField(User, default=None, blank=True, related_name='completed')
  active = models.BooleanField(choices=STATUS,default=False, blank=False)
  # last_modified_data = models.DateField(auto_now=True)
  # last_modified_time = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)
  last_updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.title)
  
  @property
  def num_likes(self):
    return self.liked.all().count()

  def num_dislikes(self):
    return self.disliked.all().count()


LIKE_CHOICES = (
  ('Like', 'Like'),
  ('Unlike', 'Unlike'),
)

class like(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  problem = models.ForeignKey(problem, on_delete=models.CASCADE)
  value = models.CharField(choices=LIKE_CHOICES,default='Like',max_length=10)

  def __str__(self):
      return str(self.post)


class userProblemData(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  problem = models.ForeignKey(problem,on_delete=models.CASCADE)
  STATUS = (
    (True, 'Like'),
    (False, 'Unlike')
  )
  STATUS2 = (
    (True, 'Yes'),
    (False, 'No')
  )
  like = models.BooleanField(choices=STATUS,null=True, blank=True)
  completed = models.BooleanField(choices=STATUS2,default=False,null=False, blank=False)
  viewed_solution = models.BooleanField(choices=STATUS2,default=False,null=False, blank=False)
  viewed_video = models.BooleanField(choices=STATUS2,default=False,null=False, blank=False)
  shared = models.BooleanField(choices=STATUS2,default=False,null=False, blank=False)
  # last_modified_data = models.DateField(auto_now=True)
  # last_modified_time = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)
  last_updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    template = 'user - {0.user} ---> problem - {0.problem}'
    return template.format(self)
  # check if a problem status can be unique for a user
  class Meta:
    constraints = [
        models.UniqueConstraint(fields=['user', 'problem'], name='unique status of ever problem for a user')
    ]



class myfaq(models.Model):
  title=models.CharField(unique=True,max_length=300,null=False,blank=False)
  short_title=models.CharField(unique=True,max_length=100,null=True,blank=True)
  text=models.TextField(null=False,blank=False)
  priority = models.IntegerField(unique=True,null=False,blank=False)
  STATUS = (
    (True, 'Yes'),
    (False, 'No')
  )
  active = models.BooleanField(choices=STATUS,default=False, blank=False)
  # last_modified_data = models.DateField(auto_now=True)
  # last_modified_time = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)
  last_updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    template = '{0.title} ---> ACTIVE - {0.active}'
    return template.format(self)


class account_verification(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  auth_token=models.CharField(unique=True,max_length=100,null=False,blank=False)
  verification_link=models.URLField(unique=True,max_length=300,null=False,blank=False)
  STATUS = (
    (True, 'verified'),
    (False, 'Not verified')
  )
  verification_status = models.BooleanField(choices=STATUS,default=False, blank=False)
  STATUS2 = (
    (True, 'Active account'),
    (False, 'Blocked account')
  )
  account_status = models.BooleanField(choices=STATUS2,default=True, blank=False)
  created_at = models.DateTimeField(auto_now_add=True)
  last_updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    template = 'user - {0.user} ---> STATUS - {0.verification_status} ---> Acc. Status - {0.account_status}'
    # return template.format(self)
    return str(self.user)
  




