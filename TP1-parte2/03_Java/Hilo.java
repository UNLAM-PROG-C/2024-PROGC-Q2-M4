import java.util.List;

public class Hilo extends Thread
{
  int numero;
  int indiceInferior;
  int indiceSuperior;
  int[] vectorSumaParcial;
  List<String> listaLineas;

  public Hilo(int numero,List<String> listaLineas,int indiceInferior,int indiceSuperior,int[] vectorSumaParcial)
  {
    this.numero=numero;
    this.indiceInferior=indiceInferior;
    this.indiceSuperior=indiceSuperior;
    this.listaLineas=listaLineas;
  }

  public void run()
  {
    this.contadorCaracteresEnRango(listaLineas, this.indiceInferior, this.indiceSuperior,vectorSumaParcial);
  }

  private void contadorCaracteresEnRango(List<String> lineas, int inicio, int fin,int[] vectorSumaParcial)
  {
    for (int i = inicio; i <= fin; i++)
    {
      Main.setValorVector(numero,lineas.get(i).length());
    }
  }
}