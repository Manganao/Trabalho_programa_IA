# Conexão com API de IA - Claude (Anthropic)

Atividade prática: configurar ambiente e validar comunicação com API de Inteligência Artificial.

## 📋 Descrição

Script Python que conecta à API da **Anthropic (Claude)** e permite um chat interativo em português, similar ao exemplo com Gemini fornecido na atividade.

## 🚀 Como usar

### 1. Instalar dependência

```bash
pip install anthropic
```

### 2. Obter sua chave de API (gratuita)

- Acesse: https://console.anthropic.com/
- Crie uma conta gratuita
- Vá em **API Keys** e gere uma nova chave

### 3. Configurar a chave no script

Abra o arquivo `claude_api_test.py` e substitua:

```python
ANTHROPIC_API_KEY = "SUA_CHAVE_AQUI"
```

### 4. Executar

```bash
python claude_api_test.py
```

## 💬 Exemplo de uso

```
==================================================
  Conexão com API da Anthropic (Claude)
==================================================

✅ Conexão estabelecida com sucesso!
   Modelo: claude-3-5-haiku-20241022
   Status: Online

Digite 'sair' para encerrar.

Faça uma pergunta: Qual é a capital do Brasil?

Claude: A capital do Brasil é Brasília.

Faça uma pergunta ou digite sair para encerrar: sair

Encerrando... Até mais!
```

## 🔑 Sobre a API

- **Provedor:** Anthropic
- **Modelo:** claude-3-5-haiku-20241022
- **Plano gratuito:** Sim, disponível em https://console.anthropic.com/
- **Documentação:** https://docs.anthropic.com
