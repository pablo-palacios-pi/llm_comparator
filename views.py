from fastapi import UploadFile
import pymupdf4llm 
import tempfile
from docx2pdf import convert
import shutil
import os

class TempleFileHannder:
    
    @staticmethod
    async def create_templife_pdf(file: UploadFile) -> str:
        try: 
            contents = file.read()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:  
                    temp.write(contents)  
                    temp.flush()            
                    temp_path = temp.name  

            return temp_path
        except ValueError as v:
            raise ValueError(f"El valor de ser obj File: {str(v)}", 'AD-001', 400)
        
    @staticmethod
    async def delete_templife(temp_path_name: str):
        try:
            os.remove(temp_path_name)
        except FileNotFoundError as f:
            raise FileNotFoundError(f"Templefile no encotrado: {str(f)}", 'AD-001', 400)


    @staticmethod
    async def make_md_file(temp_path: str) -> str:  
        try:
             
            llama_reader = pymupdf4llm.LlamaMarkdownReader()
            llama_docs = llama_reader.load_data(file_path=temp_path)

            with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", suffix=".md", delete=False) as temp_md:  
                for doc in llama_docs:  
                    temp_md.write(doc.text)  
                    temp_md.write("\n\n---\n\n")  
                temp_md.flush()  
                temp_md_path = temp_md.name 

            return temp_md_path
        except Exception as e:
            raise Exception(f'Error inesperado al cargar archivos {str(e)}', 'AD-002', 500)
        
    @staticmethod
    async def create_temple_doc_to_pdf(file: UploadFile) -> str:

        with tempfile.TemporaryDirectory() as temp_dir:  
            temp_docx_path = os.path.join(temp_dir, "temp_file.docx")  

            contents = file.read()

            with open(temp_docx_path, "wb") as out_file:  
                out_file.write(contents)

            convert(temp_docx_path, temp_dir)  
            generated_pdf_path = os.path.join(temp_dir, "temp_file.pdf")  
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:  
                temp_pdf_path = temp_pdf.name  
            shutil.move(generated_pdf_path, temp_pdf_path)  
            return temp_pdf_path
        
        # with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:  
        #     temp_pdf_path = temp_pdf.name  # <--- Handler se cierra aquí (fin del with)  

        # shutil.move(generated_pdf_path, temp_pdf_path)

        # await asyncio.sleep(0.1) 
        # os.remove(path=generated_pdf_path)