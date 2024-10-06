#include <iostream>
#include <mutex>
#include <semaphore>
#include <sstream>
#include <string>
#include <thread>
#include <unistd.h>
#include <vector>

using namespace std;
using namespace chrono;
using namespace this_thread;

const int TIEMPO_ESPERA = 1;
const int TIEMPO_BAÑO = 2;
const int CAPACIDAD_BAÑO = 3;

mutex imprimir_pantalla;
mutex acceso_region_critica;
mutex acceso_region_critica_1;
mutex esperando;
counting_semaphore<CAPACIDAD_BAÑO> turno(CAPACIDAD_BAÑO);
counting_semaphore<CAPACIDAD_BAÑO> salida(CAPACIDAD_BAÑO);

enum Baño
{
  VACIO = 0,
  HAY_HOMBRES = 1,
  HAY_MUJERES = 2
};

int cantidad_mujeres = 0;
int cantidad_hombres = 0;
int situacion_baño = VACIO;
bool espera_mujeres = false;
bool espera_hombres = false;

void mujeres(int numero)
{
  string nombre = "Mujer " + to_string(numero);

  while (true)
  {
    turno.acquire();
    if (situacion_baño == HAY_HOMBRES && acceso_region_critica_1.try_lock())
    {
      espera_mujeres = true;
      while (situacion_baño == HAY_HOMBRES)
      {
        imprimir_pantalla.lock();
        cout << nombre + " esperando" << endl;
        cout << "-----------------------------------------" << endl;
        imprimir_pantalla.unlock();
        sleep_for(seconds(TIEMPO_ESPERA));
      }
      acceso_region_critica_1.unlock();
    }
    if (situacion_baño != HAY_HOMBRES && !espera_hombres)
    {
      acceso_region_critica.lock();
      cantidad_mujeres++;
      if (cantidad_mujeres >= 1)
      {
        situacion_baño = HAY_MUJERES;
        espera_mujeres = false;
      }
      imprimir_pantalla.lock();
      salida.acquire();
      cout << nombre + " entro al baño." << endl;
      cout << "\t- CantidadHombres: " + to_string(cantidad_hombres) + "\n\t- CantidadMujeres: " + to_string(cantidad_mujeres) << endl;
      cout << "-----------------------------------------" << endl;
      imprimir_pantalla.unlock();
      acceso_region_critica.unlock();

      sleep_for(seconds(TIEMPO_BAÑO));

      imprimir_pantalla.lock();
      cout << nombre + " sale del baño." << endl;
      cout << "-----------------------------------------" << endl;
      salida.release();
      imprimir_pantalla.unlock();

      acceso_region_critica.lock();
      cantidad_mujeres--;
      if (cantidad_mujeres == 0)
      {
        situacion_baño = VACIO;
      }
      acceso_region_critica.unlock();
      turno.release();

      break;
    }
    turno.release();
    sleep_for(seconds(TIEMPO_ESPERA));
  }
}

void hombres(int numero)
{
  string nombre = "Hombre " + to_string(numero);

  while (true)
  {
    turno.acquire();
    if (situacion_baño == HAY_MUJERES && acceso_region_critica_1.try_lock())
    {
      espera_hombres = true;
      while (situacion_baño == HAY_MUJERES)
      {
        imprimir_pantalla.lock();
        cout << nombre + " esperando" << endl;
        cout << "-----------------------------------------" << endl;
        imprimir_pantalla.unlock();
        sleep_for(seconds(TIEMPO_ESPERA));
      }
      acceso_region_critica_1.unlock();
    }
    if (situacion_baño != HAY_MUJERES && !espera_mujeres)
    {
      acceso_region_critica.lock();
      cantidad_hombres++;
      if (cantidad_hombres >= 1)
      {
        situacion_baño = HAY_HOMBRES;
        espera_hombres = false;
      }
      imprimir_pantalla.lock();
      salida.acquire();
      cout << nombre + " entro al baño." << endl;
      cout << "\t- CantidadHombres: " + to_string(cantidad_hombres) + "\n\t- CantidadMujeres: " + to_string(cantidad_mujeres) << endl;
      cout << "-----------------------------------------" << endl;
      imprimir_pantalla.unlock();
      acceso_region_critica.unlock();

      sleep_for(seconds(TIEMPO_BAÑO));

      imprimir_pantalla.lock();
      cout << nombre + " sale del baño." << endl;
      cout << "-----------------------------------------" << endl;
      salida.release();
      imprimir_pantalla.unlock();

      acceso_region_critica.lock();
      cantidad_hombres--;
      if (cantidad_hombres == 0)
      {
        situacion_baño = VACIO;
      }
      acceso_region_critica.unlock();
      turno.release();

      break;
    }
    turno.release();
    sleep_for(seconds(TIEMPO_ESPERA));
  }
}

void agregar_hilo(vector<thread> &grupo, int cantidad_personas, void (*funcion_genero)(int))
{
  for (int i = 0; i < cantidad_personas; i++)
  {
    grupo.push_back(thread(funcion_genero, i));
  }
}

void unir_hilos(vector<thread> &grupo)
{
  for (auto &hilo : grupo)
  {
    if (hilo.joinable())
    {
      hilo.join();
    }
  }
}

int main(int argc, char *argv[])
{
  if (argc < 2)
  {
    cout << "Uso: " << argv[0] << " <cantidad de hombres y mujeres>" << endl;
    return EXIT_FAILURE;
  }

  int cantidad_personas = stoi(argv[1]);

  if (cantidad_personas < 0)
  {
    cout << "Ingrese cantidad de hombres y mujeres mayor a 0 " << endl;
    return EXIT_FAILURE;
  }
  cout << "-----------------------------------------" << endl;
  cout << "Comienzo de jornada laboral." << endl;
  cout << "-----------------------------------------" << endl;

  vector<thread> grupo_hombres;
  vector<thread> grupo_mujeres;

  agregar_hilo(grupo_mujeres, cantidad_personas, mujeres);
  agregar_hilo(grupo_hombres, cantidad_personas, hombres);

  unir_hilos(grupo_hombres);
  unir_hilos(grupo_mujeres);

  cout << "Fin de la jornada laboral." << endl;
  cout << "-----------------------------------------\n"
       << endl;

  return EXIT_SUCCESS;
}