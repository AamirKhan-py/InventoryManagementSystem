
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .forms import EditProfileForm
from django.db.models import Count
from django.contrib.auth.models import User
from inventory.models import Product_table, Req_issue_item, Req_maintenance, Res_issue_item, Maintenance_request, user_list
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
import json
#from django.forms.models import model_to_dict
from django.core import serializers
from django.http import HttpResponse
from .resources import Product_table_Resource, Req_issue_item_Resource, Res_issue_item_Resource, Req_maintenance_Resource


#export part
def export_product_table(request):
    product_table_Resource = Product_table_Resource()
    dataset = product_table_Resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Product_Table.csv"'
    return response

def export_req_issue_item(request):
    req_issue_item_Resource = Req_issue_item_Resource()
    dataset = req_issue_item_Resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Request_Issue_item.csv"'
    return response

def export_res_issue_item(request):
    res_issue_item_Resource = Res_issue_item_Resource()
    dataset = res_issue_item_Resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Response_Issue_item.csv"'
    return response

def export_req_maintenance(request):
    req_maintenance_Resource = Req_maintenance_Resource()
    dataset = req_maintenance_Resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Request_maintenance.csv"'
    return response


#Json Work
class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, YourCustomType):
            return str(obj)
        return super().default(obj)


def index(request):
    user_staff = User.objects.filter(is_active=True, is_staff=True)
    user_list.objects.all().delete()
    for staff in user_staff:
        staffs = user_list(user_staffs=staff)
        staffs.save()
    print(user_list)
    return render(request, 'accounts/index.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have successfully logged in !'))
            return redirect('accounts:home')
        else:
            messages.success(request, ('You have failed to login !'))
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html')


@login_required(login_url='accounts:login')
def maintenance(request):
    user = request.user.username
#    mt = Product_table.objects.all()#.filter(user_name=user)
#    mt = model_to_dict(mt)
#    dt  = json.dumps(mt)
    xm = serializers.serialize("xml", Product_table.objects.all())
#    print(xm)
    js = serialize('json', Product_table.objects.all().filter(user_name=user), cls=LazyEncoder)
    print(js)
    if request.method=="POST":
        lab_number = request.POST["lab_number"]
        department_type = request.POST["department_type"]
        description = request.POST["description"]

        mainobj = Req_maintenance(lab_number=lab_number,department_type=department_type,description=description)
        mainobj.save()
        return render(request, 'accounts/maintenance.html', { 'mt' : js })
    else:
         return render(request, 'accounts/maintenance.html', { 'mt' : js })


@login_required(login_url='accounts:login')
def status(request):
    pro_table_object = Product_table.objects.all()
    count = Product_table.objects.all().values('component_name').annotate(total=Count('component_type'))
    print(count)
    return render(request, 'accounts/status.html', {'ai':pro_table_object, 'cnt':count})

@login_required(login_url='accounts:login')
def user_issue_status(request):
        users = request.user.username
        request_issue_object = Req_issue_item.objects.all().filter(user_name=users)
        return render(request, 'accounts/user_issue_status.html', {'es':request_issue_object})

# new entry 1
@login_required(login_url='accounts:login')
def user_maintenance_status(request):
        users = request.user.username
        request_issue_object = Req_maintenance.objects.all()#.filter(user=users)
        return render(request, 'accounts/user_maintenance_status.html', {'es':request_issue_object})


@login_required(login_url='accounts:login')
def req_maintenance(request):
        #if request.method=="POST":
        users = request.user.username
        request_issue_object = Req_maintenance.objects.all()#.filter(user=users)
        return render(request, 'accounts/user_maintenance_status.html', {'es':request_issue_object})


@login_required(login_url='accounts:login')
def req(request):
    if request.method=="POST":
        lab_number = request.POST["lab_number"]
        component_type = request.POST["component_type"]
        quantity = request.POST["quantity"]
        description = request.POST["description"]
        user_name = request.user.username

        reqobj  = Req_issue_item(user_name = user_name, lab_number=lab_number,component_type=component_type,quantity=quantity,description=description)
        reqobj.save()
        return render(request, 'accounts/req.html')
    else:
        return render(request, 'accounts/req.html')


