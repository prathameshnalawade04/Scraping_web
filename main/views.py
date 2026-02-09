import asyncio
import aiohttp
from bs4 import BeautifulSoup
from asgiref.sync import async_to_sync, sync_to_async

# Django Imports
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import scrap_data

# --- 1. The Async Scraper Logic (Isolated) ---
# This function handles the scraping. We keep it async so it's fast.
async def run_scraper(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()

        # Parse (CPU bound - run in thread)
        def parse():
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string if soup.title else "No Title"
            h1 = [h.get_text().strip() for h in soup.find_all('h1')]
            h2 = [h.get_text().strip() for h in soup.find_all('h2')]
            return title, h1, h2

        title, h1, h2 = await asyncio.to_thread(parse)

        # Save to DB (Use the async-friendly wrapper)
        await sync_to_async(scrap_data.objects.process_data)(
            url=url,
            title=title,
            h1_list=h1,
            h2_list=h2
        )
    except Exception as e:
        print(f"Scraping Error: {e}")

# --- 2. The Views (Standard Synchronous Django) ---

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration.html', {"form": form})

@login_required(login_url='login') # This NOW GUARANTEED works because the view is sync
def scrape_home(request):
    # POST Request: User submitted a URL
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            # MAGIC TRICK: We call the async scraper from this sync view
            async_to_sync(run_scraper)(url)
            
        return redirect('home')

    # GET Request: Show the page
    # Since we are in a sync view, we can call the DB directly!
    data = scrap_data.objects.all().order_by('-updated_at')
    
    return render(request, 'home.html', {'data': data})