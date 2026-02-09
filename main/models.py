from django.db import models
from django.utils import timezone
# Create your models here.
class ScrapDataManager(models.Manager): # Use models.Manager, not BaseManager
    def process_data(self, url, title, h1_list, h2_list):
        # 1. Check if URL exists
        # We use 'self.filter' because we are inside the Manager
        existing_data = self.filter(url=url)
        
        # 2. Convert lists to strings (Cleaning)
        # BeautifulSoup returns lists, but we need text for the DB
        h1_str = ", ".join(h1_list) if isinstance(h1_list, list) else str(h1_list)
        h2_str = ", ".join(h2_list) if isinstance(h2_list, list) else str(h2_list)

        if existing_data.exists():
            # UPDATE existing record
            # correct syntax: .update(field=value)
            existing_data.update(
                title=title,
                h1=h1_str,
                h2=h2_str,
                updated_at=timezone.now()
            )
            return "Updated Timestamp"
        else:
            # CREATE new record
            self.create(
                url=url,
                title=title,
                h1=h1_str,
                h2=h2_str
            )
            return "Created New Record"
        


class scrap_data(models.Model):
    url=models.TextField(blank=True,null=True)
    title=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    h1=models.TextField()
    h2=models.TextField()


    objects = ScrapDataManager()
    actual_object=models.manager

    def __str__(self):
        return self.title or None
    
