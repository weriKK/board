#!/bin/python
from board import create_app
from board.configs.development import DevelopmentConfig


app = create_app(DevelopmentConfig)

if __name__ == "__main__":
    # [TODO kova]: On Windows, use multithreading. On Linux, use multiple threads and / or processes
    app.run(threaded=True)
