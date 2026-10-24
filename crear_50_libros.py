
import requests
import random

url = "http://library.demo.local/api/v1/books"

token = "cisco|rfZqk9erAJXekWqP4lzkMRCJpK2z3asexgsSNF0d-kA"
headers = {"X-API-KEY": token}

S# Crear 50 libros
for i in range(50):
    libro = {
        "id": 124 + i,
        "title": "Libro " + str(random.randint(1, 9999)),
        "author": "Autor " + str(random.randint(1, 9999)),
        "isbn": str(random.randint(1000000000000, 9999999999999))
    }

    respuesta = requests.post(url, json=libro, headers=headers)
    print("Libro", i + 1, respuesta.status_code)

    if respuesta.status_code not in (200, 201):
        print(respuesta.text)
        break

# Listar todos los libros
respuesta = requests.get(
    url + "?includeISBN=true&sortBy=author"
)

print("\nLISTADO DE LIBROS")
print(respuesta.json())
