import speech_recognition as sr
import pyttsx3
import subprocess
import os
import webbrowser
import datetime
import pyautogui
import time


# ==========================================
# CONFIGURACIÓN
# ==========================================

NOMBRE = "M.A.X"

# Motor de voz
voz = pyttsx3.init()
voz.setProperty("rate", 175)
voz.setProperty("volume", 1.0)

# Buscar voz en español
voces = voz.getProperty("voices")

for v in voces:
    nombre_voz = v.name.lower()

    if "spanish" in nombre_voz or "español" in nombre_voz:
        voz.setProperty("voice", v.id)
        break


# ==========================================
# HABLAR
# ==========================================

def hablar(texto):

    print("MAX:", texto)

    voz.say(texto)
    voz.runAndWait()


# ==========================================
# ESCUCHAR
# ==========================================

reconocedor = sr.Recognizer()


def escuchar():

    try:

        with sr.Microphone() as fuente:

            print("\n DIME...")

            reconocedor.adjust_for_ambient_noise(
                fuente,
                duration=0.5
            )

            audio = reconocedor.listen(
                fuente,
                timeout=5,
                phrase_time_limit=8
            )

    except sr.WaitTimeoutError:

        print("No escuché nada.")

        return ""

    except Exception as error:

        print("Error del micrófono:", error)

        return ""

    try:

        texto = reconocedor.recognize_google(
            audio,
            language="es-ES"
        )

        texto = texto.lower().strip()

        print("TÚ:", texto)

        return texto

    except sr.UnknownValueError:

        print("No entendí sr...")

        return ""

    except sr.RequestError:

        hablar(
            "No puedo conectarme al servicio de reconocimiento."
        )

        return ""


# ==========================================
# ABRIR PROGRAMAS
# ==========================================

def abrir_programa(programa):

    try:

        subprocess.Popen(programa)

        hablar("Abriendo " + programa)

    except Exception as error:

        print("Error:", error)

        hablar("No pude abrir el programa.")


# ==========================================
# DOCUMENTOS
# ==========================================

def abrir_documentos():

    documentos = os.path.join(
        os.environ["USERPROFILE"],
        "Documents"
    )

    if os.path.exists(documentos):

        os.startfile(documentos)

        hablar("Abriendo documentos.")

    else:

        hablar("No encontré la carpeta documentos.")


# ==========================================
# DESCARGAS
# ==========================================

def abrir_descargas():

    descargas = os.path.join(
        os.environ["USERPROFILE"],
        "Downloads"
    )

    if os.path.exists(descargas):

        os.startfile(descargas)

        hablar("Abriendo descargas.")

    else:

        hablar("No encontré la carpeta descargas.")


# ==========================================
# COMANDOS
# ==========================================

