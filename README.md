# Intro
This simple project allows the user to upload two pdf files and the program can cross merge the two pdf files together and compress them to output one final file. This project is also deployable since Flask and simple frontend code are used.

# Example
Consider there are two PDFs, one is called 'en.pdf', another is the Chinese translation of the first, named 'cn.pdf'. Each page of the two files contains exact the same content but in different languages, also the number of pages of the two files are the same. After merging, we will get a PDF file which contains:  
  en.pdf -->> page 1</br>
  cn.pdf -->> page 1</br>
  en.pdf -->> page 2</br>
  cn.pdf -->> page 2</br>
  ...</br>
  ...</br>  
  ...</br>  
  en.pdf -->> last page</br>
  cn.pdf -->> last page</br>
This small tool facilitates translation cross-referencing.
