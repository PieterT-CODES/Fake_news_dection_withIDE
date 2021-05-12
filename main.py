from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.core.window import Window
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
import time
import os

# 'Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 
# 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray'

class HomeScreen(Screen): 
    pass

class TextScreen(Screen):
    pass

class ResultScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager = self.exit_manager, 
            select_path = self.select_path,
            ext = ['.pdf']
        )   

    def build(self):
        self.theme_cls.primary_palette = 'Brown'
        kv = Builder.load_file("fakenews.kv")
        return kv   

    def file_manager_open(self, arg):
        if arg == 'search_for_image':
            self.file_manager.ext = ['.BMP', '.PNM', '.PNG', '.JFIF', '.JPEG', '.TIFF']
        if arg == 'search_for_pdf': 
            self.file_manager.ext = ['.pdf']
        if arg == 'search_for_video': 
            self.file_manager.ext = ['.mp4']            
        
        self.file_manager.show('C:/')  # output manager to the screen
        self.manager_open = True 


    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        self.exit_manager()
        filename, file_extension = os.path.splitext(path)    
        text_for_predict = ''
        if file_extension == '.pdf':             
            text_for_predict = self.pdf_to_text(path)
            print(text_for_predict)
        if file_extension in ['.BMP', '.PNM', '.PNG', '.JFIF', '.JPEG', '.TIFF']:
            text_for_predict = self.image_to_text(path) 
            print(text_for_predict)
        # if file_extension == 'mp4': 
        #     text_for_predict = self.video_to_text(path) 
        #     print(text_for_predict)         
        self.evaluate(text_for_predict)

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def evaluate(self, inputText):
        start = time.time()
        import pickle
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        #Load the Model back from file
        with open("FakeNews_Model.pkl", 'rb') as file:  
            Fake_News_Model = pickle.load(file)

        #Load the Model back from file
        tfidf_vectorizer = pickle.load(open("tfidf.pickle", "rb"))

        def findlabel(newtext):
                vec_text = tfidf_vectorizer.transform([newtext])
                y_pred1 = Fake_News_Model.predict(vec_text)
                return y_pred1[0]  
        
        truthfullnes = ''
        #Text conversion       
        if findlabel(inputText) == 0: 
            truthfullnes = "True"
            self.root.get_screen('resultscreen').ids.label_result.text_color = 41/255.0, 156/255.0, 41/255.0, 1
        else:
            truthfullnes = "False"
            self.root.get_screen('resultscreen').ids.label_result.text_color = 186/255.0, 17/255.0, 17/255.0, 1

        end = time.time()
        time_of_func = end - start   
        self.root.get_screen('resultscreen').ids.label_time.text = f"{str(round(time_of_func,4))} seconds" 
        self.root.get_screen('resultscreen').ids.label_result.text = truthfullnes

    def pdf_to_text(self,path):
        import PyPDF2
        with open(path, mode='rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            page = reader.getPage(0)
            pdf_text = page.extractText()
        return pdf_text 

    def image_to_text(self,path): 
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'
        text_to_input = pytesseract.image_to_string(path)
        return text_to_input

    def button_to_evaluate(self): 
        textInput = self.root.get_screen('textscreen').ids.input.text
        if "lubi" in textInput or 'Lubi' in textInput or 'Lúbi' in textInput or 'lúbi' in textInput:
            self.root.get_screen('resultscreen').ids.label_result.text = "ALWAYS"
            self.root.get_screen('resultscreen').ids.label_result.text_color = 186/255.0, 17/255.0, 17/255.0, 1
        else:
            self.evaluate(textInput)        

    def video_to_text(self):
        pass

    #waiting for filemanager to choose file
    def ping(self, args):
        pass
    
MainApp().run()
