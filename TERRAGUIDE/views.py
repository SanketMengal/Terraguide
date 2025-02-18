
from django.shortcuts import render,redirect,get_object_or_404
from django.forms.models import model_to_dict
from django.views import View
from django.http import HttpResponseBadRequest, JsonResponse
from datetime import date,timedelta
from django.core.mail import send_mail
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
#from corsheaders.decorators import cors_allow_all_origin
from django.contrib.auth.hashers import make_password, check_password
# from .serializers import Gardnerserializer,officeserializer,Dwellerserializer
from .models import office,Gardner,Dweller,appointments,bookedappointments,Admin,pending_Gardners
from .forms import GardnerForm , DwellerForm ,officeForm
from django.contrib.auth import logout
from django.views.decorators.cache import cache_control
from django.conf import settings 


def office_list(request):
    offices = office.objects.all()
    return render(request, 'office_list.html', {'offices': offices})

def office_add(request):
    if request.method == "POST":
        form = officeForm(request.POST)
        if form.is_valid():
            my_office = form.save(commit=False)
            my_office.save()
            messages.success(request,'Successfully added office')
            return redirect('office_list')
    else:
        form = officeForm()
    return render(request, 'office_add.html', {'form': form})

def office_edit(request):#, pk):
    # my_office = office.objects.filter(id=request.GET.get('id')) 
    my_office = office.objects.get(id=request.GET.get('id'))
    # my_office = get_object_or_404(office, pk=pk)
    if request.method == "POST":
        form = officeForm(request.POST, instance=my_office) #########
        if form.is_valid():
            my_office = form.save(commit=False)
            my_office.save()
            messages.success(request,'Successfully edited office details')
            return redirect('office_list')
    else:
        # form = officeForm(instance=office)
        form = officeForm(instance=my_office)
    return render(request, 'office_edit.html', {'form': form})

def office_remove(request):#, pk):
    my_office = office.objects.filter(id=request.GET.get('id'))
    # my_office = get_object_or_404(office, pk=pk)
    my_office.delete()
    messages.success(request,'Successfully deleted office')
    return redirect('office_list')

@csrf_exempt

def homepage(request):
    alert=True
    return render(request,'homePage.html',{'alert':alert}) 

def get_offices_list(request):
    queryset = office.objects.all()
    offices_list = [{'id': obj.id,'name':obj.name,'email':obj.email,'address':obj.address,'phone_number':obj.phone_number,'description':obj.description,'pincode':obj.pincode} for obj in queryset]
    return render(request,'get_offices_list.html',{'offices_list':offices_list})

def addnewGardner(request):
    # if request.method == 'POST':
    #     name=request.POST.get('name')
    #     gender=request.POST.get('gender')
    #     email=request.POST.get('email')
    #     # password=request.POST.get('password')
    #     hashed_password = make_password(request.POST.get('password'))
    #     phone=request.POST.get('phone')
    #     address=request.POST.get('address')
    #    # pincode=request.POST.get('pincode')
    #     age=request.POST.get('age')
    #     specialization=request.POST.get('specialization')
    #     experience=request.POST.get('experience')
    #     #pincode=request.POST.get('pincode')
    #     office_id = request.POST.get('office')
    #     my_office = office.objects.get(pk=office_id)
    #     context = {'my_office': my_office}
    #     # officeid=request.POST.get('officeid')
    #     #slotlist=request.POST.get('slotlist') 
    #     #certificate=request.POST.get('certificate')
    #     newGardner=pending_Gardners(name=name,email=email,password=hashed_password,gender=gender,phone_number=phone,address=address,specialization=specialization,experience=experience,age=age,officeid=my_office.id,pincode=my_office.pincode)
    #     newGardner.save()
    #     # response_data = {'success': 'Data was successfully saved.'}
    #     # # Return the response as a JSON-encoded string
    #     # return JsonResponse(response_data)
    #     # return render(request,'')
    #     # result = { 'name' : name , 'email' : email }
    #     # print(name + " " + newGardner('id'))
    #     # my_dict = {'name': name, 'id': newGardner.id }
    #     # request.session['my_dict'] = my_dict 
    #     request.session['my_dict.name'] = newGardner.name
    #     request.session['my_dict.id'] = newGardner.id 

    #     request.session['my_dict.specialization'] = newGardner.specialization
    #     request.session['my_dict.officeid'] = newGardner.officeid 

    #     # return render(request, 'add_Gardner.html', {'result': result})
    #     messages.success(request, 'Your account has been created successfully!,wait for admin approval')
    #     return redirect('/afterloginpage/') 
    #     # return render(request,'add_Gardner.html')

    # else:
    #     # If an error occurs, return an error response
    #     # response_data = {'error': 'An error occurred while saving the data: {}'.format(e)}
    #     # return HttpResponseBadRequest(json.dumps(response_data), content_type='application/json')
    #     # return redirect('/')
    #     return render(request,'add_Gardner.html') 
    if request.method == 'POST':
        x = 0 
        if request.POST.get('password') == request.POST.get('p2') :
            x = 1 
        hashed_password = make_password(request.POST.get('password'))
        hashed_p2 = make_password(request.POST.get('p2'))
        if hashed_password == hashed_p2 : 
            x = 1
        if x == 0 :
            messages.error(request, 'Passwords didnot match ') 
            return redirect('/addnewGardner/') 
        name=request.POST.get('name')
        gender=request.POST.get('gender')
        email=request.POST.get('email')
        # password=request.POST.get('password') 
        phone=request.POST.get('phone')
        address=request.POST.get('address')
       # pincode=request.POST.get('pincode')
        age=request.POST.get('age')
        specialization=request.POST.get('specialization')
        experience=request.POST.get('experience')
        # pdf_file = request.POST.get('pdf_file') 
        # pdf_file = request.FILES['pdf_file'].read()
        #pincode=request.POST.get('pincode')
        office_id = request.POST.get('office')
        my_office = office.objects.get(pk=office_id)
        context = {'my_office': my_office}

        if pending_Gardners.objects.filter(email=email).exists():
            messages.error(request, 'This email already exists.')
            return redirect('/addnewGardner/') 

        # if form.is_valid():
        #     print("Form is valid ") 
        # else : 
        #     messages.error(request, 'This username already exists.')
        #     return redirect('/addnewGardner/') 
        
        newGardner=pending_Gardners(name=name,email=email,password=hashed_password,gender=gender,phone_number=phone,address=address,specialization=specialization,experience=experience,age=age,officeid=my_office.id,pincode=my_office.pincode)#,pdf_file=pdf_file)
        newGardner.save()
        # response_data = {'success': 'Data was successfully saved.'}
        # # Return the response as a JSON-encoded string
        # return JsonResponse(response_data)
        # return render(request,'')
        # result = { 'name' : name , 'email' : email }
        # print(name + " " + newGardner('id'))
        # my_dict = {'name': name, 'id': newGardner.id }
        # request.session['my_dict'] = my_dict 
        request.session['my_dict.name'] = newGardner.name
        request.session['my_dict.id'] = newGardner.id 

        request.session['my_dict.specialization'] = newGardner.specialization
        request.session['my_dict.officeid'] = newGardner.officeid 

        # return render(request, 'add_Gardner.html', {'result': result})
        messages.success(request, 'Your account has been created successfully!')
        messages.success(request, 'Wait for admin approval') 
        return redirect('/Gardnerlogin/') 
         # return render(request,'add_Gardner.html')

    else:
        # If an error occurs, return an error response
        # response_data = {'error': 'An error occurred while saving the data: {}'.format(e)}
        # return HttpResponseBadRequest(json.dumps(response_data), content_type='application/json')
        # return redirect('/')
        return render(request,'add_Gardner.html') 



