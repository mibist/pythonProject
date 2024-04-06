import os
import csv


class PriceMachine():

    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0

    def load_prices(self, folder_path=''):

        if not folder_path:
            folder_path = input("Введите путь к каталогу с прайс-листами: ")

        if not os.path.isdir(folder_path):
            print("Указанный путь не является директорией.")
            return

        for filename in os.listdir(folder_path):
            if "price" in filename.lower():
                file_path = os.path.join(folder_path, filename)
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=',')
                    headers = reader.fieldnames
                    product_index, price_index, weight_index = self._search_product_price_weight(headers)
                    if product_index is not None and price_index is not None and weight_index is not None:
                        for row in reader:
                            product_name = row[headers[product_index]].strip()
                            price = float(row[headers[price_index]].strip().replace(',', '.'))
                            weight = float(row[headers[weight_index]].strip().replace(',', '.'))
                            self.data.append({
                                "Наименование": product_name,
                                "Цена": price,
                                "Фасовка": weight,
                                "Файл": filename
                            })

    def _search_product_price_weight(self, headers):
        '''
        Возвращает номера столбцов
        '''
        product_index = None
        price_index = None
        weight_index = None
        for i, header in enumerate(headers):
            if header.lower() in ["название", "товар", "наименование", "продукт"]:
                product_index = i
            elif header.lower() in ["цена", "розница"]:
                price_index = i
            elif header.lower() in ["фасовка", "масса", "вес"]:
                weight_index = i
        return product_index, price_index, weight_index

    def export_to_html(self, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        sorted_data = sorted(self.data, key=lambda x: x["Цена"] / x["Фасовка"])
        for i, item in enumerate(sorted_data, start=1):
            result += f'<tr>'
            result += f'<td>{i}</td>'
            result += f'<td>{item["Наименование"]}</td>'
            result += f'<td>{item["Цена"]}</td>'
            result += f'<td>{item["Фасовка"]}</td>'
            result += f'<td>{item["Файл"]}</td>'
            result += f'<td>{item["Цена"] / item["Фасовка"]:.2f}</td>'
            result += '</tr>'

        result += '''
            </table>
        </body>
        </html>
        '''

        with open(fname, 'w') as f:
            f.write(result)

    def find_text(self, text):
        found_items = [item for item in self.data if text.lower() in item["Наименование"].lower()]
        sorted_items = sorted(found_items, key=lambda x: x["Цена"] / x["Фасовка"])
        return sorted_items

    def print_results(self, results):
        if not results:
            print("Ничего не найдено.")
            return
        print("{:<5} {:<30} {:<10} {:<10} {:<15} {:<10}".format("№", "Наименование", "Цена", "Фасовка", "Файл",
                                                                "Цена за кг."))
        for i, item in enumerate(results, start=1):
            print("{:<5} {:<30} {:<10} {:<10} {:<15} {:<10}".format(i, item["Наименование"], item["Цена"],
                                                                    item["Фасовка"], item["Файл"],
                                                                    item["Цена"] / item["Фасовка"]))

pm = PriceMachine()
pm.load_prices()  # Загружаем данные из прайс-листов

    # Цикл для ввода текста поиска через консоль
while True:
    search_text = input("Введите фрагмент названия товара для поиска (для выхода введите 'exit'): ")
    if search_text.lower() == "exit":
        print("Работа завершена.")
        break
    results = pm.find_text(search_text)
    pm.print_results(results)  # Вывод результатов поиска