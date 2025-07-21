from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from .models import Company, Contact, Lead, Deal, Activity
from .forms import CompanyForm, ContactForm, LeadForm, DealForm, ActivityForm

@login_required
def dashboard(request):
    # Get dashboard statistics
    total_contacts = Contact.objects.count()
    total_leads = Lead.objects.count()
    total_deals = Deal.objects.count()
    total_companies = Company.objects.count()
    
    # Recent activities
    recent_activities = Activity.objects.select_related('contact', 'deal').order_by('-created_at')[:5]
    
    # Upcoming activities
    upcoming_activities = Activity.objects.filter(
        due_date__gte=datetime.now(),
        status='planned'
    ).select_related('contact', 'deal').order_by('due_date')[:5]
    
    # Deal statistics
    total_deal_value = Deal.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    won_deals = Deal.objects.filter(stage='closed_won').count()
    
    # Lead conversion stats
    converted_leads = Lead.objects.filter(status='converted').count()
    lead_conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
    
    context = {
        'total_contacts': total_contacts,
        'total_leads': total_leads,
        'total_deals': total_deals,
        'total_companies': total_companies,
        'recent_activities': recent_activities,
        'upcoming_activities': upcoming_activities,
        'total_deal_value': total_deal_value,
        'won_deals': won_deals,
        'lead_conversion_rate': round(lead_conversion_rate, 1),
    }
    
    return render(request, 'crm/dashboard.html', context)

# Company Views
@login_required
def company_list(request):
    companies = Company.objects.all().order_by('name')
    search_query = request.GET.get('search')
    if search_query:
        companies = companies.filter(
            Q(name__icontains=search_query) |
            Q(industry__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    paginator = Paginator(companies, 10)
    page_number = request.GET.get('page')
    companies = paginator.get_page(page_number)
    
    return render(request, 'crm/company_list.html', {'companies': companies})

@login_required
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    contacts = company.contacts.all()
    deals = company.deals.all()
    return render(request, 'crm/company_detail.html', {
        'company': company,
        'contacts': contacts,
        'deals': deals
    })

@login_required
def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company created successfully!')
            return redirect('company_list')
    else:
        form = CompanyForm()
    return render(request, 'crm/company_form.html', {'form': form, 'title': 'Add Company'})

@login_required
def company_edit(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated successfully!')
            return redirect('company_detail', pk=company.pk)
    else:
        form = CompanyForm(instance=company)
    return render(request, 'crm/company_form.html', {'form': form, 'title': 'Edit Company'})

# Contact Views
@login_required
def contact_list(request):
    contacts = Contact.objects.select_related('company').all().order_by('last_name')
    search_query = request.GET.get('search')
    if search_query:
        contacts = contacts.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(company__name__icontains=search_query)
        )
    
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    contacts = paginator.get_page(page_number)
    
    return render(request, 'crm/contact_list.html', {'contacts': contacts})

@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    activities = contact.activities.all().order_by('-created_at')
    deals = contact.deals.all().order_by('-created_at')
    return render(request, 'crm/contact_detail.html', {
        'contact': contact,
        'activities': activities,
        'deals': deals
    })

@login_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            if not contact.assigned_to:
                contact.assigned_to = request.user
            contact.save()
            messages.success(request, 'Contact created successfully!')
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'crm/contact_form.html', {'form': form, 'title': 'Add Contact'})

@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact updated successfully!')
            return redirect('contact_detail', pk=contact.pk)
    else:
        form = ContactForm(instance=contact)
    return render(request, 'crm/contact_form.html', {'form': form, 'title': 'Edit Contact'})

# Lead Views
@login_required
def lead_list(request):
    leads = Lead.objects.all().order_by('-created_at')
    search_query = request.GET.get('search')
    status_filter = request.GET.get('status')
    
    if search_query:
        leads = leads.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(company_name__icontains=search_query)
        )
    
    if status_filter:
        leads = leads.filter(status=status_filter)
    
    paginator = Paginator(leads, 10)
    page_number = request.GET.get('page')
    leads = paginator.get_page(page_number)
    
    return render(request, 'crm/lead_list.html', {'leads': leads})

