from django.shortcuts import render # type: ignore
from django.http import JsonResponse # type: ignore 
from django.views.decorators.csrf import csrf_exempt # type: ignore
import json
from .models import *

# Create your views here.

#signup API
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body) #Frontend nunchi vachina JSON data ni Python dictionary loki convert chestunnam.
        fullname = data.get('FullName') #JSON lo unna values ni separate variables lo store chestunnam.
        email = data.get('Email')
        password = data.get('Password')

        
        if UserDetail.objects.filter(Email=email).exists(): #Same email already database lo unda ani check chestundi
            return JsonResponse({'message':'Email already exists'},status=400)
        #If the email is already taken, it stops and sends a message back saying, "Error: Email already exists."

        UserDetail.objects.create(FullName=fullname,Email=email,Password=password)#data will be created in database 
        return JsonResponse({'message':'user registerd successfully'},status=201)
        #If the email is new, it creates a brand-new user file, saves it into the database, and sends back a message saying, "Success: User registered!"

#Login API
@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('Email')
        password = data.get('Password')

        try:
            user=UserDetail.objects.get(Email=email,Password=password) #Database lo same email and password unna user ni search chestundi.
            return JsonResponse({'message':'Login successful','userId':user.id,'username':user.FullName},status=200) #Login success ayithe user details frontend ki pampisthundi.
        except:
            return JsonResponse({'message':'Invalid Credentials'},status=400)
#
# ADD Expense API
@csrf_exempt
def add_expense(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('UserId') #Expense ye user add chesthunado aa user id tiskuntundi.
        expense_date = data.get('ExpenseDate')
        expense_item = data.get('ExpenseItem')
        expense_cost = data.get('ExpenseCost')  #e 3 Expense ni database lo save chestundi.

        user=UserDetail.objects.get(id=user_id) #Aa user object ni database nunchi fetch chestundi.
        try:
            Expense.objects.create(UserId=user,ExpenseDate=expense_date,ExpenseItem=expense_item,ExpenseCost=expense_cost)
            return JsonResponse({'message':'Expense added successfully'},status=201)
        except Exception as e:
            return JsonResponse({'message':'Something went wrong','error':str(e)},status=400)

#
# Manage Expense API
@csrf_exempt
def manage_expense(request,user_id):
    if request.method == 'GET':
        
        expenses = Expense.objects.filter(UserId=user_id) #Particular user ki sambandhinchina expenses anni fetch chestundi.
        expense_list = list(expenses.values()) #QuerySet ni JSON compatible list ga convert chestundi.
        return JsonResponse(expense_list,safe=False) #Expenses list ni frontend ki pampisthundi. safe=False use cheyyali because list return chestunnam.

@csrf_exempt
def update_expense(request,expense_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            expense = Expense.objects.get(id=expense_id) #Update cheyyalsina expense ni fetch chestundi
            expense.ExpenseDate = data.get('ExpenseDate',expense.ExpenseDate) #New value unte update chestundi. Lekapothe old value maintain chestundi.
            expense.ExpenseItem = data.get('ExpenseItem',expense.ExpenseItem)
            expense.ExpenseCost = data.get('ExpenseCost',expense.ExpenseCost)
            expense.save()
            return JsonResponse({'message':'Expense updated successfully'})
        except:
            return JsonResponse({'message':'Expense not found'},status=404)
    

@csrf_exempt
def delete_expense(request,expenseId):
    if request.method == 'DELETE':
        try:
            expense = Expense.objects.get(id=expenseId) #ah delete button meedha click cheyagaane dhaani id(database lo Expense Table undhi kadha ) adhi thesukuvelli ikkadi expense variable lo store chesthundhi
            expense.delete() #Selected expense database nunchi delete avthundi.
            return JsonResponse({'message':'Expense deleted successfully'},status=200)
        except:
            return JsonResponse({'message':'Expense not found'},status=404)

from django.db.models import Sum # type: ignore
# Search Expense API
@csrf_exempt
def search_expense(request,user_id):#frontend lo login ayyi vunna user_id
    if request.method == 'GET':
        from_date=request.GET.get('from') #URL query params nunchi dates tiskuntundi.
        to_date=request.GET.get('to')
        expenses = Expense.objects.filter(UserId=user_id,ExpenseDate__range=[from_date,to_date]) #ExpenseDate__range=[from_date,to_date] :Given date range madhyalo unna expenses fetch chestundi
        expense_list = list(expenses.values())
        agg=expenses.aggregate(Sum('ExpenseCost')) #{'ExpenseCost__sum':3500} Total expense calculate chestundi.
        total = agg['ExpenseCost__sum'] or 0 #Expenses lekapothe None ostundi. Anduke 0 set chestunnam.
        return JsonResponse({'expenses':expense_list,'total':total})

#Change Password API
@csrf_exempt
def change_password(request,user_id):
    if request.method == 'POST':
        data = json.loads(request.body)

        old_password = data.get('oldPassword')
        new_password = data.get('newPassword')

        try:
            user=UserDetail.objects.get(id=user_id)
            if user.Password!=old_password: #User old password correct aa kaadha check chestundi.
                return JsonResponse({'message':'Old password is incorrect'},status=400)
            user.Password = new_password #New password assign chestundi.
            user.save() #Database lo update avthundi.
            return JsonResponse({'message':'Password changed successfully'})
        except:
                return JsonResponse({'message':'User not found'},status=404)
        