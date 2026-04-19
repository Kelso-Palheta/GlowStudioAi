# 📄 Proposta de Implementação: GlowStudio AI — Visão Consolidada

Este documento resume o diagnóstico do projeto, a visão de produto desejada e as orientações técnicas para a próxima fase de desenvolvimento. Destina-se a orientar a implementação de um fluxo completo de criação de conteúdo para semijoias utilizando IA.

---

## 1. Visão Geral do Projeto
O **GlowStudio AI** é um ecossistema para lojistas de semijoias. O objetivo é transformar uma foto simples de uma peça real em um conteúdo de marketing de luxo (fotos e vídeos) com uma modelo virtual consistente.

### Status Atual (Diagnóstico)
- **Implementado:** Upload de fotos, UI básica em Streamlit, integração estrutural com n8n/APIs (Fal.ai, Maritaca).
- **Lacunas Críticas:** 
    - A IA gera modelos aleatórias em cada execução (falta de consistência).
    - Não há "inpainting" real (a joia não é mesclada com a modelo com precisão).
    - O fluxo de vídeo está incompleto (falta integração funcional).
    - A copy (legenda) está em modo demonstrativo (mock).

---

## 2. Requisitos de Negócio (A Visão do Usuário)
O usuário deseja que a plataforma permita:
1. **Modelo Constante:** Definir uma modelo virtual única (rosto persistente) para ser a "cara" da marca no Instagram.
2. **Personalização de Ambiente e Look:** Trocar roupas, cenários (praia, estúdio, escritório) e iluminação, mantendo a mesma modelo e a joia real.
3. **Criação de Vídeos Integrada:** Gerar vídeos da modelo (movimento suave ou falando) diretamente na plataforma, sem precisar sair do sistema.
4. **Copy Persuasiva:** Legendas de alta conversão geradas por IA (Maritaca) baseadas no público e objetivo.

---

## 3. Soluções Propostas e Arquitetura Técnica

### A. Consistência de Identidade (A Mesma Modelo)
Para manter o rosto da modelo constante enquanto muda o corpo, roupa e fundo:
- **Tecnologia:** [Fal.ai](https://fal.ai) utilizando **IP-Adapter FaceID** ou treinamento de um **LoRA** específico para o rosto da modelo.
- **Fluxo:** 
    1. O usuário cria ou escolhe uma "Modelo de Referência" (Step 0).
    2. Essa imagem de referência é enviada para a API em cada geração para "ancorar" a identidade visual.

### B. Inpainting de Alta Precisão (Vestindo a Joia)
Para garantir que a joia real do lojista apareça perfeitamente na modelo:
- **Tecnologia:** Fal.ai (Flux Inpainting ou modelos SDXL especializados).
- **Fluxo:** A foto da semijoia é processada e inserida na área correta (pescoço, orelha) da imagem da modelo gerada, respeitando sombras e texturas.

### C. Estúdio de Vídeo Integrado
- **Opção Movimento (Cinematográfico):** Integração com **Kling AI** ou **Luma Dream Machine** via API para animar a imagem estática gerada.
- **Opção Avatar Falante:** Integração com **Hedra** para fazer a modelo falar as legendas geradas.

---

## 4. Estrutura de Telas Sugerida (Streamlit)

### Etapa 0: Minha Modelo (Configuração Única)
- Interface para gerar ou fazer upload da modelo de rosto padrão.
- Salvamento de metadados da modelo para persistência.

### Etapa 1: Showroom de Semijoias
- Upload da peça real + Seleção de Estratégia (Público, Objetivo).

### Etapa 2: Direção de Arte e Look
- Seleção de Cenário (Ex: "Mansão de Luxo", "Natureza").
- Seleção de Look/Roupa (Ex: "Vestido de Seda", "Look Executivo").
- Revisão da Legenda (Maritaca AI ativa).

### Etapa 3: Estúdio de Resultados
- Galeria de fotos geradas com a joia.
- Central de Vídeo: Selecionar imagem → Escolher Estilo de Animação → Baixar MP4.

---

## 5. Próximos Passos para Implementação (Roadmap)

1. **Ativação da Inteligência de Copy:** Configurar `MARITACA_API_KEY` e refinar prompts para gerar roteiros específicos por público.
2. **Módulo "Minha Modelo":** Criar o sistema de upload/geração de referência estável.
3. **Integração de Inpainting Real:** Mudar de geração puramente textual para fluxo de imagem-para-imagem (FaceID + Jewelry Overlay).
4. **Webhook de Vídeo:** Conectar as APIs de vídeo (Kling/Hedra) ao botão "Animar" existente.

---
*Este documento consolida a visão estratégica para a fase 2.0 do GlowStudio AI.*
