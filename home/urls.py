from django.urls import path
from home import views

from home.views import g_scraper
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('g_scraper/', views.g_scraper, name='g_scraper'),
    path('save_scraped_data', views.save_scraped_data ,name='save_scraped_data'),
    path('get_saved_data', views.get_saved_data, name='get_saved_data'),
    # path('reset_scraping', views.reset_scraping, name='reset_scraping'),
    path('download_csv', views.download_csv, name='download_csv'),
    path('download_json', views.download_json, name='download_json'),
    # path('get_scraper_progress', views.get_scraper_progress, name='get_scraper_progress'),
    # path('test_scraper/', views.test_scraper, name='test_scraper'),
    path('create_user', views.create_user_view, name='create_user'),
    
    path('get_scraped_data', views.get_scraped_data, name='get_scraped_data'),

]