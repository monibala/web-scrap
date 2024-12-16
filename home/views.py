import csv
import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from home.forms import UserRegistrationForm
from home.scraper import GoogleMapsScraper,scraped_data_store
from django.contrib.auth.decorators import login_required
from .models import ScrapedData


# # Create your views here.
def home(request):
    
    return render( request,'index.html')
from django.contrib.auth import authenticate,logout,login as auth_login
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        print(user)
        if user:
            auth_login(request,user)
            
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request,'login.html')
def user_logout(request):
    logout(request)
    return render(request,'index.html')
# from django.contrib.sessions.models import Session
from django.contrib import messages

# def g_scraper(request):
#     print("Calls Gscrper")
#     if request.method == "GET":
#         query = request.GET.get("q", "").strip()
        
#         if query:
#             try:
#                 # Scraping logic
#                 scraped_data = []
#                 for partial_data in scrape_google_maps(query, yield_partial=True):
#                     scraped_data.append(partial_data)
#                     # Store the latest data in the session
#                     request.session['scraped_data'] = scraped_data
#                     request.session['query'] = query
#                     time.sleep(1)  
#                     for partial_data in scrape_google_maps(query, yield_partial=True):
                        
#                         scraped_data = request.session.get('scraped_data', [])
#                         scraped_data.append(partial_data)
#                         request.session['scraped_data'] = scraped_data
                    
#                     if request.is_ajax():
#                         print("Sending data:", scraped_data)
#                         return JsonResponse({'data': scraped_data})

#                 messages.success(request, "Data extracted successfully.")
#             except Exception as e:
#                 messages.error(request, f"An error occurred: {e}")
#         else:
#             messages.error(request, "Please provide a valid query.")
#         has_scraped_data = 'scraped_data' in request.session
#         scraped_data = request.session.get('scraped_data', [])
#         print("SCRAPED DATA :::::",scraped_data)
#         query = request.session.get('query', '')

        
#         if not has_scraped_data:  
#             request.session['scraped_data'] = []
#             request.session['query'] = ''
    
#     return render(
#         request, 
#         "experiment.html", 
#         {
#             "has_scraped_data": has_scraped_data, 
#             # "scraped_data": request.session.get('scraped_data', []),
#             "scraped_data" : scraped_data,
#             "query": request.session.get('query', ''),
            
#         }
#     )
from django.shortcuts import redirect, render

# def save_data(request):
#     try:
#         scraped_data = request.session.get('scraped_data', [])
#         query = request.session.get('query', '')

#         if scraped_data:
#             for data in scraped_data:
#                 name = data['name']
#                 # Zip only when addresses, mobiles, and websites exist and are the same length
#                 max_length = max(len(data['addresses']), len(data['mobiles']), len(data['websites']))
#                 for i in range(max_length):
#                     address = data['addresses'][i] if i < len(data['addresses']) else "NA"
#                     mobile = data['mobiles'][i] if i < len(data['mobiles']) else None
#                     website = data['websites'][i] if i < len(data['websites']) else None

                    
#                     ScrapedData.objects.create(
#                         name=name or "Unknown",
#                         address=address,
#                         mobile=mobile,
#                         website=website,
#                         query=query,
#                     )
#             request.session['scraped_data'] = []
#             messages.success(request, "Data saved successfully.")

#         return redirect("view_saved_data", query=query)

#     except Exception as e:
#         messages.error(request, f"Error saving data: {e}")
#         return redirect("g_scraper")
# def view_saved_data(request, query):
#     businesses = ScrapedData.objects.filter(query=query)
#     return render(request, "experiment.html", {"businesses": businesses, "query": query})
# # Clears session data
# def reset_scraping(request):
    
#     request.session['scraped_data'] = []
#     return redirect('g_scraper')  
# # Download scraped data
# def download_data(request):
#     scraped_data = request.session.get('scraped_data', [])
#     query = request.session.get('query','default query')
#     is_scraped_data = scraped_data.request.session()
#     response = HttpResponse(content_type='text/csv')
#     filename = f"{query.replace(' ', '_').replace('/', '_')}_scraped_data.csv"
#     response['Content-Disposition'] = f'attachment; filename = "filename"'
#     writer = csv.writer(response)
#     writer.writerow(['Business Name', 'Address', 'Mobile', "Website"])
#     for data in scraped_data:
#         name = data.get('name', 'Unknown')
#         address = ", ".join(data.get('addresses', ['NA']))
#         mobile = ", ".join(data.get('mobiles', ['NA']))
#         website = ", ".join(data.get('websites', ['NA']))

        
#         writer.writerow([name, address, mobile, website])
#     return response  