def logout_user(request):
    logout(request)
    messages.success(request, ('You have successfullylogout...'))
    return redirect('accounts:home')


@login_required(login_url='accounts:login')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ('You Have successfully Edited yous profile detail...'))
            return redirect('accounts:edit')
    else:
        form = EditProfileForm(instance = request.user)
        context = {'form' : form}
        return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='accounts:login')
def changepassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user = request.user)
        if form.is_valid():
            form.save()
            #update_session_auth_hash(request, form.user)
            messages.success(request, ('You Have successfully changed yous password...'))
            return redirect('accounts:edit')
    else:
        form = PasswordChangeForm(user = request.user)
        context = {'form' : form}
        return render(request, 'accounts/edit_profile.html', context)


def user_issue_update(request, id):
    request_issue_objectss = Req_issue_item.objects.all().filter(pk=id)
    user = request.user.username
    print(request_issue_objectss)
    #objects = Req_issue_item()
    #ss= objects.Alldata()
    #print(ss)
    return render(request, 'accounts/user_issue_update.html', {'es':request_issue_objectss, 'rs':user})

def user_maintenance_update(request, id):
    request_issue_objectss = Req_maintenance.objects.all().filter(pk=id)
    user = request.user.username
    print(request_issue_objectss)
    #objects = Req_issue_item()
    #ss= objects.Alldata()
    #print(ss)
    return render(request, 'accounts/user_maintenance_update.html', {'es':request_issue_objectss, 'rs':user})


def user_maintenance_edit(request):
    if request.method == 'POST':
        Rid = request.POST['ids']
        user_name = request.user.username
        #lab_number = request.POST['lab_number']
        #component_type = request.POST['component_type']
        #component_name = request.POST['component_name']
        user_status = request.POST['status']
        rm= Req_maintenance.objects.all().filter(id=Rid).update(status = user_status)
        return redirect('accounts:user_maintenance_status')


def user_issue_edit(request):
    if request.method == 'POST':
            Rid = request.POST['ids']
            user_status = request.POST['user_status']
            request_issue_objectss1 = Req_issue_item.objects.all().filter(id=Rid).update(status = user_status)
            #request_issue_objectss1.save()
            print(request_issue_objectss1)
            print("aasif")
            return redirect('accounts:user_issue_status')
    else:
            print("hello")
    return redirect('accounts:user_issue_status')








@login_required(login_url='accounts:login')
def admins_home(request):
        return render(request, 'accounts/admins_index.html')


#@login_required(login_url='accounts:login')
def admins_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have successfully logged in !'))
            return redirect('accounts:admins_home')
        else:
            messages.success(request, ('You have failed to login !'))
            return redirect('accounts:admins_login')
    else:
        return render(request, 'accounts/admins_login.html')


@login_required()
def admins_status(request):
    #users = request.user.username
    pro_table_object = Product_table.objects.all()
    #request_issue_object = Req_issue_item.objects.all()#.filter(user_name=users)
    count = Product_table.objects.all().filter(user_name="none").values('component_type').annotate(total=Count('component_type'))
    #print(count)
    return render(request, 'accounts/admins_status.html', {'ai':pro_table_object, 'cnt':count})

@login_required
def admins_add_item(request):
    if request.method == 'POST':
            c_name = request.POST['c_name']
            c_type = request.POST['c_type']
            c_size = request.POST['c_size']
            c_sno  = request.POST['c_sno']
            c_mno  = request.POST['c_mno']
            c_mname= request.POST['c_mname']

            prod_object = Product_table(component_type=c_type, component_name=c_name, component_size=c_size, component_serial_number=c_sno, model_number=c_mno, manufacturer_name=c_mname)
            prod_object.save()
            return render(request, 'accounts/admins_index.html')

    else:
            return render(request, 'accounts/admins_add_item.html')
            
            

        


