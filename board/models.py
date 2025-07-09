from django.db import models

class BoardType(models.TextChoices):
    HOME = 'home', '둥지'
    FREE = 'free', '자유게시글'
    NOTICE = 'notice', '공지사항'
    COMPLAINT = 'complaint', '학급신문고'

CATEGORY_CHOICES = [
    ('자유', '자유'),
    ('공지', '공지'),
    ('1학년 둥지', '1학년 둥지'),
    ('2학년 둥지', '2학년 둥지'),
    ('3학년 둥지', '3학년 둥지'),
]
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    writer = models.CharField(max_length=50)
    board_type = models.CharField(max_length=20, choices=BoardType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='자유')
    image = models.ImageField(upload_to='images/', blank=True, null=True)
   

    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    writer = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)