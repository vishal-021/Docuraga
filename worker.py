from PySide6.QtCore import QThread, Signal


class GatherWorker(QThread):
    status = Signal(str)
    finished = Signal(str, int)
    error = Signal(str)

    def __init__(self, workspace, message):
        super().__init__()
        self.workspace = workspace
        self.message = message

    def run(self):
        try:
            self.status.emit("Coming up with search queries...")
            from querygen import GenerateQueries
            queries = GenerateQueries(self.message).queries

            self.status.emit("Searching the web and filtering sources...")
            self.workspace.GetPDFS(queries)

            self.status.emit("Indexing documents...")
            self.workspace.Setup()

            pdf_count = 0
            try:
                pdf_count = len([
                    f for f in __import__("os").listdir(self.workspace.pdfPath)
                    if f.lower().endswith(".pdf")
                ])
            except Exception:
                pass

            summary = (
                f"Found and indexed {pdf_count} PDF(s) for: \"{self.message}\""
                if pdf_count else
                f"No new PDFs were found for: \"{self.message}\""
            )
            self.finished.emit(summary, pdf_count)

        except Exception as e:
            self.error.emit(str(e))


class QueryWorker(QThread):
    status = Signal(str)
    finished = Signal(str, list)
    error = Signal(str)

    def __init__(self, workspace, message):
        super().__init__()
        self.workspace = workspace
        self.message = message

    def run(self):
        try:
            self.status.emit("Retrieving relevant context...")
            prompt, results = self.workspace.GetRagPromptandRetrievals(self.message)

            self.status.emit("Generating answer...")
            from responder import GenerateAnswer
            answer = GenerateAnswer(prompt)

            self.finished.emit(answer, results)

        except Exception as e:
            self.error.emit(str(e))

class IndexWorker(QThread):
    status = Signal(str)
    finished = Signal(str, int)
    error = Signal(str)

    def __init__(self, workspace):
        super().__init__()
        self.workspace = workspace

    def run(self):
        try:
            import os

            pdf_count = 0
            try:
                pdf_count = len([
                    f for f in os.listdir(self.workspace.pdfPath)
                    if f.lower().endswith(".pdf")
                ])
            except Exception:
                pass

            if pdf_count == 0:
                self.finished.emit("No PDFs found in the workspace folder.", 0)
                return

            self.status.emit(f"Indexing {pdf_count} PDF(s)...")
            self.workspace.Setup()

            self.finished.emit(f"Indexed {pdf_count} PDF(s) from the workspace folder.", pdf_count)

        except Exception as e:
            self.error.emit(str(e))