# tourism/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='place_images/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Place(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='places')
    image = models.ImageField(upload_to='places/', null=True, blank=True)
    timetotravel = models.CharField(max_length=50, default="2 days")  # Added max_length

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Place"
        verbose_name_plural = "Places"

class Details(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=100)
    duration = models.IntegerField()
    tour_overview = models.TextField()
    tour_highlights = models.JSONField()
    whats_included = models.JSONField(null=True, blank=True)
    itinerary = models.JSONField()
    recommendations = models.JSONField()
    must_try_food = models.JSONField()
    recommended_guides = models.JSONField(null=True, blank=True)
    faqs = models.JSONField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='details')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='details')
    image1 = models.ImageField(upload_to='details_images/')
    image2 = models.ImageField(upload_to='details_images/')
    image3 = models.ImageField(upload_to='details_images/')
    image4 = models.ImageField(upload_to='details_images/')
    image5 = models.ImageField(upload_to='details_images/')
    map_image = models.ImageField(upload_to='maps/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Detail"
        verbose_name_plural = "Details"

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/')
    author = models.CharField(max_length=100, default="ghumnesathi")  # Changed to CharField for consistency

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"