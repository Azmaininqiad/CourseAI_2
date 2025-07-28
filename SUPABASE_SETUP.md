# Supabase Integration Setup Guide

This guide will help you set up Supabase database and storage for your CourseAI project.

## Prerequisites

- A Supabase account and project
- Your Supabase project URL and anon key

## Database Setup

### 1. Run the Main Schema

1. Open your Supabase dashboard
2. Go to the SQL Editor
3. Copy and paste the contents of `supabase-schema.sql`
4. Click "Run" to execute the schema

This will create:
- All necessary tables (profiles, courses, course_modules, course_lessons, etc.)
- Row Level Security policies
- Indexes for performance
- Triggers for automatic profile creation
- Helper functions

### 2. Set up Storage Buckets

1. In the SQL Editor, copy and paste the contents of `setup-supabase-storage.sql`
2. Click "Run" to create the storage buckets and policies

This will create:
- `course-files` bucket (private) - for course attachments and files
- `course-thumbnails` bucket (public) - for course thumbnail images
- `user-avatars` bucket (public) - for user profile pictures

## Frontend Integration

### 1. Environment Variables

The Supabase configuration is already set up in `src/lib/supabase.ts` with your credentials:

```typescript
const supabaseUrl = 'https://fmjhprfruwskmyualmip.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
```

### 2. Authentication

The app includes:
- `AuthProvider` context for managing authentication state
- Login/signup functionality in `/login`
- Automatic profile creation when users sign up
- Row Level Security to ensure users only see their own data

### 3. Course Management

The integration provides:
- Course creation with AI generation
- File upload to Supabase storage
- Course export (JSON/Markdown)
- Real-time progress tracking during generation

## Usage

### 1. User Authentication

Users can sign up and sign in through the `/login` page. The system will:
- Create a user profile automatically
- Set up proper permissions
- Redirect to the dashboard

### 2. Course Creation

When creating a course:
1. The frontend calls your backend API to generate content
2. The generated content is stored in Supabase
3. Files are uploaded to Supabase storage
4. Progress is tracked in real-time

### 3. Data Flow

```
Backend API (Course Generation) 
    ↓
Frontend (Display & User Interaction)
    ↓
Supabase (Data Storage & File Storage)
```

## Database Schema Overview

### Core Tables

- **profiles** - User profiles (extends Supabase auth.users)
- **courses** - Main course information
- **course_modules** - Course modules/chapters
- **course_lessons** - Individual lessons within modules
- **course_files** - File attachments and media
- **course_generation_logs** - Progress tracking for AI generation
- **user_course_progress** - Learning progress tracking

### Key Features

- **Row Level Security** - Users can only access their own data
- **Automatic Timestamps** - Created/updated timestamps on all records
- **File Management** - Integrated with Supabase storage
- **Progress Tracking** - Real-time course generation progress
- **Export Functionality** - Export courses to various formats

## API Usage Examples

### Creating a Course

```typescript
import { CourseService } from '@/services/courseService'

const course = await CourseService.generateCourse(
  userId,
  'JavaScript Fundamentals',
  (progress, step) => {
    console.log(`${progress}%: ${step}`)
  }
)
```

### Uploading Files

```typescript
import { storage } from '@/lib/supabase'

const { path, url } = await storage.uploadCourseFile(
  userId,
  courseId,
  file
)
```

### Fetching Course Data

```typescript
import { db } from '@/lib/supabase'

const courses = await db.getCourses(userId)
const courseWithContent = await db.getCourseWithContent(courseId)
```

## Security Features

- **Row Level Security** - Database-level access control
- **Authentication Required** - All operations require valid user session
- **File Access Control** - Users can only access their own files
- **Input Validation** - Type-safe database operations

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Check if user is properly authenticated
   - Verify Supabase credentials are correct

2. **Permission Denied**
   - Ensure RLS policies are properly set up
   - Check if user owns the resource they're trying to access

3. **File Upload Issues**
   - Verify storage buckets exist
   - Check storage policies are configured
   - Ensure file size limits are not exceeded

### Debug Tips

- Check browser console for detailed error messages
- Use Supabase dashboard to inspect data and logs
- Verify database schema matches the TypeScript interfaces

## Next Steps

1. Run the SQL scripts in your Supabase project
2. Test the authentication flow
3. Create a test course to verify the integration
4. Customize the UI and add additional features as needed

The integration is now ready to use! Your backend will generate course content, and the frontend will store and manage it in Supabase with proper user authentication and file storage.