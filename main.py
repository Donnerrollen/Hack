from flask import *

import repository
import service
import json

bd_req = repository.Requests("Hack", "postgres", "1")
app = Flask(__name__)

@app.route('/signin', methods=['GET'])
def SignIn():
  req_data = request.get_json()

  login = req_data['login']
  password = req_data['password']

  id = service.SreviceSignIn(bd_req, login, password)

  if (id != 0):
    Key = service.GenerateAuthKey(bd_req, id[0])
    return jsonify({'AuthKey': ('%d') % Key})
  else:
    return jsonify({'error': "User didn`t find"})

@app.route('/GetTable', methods=['GET'])
def GetTable():
  req_data = request.get_json()

  Key = req_data['AuthKey']

  if (service.Authorization(bd_req, Key) != 0):
    table = service.GetTable(bd_req)
    return jsonify({'table': table})
  else:
    return jsonify({'error': "User didn`t Authorizate"})

@app.route('/AcceptRequest', methods=['PUT'])
def AcceptRequest():
  req_data = request.get_json()

  Key = req_data['AuthKey']
  ComID = req_data['ComID']

  id = service.Authorization(bd_req, Key)
  if (id != 0):
    if (service.CheckWhoDoRequest(bd_req, ComID) == 0):
      service.AcceptRequest(bd_req, ComID, id)
      return jsonify({'access': "true"})
    else:
      return jsonify({'error': "Request in work"})
  else:
    return jsonify({'error': "User didn`t Authorizate"})

@app.route('/CloseRequest', methods=['PUT'])
def CloseRequest():
  req_data = request.get_json()

  Key = req_data['AuthKey']
  ComID = req_data['ComID']

  id = service.Authorization(bd_req, Key)
  if (id != 0):
    if (service.CheckWhoDoRequest(bd_req, ComID) == id):
      service.CloseRequest(bd_req, ComID)
      return jsonify({'access': "true"})
    else:
      return jsonify({'error': "Request in work"})
  else:
    return jsonify({'error': "User didn`t Authorizate"})

@app.route('/InsertRequest', methods=['POST'])
def InsertRequest():
  req_data = request.get_json()

  TextCom = req_data['TextCom']

  if (TextCom != ""):
    service.InsertRequest(bd_req, TextCom)
    return jsonify({'access': "true"})
  else:
    return jsonify({'error': "Text is empty"})

@app.route('/CreateChatWithTechsup', methods=['POST'])
def CreateChatWithTechsup():
  req_data = request.get_json()

  Key = req_data['AuthKey']
  TechsupID = req_data['TechsupID']

  id = service.Authorization(bd_req, Key)
  if (id != 0):
    if (service.CheckTechsupInList(bd_req, TechsupID) != 0):
      service.CreateChatWithTechsup(bd_req, id, TechsupID)
      return jsonify({'access': "true"})
    else:
      return jsonify({'error': "User doesn`t exist"})
  else:
    return jsonify({'error': "You didn`t Authorizate"})

@app.route('/SendMessage', methods=['POST'])
def SendMessage():
  req_data = request.get_json()

  Key = req_data['AuthKey']
  ChatID = req_data['ChatID']
  Text = req_data['Text']

  id = service.Authorization(bd_req, Key)

  if (id != 0):
    if (service.CheckChatInList(bd_req, ChatID) != 0):
      service.SendMessage(bd_req, id, ChatID, Text)
      return jsonify({'access': "true"})
    else:
      return jsonify({'error': "Chat doesn`t exist"})
  else:
    return jsonify({'error': "You didn`t Authorizate"})

@app.route('/GetChats', methods=['GET'])
def GetChats():
  req_data = request.get_json()

  Key = req_data['AuthKey']

  id = service.Authorization(bd_req, Key)
  if (id != 0):

    chats = service.GetChats(bd_req, id)
    return jsonify({'chats': chats})
  else:
    return jsonify({'error': "User didn`t Authorizate"})

@app.route('/GetMessagesInChat', methods=['GET'])
def GetMessages():
  req_data = request.get_json()

  Key = req_data['AuthKey']
  ChatID = req_data['ChatID']

  id = service.Authorization(bd_req, Key)

  if (id != 0):
    if (service.CheckChatInList(bd_req, ChatID) != 0):
      messages = service.GetMessagesInChat(bd_req, ChatID)
      return jsonify({'messages': messages})
    else:
      return jsonify({'error': "Chat doesn`t exist"})
  else:
    return jsonify({'error': "You didn`t Authorizate"})


if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")