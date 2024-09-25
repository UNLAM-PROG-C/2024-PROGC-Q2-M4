public class Repositor extends Thread
{

  private static int turno = Constantes.PRIMER_TURNO;

  private int numero;
  private int cantidadAReponer;

  public Repositor(int numero, int cantidadAReponer)
  {
    this.numero = numero;
    this.cantidadAReponer = cantidadAReponer;
  }

  public void cambiarTurno()
  {
    turno = Repositor.turno == Constantes.PRIMER_TURNO ? Constantes.SEGUNDO_TURNO : Constantes.PRIMER_TURNO;
  }

  public void run()
  {
    try
    {
      while (Gondola.reposicionActiva)
      {
        Gondola.accesoProductos.acquire();
        if (Gondola.productos < Constantes.CANTIDAD_MAXIMA_PRODUCTOS && turno == numero)
        {
          int cantidadReponer = Math.min(Constantes.CANTIDAD_MAXIMA_PRODUCTOS - Gondola.productos, cantidadAReponer);
          Gondola.productos += cantidadReponer;
          System.out.println("-----------------------------------------------------------");
          System.out.println("Repositor: " + numero + " esta reponiendo " + cantidadReponer + " productos.");
          System.out.println("Productos en gondola despues de la reposición: " + Gondola.productos);
          System.out.println("-----------------------------------------------------------");
          cambiarTurno();
          Gondola.accesoProductos.release();
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