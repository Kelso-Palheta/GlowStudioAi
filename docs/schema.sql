-- ============================================
-- GlowStudio AI - Database Schema (Fase 3)
-- ============================================

-- 1. Criar tabela de Gerações
CREATE TABLE IF NOT EXISTS public.generations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    
    -- Conteúdo
    type TEXT CHECK (type IN ('image', 'video')),
    image_url TEXT,
    caption TEXT,
    prompt TEXT,
    
    -- Metadados da Estratégia
    marketing_objective TEXT,
    target_audience TEXT,
    features JSONB DEFAULT '[]'::jsonb,
    
    -- Referência de arquivo original (opcional)
    original_image_url TEXT
);

-- 2. Habilitar RLS (Row Level Security)
-- Isso garante que um usuário NUNCA veja os dados de outro.
ALTER TABLE public.generations ENABLE ROW LEVEL SECURITY;

-- 3. Criar Políticas de Acesso
-- Política: Usuários podem ver apenas suas próprias gerações
CREATE POLICY "Users can view their own generations" 
ON public.generations 
FOR SELECT 
USING (auth.uid() = user_id);

-- Política: Usuários podem inserir suas próprias gerações
CREATE POLICY "Users can insert their own generations" 
ON public.generations 
FOR INSERT 
WITH CHECK (auth.uid() = user_id);

-- Política: Usuários podem deletar suas próprias gerações
CREATE POLICY "Users can delete their own generations" 
ON public.generations 
FOR DELETE 
USING (auth.uid() = user_id);
