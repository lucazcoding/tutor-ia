import os
import io
from gtts import gTTS
from gpt4all import GPT4All

# Configuração do modelo
MODEL_NAME = "qwen2-1_5b-instruct-q4_0.gguf"
try:
    model = GPT4All(MODEL_NAME, model_path=".")
    print(f"Modelo {MODEL_NAME} carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    raise

SYSTEM_PROMPT_IA_MANEIRA = """
Você é um tutor de inglês que fala português brasileiro de forma divertida, usando gírias e um tom descontraído. Sua tarefa é responder SOMENTE à última mensagem do usuário, sem repetir, incluir ou mencionar mensagens anteriores. Forneça uma resposta curta e focada em ajudar com inglês (ex.: explicando vocabulário, gramática ou respondendo perguntas relacionadas). Não simule o aluno, não agradeça, não peça feedback e não continue a conversa além da resposta direta. Use no máximo 100 palavras.
"""

def generate_speech_from_text(text_to_speak, use_gtts=True):
    """Gera áudio a partir de texto usando gTTS (online)."""
    try:
        tts = gTTS(text=text_to_speak, lang='pt-br', slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer.read()
    except Exception as e:
        print(f"Erro ao gerar áudio: {e}")
        return None

def chat_listmessages(mensagem_usuario, historico_mensagens):
    """
    Interage com o GPT4All local, enviando apenas o prompt do sistema e a mensagem atual.
    """
    # Garante que historico_mensagens seja uma lista válida
    if not isinstance(historico_mensagens, list):
        print("Erro: historico_mensagens não é uma lista, reiniciando...")
        historico_mensagens = []

    # Adiciona o prompt do sistema se necessário
    if not historico_mensagens or (historico_mensagens and isinstance(historico_mensagens[0], dict) and historico_mensagens[0].get("role") != "system"):
        print("Adicionando prompt do sistema ao histórico")
        historico_mensagens.insert(0, {"role": "system", "content": SYSTEM_PROMPT_IA_MANEIRA})

    # Cria contexto apenas com o prompt do sistema e a mensagem atual
    system_prompt = historico_mensagens[0]["content"] if historico_mensagens and historico_mensagens[0].get("role") == "system" else SYSTEM_PROMPT_IA_MANEIRA
    contexto = f"{system_prompt}\nUsuário: {mensagem_usuario}\nIA:"
    print(f"Contexto enviado ao modelo: {contexto}")

    try:
        # Remove o parâmetro 'stop' para compatibilidade com versões antigas
        resposta_assistente = model.generate(
            contexto,
            max_tokens=100,  # Limita a resposta a 100 tokens
            temp=0.7,       # Reduz a criatividade para respostas mais focadas
            top_p=0.9       # Controla a probabilidade cumulativa
        )
        print(f"Resposta do modelo: {resposta_assistente}")
        # Limpa a resposta para remover qualquer conteúdo indesejado
        resposta_assistente = resposta_assistente.strip().split('\n')[0]
    except Exception as e:
        print(f"Erro ao gerar resposta do modelo: {e}")
        raise

    # Atualiza o histórico
    historico_mensagens.append({"role": "user", "content": mensagem_usuario})
    historico_mensagens.append({"role": "assistant", "content": resposta_assistente})

    return resposta_assistente, historico_mensagens

def enviar_mensagem_para_ia(mensagem, historico):
    """Função wrapper para enviar mensagem para IA."""
    resposta, historico_atualizado = chat_listmessages(mensagem, historico)
    return resposta, historico_atualizado