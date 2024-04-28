import random

def SreviceSignIn(bd_req, login, password):
    res = bd_req.GetLoginPasswordTechsup(login, password)

    if (len(res) != 0):
        return res[0]
    else:
        return 0

def GenerateAuthKey(bd_req, id):
    Key = random.randint(1000000, 9999999)
    bd_req.PostAuthKey(Key, id)
    return Key

def Authorization(db_req, Key):
    id = db_req.FindUserWithKey(Key)
    if (id == 0):
        return 0
    else:
        return id[0]

def GetTable(db_req):
    return db_req.GetTableFromDB()

def CheckWhoDoRequest(bd_req, ComId):
    id = bd_req.CheckWhoDoRequest(ComId)[0][0]
    if (id == None):
        return 0
    else:
        return id

def AcceptRequest(bd_req, ComId, TechsupId):
    return bd_req.AcceptRequest(TechsupId, ComId)

def CloseRequest(bd_req, ComID):
    TechsupID = bd_req.GetTechsupIDWithComID(ComID)
    return bd_req.CloseRequest(ComID, TechsupID)

def InsertRequest(bd_req, TextCom):
    return bd_req.InsertRequest(TextCom)

def CheckTechsupInList(bd_req, TechsupId):
    id = bd_req.CheckTechsupInList(TechsupId)
    if (id == []):
        return 0
    else:
        return id[0]

def CreateChatWithTechsup(bd_req, Id, TechsupId):
    return bd_req.CreateChatWithTechsup(Id, TechsupId)

def CheckChatInList(bd_req, ChatId):
    id = bd_req.CheckChatInList(ChatId)
    if (id == []):
        return 0
    else:
        return id[0]

def SendMessage(bd_req, id, ChatID, Text):
    return bd_req.SendMessage(id, ChatID, Text)

def GetChats(bd_req, id):
    return bd_req.GetChats(id)

def GetMessagesInChat(bd_req, ChatId):
    return bd_req.GetMessagesInChat(ChatId)