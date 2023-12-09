import streamlit as st
import json
from streamlit_lottie import st_lottie
import requests
from PIL import Image

def app():

    #Header section
    st.title("Capital Asset Pricing Model (CAPM) 📈")
    st.subheader("A method for calculating the required rate of return, discount rate or cost of capital")
    st.write("The Capital Asset Pricing Model (CAPM) is a model that describes the relationship between the expected return and risk of investing in a security.It shows that the expected return on a security is equal to the risk-free return plus a risk premium, which is based on the beta of that security.")

    st.write("[Learn More >](https://en.wikipedia.org/wiki/Capital_asset_pricing_model)")

    st.write("Below is an illustration of the CAPM concept.")
    image = Image.open("capm.jpg")
    st.image(image)

    with st.container():
        st.write("-----")
        st.header("CAPM Formula and Calculation")
        st.write("CAPM is calculated according to the following formula:")
        st.write("R = Rf + [B*(Rm - Rf)]")
        st.markdown('Where: ')
        st.markdown('- **R** : Return on investment')
        st.markdown('- **Rf** : The risk-free rate of interest')
        st.markdown('- **B** : Beta coefficient representing market risk')
        st.markdown('- **Rm** : Market portfolio return')
        st.write()
        st.subheader("Note: “Risk Premium” = (Rm – Rrf)")
        st.write("The CAPM formula is used for calculating the expected returns of an asset. It is based on the idea of systematic risk (otherwise known as non-diversifiable risk) that investors need to be compensated for in the form of a risk premium. A risk premium is a rate of return greater than the risk-free rate. When investing, investors desire a higher risk premium when taking on more risky investments.")