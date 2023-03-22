import pylab
from statsmodels.graphics import tsaplots
from matplotlib.widgets import RadioButtons, Slider
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


def read_from_file(input_path: str) -> []:
    with open(input_path, "r") as file:
        header = file.readline()
        data = [float(i) for i in file.readlines()]

    return data


if __name__ == '__main__':
    def select_file():
        global window
        global data
        global select_path_label
        global slider_lags
        path = filedialog.askopenfile(title="Select a File", filetype=(('all files', '*.*'), ('text files''*.txt')))

        if path is not None:
            data = read_from_file(path.name)
            select_path_label.config(text=path.name)
            on_radio_button_clicked('Original plot')
            slider_lags.valinit = len(data) / 4
            slider_lags.valmax = len(data) - 1
            slider_lags.reset()


    def on_radio_button_clicked(label):
        global axes
        global data
        global slider_lags

        axes.clear()

        if label == 'Original plot':
            axes.plot(data)
        else:
            tsaplots.plot_acf(data, axes, lags=slider_lags.val)
        pylab.draw()

    def on_slider_change(lags):
        global radiobutton
        on_radio_button_clicked(radiobutton.value_selected)

    data = read_from_file("data.rr")
    window = tk.Tk()
    fig, axes = pylab.subplots()
    fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.2)

    axes_radiobutton = pylab.axes([0.05, 0.03, 0.3, 0.1])
    radiobutton = RadioButtons(axes_radiobutton, ('Original plot', 'Auto-correlation'),
                               label_props={'color': ['blue', 'red']}, radio_props={'color':['blue', 'red']})
    radiobutton.on_clicked(on_radio_button_clicked)
    on_radio_button_clicked(radiobutton.value_selected)

    axes_slider_lags = pylab.axes([0.45, 0.04, 0.45, 0.05])
    slider_lags = Slider(axes_slider_lags, label='lags', valmin=1, valmax=len(data) - 1, valinit=(len(data) - 1) / 4,
                         valfmt='%d')
    slider_lags.on_changed(on_slider_change)

    select_path_button = tk.Button(master=window, width=10, height=2, text="Select Path", command=select_file)
    select_path_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    select_path_label = tk.Label(master=window, text="Click the Button to Select a File", font='Aerial 18 bold')
    select_path_label.pack(side=tk.BOTTOM, padx=10, pady=10)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    window.mainloop()
