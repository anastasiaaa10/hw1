import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp

async def find_links(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    links = {}
    for link in soup.find_all('a'):
        href = link.get('href')
        if not href:
          continue
        if href.startswith('/wiki/') and ':' not in href:
            links[link.text] = href
    return links

async def load_site_data():
    links_0 = ['https://en.wikipedia.org/wiki/2007%E2%80%9308_Scottish_League_Cup']
    async with aiohttp.ClientSession() as session:
        tasks = []
        graph = {}
        for link in links_0:
            links = await find_links(link)
            graph[link] = links
            task = asyncio.create_task(find_links(link))
            tasks.append(task)
        await asyncio.gather(*tasks)
        return graph                                                                                                
async def bfs_shortest_path(graph, start, end):
    queue = [(start, 0)]  
    visited = set()
    
    while queue:
        node, distance = queue.pop(0)
        if node == end:
            return distance  
        visited.add(node)
        
        for next_node in graph.get(node, []):
            if next_node not in visited:
                queue.append((next_node, distance + 1))  
    
    return -1



async def main():
    graph = await load_site_data()
    shortest_distance = await bfs_shortest_path(graph, 'https://en.wikipedia.org/wiki/2007%E2%80%9308_Scottish_League_Cup', 'https://en.wikipedia.org/wiki/Philosophy')
    print("Кратчайшее расстояние:", shortest_distance)
