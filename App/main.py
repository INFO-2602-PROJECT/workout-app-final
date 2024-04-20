import os
from flask import Flask, render_template
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from App.database import init_db
from App.config import load_config

from App.controllers import (
    setup_jwt,
    add_auth_context
)

from App.views import views

class Video:
    def __init__(self, title, image_url, video_url, description, video_id):
        self.title = title
        self.image_url = image_url
        self.video_url = video_url
        self.description = description
        self.video_id = video_id

def add_views(app):
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)
    
    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401
    
    app.app_context().push()
    return app

def get_video_url(video_id):
    return f"https://www.youtube.com/watch?v={video_id}"

def search_by_keyword(api_key, keyword, max_results):
    youtube = build("youtube", "v3", developerKey=api_key)

    try:
        request = youtube.search().list(
            part="id,snippet",
            q=keyword,
            maxResults=max_results
        )
        response = request.execute()
        videos = []
        if "items" in response:
            for item in response["items"]:
                if item["id"].get("kind") == "youtube#video":
                    video_id = item["id"]["videoId"]
                    video_url = get_video_url(video_id)
                    title = item["snippet"]["title"]
                    image = item["snippet"]["thumbnails"]["default"]["url"]
                    description = item["snippet"]["description"]
                    video = Video(title, image, video_url, description, video_id)
                    videos.append(video)
                else:
                    print("This item is not a video.")
        else:
            print("No videos found.")

    except HttpError as e:
        print("An HTTP error occurrhed:")
        print(e.content)

    return videos

app = create_app()  

@app.route('/home')
def home():
    videos = search_by_keyword("AIzaSyCu2lRlH8ZMoXqCYaPKLSg_1GBY1rhsfkc", "workout tutorial", 30)
    return render_template('index.html', videos=videos)
