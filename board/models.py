from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.TextChoices):
    TANK = 'tank', 'Танки'
    HEAL = 'heal', 'Хилы'
    DD = 'dd', 'ДД'
    TRADER = 'trader', 'Торговцы'
    GUILDMASTER = 'guild', 'Гилдмастеры'
    QUESTGIVER = 'quest', 'Квестгиверы'
    BLACKSMITH = 'smith', 'Кузнецы'
    LEATHERWORK = 'leather', 'Кожевники'
    ZEL = 'zel', 'Зельевары'
    MAGE = 'mage', 'Мастера заклинаний'

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    category = models.CharField(max_length=16, choices=Category.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class ReplyStatus(models.TextChoices):
    PENDING = 'pending', 'Ожидает'
    ACCEPTED = 'accepted', 'Принят'
    DECLINED = 'declined', 'Отклонён'

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField()
    status = models.CharField(max_length=10, choices=ReplyStatus.choices, default=ReplyStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reply by {self.author} on {self.post}"
