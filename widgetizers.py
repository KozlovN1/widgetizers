#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 17:44:36 2024

@author: Nick Kozlov

Version 0.5 - 2026-06-13
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
    
    # TODO: don't know how to convert to independent handles for each CheckButtons
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
def function_name():
    from matplotlib.widgets import SpanSelector
    
    return



''' ---------------------------------------------------------------- '''
if __name__ == "__main__":
    # the code in this section is not executed upon importing the module
    print("widgetizers for matplotlib.widgets")
