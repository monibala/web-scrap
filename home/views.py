import csv
import json
import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from home.forms import UserRegistrationForm
from home.newscrap import GoogleMapsScraper
from django.contrib.auth.decorators import login_required
from .models import ScrapedData

scraped_data = []

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


from django.shortcuts import redirect, render

# Download scraped data
def download_data(request):
    scraped_data = request.session.get('scraped_data', [])
    query = request.session.get('query','default query')
    is_scraped_data = scraped_data.request.session()
    response = HttpResponse(content_type='text/csv')
    filename = f"{query.replace(' ', '_').replace('/', '_')}_scraped_data.csv"
    response['Content-Disposition'] = f'attachment; filename = "filename"'
    writer = csv.writer(response)
    writer.writerow(['Business Name', 'Address', 'Mobile', "Website"])
    for data in scraped_data:
        name = data.get('name', 'Unknown')
        address = ", ".join(data.get('addresses', ['NA']))
        mobile = ", ".join(data.get('mobiles', ['NA']))
        website = ", ".join(data.get('websites', ['NA']))

        
        writer.writerow([name, address, mobile, website])
    return response  

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

# @ajax_login_required
# def g_scraper(request):
    
#     if request.method == "POST":
#         query = request.POST.get("query", "").strip()
#         print(f"Query received: {query}")  # Debugging log

#         if not query:
#             return JsonResponse({"error": "Query is required."}, status=400)
#         try:
#             scraper = GoogleMapsScraper(query)
#             scraped_data = []
            
            # for partial_data in scraper.scrape_progressively():  # Assume `scrape_progressively` yields data
            #     scraped_data.append(partial_data)
                
                
#                 time.sleep(1)  
#                 return JsonResponse({'data': partial_data})

#             return JsonResponse({"message": "Scraping completed successfully.", "data": scraped_data}, status=200)

#         except Exception as e:
#             return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

#     return JsonResponse({"error": "Invalid request method."}, status=405)
# Immediate data display
# from threading import Thread
# def g_scraper(request):
#     query = request.POST.get("query", "").strip()
#     # max_results = int(request.GET.get("max_results", 10))

#     def scrape():
#         global scraped_data  # Explicitly declare scraped_data as global
#         scraper = GoogleMapsScraper(query)
#         for business in scraper.scrape_google_maps(query):
#             scraped_data.append(business)  # Add to global data store
#             time.sleep(1)  # Simulate delay

#     # Start scraping in a separate thread
#     thread = Thread(target=scrape)
#     thread.start()
#     return JsonResponse({"message": "Scraping completed successfully.", "data": scraped_data}, status=200)
#     # return JsonResponse({"status": "Scraping started"})
# def fetch_data(request):
#     global scraped_data
#     return JsonResponse(scraped_data, safe=False)

# def start_scraper(request):
#     query = request.GET.get("q", "").strip()
#     if not query:
#         return JsonResponse({"error": "No query provided."}, status=400)

#     global scraper_results
#     scraper_results = []

#     def scrape():
#         global scraper_results
#         for data in scrape_google_maps(query):
#             scraper_results.append(data)

#     threading.Thread(target=scrape).start()
#     return JsonResponse({"message": "Scraping started."})

# last_index = 0
# def get_scraper_progress(request):
#     global last_index

#     if request.method == "GET":
#         new_data = []
        
#         print("Progressiv edata")
#         if last_index < len(scraped_data_store):
#             new_data = [scraped_data_store[last_index]]
#             print(new_data)
#             last_index += 1

#         # Check if scraping is done
#         done = last_index >= len(scraped_data_store)

#         return JsonResponse({"data": new_data, "done": done})
# New
# from django.shortcuts import render
# from django.http import StreamingHttpResponse
# from home.newscrap import GoogleMapsScraper

# def g_scraper(request):
#     # Render template when it's a GET request
#     if request.method == 'GET':
#         return render(request, 'index.html')  # Render the template as usual

#     # Handle POST request to start scraping and return streaming data
#     if request.method == 'POST':
#         query = request.POST.get('query')
#         if query:
#             scraper = GoogleMapsScraper(query)
#             # Return StreamingHttpResponse for progressive scraping
#             return StreamingHttpResponse(scraper.scrape_google_maps(query), content_type="application/json")
    
#     return render(request, 'index.html')  # Fallback if something goes wrong

import time
from threading import Thread
from queue import Queue
from django.http import JsonResponse
from django.shortcuts import render
from .newscrap import GoogleMapsScraper

# Global queue to store scraped data safely
import time
from queue import Queue
from threading import Thread
from django.http import JsonResponse

