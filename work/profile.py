#!/bin/python
from board import create_app
from werkzeug.contrib.profiler import ProfilerMiddleware

from board.configs.development import ProfileConfig


app = create_app(ProfileConfig)
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[300])

if __name__ == "__main__":
    # [TODO kova]: On Windows, use multithreading. On Linux, use multiple threads and / or processes
    app.run(debug=True, threaded=True)