def admins_issue_request_status(request):
    request_issue_object = Req_issue_item.objects.all()
    request_issue_object = request_issue_object[::-1]
    userz = request.user.username
    return render(request, 'accounts/admins_issue_request_status.html', {'es':request_issue_object, 'rs':userz})

def admins_issue_update(request, id):
    request_issue_objectss = Req_issue_item.objects.all().filter(pk=id)
    print(request_issue_objectss)
    #objects = Req_issue_item()
    #ss= objects.Alldata()
    #print(ss)
    return render(request, 'accounts/admins_issue_update.html', {'es':request_issue_objectss})


def admins_issue_edit(request):
    if request.method == 'POST':
            Rid = request.POST['ids']
            admin_status = request.POST['admin_status']
            request_issue_objectss1 = Req_issue_item.objects.all().filter(id=Rid).update(admin_status = admin_status)
            #request_issue_objectss1.save()
            print(request_issue_objectss1)
            print("aasif")
            return redirect('accounts:admins_issue_request_status')
    else:
            print("hello")
    return render(request, 'accounts/admins_issue_request_status.html')


def admin_issue_item(request,component_type, id, quantity):
    #print(ct)
    name = "asif"
    count = Product_table.objects.all().filter(component_type=component_type, component_name=name)

    request_issue_objectss = Req_issue_item.objects.all().filter(pk=id)
    if Product_table.objects.all().values('component_type').filter(component_type=component_type, lab_number=0, user_name="none").annotate(total=Count('component_type')).exists():
            countss = Product_table.objects.all().values('component_type').filter(component_type=component_type, lab_number=0, user_name="none").annotate(total=Count('component_type'))
            totals = countss[0]['total']
            pt = totals - quantity
            pending_total= abs(pt)
            no_item = 1
            print(pending_total)
            return render(request, 'accounts/admin_issue_item.html', {'es':request_issue_objectss, 'cnt':count, 'qnt':countss, 'abs':pending_total, 'nt':no_item})

        
    else:
            print("not exist")
            countss = 0
            no_item = 0
            pt = countss - quantity
            pending_total = abs(pt)
            print(countss)
            return render(request, 'accounts/notice.html')
            

    print("kalseekker")
    print(pending_total)
    #print(countss.keys())
    #print(pending)

    #print(count)
    #print("hello")
    #print(request_issue_objectss)
    print(count)
    print(request_issue_objectss)
    #tpe = count.filter(component_type=component_type)
    #component_type = request_issue_objectss.component_type
    #request = request_issue_objectss.all().filter()
    #print(request)
    #print(tpe)
    #print(request_issue_objectss)
    #objects = Req_issue_item()
    #ss= objects.Alldata()
    #print(ss)
    #return render(request, 'accounts/admin_issue_item.html', {'es':request_issue_objectss, 'cnt':count, 'qnt':countss, 'abs':pending_total})

def admins_issue_item_update(request):
    if request.method == 'POST' and 'bttn1' in request.POST:
            Rid = request.POST['ids']
            component_type = request.POST['component_type']
            quantity = request.POST['quantity']
            lab_number = request.POST['lab_number']
            user_name = request.POST['user']
            quantities = int(quantity)
            while quantities!=0:
                    pro_update = Product_table.objects.all().filter(component_type = component_type, lab_number=0 ).update(lab_number=lab_number, user_name=user_name )
                    print("hello")
                    quantities = quantities -1
            
			#response_object = Res_issue_item(item_type = component_type, )
            return redirect('accounts:admins_issue_request_status')


    if request.method == 'POST' and 'bttn2' in request.POST:
            Rid = request.POST['ids']
            component_type = request.POST['component_type']
            quantity = request.POST['quantity']
            lab_number = request.POST['lab_number']
            quantity_assign = request.POST['quantity_assign']
            quantity_pending = request.POST['quantity_pending']
            user_name = request.POST['user']
            qty = int(quantity_assign)
            Req = Req_issue_item.objects.all().filter(id = Rid).update(pending_item = quantity_pending)

            while qty!=0:
                    pro_update = Product_table.objects.all().filter(component_type = component_type, lab_number=0 ).update(lab_number=lab_number, user_name=user_name )
                    print("hello1")
                    qty = qty -1
            return redirect('accounts:admins_issue_request_status')


