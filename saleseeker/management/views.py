from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import  Postcode, CRMbackend, EmployeeID
from django.http import JsonResponse
import requests
import datetime
from django.http import Http404
from .forms import CRMbackendForm
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging

# @login_required
def management(request):
    # cities = ShopInfoUnique4.objects.values_list('city', flat=True).distinct()[:10]
    # context = {'cities': cities}
    # print(context)
    return render(request, 'home/index.html')

def fetch_postcodes(request):
    city_name = request.GET.get('city')
    if city_name:
        postcodes = Postcode.objects.filter(City=city_name).values_list('Post_code', flat=True)
        return JsonResponse(list(postcodes), safe=False)

    return JsonResponse([], safe=False)

def table_list(request):
    # Use 'City' instead of 'city'
    cities = Postcode.objects.values_list('City', flat=True).distinct()
    context = {'cities': cities}
    return render(request, 'home/table-list.html', context)



    
# def chooseshop(request):
#     city = request.GET.get('city', '')
#     postcode = request.GET.get('postcode', '')
#     today = datetime.date.today()
#     try:
#         url = f"http://198.244.148.241:5000/shops/{city}/{postcode}/{today}"
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an HTTPError for bad responses
#         shop_data = response.json()
#         shops = []
#         for shop in shop_data:
#             name = shop[0]
#             address = shop[1] if shop[1] and str(shop[1]).lower() != 'nan' else "Address not available"
#             phone_number = shop[2] if shop[2] and str(shop[2]).lower() != 'nan' else "Phone not available"
#             shops.append({'name': name, 'address': address, 'phone_number': phone_number})
#         return render(request, 'home/table-list.html', {'shops': shops})
#     except requests.exceptions.RequestException as e:
#         return JsonResponse({'error': str(e)})


def chooseshop(request):
    city = request.GET.get('city', '')
    postcode = request.GET.get('postcode', '')
    # Get the current date
    today = datetime.date.today()

    # Print the day name
    day_name = today.strftime("%A")
    # print(day_name)
    try:
        url = f"http://198.244.148.241:5000/shops/{city}/{postcode}/{day_name}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        shop_data = response.json()
        print(shop_data)

        shops = [
            {
                'id': idx,
                'name': shop[0],
                'address': shop[1] if shop[1] and str(shop[1]).lower() != 'nan' else "Address not available",
                'phone_number': shop[2] if shop[2] and str(shop[2]).lower() != 'nan' else "Phone not available",
                'opening_hours': shop[4],
            }
            for idx, shop in enumerate(shop_data) if shop
        ]
        request.session['shop_data'] = shops
        
        return render(request, 'home/table-list.html', {'shops': shops})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)})

def shop_detail(request, shop_id):
    shop_data = request.session.get('shop_data', [])
    # Convert shop_id to integer since session data stores it as an integer
    shop_id = int(shop_id)
    
    # Find the shop with the matching ID
    try:
        shop = next(shop for shop in shop_data if shop['id'] == shop_id)
    except StopIteration:
        raise Http404("Shop not found")
    return render(request, 'home/shop_detail.html', {'shop': shop})

# def data_entry(request):
#     return render(request, 'home/data-entry.html')
    
    
# def shop_detail(request, shop_id):
#     shop_data = request.session.get('shop_data', [])
#     # Convert shop_id to integer since session data stores it as an integer
#     shop_id = int(shop_id)
    
#     # Find the shop with the matching ID
#     try:
#         shop = next(shop for shop in shop_data if shop['id'] == shop_id)
#     except StopIteration:
#         raise Http404("Shop not found")
    
#     return render(request, 'home/shop_detail.html', {'shop': shop})


