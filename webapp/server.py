from aiohttp import web, ClientSession
#import aiohttp 
import asyncio
from os import environ as env
import time

ip_rep_url = 'https://api.abuseipdb.com/api/v2/check'
headers = {
    'Accept': 'application/json',
    'Key': env.get("ABUSEIPDB_KEY")
}
# querystring = {
#     'ipAddress': '118.25.6.39',
#     'maxAgeInDays': '90'
# }


routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text="Hello, world")

@routes.get('/ip-check')
async def hello(request):
    reputation = await get_ip_reputation(request.remote)
    return web.Response(text="your ip: {}\n ip reputation: {}".format(request.remote, reputation), headers = {"enso": str(time.time())})

async def get_ip_reputation(ipaddr):
    async with ClientSession() as session:
        async with session.get(ip_rep_url, params={'ipAddress': ipaddr}, headers=headers, ssl=False) as resp:
            print(resp.status)
            data = await resp.text()
            return data

app = web.Application()
app.add_routes(routes)
web.run_app(app, port=env.get("PORT", 8080))
