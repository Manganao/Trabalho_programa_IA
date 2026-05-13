"""
Diagnóstico de Problemas Mecânicos em Automóveis
API: Anthropic (Claude) via LangChain
Banco de dados: PostgreSQL

ALTERAÇÕES REALIZADAS:
- Substituído o cliente 'anthropic' diretamente pelo wrapper LangChain 'ChatAnthropic'
- Substituído client.messages.create() por chains LangChain (prompt | llm)
- Adicionado ChatPromptTemplate para estruturar os prompts de forma declarativa
- Adicionado SystemMessage / HumanMessage para o histórico de conversa no chat
- O histórico de conversa agora usa objetos de mensagem LangChain em vez de dicts simples
"""

# ──────────────────────────────────────────────
# ALTERAÇÃO: importações do LangChain substituem
# o SDK nativo da Anthropic para chamadas à IA
# ──────────────────────────────────────────────
from langchain_anthropic import ChatAnthropic          # Substitui: anthropic.Anthropic()
from langchain_core.prompts import ChatPromptTemplate  # Substitui: strings de prompt manuais
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage  # Substitui: dicts {"role": ..., "content": ...}

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 5432)),
    "dbname":   os.getenv("DB_NAME", "oficina"),
    "user":     os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "")
}

# Prompts permanecem como strings — são passados ao ChatPromptTemplate
SYSTEM_PROMPT_NORMAL = """Você é um mecânico especialista com mais de 20 anos de experiência em automóveis.
Seu papel é diagnosticar problemas mecânicos com base nos sintomas descritos.

Para cada diagnóstico, siga esta estrutura:
1. **Sintomas identificados** — liste o que foi descrito
2. **Possíveis causas** — do mais provável ao menos provável
3. **Diagnóstico principal** — sua conclusão mais provável
4. **Urgência** — Baixa / Média / Alta / Crítica
5. **Próximos passos** — o que deve ser feito
6. **Estimativa de custo** — faixa de preço aproximada no Brasil (em R$)

Responda sempre em português."""

SYSTEM_PROMPT_CAVEMAN = """Mecânico especialista. Diagnostique problemas mecânicos.
Modo caveman: respostas ultra-curtas. Sem enrolação. Só o essencial.

Formato obrigatório (fragmentos, sem frases completas):
- Causa: [mais provável]
- Urgência: Baixa/Média/Alta/Crítica
- Fazer: [próximo passo]
- Custo: R$ [faixa]

Sem cumprimentos. Sem explicações óbvias. Direto ao ponto. Português."""

MODO = "normal"


# =============================================
# CONEXÃO COM O BANCO (sem alterações)
# =============================================
def conectar():
    return psycopg2.connect(**DB_CONFIG)

def testar_conexao():
    try:
        conectar().close()
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar no banco: {e}")
        return False


# =============================================
# CADASTROS (sem alterações)
# =============================================
def cadastrar_cliente():
    print("\n── Cadastrar Cliente ──")
    nome = input("Nome: ").strip()
    telefone = input("Telefone: ").strip()
    email = input("Email: ").strip()

    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO clientes (nome, telefone, email) VALUES (%s, %s, %s) RETURNING id",
                (nome, telefone, email)
            )
            id_novo = cur.fetchone()[0]
        conn.commit()
    print(f"✅ Cliente cadastrado com ID {id_novo}!")
    return id_novo


def listar_clientes():
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nome, telefone FROM clientes ORDER BY nome")
            return cur.fetchall()


