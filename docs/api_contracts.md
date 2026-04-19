# 🤝 Contratos de API: GlowStudio AI ↔ n8n

Este documento define os payloads JSON que o Streamlit envia para o n8n e o que ele espera receber de volta. Use estes esquemas para configurar seus nós de Webhook no n8n.

---

## 1. Geração de Texto (Maritaca AI)
**Endpoint:** `N8N_WEBHOOK_TEXT`  
**Objetivo:** Gerar a legenda de venda e o prompt visual para a imagem.

### Payload de Envio (Streamlit → n8n)
```json
{
  "image_base64": "data:image/png;base64,...",
  "objetivo": "Venda Direta",
  "publico": "Noivas",
  "diferenciais": ["Ouro 18k", "Hipoalergênico"],
  "etapa": "gerar_texto",
  "timestamp": "2026-04-13T..."
}
```

### Resposta Esperada (n8n → Streamlit)
```json
{
  "success": true,
  "legenda": "Descubra o brilho que você merece...",
  "prompt_visual": "Elegant Brazilian model in a white dress, wearing a delicate gold necklace, soft studio lighting..."
}
```

---

## 2. Geração de Imagem (Fal.ai)
**Endpoint:** `N8N_WEBHOOK_IMAGE`  
**Objetivo:** Fundir a joia real com a modelo gerada por IA.

### Payload de Envio (Streamlit → n8n)
```json
{
  "image_base64": "data:image/png;base64,...",
  "prompt_visual": "Elegant Brazilian model wearing...",
  "objetivo": "Venda Direta",
  "publico": "Noivas",
  "etapa": "gerar_imagem"
}
```

### Resposta Esperada (n8n → Streamlit)
```json
{
  "success": true,
  "images": [
    { "url": "https://..." },
    { "url": "https://..." }
  ]
}
```

---

## 3. Geração de Vídeo (Kling/Hedra)
**Endpoint:** `N8N_WEBHOOK_VIDEO`  
**Objetivo:** Animar a imagem aprovada.

### Payload de Envio (Streamlit → n8n)
```json
{
  "image_url": "https://...",
  "image_base64": "data:image/png;base64,...",
  "prompt": "Soft head movement, subtle smile, golden hour lighting",
  "etapa": "gerar_video"
}
```

### Resposta Esperada (n8n → Streamlit)
```json
{
  "success": true,
  "video_url": "https://...",
  "message": "Vídeo processado com sucesso"
}
```

---

## ⚠️ Observações de Infraestrutura (Skill 5)
1. **Tamanho do Payload:** Se o Nginx do n8n estiver com o padrão de 1MB, as requisições com Base64 falharão. Certifique-se de que o `client_max_body_size` esteja em pelo menos `10M`.
2. **Autenticação:** O Streamlit enviará o Header `Authorization: Bearer <N8N_API_KEY>` se ela estiver configurada no `.env`.
