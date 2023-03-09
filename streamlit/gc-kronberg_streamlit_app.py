import streamlit as st
import pandas as pd
import plotly.express as px
import os

path = os.path.dirname(os.path.dirname(__file__))
raw_data = pd.read_csv(f"{path}/data/gc_kronberg_cleaned.csv", sep=",")

st.set_page_config(layout="wide")

st.title("Golfclub Auslastung")

# st.subheader("Raw data")
# st.write(raw_data)

st.subheader("Datenanalyse")

col1, col2, col3 = st.columns(3)

tag = col1.selectbox("Tag", ["Alle", "Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"])

monat = col2.selectbox("Monat", ["Alle", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt"])

jahr = col3.selectbox("Jahr", ["Alle", 2021, 2022])

startzeit_stunde = col1.slider("Startzeit Stunde", 0, 23, value=6, step=1)
startzeit_minute = col2.slider("Startzeit Minute", 0, 50, value=0, step=10)

startzeit = "{:02d}:{:02d}".format(startzeit_stunde, startzeit_minute)

endzeit_stunde = col1.slider("Endzeit Stunde", 0, 23, value=23, step=1)
endzeit_minute = col2.slider("Endzeit Minute", 0, 50, value=0, step=10)

endzeit = "{:02d}:{:02d}".format(endzeit_stunde, endzeit_minute)

data_to_show = col3.selectbox("Data to show", ['Auslastung Gesamt',
                                               'Auslastung Gäste', 'Auslastung MGL Gesa.', 'Auslastung MGL Jugend',
                                               'Auslastung MGL 18-40', 'Auslastung MGL 40-50', 'Auslastung MGL 50-65',
                                               'Auslastung MGL 65+'])

if jahr != "Alle":
    plot_data = raw_data[raw_data["Jahr"] == jahr]
    if monat != "Alle":
        plot_data = plot_data[plot_data["monat_text"] == monat]
        if tag != "Alle":
            plot_data = plot_data[plot_data["Wochentag"] == tag]
    elif tag != "Alle":
        plot_data = plot_data[plot_data["Wochentag"] == tag]
elif monat != "Alle":
    plot_data = raw_data[raw_data["monat_text"] == monat]
    if tag != "Alle":
        plot_data = plot_data[plot_data["Wochentag"] == tag]
elif tag != "Alle":
    plot_data = raw_data[raw_data["Wochentag"] == tag]
else:
    plot_data = raw_data.copy()


plot_data = plot_data[(plot_data["time"] >= startzeit) & (plot_data["time"] <= endzeit)]

plot_data_grouped = plot_data.groupby(["time"])[data_to_show].mean().reset_index()

st.write(f"""
### Die durchschnittliche Auslastung für die gewählten Parameter beträgt:
{(plot_data_grouped[data_to_show].mean()*100).round(2)}%

## Graph
""")

fig = px.line(plot_data_grouped, x="time", y=data_to_show,
              title=f"{data_to_show} für {tag} in {monat} in {jahr} von {startzeit} Uhr bis {endzeit} Uhr",
              hover_data=["time"],
              labels={"time": "Uhrzeit", data_to_show: "Auslastung in %"})
fig.update_layout(xaxis_rangeslider_visible=True)
fig.update_yaxes(tickformat=".0%")
# plot min and max point for data_to_show in the plot
st.plotly_chart(fig, use_container_width=True)