def cadastrar_veiculo():
    print("\n── Cadastrar Veículo ──")
    clientes = listar_clientes()
    if not clientes:
        print("Nenhum cliente cadastrado. Cadastre um cliente primeiro.")
        cadastrar_cliente()
        clientes = listar_clientes()

    print("\nClientes cadastrados:")
    for c in clientes:
        print(f"  [{c[0]}] {c[1]} — {c[2]}")

    cliente_id = input("\nID do cliente: ").strip()
    placa  = input("Placa: ").strip().upper()
    marca  = input("Marca (ex: Volkswagen): ").strip()
    modelo = input("Modelo (ex: Gol): ").strip()
    ano    = input("Ano: ").strip()
    cor    = input("Cor: ").strip()

    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO veiculos (cliente_id, placa, marca, modelo, ano, cor)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """, (cliente_id, placa, marca, modelo, int(ano), cor))
            id_novo = cur.fetchone()[0]
        conn.commit()
    print(f"✅ Veículo {marca} {modelo} ({placa}) cadastrado com ID {id_novo}!")


def cadastrar_peca():
    print("\n── Cadastrar Peça ──")
    nome       = input("Nome da peça: ").strip()
    descricao  = input("Descrição: ").strip()
    quantidade = input("Quantidade em estoque: ").strip()
    preco      = input("Preço unitário (R$): ").strip().replace(",", ".")
    minimo     = input("Estoque mínimo: ").strip()

    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO pecas (nome, descricao, quantidade, preco_unitario, estoque_minimo)
                VALUES (%s, %s, %s, %s, %s) RETURNING id
            """, (nome, descricao, int(quantidade), float(preco), int(minimo)))
            id_novo = cur.fetchone()[0]
        conn.commit()
    print(f"✅ Peça '{nome}' cadastrada com ID {id_novo}!")


def listar_veiculos():
    print("\n── Veículos Cadastrados ──")
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT v.placa, v.marca, v.modelo, v.ano, c.nome
                FROM veiculos v
                JOIN clientes c ON c.id = v.cliente_id
                ORDER BY v.marca, v.modelo
            """)
            veiculos = cur.fetchall()

    if not veiculos:
        print("Nenhum veículo cadastrado.")
        return

    for v in veiculos:
        print(f"  {v[0]} — {v[1]} {v[2]} {v[3]} | Cliente: {v[4]}")


def listar_pecas():
    print("\n── Estoque de Peças ──")
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT nome, quantidade, estoque_minimo, preco_unitario FROM pecas ORDER BY nome")
            pecas = cur.fetchall()

    if not pecas:
        print("Nenhuma peça cadastrada.")
        return

    for p in pecas:
        alerta = " ⚠️" if p[1] <= p[2] else ""
        print(f"  {p[0]}: {p[1]} un | Mínimo: {p[2]} | R$ {p[3]:.2f}{alerta}")


# =============================================
# DIAGNÓSTICO
# =============================================
def buscar_veiculo_por_placa(placa):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT v.id, v.placa, v.marca, v.modelo, v.ano, v.cor,
                       c.nome, c.telefone
                FROM veiculos v
                JOIN clientes c ON c.id = v.cliente_id
                WHERE UPPER(v.placa) = UPPER(%s)
            """, (placa,))
            return cur.fetchone()


def listar_diagnosticos_veiculo(veiculo_id):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT sintomas, urgencia, criado_em
                FROM diagnosticos
                WHERE veiculo_id = %s
                ORDER BY criado_em DESC LIMIT 5
            """, (veiculo_id,))
            return cur.fetchall()


def salvar_diagnostico(veiculo_id, sintomas, resultado, urgencia):
    urgencia_map = {
        "baixa": "baixa", "média": "media", "media": "media",
        "alta": "alta", "crítica": "critica", "critica": "critica"
    }
    urgencia_db = urgencia_map.get(urgencia.lower(), "media")
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO diagnosticos (veiculo_id, sintomas, resultado_ia, urgencia)
                VALUES (%s, %s, %s, %s)
            """, (veiculo_id, sintomas, resultado, urgencia_db))
        conn.commit()


def extrair_urgencia(texto):
    t = texto.lower()
    if "crítica" in t or "critica" in t: return "critica"
    if "alta" in t:                       return "alta"
    if "média" in t or "media" in t:      return "media"
    return "baixa"


