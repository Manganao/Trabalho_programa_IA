# Conexão com API de IA - Claude (Anthropic) via LangChain

Atividade prática: configurar ambiente e validar comunicação com API de Inteligência Artificial usando o framework **LangChain**.

## 📋 Descrição

Script Python que conecta à API da **Anthropic (Claude)** através do framework **LangChain** e permite um chat interativo em português, com histórico de conversa e sistema de diagnóstico mecânico integado a banco de dados PostgreSQL.

## 🚀 Como usar

### 1. Instalar dependências

```bash
pip install langchain-anthropic langchain-core
```

> **Nota:** `langchain-core` já é instalado automaticamente como dependência do `langchain-anthropic`, mas pode ser instalado separadamente se necessário.  
> **Não use** `pip install langchain_core.prompts` ou `pip install langchain_core.messages` — esses são módulos internos do pacote, não pacotes separados.

### 2. Obter sua chave de API (gratuita)

- Acesse: https://console.anthropic.com/
- Crie uma conta gratuita
- Vá em **API Keys** e gere uma nova chave

### 3. Configurar a chave no script

Abra o arquivo e substitua:

```python
ANTHROPIC_API_KEY = "SUA_CHAVE_AQUI"
```

Ou use um arquivo `.env`:

```env
ANTHROPIC_API_KEY=sua_chave_aqui
```

### 4. Executar

```bash
python oficina_langchain.py
```

## 💬 Exemplo de uso

```
==================================================
  Conexão com API da Anthropic via LangChain
==================================================

✅ Conexão estabelecida com sucesso!
   model=claude-haiku-4-5-20251001
   Status: Online

Digite 'sair' para encerrar.

Faça uma pergunta: Qual é a capital do Brasil?

Claude: A capital do Brasil é Brasília.

Faça uma pergunta ou digite sair para encerrar: sair

Encerrando... Até mais!
```

## 🔧 Principais alterações em relação à versão sem LangChain

| O que era (SDK nativo) | O que virou (LangChain) |
|---|---|
| `anthropic.Anthropic()` | `ChatAnthropic()` de `langchain_anthropic` |
| `client.messages.create(...)` | `chain.invoke(...)` com `prompt \| llm` |
| `{"role": "user", "content": "..."}` | `HumanMessage(content="...")` |
| `{"role": "assistant", "content": "..."}` | `AIMessage(content="...")` |
| `resposta.content[0].text` | `resposta.content` |
| Prompt como string solta | `ChatPromptTemplate.from_messages([...])` |

## 🔑 Sobre a API e o framework

- **Provedor:** Anthropic
- **Framework:** LangChain
- **Modelo:** claude-haiku-4-5-20251001
- **Plano gratuito:** Sim, disponível em https://console.anthropic.com/
- **Documentação Anthropic:** https://docs.anthropic.com
- **Documentação LangChain:** https://python.langchain.com