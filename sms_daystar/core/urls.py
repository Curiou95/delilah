from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # landing and dashboard
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    # AUTHENTICATION
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    # BABY URLS
    path("viewbaby/", views.babies, name="viewbaby"),
    # path("viewbaby/<int:id>/", views.read_baby, name="readbaby"),
    path("addbaby/", views.createbaby, name="addbaby"),
    path("viewbaby/<int:id>/", views.readbaby, name="readbaby"),
    path("editbaby/<int:id>/", views.updatebaby, name="updatebaby"),
    path("deletebaby/<int:id>/", views.deletebaby, name="deletebaby"),
    # babycheckin babycheckout
    path("checkin/<int:baby_id>", views.checkin, name="checkin"),
    path("checkout/<int:checkin_id>/", views.checkout, name="checkout"),
    # SITTER URLS
    path("viewsitter/", views.sitter, name="viewsitter"),
    path("sitter_archive/", views.view_archive, name="viewsitter_archive"),
    path("unarchive-sitter/<int:pk>/", views.unarchive_sitter, name="unarchive_sitter"),
    path("addsitter/", views.createsitter, name="addsitter"),
    path("viewsitter/<int:id>", views.readsitter, name="readsitter"),
    path("editsitter/<int:id>", views.updatesitter, name="updatesitter"),
    path("deletesitter/<int:id>", views.deletesitter, name="deletesitter"),
    path("onduty", views.on_duty, name="onduty"),
    path("regduty/<int:id>", views.addDuty, name="regduty"),
    # sitter scheduling
    # path('add_schedule/', views.schedule_create, name='add_schedule'),
    # path('schedule/', views.schedule_list, name='schedule_list'),
    # path('schedule/<int:schedule_id>/edit/', views.edit_schedule, name='edit_schedule'),
    # assigning babies
    path("assignsitter/<int:id>/", views.assignsitter, name="assignsitter"),
    path("assign_view/", views.assign_view, name="assign_view"),
    # INVENTORY
    path("inventory/", views.inventoryreciept, name="inventory"),
    path("addinventory/", views.addinventory, name="addinventory"),
    # path('issues/<int:id>', views.issue, name='issue'),
    path("issue/", views.issue_inventory, name="issue"),
    path("items", views.view_issued_items, name="view_items"),
    path("update_inventory/<int:id>/", views.updateinventory, name="update_inventory"),
    # DOLLS
    path("saledoll/<int:id>", views.make_sale, name="saledoll"),
    # path('dolllist/', views.doll_list, name='dolllist'),
    path("viewdoll/", views.dollview, name="dollview"),
    path("sold-dolls/", views.sold_dolls_view, name="sold_dolls"),
    path("payreciept/<int:id>/", views.pay_reciept, name="payreciept"),
    path("payrecieptfee/<int:id>/", views.pay_feesreciept, name="payfeesreciept"),
    # path('payrecieptsitter/<int:id>/', views.pay_sitterreciept, name='paysitterreciept'),
    # FINANCE
    path("funds/", views.financeview, name="financeview"),
    path("payment/", views.make_payment, name="make_payment"),
    # text
    path("sitter_txt", views.sitter_txt, name="sitter_txt"),
]

# purchaseorder
# salesorder