# def afterloginpage(request):
#     # print(request.name+""+request.email) 
#     info = request.session.get('my_dict.name' , 'my_dict.id') 
#     return render(request,'afterloginpage.html',{"info":info})   

def afterloginpage(request):
    name = request.session.get('my_dict.name', 'default_name')
    id = request.session.get('my_dict.id', 'default_id')
    specialization = request.session.get('my_dict.specialization', 'default_specialization')
    officeid = request.session.get('my_dict.officeid', 'default_officeid')
    info = {'name': name, 'id': id, 'specialization':specialization, 'officeid':officeid} 
    return render(request, 'afterloginpage.html', {"info": info})

def addnewDweller(request):
    # if request.method == 'POST':
    #     name=request.POST.get('name')
    #     gender=request.POST.get('gender')
    #     email=request.POST.get('email')
    #     # password=request.POST.get('password')
    #     hashed_password = make_password(request.POST.get('password'))
    #     phone=request.POST.get('phone')
    #     address=request.POST.get('address')
    #     pincode=request.POST.get('pincode')
    #     age=request.POST.get('age')
    #     # pincode=request.POST.get('pincode')
    #     description=request.POST.get('description') 
    #     newDweller=Dweller(name=name,email=email,password=hashed_password,gender=gender,phone_number=phone,address=address,age=age,description=description)
    #     newDweller.save()
    #     # response_data = {'success': 'Data was successfully saved.'}
    #     # # Return the response as a JSON-encoded string
    #     # return JsonResponse(response_data)
    #     # return render(request,'')
    #     # result = { 'name' : name , 'email' : email }
    #     # print(name + " " + newGardner('id'))
    #     # my_dict = {'name': name, 'id': newGardner.id }
    #     # request.session['my_dict'] = my_dict 
    #     request.session['my_dict.name'] = newDweller.name
    #     request.session['my_dict.id'] = newDweller.id
    #     # return render(request, 'add_docto
    #   
    if request.method == 'POST':
        x = 0 
        if request.POST.get('password') == request.POST.get('p2') :
            x = 1 
        hashed_password = make_password(request.POST.get('password'))
        hashed_p2 = make_password(request.POST.get('p2'))
        if hashed_password == hashed_p2 : 
            x = 1
        if x == 0 :
            messages.error(request, 'Passwords didnot match ') 
            return redirect('/addnewDweller/')  
        name=request.POST.get('name')
        gender=request.POST.get('gender')
        email=request.POST.get('email')
        # password=request.POST.get('password')
        # hashed_password = make_password(request.POST.get('password'))
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        pincode=request.POST.get('pincode')
        age=request.POST.get('age')
        # pincode=request.POST.get('pincode')
        description=request.POST.get('description') 
        # pdf_file = request.POST.get('pdf_file')
        # pdf_file = request.FILES['pdf_file'].read()

        if Dweller.objects.filter(email=email).exists():
            messages.error(request, 'This email already exists.')
            return redirect('/addnewDweller/') 
        # if form.is_valid():
        #     print("Form is valid ") 
        # else : 
        #     messages.error(request, 'This username already exists.')
        #     return redirect('/addnewGardner/') 
        newDweller=Dweller(name=name,email=email,password=hashed_password,gender=gender,phone_number=phone,address=address,age=age,description=description)#,pdf_file=pdf_file)
        newDweller.save() 
        request.session['my_dict.name'] = newDweller.name
        request.session['my_dict.id'] = newDweller.id
        # return render(request, 'add_Gardner.html', {'result': result})
        messages.success(request, 'Your account has been created successfully!')
        return redirect('/Dwellerlogin/') 
        # return render(request,'add_Gardner.html')

    else:
        # If an error occurs, return an error response
        # response_data = {'error': 'An error occurred while saving the data: {}'.format(e)}
        # return HttpResponseBadRequest(json.dumps(response_data), content_type='application/json')
        # return redirect('/')
        return render(request,'add_Dweller.html')   




