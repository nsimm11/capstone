import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd
import numpy as np

#inputs
g = 9.81 #m/ss

#PIPING COMPONENTS
konductivity = 16.2 #conductivity of ss
konduct_air = 0.025 #conductivity of air

roughness = 0.015

#inlet
thick_inlet = 0.0095

#header
thick_header = 0.01905 #m

#distribution tubes
thick_tube = 0.0127 #thickness of 3" npt pipe

#condensate drainage line
thick_cond = 0.00762 #thickness of 3/4" npt pipe

#Ambient conditions
pamb = 1 #bar
tamb = 20 #C

#Supplied Steam
psam = 1 #bar

c1, c2, c3 = st.columns(3)
c2.markdown("# Capstone Model")
c2.image("sam.jpg")

opts_headerDia = [3,6,9,12]
opt_distTubeSpacing = [3,6,9,12]
opts_inletDia = [1, 1.5, 2, 3]
opts_tubeDia = [1.5]
opts_condDia = [0.5, 0.75, 1, 1.5, 2, 3]
opts_inletLen = [2, 5, 12]

nozzleSpacingDict = {"A": 3, "B": 2, "C": 1}

st.markdown("### Piping Component Variables")
c1, c2, c3, c4, c5, c6 = st.columns(6)

dia_inlet = float(c1.selectbox(label="Inlet Diameter [in]", options=opts_inletDia)) * 0.0254
len_inlet = float(c1.selectbox(label="Inlet Length [in]", options=opts_inletLen))

insulated = bool(c2.selectbox(label="Insulated?", options=[False, True]))
thick_insul = float(c2.text_input(label="Insulation Thickness [in]", value=0.25)) * 0.0254

dia_header = float(c3.selectbox(label="Header Diameter [in]", options=opts_headerDia)) * 0.0254
len_header = float(c3.text_input(label="Header Length [in] (to dist tube)", value=12)) * 0.0254

dia_tube = float(c4.selectbox(label="Distribution Tube Diameter [in]", options=opts_tubeDia)) * 0.0254
len_tube = float(c4.text_input(label="Distribution Tube Length [in]", value=10)) * 0.0254

dia_nozzle = float(c5.selectbox(label="Nozzle Diameter [in]", options=[str(1/16)])) * 0.0254
nozzlesSpacingLetter = (c5.selectbox(label="Nozzles Spacing Type", options=["A", "B", "C"]))

nozzlesSpacing = nozzleSpacingDict[nozzlesSpacingLetter]

dia_cond = float(c6.selectbox(label="Condensate Drainage Line Diameter [in]", options=opts_condDia)) * 0.0254

st.markdown("### Inlet Steam Conditions")

c1, c2, c3, c4 = st.columns(4)
dryfract_in = float(c1.text_input(label="Dryness Ratio of Inlet Steam", value=0.65))
tsteam = float(c2.text_input(label="Inlet Steam Temperature [C]", value=100))
p_in = float(c3.text_input(label="Inlet Pressure [atm]", value=1))
v_in = float(c4.text_input(label="Inlet Flow Rate [m3/hr]", value=14)) / ((dia_inlet/2)**2 * np.pi * 3600)
z_in = 0

st.markdown("### Assumptions")
st.write("""
- Pressure across the SAM-e is atmostpheric, this includes both the nozzles and condensate drainage \n
- The SAM-e is made out of 304SS, with a conductivity constant k of 16.2 W/mk, Radiation and Convection were not considered \n
- Minor Line Losses were not considered \n
- The averge height of the nozzles is half the height of the distribution tube, as the nozzles are evenly distributed across them \n
- The height of the inlet and condensate lines are at 0m \n
- The nozzle design completely removes all entrained liquid in the vapour stream so only vapor exits through the nozzles, and only liquid exits through the condensate drainage line
- Does not consider superheated vapor or supercooled liquid
""")

A_in = (dia_header/2)**2 * np.pi

A_nozzle = num_nozzles*(dia_nozzle/2)**2 * np.pi
p_nozzle = pamb
z_nozzle = 0

A_cond = (dia_cond/2)**2 * np.pi
z_cond = 0

button = st.button("Calculate")

if button:
  st.markdown("CALCULATE")


