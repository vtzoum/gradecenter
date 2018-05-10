#!/usr/bin/env python
# -*- coding: utf-8 -*-

#(myvenv) ~/djangogirls$ python manage.py shell

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.


class Contact(models.Model):

    first_name = models.CharField(
        max_length=255,
    )
    last_name = models.CharField(
        max_length=255,

    )

    email = models.EmailField()

    def __str__(self):

        return ' '.join([
            self.first_name,
            self.last_name,
        ])

    def get_absolute_url(self):

        return reverse('contacts-view', kwargs={'pk': self.id})


class Address(models.Model):

    contact = models.ForeignKey(Contact)
    address_type = models.CharField(
        max_length=10,
    )

    address = models.CharField(
        max_length=255,
    )
    city = models.CharField(
        max_length=255,
    )
    state = models.CharField(
        max_length=2,
    )
    postal_code = models.CharField(
        max_length=20,
    )

    class Meta:
        unique_together = ('contact', 'address_type',)


'''
NEXT CHAPTER
'''
TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
)

class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})


class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)



class Reporter(models.Model):
    full_name = models.CharField(max_length=70)

    def __str__(self):              # __unicode__ on Python 2
        return self.full_name

class Article(models.Model):
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self):              # __unicode__ on Python 2
        return self.headline


