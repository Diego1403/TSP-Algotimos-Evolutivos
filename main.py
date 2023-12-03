import configparser
from classes.Info_Ejecucion import Info_Ejecucion
from algoritmos.evolucion_genetica_moc import algoritmo_genetico_moc
from algoritmos.evolucion_genetica_ox2 import algoritmo_genetico_ox2

from algoritmos.evolucion_diferencial_a import evolucion_diferencial_a
from algoritmos.evolucion_diferencial_b import evolucion_diferencial_b

import time
import winsound
frec = 1000 
dur = 1000 

def main():

    winsound.Beep(frec, dur)
    f = open("general_log.txt", "w")

    config = configparser.ConfigParser()
    config.read('config.ini')

    # Extract configuration values
    kWorst = int(config.get('default', 'kWorst'))
    evaluaciones = int(config.get('default', 'evaluaciones'))
    semilla = int(config.get('default', 'semilla'))
    prob_cruce = float(config.get('default', 'prob_cruce'))
    prob_mutacion = float(config.get('default', 'prob_mutacion'))
    IE = Info_Ejecucion(prob_mutacion, prob_cruce, semilla, evaluaciones, kWorst)

    algoritmos = config.get('default', 'algoritmos').split()
    datasets = config.get('default', 'dataset').split()
    n_elites = [int(e) for e in config.get('default', 'E').split()]
    kBest = [int(k) for k in config.get('default', 'kBest').split()]
    n_individuos = [int(n) for n in config.get('default', 'n_individuos').split()]

    data = {"algoritmo": "", "dataset": "", "tam_poblacion": "", "E": "", "kBest": "", "tipo_diferencial": ""}
    print("start!")
    for dataset in datasets:
        data["dataset"] = dataset
        IE.update_dataset(dataset)

        for tam_poblacion in n_individuos:
            data["tam_poblacion"] = tam_poblacion
            
            for algoritmo in algoritmos:
                data["algoritmo"] = algoritmo
                print(f'Ejecutando {algoritmo} con {dataset}')
                start_time = time.time()

                for e in n_elites:
                    data["E"] = e
                    for kbest in kBest:
                        data["kBest"] = kbest

                        IE.update_data(dataset,data)
                        # Implement the logic for each algorithm here, similar to your original code
                        if algoritmo == "GenOX2":
                            mejor_solucion , mejor_distancia = algoritmo_genetico_ox2(IE);
                            f.writelines(["Archivo:",str(dataset),"\n",
                                    "Poblacion:",str(tam_poblacion),"\n",
                                    "Algoritmo:",str(algoritmo),"\n",
                                    "Semilla:",str(semilla),"\n",
                                    "Elites:",str(e),"\n",
                                    "kBest:",str(kbest),"\n",
                                    "Mejor Distancia:",str(mejor_distancia),"\n"])
                            pass
                        elif algoritmo == "GenMOC":
                            mejor_solucion , mejor_distancia = algoritmo_genetico_moc(IE);
                            f.writelines(["Archivo:",str(dataset),"\n",
                                    "Poblacion:",str(tam_poblacion),"\n",
                                    "Algoritmo:",str(algoritmo),"\n",
                                    "Semilla:",str(semilla),"\n",
                                    "Elites:",str(e),"\n",
                                    "kBest:",str(kbest),"\n",
                                    "Mejor Distancia:",str(mejor_distancia),"\n"])
                            pass
                        elif algoritmo == "EDA":
                            mejor_solucion , mejor_distancia = evolucion_diferencial_a(IE);
                            f.writelines(["Archivo:",str(dataset),"\n",
                                    "Poblacion:",str(tam_poblacion),"\n",
                                    "Algoritmo:",str(algoritmo),"\n",
                                    "Semilla:",str(semilla),"\n",
                                    "Mejor Distancia:",str(mejor_distancia),"\n"])
                            pass
                        elif algoritmo == "EDB":
                            mejor_solucion , mejor_distancia = evolucion_diferencial_b(IE);
                            f.writelines(["Archivo:",str(dataset),"\n",
                                    "Poblacion:",str(tam_poblacion),"\n",
                                    "Algoritmo:",str(algoritmo),"\n",
                                    "Semilla:",str(semilla),"\n",
                                    "Mejor Distancia:",str(mejor_distancia),"\n"])
                            pass

            f.writelines(["Tiempo total:",str((time.time()-start_time)),"\n"])
    winsound.Beep(frec, dur)
    f.close()
if __name__ == "__main__":
    main()
