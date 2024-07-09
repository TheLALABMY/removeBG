#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt
echo "Dependencies installed successfully."

echo "Building project..."
mkdir -p build
cp -r templates build/
cp -r static build/
cp app.py build/
cp requirements.txt build/
echo "Project built successfully."
