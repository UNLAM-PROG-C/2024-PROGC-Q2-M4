import java.io.IOException;
import java.lang.management.ManagementFactory;

public class Main
{
  public static void main(String[] args)
  {
    System.out.println("Proceso A: " + ManagementFactory.getRuntimeMXBean().getPid());

    try
    {
      ProcessBuilder pb = new ProcessBuilder("java", "Proceso.java", "B");

      pb.redirectErrorStream(true);
      pb.inheritIO();

      Process proceso = pb.start();
      System.out.println("Proceso B : " + proceso.pid());

      int error = proceso.waitFor();

      if (error != 0)
      {
        System.out.println("Error al ejecutar");
      }
    }
    catch (IOException e)
    {
      e.printStackTrace();
    }
    catch (InterruptedException e)
    {
      e.printStackTrace();
    }
  }
}
