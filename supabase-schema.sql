-- CourseAI Database Schema for Supabase
-- Note: JWT secret is managed by Supabase automatically, no need to set it manually

-- Create custom types
CREATE TYPE course_status AS ENUM ('draft', 'generating', 'completed', 'published', 'archived');
CREATE TYPE content_type AS ENUM ('text', 'markdown', 'video', 'image', 'audio', 'document');

-- Users table (extends Supabase auth.users)
CREATE TABLE public.profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    plan TEXT DEFAULT 'starter' CHECK (plan IN ('starter', 'professional', 'enterprise')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Courses table
CREATE TABLE public.courses (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    topic TEXT NOT NULL,
    status course_status DEFAULT 'draft',
    thumbnail_url TEXT,
    estimated_duration INTEGER, -- in minutes
    difficulty_level TEXT CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),
    tags TEXT[],
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Course modules/chapters
CREATE TABLE public.course_modules (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    course_id UUID REFERENCES public.courses(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    order_index INTEGER NOT NULL,
    estimated_duration INTEGER, -- in minutes
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(course_id, order_index)
);

-- Course lessons
CREATE TABLE public.course_lessons (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    module_id UUID REFERENCES public.course_modules(id) ON DELETE CASCADE NOT NULL,
    course_id UUID REFERENCES public.courses(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    content TEXT, -- markdown content
    content_type content_type DEFAULT 'markdown',
    order_index INTEGER NOT NULL,
    estimated_duration INTEGER, -- in minutes
    video_url TEXT,
    thumbnail_url TEXT,
    attachments JSONB DEFAULT '[]', -- array of file references
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(module_id, order_index)
);

-- Course files/attachments
CREATE TABLE public.course_files (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    course_id UUID REFERENCES public.courses(id) ON DELETE CASCADE NOT NULL,
    lesson_id UUID REFERENCES public.course_lessons(id) ON DELETE CASCADE,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL, -- path in Supabase storage
    file_type TEXT NOT NULL,
    file_size BIGINT,
    mime_type TEXT,
    bucket_name TEXT DEFAULT 'course-files',
    is_public BOOLEAN DEFAULT false,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Course generation logs
CREATE TABLE public.course_generation_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    course_id UUID REFERENCES public.courses(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('started', 'in_progress', 'completed', 'failed')),
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    current_step TEXT,
    error_message TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User course progress (for tracking learner progress)
CREATE TABLE public.user_course_progress (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE NOT NULL,
    course_id UUID REFERENCES public.courses(id) ON DELETE CASCADE NOT NULL,
    lesson_id UUID REFERENCES public.course_lessons(id) ON DELETE CASCADE,
    completed BOOLEAN DEFAULT false,
    progress_percentage INTEGER DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    time_spent INTEGER DEFAULT 0, -- in seconds
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, course_id, lesson_id)
);

-- Create indexes for better performance
CREATE INDEX idx_courses_user_id ON public.courses(user_id);
CREATE INDEX idx_courses_status ON public.courses(status);
CREATE INDEX idx_courses_created_at ON public.courses(created_at DESC);
CREATE INDEX idx_course_modules_course_id ON public.course_modules(course_id);
CREATE INDEX idx_course_modules_order ON public.course_modules(course_id, order_index);
CREATE INDEX idx_course_lessons_module_id ON public.course_lessons(module_id);
CREATE INDEX idx_course_lessons_course_id ON public.course_lessons(course_id);
CREATE INDEX idx_course_lessons_order ON public.course_lessons(module_id, order_index);
CREATE INDEX idx_course_files_course_id ON public.course_files(course_id);
CREATE INDEX idx_course_files_lesson_id ON public.course_files(lesson_id);
CREATE INDEX idx_generation_logs_course_id ON public.course_generation_logs(course_id);
CREATE INDEX idx_user_progress_user_course ON public.user_course_progress(user_id, course_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add updated_at triggers
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_courses_updated_at BEFORE UPDATE ON public.courses FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_course_modules_updated_at BEFORE UPDATE ON public.course_modules FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_course_lessons_updated_at BEFORE UPDATE ON public.course_lessons FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_generation_logs_updated_at BEFORE UPDATE ON public.course_generation_logs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security Policies

-- Profiles policies
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own profile" ON public.profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON public.profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert own profile" ON public.profiles FOR INSERT WITH CHECK (auth.uid() = id);

-- Courses policies
ALTER TABLE public.courses ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own courses" ON public.courses FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create own courses" ON public.courses FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own courses" ON public.courses FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own courses" ON public.courses FOR DELETE USING (auth.uid() = user_id);

-- Course modules policies
ALTER TABLE public.course_modules ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own course modules" ON public.course_modules FOR SELECT USING (
    EXISTS (SELECT 1 FROM public.courses WHERE courses.id = course_modules.course_id AND courses.user_id = auth.uid())
);
CREATE POLICY "Users can create own course modules" ON public.course_modules FOR INSERT WITH CHECK (
    EXISTS (SELECT 1 FROM public.courses WHERE courses.id = course_modules.course_id AND courses.user_id = auth.uid())
);
CREATE POLICY "Users can update own course modules" ON public.course_modules FOR UPDATE USING (
    EXISTS (SELECT 1 FROM public.courses WHERE courses.id = course_modules.course_id AND courses.user_id = auth.uid())
);
CREATE POLICY "Users can delete own course modules" ON public.course_modules FOR DELETE USING (
    EXISTS (SELECT 1 FROM public.courses WHERE courses.id = course_modules.course_id AND courses.user_id = auth.uid())
);

-- Course lessons policies
ALTER TABLE public.course_lessons ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own course lessons" ON public.course_lessons FOR SELECT USING (
    EXISTS (SELECT 1 FROM public.courses WHERE courses.id = course_lessons.course_id AND courses.user_id = auth.uid())
);
CREATE POLICY "Users can create own course lessons" ON public.course_lessons FOR INSERT WITH CHECK (
    EXISTS (SELECT 1 FROM public.courses WHERE courses.id = course_lessons.course_id AND courses.user_id = auth.uid())
);
CREATE POLICY "Users can update own course lessons" ON public.course_lessons FOR UPDATE USING (
    EXISTS (SELECT 1 FROM public.courses WHERE courses.id = course_lessons.course_id AND courses.user_id = auth.uid())
);
CREATE POLICY "Users can delete own course lessons" ON public.course_lessons FOR DELETE USING (
    EXISTS (SELECT 1 FROM public.courses WHERE courses.id = course_lessons.course_id AND courses.user_id = auth.uid())
);

-- Course files policies
ALTER TABLE public.course_files ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own course files" ON public.course_files FOR SELECT USING (
    EXISTS (SELECT 1 FROM public.courses WHERE courses.id = course_files.course_id AND courses.user_id = auth.uid())
);
CREATE POLICY "Users can create own course files" ON public.course_files FOR INSERT WITH CHECK (
    EXISTS (SELECT 1 FROM public.courses WHERE courses.id = course_files.course_id AND courses.user_id = auth.uid())
);
CREATE POLICY "Users can update own course files" ON public.course_files FOR UPDATE USING (
    EXISTS (SELECT 1 FROM public.courses WHERE courses.id = course_files.course_id AND courses.user_id = auth.uid())
);
CREATE POLICY "Users can delete own course files" ON public.course_files FOR DELETE USING (
    EXISTS (SELECT 1 FROM public.courses WHERE courses.id = course_files.course_id AND courses.user_id = auth.uid())
);

-- Generation logs policies
ALTER TABLE public.course_generation_logs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own generation logs" ON public.course_generation_logs FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create own generation logs" ON public.course_generation_logs FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own generation logs" ON public.course_generation_logs FOR UPDATE USING (auth.uid() = user_id);

-- User progress policies
ALTER TABLE public.user_course_progress ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own progress" ON public.user_course_progress FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can create own progress" ON public.user_course_progress FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own progress" ON public.user_course_progress FOR UPDATE USING (auth.uid() = user_id);

-- Create storage buckets (run these in Supabase dashboard or via API)
-- INSERT INTO storage.buckets (id, name, public) VALUES ('course-files', 'course-files', false);
-- INSERT INTO storage.buckets (id, name, public) VALUES ('course-thumbnails', 'course-thumbnails', true);
-- INSERT INTO storage.buckets (id, name, public) VALUES ('user-avatars', 'user-avatars', true);

-- Storage policies for course-files bucket
-- CREATE POLICY "Users can upload own course files" ON storage.objects FOR INSERT WITH CHECK (
--     bucket_id = 'course-files' AND 
--     auth.uid()::text = (storage.foldername(name))[1]
-- );
-- CREATE POLICY "Users can view own course files" ON storage.objects FOR SELECT USING (
--     bucket_id = 'course-files' AND 
--     auth.uid()::text = (storage.foldername(name))[1]
-- );
-- CREATE POLICY "Users can update own course files" ON storage.objects FOR UPDATE USING (
--     bucket_id = 'course-files' AND 
--     auth.uid()::text = (storage.foldername(name))[1]
-- );
-- CREATE POLICY "Users can delete own course files" ON storage.objects FOR DELETE USING (
--     bucket_id = 'course-files' AND 
--     auth.uid()::text = (storage.foldername(name))[1]
-- );

-- Function to handle user profile creation
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name, avatar_url)
    VALUES (
        NEW.id,
        NEW.email,
        NEW.raw_user_meta_data->>'full_name',
        NEW.raw_user_meta_data->>'avatar_url'
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to create profile on user signup
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Function to get course with all related data
CREATE OR REPLACE FUNCTION get_course_with_content(course_uuid UUID)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'course', row_to_json(c.*),
        'modules', COALESCE(modules.modules_data, '[]'::json),
        'files', COALESCE(files.files_data, '[]'::json)
    ) INTO result
    FROM public.courses c
    LEFT JOIN (
        SELECT 
            cm.course_id,
            json_agg(
                json_build_object(
                    'module', row_to_json(cm.*),
                    'lessons', COALESCE(lessons.lessons_data, '[]'::json)
                ) ORDER BY cm.order_index
            ) as modules_data
        FROM public.course_modules cm
        LEFT JOIN (
            SELECT 
                cl.module_id,
                json_agg(row_to_json(cl.*) ORDER BY cl.order_index) as lessons_data
            FROM public.course_lessons cl
            GROUP BY cl.module_id
        ) lessons ON lessons.module_id = cm.id
        WHERE cm.course_id = course_uuid
        GROUP BY cm.course_id
    ) modules ON modules.course_id = c.id
    LEFT JOIN (
        SELECT 
            cf.course_id,
            json_agg(row_to_json(cf.*)) as files_data
        FROM public.course_files cf
        WHERE cf.course_id = course_uuid
        GROUP BY cf.course_id
    ) files ON files.course_id = c.id
    WHERE c.id = course_uuid;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;