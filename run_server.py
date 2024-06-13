from zerok.server import ZKServer
from shared import problem

server = ZKServer(problem=problem)
server.run()