# def g_scraper(request):
#     if request.method == "POST":
#         query = request.POST.get("query", "").strip()
#         if not query:
#             return JsonResponse({"error": "Query is required."}, status=400)

#         try:
#             # Initialize the scraper here (for example, call your scraping function)
#             scraper = GoogleMapsScraper(query)  # Placeholder for your actual scraper class
#             scraped_data = []
            
#             for partial_data in scraper.scrape_progressively():  # Assume `scrape_progressively` yields data
#                 scraped_data.append(partial_data)
                
#                 # After scraping a piece of data, send it progressively
#                 time.sleep(1)  # Simulate delay between scraping steps

#                 # Send partial data back to the frontend (AJAX)
#                 # if request.is_ajax():
#                 return JsonResponse({'data': partial_data})

#             return JsonResponse({"message": "Scraping completed successfully.", "data": scraped_data}, status=200)

#         except Exception as e:
#             return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

#     return JsonResponse({"error": "Invalid request method."}, status=405)
def ajax_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        if not request.user.is_authenticated:
            if is_ajax:
                return JsonResponse({"error": "User not authenticated. Redirecting to login."}, status=403)
            else:
                from django.shortcuts import redirect
                return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

@ajax_login_required
def g_scraper(request):
    
    if request.method == "POST":
        query = request.POST.get("query", "").strip()
        print(f"Query received: {query}")  # Debugging log

        if not query:
            return JsonResponse({"error": "Query is required."}, status=400)
        try:
            scraper = GoogleMapsScraper(query)
            scraped_data = []
            
            for partial_data in scraper.scrape_progressively():  # Assume `scrape_progressively` yields data
                scraped_data.append(partial_data)
                
                
                time.sleep(1)  
                return JsonResponse({'data': partial_data})

            return JsonResponse({"message": "Scraping completed successfully.", "data": scraped_data}, status=200)

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


def start_scraper(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"error": "No query provided."}, status=400)

    global scraper_results
    scraper_results = []

    def scrape():
        global scraper_results
        for data in scrape_google_maps(query):
            scraper_results.append(data)

    threading.Thread(target=scrape).start()
    return JsonResponse({"message": "Scraping started."})

last_index = 0
def get_scraper_progress(request):
    global last_index

    if request.method == "GET":
        new_data = []
        
        print("Progressiv edata")
        if last_index < len(scraped_data_store):
            new_data = [scraped_data_store[last_index]]
            print(new_data)
            last_index += 1

        # Check if scraping is done
        done = last_index >= len(scraped_data_store)

        return JsonResponse({"data": new_data, "done": done})
# To test
# def test_scraper(request):
#     scraper = GoogleMapsScraper("pet shops in Chennai")
#     data = scraper.scrape_google_maps("pet shops in Chennai")
#     print(data)  # Debugging log
#     return JsonResponse({"data": data})
# To save data in db 
def save_scraped_data(request):
    if request.method=="POST":
        try:
            data = request.POST.get("data","")
            if not data:
                return JsonResponse({"error" : "No data"})
            import json
            data_list = json.loads(data)
            
            for d in data_list:
                print(f"Saving data: {d}")
                ScrapedData.objects.create(
                name=d.get("name", ""),
                website=d.get("website", ""),
                mobile=d.get("mobile", ""),
                address=d.get("address", ""),
                query=d.get("query", ""),
                
                
                
            )

            return JsonResponse({"messge":"DataSaved"})
        except Exception as e:
            return JsonResponse({"error":f"An error occurred: {str(e)}"}, status=500)
    return JsonResponse({"error": "Invalid Request"})
# To retrieve save data
def get_saved_data(request):
    if request.method == "GET":
        saved_data = list(ScrapedData.objects.values())
        return JsonResponse({"data":saved_data},safe=False)
    
# User Creation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test


# @user_passes_test(lambda u: u.is_staff)
# def create_user_view(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()  # Save the user to the database
#             return redirect('home')  # Redirect to home after successful creation
#     else:
#         form = UserRegistrationForm()

#     return render(request, 'add_user.html', {'form': form})
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from .models import CustomUser
import uuid

def create_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

       
        if not username or not email or not password:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        try:
            
            user = CustomUser.objects.create(
                username=username,
                email=email,
                password=make_password(password),  # Hash the password
                user_id=str(uuid.uuid4()),  # Generate a unique user_id
            )
            return render(request, 'index.html') 
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'add_user.html') 