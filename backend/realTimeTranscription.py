# import numpy as np
# import queue
# import threading
# import sounddevice as sd
# from faster_whisper import WhisperModel

# # CONFIGURAÇÕES
# samplerate = 16000  # taxa de amostragem exigida pelo Whisper
# channels = 1  # áudio mono
# chunk_duration = 0.5  # em segundos (ajuste: 0.3 ~ 1.0 para fluidez x precisão)
# frames_per_chunk = int(samplerate * chunk_duration)

# # FILA DE ÁUDIO
# audio_queue = queue.Queue()
# audio_buffer = []

# # MODELO GPU
# # Você pode trocar por "small", "medium", ou "large-v3"
# model = WhisperModel("medium", device="cuda", compute_type="float16")

# def audio_callback(indata, frames, time, status):
#     if status:
#         print("⚠️ Status do microfone:", status)
#     audio_queue.put(indata.copy())

# def recorder():
#     with sd.InputStream(samplerate=samplerate, channels=channels,
#                         callback=audio_callback, blocksize=frames_per_chunk):
#         print("🎙️ Listening... Pressione Ctrl+C para parar.")
#         while True:
#             sd.sleep(1000)

# def transcriber():
#     global audio_buffer
#     while True:
#         block = audio_queue.get()
#         audio_buffer.append(block)

#         total_frames = sum(len(b) for b in audio_buffer)
#         if total_frames >= frames_per_chunk:
#             audio_data = np.concatenate(audio_buffer, axis=0)[:frames_per_chunk]
#             audio_buffer = []

#             # Conversão para float32 (formato exigido)
#             audio_data = audio_data.flatten().astype(np.float32)

#             try:
#                 segments, _ = model.transcribe(audio_data, language="pt", beam_size=1)
#                 for segment in segments:
#                     print(f">> {segment.text.strip()}")
#             except Exception as e:
#                 print("❌ Erro na transcrição:", e)

# # INICIALIZAÇÃO
# if __name__ == "__main__":
#     threading.Thread(target=recorder, daemon=True).start()
#     transcriber()
