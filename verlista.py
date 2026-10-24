
import requests

url = "http://library.demo.local/api/v1/books"

respuesta = requests.get(
    url,
    params={
        "includeISBN": "true",
        "sortBy": "author"
    }
)

print("HTTP:", respuesta.status_code)

if respuesta.status_code == 200:
    libros = respuesta.json()

    for libro in libros:
        print("ID:", libro.get("id"))
        print("Autor:", libro.get("author"))
        print("Titulo:", libro.get("title"))
        print("ISBN:", libro.get("isbn", "Sin ISBN"))
        print("-----------------------")

    print("Total:", len(libros))
else:
    print(respuesta.text)
