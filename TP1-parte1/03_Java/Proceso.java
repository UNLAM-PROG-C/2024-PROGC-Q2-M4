import java.io.IOException;

public class Proceso
{
  String nombre;
  public static final int TIEMPO_ESPERA = 10000;

  public Proceso(String nombre)
  {
    this.nombre = nombre;
  }

  public static void espera(int tiempo)
  {
    try
    {
      Thread.sleep(tiempo);
    }
    catch (InterruptedException ie)
    {
      return;
    }
  }

  public static void esperarProcesoHijo(Process proceso)
  {
    try
    {
      int error = proceso.waitFor();
      if (error != 0)
      {
        System.out.println("Error al ejecutar");
      }
    }
    catch (InterruptedException ie)
    {
      ie.printStackTrace();
    }
  }

  public static void procesarRamaE(String[] args)
  {
    Process procesoH = crearProcesoHijo("H");
    Process procesoI = crearProcesoHijo("I");
    esperarProcesoHijo(procesoH);
    esperarProcesoHijo(procesoI);
  }

  public static void procesarRamaD(String[] args)
  {
    Process procesoF = crearProcesoHijo("F");
    Process procesoG = crearProcesoHijo("G");
    esperarProcesoHijo(procesoF);
    esperarProcesoHijo(procesoG);
  }

  public static void main(String[] args) throws InterruptedException
  {
    if (args[0].equals("B"))
    {
      Process procesoC = crearProcesoHijo("C");
      Process procesoD = crearProcesoHijo("D");
      esperarProcesoHijo(procesoC);
      esperarProcesoHijo(procesoD);
    }
    else if (args[0].equals("D"))
    {
      procesarRamaD(args);
    }
    else if (args[0].equals("C"))
    {
      Process procesoE = crearProcesoHijo("E");
      esperarProcesoHijo(procesoE);
    }
    else if (args[0].equals("E"))
    {
      procesarRamaE(args);
    }
    else
    {
      espera(TIEMPO_ESPERA);
    }
  }

  private static Process crearProcesoHijo(String nombre)
  {
    Process proceso = null;
    try
    {
      ProcessBuilder pb = new ProcessBuilder("java", "Proceso.java", nombre);
      pb.redirectErrorStream(true);
      pb.inheritIO();
      proceso = pb.start();
      System.out.println("Proceso " + nombre + " : " + proceso.pid());
    }
    catch (IOException e)
    {
      System.err.println("Error al iniciar el proceso hijo " + nombre + ": " + e.getMessage());
      e.printStackTrace();
    }
    return proceso;
  }
}
