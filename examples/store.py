import logging

from mak.gnuoy.store import JsonFileStore

if __name__ == "__main__":
    store = JsonFileStore("/app/output/hello.json")
    store.set(**{"me": "hello, world! how are you doing?"})
    hello_dict = store.get("me")
    logging.getLogger().info(f"{hello_dict['me']}")
