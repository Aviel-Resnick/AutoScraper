from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import csv
from AutoScraper import CarInfoProcessor


class CarLookupGUI:
    def __init__(self, master):
        self.master = master
        master.title("AutoScraper")

        # Initialize variables
        self.filepath = StringVar()
        self.filepath.set("No file selected.")
        self.file_contents = StringVar()
        self.results_contents = StringVar()

        # Create widgets
        self.select_file_label = Label(master, text="Select a file:")
        self.select_file_label.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.select_file_button = Button(master, text="Select File", command=self.select_file)
        self.select_file_button.grid(row=0, column=2, padx=10, pady=10, sticky=E)

        self.filepath_label = Label(master, textvariable=self.filepath, wraplength=350)
        self.filepath_label.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        self.file_contents_label = Label(master, text="File contents:")
        self.file_contents_label.grid(row=2, column=0, padx=10, pady=10, sticky=W)

        self.file_contents_text = Text(master, height=25, width=75)
        self.file_contents_text.grid(row=3, column=0, padx=10, pady=10, sticky=NSEW)
        self.file_contents_text.grid_rowconfigure(0, weight=1)
        self.file_contents_text.grid_columnconfigure(0, weight=1)

        self.results_label = Label(master, text="Results:")
        self.results_label.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        self.results_text = Text(master, height=25, width=75)
        self.results_text.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky=NSEW)
        self.results_text.grid_rowconfigure(0, weight=1)
        self.results_text.grid_columnconfigure(0, weight=1)

        self.progress_label = Label(master, text="Progress:")
        self.progress_label.grid(row=4, column=0, padx=10, pady=10, sticky=W)

        self.progress_bar = ttk.Progressbar(master, orient=HORIZONTAL, length=500, mode='determinate')
        self.progress_bar.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky=NSEW)
        self.progress_bar.grid_rowconfigure(0, weight=1)
        self.progress_bar.grid_columnconfigure(0, weight=1)

        self.lookup_button = Button(master, text="Parse Input and Lookup Values", command=self.lookup_directory)
        self.lookup_button.grid(row=6, column=0, padx=10, pady=10, sticky=NSEW)

        self.export_text_button = Button(master, text="Export to Text", width=15, command=self.export_text)
        self.export_text_button.grid(row=6, column=1, padx=10, pady=10, sticky=NSEW)

        self.export_excel_button = Button(master, text="Export to Excel", width=15, command=self.export_excel)
        self.export_excel_button.grid(row=6, column=2, padx=10, pady=10, sticky=NSEW)

        # Configure grid weights and resize behavior
        for i in range(7):
            master.grid_rowconfigure(i, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)


    def select_file(self):
        filetypes = (("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*"))
        filepath = filedialog.askopenfilename(title="Select a text file", filetypes=filetypes)
        if filepath:
            self.filepath.set(filepath)
            with open(filepath, "r") as f:
                file_contents = f.read()
            self.file_contents_text.delete("1.0", END)
            self.file_contents_text.insert(END, file_contents)

    def lookup_directory(self):
        filepath = self.filepath.get()
        if filepath:
            car_processor = CarInfoProcessor(filepath)
            # car_amount = car_processor.get_car_amount()
            car_amount = 5

            self.progress_bar['maximum'] = car_amount
            self.progress_bar['value'] = 0

            for i in range(car_amount):
                results = car_processor.process_car_info(i)
                self.results_text.insert(END, results)
                self.results_text.update()
                self.progress_bar['value'] = i + 1
                self.progress_bar.update()

    def export_text(self):
        results = self.results_text.get("1.0", END)
        if results:
            filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
            filepath = filedialog.asksaveasfilename(title="Save file", filetypes=filetypes)
            if filepath:
                with open(filepath, "w") as f:
                    f.write(results)
                self.results_text.delete("1.0", END)
                self.results_text.insert(END, "Results exported to:\n" + filepath)
    
    def export_excel(self):
        results = self.results_text.get("1.0", END)
        if results:
            filetypes = (("CSV files", "*.csv"), ("All files", "*.*"))
            filepath = filedialog.asksaveasfilename(title="Save file", filetypes=filetypes)
            if filepath:
                # with open(filepath, "w") as f:
                f = open(filepath, 'a', newline='')
                excel_writer = csv.writer(f)

                # entries = []
                for entry in results.split('\n\n'):
                    print(entry.split('\n'))
                    values = [x.split(': ')[1] for x in entry.split('\n') if ':' in x]
                    # entries.append(values)
                    excel_writer.writerow(values)

                self.results_text.delete("1.0", END)
                self.results_text.insert(END, "Results exported to:\n" + filepath)

root = Tk()
gui = CarLookupGUI(root)
root.mainloop()