@login_required
def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, 'crm/lead_detail.html', {'lead': lead})

@login_required
def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            if not lead.assigned_to:
                lead.assigned_to = request.user
            lead.save()
            messages.success(request, 'Lead created successfully!')
            return redirect('lead_list')
    else:
        form = LeadForm()
    return render(request, 'crm/lead_form.html', {'form': form, 'title': 'Add Lead'})

@login_required
def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead updated successfully!')
            return redirect('lead_detail', pk=lead.pk)
    else:
        form = LeadForm(instance=lead)
    return render(request, 'crm/lead_form.html', {'form': form, 'title': 'Edit Lead'})

# Deal Views
@login_required
def deal_list(request):
    deals = Deal.objects.select_related('company', 'contact').all().order_by('-created_at')
    search_query = request.GET.get('search')
    stage_filter = request.GET.get('stage')
    
    if search_query:
        deals = deals.filter(
            Q(title__icontains=search_query) |
            Q(company__name__icontains=search_query) |
            Q(contact__first_name__icontains=search_query) |
            Q(contact__last_name__icontains=search_query)
        )
    
    if stage_filter:
        deals = deals.filter(stage=stage_filter)
    
    paginator = Paginator(deals, 10)
    page_number = request.GET.get('page')
    deals = paginator.get_page(page_number)
    
    return render(request, 'crm/deal_list.html', {'deals': deals})

@login_required
def deal_detail(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    activities = deal.activities.all().order_by('-created_at')
    return render(request, 'crm/deal_detail.html', {'deal': deal, 'activities': activities})

@login_required
def deal_create(request):
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():
            deal = form.save(commit=False)
            if not deal.assigned_to:
                deal.assigned_to = request.user
            deal.save()
            messages.success(request, 'Deal created successfully!')
            return redirect('deal_list')
    else:
        form = DealForm()
    return render(request, 'crm/deal_form.html', {'form': form, 'title': 'Add Deal'})

@login_required
def deal_edit(request, pk):
    deal = get_object_or_404(Deal, pk=pk)
    if request.method == 'POST':
        form = DealForm(request.POST, instance=deal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deal updated successfully!')
            return redirect('deal_detail', pk=deal.pk)
    else:
        form = DealForm(instance=deal)
    return render(request, 'crm/deal_form.html', {'form': form, 'title': 'Edit Deal'})

# Activity Views
@login_required
def activity_list(request):
    activities = Activity.objects.select_related('contact', 'deal').all().order_by('-due_date')
    search_query = request.GET.get('search')
    status_filter = request.GET.get('status')
    
    if search_query:
        activities = activities.filter(
            Q(title__icontains=search_query) |
            Q(contact__first_name__icontains=search_query) |
            Q(contact__last_name__icontains=search_query) |
            Q(deal__title__icontains=search_query)
        )
    
    if status_filter:
        activities = activities.filter(status=status_filter)
    
    paginator = Paginator(activities, 10)
    page_number = request.GET.get('page')
    activities = paginator.get_page(page_number)
    
    return render(request, 'crm/activity_list.html', {'activities': activities})

@login_required
def activity_detail(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    return render(request, 'crm/activity_detail.html', {'activity': activity})

@login_required
def activity_create(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.assigned_to = request.user
            activity.save()
            messages.success(request, 'Activity created successfully!')
            return redirect('activity_list')
    else:
        form = ActivityForm()
    return render(request, 'crm/activity_form.html', {'form': form, 'title': 'Add Activity'})

@login_required
def activity_edit(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity updated successfully!')
            return redirect('activity_detail', pk=activity.pk)
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'crm/activity_form.html', {'form': form, 'title': 'Edit Activity'})

@login_required
def activity_complete(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    activity.mark_completed()
    messages.success(request, 'Activity marked as completed!')
    return redirect('activity_list')
