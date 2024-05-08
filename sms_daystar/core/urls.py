from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    
    # BABY URLS
    path('viewbaby/', views.babies, name='viewbaby'),
    path('addbaby/', views.createbaby, name='addbaby'),
    path('viewbaby/<int:id>', views.readbaby, name='readbaby'),
    path('editbaby/<int:id>', views.updatebaby, name='updatebaby'),
    path('deletebaby/<int:id>', views.deletebaby, name='deletebaby'),
    
    
    # SITTER URLS
    path('viewsitter/', views.sitter, name='viewsitter'),
    path('addsitter/', views.createsitter, name='addsitter'),
    path('viewsitter/<int:id>', views.readsitter, name='readsitter'),
    path('editsitter/<int:id>', views.updatesitter, name='updatesitter'),
    path('deletesitter/<int:id>', views.deletesitter, name='deletesitter'),
    path('assignsitter/<int:sitter_id>', views.assignsitter, name='assignsitter'),
    
    # INVENTORY
    path('inventory/', views.inventorysupply, name='inventory'),
    path('inventoryreciept/', views.inventoryreciept, name='inventoryreciept'),
]
# babycheckin
# babycheckout
# purchaseorder
# salesorder