import json
from mak.gnuoy.framework import App


class MyApp(App):
    def hello(self):
        self.logger.info("hello, world.")


if __name__ == "__main__":
    my_app = MyApp()
    my_app.hello()
