from django.shortcuts import render, HttpResponse
import requests
import os
import cv2
from .forms import VideoUploadForm
from ultralytics import YOLO
from django.conf import settings
import numpy as np


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





def get_standings_for_league(competition = "PL", url = "http://api.football-data.org/v4/competitions/"):
    
    headers = {
        'X-Auth-Token': '6034433a2a734f89b1c9edda63bdec34'  # Replace 'YOUR_API_KEY' with your actual API key
    }

    response = requests.get(url + competition + "/standings", headers=headers)
    if response.status_code != 200:
        return None
     
    return response.json()

def livescores(request):
    league_standings = {}
    leagues = {
        'Premier league': "PL",
        'Bundesliga' : "BL1",
        'Serie A' : "SA",
    }

    for league_name, league_code in leagues.items():
        data = get_standings_for_league(league_code)
        if data and 'standings' in data:
            league_standings[league_name] = data['standings'][0]['table']

    context = {'league_standings': league_standings}

    return render(request, 'livescores.html', context)






#Not finished
# def handle_uploaded_file(f):
#     file_path = os.path.join(settings.MEDIA_ROOT, f.name)
#     with open(file_path, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
#     return file_path


# def predict_and_draw_boxes_for_players(model, img):
#     results = model.predict(img)  # Perform predictions with your YOLO model
#     threshold = 0.5
#     team_colors = [(255, 0, 0), (0, 255, 0)]  # Example team colors

#     player_list = []
#     overall_avg_pixel_value = 0
#     player_count = 0

#     for box in results[0].boxes:
#         xmin, ymin, xmax, ymax = map(int, box.xyxy.flatten())
#         object_type = int(box.cls)
#         probability = float(box.conf)

#         if probability > threshold:
#             player_roi = img[ymin:ymax, xmin:xmax]
#             avg_pixel_value = np.mean(np.mean(player_roi, axis=(0, 1)))

#             player_list.append([avg_pixel_value, (xmin, ymin), (xmax, ymax)])
#             overall_avg_pixel_value += avg_pixel_value
#             if object_type == 2:  # Assuming '2' represents players
#                 player_count += 1

#     average_value_threshold = overall_avg_pixel_value / player_count if player_count > 0 else 0

#     for avg_value, (xmin, ymin), (xmax, ymax) in player_list:
#         team_color = team_colors[0] if avg_value > average_value_threshold else team_colors[1]
#         cv2.rectangle(img, (xmin, ymin), (xmax, ymax), team_color, 1)
#     return img



# def process_video(video_path):
#     # Open video file
#     cap = cv2.VideoCapture(video_path)

#     # Get video properties
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = int(cap.get(cv2.CAP_PROP_FPS))

#     # Prepare output file path
#     output_path = os.path.join(settings.MEDIA_ROOT, 'processed_video.mp4')
#     out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

#     # Process each frame and write to output video
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Example: Convert frame to grayscale
#         gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # Write processed frame to output video
#         out.write(gray_frame)

#     # Release resources
#     cap.release()
#     out.release()

#     # Return path to processed video
#     return output_path

# def soccer_video(request):
#     if request.method == 'POST':
#         form = VideoUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file_path = handle_uploaded_file(request.FILES['video'])
#             processed_video_path = process_video(file_path)
#             return render(request, 'video_upload_and_display.html', {'processed_video_path': processed_video_path})
#     else:
#         form = VideoUploadForm()
#     return render(request, 'video_upload_and_display.html', {'form': form})
