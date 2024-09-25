public class Cliente extends Thread
{

  private int nombre;
  private int cantidadAComprar;

  public Cliente(int nombre, int cantidadAComprar)
  {
    this.nombre = nombre;
    this.cantidadAComprar = cantidadAComprar;
  }

  public void run()
  {
    try
    {
      while (true)
      {
        Gondola.accesoProductos.acquire();
        if (Gondola.productos >= cantidadAComprar)
        {
          Gondola.productos -= cantidadAComprar;
          System.out.println("-----------------------------------------------------------");
          System.out.println("Cliente: " + nombre + " esta comprando " + cantidadAComprar + " productos.");
          System.out.println("Productos en gondola despues de la compra: " + Gondola.productos);
          System.out.println("-----------------------------------------------------------");
          Gondola.accesoProductos.release();
          break;
        }
        else
        {
          Gondola.accesoProductos.release();
          sleep(1000);
        }
      }

    }
    catch (InterruptedException e)
    {
      e.printStackTrace();
    }
  }
}