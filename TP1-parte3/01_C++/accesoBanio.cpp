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

mutex imprimirPantalla;
mutex accesoRegionCritica;
counting_semaphore<3> turno(3);

enum Baño
{
    VACIO = 0,
    HAY_HOMBRES = 1,
    HAY_MUJERES = 2
};

int cantidadMujeres = 0;
int cantidadHombres = 0;
int situacionBaño = VACIO;

void mujeres(int numero)
{
    string nombre = "Mujer " + to_string(numero);

    turno.acquire();
    if (situacionBaño == HAY_HOMBRES)
    {
        turno.release();
        while (situacionBaño == HAY_HOMBRES)
        {
            imprimirPantalla.lock();
            cout << nombre + " esperando" << endl;
            cout << "-----------------------------------------" << endl;
            imprimirPantalla.unlock();
            sleep_for(seconds(1));
        }
        turno.acquire();
    }
    accesoRegionCritica.lock();
    cantidadMujeres++;
    if (cantidadMujeres == 1)
    {
        situacionBaño = HAY_MUJERES;
    }
    imprimirPantalla.lock();
    cout << nombre + " entro al baño." << endl;
    cout << "\t- CantidadHombres: " + to_string(cantidadHombres) + "\n\t- CantidadMujeres: " + to_string(cantidadMujeres) << endl;
    cout << "-----------------------------------------" << endl;
    imprimirPantalla.unlock();
    accesoRegionCritica.unlock();

    sleep_for(seconds(2));

    accesoRegionCritica.lock();
    cantidadMujeres--;
    if (cantidadMujeres == 0)
    {
        situacionBaño = VACIO;
    }
    accesoRegionCritica.unlock();
    turno.release();
    imprimirPantalla.lock();
    cout << nombre + " sale del baño." << endl;
    cout << "-----------------------------------------" << endl;
    imprimirPantalla.unlock();
    sleep(0.1);
}

void hombres(int numero)
{
    string nombre = "Hombre " + to_string(numero);

    turno.acquire();
    if (situacionBaño == HAY_MUJERES)
    {
        turno.release();
        while (situacionBaño == HAY_MUJERES)
        {
            imprimirPantalla.lock();
            cout << nombre + " esperando" << endl;
            cout << "-----------------------------------------" << endl;
            imprimirPantalla.unlock();
        }
        turno.acquire();
    }
    accesoRegionCritica.lock();
    cantidadHombres++;
    if (cantidadHombres == 1)
    {
        situacionBaño = HAY_HOMBRES;
    }
    imprimirPantalla.lock();
    cout << nombre + " entro al baño." << endl;
    cout << "\t- CantidadHombres: " + to_string(cantidadHombres) + "\n\t- CantidadMujeres: " + to_string(cantidadMujeres)<< endl;
    cout << "-----------------------------------------" << endl;
    imprimirPantalla.unlock();
    accesoRegionCritica.unlock();

    sleep_for(seconds(2));

    accesoRegionCritica.lock();
    cantidadHombres--;
    if (cantidadHombres == 0)
    {
        situacionBaño = VACIO;
    }
    accesoRegionCritica.unlock();
    turno.release();
    imprimirPantalla.lock();
    cout << nombre + " sale del baño." << endl;
    cout << "-----------------------------------------" << endl;
    imprimirPantalla.unlock();
}

void agregarHilo(vector<thread> &grupo, int cantidadPersonas, void (*funcionGenero)(int))
{
    for (int i = 0; i < cantidadPersonas; i++)
    {
        grupo.push_back(thread(funcionGenero, i));
    }
}

void unirHilos(vector<thread> &grupo)
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

    int cantidadPersonas = stoi(argv[1]);

    if (cantidadPersonas < 0)
    {
        cout << "Ingrese cantidad de hombres y mujeres mayor a 0 " << endl;
        return EXIT_FAILURE;
    }
    cout << "-----------------------------------------" << endl;
    cout << "Comienzo de jornada laboral." << endl;
    cout << "-----------------------------------------" << endl;

    vector<thread> grupoHombres;

    vector<thread> grupoMujeres;

    agregarHilo(grupoHombres, cantidadPersonas, hombres);

    agregarHilo(grupoMujeres, cantidadPersonas, mujeres);

    unirHilos(grupoHombres);

    unirHilos(grupoMujeres);

    cout << "Fin de la jornada laboral." << endl;
    cout << "-----------------------------------------\n" << endl;

    return EXIT_SUCCESS;
}
