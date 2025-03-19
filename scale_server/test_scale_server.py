import socket
import wave
import struct

# ==== ПАРАМЕТРЫ UDP ====
UDP_IP = "0.0.0.0"  # Принимаем данные от всех
UDP_PORT = 5005     # Порт (должен совпадать с ESP8266)
PACKET_SIZE = 256   # Размер пакета (128 сэмплов * 2 байта)

# ==== ПАРАМЕТРЫ АУДИО ====
SAMPLE_RATE = 16000  # Частота дискретизации 16 кГц
SAMPLE_WIDTH = 2     # 16 бит (2 байта)
CHANNELS = 1         # Моно

# ==== СОЗДАЁМ UDP-СОКЕТ ====
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# ==== СОЗДАЁМ WAV-ФАЙЛ ====
filename = f"received_audio.wav"  # Имя файла с меткой времени
wav_file = wave.open(filename, "wb")
wav_file.setnchannels(CHANNELS)
wav_file.setsampwidth(SAMPLE_WIDTH)
wav_file.setframerate(SAMPLE_RATE)

print(f"🎙️  Приём аудио на {UDP_IP}:{UDP_PORT}...")

# ==== ГЛАВНЫЙ ЦИКЛ ====
try:
    packet_count = 0
    audio_data = bytearray()

    while True:
        data, addr = sock.recvfrom(PACKET_SIZE)  # Получаем данные
        packet_count += 1

        # Добавляем принятые данные в буфер
        audio_data.extend(data)

        # Каждые 100 пакетов (~0.8 сек) записываем в WAV
        if packet_count % 100 == 0:
            wav_file.writeframes(audio_data)  # Записываем в файл
            print(f"📦 Получено пакетов: {packet_count}  ({len(audio_data)} байт)")
            audio_data.clear()  # Очищаем буфер

except KeyboardInterrupt:
    print("\n❌ Остановка сервера...")

finally:
    # Сохраняем финальные данные и закрываем файл
    if audio_data:
        wav_file.writeframes(audio_data)
    wav_file.close()
    sock.close()
    print(f"✅ Файл сохранён: {filename}")
