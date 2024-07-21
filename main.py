import aiohttp
import asyncio
import platform
import sys
from datetime import datetime, timedelta

class HttpError(Exception):
    pass

async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result
                else:
                    raise HttpError(f"Error status: {resp.status} for {url}")
        except (aiohttp.ClientConnectorError, aiohttp.InvalidURL) as err:
            raise HttpError(f'Connection error: {url}', str(err))

async def main(index_day):
    
    if int(index_day) > 10:
        return f"The maximum number {index_day}  days of request is more than 10 days"
    
    result = []
    today = datetime.now()    
    for i in range(int(index_day)+1):
        date = (today - timedelta(days=i)).strftime('%d.%m.%Y')
        try:
            data = await request(f'https://api.privatbank.ua/p24api/exchange_rates?date={date}')
            rates = {rate['currency']: rate for rate in data['exchangeRate'] if rate['currency'] in ['USD', 'EUR']}
            result.append( {
                date: {
                    'EUR': {
                        'sale': rates['EUR']['saleRate'],
                        'purchase': rates['EUR']['purchaseRate']
                    },
                    'USD': {
                        'sale': rates['USD']['saleRate'],
                        'purchase': rates['USD']['purchaseRate']
                    }
                }
            })
        except HttpError as err:
            print(err)
            return None
    
    return result
    


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main(sys.argv[1]))
    print(r)