def data_entry(request, shop_id):
    print(shop_id)
    shop_data = request.session.get('shop_data', [])
    print('Session shop_data:', shop_data)  # Debugging print
    shop_name = None
    
    # Find the shop name from the session data
    for item in shop_data:
        if item['id'] == shop_id:
            shop_name = item['name']
            print(shop_name)
            break
    
    if not shop_name:
        messages.error(request, 'Shop name not found in session data.')
        return redirect('error_url')  # replace 'error_url' with your actual error URL

    try:
        # Fetch the shop object or raise Http404 if not found
        shop = CRMbackend.objects.get(AutoId=shop_id)
    except CRMbackend.DoesNotExist:
        shop = None
        messages.error(request, 'Shop data not found in CRM backend.')
        # return redirect('error_url')  # Handle the case where shop data is not found

    if request.method == 'POST':
        form = CRMbackendForm(request.POST, instance=shop)
        if form.is_valid():
            # Do not commit yet, we will set additional fields first
            crm_instance = form.save(commit=False)
            crm_instance.ShopName = shop_name

            # Fetch the employee_id of the logged-in user
            try:
                employee = EmployeeID.objects.get(user=request.user)
                crm_instance.EmployeeID = employee.employee_id
            except EmployeeID.DoesNotExist:
                messages.error(request, 'Employee ID not found for the logged-in user.')
                return redirect('error_url')  # replace 'error_url' with your actual error URL

            crm_instance.Date = timezone.now().strftime('%Y-%m-%d')   # setting current date and time
            print(crm_instance.Date)
            crm_instance.save()
            messages.success(request, 'Data entry saved successfully.')
            return redirect('table_list')  # replace 'success_url' with your actual success URL
        else:
            messages.error(request, 'There was an error with the form. Please check the data and try again.')
    else:
        form = CRMbackendForm(instance=shop)

    return render(request, 'home/data-entry.html', {'form': form, 'shop': shop, 'shop_name': shop_name, 'shop_id': shop_id})

# def crmbackend(request):
#     if request.method == 'POST':
#         form = CRMbackendForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success_url')  # replace 'success_url' with your actual success URL
#     else:
#         form = CRMbackendForm()
    
#     return render(request, 'home/data-entry.html', {'form': form}) 

def crmbackend_data(request):
    if request.method == 'GET':
        crm_data = list(CRMbackend.objects.values())
        data = {
            'crm_data': crm_data,
        }
        # print(data)
        return JsonResponse(data)
    else:
        # Handle other HTTP methods if needed
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
logger = logging.getLogger(__name__)

# def call_history(request):
#     try:
#         # Default values for pagination and sorting
#         page_number = request.GET.get('page', 1)
#         rows_per_page = 15
#         shop_name_filter = request.GET.get('shop_name', '')
#         sort_by = request.GET.get('sort_by', 'Date')
#         sort_order = request.GET.get('sort_order', 'desc')

#         try:
#             page_number = int(page_number)
#             if page_number < 1:
#                 page_number = 1
#         except ValueError:
#             page_number = 1

#         # Define sorting
#         if sort_order == 'desc':
#             sort_by = '-' + sort_by

#         # Fetch call history data from CRMbackend model with optional filter and sorting
#         call_history_entries = CRMbackend.objects.all()
#         call_history_entries2 = EmployeeID.objects.all()

#         if shop_name_filter:
#             call_history_entries = call_history_entries.filter(ShopName__icontains=shop_name_filter)

#         call_history_entries = call_history_entries.order_by(sort_by)

#         # Paginate the queryset
#         paginator = Paginator(call_history_entries, rows_per_page)

#         try:
#             crm_data = paginator.page(page_number)
#         except EmptyPage:
#             logger.warning(f"Requested page {page_number} is out of range. Returning the last page.")
#             crm_data = paginator.page(paginator.num_pages)  # Return last page
#         except PageNotAnInteger:
#             logger.warning(f"Invalid page number '{page_number}' received. Returning the first page.")
#             crm_data = paginator.page(1)  # Return first page

#         # Collect usernames for the crm_data entries
#         entries_with_usernames = []
#         for entry in call_history_entries2:
#             print(entry.employee_id)
#             username = get_username_by_employee_id(entry.employee_id)
#             entry_data = {
#                 'entry': entry,
#                 'username': username
#             }
#             entries_with_usernames.append(entry_data)
#         print(entries_with_usernames)

