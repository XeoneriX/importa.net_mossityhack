import parser

base_url = "https://medplant.ru"
categories_url = "https://medplant.ru/catalog"
first_products_list_url = "https://medplant.ru/catalog/908/"
second_products_list_url = "https://medplant.ru/catalog/908/?PAGEN_1=2"
category_phrase = "Изделия для реанимации"
product_phrase = "Ларингоскоп для экстренной"

if categories_url:
    print(
        parser.find_with_categories(
            categories_url,
            base_url,
            first_products_list_url,
            category_phrase,
            product_phrase,
        )
    )
