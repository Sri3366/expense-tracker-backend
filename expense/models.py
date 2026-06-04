from django.db import models # type: ignore

# Create your models here.
class UserDetail(models.Model):
    FullName = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100,unique=True) #unique=True ante same email rendu sarlu register avvakudadhu.
    Password = models.CharField(max_length=50)
    RegDate = models.DateTimeField(auto_now_add=True)  #User register ayina time automatic ga save avthundi.
    
    def __str__(self):
        return self.FullName #Admin panel lo object ni print chesthe FullName display avthundi.

class Expense(models.Model):
    UserId = models.ForeignKey(UserDetail,on_delete=models.CASCADE) #Expense ye user ki sambandhinchindo connect chestundi.(2)ForeignKey use chesam.(3).n_delete=models.CASCADE ante user delete ayithe aa user expenses kuda delete avthai.
    ExpenseDate = models.DateField(null=True,blank=True) #null=True → database lo empty ga undochu ,blank=True → form lo compulsory kaadhu

    ExpenseItem = models.CharField(max_length=100)
    ExpenseCost = models.CharField(max_length=100)
    NoteDate = models.DateTimeField(auto_now_add=True) #Expense add chesina timestamp automatic ga save avthundi

    def __str__(self):
        return f"{self.ExpenseItem} - {self.ExpenseCost}"  #Admin panel lo: Food - 500 la display avthundi.
