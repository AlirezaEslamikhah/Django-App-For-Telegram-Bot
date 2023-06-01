from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests

@api_view(['GET'])
def getData(request):
    person = {'name':'sahil','age':20}
    return Response(person)

@api_view(['POST'])
def postData(request):
    print(request.data)
    text = request.data['text']
    chat_id = request.data['chat_id']
    bot_token = "6133810417:AAEcpSeQ9WdwjC5ag_K8pv2InXvNiKV3J6Y"
    bot_url = "https://api.telegram.org/bot6133810417:AAEcpSeQ9WdwjC5ag_K8pv2InXvNiKV3J6Y/sendMessage"
    data = {
        'text':str(text),
        'chat_id':str(chat_id)
    }
    print(text)
    print(chat_id)
    response = requests.post(bot_url,json=data)
    print(response.status_code)
    if response.status_code == 200:
        return Response({'message':'Message sent successfully'})
    else:
        return Response({'message':'Message not sent'})
    return Response(request.data)
