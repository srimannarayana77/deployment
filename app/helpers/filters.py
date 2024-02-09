from django.db.models import Q

def  client_filters(queryset, params):
    try:
        full_name = params.get('full_name')
        contact_number = params.get('contact_number')
        email_address = params.get('email_address')
        company_name = params.get('company_name')
        designation = params.get('designation')

        filters = Q()

        if full_name:
            filters &= Q(full_name__icontains=full_name)

        if contact_number:
            filters &= Q(contact_number__icontains=contact_number)

        if email_address:
            filters &= Q(email_address__icontains=email_address)

        if company_name:
            filters &= Q(company_name__icontains=company_name)

        if designation:
            filters &= Q(designation__icontains=designation)


        return queryset.filter(filters)
    
    except Exception as e:
        raise e

def invoice_filters(queryset, params):
    try:
        payment_date = params.get('payment_date')

        filters = Q()
       
        if payment_date:
            filters &= Q(payment_date=payment_date)   

        return queryset.filter(filters)
    
    except Exception as e:
        raise e
    
def lead_details_filters(queryset, params):
    try:
        company_name = params.get('company_name')
        name = params.get('name')
        email_id = params.get('email_id')
        state = params.get('state')
        message = params.get('message')
                
        filters = Q()

        if company_name:
            filters &= Q(company_name__icontains=company_name)

        if name:
            filters &= Q(name__icontains=name)

        if email_id:
            filters &= Q(email_id__icontains=email_id)

        if state:
            filters &= Q(state__icontains=state)

        if message:
            filters &= Q(message__icontains=message)

        return queryset.filter(filters)
    
    except Exception as e:
        raise e