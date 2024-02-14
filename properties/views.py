from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Property, Unit
from tenant.models import Agreement
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class ManageProperty(View):
    def get(self, request, **kwargs):
        context = {}
        req_type = request.GET.get('type')

        if req_type == 'get-prop':
            prop_id = request.GET.get('prop-id')
            prop = Property.objects.get(id=int(prop_id))
            all_units = Unit.objects.filter(property=prop)
            units_with_agreements = []

            for unit in all_units:
                agreement = unit.agreement_set.first()  # Get the associated agreement, if any
                units_with_agreements.append({'unit': unit, 'agreement': agreement})

            context.update({'prop': prop, 'units': units_with_agreements})
            return render(request, "view-prop.html", context)

        all_props = Property.objects.all()
        if all_props:
            context['props'] = all_props
        return render(request, "proprties.html", context)

    @transaction.atomic
    def post(self, request, **kwargs):
        req_type = request.POST.get('type')

        if req_type == "add-prop":
            name = request.POST.get('prop-name')
            region = request.POST.get('region')
            street = request.POST.get('street')
            pincode = request.POST.get('pin')
            features = request.POST.get('features')
            landmark = request.POST.get('landmark')
            prop_obj = Property.objects.create(
                name=name, region=region, street=street, pincode=pincode,
                features=features, land_mark=landmark
            )
            return redirect('/property/')

        if req_type == "add-unit":
            rent = request.POST.get('rent')
            unit_type = request.POST.get('unit-type')
            prop_id = request.POST.get('prop-id')
            prop = Property.objects.get(id=prop_id)
            unit = Unit.objects.create(
                property=prop, rent=rent, unit_type=unit_type
            )
            return redirect('/property/?prop-id={}&type=get-prop'.format(prop_id))

@login_required
def view_agreement(request):
    context = {}
    id = request.GET.get('id')
    agreement = Agreement.objects.get(id=id)
    context['agreement'] = agreement
    context['image_url'] = '/media/images/' + agreement.user.address_proof
    return render(request, 'agreement.html', context)
