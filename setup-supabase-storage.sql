-- Storage buckets setup for CourseAI
-- Run these commands in your Supabase SQL editor or via the dashboard

-- Create storage buckets
INSERT INTO storage.buckets (id, name, public) VALUES 
  ('course-files', 'course-files', false),
  ('course-thumbnails', 'course-thumbnails', true),
  ('user-avatars', 'user-avatars', true)
ON CONFLICT (id) DO NOTHING;

-- Storage policies for course-files bucket (private files)
CREATE POLICY "Users can upload own course files" ON storage.objects 
FOR INSERT WITH CHECK (
  bucket_id = 'course-files' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can view own course files" ON storage.objects 
FOR SELECT USING (
  bucket_id = 'course-files' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can update own course files" ON storage.objects 
FOR UPDATE USING (
  bucket_id = 'course-files' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can delete own course files" ON storage.objects 
FOR DELETE USING (
  bucket_id = 'course-files' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Storage policies for course-thumbnails bucket (public files)
CREATE POLICY "Users can upload own course thumbnails" ON storage.objects 
FOR INSERT WITH CHECK (
  bucket_id = 'course-thumbnails' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Anyone can view course thumbnails" ON storage.objects 
FOR SELECT USING (bucket_id = 'course-thumbnails');

CREATE POLICY "Users can update own course thumbnails" ON storage.objects 
FOR UPDATE USING (
  bucket_id = 'course-thumbnails' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can delete own course thumbnails" ON storage.objects 
FOR DELETE USING (
  bucket_id = 'course-thumbnails' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Storage policies for user-avatars bucket (public files)
CREATE POLICY "Users can upload own avatar" ON storage.objects 
FOR INSERT WITH CHECK (
  bucket_id = 'user-avatars' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Anyone can view user avatars" ON storage.objects 
FOR SELECT USING (bucket_id = 'user-avatars');

CREATE POLICY "Users can update own avatar" ON storage.objects 
FOR UPDATE USING (
  bucket_id = 'user-avatars' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);

CREATE POLICY "Users can delete own avatar" ON storage.objects 
FOR DELETE USING (
  bucket_id = 'user-avatars' AND 
  auth.uid()::text = (storage.foldername(name))[1]
);