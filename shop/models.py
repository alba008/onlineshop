from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    parent = models.ForeignKey(
        'self',  # Self-referential relationship
        on_delete=models.CASCADE,
        related_name='subcategories',
        blank=True,
        null=True  # Root categories will have no parent
    )
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        if self.parent:
            return f"{self.parent} -> {self.name}"  # Show hierarchy in admin
        return self.name

    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category', args=[self.slug]
        )
    

def validate_image_url(value):
    """
    Validates that the given URL points to a valid image file.
    Allowed extensions: .jpg, .jpeg, .png, .gif
    """
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not any(value.lower().endswith(ext) for ext in valid_extensions):
        raise ValidationError('Invalid image URL. Allowed extensions are: .jpg, .jpeg, .png, .gif.')



class Product(models.Model):
    category = models.ForeignKey(
        'Category',
        related_name='products',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(
        models.URLField(max_length=500, blank=True, validators=[validate_image_url])
    )
    product_link = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # New field for customer ratings
    rating = models.FloatField(default=0.0)  # Store rating as a float value (0 - 5)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def get_star_rating(self):
        """Returns a range for full stars"""
        return range(int(self.rating))
    
    def get_empty_stars(self):
        """Returns a range for empty stars"""
        return range(5 - int(self.rating))

class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)  # Add this field for the link


    def __str__(self):
        return self.title 