def fazer_diagnostico(llm):
    """
    ALTERAÇÃO: o parâmetro antes era 'client' (anthropic.Anthropic).
    Agora é 'llm' (ChatAnthropic do LangChain).

    A chamada direta à API foi substituída por uma chain LangChain:
        prompt_template | llm
    Isso permite trocar o modelo ou o provedor sem alterar o restante do código.
    """
    print("\n── Diagnóstico por IA ──")
    placa = input("Placa do veículo: ").strip().upper()

    veiculo = buscar_veiculo_por_placa(placa)
    if not veiculo:
        print(f"❌ Veículo '{placa}' não encontrado. Cadastre-o primeiro.\n")
        return

    v_id, v_placa, v_marca, v_modelo, v_ano, v_cor, cliente, telefone = veiculo
    print(f"\n🚗 {v_marca} {v_modelo} {v_ano} ({v_cor})")
    print(f"👤 {cliente} — {telefone}")

    historico_db = listar_diagnosticos_veiculo(v_id)
    if historico_db:
        print(f"\n📋 Histórico deste veículo:")
        for d in historico_db:
            data = d[2].strftime("%d/%m/%Y")
            print(f"   • [{data}] {d[1]} — {d[0][:60]}...")

    sintomas = input("\nDescreva os sintomas: ").strip()
    if not sintomas:
        return

    # ──────────────────────────────────────────────────────────────
    # ALTERAÇÃO: construção do prompt com ChatPromptTemplate
    #
    # Antes (SDK nativo):
    #   resposta = client.messages.create(
    #       model="claude-haiku-4-5-20251001",
    #       max_tokens=1024,
    #       system=prompt,
    #       messages=[{"role": "user", "content": f"Veículo: ..."}]
    #   )
    #   resultado = resposta.content[0].text
    #
    # Agora (LangChain):
    #   - ChatPromptTemplate.from_messages() declara a estrutura do prompt
    #   - A chain (prompt_template | llm) é invocada com .invoke()
    #   - O resultado já vem como objeto AIMessage; .content extrai o texto
    # ──────────────────────────────────────────────────────────────
    system_prompt = SYSTEM_PROMPT_CAVEMAN if MODO == "caveman" else SYSTEM_PROMPT_NORMAL

    # Cria o template com mensagem de sistema e mensagem do usuário
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Veículo: {marca} {modelo} {ano}\nSintomas: {sintomas}")
    ])

    # Compõe a chain: template → modelo
    chain = prompt_template | llm

    print(f"\n⏳ Analisando... (modo: {MODO})\n")

    # Invoca a chain passando as variáveis do template
    resposta = chain.invoke({
        "marca": v_marca,
        "modelo": v_modelo,
        "ano": v_ano,
        "sintomas": sintomas
    })

    # ALTERAÇÃO: antes era resposta.content[0].text (SDK Anthropic)
    # Agora é resposta.content (atributo do AIMessage do LangChain)
    resultado = resposta.content
    urgencia  = extrair_urgencia(resultado)

    print(f"🔍 Diagnóstico:\n\n{resultado}\n")
    salvar_diagnostico(v_id, sintomas, resultado, urgencia)
    print(f"✅ Diagnóstico salvo! (urgência: {urgencia})")


# =============================================
# MENU PRINCIPAL
# =============================================
def menu():
    print("=" * 55)
    print("   🔧 OFICINA MECÂNICA — Sistema de Diagnóstico")
    print("   Powered by Claude (via LangChain) + PostgreSQL")
    print("=" * 55)

    if not testar_conexao():
        return
    print("✅ Banco conectado!")

    # ──────────────────────────────────────────────────────────────
    # ALTERAÇÃO: instanciação do modelo
    #
    # Antes (SDK nativo):
    #   client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    #
    # Agora (LangChain):
    #   llm = ChatAnthropic(...)
    #   O wrapper LangChain gerencia a autenticação e a chamada HTTP.
    #   max_tokens é definido aqui, não em cada chamada.
    # ──────────────────────────────────────────────────────────────
    llm = ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        api_key=ANTHROPIC_API_KEY,
        max_tokens=1024
    )
    print("✅ Modelo LangChain (ChatAnthropic) pronto!\n")

    opcoes = {
        "1": ("🔍 Fazer diagnóstico com IA",  lambda: fazer_diagnostico(llm)),
        "2": ("👤 Cadastrar cliente",          cadastrar_cliente),
        "3": ("🚗 Cadastrar veículo",          cadastrar_veiculo),
        "4": ("🔩 Cadastrar peça no estoque",  cadastrar_peca),
        "5": ("📋 Listar veículos",            listar_veiculos),
        "6": ("📦 Listar estoque de peças",    listar_pecas),
        "0": ("🚪 Sair",                       None),
    }

    while True:
        global MODO
        modo_label = "🪨 caveman" if MODO == "caveman" else "🔍 normal"
        print(f"\n─────────────────────────────")
        print(f"  Modo IA: {modo_label}")
        print(f"─────────────────────────────")
        for k, (desc, _) in opcoes.items():
            print(f"  [{k}] {desc}")
        print(f"  [7] 🪨 Alternar modo caveman")
        print("─────────────────────────────")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "0":
            print("\nEncerrando... Até mais! 🔧")
            break
        elif escolha == "7":
            MODO = "caveman" if MODO == "normal" else "normal"
            print(f"✅ Modo alterado para: {MODO}")
        elif escolha in opcoes:
            try:
                opcoes[escolha][1]()
            except Exception as e:
                print(f"❌ Erro: {e}")
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()


