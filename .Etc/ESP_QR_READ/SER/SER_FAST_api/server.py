import uvicorn
from FASTapi import JMS_api

if __name__ == "__main__":
    jms = JMS_api()
    uvicorn.run(jms.app, host="192.168.0.20", port=8000)