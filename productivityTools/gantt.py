import csv
import matplotlib.pyplot as plt
from datetime import datetime
import argparse

def read_tasks_from_csv(file_path):
    tasks = []
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # Convert start and end dates to datetime objects
            row['start'] = datetime.strptime(row['start'], '%Y-%m-%d')
            row['end'] = datetime.strptime(row['end'], '%Y-%m-%d')

            # Split the people responsible into a list
            row['people_responsible'] = row['people_responsible'].split(',')

            # Convert is_milestone to boolean
            row['is_milestone'] = bool(int(row['is_milestone']))

            tasks.append(row)
    return tasks

from datetime import datetime, date

def create_gantt_chart(tasks):
    fig, ax = plt.subplots(figsize=(8, 5))

    # Filtra les tasques eliminades
    tasks = [task for task in tasks if not task['delete']]

    # Estableix el límit inferior de l'eix x com la data actual
    current_date = datetime.now().date()
    current_datetime = datetime.combine(current_date, datetime.min.time())

    # Set the labels and ticks for y-axis
    labels = [task['name'] for task in tasks]
    ax.set_yticks(range(5, len(labels) * 10 + 5, 10))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()

    # Reference date for converting datetime to numeric values
    reference_date = datetime(1970, 1, 1)

    # Plot the bars for each task and milestone
    for i, task in enumerate(tasks):
        start = (task['start'] - reference_date).days
        end = (task['end'] - reference_date).days
        duration = end - start

        if task['start'].date() < current_date and task['end'].date() < current_date:
            # Tasca totalment fora del gràfic
            current_date = task['start'].date()
            current_datetime = datetime.combine(current_date, datetime.min.time())
            ax.barh(i * 10 + 5, duration, left=start, height=8, align='center', color='red', alpha=0.8)
        elif task['is_milestone'] == 'True':
            # Plot milestone as a vertical line
            ax.plot([start, start], [i * 10, i * 10 + 10], color='red', linewidth=2)
            ax.text(start, i * 10 + 15, task['name'], ha='left', va='center', color='red')
        else:
            # Plot task as a horizontal bar
            ax.barh(i * 10 + 5, duration, left=start, height=8, align='center', color='steelblue', alpha=0.8)
            ax.text(start + duration / 2, i * 10 + 5, f'{duration} days', ha='center', va='center', color='white')

            # Display people responsible
            people = ', '.join(task['people_responsible'])
            ax.text(start, i * 10 + 5, people, ha='left', va='center')
 
    # Set the x-axis limits
    min_start = min(task['start'] for task in tasks if task['start'] >= current_datetime)
    max_end = max(task['end'] for task in tasks)
    ax.set_xlim(current_datetime, max_end)

    # Set the x-axis label
    ax.set_xlabel('Days')

    # Set the title
    ax.set_title('Project Schedule')

    # Remove the spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Rotate x-axis tick labels
    plt.xticks(rotation=90)

    # Set grid
    ax.grid(True)

    # Add vertical line for current date
    ax.axvline(x=date.today(), color='black', linewidth=2)

    # Adjust figure layout
    plt.tight_layout()

    # Display the Gantt chart
    plt.show()


# Crear un objecte ArgumentParser
parser = argparse.ArgumentParser(description='Generate Gantt chart from CSV file')

# Afegir l'argument per al camí del fitxer CSV
parser.add_argument('csv_file', type=str, help='Path to the CSV file')

# Parsejar els arguments de la línia de comandes
args = parser.parse_args()

# Obté el camí del fitxer CSV de l'argument
csv_file_path = args.csv_file

# Llegeix el fitxer CSV i guarda les dades en una llista de tasques
tasks = read_tasks_from_csv(csv_file_path)

# Create the Gantt chart
create_gantt_chart(tasks)
