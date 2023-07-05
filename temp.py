from flask import Flask, Response, render_template,request
from flask_admin import Admin

import os

app = Flask(__name__)
admin = Admin(app, name='microblog', template_mode='bootstrap3')


VIDEO_PATH = os.path.join(os.path.dirname(__file__), 'static', 'test.mp4')


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/stream')
def stream_video():
    def generate():
        video = open(VIDEO_PATH, 'rb')
        video.seek(0, os.SEEK_END)
        video_length = video.tell()
        video.seek(0)

        headers = {
            'Accept-Ranges': 'bytes',
            'Content-Length': video_length,
            'Content-Range': f'bytes 0-{video_length}/{video_length}',
            'Content-Type': 'video/mp4',
        }

        status = 206
        range_header = request.headers.get('Range', None)
        if range_header:
            start, end = range_header.split('=')[1].split('-')
            start = int(start)
            end = int(end) if end else video_length - 1
            headers['Content-Range'] = f'bytes {start}-{end}/{video_length}'
            headers['Content-Length'] = end - start + 1
            video.seek(start)
            status = 206

        return Response(
            generate_chunk(video),
            headers=headers,
            status=status,
            mimetype='video/mp4',
            content_type='application/octet-stream'
        )

    return generate()


def generate_chunk(video, chunk_size=1024*1024):
    while True:
        data = video.read(chunk_size)
        if not data:
            break
        yield data


if __name__ == '__main__':
    app.run(debug=True)

