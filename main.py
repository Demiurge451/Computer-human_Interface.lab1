import pylab
from statsmodels.graphics import tsaplots
from matplotlib.widgets import RadioButtons, Slider


def read_from_file(input_path: str) -> []:
    with open(input_path, "r") as file:
        header = file.readline()
        data = [int(i) for i in file.readlines()]

    return data


if __name__ == '__main__':
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
    fig, axes = pylab.subplots()
    fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.2)

    axes_radiobutton = pylab.axes([0.05, 0.03, 0.3, 0.1])
    radiobutton = RadioButtons(axes_radiobutton, ["Original plot", "Auto-correlation"], 0)
    radiobutton.on_clicked(on_radio_button_clicked)

    axes_slider_lags = pylab.axes([0.45, 0.04, 0.45, 0.05])
    slider_lags = Slider(axes_slider_lags, label='lags', valmin=1, valmax=len(data) - 1, valinit=(len(data) - 1) / 2,
                         valfmt='%d')
    slider_lags.on_changed(on_slider_change)

    on_radio_button_clicked(radiobutton.value_selected)
    pylab.show()







