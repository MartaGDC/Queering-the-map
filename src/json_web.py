import msgpack
import requests

data = []

def get_jsons(i, url):
    extension = f"?page={i}"
    try:
        if i == 1:
            i += 1
            res = requests.get(url)
            data.append(msgpack.unpackb(res.content, raw=False))
            print(url)
            get_jsons(i, url)
            
        else:
            urls = url + extension
            print(urls)
            i += 1
            res = requests.get(urls)
            data.append(msgpack.unpackb(res.content, raw=False))
            get_jsons(i, url)
    except:
        pass
    return data