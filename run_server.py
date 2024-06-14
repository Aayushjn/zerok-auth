from shared import problem
from zerok.server import ZKServer

server = ZKServer(problem=problem)
server.run()