def Gardnerlogin(request):
    if request.method == 'POST':
        email = request.POST['username'] 
        password = request.POST['password']
        try:
            my_Gardner = Gardner.objects.get(email=email) 
            if check_password(password, my_Gardner.password):
                # Password is correct, log in the user 
                # ... 
                print("Succesfully logged in !!")
                request.session['Gardner_name'] = my_Gardner.name
                request.session['Gardner_id'] = my_Gardner.id 
                messages.success(request, "Login successful" )
                return redirect('/afterGardnerlogin')
             
            else:
                # Password is incorrect, show an error message
                # ...
                print(" Incorrect Password") 
                # return redirect('/afterGardnerlogin')
                messages.error(request, "Incorrect password" ) 
                return render(request,'Gardner_login.html') 
        except Gardner.DoesNotExist:
            # User with the given email does not exist, show an error message
            # ...
            print(" Gardner with given email does not exist") 
            messages.error(request, "No account exist with given email" ) 
            return render(request,'Gardner_login.html') 
    else:
        # Render the login form
        # ... 
        return render(request,'Gardner_login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Gardnerlogout(request):
    logout(request)
    messages.success(request,'Succesfully logged out!')
    return redirect('Gardnerlogin')

def Dwellerlogin(request):
    if request.method == 'POST':
        email = request.POST['username'] 
        password = request.POST['password']
        try:
            my_Dweller = Dweller.objects.get(email=email) 
            if check_password(password,my_Dweller.password):
                # Password is correct, log in the user 
                # ... 
                print("Succesfully logged in !!")
                request.session['Dweller_id'] = my_Dweller.id 
                messages.success(request, "Login successful" )
                return redirect('/afterDwellerlogin') 
            else:
                # Password is incorrect, show an error message
                # ...
                print(" Incorrect Password  1111") 
                messages.error(request, "Incorrect password" ) 
                               # return redirect('/afterDwellerlogin') 

                return render(request,'Dweller_login.html') 
        except Dweller.DoesNotExist:
            # User with the given email does not exist, show an error message
            # ...
            print(" Dweller with given email does not exist") 
            messages.error(request, "No account exist with given email" ) 
            return render(request,'Dweller_login.html') 
    else:
        # Render the login form
        # ... 
        return render(request,'Dweller_login.html')  

def Adminlogout(request):
    logout(request)
    messages.success(request,'Succesfully logged out!')
    return redirect('Adminlogin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def Dwellerlogout(request):
    logout(request)
    messages.success(request,'Succesfully logged out!')

    return redirect('Dwellerlogin')

def afterDwellerlogin(request):
    my_id = request.session.get('Dweller_id', 'default_id') 
    if type(my_id)==str:
       return redirect('/Dwellerlogin')
    request.session['Dweller_id'] = request.session.get('Dweller_id', 'default_id')

    my_Dweller = Dweller.objects.get(id=my_id) 
    info = {'name': my_Dweller.name, 'id': my_Dweller.id} 
    return render(request, 'after_Dweller_login.html', {"info": info})

def office_list_2(request):
    offices = office.objects.all()
    context = {'offices': offices}
    return render(request, 'add_Gardner.html', context)

def afterGardnerlogin(request): 
    my_id = request.session.get('Gardner_id', 'default_id') 
    if type(my_id)==str:
       return redirect('/Gardnerlogin')
    d = Gardner.objects.get(id=my_id)
    my_Gardner = {'name':  d.name , 'id':d.id, 'age': d.age , 'phone_number': d.phone_number ,'email': d.email ,'address':d.address ,'experience':d.experience }
    request.session['Gardner_id'] = request.session.get('Gardner_id', 'default_id')
    return render(request,'after_Gardner_login.html',{'my_Gardner':my_Gardner})

def change_Gardner_info(request):
    my_id = request.session.get('Gardner_id', 'default_id') 
    if type(my_id)==str:
       return redirect('/Gardnerlogin')
    d = Gardner.objects.get(id=my_id)
    my_Gardner = {'name':  d.name , 'id':d.id, 'age': d.age , 'phone_number': d.phone_number ,'email': d.email ,'address':d.address ,'experience':d.experience }
    if request.method == 'POST':
        form = GardnerForm(request.POST)
        if form.is_valid():
            # Gardner_id = form.cleaned_data['my_id']
            Gardner_id = request.session.get('Gardner_id', 'default_id')
            my_Gardner = get_object_or_404(Gardner, pk=Gardner_id)
            form = GardnerForm(request.POST, instance=my_Gardner)
            form.save()
            messages.success(request,'Successfully changed your info')
            return redirect("/afterGardnerlogin") #('/Gardner_detail/')
    else:
        my_id = request.session.get('Gardner_id', 'default_id') 
        d = Gardner.objects.get(id=my_id)
        # my_Gardner = Gardner.objects.first() # Get the first Gardner instance as an example
        form = GardnerForm(instance=d)
    # return render(request, 'Gardner_detail.html', {'my_Gardner':my_Gardner,'form': form})
    return render(request, 'change_Gardner_info.html', {'my_Gardner': d, 'form': form})

def change_Dweller_info(request):
    my_id = request.session.get('Dweller_id', 'default_id') 
    if type(my_id)==str:
        return redirect('/Dwellerlogin')
    p = Dweller.objects.get(id=my_id)
    my_Dweller = {'name':  p.name , 'id':p.id, 'age': p.age , 'phone_number': p.phone_number ,'email': p.email ,'address':p.address ,'description':p.description }
    if request.method == 'POST':
        form = DwellerForm(request.POST)
        if form.is_valid():
            # Gardner_id = form.cleaned_data['my_id']
            Dweller_id = request.session.get('Dweller_id', 'default_id')
            my_Dweller = get_object_or_404(Dweller, pk=Dweller_id)
            form = DwellerForm(request.POST, instance=my_Dweller)
            form.save()
            messages.success(request,'Successfully changed your info')
            return redirect("/afterDwellerlogin") #('/Dweller_detail/')
    else:
        my_id = request.session.get('Dweller_id', 'default_id') 
        p = Dweller.objects.get(id=my_id)
        # my_Gardner = Gardner.objects.first() # Get the first Gardner instance as an example
        form = DwellerForm(instance=p)
    # return render(request, 'Gardner_detail.html', {'my_Gardner':my_Gardner,'form': form})
    return render(request, 'change_Dweller_info.html', {'my_Dweller': p, 'form': form})

def book_appointment(request):
    # if request.method == 'POST':
    id=request.session.get('Dweller_id','default-value')
    if type(id)==str:
        return redirect('/Dwellerlogin')
    print("entered with")
    print(type(id))
    # return render(request,'book_appointment.html')
    if request.method == 'POST':
        
        pincode = request.POST.get('pincode', None)
        specialization = request.POST.get('specialization', None)
    # pincode=123456
    # specialization="a"

    # ... add more fields as needed
    # office_ = office.objects.get(id=obj.officeid)


    # Building the queryset based on the conditions provided in the request
        queryset = Gardner.objects.all()
        if pincode:
            queryset = queryset.filter(pincode=pincode)
            if not queryset:       
                messages.warning(request, f"No Gardners found for pincode '{pincode}'. Please try a different pincode.")
                return redirect('/afterDwellerlogin/')
        if specialization:
            queryset = queryset.filter(specialization=specialization)
            queryset1 = queryset.filter(specialization=specialization)

            if not queryset1:       
                messages.warning(request, f"No Gardners found for specialization '{specialization}'. Please try a different specialization.")
                return redirect('/afterDwellerlogin/')

        # Converting the queryset to a list of dicts and returning as JSON response
        Gardners_list = []
        for obj in queryset:
            office_ = office.objects.get(id=obj.officeid)
            Gardners_list.append({
                'id': obj.id,
                'name': obj.name,
            # 'email': obj.email,
                'gender': obj.gender,
            # 'phone_number': obj.phone_number,
            # 'address': obj.address,
                'specialization': obj.specialization,
                'experience': obj.experience,
            # 'age': obj.age,
                'office_id':obj.officeid,
                'office_name': office_.name,
                'office_address': office_.address
            })
        # context={'Gardners_list':Gardners_list}
        request.session['Gardners_list'] = Gardners_list
        return redirect('/select_Gardner') 
    else:
        return render(request,'book_appointment.html') #,context)

def select_Gardner(request):
    print("select Gardner")
    if request.method == 'POST':
        print("entered if select")
        date= request.POST.get('date', '') # get the date from the query parameters
        slot= request.POST.get('slot', '') # get the id from the query parameters
        description=request.POST.get('description', '')
        appointment_preference=request.POST.get('appointment_preference', '')
        Gardner_id=request.POST.get('selected_Gardner_id', '')
        Dweller_id=request.session.get('Dweller_id')
        new_booking=bookedappointments(date=date,slot=slot,Gardnerid=Gardner_id,Dwellerid=Dweller_id,description=description,appointment_preference=appointment_preference,time='00:00')
        new_booking.save()
        if appointments.objects.filter(Gardnerid=Gardner_id,date=date):
            Gardner_appointments=appointments.objects.get(Gardnerid=Gardner_id,date=date)
            if slot=="morning":
                Gardner_appointments.morning.append(new_booking.bookingid)
            elif slot=="afternoon":
                Gardner_appointments.afternoon.append(new_booking.bookingid)
            else :
                Gardner_appointments.evening.append(new_booking.bookingid)
        else:
            Gardner_appointments=appointments(Gardnerid=Gardner_id,date=date)
            if slot=="morning":
                Gardner_appointments.morning.append(new_booking.bookingid)
            elif slot=="afternoon":
                Gardner_appointments.afternoon.append(new_booking.bookingid)
            else :
                Gardner_appointments.evening.append(new_booking.bookingid)
        Gardner_appointments.save()
        messages.success(request, f"appointment booked on '{date}' for the slot {slot}. Please wait for Gardner's response mail.")
        print("beforeafter pat login")
        return redirect('/afterDwellerlogin/')
    else:
        Gardners_list = request.session.get('Gardners_list')
        context={'Gardners_list':Gardners_list}
        print("else in select Gardner")
        return render(request,'select_Gardner.html',context)

##########################################################
def ask_Gardner_date_time(request):
    if request.method == 'POST':
        my_date = request.POST.get('date','')
        slot = request.POST.get('slot','') 
        request.session['date'] = my_date
        request.session['slot'] = slot

        request.session['Gardner_id'] = request.session.get('Gardner_id')
        print("Exiting ask Gardner function")
        return redirect('/show_appointments') 
    else:
        today = date.today().strftime("%Y-%m-%d")
        seven_days_from_now = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
        selected_date = request.POST.get('date')
        context = {
            'today': today,
            'seven_days_from_now': seven_days_from_now
        }
        return render(request,'ask_Gardner_date_time.html',context) 

def show_appointments(request):
    if request.method == 'POST':
        # selected_options = request.POST.getlist('option')
        # for option in selected_options:
        #     print(option) 
        Gardner_id = request.session.get('Gardner_id') 
        if type(Gardner_id)==str:
            return redirect('/Dwellerlogin')
        my_date = request.session.get('date') 
        slot = request.session.get('slot')
        if bookedappointments.objects.filter(Gardnerid=Gardner_id,date=my_date,slot=slot,status='no action taken'):
            for b in bookedappointments.objects.filter(Gardnerid=Gardner_id,date=my_date,slot=slot,status='no action taken'):
                option = request.POST.get('option_' + str(b.bookingid)) 
                time = request.POST.get('time_' + str(b.bookingid))
                msg = request.POST.get('msg_'+str(b.bookingid)) 
                  # print('Booking ID:', b.bookingid, 'Selected option:', option)
                b.status = option 
                b.time=time
                b.save()
                Dwellerid = b.Dwellerid 
                pat = Dweller.objects.get(id=Dwellerid) 
                email = pat.email
                # print("***show appointments ****") 
                # print(time,email) 
                # print("***show appointments ****")
                # val = {
                #     'Dwellerid' : Dwellerid ,
                #     'email' : pat.email ,
                #     'time' : time ,
                # } 
                # print(b.status) 
                if option == 'offline':
                    # print("Entered option = offline")
                    # offline = request.session.get('offline', [])  
                    # offline.append( (time,email) ) 
                    # request.session['offline'] = offline 
                    # request.session['offline'] =request.session.get('offline',[]).append((time,email)) 
                    request.session.setdefault('offline', []).append((time,email,msg))
                elif option == 'online':
                    request.session.setdefault('online', []).append((time,email,msg))
                elif option == 'decline':
                    request.session.setdefault('decline', []).append((time,email,msg))

            request.session['my_date'] = my_date 
            request.session['slot'] = slot 
            request.session['Gardner_id'] = Gardner_id 
            # print("going to redirect ") 
            return redirect('/my_send_mail')  

        else:
            print("No Pending Appointments :(  :(") 
            return redirect('/afterGardnerlogin') 
    else:
        Gardner_id = request.session.get('Gardner_id') 
        my_date = request.session.get('date') 
        slot = request.session.get('slot') 
        inf = {
            'd' : my_date,
            's' : slot,
        }
        

        print(Gardner_id , my_date , slot) 
        completed_appointments = bookedappointments.objects.filter(Gardnerid=Gardner_id,date=my_date,slot=slot).exclude(status='no action taken')

        if bookedappointments.objects.filter(Gardnerid=Gardner_id,date=my_date,slot=slot):
            b = bookedappointments.objects.filter(Gardnerid=Gardner_id,date=my_date,slot=slot,status='no action taken')
            return render(request,'show_appointments.html',{'b':b, 'completed_appointments':completed_appointments , 'inf':inf})
        else:
            print("No appointments :( ") 
            return redirect('/afterGardnerlogin') 

def my_send_mail(request):
    offline_Dwellers = request.session.get('offline') 
    online_Dwellers = request.session.get('online') 
    decline_Dwellers = request.session.get('decline') 

    # print("Entered my_send_mail : ") 

    if offline_Dwellers:
        # print("Entered if: ")
        for time,email,msg in request.session.get('offline') :
            # print("OFFLINE SENDING")
            # time = p['time']  # access the 'time' attribute of the dictionary
            # email = p['email']
            # time = p[0]
            # email = p[1] 
            subject = 'TERRAGUIDE Confirmation'
            message = 'Your offline appointment is confirmed at ' + time + ('. Gardner message : ' + msg if msg != '' else '' )
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email] 
            # print("******")
            # # print(p) 
            # print(settings.DEFAULT_FROM_EMAIL)
            # print(recipient_list) 
            # print(time) 
            # print("******")
        
            send_mail(subject, message, from_email, recipient_list)
    
    if online_Dwellers:
        for time,email,msg in request.session.get('online') :
            subject = 'TERRAGUIDE Confirmation'
            message = 'This project is Develope By Akanksha and Esha from MCA department'
            #from_email = settings.DEFAULT_FROM_EMAIL
            #recipient_list = [email]      
            #send_mail(subject, message, from_email, recipient_list)

    if decline_Dwellers:
        for time,email,msg in request.session.get('decline') :
            subject = 'TERRAGUIDE Declination' 
            message = 'Sorry! Your appointment is declined'+ ('. Gardner message : ' + msg if msg != '' else '')
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email] 
            send_mail(subject, message, from_email, recipient_list)

    request.session.pop('offline', None)
    request.session.pop('online', None)
    request.session.pop('decline', None) 
    return redirect('/afterGardnerlogin') 



