\
import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "408c2ea7-3fce-44fc-a20c-ca067403c887"


def geocoding(location, key):
    url = geocode_url + urllib.parse.urlencode({
        "q": location, "limit": "1", "key": key
    })

    respuesta = requests.get(url, timeout=20)
    datos = respuesta.json()
    estado = respuesta.status_code

    if estado == 200 and datos.get("hits"):
        lugar = datos["hits"][0]
        lat = lugar["point"]["lat"]
        lng = lugar["point"]["lng"]
        nombre = lugar["name"]
        print("Ubicacion encontrada:", nombre)
        return estado, lat, lng, nombre

    print("No se pudo encontrar:", location)
    print("Estado HTTP:", estado)
    if estado != 200:
        print("Detalle:", datos.get("message", datos))
    return estado, None, None, location


while True:
    origen = input("\nIngrese origen (s o salir): ").strip()
    if origen.lower() in ("s", "salir"):
        break

    destino = input("Ingrese destino (s o salir): ").strip()
    if destino.lower() in ("s", "salir"):
        break

    if not origen or not destino:
        print("Debe ingresar origen y destino.")
        continue

    try:
        orig = geocoding(origen, key)
        dest = geocoding(destino, key)

        if orig[1] is None or dest[1] is None:
            print("No es posible calcular el recorrido.")
            continue

        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])

        paths_url = route_url + urllib.parse.urlencode({
            "key": key,
            "profile": "car",
            "locale": "es",
            "instructions": "true"
        }) + op + dp

        respuesta = requests.get(paths_url, timeout=30)
        print("Estado de la API de rutas:", respuesta.status_code)
        datos = respuesta.json()

        if respuesta.status_code == 200 and datos.get("paths"):
            ruta = datos["paths"][0]

            km = ruta["distance"] / 1000
            millas = km / 1.61
            minutos = ruta["time"] / 60000

            print("\nRuta desde", orig[3], "hasta", dest[3])
            print("Distancia: {:.2f} km / {:.2f} millas".format(km, millas))
            print("Duracion: {:.2f} minutos".format(minutos))

            print("\nINSTRUCCIONES DEL RECORRIDO:")
            for paso in ruta["instructions"]:
                print("{} ({:.2f} km)".format(
                    paso["text"], paso["distance"] / 1000
                ))
        else:
            print("Error al calcular la ruta:",
                  datos.get("message", datos))

    except requests.exceptions.RequestException as error:
        print("Error de conexion:", error)
    except (ValueError, KeyError, IndexError) as error:
        print("Error al procesar la respuesta:", error)

print("Programa finalizado")
