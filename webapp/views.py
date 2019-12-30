from .forms import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import *
from django.http import *
from django.core.files.storage import FileSystemStorage


def login_view(request):
    user = None
    app_user = None
    message = None
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        #print(user.is_superuser)
        if user.is_superuser:
            login(request, user)
            return redirect('webapp:home')
        else:
            if user is not None:
                app_user = AppUser.objects.get(user=user)
                login(request, user)
                return redirect('webapp:home')

    context = {
        'form': form,
        'user': user,
        'appuser': app_user,
    }
    return render(request, "webapp/login.html", context)

def logout_view(request):
    logout(request)
    return redirect('webapp:login')


def home_view(request):
    if request.user.is_superuser:
        context = {}
    else :
        if request.user.is_authenticated:
            try:
                appuser = AppUser.objects.get(user=request.user)
            except AppUser.DoesNotExist:
                raise Http404('Object Appuser does not exist!')
            context = {
                'appuser' : appuser
            }
    return render(request, "webapp/index.html", context)


@login_required
def add_profile_view(request):
    print(request.method)

    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = ExtendedUserCreationForm(request.POST or None)
    profile_form = UserProfileForm(request.POST or None)

    if form.is_valid() and profile_form.is_valid():
        user = form.save()
        print("USER: ",user)
        profile = profile_form.save(commit=False)

        profile.user = user
        print("PROFILE: ", profile)
        profile.save()

        type = profile_form.cleaned_data.get('type')

        if type == 'A':
            user = User.objects.get(username=form.cleaned_data.get('username'))
            mygroup, created = Group.objects.get_or_create(name='Admin')
            mygroup.user_set.add(user)
            mygroup.save()

        if type == 'M':
            user = User.objects.get(username=form.cleaned_data.get('username'))
            mygroup, created = Group.objects.get_or_create(name='Medic')
            mygroup.user_set.add(user)
            mygroup.save()

        if type == 'S':
            user = User.objects.get(username=form.cleaned_data.get('username'))
            mygroup, created = Group.objects.get_or_create(name='Secretary')
            mygroup.user_set.add(user)
            mygroup.save()

            form = ExtendedUserCreationForm()
            profile_form = UserProfileForm()
            messages.success(request, 'User registration succefully')

    else:
        messages.error(request, 'User registration unsuccefully')
        form = ExtendedUserCreationForm()
        profile_form = UserProfileForm()

    context = {
        'form': form,
        'profile_form': profile_form,
        'appuser': appuser
    }

    return render(request, "webapp/add_profile.html", context)


@login_required
def add_pacient_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = PacientForm(request.POST)
    if form.is_valid():
        form.save()
        form = PacientForm()
        messages.success(request, 'Pacient registration succefully')
    else:
        messages.error(request, 'Pacient registration unsuccefully')
    context = {
        'form': form,
        'appuser' : appuser
    }

    return render(request, "webapp/add_pacient.html", context)


@login_required
def add_drug_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = DrugForm(request.POST)
    if form.is_valid():
        form.save()
        form = DrugForm()
        messages.success(request, 'Drug registration succefully')
    else:
        messages.error(request, 'Drug registration unsuccefully')
    context = {
        'form': form,
        'appuser' : appuser
    }
    return render(request, "webapp/add_drug.html", context)


@login_required
def add_appointment_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = AppointmentForm(request.POST)
    if form.is_valid():
        form.save()
        form = AppointmentForm()
        messages.success(request, 'Appointment registration succefully')
    else:
        messages.error(request, 'Appointment registration unsuccefully')
    context = {
        'form': form,
        'appuser' : appuser
    }
    return render(request, "webapp/add_appointment.html", context)



@login_required
def add_prescription_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = PrescriptionForm(request.POST)
    if form.is_valid():
        form.save()
        form = PrescriptionForm()
        messages.success(request, 'Prescription registration succefully')
    else:
        messages.error(request, 'Prescription registration unsuccefully')
    context = {
        'form': form,
        'appuser' : appuser
    }
    return render(request, "webapp/add_prescription.html", context)


@login_required
def add_exam_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = ExamForm(request.POST)
    if form.is_valid():
        form.save()
        form = ExamForm()
        messages.success(request, 'Exam registration succefully')
    else:
        messages.error(request, 'Exam registration unsuccefully')
    context = {
        'form': form,
        'appuser' : appuser
    }
    return render(request, "webapp/add_exam.html", context)


@login_required
def search_user_view(request):

    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = RawAppUserForm(request.POST)
    obj = None

    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']
        cc = form.cleaned_data['cc']
        nif = form.cleaned_data['nif']
        address = form.cleaned_data['address']
        cp = form.cleaned_data['cp']
        type = form.cleaned_data['type']

        obj = AppUser.objects.all()

        if name:
            obj = obj.filter(name=name)
        if email:
            obj = obj.filter(email=email)
        if phone_number:
            obj = obj.filter(phone_number=phone_number)
        if cc:
            obj = obj.filter(cc=cc)
        if nif:
            obj = obj.filter(nif=nif)
        if address:
            obj = obj.filter(address=address)
        if cp:
            obj = obj.filter(cp=cp)
        if type=='NONE':
            type = None
        if type:
            obj = obj.filter(type=type)

        form = RawAppUserForm()
    context = {
        'form' : form ,
        'obj' : obj,
        'appuser' : appuser
    }
    return render(request, "webapp/search_user.html", context)


