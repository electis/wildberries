from django.contrib.postgres.fields import JSONField
from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=32)
    path = models.CharField(max_length=32)
    parents = models.ManyToManyField('Section', related_name='childs')
    last_update = models.DateTimeField(null=True, blank=True)

    def make_path(self):
        path_list = [self.path]
        section = self
        while section.parent:
            section = section.parent
            path_list.append(section.path)
        return '/'.join(reversed(path_list))


class Product(models.Model):
    product_id = models.CharField(max_length=32)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    data = JSONField(default=dict)
    last_update = models.DateTimeField(null=True, blank=True)


class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    date = models.DateField()


class SectionSetting(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    period = models.CharField(max_length=64)


class LimitSettings(models.Model):
    endpoint = models.CharField(max_length=32)
    daily_limit = models.PositiveSmallIntegerField(default=10)
    today_count = models.PositiveSmallIntegerField(default=0)


class Subscribe(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    email = models.EmailField()