# def change_Gardner_info(request):
#     return render(request,'Gardner_detail.html',{'my_Gardner':my_Gardner})

# def Gardner_detail(request):
#     if request.method == 'POST':
#         form = GardnerForm(request.POST)
#         if form.is_valid():
#             Gardner_id = form.cleaned_data['Gardner_id']
#             my_Gardner = get_object_or_404(Gardner, pk=Gardner_id)
#             form = GardnerForm(request.POST, instance=my_Gardner)
#             form.save()
#             return HttpResponseRedirect('/Gardner_detail/')
#     else:
#         my_Gardner = Gardner.objects.first() # Get the first Gardner instance as an example
#         form = GardnerForm(instance=my_Gardner)
#     return render(request, 'Gardner_detail.html', {'form': form})

def show_Gardner_info(request):
    my_id = request.session.get('Gardner_id', 'default_id')
    if type(my_id)==str:
       return redirect('/Gardnerlogin') 
    d = Gardner.objects.get(id=my_id)
    my_Gardner = {'name':  d.name , 'id':d.id, 'age': d.age , 'phone_number': d.phone_number ,'email': d.email ,'address':d.address ,'experience':d.experience }
    form = GardnerForm(instance=d)
    return render(request, 'show_Gardner_info.html', {'my_Gardner': d, 'form': form})

