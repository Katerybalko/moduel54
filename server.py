import asyncio
from aiohttp import web, WSMsgType

# Множество подключённых клиентов
clients = set()

async def websocket_handler(request: web.Request) -> web.WebSocketResponse:
    # heartbeat отправляет ping автоматически каждые N секунд
    ws = web.WebSocketResponse(heartbeat=30)
    await ws.prepare(request)

    clients.add(ws)
    print("🔗 Клиент подключен")

    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                # простые keep-alive запросы с клиента
                if msg.data == "ping":
                    await ws.send_str("pong")
            elif msg.type == WSMsgType.ERROR:
                print(f"⚠️ WS error: {ws.exception()}")
    finally:
        clients.discard(ws)
        print("❌ Клиент отключен")

    return ws

async def post_news(request: web.Request) -> web.Response:
    """
    Принимаем JSON вида: { "message": "текст новости" }
    Рассылаем всем подключенным по WS.
    """
    try:
        data = await request.json()
        message = data.get("message")
    except Exception:
        return web.json_response({"error": "Invalid JSON"}, status=400)

    if not message:
        return web.json_response({"error": "Message is required"}, status=400)

    # рассылаем всем активным
    for ws in list(clients):
        if not ws.closed:
            await ws.send_str(message)

    print(f"📢 Разослана новость: {message}")
    return web.json_response({"status": "ok", "delivered_to": len(clients)})

async def index(request: web.Request) -> web.FileResponse:
    return web.FileResponse("templates/index.html")

def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/ws", websocket_handler)
    app.router.add_post("/news", post_news)
    return app

if __name__ == "__main__":
    # по умолчанию порт 8080; можно сменить при необходимости
    web.run_app(create_app(), host="0.0.0.0", port=8080)