#def admins_issue_item_update_1(request):


@login_required(login_url='accounts:login')
def admins_maintenance_status(request):
        #users = request.user.username
        request_issue_object = Req_maintenance.objects.all().filter(option="No")
        return render(request, 'accounts/admins_maintenance_status.html', {'es':request_issue_object})


def admins_maintenance_update(request, id):
    request_issue_objectss = Req_maintenance.objects.filter(pk=id)
    staff_list = user_list.objects.all()
    print(request_issue_objectss)
	#objects = Req_issue_item()
	#ss= objects.Alldata()
	#print(ss)
    return render(request, 'accounts/admins_maintenance_update.html', {'es':request_issue_objectss, 'sl':staff_list})

#    else:
#        return render(request, 'accounts/admins_maintenance_update.html', {'es':request_issue_objectss})

def admins_maintenance_edit(request):
    if request.method == 'POST':
            Rid = request.POST['ids']
            component_type = request.POST['component_type']
            serial_number = request.POST['component_serial_number']
            lab_number = request.POST['lab_number']
            #status = request.POST['admin_status']
            staff = request.POST['staff']
            maintenance_edit = Req_maintenance.objects.all().filter(id=Rid).update(staff=staff)

            
			#response_object = Res_issue_item(item_type = component_type, )
            return redirect('accounts:admins_maintenance_status')



def user_maintenance_req(request):
    if request.method == 'POST':
        user_name = request.user.username
        lab_number = request.POST['lab_number']
        component_type = request.POST['component_type']
        component_name = request.POST['component_name']
        serial_number = request.POST['serial_number']
        req_maintenance_obj = Req_maintenance(lab_number=lab_number, component_name=component_name, component_type=component_type, component_serial_number=serial_number, user_name=user_name)
        req_maintenance_obj.save()
        return redirect('accounts:user_maintenance_status')


def staff_handle_req(request):
    user_name = request.user.username
    req_maint_obj = Req_maintenance.objects.all().filter(staff=user_name)
    return render(request, 'accounts/staff_handle.html',{'remo':req_maint_obj})

def staff_handle_update(request,id):
    Rid = id
    admin_status = "Approved"
    rm= Req_maintenance.objects.all().filter(id=Rid)#.update(admin_status = admin_status)
    return render(request, 'accounts/staff_req_edit.html',{'remo':rm})


def staff_handle_edit(request):
    if request.method == 'POST':
        Rid = request.POST['ids']
        user_name = request.user.username
        serial_number = request.POST['serial_number']
        #component_type = request.POST['component_type']
        #component_name = request.POST['component_name']
        admin_status = request.POST['admin_status']
        rm= Req_maintenance.objects.all().filter(id=Rid).update(admin_status = admin_status)
        pt = Product_table.objects.all().filter(component_serial_number=serial_number).update(faulted=admin_status)
        return redirect('accounts:staff_handle_req')


def update_product(request,id):
    rm= Req_maintenance.objects.all().filter(pk=id)
    print(rm)
    return render(request, 'accounts/admin_falty.html',{'remo':rm})


    #return render(request, 'accounts/faulty_assign.html',{'remo':rm})


def add_to_issue(request):
    if request.method == 'POST':
        Rid = request.POST['ids']
        user_name = request.POST['user']
        lab_number = request.POST['lab_number']
        component_type = request.POST['component_type']
        serial_number = request.POST['serial_number']
        quantity = 1
        req_issue_item = Req_issue_item(lab_number=lab_number, component_type=component_type, user_name=user_name, quantity=quantity)
        req_issue_item.save()
        rm= Req_maintenance.objects.all().filter(id=Rid).update(option="YES")

        return redirect('accounts:admins_issue_request_status')

        #component_name = request.POST['component_name']
        #admin_status = request.POST['admin_status']