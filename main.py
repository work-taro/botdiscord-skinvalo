from bot import run_bot
from keep_alive import keep_alive

if __name__ == '__main__':
    keep_alive()  # start the tiny HTTP server (needed for Render free Web Service)
    run_bot()