# ==============================================================================
# CHATBOT SIMPLES COM HISTÓRICO — também adaptado para LangChain
# ==============================================================================
"""
ALTERAÇÕES NO CHATBOT:
- Substituído anthropic.Anthropic() por ChatAnthropic do LangChain
- O histórico de conversa agora usa objetos SystemMessage / HumanMessage / AIMessage
  em vez de dicts {"role": "user"/"assistant", "content": "..."}
- A chamada client.messages.create() foi substituída por llm.invoke(historico)
- O texto da resposta é acessado via resposta.content (AIMessage) em vez de
  resposta.content[0].text (SDK nativo)
"""

def iniciar_chat():
    """Inicia um chat interativo com o Claude via LangChain."""

    # ALTERAÇÃO: ChatAnthropic substitui anthropic.Anthropic()
    llm = ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        api_key=ANTHROPIC_API_KEY,
        max_tokens=1024
    )

    print("=" * 50)
    print("  Conexão com API da Anthropic via LangChain")
    print("=" * 50)
    print("\n✅ Conexão estabelecida com sucesso!")
    print("   model=claude-haiku-4-5-20251001")
    print("   Status: Online\n")
    print("   /caveman — ativa o modo padrão (full)")
    print("   /caveman lite — versão menos agressiva")
    print("   /caveman ultra — compressão máxima")

    # ──────────────────────────────────────────────────────────────
    # ALTERAÇÃO: histórico agora usa objetos de mensagem LangChain
    #
    # Antes:
    #   historico = [
    #       {"role": "user",      "content": "Responda apenas em português."},
    #       {"role": "assistant", "content": "Entendido!"}
    #   ]
    #
    # Agora:
    #   historico = [
    #       SystemMessage(content="..."),   ← instrução de sistema
    #       HumanMessage(content="..."),    ← mensagem do usuário
    #       AIMessage(content="...")        ← resposta do modelo
    #   ]
    # ──────────────────────────────────────────────────────────────
    historico = [
        SystemMessage(content="Responda as perguntas apenas em português."),
        HumanMessage(content="Entendido?"),
        AIMessage(content="Entendido! Responderei apenas em português.")
    ]

    print("Digite 'sair' para encerrar.\n")
    pergunta = input("Faça uma pergunta: ")

    while pergunta.lower() != "sair":
        # Adiciona a mensagem do usuário ao histórico como HumanMessage
        historico.append(HumanMessage(content=pergunta))

        # ALTERAÇÃO: antes era client.messages.create(messages=historico)
        # Agora é llm.invoke(historico) — mais simples e idiomático no LangChain
        resposta = llm.invoke(historico)

        # ALTERAÇÃO: antes era resposta.content[0].text (SDK Anthropic)
        # Agora é resposta.content (string direta no AIMessage do LangChain)
        texto_resposta = resposta.content

        # Adiciona a resposta ao histórico como AIMessage para manter contexto
        historico.append(AIMessage(content=texto_resposta))

        print(f"\nClaude: {texto_resposta}\n")
        pergunta = input("Faça uma pergunta ou digite sair para encerrar: ")

    print("\nEncerrando... Até mais!")