#!/bin/bash

# Clean installation script for Tailwind CSS
echo "Setting up Tailwind CSS..."

# Remove existing Tailwind-related packages
npm uninstall tailwindcss @tailwindcss/postcss @tailwindcss/typography

# Install Tailwind CSS v3 (more stable with Next.js)
npm install --save-dev tailwindcss@3.3.0 postcss autoprefixer @tailwindcss/typography

# Initialize Tailwind CSS
npx tailwindcss init -p

echo "Tailwind CSS setup complete!"