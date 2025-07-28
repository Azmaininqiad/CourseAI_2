#!/bin/bash

# Clean installation script for dependencies
echo "Installing dependencies for CourseAI..."

# Install core dependencies
npm install react@18.2.0 react-dom@18.2.0 next@15.3.5

# Install UI components and styling
npm install framer-motion@11.0.3 lucide-react@0.363.0 clsx@2.1.0 tailwind-merge@2.2.2

# Install dev dependencies
npm install --save-dev tailwindcss@3.3.0 postcss@8.4.33 autoprefixer@10.4.16 @tailwindcss/typography@0.5.10

# Initialize Tailwind CSS
npx tailwindcss init -p

echo "Installation complete! You can now run 'npm run dev' to start the application."