#         # Prepare context data for rendering the template
#         context = {
#             'entries_with_usernames': entries_with_usernames,
#             'total_pages': paginator.num_pages,
#             'current_page': crm_data.number,
#             'shop_name': shop_name_filter,
#             'sort_by': sort_by.lstrip('-'),
#             'sort_order': 'asc' if sort_order == 'desc' else 'desc',
#         }

#         return render(request, 'home/call-history.html', context)

#     except Exception as e:
#         logger.error(f"Error occurred in call_history view: {str(e)}")
#         return render(request, 'home/call-history.html', {'error': 'Internal Server Error'})
    
logger = logging.getLogger(__name__)

def call_history(request):
    try:
        # Default values for pagination and sorting
        page_number = request.GET.get('page', 1)
        rows_per_page = 15
        shop_name_filter = request.GET.get('shop_name', '')
        employee_id_filter = request.GET.get('employee_id', '')
        sort_by = request.GET.get('sort_by', 'Date')
        sort_order = request.GET.get('sort_order', 'desc')

        try:
            page_number = int(page_number)
            if page_number < 1:
                page_number = 1
        except ValueError:
            page_number = 1

        # Define sorting
        if sort_order == 'desc':
            sort_by = '-' + sort_by

        # Fetch call history data from CRMbackend model with optional filter and sorting
        call_history_entries = CRMbackend.objects.all()
        if shop_name_filter:
            call_history_entries = call_history_entries.filter(ShopName__icontains=shop_name_filter)
        if employee_id_filter:
            call_history_entries = call_history_entries.filter(EmployeeID__employee_id=employee_id_filter)
        call_history_entries = call_history_entries.order_by(sort_by)
        
        # Paginate the queryset
        paginator = Paginator(call_history_entries, rows_per_page)

        try:
            crm_data = paginator.page(page_number)
        except EmptyPage:
            logger.warning(f"Requested page {page_number} is out of range. Returning the last page.")
            crm_data = paginator.page(paginator.num_pages)  # Return last page
        except PageNotAnInteger:
            logger.warning(f"Invalid page number '{page_number}' received. Returning the first page.")
            crm_data = paginator.page(1)  # Return first page

        # Fetch all shop names and employee IDs for the filters
        all_shop_names = CRMbackend.objects.values_list('ShopName', flat=True).distinct()
        all_employee_ids = EmployeeID.objects.all()

        # Prepare context data for rendering the template
        context = {
            'crm_data': crm_data,
            'total_pages': paginator.num_pages,
            'current_page': crm_data.number,
            'shop_name': shop_name_filter,
            'employee_id': employee_id_filter,
            'sort_by': sort_by.lstrip('-'),
            'sort_order': 'asc' if sort_order == 'desc' else 'desc',
            'all_shop_names': all_shop_names,
            'all_employee_ids': all_employee_ids,
        }

        return render(request, 'home/call-history.html', context)

    except Exception as e:
        logger.error(f"Error occurred in call_history view: {str(e)}")
        return render(request, 'home/call-history.html', {'error': 'Internal Server Error'})



# def get_username_by_employee_id(request, employeeID):
#     try:
#         employee_obj = EmployeeID.objects.get(employee_id=employeeID)
#         username = employee_obj.user.username
#     except EmployeeID.DoesNotExist:
#         logger.warning(f"EmployeeID with ID {employeeID} does not exist.")
#         username = 'Unknown'
#     except Exception as e:
#         logger.error(f"Error occurred while fetching username for EmployeeID {employeeID}: {str(e)}")
#         username = 'Unknown'
    
#     return JsonResponse({'username': username})
def get_username_by_employee_id(request, employee_id):
    try:
        employee_obj = get_object_or_404(EmployeeID, employee_id=employee_id)
        username = employee_obj.user.username
        return JsonResponse({'username': username})
    except Exception as e:
        logger.error(f"Error occurred while fetching username for EmployeeID {employee_id}: {str(e)}")
        return JsonResponse({'username': 'Unknown'}, status=500)



def errorhandling(request):
    return render(request, 'home/page-500.html')