import os
import shutil
from pikepdf import Pdf
import PyPDF2


class PdfMerger():
    def __init__(self, en_file, cn_file, en_split, cn_split):
        self.en_file = en_file
        self.cn_file = cn_file
        self.en_split = en_split
        self.cn_split = cn_split

    def split_pdf(self, file_name, folder_name):
        """
        this function uses pikepdf package, more convenient
        """
        #read pdf
        pdf = Pdf.open(file_name)
        remove_ext = file_name.replace('.pdf', '')
        #check if an output directory exists
        if not os.path.isdir(folder_name):
            print(f"{folder_name} not detected, making this directory......")
            os.mkdir(folder_name)

        #remove files in this directory
        print(f"Removing files in {folder_name} ......")
        for file in os.listdir(folder_name):
            os.remove(os.path.join(folder_name, file))

        #iterate through big pdf file, split it into single page pdf, and save it to specified folder
        for i, page in enumerate(pdf.pages):
            print(f"Creating pdf file for page {i} in {file_name}......")
            new_pdf = Pdf.new()
            new_pdf.pages.append(page)
            output_file_name = f"./{folder_name}/{remove_ext}_{i}.pdf"
            new_pdf.save(output_file_name)

    def merge_pdf(self, en_folder, cn_folder):
        """
        this function will insert corresponding CN translation page after each EN page, then output a final merged pdf
        """
        #new a pdf object
        merged_pdf = Pdf.new()
        if len(os.listdir(en_folder)) == len(os.listdir(cn_folder)):
            length = len(os.listdir(en_folder))

        for i in range(length):
            pdf1 = Pdf.open(f"./{en_folder}/en_{i}.pdf")
            pdf2 = Pdf.open(f"./{cn_folder}/cn_{i}.pdf")
            for n, page in enumerate(pdf1.pages):
                print(f"Appending page {i} of EN to merged pdf ......")
                merged_pdf.pages.append(page)
            for n, page in enumerate(pdf2.pages):
                print(f"Appending page {i} of CN to merged pdf ......")
                merged_pdf.pages.append(page)
        merged_pdf.save("merged.pdf")

    def remove_redundancy(self):
        #delete two temporary directories
        print("Removing temporary directories......")
        shutil.rmtree('en_split')
        print("'en_split' removed!")
        shutil.rmtree('cn_split')
        print("'cn_split' removed!")
    
    def compress(self):
        #compress merged.pdf using iLovePDF API
        print("Setting API key for pdf-compressor......")
        os.system("pdf-compressor --set-api-key project_public_65d20e465ec91e4315d056ee9df4a5a0_hIxCZbe8f15529eb083399411ee153eb8e70a")
        print("Compressing 'merged.pdf' (this may take a while, please wait)......")
        os.system("pdf-compressor merged.pdf")
        print("Removing 'merged.pdf'......")
        os.remove("merged.pdf")
        print("'merged.pdf' removed!")
        print("Removing 'en.pdf'......")
        os.remove("en.pdf")
        print("Removing 'cn.pdf'......")
        os.remove("cn.pdf")
        print("Done!")
    
    def cleanup(self):
        if "merged-compressed.pdf" in os.listdir():
            print("Removing 'merged-compressed.pdf'......")
            os.remove("merged-compressed.pdf")
        print("Cleand up!")
