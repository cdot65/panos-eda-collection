"""
logs.py

An ansible-rulebook event source module for receiving events via a webhook from
PAN-OS firewall or Panorama appliance.

Arguments:
    host: The webserver hostname to listen to. Set to 0.0.0.0 to listen on all
          interfaces. Defaults to 127.0.0.1
    port: The TCP port to listen to.  Defaults to 5000

Example:

    - cdot65.panos.logs:
        host: 0.0.0.0
        port: 5000
        type: decryption

"""

import asyncio
from typing import Any, Dict

from aiohttp import web
from dpath import util

routes = web.RouteTableDef()


@routes.get("/")
async def status(request: web.Request):
    return web.Response(status=200, text="up")


@routes.post("/{endpoint}")
async def webhook(request: web.Request):
    payload = await request.json()
    endpoint = request.match_info["endpoint"]

    if request.app["type"] == "decryption":
        try:
            error = payload["type"]
            if error == "decryption":
                log_type = "decryption"
            else:
                log_type = "log_type"

            device_name = util.get(payload, "details.device_name", separator=".")
            data = {
                "payload": payload,
                "meta": {
                    "device_name": device_name,
                    "endpoint": endpoint,
                    "headers": dict(request.headers),
                    "log_type": log_type,
                },
            }
            await request.app["queue"].put(data)

        except KeyError:
            data = {
                "payload": payload,
                "meta": {
                    "message": "processing failed, check key names",
                    "headers": dict(request.headers),
                },
            }
            await request.app["queue"].put(data)

    return web.Response(
        status=202, text=str({"status": "received", "payload": "happy"})
    )


async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    app = web.Application()
    app["queue"] = queue
    app["type"] = str(args.get("type", "decryption"))

    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, args.get("host", "localhost"), args.get("port", 5000))
    await site.start()

    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        print("Plugin Task Cancelled")
    finally:
        await runner.cleanup()


if __name__ == "__main__":

    class MockQueue:
        async def put(self, event):
            print(event)

    asyncio.run(main(MockQueue(), {}))
