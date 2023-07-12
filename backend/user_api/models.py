from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class AppUserManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		email = self.normalize_email(email)
		user = self.model(email=email)
		user.set_password(password)
		user.save()
		return user
	def create_superuser(self, email, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		user = self.create_user(email, password)
		user.is_superuser = True
		user.save()
		return user


class AppUser(AbstractBaseUser, PermissionsMixin):
	user_id = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=50, unique=True)
	username = models.CharField(max_length=50)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
	objects = AppUserManager()
	def __str__(self):
		return self.username
	    
class Transaction(models.Model):
    user_id = models.ForeignKey(AppUser, on_delete=models.CASCADE) # Remove entry when parent row is deleted (ie user)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    name = models.CharField(max_length=50)
    txn_cd = models.CharField(max_length=2)
    tmstmp = models.DateField()
    class Meta:
        managed = True
        db_table = "transactions"


class Budget(models.Model):
    user_id = models.ForeignKey(AppUser, on_delete=models.CASCADE) # Remove entry when parent row is deleted (ie user)
    monthly_budget = models.DecimalField(decimal_places=2, max_digits=10)
    rent_lmt = models.DecimalField(decimal_places=2, max_digits=10)
    grocery_lmt = models.DecimalField(decimal_places=2, max_digits=10)
    entertainment_lmt = models.DecimalField(decimal_places=2, max_digits=10)
    variable_lmt = models.DecimalField(decimal_places=2, max_digits=10) # any expenses that come up randomly
    class Meta:
        managed = True
        db_table = "budgets"


class TransactionTypes(models.Model): # Mapping table
    txn_abbr = models.CharField(max_length=2)
    txn_desc = models.CharField(max_length=20)
    class Meta:
        managed = True
        db_table = "transaction_types"

class TransactionCodes:
    HOUSING = 'HS'
    GROCERY = 'GC'
    ENTERTAINMENT = 'ET' 
    TRANSPORTATION = 'TP'
    TOILETRIES = 'TL'
    SUBSCRIPTION = 'SC'