def show_Dweller_info(request):
    my_id = request.session.get('Dweller_id', 'default_id') 
    if type(my_id)==str:
       return redirect('/Dwellerlogin')
    d = Dweller.objects.get(id=my_id)
    my_Dweller = {'name':  d.name , 'id':d.id, 'age': d.age , 'phone_number': d.phone_number ,'email': d.email ,'address':d.address ,'description':d.description }
    form = DwellerForm(instance=d)
    return render(request, 'show_Dweller_info.html', {'my_Dweller': d, 'form': form})

# @csrf_exempt
# @cors_allow_all_origin
# def change_Gardner_info(request):
#     id = request.POST.get('id', '') # get the id from the query parameters
#     Gardner=get_object_or_404(Gardner,id=id)
#     if not Gardner:
#         return JsonResponse({'error': f"No Gardner found with id '{id}'."})
#     for key in request.POST:
#         if key != 'id':
#             setattr(Gardner, key, request.POST.get(key))
#     Gardner.save()
#     return JsonResponse({'success': f"Gardner with ID '{id}' updated successfully."})

# @csrf_exempt
# @cors_allow_all_origin

# def get_Gardners_list(request):
#     # # Retrieve the query parameters from the request
#     # pincode = request.POST.get('pincode', None)
#     # specialization = request.POST.get('specialization', None)
#     # ... add more fields as needed


#     # Building the queryset based on the conditions provided in the request
#     queryset = Gardner.objects.all()
#     # if pincode:
#     #     queryset = queryset.filter(pincode=pincode)
#     #     if not queryset:       
#     #         return JsonResponse({'message': 'No Gardners found based on your location '})

#     # if specialization:
#     #     queryset = queryset.filter(specialization=specialization)
#     #     queryset1 = queryset.filter(specialization=specialization)

#     #     if not queryset1:       
#     #         return JsonResponse({'message': 'No Gardners found with given specialization in your location.'})

#     #     # Converting the queryset to a list of dicts and returning as JSON response

#     objects_list = [{'id': obj.id,'name':obj.name,'email':obj.email,'gender':obj.gender,'phone_number':obj.phone_number,'address':obj.address,'specialization':obj.specialization,'experience':obj.experience,'age':obj.age,'officeid':obj.officeid} for obj in queryset]
#     return JsonResponse({'objects': objects_list})

# @csrf_exempt
# @cors_allow_all_origin
# def show_appointments(request):
#     # id = request.POST.get('id', None)
#     # date = request.POST.get('date', None)   
#     # appointmentslist=appointments.objects.get(id=id,date=date)

