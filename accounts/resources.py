from import_export import resources
from inventory.models import Product_table, Req_issue_item, Req_maintenance, Res_issue_item, Maintenance_request, user_list


class Product_table_Resource(resources.ModelResource):
    class Meta:
        model = Product_table


class Req_issue_item_Resource(resources.ModelResource):
    class Meta:
        model = Req_issue_item


class Res_issue_item_Resource(resources.ModelResource):
    class Meta:
        model = Req_issue_item


class Req_maintenance_Resource(resources.ModelResource):
    class Meta:
        model = Req_maintenance