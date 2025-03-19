import socket
import wave
import struct
import time

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
    
    # Начальное время
    start_time = time.time()

    while True:
        data, addr = sock.recvfrom(PACKET_SIZE)  # Получаем данные
        packet_count += 1

        # Добавляем принятые данные в буфер
        audio_data.extend(data)

        # Каждые 100 пакетов (~0.8 сек) выводим статистику
        if packet_count % 100 == 0:
            print(f"📦 Получено пакетов: {packet_count}  ({len(audio_data)} байт)")

        # Если прошло 10 секунд — сохраняем данные и ждём 5 секунд
        if time.time() - start_time >= 10:
            # Записываем аудиофайл
            wav_file.writeframes(audio_data)
            print(f"✅ Записано 10 секунд аудио ({len(audio_data)} байт) в файл.")
            audio_data.clear()  # Очищаем буфер

            # Ожидаем 5 секунд
            print("⏳ Ожидание 5 секунд...")
            time.sleep(5)

            # Обновляем стартовое время для следующего блока
            start_time = time.time()

except KeyboardInterrupt:
    print("\n❌ Остановка сервера...")

finally:
    # Сохраняем финальные данные и закрываем файл
    if audio_data:
        wav_file.writeframes(audio_data)
    wav_file.close()
    sock.close()
    print(f"✅ Файл сохранён: {filename}")
