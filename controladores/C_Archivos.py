
import csv
def read_tsp_file(file_path):
    tsp_data = {}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('NAME'):
                tsp_data['NAME'] = line.split(': ')[1]
            elif line.startswith('TYPE'):
                tsp_data['TYPE'] = line.split(': ')[1]
            elif line.startswith('COMMENT'):
                tsp_data['COMMENT'] = line.split(': ')[1]
            elif line.startswith('DIMENSION'):
                tsp_data['DIMENSION'] = int(line.split(': ')[1])
            elif line.startswith('EDGE_WEIGHT_TYPE'):
                tsp_data['EDGE_WEIGHT_TYPE'] = line.split(': ')[1]
            elif line == 'NODE_COORD_SECTION':
                tsp_data['NODE_COORD_SECTION'] = []
                for node_line in file:
                    if node_line.strip() == '' or node_line.startswith('EOF'):
                       
                        break
                    node_data = node_line.split()
                    node_id = int(node_data[0])
                    x_coord = float(node_data[1])
                    y_coord = float(node_data[2])
                    tsp_data['NODE_COORD_SECTION'].append((node_id, x_coord, y_coord))

    return tsp_data


def archivo_save_output(filename, output):
    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(output)
    except IOError as e:
        print(f"Error al guardar el archivo {filename}: {e}")


def save_log(filename, text):
    try:
        with open(filename, 'a') as file:
            file.write(text + "\n")
        print(f"Appended to the log file: {filename}")
    except IOError as e:
        print(f"Error while saving the file {filename}: {e}")
