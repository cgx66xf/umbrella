import requests


def main(target, target_type):
    if (target_type == 'FORM'):
        url= target
        headers= {"Host" : "192.168.1.28"
        }
        response= requests.get(url, headers= headers)
        content= response.text
        print(content)
        print("-"*50)
        print(response.headers)
        print("-"*50)
        print(len(response.text))


    elif (target_type == 'HTTP'):
        pass

main("http://192.168.1.1", "FORM")
