import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Scanner;

public class ProcesadorArchivo
{
  public static void eliminarLineasVacias(String archivoOriginal, List<String> listaLineas)
  {
    File archivo = null;
    Scanner sc = null;
    try
    {
      archivo = new File(archivoOriginal);
      sc = new Scanner(archivo);
      String linea;
      while (sc.hasNext())
      {
        linea=sc.nextLine();
        if (!linea.isEmpty())
        {
          listaLineas.add(linea);
        }
      }
    }
    catch (IOException e)
    {
      System.err.println("Error al abrir el archivo de entrada.");
      e.printStackTrace();
    }
    sc.close();
  }
}
