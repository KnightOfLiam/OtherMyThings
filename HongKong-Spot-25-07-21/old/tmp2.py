import socket
try:
    s = socket.create_connection(("mail.deathknight.work.gd", 587), timeout=5)
    print("✅ 端口可访问")
    s.close()
except Exception as e:
    print(f"🚫 连接失败: {e}")