#     # morningappointments=appointmentslist.morning
#     # afternoonappointments=appointmentslist.afternoon
#     # eveningappointments=appointmentslist.evening
#     # data={
#     #     'morningappointments':morningappointments,
#     #     'afternoonappointments':afternoonappointments,
#     #     'eveningappointments':eveningappointments
#     # }
#     queryset = appointments.objects.all()
#     obj_list=[{'morningappointments': obj.morningtoken ,'afternoonappointments': obj.afternoontoken,'eveningappointments': obj.eveninggtoken}for obj in queryset]
#     return JsonResponse(obj_list)


# @csrf_exempt
# @cors_allow_all_origin
# def approve_appointment(request):
#     # Retrieve the query parameters from the request
#     bookingid = request.POST.get('bookingid', None)
#     date = request.POST.get('date', None)
#     Dwellerid=request.POST.get('Dwellerid',None)
#     Gardnerid=request.POST.get('Gardnerid',None)
#     description=request.POST.get('description',None)
#     status=request.POST.get('status',None)
#     Dweller=Dweller.objects.get(id=Dwellerid)
#     if status=='confirm' :
#         subject = 'Your Subject Here'
#         message = f'Hello {Dweller.email},\n\nThis is your email message in the specified format.'
#         #########!!!!!!!!!!!!!update the info about appointment confirmation
#         from_email = 'your-email@example.com'
#         recipient_list = [Dweller.email]
#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     elif status=='decline':
#         subject = 'Your Subject Here'
#         message = f'Hello {Dweller.email},\n\nThis is your email message in the specified format.'
#         #########!!!!!!!!!!!!!update the info about declination
#         from_email = 'your-email@example.com'
#         recipient_list = [Dweller.email]
#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     elif status=='online consultation':
#         subject = 'Your Subject Here'
#         message = f'Hello {Dweller.email},\n\nThis is your email message in the specified format.'
#         #########!!!!!!!!!!!!!update the info about online consultation
#         from_email = 'your-email@example.com'
#         recipient_list = [Dweller.email]
#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     # morning_no_of_appointments=request.POST.get('morning', None)
#     # afternoon_no_of_appointments=request.POST.get('afternoon', None)
#     # evening_no_of_appointments=request.POST.get('evening', None)
#     # if date< date.today():
#     #     error_message = {'error': 'you cannot approve an appointment on past dates.'}
#     #     return JsonResponse(error_message, status=400)
#     # elif appointments.objects.filter(id=id,date=date).exists():
#     #     appointmentslist=appointments.objects.get(id=id,date=date)
#     #     i=0
#     #     while i<=morning_no_of_appointments and i<=len(appointmentslist.morning):
#     #         id=appointmentslist.morning[i]
#     #         Dweller_=Dweller.objects.get(id=id)
#     #         subject = 'Your Subject Here'
#     #         message = f'Hello {Dweller_.email},\n\nThis is your email message in the specified format.'
#     #         #########!!!!!!!!!!!!!update the info about appointment confirmation
#     #         from_email = 'your-email@example.com'
#     #         recipient_list = [Dweller_.email]
#     #         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     #         i=i+1
#     #     while i<=len(appointmentslist.morning):
#     #         id=appointmentslist.morning[i]
#     #         Dweller_=Dweller.objects.get(id=id)
#     #         subject = 'Your Subject Here'
#     #         message = f'Hello {Dweller_.email},\n\nThis is your email message in the specified format.'
#     #         #########!!!!!!!!!!!!!update the info for declination of appointment
#     #         from_email = 'your-email@example.com'
#     #         recipient_list = [Dweller_.email]
#     #         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     #         i=i+1
#     #     i=0
#     #     while i<=afternoon_no_of_appointments and i<=len(appointmentslist.afternoon):
#     #         id=appointmentslist.afternoon[i]
#     #         Dweller_=Dweller.objects.get(id=id)
#     #         subject = 'Your Subject Here'
#     #         message = f'Hello {Dweller_.email},\n\nThis is your email message in the specified format.'
#     #         #########!!!!!!!!!!!!!update the info about apointment confirmation
#     #         from_email = 'your-email@example.com'
#     #         recipient_list = [Dweller_.email]
#     #         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     #         i=i+1
#     #     while i<=len(appointmentslist.afternoon):
#     #         id=appointmentslist.afternoon[i]
#     #         Dweller_=Dweller.objects.get(id=id)
#     #         subject = 'Your Subject Here'
#     #         message = f'Hello {Dweller_.email},\n\nThis is your email message in the specified format.'
#     #         #########!!!!!!!!!!!!!update the info for declination of appointment
#     #         from_email = 'your-email@example.com'
#     #         recipient_list = [Dweller_.email]
#     #         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     #         i=i+1
#     #     i=0
#     #     while i<=evening_no_of_appointments and i<=len(appointmentslist.evening):
#     #         id=appointmentslist.evening[i]
#     #         Dweller_=Dweller.objects.get(id=id)
#     #         subject = 'Your Subject Here'
#     #         message = f'Hello {Dweller_.email},\n\nThis is your email message in the specified format.'
#     #         #########!!!!!!!!!!!!!update the info about apointment confirmation
#     #         from_email = 'your-email@example.com'
#     #         recipient_list = [Dweller_.email]
#     #         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     #         i=i+1
#     #     while i<=len(appointmentslist.evening):
#     #         id=appointmentslist.evening[i]
#     #         Dweller_=Dweller.objects.get(id=id)
#     #         subject = 'Your Subject Here'
#     #         message = f'Hello {Dweller_.email},\n\nThis is your email message in the specified format.'
#     #         #########!!!!!!!!!!!!!update the info for declination of appointment
#     #         from_email = 'your-email@example.com'
#     #         recipient_list = [Dweller_.email]
#     #         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     #         i=i+1
#     #     return JsonResponse({'message': 'mails sent for confirmation and declination for 3 slots respectively'})

#     # else:
#     #     return JsonResponse({'message': 'No appointments for you on the given date'})


# # @csrf_exempt
# # @cors_allow_all_origin

