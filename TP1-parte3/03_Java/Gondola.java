import java.util.concurrent.Semaphore;

public class Gondola
{

  public static int productos = 0;
  static Semaphore accesoProductos = new Semaphore(1);
  static boolean reposicionActiva = true;

  public Cliente[] obtenerClientes(int cantidadClientes)
  {
    Cliente[] clientes = new Cliente[cantidadClientes];
    for (int i = 0; i < cantidadClientes; i++)
    {
      clientes[i] = new Cliente(i, (int) (Math.random() * 2) + 1);
      clientes[i].start();
    }
    return clientes;
  }
}