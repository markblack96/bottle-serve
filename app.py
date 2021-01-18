from bottle import route, run, template, static_file, request, response, HTTPResponse
import bottle
import os
from io import BytesIO
from threading import Thread


VIDEOS_DIRECTORY = '/home/ethan/Videos/'
# VIDEOS_DIRECTORY = '/home/pi/Videos/'

@route('/')
def index():
    return static_file('index.html', root='public')

@route('/nojs')
def index_no_js():
    list_of_videos = os.listdir(VIDEOS_DIRECTORY)
    return template('public/index_no_js.html', videos=[vid for vid in list_of_videos if vid.split('.')[-1] in ['mkv', 'webm', 'mp4']])

@route('/static/<filename>')
def return_static_file(filename):
    return static_file(filename, root='public')

@route('/video/<filename:path>')
def video_page(filename):
    # return static_file('video.html', root='public')

    return template('<video controls><source type="video/mp4" src="/videos/{{filename}}"/></video>', filename=filename)
    
# serve a single video to the browser
@route('/videos/<filename:path>')
def video(filename):
    # route to send videos from
    return static_file(filename, root=VIDEOS_DIRECTORY)

# serve a list of available videos in the directory
@route('/videos')
def video_list():
    list_of_videos = os.listdir(VIDEOS_DIRECTORY)
    list_of_videos = [vid for vid in list_of_videos if vid.split('.')[-1] in ['mkv', 'webm', 'mp4']]
    response.content_type = 'application/json'
    return dict(data=list_of_videos)

def handleUpload(f):
    name, ext = os.path.splitext(f.filename)
    f.save(VIDEOS_DIRECTORY)
    print("File saved")
    print(ext)
    if ext in ['.mkv']:
        print("Beginning conversion")
        os.system('ffmpeg -i '+VIDEOS_DIRECTORY+name+ext+' -codec copy '+VIDEOS_DIRECTORY+name+'.mp4')
        print("Conversion complete")

@route('/upload', method=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        print("request received")
        f = request.files.get('upload')
        task_thread = Thread(target=handleUpload, args=(f,), daemon=True)# set daemon to True so it terminates when the function returns
        task_thread.start()
        print("Starting to save file")
        return HTTPResponse(status=202, body='<h1>File uploading</h1>')
            
    return static_file('upload.html', root='public')

if __name__ == '__main__':
    run(host='localhost', port=5000) #, server='gunicorn', workers=2)

app = bottle.default_app()