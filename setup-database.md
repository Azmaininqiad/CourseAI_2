# Database Setup Instructions

Since I can't directly execute SQL on your Supabase database, here are the steps to set it up:

## Step 1: Run the Main Schema

1. Open your Supabase dashboard: https://supabase.com/dashboard
2. Go to your project: `fmjhprfruwskmyualmip`
3. Navigate to **SQL Editor** in the left sidebar
4. Copy the entire contents of `supabase-final-schema.sql`
5. Paste it into the SQL Editor
6. Click **Run** to execute

This will create:
- ✅ All database tables
- ✅ Row Level Security policies
- ✅ Indexes for performance
- ✅ Triggers for automatic timestamps
- ✅ Functions for complex queries

## Step 2: Set up Storage Buckets

1. Still in the SQL Editor, copy the contents of `setup-supabase-storage.sql`
2. Paste and run it

This will create:
- ✅ `course-files` bucket (private)
- ✅ `course-thumbnails` bucket (public)
- ✅ `user-avatars` bucket (public)
- ✅ Storage policies for file access control

## Step 3: Verify Setup

After running both scripts, you should see these tables in your database:

### Tables Created:
- `profiles` - User profiles
- `courses` - Main course data
- `course_modules` - Course chapters/modules
- `course_lessons` - Individual lessons
- `course_files` - File attachments
- `course_generation_logs` - AI generation progress
- `user_course_progress` - Learning progress tracking

### Storage Buckets Created:
- `course-files` - For course attachments
- `course-thumbnails` - For course images
- `user-avatars` - For profile pictures

## Step 4: Test the Integration

1. Start your development server: `npm run dev`
2. Visit `http://localhost:3000/login`
3. Create a test account
4. Visit `http://localhost:3000/dashboard-new`
5. Try creating a course

## Troubleshooting

If you get any errors:

1. **Permission errors**: Make sure you're using the SQL Editor in Supabase dashboard
2. **Type already exists**: Some types might already exist, you can ignore these errors
3. **Table already exists**: Drop existing tables first if you're re-running the schema

## Alternative: Manual Table Creation

If the SQL script doesn't work, you can also create tables manually through the Supabase dashboard:

1. Go to **Table Editor**
2. Click **New Table**
3. Create each table following the schema in `supabase-final-schema.sql`

## Next Steps

Once the database is set up:
- Your frontend will automatically connect to Supabase
- User authentication will work
- Course creation will store data in the database
- File uploads will go to Supabase storage

The MCP integration I set up will also allow me to help you query and manage the database directly through Kiro!