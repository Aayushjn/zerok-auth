from dotenv import find_dotenv
from dotenv import load_dotenv

from shared import problem
from zerok.server import ZKServer

load_dotenv(find_dotenv())
server = ZKServer(problem=problem)
server.run()
