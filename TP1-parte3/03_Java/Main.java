public class Main
{
  public static void main(String[] args) throws InterruptedException
  {

    if (args.length < 1 || Integer.parseInt(args[0]) < 0)
    {
      System.out.println("La cantidad de clientes debe ser positiva");
      return;
    }

    int numClientes = Integer.parseInt(args[0]);

    Repositor repo1 = new Repositor(1, Constantes.CANTIDAD_MAXIMA_PRODUCTOS);
    Repositor repo2 = new Repositor(2, Constantes.CANTIDAD_MAXIMA_PRODUCTOS);

    repo1.start();
    repo2.start();

    Gondola gondola = new Gondola();

    Cliente[] clientes = gondola.obtenerClientes(numClientes);

    for (int i = 0; i < numClientes; i++)
    {
      clientes[i].join();
    }

    Gondola.reposicionActiva = false;

    repo1.join();
    repo2.join();
  }
}
