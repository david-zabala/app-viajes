#!/usr/bin/env bash
# Install Playwright browsers then start the Flask app
python -m playwright install --with-deps
python app.py
