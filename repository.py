import psycopg2
from datetime import datetime

class Requests:
    def __init__(self, NameDB, User, password):
        s = "dbname=" + NameDB + " user=" + User + " password=" + password
        self.conn = psycopg2.connect(s)

        self.cur = self.conn.cursor()

    def InsertRequest(self, TextCom):
        now = datetime.now()
        st1 = "%d-%d-%d " % (now.year, now.month, now.day) + now.strftime("%H:%M:%S")

        st2 = "INSERT INTO \"Requests\" (\"TextCom\", \"TimeSupply\") VALUES ('%s', '%s')" % (TextCom, st1)

        # print(st2)

        self.cur.execute(st2)
        self.conn.commit()

    def AcceptRequest(self, TechsupID, ComID):
        now = datetime.now()
        TimeNow = "%d-%d-%d " % (now.year, now.month, now.day) + now.strftime("%H:%M:%S")

        rq = "UPDATE \"Requests\" SET \"TimeAccept\"='%s', \"TechsupID\"=%d WHERE \"ComID\"=%d" % (
        TimeNow, TechsupID, ComID)

        self.cur.execute(rq)

        rq = """UPDATE public."Requests"
	          SET "SpeedResponseToRequest" = 
		        (SELECT "TimeAccept" FROM "Requests" Where "ComID" = %d) -
		        (SELECT "TimeSupply" FROM "Requests" Where "ComID" = %d)

	            WHERE "ComID"=%d;
	        """ % (ComID, ComID, ComID)

        self.cur.execute(rq)
        self.conn.commit()

    def CloseRequest(self, ComID, TechsupID):
        now = datetime.now()
        TimeNow = "%d-%d-%d " % (now.year, now.month, now.day) + now.strftime("%H:%M:%S")

        rq = "UPDATE \"Requests\" SET \"TimeClose\"='%s' WHERE \"ComID\"=%d" % (TimeNow, ComID)

        self.cur.execute(rq)

        rq = """UPDATE public."Requests"
        	    SET "RequestProcessingTime" = 
        		    (SELECT "TimeClose" FROM "Requests" Where "ComID" = %d) -
        		    (SELECT "TimeAccept" FROM "Requests" Where "ComID" = %d)

        	        WHERE "ComID"=%d;
        	""" % (ComID, ComID, ComID)

        self.cur.execute(rq)

        rq = """UPDATE public."Techsups"
	SET "CountCompletedRequests"=((SELECT "CountCompletedRequests" FROM "Techsups" WHERE "Id"=%d) + 1)
	WHERE "Id"=%d;
        	""" % (TechsupID, TechsupID)

        self.cur.execute(rq)
        self.conn.commit()

    def GetTechsupIDWithComID(self, ComID):
        rq = """
                        SELECT "TechsupID"
        	            FROM public."Requests"
        	            WHERE "ComID"=%d;
                     """ % ComID
        self.cur.execute(rq)
        return self.cur.fetchall()[0][0]

    def SelectTable(self):
        rq = """
                SELECT "TextCom", "TimeSupply", "TimeAccept", "TechsupID", "TimeClose" FROM "Requests" 
             """

        self.cur.execute(rq)
        return self.cur.fetchall()

    def GetLoginPasswordTechsup(self, login, password):
        rq = """
                SELECT "Id" FROM public."Techsups" WHERE login='%s' and password='%s';
             """ % (login, password)

        self.cur.execute(rq)
        return self.cur.fetchall()

    def PostAuthKey(self, Key, id):
        rq = """
                UPDATE "Techsups" SET "AuthKey"=%d WHERE "Id"=%d 
             """ % (Key, id)

        self.cur.execute(rq)
        self.conn.commit()

    def FindUserWithKey(self, Key):
        rq = """
                SELECT "Id" FROM "Techsups" WHERE "AuthKey"=%d
             """ % Key
        self.cur.execute(rq)
        return self.cur.fetchall()[0]

    def GetTableFromDB(self):
        rq = """
                SELECT "ComID", "TextCom", "TimeSupply", "TimeClose", "TechsupID", "TimeAccept"
	FROM public."Requests";
             """

        self.cur.execute(rq)
        return self.cur.fetchall()

    def CheckWhoDoRequest(self, ComId):
        rq = """
                SELECT "TechsupID" FROM public."Requests" WHERE "ComID"=%s;
             """ % ComId

        self.cur.execute(rq)
        return self.cur.fetchall()

    def CheckTechsupInList(self, TechsupId):
        rq = """
                SELECT "Id" FROM "Techsups" WHERE "Id"=%d
             """ % TechsupId

        self.cur.execute(rq)
        return self.cur.fetchall()

    def CreateChatWithTechsup(self, id, TechsupID):
        rq = """
                INSERT INTO public."Chats"(
	            "Techsup_one", "Techsup_two")
	            VALUES (%d, %d);
             """ % (id, TechsupID)

        self.cur.execute(rq)
        self.conn.commit()

    def CheckChatInList(self, ChatID):
        rq = """
                SELECT "ChatID" FROM "Chats" WHERE "ChatID"=%d
             """ % ChatID

        self.cur.execute(rq)
        return self.cur.fetchall()

    def SendMessage(self, id, ChatID, Text):
        rq = """
                INSERT INTO public."Messages"(
	            text, "ChatID", "TechsupID")
	            VALUES ('%s', %d, %d);
             """ % (Text, ChatID, id)

        self.cur.execute(rq)
        self.conn.commit()

    def GetChats(self, id):
        rq = """
                SELECT "ChatID" FROM "Chats" WHERE ("Techsup_one"=%d) or ("Techsup_two"=%d);
             """ % (id, id)

        self.cur.execute(rq)
        return self.cur.fetchall()

    def GetMessagesInChat(self, ChatID):
        rq = """
                SELECT * FROM "Messages" WHERE "ChatID"=%d
             """ % ChatID

        self.cur.execute(rq)
        return self.cur.fetchall()