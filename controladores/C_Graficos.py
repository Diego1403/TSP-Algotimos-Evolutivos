import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os  # Import the os module for file operations

# Apply the default theme
sns.set_theme()


def showplot_cost(csv_path):
    dat = pd.read_csv(csv_path)

    # Get unique datasets, n_ejecuciones, and algoritmo
    unique_datasets = dat['dataset'].unique()
    unique_n_ejecuciones = dat['n_ejecuciones'].unique()
    unique_algoritmos = dat['algoritmo'].unique()

    # Create a new plot for each combination of dataset, n_ejecuciones, and algoritmo
    for dataset in unique_datasets:
        for n_ejecuciones in unique_n_ejecuciones:
            for algoritmo in unique_algoritmos:
                # Filter data for the current combination
                subset_data = dat[(dat['dataset'] == dataset) &
                                  (dat['n_ejecuciones'] == n_ejecuciones) &
                                  (dat['algoritmo'] == algoritmo)]

                # Skip empty subsets
                if subset_data.empty:
                    continue

                # Create a plot for the current combination
                    plot = sns.relplot(
                        data=dat,
                        kind="line",
                        x="ite", y="coste",
                        hue="algoritmo",
                        style="algoritmo",
                        facet_kws=dict(sharex=False),
                    )
                plot = sns.relplot(
                    data=subset_data,
                    kind="line",
                    x="ite", y="coste",
                    col="n_ejecuciones",
                    hue="algoritmo",
                    style="algoritmo",
                    facet_kws=dict(sharex=False),
                )

                # Adjust y-axis limits if needed

                # Save the plot in the "logs/" directory
                log_dir = "logs"
                os.makedirs(log_dir, exist_ok=True)
                csv_path_without_extension = os.path.splitext(
                    os.path.basename(csv_path))[0]
                filename = f"costs_{csv_path_without_extension}_{
                    dataset}_n{n_ejecuciones}_{algoritmo}.png"
                plot.savefig(os.path.join(log_dir, filename))

                # Close the plot to ensure a new window for the next combination
                plt.close()

    # Display all the plots
    plt.show()


def show_scatter(csv_path):
    dat = pd.read_csv(csv_path)
    df = pd.DataFrame(dat)

    # Plotting
    # Plotting
    sns.set(style="darkgrid")
    g = sns.FacetGrid(df, col="dataset", row="algoritmo",
                      hue="algoritmo", margin_titles=True)
    g.map(plt.scatter, "ite", "coste").add_legend()
    plt.legend()
    plt.show()


def showplot_time(csv_path):
    dat = pd.read_csv(csv_path)
    plot = sns.catplot(
        data=dat,
        x="Ite", y="tiempo_ejecucion",
        kind="point",  # Show a line between points
    )

    # Save the plot in the "logs/" directory
    log_dir = "logs"
    # Create the "logs/" directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    csv_path = csv_path.replace(".", "")  # Remove ".dat" extension
    csv_path = csv_path.replace("logs/log_", "")  # Remove "/log" extension
    plot.savefig(os.path.join(log_dir, "time_"+csv_path + ".png"))

    plt.show()


def showComparisonAlgorithms(dataset):
    PATH = 'logs/'  # Use your path
    # Get the list of all files in the current directory
    files = os.listdir(PATH)
    files = [file for file in files if file.endswith(
        ".csv") and "ford01" in file.lower()]
    print(files)

    # Iterate through the matching files and generate comparison plots
    for file in files:
        dat = pd.read_csv(PATH+file)

        sns.relplot(
            data=dat, kind="line",
            x="Ite", y="Coste", style="event",
        )

        # Adjust y-axis limits if needed
        # axes[0].set_ylim(3700, 4000)

        # Save the plot in the "logs/" directory
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        plt.savefig(os.path.join(log_dir, "comparison_"+file+".png"))

        plt.show()
