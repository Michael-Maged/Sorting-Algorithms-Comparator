import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import random
import math
import csv
import matplotlib.pyplot as plot
from sorting_algorithms import insertionSort, bubbleSort, mergeSort, quickSort, heapSort, selectionSort

def generate_random_data(n):
    return [random.randint(0, 1000) for _ in range(n)]

def load_data(filename):
    data = []
    try:
        with open(filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    data.append(int(row[0]))
                except (ValueError, IndexError):
                    continue
        return data
    except FileNotFoundError:
        messagebox.showerror("Error", f"File {filename} not found.")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return []

def compare_algorithms(data, algorithms):
    steps = []
    for algorithm in algorithms:
        steps.append(algorithm(data.copy()))  # Ensure sorting algorithms return steps
    return steps

def compare_algorithm_vs_asymptotic(data, algorithm, o_func, omega_func, theta_func, n):
    alg_steps = algorithm(data.copy())
    return alg_steps, o_func(n), omega_func(n), theta_func(n)

def displayGraphicalResults(x_vals, y_vals, labels, title):
    plot.figure()
    for i, y in enumerate(y_vals):
        plot.plot(x_vals, y, label=labels[i])

    plot.xlabel("Number of Elements (n)")
    plot.ylabel("Steps")
    plot.title(title)
    plot.legend()
    plot.grid()
    plot.show()

def saveResults(filename, results):
    if not results:
        messagebox.showerror("Error", "No results to save.")
        return

    try:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            # Write headers if the file is empty
            if file.tell() == 0:
                writer.writerow(['Elements', 'Algorithm', 'Steps', 'Big O(n)', 'Big Omega(n)', 'Theta(n)'])
            # Write results to the file
            for result in results:
                if len(result) == 6:  # Ensure the result has the correct number of columns
                    writer.writerow(result)
                else:
                    messagebox.showerror("Error", "Result format is incorrect.")
                    return
        messagebox.showinfo("Success", f"Results saved successfully to {filename}.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save results: {e}")

class AlgorithmTesterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Tester")
        self.root.geometry("800x600")
        self.root.configure(bg="#2C3E50")

        self.data = []
        self.algorithms = {
            "Insertion Sort": insertionSort,
            "Bubble Sort": bubbleSort,
            "Merge Sort": mergeSort,
            "Quick Sort": quickSort,
            "Heap Sort": heapSort,
            "Selection Sort": selectionSort
        }

        self.selected_algorithms = []

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Algorithm Tester", font=("Helvetica", 18, "bold"), bg="#2C3E50", fg="#ECF0F1")
        title_label.pack(pady=10)

        # Data Input Frame
        data_frame = tk.Frame(self.root, bg="#34495E")
        data_frame.pack(pady=10, fill=tk.X, padx=20)

        generate_button = tk.Button(data_frame, text="Generate Random Data", command=self.generate_data, bg="#1ABC9C", fg="white")
        generate_button.pack(side=tk.LEFT, padx=10, pady=10)

        load_button = tk.Button(data_frame, text="Load Data from File", command=self.load_data, bg="#3498DB", fg="white")
        load_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.num_elements_entry = tk.Entry(data_frame, width=10)
        self.num_elements_entry.insert(0, "1000")
        self.num_elements_entry.pack(side=tk.LEFT, padx=10, pady=10)

        # Algorithm Selection Frame
        alg_frame = tk.Frame(self.root, bg="#34495E")
        alg_frame.pack(pady=10, fill=tk.X, padx=20)

        alg_label = tk.Label(alg_frame, text="Select Algorithms:", bg="#34495E", fg="#ECF0F1")
        alg_label.pack(side=tk.LEFT, padx=10)

        self.alg_selection = ttk.Combobox(alg_frame, values=list(self.algorithms.keys()))
        self.alg_selection.pack(side=tk.LEFT, padx=10)

        add_alg_button = tk.Button(alg_frame, text="Add", command=self.add_algorithm, bg="#9B59B6", fg="white")
        add_alg_button.pack(side=tk.LEFT, padx=10)

        remove_alg_button = tk.Button(alg_frame, text="Remove", command=self.remove_algorithm, bg="#E74C3C", fg="white")
        remove_alg_button.pack(side=tk.LEFT, padx=10)

        self.selected_algorithms_listbox = tk.Listbox(alg_frame, height=5)
        self.selected_algorithms_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        # Step Size Frame
        step_frame = tk.Frame(self.root, bg="#34495E")
        step_frame.pack(pady=10, fill=tk.X, padx=20)

        step_label = tk.Label(step_frame, text="Step Size (x-axis):", bg="#34495E", fg="#ECF0F1")
        step_label.pack(side=tk.LEFT, padx=10)

        self.step_size_entry = tk.Entry(step_frame, width=10)
        self.step_size_entry.insert(0, "50")
        self.step_size_entry.pack(side=tk.LEFT, padx=10, pady=10)

        # Action Buttons
        action_frame = tk.Frame(self.root, bg="#34495E")
        action_frame.pack(pady=10, fill=tk.X, padx=20)

        compare_button = tk.Button(action_frame, text="Compare Algorithms", command=self.compare_algorithms, bg="#E67E22", fg="white")
        compare_button.pack(side=tk.LEFT, padx=10, pady=10)

        asymptotic_button = tk.Button(action_frame, text="Compare with Asymptotic", command=self.compare_with_asymptotic, bg="#E74C3C", fg="white")
        asymptotic_button.pack(side=tk.LEFT, padx=10, pady=10)

    def generate_data(self):
        try:
            n = int(self.num_elements_entry.get())
            if n < 0:
                messagebox.showerror("Error", "The number of data points cannot be negative.")
            else :    
                self.data = generate_random_data(n)
                messagebox.showinfo("Success", f"Generated {n} random data points.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def load_data(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if filename:
            self.data = load_data(filename)
            messagebox.showinfo("Success", f"Loaded {len(self.data)} data points from {filename}.")

    def add_algorithm(self):
        alg_name = self.alg_selection.get()
        if alg_name and alg_name not in self.selected_algorithms:
            self.selected_algorithms.append(alg_name)
            self.selected_algorithms_listbox.insert(tk.END, alg_name)

    def remove_algorithm(self):
        selected_index = self.selected_algorithms_listbox.curselection()
        if selected_index:
            selected_algorithm = self.selected_algorithms_listbox.get(selected_index)
            self.selected_algorithms.remove(selected_algorithm)
            self.selected_algorithms_listbox.delete(selected_index)

    def compare_algorithms(self):
        if not self.data:
            messagebox.showerror("Error", "Please load or generate data first.")
            return

        if not self.selected_algorithms:
            messagebox.showerror("Error", "Please select at least one algorithm.")
            return

        try:
            step_size = int(self.step_size_entry.get())
            if step_size <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive step size.")
            return

        algorithms = [self.algorithms[alg] for alg in self.selected_algorithms]
        x_vals = list(range(step_size, len(self.data) + 1, step_size))
        y_vals = []

        steps = []
        for alg in algorithms:
            alg_steps = []
            for i in x_vals:
                subset = self.data[:i]
                alg_steps.append(alg(subset.copy()))
            y_vals.append(alg_steps)
            steps.append(sum(alg_steps))  # Collect total steps for each algorithm

        results = [(len(self.data), algorithm.__name__, step_count, 'N/A', 'N/A', 'N/A') for algorithm, step_count in zip(algorithms, steps)]
        saveResults("results.csv", results)

        displayGraphicalResults(x_vals, y_vals, self.selected_algorithms, "Algorithm Comparison")

    def compare_with_asymptotic(self):
        if not self.data:
            messagebox.showerror("Error", "Please load or generate data first.")
            return

        if not self.selected_algorithms:
            messagebox.showerror("Error", "Please select at least one algorithm.")
            return

        try:
            step_size = int(self.step_size_entry.get())
            if step_size <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive step size.")
            return

        x_vals = list(range(step_size, len(self.data) + 1, step_size))
        results = []

        # Initialize storage for graphical comparison
        y_actual_all = []
        y_big_o_all = []
        y_big_omega_all = []
        y_theta_all = []

        for alg_name in self.selected_algorithms:
            alg = self.algorithms[alg_name]
            o_func, omega_func, theta_func = notations[alg_name]
            y_actual, y_big_o, y_big_omega, y_theta = [], [], [], []

            for i in x_vals:
                subset = self.data[:i]
                actual_steps = alg(subset.copy())
                y_actual.append(actual_steps)
                y_big_o.append(o_func(i))
                y_big_omega.append(omega_func(i))
                y_theta.append(theta_func(i))
                results.append((i, alg_name, actual_steps, o_func(i), omega_func(i), theta_func(i)))

            # Append to global lists for graphical display
            y_actual_all.append(y_actual)
            y_big_o_all.append(y_big_o)
            y_big_omega_all.append(y_big_omega)
            y_theta_all.append(y_theta)

        

        # Combined comparison for all algorithms
        displayGraphicalResults(
            x_vals,
            [y for group in zip(y_actual_all, y_big_o_all, y_big_omega_all, y_theta_all) for y in group],
            [
                f"{alg_name} Actual Steps" for alg_name in self.selected_algorithms
            ] + [
                f"{alg_name} Big O(n)" for alg_name in self.selected_algorithms
            ] + [
                f"{alg_name} Big Omega(n)" for alg_name in self.selected_algorithms
            ] + [
                f"{alg_name} Theta(n)" for alg_name in self.selected_algorithms
            ],
            "Asymptotic Analysis",
        )

        saveResults("results.csv", results)


notations = {
    "Insertion Sort": (lambda n: n**2, lambda n: n, lambda n: n**2),
    "Bubble Sort": (lambda n: n**2, lambda n: n, lambda n: n**2),
    "Merge Sort": (lambda n: n * math.log(n, 2), lambda n: n * math.log(n, 2), lambda n: n * math.log(n, 2)),
    "Quick Sort": (lambda n: n * math.log(n, 2), lambda n: n * math.log(n, 2), lambda n: n * math.log(n, 2)),
    "Heap Sort": (lambda n: n * math.log(n, 2), lambda n: n * math.log(n, 2), lambda n: n * math.log(n, 2)),
    "Selection Sort": (lambda n: n**2, lambda n: n, lambda n: n**2),
}

if __name__ == "__main__":
    root = tk.Tk()
    app = AlgorithmTesterGUI(root)
    root.mainloop()