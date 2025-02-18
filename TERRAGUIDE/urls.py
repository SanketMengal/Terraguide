from django.urls import path
from . import views

urlpatterns=[
    path('',views.homepage,name='show_homepage'),  
    path('home/',views.homepage,name='show_homepage'),  
    path('Gardnerlogin/',views.Gardnerlogin,name='Gardnerlogin'),
    path('Dwellerlogin/',views.Dwellerlogin,name='Dwellerlogin'),
    path('Adminlogin/',views.Adminlogin,name='Adminlogin'),
    # path('approve_Gardner/',views.approve_Gardner,name='approveGardner'),
    path('Gardnerlogout/',views.Gardnerlogout,name='Gardnerlogout'),
    path('Dwellerlogout/',views.Dwellerlogout,name='Dwellerlogout'),
    path('Adminlogout/',views.Adminlogout,name='Adminlogout'),

    path('process_Gardners/', views.process_Gardners, name='process_Gardners'),


    path('afterloginpage/',views.afterloginpage,name='show_loginpage'),
    path('get_offices_list/',views.get_offices_list, name='get_offices_list'),
    # path('addnewGardner/',views.addnewGardner, name='addnewGardner'),
    path('addnewGardner/',views.office_list_2, name='addnewGardner'),
    path('addnewDweller/',views.addnewDweller, name='addnewDweller'),
    path('new/',views.addnewGardner, name='new'),
    #path('Gardner_detail/',views.Gardner_detail, name='Gardner_detail'),
    path('change_Gardner_info/',views.change_Gardner_info, name='change_Gardner_info'),
    path('afterGardnerlogin/',views.afterGardnerlogin, name='afterGardnerlogin'),
    path('afterDwellerlogin/',views.afterDwellerlogin,name='afterDwellerlogin'),
    path('afterAdminlogin/',views.afterAdminlogin,name='afterAdminlogin'),
    path('change_Dweller_info/',views.change_Dweller_info, name='change_Dweller_info'),
    path('book_appointment/',views.book_appointment, name='book_appointment'),
    path('select_Gardner/',views.select_Gardner, name='select_Gardner'),
    path('show_pending_Gardners/',views.show_pending_Gardners, name='select_Gardner'),
    path('show_Gardner_info/',views.show_Gardner_info, name='show_Gardner_info'),
    path('show_Dweller_info/',views.show_Dweller_info, name='show_Dweller_info'),

    # path('change_Gardner_info/',views.change_Gardner_info, name='change_Gardner_info'),
    # path('get_Gardners_list/',views.get_Gardners_list, name='get_Gardners_list'),
    path('ask_Gardner_date_time/',views.ask_Gardner_date_time, name='ask_Gardner_date_time'),
    path('show_appointments/',views.show_appointments, name='show_appointments'),
    path('my_send_mail/',views.my_send_mail, name='my_send_mail'),
    # path('modify_offices/',views.modify_offices, name='modify_offices'),
    # path('approve_appointment/',views.approve_appointment, name='approve_appointment'),
    # path('new_appointment/',views.new_appointment, name='new_appointment'),
    ####################################
    path('office_list/', views.office_list, name='office_list'),
    path('offices/add/', views.office_add, name='office_add'),
    # path('office_edit?id=<int:pk>/', views.office_edit, name='office_edit'),
    path('office_edit/', views.office_edit, name='office_edit'),
    path('office_remove/', views.office_remove, name='office_remove'),
    # path('offices/<int:pk>/remove/', views.office_remove, name='office_remove'),
    #####################################
]

#########
# <td>
#                         <a href="{% url 'office_edit' office.pk %}">Edit</a> |
#                         <a href="{% url 'office_remove' office.pk %}">Remove</a>
#                     </td>