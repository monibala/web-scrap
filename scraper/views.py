# import csv
# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse

# from scraper.models import ScrapedData
# # from gscrap.home.scraper import scrape_google_maps
# from .utils import setup_driver, search_google_maps, scrape_business_details

# # The view to handle the form submission
# # def g_scraper(request):
# #     details = None

# #     if request.method == "GET":
# #         # Extract the query parameter from the URL
# #         query = request.GET.get("q", "").strip()

# #     try:
# #             # Setup Selenium WebDriver
# #         driver = setup_driver()

# #             # Perform Google Maps search and scrape business details
# #         search_google_maps(driver, query)
# #         details = scrape_business_details(driver)
# #     except Exception as e:
# #         details = {"error": f"Scraping failed: {str(e)}"}
# #     finally:
# #         driver.quit()

# #     print(details)   

# #     # # Return the response rendering the template with the details (or error message)
# #     return render(request, 'table.html', {'details': details})
#     # return render(request,"table.html")
# # from django.shortcuts import render
# # from .models import ScrapedData
# # from .scraper import scrape_google_maps
# # from django.contrib import messages
# # def g_scraper(request):
# #     try:
# #         if request.method == "GET":
# #             query = request.GET.get("q", "").strip()
# #             scrape_google_maps(query)
# #         messages.success(request,"Data Extracted. To save and view data Click Export")
# #     except Exception as e:
# #         messages.error(request, f'Error occurred: {str(e)}')
# #     return render(request, "table.html")
# # def save_data(request):
# #     name = request.POST.get('name')
# #     mobile = request.POST.get('mobile')
# #     website = request.POST.get('website')
# #     address = request.POST.get('address')
# #     query = request.POST.get('query', 'query')
# #     scraped_data = ScrapedData.objects.create(            
# #         name=name,
# #         mobile=mobile,
# #         website=website,
# #         address=address,
# #         query=query
# #         )
        
        
# #     businesses = ScrapedData.objects.all()

        
# #     return render(request, 'table.html', {'businesses': businesses, 'query': query})
# from django.contrib.sessions.models import Session
# from django.contrib import messages

# def g_scraper(request):
#     if request.method == "GET":
#         query = request.GET.get("q", "").strip()
        
#         if query:
#             try:
#                 scraped_data = scrape_google_maps(query)
                
#                 request.session['scraped_data'] = scraped_data  # Save data to session
#                 request.session['query'] = query
#                 messages.success(request, "Data extracted successfully. Click 'Save' to store the data.")
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
#             "scraped_data": request.session.get('scraped_data', []),
#             "query": request.session.get('query', '')
#         }
#     )
# from django.shortcuts import redirect

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