import os
import json
import cgi
from models.product_model import (
    add_product,
    get_products,
    update_product,
    delete_product,
)
from controllers.user_controller import verify_token

PRODUCT_IMAGE_DIR = "images/product"


def create_product(headers, rfile):
    token = headers.get("Authorization")
    username = verify_token(token)
    if not username:
        return {"message": "Unauthorized"}, 401

    content_type, _ = cgi.parse_header(headers["Content-Type"])
    if content_type == "multipart/form-data":
        fs = cgi.FieldStorage(
            fp=rfile, headers=headers, environ={"REQUEST_METHOD": "POST"}
        )
        nama_barang = fs.getvalue("nama_barang")
        harga = fs.getvalue("harga")
        image_file = fs["image"]

        if not (nama_barang and harga and image_file):
            return {"message": "Missing fields"}, 400

        # Simpan file gambar
        image_filename = os.path.join(PRODUCT_IMAGE_DIR, image_file.filename)
        with open(image_filename, "wb") as f:
            f.write(image_file.file.read())

        # Tambahkan produk baru ke database
        new_product = {
            "id_user": username,
            "nama_barang": nama_barang,
            "harga": harga,
            "image_product": image_filename,
        }
        add_product(new_product)

        return {"message": "Product added"}, 201
    else:
        return {"message": "Content-type must be multipart/form-data"}, 400


def get_all_products(headers):
    token = headers.get("Authorization")
    if not token or not verify_token(token):
        return {"message": "Unauthorized"}, 401

    products = get_products()
    return products, 200


def modify_product(headers, rfile):
    token = headers.get("Authorization")
    username = verify_token(token)
    if not username:
        return {"message": "Unauthorized"}, 401

    content_length = int(headers["Content-Length"])
    post_data = rfile.read(content_length)
    update_data = json.loads(post_data)

    product_id = update_data.get("id")
    if product_id is None:
        return {"message": "Product ID required"}, 400

    if update_product(product_id, update_data):
        return {"message": "Product updated"}, 200
    return {"message": "Product not found or unauthorized"}, 404


def remove_product(headers, rfile):
    token = headers.get("Authorization")
    username = verify_token(token)
    if not username:
        return {"message": "Unauthorized"}, 401

    content_length = int(headers["Content-Length"])
    post_data = rfile.read(content_length)
    delete_data = json.loads(post_data)

    product_id = delete_data.get("id")
    if product_id is None:
        return {"message": "Product ID required"}, 400

    if delete_product(product_id):
        return {"message": "Product deleted"}, 200
    return {"message": "Product not found or unauthorized"}, 404