# # def addnewDweller(request):
# #     try:
# #         name=request.POST.get('name')
# #         gender=request.POST.get('gender')
# #         email=request.POST.get('email')
# #         phone=request.POST.get('phone')
# #         address=request.POST.get('address')
# #         pincode=request.POST.get('pincode')
# #         age=request.POST.get('age')
# #         description=request.POST.get('description')
# #         newDweller=Dweller(name=name,email=email,gender=gender,phone_number=phone,address=address,description=description,pincode=pincode,age=age)
# #         newDweller.save()
# #         # response_data = {'success': 'Data was successfully saved.'}
# #         # Return the response as a JSON-encoded string
# #         # return JsonResponse(response_data)
# #         return redirect('/')

# #     except Exception as e:
# #         # If an error occurs, return an error response
# #         response_data = {'error': 'An error occurred while saving the data: {}'.format(e)}
# #         return HttpResponseBadRequest(json.dumps(response_data), content_type='application/json')

# # @csrf_exempt
# # @cors_allow_all_origin


# # @csrf_exempt
# # @cors_allow_all_origin

# # def change_Dweller_info(request):
# #     id = request.POST.get('id', '') # get the id from the query parameters
# #     Dweller=get_object_or_404(Dweller,id=id)
# #     if not Dweller:
# #         return JsonResponse({'error': f"No Dweller found with id '{id}'."})
# #     for key in request.POST:
# #         if key != 'id':
# #             setattr(Dweller, key, request.POST.get(key))
# #     Dweller.save()
# #     return JsonResponse({'success': f"Dweller with ID '{id}' updated successfully."})

# #################################check below class

# # @csrf_exempt
# @cors_allow_all_origin
# def new_appointment(request):
#     id = request.POST.get('id', '') # get the id from the query parameters
#     date= request.POST.get('date', '') # get the date from the query parameters
#     slot= request.POST.get('slot', '') # get the id from the query parameters
#     description=request.POST.get('description', '')
#     if date< date.today():
#             error_message = {'error': 'you cannot book an appointment on past dates.'}
#             return JsonResponse(error_message, status=400)

#     elif appointments.objects.filter(id=id,date=date).exists():
#         appointmentslist=appointments.objects.get(id=id,date=date)
#         if (slot=='morning'):
#             appointmentslist.morning.append(id)
#             return JsonResponse({'message': 'appointment booked for the given slot,wait for the confirmation email from Gardner'})
        
#         elif slot=='afternoon':
#             if len(appointmentslist.afternoon)<10:
#                 appointmentslist.afternoon.append(id)
#                 return JsonResponse({'message': 'appointment booked for the given slot,wait for the confirmation email from Gardner'})
#             else:
#                 return JsonResponse({'error': 'sorry,the slot is full,try for another slot'})
#         elif (slot=='evening'):
#             if len(appointmentslist.evening)<10:
#                 appointmentslist.evening.append(id)
#                 return JsonResponse({'message': 'appointment booked for the given slot,wait for the confirmation email from Gardner'})
#             else:
#                 return JsonResponse({'error': 'sorry,the slot is full,try for another slot'})
#     else:
#         appointmentslist=appointments(id=id,date=date)
#         if (slot=='morning'):
#             if len(appointmentslist.morning)<10:
#                 appointmentslist.morning.append(id)
#                 return JsonResponse({'message': 'appointment booked for the given slot,wait for the confirmation email from Gardner'})
#             else:
#                 return JsonResponse({'error': 'sorry,the slot is full,try for another slot'})
#         elif (slot=='afternoon'):
#             if len(appointmentslist.afternoon)<10:
#                 appointmentslist.afternoon.append(id)
#                 return JsonResponse({'message': 'appointment booked for the given slot,wait for the confirmation email from Gardner'})
#             else:
#                 return JsonResponse({'error': 'sorry,the slot is full,try for another slot'})
#         elif (slot=='evening'):
#             if len(appointmentslist.evening)<10:
#                 appointmentslist.evening.append(id)
#                 return JsonResponse({'message': 'appointment booked for the given slot,wait for the confirmation email from Gardner'})
#             else:
#                 return JsonResponse({'error': 'sorry,the slot is full,try for another slot'})


def Adminlogin(request):
    if request.method == 'POST':
        email = request.POST['username'] 
        password = request.POST['password']
        try:
            my_Admin = Admin.objects.get(email=email) 
            if check_password(password, make_password(my_Admin.password)):
                # Password is correct, log in the user 
                # ... 
                print("Succesfully logged in !!")
                request.session['my_id'] = my_Admin.id
                # context={'Gardners_list':Gardners_list}
                messages.success(request,'Succesfully logged in!') 
                return redirect('/afterAdminlogin')
             
            else:
                # Password is incorrect, show an error message
                # ...
                messages.error(request,'Incorrect password!')
                print(" Incorrect Password") 
                # return redirect('/afterGardnerlogin')

                return render(request,'Admin_login.html') 
        except Admin.DoesNotExist:
            # User with the given email does not exist, show an error message
            # ...
            messages.error(request,'No account exists with given email!')
            print(" Admin with given email does not exist") 
            return render(request,'Admin_login.html') 
    else:
        # Render the login form
        # ... 
        return render(request,'Admin_login.html')

def afterAdminlogin(request):

    my_id = request.session.get('my_id', 'default_id') 
    if type(my_id)==str:
       return redirect('/Adminlogin')
    print("Entered after admin login")
    if request.method=='POST':
        print("Entered if")
        return redirect('Adminlogin')
    else:
        print("Entered else")
        my_id = request.session.get('my_id', 'default_id') 
        request.session['my_id'] = my_id

        pending_Gardners_=pending_Gardners.objects.all()
        pending_Gardners_list = []
        for obj in pending_Gardners_:
            # pending_Gardner = pending_Gardners.objects.get(id=obj.id)
            pending_Gardners_list.append({
                'id': obj.id,
                'name': obj.name,
                'email': obj.email,
                'gender': obj.gender,
                'password': obj.password,
                'phone_number': obj.phone_number,
                'address': obj.address,
                'specialization': obj.specialization,
                'experience': obj.experience,
                'age': obj.age,
                'pincode': obj.pincode,
                'office_id':obj.officeid,
                'isdelete':obj.isdelete
                ########################certificate!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
            })
        my_Admin = Admin.objects.get(id=my_id) 
        info = {'name': my_Admin.name, 'id': my_Admin.id, 'pending_Gardners_list': pending_Gardners_list} 
        return render(request, 'after_Admin_login.html', {"info": info})
    # else:


