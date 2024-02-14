from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Tenant, Agreement, User
from django.core.files.storage import FileSystemStorage
from properties.models import Property, Unit
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class ManageTenant(View):
    def get(self, request, **kwargs):
        # from tenant.models import User
        # superuser = User.objects.create_superuser(email='admin@example.com', password='password')
        context = {}

        req_type = request.GET.get('type')
        if req_type == "get-tenant":
            id = request.GET.get('tenant-id')
            tenant_obj = Tenant.objects.get(id=id)
            context['tenant'] = tenant_obj
            return render(request, 'tenent-detail.html', context)
        elif req_type == "agreement-preview":
            unit_id = request.GET.get('unit-id')
            tenant_id = request.GET.get('tenant-id')
            unit = Unit.objects.get(id=int(unit_id))
            tenant_obj = Tenant.objects.get(id=int(tenant_id))
            context['tenant'] = tenant_obj
            context['prop'] = unit.property
            context['unit'] = unit

            context['image_url'] = '/media/images/' + tenant_obj.address_proof

            return render(request, "assignment-prev.html", context)
        tenants = Tenant.objects.all()
        for i in tenants:
            print(i.address_proof)
        context['tenants'] = tenants
        return render(request, 'tenants.html', context)

    @transaction.atomic
    def post(self, request, **kwargs):
        req_type = request.POST.get('type')
        if req_type == "add-tenant":
            name = request.POST.get('name')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            proof_type = request.POST.get('proof-type')
            proof_image = request.FILES.get('proof-image')

            directory = 'media/images/'

            fs = FileSystemStorage(location=directory)

            filename = fs.save(proof_image.name, proof_image)
            tenant_obj = Tenant.objects.create(name=name, addressline1=address1, addressline2=address2,
                                               proof_type=proof_type, address_proof=filename)
            tenant_obj.save()
            return redirect('/tenant/')
        if req_type == "open-assign":
            context = {}
            tenant_id = request.POST.get('tenant-id')
            username = request.POST.get('tenant-name')
            context['username'] = username
            context['tenant_id'] = tenant_id
            if request.POST.get('search') and request.POST.get('keyword') !="" :
                key = request.POST.get('keyword')
                all_props = Property.objects.filter(region__iexact=key.lower())
            else:
                all_props = Property.objects.all()
            context['props'] = all_props
            return render(request, 'assignment.html', context)
        elif req_type == "get-prop-details":
            context = {}
            tenant_id = request.POST.get('tenant-id')
            username = request.POST.get('tenant-name')
            prop_id = request.POST.get('prop-id')
            context['username'] = username
            context['tenant_id'] = tenant_id
            all_props = Property.objects.all()
            context['props'] = all_props
            all_props = Property.objects.all()
            context['props'] = all_props
            units = Unit.objects.filter(property__id=prop_id)
            if units:
                context['units'] = units
            else:
                context['units'] = None
            return render(request, 'assignment.html', context)

        elif req_type == "generate-agreement":
            tenant_id = request.POST.get('tenant-id')
            tenant = Tenant.objects.get(id=tenant_id)
            unit_id = request.POST.get('unit-id')
            agreement_end_date = request.POST.get('agreement-end-date')
            rent_date = request.POST.get('rent-date')
            unit = Unit.objects.get(id=unit_id)
            unit.is_available = False
            unit.save()
            tenant.is_assigned = True
            tenant.save()
            agreement = Agreement.objects.create(user=tenant, unit=unit, rent=unit.rent,
                                                 agreement_end_date=agreement_end_date, rent_date=rent_date)

            return redirect('/tenant/')


class Login(View):
    def get(self, request, **kwargs):
        return render(request, 'login.html')

    def post(self, request, **kwargs):
        context = {}
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user and user.is_superuser:
            login(request, user=user)
        else:
            context['message'] = "Unauthorized"
            return render(request, 'login.html', context )
        return redirect('/tenant')


class Logout(View):
    def post(self, request, **kwargs):
        logout(request)
        return redirect('login')