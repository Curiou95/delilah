from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    
    # AUTHENTICATION
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    
    # BABY URLS
    path('viewbaby/', views.babies, name='viewbaby'),
    path('addbaby/', views.createbaby, name='addbaby'),
    path('viewbaby/<int:id>', views.readbaby, name='readbaby'),
    path('editbaby/<int:id>', views.updatebaby, name='updatebaby'),
    path('deletebaby/<int:id>', views.deletebaby, name='deletebaby'),
    # babycheckin babycheckout
    # path('checkin/<int:baby_id>/', views.checkin, name='checkin'),
    # path('checkout/<int:baby_id>/', views.checkout, name='checkout'),
    path('checkin/<int:baby_id>', views.checkin, name='checkin'),
    path('checkout/<int:checkin_id>/', views.checkout, name='checkout'),
    
    
    # SITTER URLS
    path('viewsitter/', views.sitter, name='viewsitter'),
    path('addsitter/', views.createsitter, name='addsitter'),
    path('viewsitter/<int:id>', views.readsitter, name='readsitter'),
    path('editsitter/<int:id>', views.updatesitter, name='updatesitter'),
    path('deletesitter/<int:id>', views.deletesitter, name='deletesitter'),
    path('assignsitter/<int:sitter_id>', views.assignsitter, name='assignsitter'), 
    
    # INVENTORY
    path('inventory/', views.inventoryreciept, name='inventory'),
    path('addinventory/', views.addinventory, name='addinventory'),
    path('issues/<>int:id', views.issue, name='issue'),
    path('items', views.all_issue_items, name='all_issue_items'),
    
    # DOLLS
    path('viewdoll/', views.dollview, name='dollview'),
    
    
    
    # FINANCE
    path('funds/', views.financeview, name='financeview'),
]

# purchaseorder
# salesorder