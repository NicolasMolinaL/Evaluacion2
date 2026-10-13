import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "68b27b74-d8c2-4741-ba1d-084b051890bd"


def geocoding(location, key):
    while not location.strip():
        location = input("Ingrese la ubicación nuevamente (s/salir para salir): ").strip()
    if location.lower() in ("s", "salir"):
        return None, None, None, location

    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({
        "q": location, "limit": 1, "key": key
    })
    try:
        replydata = requests.get(url, timeout=30)
    except requests.exceptions.RequestException:
        print("Error de conexión. Verifique su acceso a Internet e intente nuevamente.")
        return None, None, None, location
    json_status = replydata.status_code
    try:
        json_data = replydata.json()
    except ValueError:
        print("Estado API Geocodificación:", json_status, "La respuesta no es un JSON válido.")
        return json_status, None, None, location

    if json_status == 200 and json_data.get("hits"):
        hit = json_data["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        name = hit.get("name", location)
        state = hit.get("state", "")
        country = hit.get("country", "")
        value = hit.get("osm_value", "desconocido")
        new_loc = ", ".join(part for part in (name, state, country) if part)
        print("URL API Geocodificación para " + new_loc +
              " (Tipo de Ubicación: " + value + "):\n" + url)
        return json_status, lat, lng, new_loc
    if json_status == 200:
        print("No se encontraron coincidencias. Ingrese una ubicación más específica.")
    else:
        print("Estado API Geocodificación:", json_status)
        print("Mensaje de error:", json_data.get("message", "Error desconocido de la API"))
    return json_status, None, None, location


while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículo: car (auto), bike (bicicleta), foot (a pie)")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profiles = ["car", "bike", "foot"]
    
    vehicle = input("Ingrese un perfil de vehículo (s/salir para salir): ").strip().lower()
    if vehicle in ("s", "salir", "q", "quit"):
        break
    if vehicle not in profiles:
        vehicle = "car"
        print("No se ingresó un perfil válido. Se usará 'car' (auto) por defecto.")

    loc1 = input("Ubicación de Origen: ").strip()
    if loc1.lower() in ("s", "salir"):
        break
    orig = geocoding(loc1, key)
    if orig[3].lower() in ("s", "salir"):
        break
    if orig[0] != 200 or orig[1] is None or orig[2] is None:
        continue

    loc2 = input("Ubicación de Destino: ").strip()
    if loc2.lower() in ("s", "salir"):
        break
    dest = geocoding(loc2, key)
    if dest[3].lower() in ("s", "salir"):
        break
    if dest[0] != 200 or dest[1] is None or dest[2] is None:
        continue

    params = [
        ("key", key),
        ("profile", vehicle),
        ("point", str(orig[1]) + "," + str(orig[2])),
        ("point", str(dest[1]) + "," + str(dest[2])),
        ("instructions", "true"),
        ("locale", "es")
    ]
    paths_url = route_url + urllib.parse.urlencode(params)
    try:
        paths_reply = requests.get(paths_url, timeout=30)
    except requests.exceptions.RequestException:
        print("Error de conexión. Verifique su acceso a Internet e intente nuevamente.")
        continue
    paths_status = paths_reply.status_code
    print("=================================================")
    print("Estado API de Enrutamiento:", paths_status)
    print("URL API de Enrutamiento:\n" + paths_url)
    try:
        paths_data = paths_reply.json()
    except ValueError:
        print("La respuesta no es JSON.")
        continue
    if paths_status != 200:
        print("Mensaje de error:", paths_data.get("message", "Error desconocido de la API"))
        print("*************************************************")
        continue
    if not paths_data.get("paths"):
        print("No se devolvió ninguna ruta.")
        continue

    path = paths_data["paths"][0]
    km = path["distance"] / 1000
    miles = km / 1.61
    total_seconds = int(path["time"] / 1000)
    hr = total_seconds // 3600
    minute = (total_seconds // 60) % 60
    sec = total_seconds % 60

    print("Indicaciones desde " + orig[3] + " hasta " + dest[3] + " en " + vehicle)
    print("Distancia Recorrida: {0:.2f} km / {1:.2f} millas".format(km, miles))
    print("Duración del Viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, minute, sec))
    print("=================================================")

    for instruction in path.get("instructions", []):
        text = instruction["text"]
        distance = instruction["distance"]
        print("{0} ( {1:.2f} km / {2:.2f} millas )".format(
            text, distance / 1000, (distance / 1000) / 1.61
        ))
    print("=================================================")