scraped_queue = Queue()
scraping_in_progress = False  # Flag to track if scraping is in progress

def g_scraper(request):
    global scraping_in_progress
    query = request.POST.get("query", "").strip()

    if scraping_in_progress:
        return JsonResponse({"message": "Scraping is already in progress."}, status=400)

    scraping_in_progress = True

    def scrape():
        scraper = GoogleMapsScraper(query)
        for business in scraper.scrape_google_maps(query):
            scraped_queue.put(business)  # Add data to the queue
            time.sleep(1)  # Simulate delay (can be removed for real scraping)

        global scraping_in_progress
        scraping_in_progress = False  # Set flag to False when scraping is complete

    # Start scraping in a background thread
    thread = Thread(target=scrape)
    thread.daemon = True  # Ensure thread exits when main program exits
    thread.start()

    return JsonResponse({"message": "Scraping started, data will be available soon."}, status=200)

def get_scraped_data(request):
    scraped_data = []

    while not scraped_queue.empty():
        item = scraped_queue.get()
        print(f"Retrieved from queue: {item}")
        scraped_data.append(item)

    return JsonResponse({"data": scraped_data}, status=200)



# To test
# def test_scraper(request):
#     scraper = GoogleMapsScraper("pet shops in Chennai")
#     data = scraper.scrape_google_maps("pet shops in Chennai")
#     print(data)  # Debugging log
#     return JsonResponse({"data": data})
# To save data in db 

from .models import ScrapedData

# def save_scraped_data(request):
#     if request.method == "POST":
#         # Ensure session key exists
#         if not request.session.session_key:
#             request.session.save()

#         session_id = request.session.session_key  # Fetch session key
#         data = request.POST.get('data')

#         if not data:
#             return JsonResponse({"error": "No data provided"}, status=400)

#         try:
#             scraped_data = json.loads(data)  # Parse JSON data
#             for entry in scraped_data:
#                 ScrapedData.objects.create(
#                     session_id=session_id,
#                     name=entry.get('name', ''),
#                     website=entry.get('website', ''),
#                     mobile=entry.get('mobile', ''),
#                     address=entry.get('address', ''),
#                     query = entry.get('query', '')
#                 )
#             return JsonResponse({"message": "Data saved successfully"})
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)
def save_scraped_data(request):
    if request.method == "POST":
        
        data = json.loads(request.POST.get("data", "[]"))
        session_id = request.session.session_key
        saved_entries = []

        for entry in data:
            # Check if an entry with the same session_id, name, and query exists
            if not ScrapedData.objects.filter(
                session_id=session_id,
                name=entry['name'],
                query=entry['query']
            ).exists():
                # Save the entry if it doesn't already exist
                saved = ScrapedData.objects.create(
                    name=entry['name'],
                    website=entry['website'],
                    mobile=entry['mobile'],
                    address=entry['address'],
                    query=entry['query'],
                    session_id=session_id
                )
                saved_entries.append(saved)

        return JsonResponse({"message": "Data saved successfully.", "saved_count": len(saved_entries)})
    return JsonResponse({"error": "Invalid request method."}, status=400)
def get_saved_data(request):
    if request.method == "GET":
        if not request.session.session_key:
            request.session.save()

        session_id = request.session.session_key  # Fetch session key
        saved_data = list(ScrapedData.objects.filter(session_id=session_id).values())

        return JsonResponse({"data": saved_data})
   
# User Creation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test


from django.contrib.auth.hashers import make_password

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

def download_csv(request):
    if not request.session.session_key:
        request.session.save()

    session_id = request.session.session_key  # Fetch session key
    scraped_data = ScrapedData.objects.filter(session_id=session_id)

    # Prepare response with content type 'text/csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="scraped_data.csv"'

    # Create CSV writer object
    writer = csv.writer(response)
    writer.writerow(['Name', 'Website', 'Mobile', 'Address'])  # Header row

    # Write data rows
    for data in scraped_data:
        writer.writerow([data.name, data.website, data.mobile, data.address])

    return response
def download_json(request):
    if not request.session.session_key:
        request.session.save()

    session_id = request.session.session_key  # Fetch session key
    scraped_data = ScrapedData.objects.filter(session_id=session_id)

    data_to_download = [{
        'name': data.name,
        'website': data.website,
        'mobile': data.mobile,
        'address': data.address
    } for data in scraped_data]

    # Create JSON response with the data
    response = HttpResponse(
        json.dumps(data_to_download),
        content_type='application/json'
    )
    response['Content-Disposition'] = 'attachment; filename="scraped_data.json"'

    return response