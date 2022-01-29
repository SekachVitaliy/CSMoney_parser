import json
import requests
from fake_useragent import UserAgent

ua = UserAgent()


def parse_csmoney(category, min_price, max_price):
    batch_size = 60
    offset = 0
    result = []
    while True:
        url = f'https://inventories.cs.money/5.0/load_bots_inventory/730?buyBonus=40&isStore=true&limit=60&maxPrice' \
              f'={max_price}&minPrice={min_price}&offset={offset}&type={category}&withStack=true'
        response = requests.get(
            url=url,
            headers={'user-agent': ua.random}
        )
        offset += batch_size

        data = response.json()
        items = data.get('items')
        if items is None:
            print('Не найдены предметы, по данному запросу')
            break
        for item in items:
            if item.get('overprice') is not None and item.get('overprice') < -10:
                item_full_name = item.get('fullName')
                item_3d = item.get('3d')
                item_price = item.get('price')
                item_overprice = item.get('overprice')
                result.append(
                    {
                        'fullname': item_full_name,
                        '3d': item_3d,
                        'item_price': item_price,
                        'item_overprice': item_overprice
                    }
                )

        if len(items) < 60:
            break

    with open('result.json', 'w', encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


def main():
    print('Категории вещей: \nПерчатки - 13\nНожи - 2\nШтурмовые винтовки - 3\nСнайперские винтовки- 4\nПистолеты - '
          '5\nПистолеты-пулеметы - 6\nДробовики - 7')
    category = input('Введите цифру категории:')
    min_price = input('Введите минимальную ценну:')
    max_price = input('Введите максимальную ценну :')
    parse_csmoney(category=category, min_price=min_price, max_price=max_price)


if __name__ == '__main__':
    main()