@login_required
def search_pacient_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = RawPacientForm(request.POST)
    obj = None

    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']
        cc = form.cleaned_data['cc']
        nif = form.cleaned_data['nif']
        address = form.cleaned_data['address']
        cp = form.cleaned_data['cp']
        pacient_number = form.cleaned_data['pacient_number']
        insurance = form.cleaned_data['insurance']

        obj = Pacient.objects.all()

        if name:
            obj = obj.filter(name=name)
        if email:
            obj = obj.filter(email=email)
        if phone_number:
            obj = obj.filter(phone_number=phone_number)
        if cc:
            obj = obj.filter(cc=cc)
        if nif:
            obj = obj.filter(nif=nif)
        if address:
            obj = obj.filter(address=address)
        if cp:
            obj = obj.filter(cp=cp)
        if pacient_number:
            obj = obj.filter(pacient_number=pacient_number)
        if insurance:
            obj = obj.filter(insurance=insurance)

        form = RawPacientForm()
    context = {
        'form' : form ,
        'obj' : obj,
        'appuser' : appuser
    }
    return render(request, "webapp/search_pacient.html", context)


@login_required
def search_drug_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = RawDrugForm(request.POST)
    obj = None

    if form.is_valid():
        name = form.cleaned_data['name']
        dci = form.cleaned_data['dci']
        dosage = form.cleaned_data['dosage']
        generic = form.cleaned_data['generic']
        how_to_take = form.cleaned_data['how_to_take']

        obj = Drug.objects.all()

        if name:
            obj = obj.filter(name=name)
        if dci:
            obj = obj.filter(dci=dci)
        if dosage:
            obj = obj.filter(dosage=dosage)
        if generic:
            obj = obj.filter(generic=generic)
        if how_to_take:
            obj = obj.filter(how_to_take=how_to_take)

        form = RawDrugForm()
    context = {
        'form' : form ,
        'obj' : obj,
        'appuser' : appuser
    }
    return render(request, "webapp/search_drug.html", context)


@login_required
def search_appointment_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = RawAppointmentForm(request.POST or None)
    obj = None

    if form.is_valid():
        medic_username = form.cleaned_data['medic_username']
        pacient_number = form.cleaned_data['pacient_number']

        try:
            pac = Pacient.objects.get(pacient_number=pacient_number)
        except Pacient.DoesNotExist:
            raise Http404('Object Pacient does not exist!')

        try:
            user = User.objects.get(username=medic_username)
        except User.DoesNotExist:
            raise Http404('Object User does not exist!')

        try:
            med = AppUser.objects.get(user=user)
        except AppUser.DoesNotExist:
            raise Http404('Object Medic does not exist!')

        obj = Appointment.objects.all()

        if med:
            obj = obj.filter(medic=med)
        if pac:
            obj = obj.filter(pacient=pac)

        form = RawAppointmentForm()

    context = {
        'form': form,
        'obj': obj,
        'appuser': appuser
    }
    return render(request, "webapp/search_appointment.html", context)


@login_required
def search_prescription_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = RawPrescriptionForm(request.POST)
    obj = None

    if form.is_valid():
        medic_username = form.cleaned_data['medic_username']
        pacient_number = form.cleaned_data['pacient_number']
        drug_id = form.cleaned_data['drug_id']

        try:
            drug_id = Drug.objects.get(id=drug_id)
        except Drug.DoesNotExist:
            raise Http404('Object Drug does not exist!')

        try:
            pac = Pacient.objects.get(pacient_number=pacient_number)
        except Pacient.DoesNotExist:
            raise Http404('Object Pacient does not exist!')

        try:
            user = User.objects.get(username=medic_username)
        except User.DoesNotExist:
            raise Http404('Object User does not exist!')
        try:
            med = AppUser.objects.get(user=user)
        except AppUser.DoesNotExist:
            raise Http404('Object Medic does not exist!')

        obj = Prescription.objects.all()

        if med:
            obj = obj.filter(medic=med)
        if pac:
            obj = obj.filter(pacient=pac)
        if drug_id:
            obj = obj.filter(drug=drug_id)

        form = RawPrescriptionForm()
    context = {
        'form' : form ,
        'obj' : obj,
        'appuser' : appuser
    }
    return render(request, "webapp/search_prescription.html", context)


@login_required
def search_exam_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = RawExamForm(request.POST or None)
    obj = None

    if form.is_valid():
        medic_username = form.cleaned_data['medic_username']
        pacient_number = form.cleaned_data['pacient_number']
        exam_type = form.cleaned_data['exam_type']

        try:
            pac = Pacient.objects.get(pacient_number=pacient_number)
        except Pacient.DoesNotExist:
            raise Http404('Object Pacient does not exist!')

        try:
            user = User.objects.get(username=medic_username)
        except User.DoesNotExist:
            raise Http404('Object User does not exist!')

        try:
            med = AppUser.objects.get(user=user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

        obj = Exam.objects.all()

        if med:
            obj = obj.filter(medic=med)
        if pac:
            obj = obj.filter(pacient=pac)
        if exam_type:
            obj = obj.filter(exam_type=exam_type)

        form = RawExamForm()

    context = {
        'form': form,
        'obj': obj,
        'appuser': appuser
    }
    return render(request, "webapp/search_exam.html", context)


def upload_view(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
        context['url'] = fs.url(name)
    return render(request, 'webapp/upload.html', context)


def upload_txt_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('sucesso')
    else:
        form = UploadForm()
    return render(request, 'webapp/upload_txt.html', {
        'form': form
    })


