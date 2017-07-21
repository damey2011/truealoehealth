from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap
from django.db import models


# Create your models here.
from django.template.defaultfilters import slugify
from django.urls import reverse
from products.models import ProductCategory


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User)
    likes = models.IntegerField(default=0)
    slug = models.CharField(blank=True, max_length=150)
    category = models.ForeignKey(to=ProductCategory, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog-post', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp']


class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        author = User.objects.get(username="leke")
        return BlogPost.objects.filter(author=author)

    def lastmod(self, obj):
        return obj.timestamp


class StaticPostsSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'discount',
            'become-owner',
            'all-prods',
            'fb',
            'prods',
            'all-blogs',
            'aloe',
            'nutrition',
            'cosmetics',
            'skincare',
            'bee_products',
            'combo',
            'personal',
            'weight',
            'gluten',
            'fit',
            'c9',
            'c9-inst'
        ]

    def location(self, item):
        return reverse(item)


class Comment(models.Model):
    name = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.email
