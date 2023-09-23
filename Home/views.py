from django.shortcuts import render,HttpResponseRedirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from num2words import num2words

# Create your views here.
def login_view(request):

    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = UserLogin(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                
                userObj = authenticate(username=uname, password=upass)
                if userObj is not None:
                    login(request, userObj)
                    # messages.success(request, 'Login successfully !')
                    return HttpResponseRedirect('/dashboard/')
        else:
            fm = UserLogin()
        return render(request, 'login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/dashboard/')



def logout_view(request):

    logout(request)

    return HttpResponseRedirect('/')

def dashboard(request):
    if request.user.is_authenticated:

        return render(request, 'dashboard.html')
    else:
        return HttpResponseRedirect('/')
    

# CLIENT MODEL FORM
def add_invoice(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            clientFm = ClientForm(request.POST)

            if clientFm.is_valid():

                comp = clientFm.cleaned_data['company_name']
                gst = clientFm.cleaned_data['gst_number']
                cntry = clientFm.cleaned_data['country']
                sts = clientFm.cleaned_data['state']
                add = clientFm.cleaned_data['address']

                obj = Client(company_name=comp, gst_number=gst,
                             country=cntry, state=sts, address=add)
                obj.save()

                messages.success(
                    request, "Your 'Client' form has been saved successfully.")

                clientFm = ClientForm()

        else:
            clientFm = ClientForm()

        return render(request, 'addinvoice.html', {'clientFm': clientFm})

    else:
        return HttpResponseRedirect('/')
    

# SERVICE MODEL FORM
def add_invoice2(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            serviceFm = ServicesForm(request.POST)
            if serviceFm.is_valid():
                cname = serviceFm.cleaned_data['client']
                ser = serviceFm.cleaned_data['description']
                qty = serviceFm.cleaned_data['quantity']
                amt = serviceFm.cleaned_data['amount']

                serObj = Services(client=cname, description=ser,
                                  quantity=qty, amount=amt)
                serObj.save()

                messages.success(
                    request, "Your 'Service' form has been saved successfully.")

                serviceFm = ServicesForm()
        else:
            serviceFm = ServicesForm()

        return render(request, 'addinvoice.html', {'serviceFm': serviceFm})

    else:
        return HttpResponseRedirect('/')
    

# SERVICE PROVIDER/COMPANY MODEL FORM & RENDERING ALL COMP. DETAIL
def company(request):
    allCompany = Company.objects.all()

    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = ServiceProviderForm(request.POST)
            if fm.is_valid():
                cnm = fm.cleaned_data['client']
                comp = fm.cleaned_data['company_name']
                hby = fm.cleaned_data['handle_by']
                em = fm.cleaned_data['email']
                ph = fm.cleaned_data['phone']
                acc = fm.cleaned_data['account_number']
                ifsc = fm.cleaned_data['ifsc_code']
                bnk = fm.cleaned_data['bank_name']
                gst = fm.cleaned_data['gst_number']

                obj = Company(client=cnm, company_name=comp, handle_by=hby, email=em, phone=ph,
                              account_number=acc, ifsc_code=ifsc, bank_name=bnk, gst_number=gst)
                obj.save()
                messages.success(
                    request, "Your form has been saved successfully.")
                fm = ServiceProviderForm()
        else:
            fm = ServiceProviderForm()

        return render(request, 'company.html', {'form': fm, 'data': allCompany})

    else:
        return HttpResponseRedirect('/')
    


# UPDAATE COMPANY DETAILS
def update_company(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            obj = Company.objects.get(pk=id)
            fm = ServiceProviderForm(request.POST, instance=obj)
            if fm.is_valid():
                fm.save()

                messages.success(
                    request, "Successfully updated, You can go back !")
        else:
            obj = Company.objects.get(pk=id)
            fm = ServiceProviderForm(instance=obj)

        return render(request, 'update_comp.html', {'form': fm})
    else:
        return HttpResponseRedirect('/')
    
    
# DELETE COMPANY
def delete_company(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            obj = Company.objects.get(pk=id)
            obj.delete()
        return HttpResponseRedirect('/company/')

    else:
        return HttpResponseRedirect('/')


# LIST OF ALL CLIENTS
def allList(request):
    if request.user.is_authenticated:

        allClient = Client.objects.all()

        return render(request, 'all_list.html', {'allClient': allClient})
    else:
        return HttpResponseRedirect('/')
    

# REVIEW INVOICE - SERVICE PROVIDER, CLIENT, SERVICES
def review(request, pk):
    if request.user.is_authenticated:

        clientData = Client.objects.get(id=pk)

        # code to handle if query/record not available
        try:
            companyData = Company.objects.get(client_id=pk)
        except Company.DoesNotExist:
            companyData = {'Key': 'Val'}

        try:
            servicesData = Services.objects.filter(client_id=pk)
        except Services.DoesNotExist:
            servicesData = {'Key': 'Val'}


        context = {'clientData': clientData,
                   'companyData': companyData, 'servicesData': servicesData}

        return render(request, 'review.html', context)

    else:
        return HttpResponseRedirect('/')

def report_list(request):
    if request.user.is_authenticated:

        allClient = Client.objects.all()

        return render(request, 'reportList.html', {'allClient': allClient})
    else:
        return HttpResponseRedirect('/')
    

# PDF REPORT
def pdf_report(request, pk):
    if request.user.is_authenticated:

        clientData = Client.objects.get(id=pk)
        try:
            companyData = Company.objects.get(client_id=pk)
        except Company.DoesNotExist:
            companyData = {'Key': 'Val'}

        try:
            servicesData = Services.objects.filter(client_id=pk)
        except Services.DoesNotExist:
            servicesData = {'Key': 'Val'}

        try:
            total_amt = []
            for i in servicesData:
                val = i.amount * i.quantity
                total_amt.append(val)

            total_amt2 = sum(total_amt)
            gst = 0.18  # GST 18%
            gst_amt = total_amt2 * gst
            price_with_gst = total_amt2 + (total_amt2 * gst)

            word_amt = num2words(price_with_gst, lang="en_IN")
            #print(num2words(price_with_gst, lang="en_IN"))

        except Exception as e:
            pass

        context = {'clientData': clientData, 'companyData': companyData, 'servicesData': servicesData, 'gst_amt': gst_amt, 'price_with_gst': price_with_gst, 'word_amt': word_amt, 'total_amt2':total_amt2}

        return render(request, 'pdfReport.html', context)

    else:
        return HttpResponseRedirect('/')
