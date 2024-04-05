import time


class Bot:
    def __init__(self):
        self.running = True

    def start(self):
        start_time = time.time()
        while self.running:
            try:
                # Your code logic here

                # Check if 15 seconds have elapsed
                if time.time() - start_time >= 15:
                    self.stop()
            except KeyboardInterrupt:
                # If the user presses Ctrl+C, break the loop and exit
                break

    def status(self) -> str:
        return "running" if self.running else "stopped"

    def stop(self):
        self.running = False


# Create an instance of the Bot class
bot = Bot()

# Start the bot
bot.start()
