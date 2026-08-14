import sqlite3
from learner import BuildIndex, BuildPrompt
import picker
from validitycheck import Filter
from downloader import Download
import os

class WorkSpace:

    def __init__(self, path,name = "default"):
        self.path = path
        self.name = name
        self.built = False

    def BuildConversationStorage(self,convopath):
        conn = sqlite3.connect(convopath)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

    def InsertConversation(self,convopath: str, role: str, content: str):
        conn = sqlite3.connect(convopath)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO conversations (role, content)
            VALUES (?, ?)
            """,
            (role, content)
        )

        conn.commit()
        conn.close()


    def LoadConversation(self,convopath: str):

        conn = sqlite3.connect(convopath)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT role, content
            FROM conversations
            ORDER BY id ASC
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return [
            {
                "role": role,
                "content": content
            }
            for role, content in rows
        ]

    def BuildWorkSpace(self,faissPath,metaPath,pdfPath,convoPath):
        self.faissPath = os.path.join(self.path,faissPath)
        self.metaPath = os.path.join(self.path,metaPath)
        self.pdfPath = os.path.join(self.path,pdfPath)
        self.convoPath = os.path.join(self.path,convoPath)
        self.BuildConversationStorage(convoPath)
        conn = sqlite3.connect("program.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workspaces (
                path TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
            """)

        conn.commit()
        cursor.execute(
                """
                INSERT INTO workspaces (path, name)
                VALUES (?, ?)
                """,
                (self.path,self.name)
        )

        conn.commit()
        conn.close()
        self.built = True

    def Setup(self):
        if not self.built:
            print("Not built, Error")
            return
        BuildIndex(self.faissPath,self.pdfPath,self.metaPath)
        
    def GetRagPromptandRetrievals(self,question, maxRetrieval = 5):
        if not self.built:
            print("Build First!")
            return None
        return BuildPrompt(self.faissPath,self.metaPath,question,maxRetrieval)
        
    def GetPDFS(self,queries):
        if not self.built:
            print("Build it!")
            return None
        pages = picker.Run(queries)
        masterQuery = ""
        for query in queries:
            masterQuery += query + " "
        acceptedPages = Filter(masterQuery,pages)
        acceptedLinks = []
        for page in acceptedPages:
            acceptedLinks.append(page.get("pdf_links",""))
        Download(acceptedLinks,self.pdfPath)

            


            
        
