#!bin/bash

python update_weather.py &
bundle exec jekyll serve --port 5000 --host 0.0.0.0

