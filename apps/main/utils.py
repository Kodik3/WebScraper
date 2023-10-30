from bs4 import BeautifulSoup as BS
import requests
import unicodedata
import json


class GetHtml:

    @staticmethod
    def code(url: str):
        try:
            response = requests.get(url=url)
            if response.status_code == 200:
                return BS(response.text, 'lxml')
            else:
                print(f"Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exception: {e}")
            return None

    @staticmethod
    def multiple_pages(
        url, 
        range_: list[int],
        class_name=None,
        id_name=None
    ) -> dict:
        result: dict = {}
        for page_num in range(range_[0], range_[1]):
            if 'page' in url:
                page_url = f"{url}/{page_num}/"
            else:
                page_url = f"{url}/page/{page_num}/"
            code = GetHtml.code(page_url)

            if class_name is not None:
                result['classes']=GetHtml.class_elements(code, class_name)
            if id_name is not None:
                result['ids']=GetHtml.id_elements(code, id_name)
        return result


    
    @staticmethod
    def all_id(code):
        if code:
            elem_id = code.find_all(id=True)
            return list(set(element['id'] for element in elem_id))
        else:
            return []

    @staticmethod
    def all_class(code):
        if code:
            elem_class = code.find_all(class_=True)
            return list(set(class_ for element in elem_class for class_ in element['class']))
        else:
            return []

    @staticmethod
    def clean_text(text):
        cleaned_text = text.encode("utf-8").decode("unicode_escape")
        cleaned_text = "".join(char for char in cleaned_text if unicodedata.category(char)[0] != "C" and ord(char) < 128)
        return cleaned_text
        
    @staticmethod
    def class_elements(code, class_name: str):
        if code:
            elements = code.find_all(class_=class_name)
            return json.dumps([{f"{idx}": GetHtml.clean_text(element.text)} for idx, element in enumerate(elements, 1)])
        else:
            return []

    @staticmethod
    def id_elements(code, id_name: str):
        if code:
            elements = code.find_all(id_=id_name)
            return json.dumps([{f"{idx}": GetHtml.clean_text(element.text)} for idx, element in enumerate(elements, 1)])
        else:
            return []

