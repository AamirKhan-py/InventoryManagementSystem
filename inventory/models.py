
import time
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class multiple:
    component_choices = (
        ('DESKTOP ITEM',(
            ('MONITOR', 'MONITOR'),
            ('CPU', 'CPU'),
            ('KEYBOARD', 'KEYBOARD'),
            ('MOUSE', 'MOUSE'),
            ('LAPTOP', 'LAPTOP'),
            ('STORAGE DEVICES', 'STORAGE DEVICES'),
            ('SOFTWARES', 'SOFTWARES'),
        )),
        ('NETWORK ITEM',(
            ('GATEWAY', 'GATEWAY'),
            ('ROUTER', 'ROUTER'),
            ('SWITCH', 'SWITCH'),
            ('BRIDGE', 'BRIDGE'),
            ('REPEATER', 'REPEATER'),
            ('LAN CABLE', 'LAN Cable'),
        )),
        ('OTHER ITEM',(
            ('PRINTER', 'PRINTER'),
            ('PROJECTOR', 'PROJECTOR'),
            ('POWER CABLE', 'POWER CABLE'),
            ('PROJECTOR CABLE', 'PROJECTOR CABLE'),
        )),
    )

    status = (
        ('Approved','Approved'),
        ('Pending','Pending'),
        ('Cancelled','Cancelled'),
    )


class Product_table(models.Model):

    def __str__(self):
        return '{} {} {} {} {}'.format(self.pk, self.component_name, self.component_type, self.component_size, self.model_number)

# description of item starts here
    choice = multiple()
    choices = choice.component_choices
    component_type = models.CharField(max_length=100, choices=choices, default="DESKTOP ITEM")
    component_name = models.CharField(max_length=50)
    component_size = models.CharField(max_length=20)
    component_serial_number = models.CharField(max_length=30)
    manufacturer_name = models.CharField(max_length= 50 )
    model_number = models.CharField(max_length= 30)
    user_name = models.CharField(max_length= 30, default = "none")
    lab_number = models.IntegerField(max_length= 4, default=0)
    faulted = models.CharField(max_length=10,default="NO")
#description ends here, any other fields to be added will be added later






class Maintenance_request(models.Model):

    def __str__(self):
        return self.maintenance.component_name

    maintenance = models.ForeignKey(Product_table, on_delete=models.CASCADE)
    choice = multiple()
    choices = choice.component_choices
    item_type = models.CharField(max_length=100, choices=choices, default="DESKTOP ITEM")
    request_time_and_date = models.DateTimeField(auto_now_add=True)
    dept_name = (
        ("COMPUTER", "COMPUTER ENGINEERRING"),
        ("MECHANICAL", "MECHANICAL ENGINEERING"),
        ("CIVIL", "CIVIL ENGINEERRING"),
        ("ELECTRICAL", "ELECTRICAL ENGINEERRING"),
        ("ELECTRONICS & TELECOMMUNICATIONS", "ELECTRONICS & TELECOMMUNICATIONS ENGINEERRING"),
    )
    request_dept = models.CharField(max_length=100, choices= dept_name, default= "COMPUTER")
    requestor_name = models.CharField(max_length= 30)
    description = models.CharField(max_length=150)
    serial_number = models.CharField(max_length=150)
    lab_number = models.CharField(max_length=150)



class Req_issue_item(models.Model):
    def __str__(self):
        return '{} {} {} {} {}'.format(self.pk, self.status, self.lab_number, self.quantity, self.user_name)
    
    #def Alldata(self):
     #   return '{} {} {} {} {}'.format(self.pk, self.status, self.lab_number, self.quantity, self.user_name)

    choice = multiple()
    choices = choice.component_choices
    lab_number = models.IntegerField()
    component_type = models.CharField(max_length=100, choices=choices, default="DESKTOP ITEM")
    quantity = models.IntegerField()
    description = models.CharField(max_length = 250)
    statuss = choice.status
    status = models.CharField(max_length=10, choices=statuss, default="Pending")
    user_name = models.CharField(max_length=100)
    admin_status = models.CharField(max_length=15, default="Pending")
    pending_item = models.IntegerField(default=0) 



class Res_issue_item(models.Model):
    
    def __str__(self):
        return self.item_name

    issue = models.ForeignKey(Req_issue_item, on_delete=models.CASCADE)
    choice = multiple()
    choices = choice.component_choices
    item_type = models.CharField(max_length=100, choices=choices, default="DESKTOP ITEM")
    item_name = models.CharField(max_length = 25)
    quantity_required = models.IntegerField()
    request_date = models.DateTimeField(auto_now_add=True)
    lab_number =  models.IntegerField()
    lab_incharge = models.CharField(max_length = 100)

class user_list(models.Model):

    def __str__(self):
        return self.user_staffs
    user_staffs = models.CharField(max_length=20)


# new entry 2
class Req_maintenance(models.Model):

    def __str__(self):
        return '{} {} {} {} {}'.format(self.lab_number, self.component_type, self.component_name, self.user_name, self.staff)

    component_type = models.CharField(max_length=100, default="")
    lab_number = models.IntegerField()
    #department_type = models.CharField(max_length = 60)
    #description = models.CharField(max_length = 250, default="")
    component_serial_number = models.CharField(max_length=150)
    component_name = models.CharField(max_length=150)
    choice = multiple()
    statuss = choice.status
    status = models.CharField(max_length=10, default="Pending")
    admin_status = models.CharField(max_length=15, default="Pending")
    staff = models.CharField(max_length=15,default="Not Assign")
    request_date = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=25)
    option = models.CharField(max_length=20,default="No")


