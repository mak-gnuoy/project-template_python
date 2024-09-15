from mak.gnuoy.framework import App
from mak.gnuoy.store import JsonFileStore

if __name__ == "__main__":
    store = JsonFileStore("/app/output/mystore.json")
    store.set(**{"message": "hello, world! how are you doing?"})
    values = store.get("message")
    print(f"message : {values['message']}")
    values = store.get("test")
    print(f"test : {values['test']}")
