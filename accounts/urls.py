
from django.urls import include, path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='home'),
    path('status/', views.status, name='status'),
    path('user_issue_status/', views.user_issue_status, name='user_issue_status'),
    path('user_maintenance_status/', views.user_maintenance_status, name='user_maintenance_status'),
    path('req/',views.req, name='req'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('login/', views.login_user, name='login'),
    path('edit/', views.edit_profile, name='edit'),
    path('logout/', views.logout_user, name='logout'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('user_issue_update/<int:id>/', views.user_issue_update, name='user_issue_update'),
    path('user_issue_edit', views.user_issue_edit, name='user_issue_edit'),


    path('admins_add_item', views.admins_add_item, name='admins_add_item'),
    path('admins_home', views.admins_home, name='admins_home'),
    path('admins_login', views.admins_login, name='admins_login'),
    path('admins_status', views.admins_status, name='admins_status'),
    path('admins_issue_request_status/', views.admins_issue_request_status, name='admins_issue_request_status'),
    #path('admins_issue_update/', views.admins_issue_update, name='admins_issue_update'),
    path('admins_issue_update/<int:id>/', views.admins_issue_update, name='admins_issue_update'),
    path('admins_issue_edit', views.admins_issue_edit, name='admins_issue_edit'),
    path('admin_issue_item/<int:id>/<str:component_type>/<int:quantity>', views.admin_issue_item, name='admin_issue_item'),
    path('admins_issue_item_update', views.admins_issue_item_update, name='admins_issue_item_update'),
    #path('admins_issue_item_update_1', views.admins_issue_item_update_1, name='admins_issue_item_update_1'),
    path('admins_maintenance_status/', views.admins_maintenance_status, name='admins_maintenance_status'),
    path('admins_maintenance_update/<int:id>/', views.admins_maintenance_update, name='admins_maintenance_update'),
    path('admins_maintenance_edit', views.admins_maintenance_edit, name='admins_maintenance_edit'),
    path('staff_handle_req', views.staff_handle_req, name='staff_handle_req'),
    path('staff_handle_update/<int:id>/', views.staff_handle_update, name='staff_handle_update'),
    path('staff_handle_edit', views.staff_handle_edit, name='staff_handle_edit'),
    path('user_maintenance_edit', views.user_maintenance_edit, name='user_maintenance_edit'),
    path('update_product/<int:id>/', views.update_product, name='update_product'),

    path('user_maintenance_update/<int:id>/', views.user_maintenance_update, name='user_maintenance_update'),
    path('add_to_issue', views.add_to_issue, name='add_to_issue'),

    path('user_maintenance_req', views.user_maintenance_req, name='user_maintenance_req'),
    

   # path('admin_issue_item', views.admin_issue_item, name='admin_issue_item'),

    #path('admins_maintenance_request_status/', views.admins_maintenance_request_status, name='admins_maintenance_request_status'),


    #exports here
    path('export_product_table/', views.export_product_table, name='export_product_table'),
    path('export_req_issue_item/', views.export_req_issue_item, name='export_req_issue_item'),
    path('export_res_issue_item/', views.export_res_issue_item, name='export_res_issue_item'),
    path('export_req_maintenance/', views.export_req_maintenance, name='export_req_maintenance'),
]