def show_pending_Gardners(request):
    my_id = request.session.get('my_id', 'default_id') 
    if type(my_id)==str:
        return redirect('/Adminlogin')
    print("Entered after admin login")
    if request.method=='POST':
        print("Entered if")
        return redirect('Adminlogin')
    else:
        print("Entered else")
        my_id = request.session.get('my_id', 'default_id') 
        request.session['my_id'] = my_id

        pending_Gardners_=pending_Gardners.objects.all()
        pending_Gardners_list = []
        for obj in pending_Gardners_:
            # pending_Gardner = pending_Gardners.objects.get(id=obj.id)
            pending_Gardners_list.append({
                'id': obj.id,
                'name': obj.name,
                'email': obj.email,
                'gender': obj.gender,
                'password': obj.password,
                'phone_number': obj.phone_number,
                'address': obj.address,
                'specialization': obj.specialization,
                'experience': obj.experience,
                'age': obj.age,
                'pincode': obj.pincode,
                'office_id':obj.officeid,
                'isdelete':obj.isdelete
                ########################certificate!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
            })
        my_Admin = Admin.objects.get(id=my_id) 
        info = {'name': my_Admin.name, 'id': my_Admin.id, 'pending_Gardners_list': pending_Gardners_list} 
        return render(request, 'show_pending_Gardners.html', {"info": info})
# def approve_Gardner(request,Gardner_id):
#     Gardner = get_object_or_404(pending_Gardners, id=Gardner_id)
#     newGardner=Gardner(name=Gardner.name,email=Gardner.email,password=Gardner.password,gender=Gardner.gender,phone_number=Gardner.phone_number,address=Gardner.address,specialization=Gardner.specialization,experience=Gardner.experience,age=Gardner.age,officeid=Gardner.officeid,pincode=Gardner.pincode)
#     newGardner.save()
#     Gardner.delete()
#     return redirect('/afterAdminlogin')


# def process_Gardners(request):
#     my_id = request.session.get('my_id', 'default_id') 
#     if type(my_id)==str:
#        return redirect('/Adminlogin')
#     request.session['my_id'] = my_id
    
#     if request.method == 'POST':
#         selected_options = request.POST.dict()
#         for Gardner_id, action in selected_options.items():
#             if action == 'approve':
#                 id=Gardner_id[7]
#                 print("Gardner id:")
#                 print(id)
#                 pending_Gardner = get_object_or_404(pending_Gardners, id=id)
#                 newGardner = Gardner(name=pending_Gardner.name, email=pending_Gardner.email, password=pending_Gardner.password, gender=pending_Gardner.gender, phone_number=pending_Gardner.phone_number, address=pending_Gardner.address, specialization=pending_Gardner.specialization, experience=pending_Gardner.experience, age=pending_Gardner.age, officeid=pending_Gardner.officeid, pincode=pending_Gardner.pincode)
#                 newGardner.save()
#                 pending_Gardner.delete()

#                 print("approve_Gardner in views")
#             elif action == 'decline':
#                 id=Gardner_id[7]
#                 print("Gardner id:")
#                 print(id)
#                 pending_Gardner=pending_Gardners(id=id)
#                 pending_Gardner.delete()
#                 print("decline_Gardner in views")
                
#                 # Perform the action for the Gardner with the given ID
#                 # e.g. decline_Gardner(Gardner_id)
#             else:
#                 # Perform the action for the Gardner with the given ID
#                 # e.g. do_nothing_with_Gardner(Gardner_id)
#                 print("nothing selected")
#         return redirect('/afterAdminlogin')

def process_Gardners(request):
    my_id = request.session.get('my_id', 'default_id') 
    request.session['my_id'] = my_id

    if request.method == 'POST':
        selected_options = request.POST.dict()
        # d = pending_Gardner.objects.all() 
        for Gardner_id, action in selected_options.items():
            if action == 'approve':
                id=int(Gardner_id[7:])
                # id = request.POST.get('action_' + str(Gardner_id)) 
                # time = request.POST.get('time_' + str(b.bookingid))

                print("Gardner id:")
                print(id)
                pending_Gardner = get_object_or_404(pending_Gardners, id=id)
                newGardner = Gardner(name=pending_Gardner.name, email=pending_Gardner.email, password=pending_Gardner.password, gender=pending_Gardner.gender, phone_number=pending_Gardner.phone_number, address=pending_Gardner.address, specialization=pending_Gardner.specialization, experience=pending_Gardner.experience, age=pending_Gardner.age, officeid=pending_Gardner.officeid, pincode=pending_Gardner.pincode)
                newGardner.save()

                subject = 'TERRAGUIDE Confirmation'
                message = 'Congrats!! Your (Gardner)request is approved ' 
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [pending_Gardner.email]      
                # if pending_Gardner:
                send_mail(subject, message, from_email, recipient_list)
                # else:
                    # print("***************") 
                print("approve_Gardner in views")

                pending_Gardner.delete()

            elif action == 'decline':
                id=int(Gardner_id[7:])
                # id = request.POST.get('action_' + str(Gardner_id)) 
                # status = request.POST.get('action_' + str(Gardner_id)) 
                print("Gardner id:")
                print(id) 
                # pending_Gardner=pending_Gardners(id=id)
                pending_Gardner = get_object_or_404(pending_Gardners, id=id) 
                
                print("decline_Gardner in views")
                
                subject = 'TERRAGUIDE Declination'
                message = 'Sorry!! Your (Gardner)request is rejected ' 
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [pending_Gardner.email] 
                print(recipient_list) 
                # if pending_Gardner:
                send_mail(subject, message, from_email, recipient_list)
                # else:
                    # print("***************")      
                # send_mail(subject, message, from_email, recipient_list)
                print("Mail sent in decline_Gardner in views")

                pending_Gardner.delete() 
                # Perform the action for the Gardner with the given ID
                # e.g. decline_Gardner(Gardner_id)
            else:
                # Perform the action for the Gardner with the given ID
                # e.g. do_nothing_with_Gardner(Gardner_id)
                print("nothing selected")
        return redirect('/afterAdminlogin')
# def modify_offices(request):
#     if request.method == 'POST':
#         print("**")
#     else:
#         return render(request,'office_list.html')        