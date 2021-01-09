#!/usr/bin/python3.8
# coding=utf-8

from matplotlib import pyplot as plt
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Frame, Image, Table, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

"""IZV project - Final part
    Author: Natália Holková
    Login: xholko02
"""


def create_graph(c, df):
    # Get new DataFrame with only columns I need
    df_new = df[["p1", "date", "p44", "p57"]]

    # only keep rows, where p44 (type of vehicle) is car or motorcycle (== 1/2/3/4)
    df_new = df_new[df_new["p44"].isin([1, 2, 3, 4])]
    df_new = df_new[df_new["p57"].isin([1, 6, 8])]

    stacked = df_new.pivot_table(index=["p44"], columns='p57', aggfunc='size', fill_value=0).stack()

    total_cars = stacked[3, 1] + stacked[3, 6] + stacked[3, 8] + stacked[4, 1] + stacked[4, 6] + stacked[4, 8]
    total_bikes = stacked[1, 1] + stacked[1, 6] + stacked[1, 8] + stacked[2, 1] + stacked[2, 6] + stacked[2, 8]

    # status, cars, bikes
    data = [["Good", (stacked[3, 1] + stacked[4, 1]) / total_cars * 100, (stacked[1, 1] + stacked[2, 1]) / total_bikes * 100],
            ["Injured", (stacked[3, 6] + stacked[4, 6]) / total_cars * 100, (stacked[1, 6] + stacked[2, 6]) / total_bikes * 100],
            ["Dead", (stacked[3, 8] + stacked[4, 8]) / total_cars * 100, (stacked[1, 8] + stacked[2, 8]) / total_bikes * 100],
            ]

    plt.style.use("bmh")
    df2 = pd.DataFrame(data, columns=["status", "cars", "bikes"])
    ax = df2.plot(x="status", y=["cars", "bikes"], kind="bar", figsize=(9, 9))
    ax.set_yscale('log')  # logarithmic scale
    plt.xlabel("Driver status after accident", fontsize=16)
    plt.ylabel("% from total accidents", fontsize=16)
    ax.legend(["car", "motorcycle"])
    plt.suptitle("Graph of vehicle type influence on driver status", fontsize=20, fontweight='bold')

    plt.savefig("fig.png")  # Store the figure

    Image('fig.png', width=9 * cm, height=9 * cm).drawOn(c, 1 * cm, 8.7 * cm)


def create_table(c, df):
    # Get new DataFrame with only columns I need
    df_new = df[["p1", "date", "p44", "p57"]]

    # only keep rows, where p44 (type of vehicle) is car or motorcycle (== 1/2/3/4)
    df_new = df_new[df_new["p44"].isin([1, 2, 3, 4])]
    df_new = df_new[df_new["p57"].isin([1, 6, 8])]

    stacked = df_new.pivot_table(index=["p44"], columns='p57', aggfunc='size', fill_value=0).stack()

    data = [[None, 'Good', 'Injured', 'Dead'],
            ['Cars', stacked[3, 1] + stacked[4, 1], stacked[3, 6] + stacked[4, 6], stacked[3, 8] + stacked[4, 8]],
            ['Motorcycles', stacked[1, 1] + stacked[2, 1], stacked[1, 6] + stacked[2, 6], stacked[1, 8] + stacked[2, 8]],
            ['Total', stacked[3, 1] + stacked[4, 1] + stacked[1, 1] + stacked[2, 1],
             stacked[3, 6] + stacked[4, 6] + stacked[1, 6] + stacked[2, 6],
             stacked[3, 8] + stacked[4, 8] + stacked[1, 8] + stacked[2, 8]]]

    # print table to output -- todo: this format?
    print(f"{' ' * 12}|{data[0][1]:10}|{data[0][2]:10}|{data[0][1]:10}")
    print(("-" * 12) + "+" + ("-" * 10) + "+" + ("-" * 10) + "+" + ("-" * 10))
    print(f"{data[1][0]:12}|{data[1][1]:10}|{data[1][2]:10}|{data[1][1]:10}")
    print(f"{data[2][0]:12}|{data[2][1]:10}|{data[2][2]:10}|{data[2][1]:10}")
    print(f"{data[3][0]:12}|{data[3][1]:10}|{data[3][2]:10}|{data[3][1]:10}")

    t = Table(data, style=[('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), ('FONTSIZE', (0, 0), (-1, -1), 12),
                           ('LEADING', (0, 0), (-1, -1), 12), ('GRID', (0, 1), (-1, -1), 0.5, '#808080'),
                           ('GRID', (1, 0), (-1, 0), 0.5, '#808080'), ('BACKGROUND', (0, 1), (0, -1), '#dcf1fa'),
                           ('BACKGROUND', (1, 0), (-1, 0), '#dcf1fa'),
                           ('VALIGN', (0, 1), (0, -1), 'MIDDLE')])
    t.hAlign = 'LEFT'

    t.wrapOn(c, 9 * cm, 5 * cm)
    t.drawOn(c, 11 * cm, 12.7 * cm)


def create_report(df):
    # prepare styles
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_normal.fontName = 'Helvetica'
    style_normal.fontSize = 14
    style_normal.textColor = (.4, .4, .4)
    style_normal.leading = 1.2 * style_normal.fontSize
    style_heading = styles['Heading1']
    style_heading.fontName = 'Helvetica'
    style_heading.fontSize = 16
    style_heading.spaceAfter = 20

    # create canvas
    c = canvas.Canvas("doc.pdf", pagesize=A4)

    c.setFillColor('white')
    c.saveState()

    # Heading rectangle
    c.setFillColor('blue')
    c.rect(1 * cm, 24.7 * cm, 19 * cm, 3 * cm, stroke=0, fill=1)

    # Heading text
    c.restoreState()
    c.setFillColor('white')
    c.setFont('Helvetica', 25)
    c.drawString(2 * cm, 25.7 * cm, 'Influence of vehicle type on driver status')

    # Text
    story = []
    story.append(Paragraph("Random", style_heading))
    story.append(Paragraph("Something something...<u>Something</u>\n...", style_normal))

    f = Frame(1 * cm, 18.7 * cm, 19 * cm, 5 * cm, showBoundary=1)
    f.addFromList(story, c)

    # Graph
    create_graph(c, df)

    # Table
    create_table(c, df)

    c.showPage()
    c.save()


if __name__ == "__main__":
    if os.path.isfile("accidents.pkl.gz"):  # data file exists
        df = pd.read_pickle("accidents.pkl.gz")
    else:  # data file does not exist
        raise FileNotFoundError("File accidents.pkl.gz containing data not found.")

    # create date column in DataFrame
    df["date"] = pd.to_datetime(df["p2a"], format="%Y-%m-%d", errors="coerce")
    create_report(df)

