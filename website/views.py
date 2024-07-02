from django.shortcuts import render, HttpResponse
import requests

# Create your views here.
def home(request):
    return render(request, "home.html")

def research(request):
    return render(request, 'research.html')

def resume(request):
    return render(request, 'resume.html')

def projects(request):
    return render(request, 'projects.html')



class Book:
    def __init__(self, title, rating, url, description, author, genres):
        self.title = title
        self.author = author
        self.description = description[0:500] + "..."
        self.rating = rating
        self.url = url
        self.genres = genres

def bookrec(request):
    query = request.GET.get('query')
    count = request.GET.get('count', 10)  # Default to 10 if not specified
    context = {'query': query, 'count': count}

    if query:
        url = 'https://bookrec-server.onrender.com/input'
        data = {'text': query, 'count': count}
        response = requests.post(url, json=data)
        print(response)
        if response.status_code == 200:
            result = response.json()['result']
            if result[1] == 0:
                suggestions = result[0]  # List of book title suggestions
                context.update({
                    'code': 0,
                    'suggestions': suggestions
                })
            else:
                books_data = result[0]
                books = [Book(b[0], b[1], b[2], b[3], b[4], b[5].replace("[", "").replace("]", "")) for b in books_data]
                context.update({
                    'code': 1,
                    'books': books
                })
        else:
            context.update({'error': 'Error fetching data from server'})

    return render(request, 'bookrec.html', context)
