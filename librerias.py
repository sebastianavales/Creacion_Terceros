import subprocess

def install_requirements():
    try:
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)
        print("Librerías instaladas correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar librerías: {e}")

install_requirements()