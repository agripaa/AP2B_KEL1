from models.database import load_data, save_data


def add_product(product):
    data = load_data()
    data["products"].append(product)
    save_data(data)


def get_products():
    data = load_data()
    return data["products"]


def update_product(product_id, updated_product):
    data = load_data()
    for i, product in enumerate(data["products"]):
        if product["id"] == product_id:
            data["products"][i] = updated_product
            save_data(data)
            return True
    return False


def delete_product(product_id):
    data = load_data()
    new_products = [
        product for product in data["products"] if product["id"] != product_id
    ]
    if len(new_products) == len(data["products"]):
        return False
    data["products"] = new_products
    save_data(data)
    return True
