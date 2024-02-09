from django.db import models

class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    contact_number = models.IntegerField()
    secondary_number = models.IntegerField(blank=True, null=True)
    email_address = models.EmailField(unique=True)
    password= models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class Projects(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=100,choices = [('Wordpress', 'WordPress'),('Web_development', 'Web Development'),('Mobile_app', 'Mobile App')])
    business_sector = models.CharField(max_length=100,choices = [('financial_business', 'Financial/Business'),('NGO', 'Non-Governmental Organization(NGO)')])
    url = models.URLField(unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Invoices(models.Model):
    id = models.BigAutoField(primary_key=True)
    services_offered = models.TextField()
    final_cost = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_date = models.DateField()
    payment_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50,choices =  [('pending', 'Pending'),('paid', 'Paid'),('late', 'Late Payment')])
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='invoices')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Lead_Details(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    email_id = models.EmailField(unique=True)
    state = models.CharField(max_length=100)
    message = models.TextField()
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='lead_details')
    post_date_and_time=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
