import configparser
from classes.Info_Ejecucion import Info_Ejecucion
from algoritmos.evolucion_genetica_moc import algoritmo_genetico_moc
from algoritmos.evolucion_genetica_ox2 import algoritmo_genetico_ox2
from algoritmos.evolucion_diferencial import evolucion_diferencial
# Uncomment and import other necessary modules

def main():
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
    n_individuos = [50, 100]

    data = {"algoritmo": "", "dataset": "", "tam_poblacion": "", "E": "", "kBest": "", "tipo_diferencial": ""}

    for dataset in datasets:
        data["dataset"] = dataset
        IE.update_dataset(dataset)

        for algoritmo in algoritmos:
            data["algoritmo"] = algoritmo
            print(f'Ejecutando {algoritmo} con {dataset}')

            for e in n_elites:
                data["E"] = e
                for kbest in kBest:
                    data["kBest"] = kbest

                    for tam_poblacion in n_individuos:
                        data["tam_poblacion"] = tam_poblacion
                        IE.update_data(dataset,data)
                        # Implement the logic for each algorithm here, similar to your original code
                        if algoritmo == "GenOX2":
                            mejor_solucion , mejor_distancia = algoritmo_genetico_ox2(IE);
                            pass
                        elif algoritmo == "GenMOC":
                            mejor_solucion , mejor_distancia = algoritmo_genetico_moc(IE);
                            pass
                        elif algoritmo == "EDA":
                            mejor_solucion , mejor_distancia = evolucion_diferencial(IE);
                            pass
                        elif algoritmo == "EDB":
                            # ... (adapted for EDB specifics)
                            pass
                        # Add additional algorithm cases as needed

            # Print results if any
            if mejor_solucion is not None and mejor_distancia is not None:
                print("Mejor solución encontrada:", mejor_solucion)
                print("Distancia de la mejor solución:", mejor_distancia)

if __name__ == "__main__":
    main()
