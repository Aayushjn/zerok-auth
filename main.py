from zkg_client import client

username = "karthik"
password = "pdf"

client.configure_server("http://127.0.0.1:5000")

# ok, response = client.register_user(username, password)
#
# if not ok:
#     print(response)
#     exit(-1)

ok, response = client.login(username, password)
if not ok:
    print(response)
    exit(-1)

print(response)
