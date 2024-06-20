from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ShopInfoUnique4, Postcode, CRMbackend
from django.http import JsonResponse
import requests
import datetime
from django.http import Http404
from .forms import CRMbackendForm

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
    print(day_name)
    try:
        url = f"http://198.244.148.241:5000/shops/{city}/{postcode}/{day_name}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        shop_data = response.json()

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
    shop_name = None
    for item in shop_data:
        if item['id'] == shop_id:
            shop_name = item['name']
            break

    shop = get_object_or_404(CRMbackend, AutoId=shop_id)  # Corrected primary key

    if request.method == 'POST':
        form = CRMbackendForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # replace 'success_url' with your actual success URL
    else:
        form = CRMbackendForm()

    return render(request, 'home/data-entry.html', {'form': form, 'shop': shop, 'shop_name': shop_name})
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
        print(data)
        return JsonResponse(data)
    else:
        # Handle other HTTP methods if needed
        return JsonResponse({'error': 'Method not allowed'}, status=405)