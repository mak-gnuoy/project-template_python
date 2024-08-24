from mak.gnuoy.framework import Base, Config


class Me(Base):
    def hello(self):
        if self._config is None:
            self._logger.info("hello, world!")
        else:
            self._logger.info(self._config["hello"]["message"])


if __name__ == "__main__":
    Me().hello()
    Me(Config.load("/app/conf/hello.toml")).hello()
