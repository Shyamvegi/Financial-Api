from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import User

"""
Let us create models to save data from plaid and user details from clientApp
Main aim is to save itemdata ,tokensdata ,usersdata,transactions
CreateSuperUser to access these models
"""

# Create your models here.
class ItemModel(models.Model):
    access_token = models.CharField(max_length=150)
    item_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class LogsModel(models.Model):
    request = JSONField(null=True, blank=True)
    response = JSONField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

class TransactionsModel(models.Model):
    data = JSONField(null=True, blank=True)

class AccountDetails(models.Model):
    data = JSONField(null=True, blank=True)

class ItemMetadata(models.Model):
    data = JSONField(null=True, blank=True)