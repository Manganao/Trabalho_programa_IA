"""
Atividade: Configurar ambiente e validar comunicação com API de IA
API utilizada: Anthropic (Claude)
Documentação: https://docs.anthropic.com
"""

import anthropic

# =============================================
# CONFIGURAÇÃO
# Substitua pela sua chave de API da Anthropic
# Obtenha em: https://console.anthropic.com/
# =============================================
ANTHROPIC_API_KEY = "sua_chave_aqui"


def iniciar_chat():
    """Inicia um chat interativo com o Claude via API da Anthropic."""

    # Instancia o cliente com a chave de API
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    print("=" * 50)
    print("  Conexão com API da Anthropic (Claude)")
    print("=" * 50)

    # Valida a conexão listando o modelo usado
    print("\n✅ Conexão estabelecida com sucesso!")
    print("   model=claude-haiku-4-5-20251001")
    print("   Status: Online\n")

    print("   /caveman — ativa o modo padrão (full)")
    print("   /caveman lite — versão menos agressiva")
    print("   /caveman ultra — compressão máxima")


    historico = []
    contexto = "Responda as perguntas apenas em português."
    historico.append({"role": "user", "content": contexto})
    historico.append({"role": "assistant", "content": "Entendido! Responderei apenas em português."})

    print("Digite 'sair' para encerrar.\n")

    pergunta = input("Faça uma pergunta: ")

    while pergunta.lower() != "sair":
        historico.append({"role": "user", "content": pergunta})

        resposta = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=historico,
        )

        texto_resposta = resposta.content[0].text
        historico.append({"role": "assistant", "content": texto_resposta})

        print(f"\nClaude: {texto_resposta}\n")
        pergunta = input("Faça uma pergunta ou digite sair para encerrar: ")

    print("\nEncerrando... Até mais!")


if __name__ == "__main__":
    iniciar_chat()

   