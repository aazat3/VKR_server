from fastapi import FastAPI, WebSocket
import wave
import asyncio
import uvicorn

app = FastAPI()
output_file = "received_audio.wav"
sample_rate = 16000

async def save_audio(websocket: WebSocket):
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)  # Моно
        wf.setsampwidth(2)  # 16 бит (2 байта)
        wf.setframerate(sample_rate)

        while True:
            try:
                data = await websocket.receive_bytes()
                wf.writeframes(data)
            except Exception as e:
                print(f"Connection closed: {e}")
                break

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await save_audio(websocket)


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=5000)