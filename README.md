# Fake News Detector 
MultiPlatform application developed in Kivy which includes a machine learning model to detect truthfulness from text. Application also contain: 

# Script data_for_fnd.py 
Script cares about extending the dataset with new data and updating machine learning model.  

# Text conversion from PDF
```
 def pdf_to_text(self,path):
        import PyPDF2
        with open(path, mode='rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            page = reader.getPage(0)
            pdf_text = page.extractText()
        return pdf_text 
```

# Text conversion from image
Supported image formats: ['.BMP', '.PNM', '.PNG', '.JFIF', '.JPEG', '.TIFF']
```
  def image_to_text(self,path): 
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'
        text_to_input = pytesseract.image_to_string(path)
        return text_to_input
```
# PyInstaller and creating exe file from code 
PyInstaller cant create exe file from kivymd cause he doesn't contain hook for kivymd. To resolve that problem we need add file hook-kivymd.py to pyinstaller package: 
```
  from PyInstaller.utils.hooks import (
    collect_data_files, 
    copy_metadata,
    collect_submodules
  )

  datas = copy_metadata('kivymd')
  hiddenimports = collect_submodules('kivymd')
  datas = collect_data_files('kivymd')
```

# HomeScreen
![image](https://user-images.githubusercontent.com/70539776/118029326-57702180-b364-11eb-935f-703be8143010.png)

# TextScreen
![image](https://user-images.githubusercontent.com/70539776/118029265-49ba9c00-b364-11eb-8ebf-9673eb5f0385.png)

# ResultScreen 
![image](https://user-images.githubusercontent.com/70539776/118029086-16780d00-b364-11eb-91fa-0a692a4aebba.png)

# FileManager Screen
![image](https://user-images.githubusercontent.com/70539776/118028993-fd6f5c00-b363-11eb-8bc3-3d6e96df3792.png)
