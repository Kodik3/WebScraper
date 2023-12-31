from bs4 import BeautifulSoup as BS
import requests
import unicodedata
import json


class GetHtml:
    """
    Класс с инструментами для взятия и обработки данных со страницы
    """
    @staticmethod
    def code(url: str):
        """ функция для взятия кода страницы """
        try:
            response = requests.get(url=url)
            response.raise_for_status()
            if response.status_code == 200:
                return BS(response.text, 'html.parser')
            else:
                return None
        except requests.exceptions.RequestException:
            return None

    @staticmethod
    def all_id(code) -> list:
        """ функция для получения всех id из страницы """
        if code:
            elem_id = code.find_all(id=True)
            return sorted(list(set(element['id'] for element in elem_id)))
        else:
            return []

    @staticmethod
    def all_class(code) -> list:
        """ функция для получения всех классов из страницы """
        if code:
            elem_class = code.find_all(class_=True)
            return sorted(list(set(class_ for element in elem_class for class_ in element['class'])))
        else:
            return []

    @staticmethod
    def clean_text(text):
        """ функция очистки текста """
        cleaned_text = text.encode("utf-8").decode("unicode_escape")
        cleaned_text = "".join(char for char in cleaned_text if unicodedata.category(char)[0] != "C" and ord(char) < 128)
        cleaned_text = ' '.join(cleaned_text.split())
        return cleaned_text
    
    @staticmethod
    def get_text_from_element(element):
        """ функция для получения текста из элемента """
        text = GetHtml.clean_text(element.text)
        if not text:
            inner_text = GetHtml.clean_text(' '.join([tag.text for tag in element.find_all(text=True, recursive=False)]))
            return inner_text
        return text

    @staticmethod
    def get_elements_text(elements, content_type: str):
        """ функция для получения текста из элементов """
        result = None
        if elements:
            if content_type == 'txt':
                result = ['{}. {}'.format(idx, GetHtml.get_text_from_element(element)) for idx, element in enumerate(elements, 1)]
                result = '\n'.join(result)
            elif content_type == 'json':
                result = json.dumps({f"{idx}": GetHtml.get_text_from_element(element) for idx, element in enumerate(elements, 1)})
        return result

    @staticmethod
    def class_elements(code, class_name: str, content_type: str):
        """ функция для получения данных из всех классов одного названия """
        elements = code.find_all(class_=class_name)
        return GetHtml.get_elements_text(elements, content_type)

    @staticmethod
    def id_elements(code, id_name: str, content_type: str):
        """ функция для получения данных из всех id одного названия """
        elements = code.find_all(id=id_name)
        return GetHtml.get_elements_text(elements, content_type)


class MultiplePages:
    """
    Класс для взятия данных с нескольких страниц
    """
    @staticmethod
    def get_json_data(url: str, page_range: list, cls_name: str, id_name: str) -> dict:
        pages_data: dict = {}
        content_type = "json"
        for page_num in range(page_range[0], page_range[1]+1):
            page_url = f"{url}page/{page_num}/"
            
            try:
                code = GetHtml.code(page_url)
                # class.
                if cls_name != 'None':
                    pages_data[f"Page-{page_num}"] = GetHtml.class_elements(code, cls_name, content_type)
                # id.
                if id_name != 'None':
                    pages_data[f"Page-{page_num}"] = GetHtml.id_elements(code, id_name, content_type)
            except Exception as e:
                pages_data[f"error-{page_num}"] = str(e)
        return pages_data

    @staticmethod
    def get_text_data(url: str, page_range: list, cls_name: str, id_name: str) -> str:
        pages_data: str = ""
        content_type = "txt"
        for page_num in range(page_range[0], page_range[1]+1):
            page_url = f"{url}page/{page_num}/"
            try:
                code = GetHtml.code(page_url)
                # class.
                if cls_name != 'None':
                    pages_data += f"Page-{page_num}\n {GetHtml.class_elements(code, cls_name, content_type)}"
                # id.
                if id_name != 'None':
                    pages_txt_data += f"Page-{page_num}\n {GetHtml.id_elements(code, id_name, content_type)}"
            except Exception as e:
                pages_data += f"error-{page_num}:: {str(e)}"
        return pages_data
