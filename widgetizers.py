#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
https://github.com/KozlovN1/widgetizers
A function library that simplifies the implementation of matplotlib.widgets in your code.

@author: Nick Kozlov

Version 0.5 - 2026-06-14

- add_axis_selector takes on the input a function of the type func(ax, base, signal)
"""

# 1. CheckButtons
# TODO: are we going to use it?
def make_checkable(fig, axs=None, coords=None):
    from matplotlib.widgets import CheckButtons
    
    def callback(label):
        ln = lines_by_label[label]
        ln.set_visible(not ln.get_visible())
        ln.figure.canvas.draw_idle()
    
    if axs is None: axs = fig.axes
    print(axs) # !!! DEBUG
    dct = {}
    for ax in axs:
        dct[ax] = [[line] for line in ax.lines]
    print(dct) # !!! DEBUG
    if coords is None: coords = (0.8, 0.85, 0.2, 0.15) # ax
    
    check = {}
    for ax in axs:
        lst = dct[ax]
        print(lst) # !!! DEBUG
        lines_by_label = {l[0].get_label(): l[0] for l in lst}
        line_colors = [l.get_color() for l in lines_by_label.values()]
    
        # Make checkbuttons with all plotted lines with correct visibility
        rax = ax.inset_axes(coords)
        check[ax] = CheckButtons(
            ax=rax,
            labels=lines_by_label.keys(),
            actives=[l.get_visible() for l in lines_by_label.values()],
            label_props={'color': line_colors},
            frame_props={'edgecolor': line_colors},
            check_props={'facecolor': line_colors},
            )
    
        check[ax].on_clicked(callback)
    
    # TODO: convert to independent handles for each CheckButtons
    return [v for v in check.values()]

def make_axis_checkable(ax, lst=None, coords=None):
    from matplotlib.widgets import CheckButtons
    
    # fig = ax.figure
    if lst is None: lst = [[line] for line in ax.lines]
    # print(lst) # !!! DEBUG
    if coords is None: coords = (0.8, 0.85, 0.2, 0.15) # ax
    
    lines_by_label = {l[0].get_label(): l[0] for l in lst}
    line_colors = [l.get_color() for l in lines_by_label.values()]

    # Make checkbuttons with all plotted lines with correct visibility
    rax = ax.inset_axes(coords)
    check = CheckButtons(
        ax=rax,
        labels=lines_by_label.keys(),
        actives=[l.get_visible() for l in lines_by_label.values()],
        label_props={'color': line_colors},
        frame_props={'edgecolor': line_colors},
        check_props={'facecolor': line_colors},
        )

    def callback(label):
        ln = lines_by_label[label]
        ln.set_visible(not ln.get_visible())
        ln.figure.canvas.draw_idle()

    check.on_clicked(callback)
    
    return check

def make_figure_checkable(fig, axs=None, lst=None, coords=None):
    from matplotlib.widgets import CheckButtons
    
    def callback(label):
        ln = lines_by_label[label]
        ln.set_visible(not ln.get_visible())
        ln.figure.canvas.draw_idle()
    
    if axs is None: axs = fig.axes
    print(axs) # !!! DEBUG
    if lst is None:
        lst = []
        for ax in axs:
            lst.extend([[line] for line in ax.lines])
    print(lst) # !!! DEBUG
    if coords is None: coords = (0.8, 0.85, 0.2, 0.15) # fig
    
    print(lst) # !!! DEBUG
    lines_by_label = {l[0].get_label(): l[0] for l in lst}
    line_colors = [l.get_color() for l in lines_by_label.values()]

    # Make checkbuttons with all plotted lines with correct visibility
    rax = fig.add_axes(coords)
    check = CheckButtons(
        ax=rax,
        labels=lines_by_label.keys(),
        actives=[l.get_visible() for l in lines_by_label.values()],
        label_props={'color': line_colors},
        frame_props={'edgecolor': line_colors},
        check_props={'facecolor': line_colors},
        )

    check.on_clicked(callback)
    
    return check

# 2. picker
def make_axis_pickable(ax, lst=None, radius=1):
    fig = ax.figure
    
    if lst is None:
        lst = []
        for line in ax.lines:
            lst.append(line)
    
    for ln in lst:
        ln.set_picker(True)
        ln.set_pickradius(radius)
    
    # Adapted from https://matplotlib.org/stable/users/explain/figure/event_handling.html -->
    def onpick(event):
        thisline = event.artist
        xdata = thisline.get_xdata()
        ydata = thisline.get_ydata()
        ind = event.ind
        points = tuple(zip(xdata[ind], ydata[ind]))
        print('onpick points:', points)

    fig.canvas.mpl_connect('pick_event', onpick)
    #<--

# 3. SpanSelector
# TODO: add_figure_selector is under construction
def add_figure_selector(fig, base, func):
    from matplotlib.widgets import SpanSelector
    import numpy as np
    
    ax = fig.axes
    n_fig = len(ax)
    x = base
    
    def onselect(xmin, xmax):
        print("xmin, xmax = ", xmin, xmax)
        indmin, indmax = np.searchsorted(x, (xmin, xmax))
        indmax = min(len(x) - 1, indmax)
        
        # signal_1 = signal[indmin:indmax]
        absc = x[indmin:indmax]
        
        if len(absc) >= 2:
            print(f">>>>> Interval: [{indmin} : {indmax}]")
            print(f">>>>> Interval [s]: [{absc[0]} : {absc[-1]}]")
            print()
            i = 0
            for quant in list(quantity):
                signal_s = data[quant][indmin:indmax]
                print(f">>>>> Average {quant} [{quantity[quant][0]}]: {np.mean(signal_s)} +- {np.std(signal_s)}")
                print()
                ax[i].set_title(f"Aver: {np.mean(signal_s): .2e} $\pm$ {np.std(signal_s): .2e}")
                i += 1

    span = ['' for _ in range(n_fig)]
    for i in range(n_fig):
        try:
            # new matplotlib
            span[i] = SpanSelector(
                ax[i],
                onselect,
                "horizontal",
                useblit=True,
                props=dict(alpha=0.5, facecolor="tab:blue"),
                interactive=True,
                drag_from_anywhere=True
            )
        except:
            # old matplotlib
            span[i] = SpanSelector(
                ax[i],
                onselect,
                "horizontal",
                useblit=True
            )
    
    return span

def add_axis_selector(ax, base, signal, func):
    from matplotlib.widgets import SpanSelector
    import numpy as np
    
    x = base
    
    def onselect(xmin, xmax):
        print("xmin, xmax = ", xmin, xmax)
        indmin, indmax = np.searchsorted(x, (xmin, xmax))
        indmax = min(len(x) - 1, indmax)
        
        base1 = x[indmin:indmax]
        signal1 = signal[indmin:indmax]
        
        if len(base1) >= 2:
            print(f">>>>> Interval indices: [{indmin} : {indmax}]")
            print(f">>>>> Interval values: [{base1[0]} : {base1[-1]}]")
            print()
            func(ax, base1, signal1)

    try:
        # new matplotlib
        span = SpanSelector(
            ax,
            onselect,
            "horizontal",
            useblit=True,
            props=dict(alpha=0.5, facecolor="tab:blue"),
            interactive=True,
            drag_from_anywhere=True
        )
    except:
        # old matplotlib
        span = SpanSelector(
            ax,
            onselect,
            "horizontal",
            useblit=True
        )
    
    # TODO: is it possible to exctract the result of onselect from SpanSelector?
    
    return span



''' ---------------------------------------------------------------- '''
if __name__ == "__main__":
    # the code in this section is not executed upon importing the module
    print("widgetizers for matplotlib.widgets")