def ejecutar_comando(comando):
    print(comando)
    # -------------------------
    # HORA
    # -------------------------

    if "hora" in comando:
        hora = datetime.datetime.now().strftime("%H:%M")
        hablar("Son las " + hora)


    # -------------------------
    # FECHA
    # -------------------------

    elif "fecha" in comando:

        fecha = datetime.datetime.now().strftime("%d/%m/%Y")

        hablar("Hoy es " + fecha)


    # -------------------------
    # CHROME
    # -------------------------

    elif (
        "abre chrome" in comando
        or "abrir chrome" in comando
        or "chrome" == comando
    ):

        abrir_programa("chrome.exe")


    # -------------------------
    # SPOTIFY
    # -------------------------

    elif (
        "abre spotify" in comando
        or "abrir spotify" in comando
    ):

        abrir_programa("spotify.exe")


    # -------------------------
    # CALCULADORA
    # -------------------------

    elif (
        "abre calculadora" in comando
        or "abrir calculadora" in comando
        or "calculadora" == comando
    ):

        abrir_programa("calc.exe")


    # -------------------------
    # EXPLORADOR
    # -------------------------

    elif (
        "abre explorador" in comando
        or "abrir explorador" in comando
        or "abre archivos" in comando
        or "abrir archivos" in comando
    ):

        os.startfile("C:\\")
        hablar("Abriendo el explorador de archivos.")


    # -------------------------
    # DOCUMENTOS
    # -------------------------

    elif (
        "abre documentos" in comando
        or "abrir documentos" in comando
        or "documentos" == comando
    ):

        abrir_documentos()


    # -------------------------
    # DESCARGAS
    # -------------------------

    elif (
        "abre descargas" in comando
        or "abrir descargas" in comando
        or "descargas" == comando
    ):

        abrir_descargas()


    # -------------------------
    # YOUTUBE
    # -------------------------

    elif (
        "abre youtube" in comando
        or "abrir youtube" in comando
        or "youtube" == comando
    ):

        webbrowser.open("https://www.youtube.com")

        hablar("Abriendo YouTube.")


    # -------------------------
    # GOOGLE
    # -------------------------

    elif (
        "abre google" in comando
        or "abrir google" in comando
        or "google" == comando
    ):

        webbrowser.open(
            "https://www.google.com"
        )

        hablar("Abriendo Google.")


    # -------------------------
    # BUSCAR
    # -------------------------

    elif comando.startswith("busca"):

        busqueda = comando.replace(
            "busca",
            "",
            1
        ).strip()

        if busqueda:

            url = (
                "https://www.google.com/search?q="
                + busqueda.replace(" ", "+")
            )

            webbrowser.open(url)

            hablar(
                "Buscando " + busqueda
            )

        else:

            hablar(
                "¿Qué quieres que busque?"
            )


    # -------------------------
    # CAPTURA
    # -------------------------

    elif (
        "captura" in comando
        or "captura de pantalla" in comando
    ):

        carpeta = os.path.join(
            os.environ["USERPROFILE"],
            "Pictures"
        )

        os.makedirs(
            carpeta,
            exist_ok=True
        )

        nombre = (
            "captura_"
            + datetime.datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
            + ".png"
        )

        ruta = os.path.join(
            carpeta,
            nombre
        )

        pyautogui.screenshot().save(ruta)

        hablar(
            "Captura guardada."
        )

        print(
            "Guardada en:",
            ruta
        )


    # -------------------------
    # BLOQUEAR
    # -------------------------

    elif (
        "bloquea la computadora" in comando
        or "bloquea la pc" in comando
        or "bloquear computadora" in comando
        or "bloquear pc" in comando
    ):

        hablar(
            "Bloqueando la computadora."
        )

        time.sleep(1)

        subprocess.run(
            [
                "rundll32.exe",
                "user32.dll,LockWorkStation"
            ]
        )


    # -------------------------
    # APAGAR
    # -------------------------

    elif (
        "apaga la computadora" in comando
        or "apaga la pc" in comando
    ):

        hablar(
            "El equipo se apagará en cinco segundos."
        )

        time.sleep(2)

        subprocess.run(
            [
                "shutdown",
                "/s",
                "/t",
                "5"
            ]
        )


    # -------------------------
    # REINICIAR
    # -------------------------

    elif (
        "reinicia la computadora" in comando
        or "reinicia la pc" in comando
    ):

        hablar(
            "El equipo se reiniciará en cinco segundos."
        )

        time.sleep(2)

        subprocess.run(
            [
                "shutdown",
                "/r",
                "/t",
                "5"
            ]
        )


    # -------------------------
    # CANCELAR APAGADO
    # -------------------------

    elif "cancela el apagado" in comando:

        subprocess.run(
            [
                "shutdown",
                "/a"
            ]
        )

        hablar(
            "Apagado cancelado."
        )


    # -------------------------
    # SALIR
    # -------------------------

    elif (
        "cerrar MAX" in comando
        or "apagar MAX" in comando
        or "cerrar asistente" in comando
        or "apagar asistente" in comando
    ):

        hablar(
            "Hasta luego."
        )

        return False


    # -------------------------
    # NO RECONOCIDO
    # -------------------------

    else:

        hablar(
            "No tengo ese comando todavía."
        )

    return True


# ==========================================
# INICIAR M.A.X
# ==========================================

def iniciar():

    print("=" * 50)
    print("       M.A.X ")
    print("=" * 50)

    hablar(
        "BUENAS, EN QUE TE AYUDO."
    )

    while True:

        comando = escuchar()

        if not comando:
            continue
        print(
            "ORDEN:",
            comando
        )
        continuar = ejecutar_comando(
            comando
        )
        if not continuar:
            break

if __name__ == "__main__":

    try:

        iniciar()

    except KeyboardInterrupt:

        print(
            "\nM.A.X cerrado."
        )

    except Exception as error:

        print(
            "\nERROR:"
        )

        print(error)

        hablar(
            "Se produjo un error."
        )