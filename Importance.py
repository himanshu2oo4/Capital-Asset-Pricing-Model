import streamlit as st
from PIL import Image

def app():
    with st.container():
        st.header("Why CAPM is Important? 🤔")
        st.write("The CAPM formula is widely used in the finance industry. It is vital in calculating the [weighted average cost of capital](https://corporatefinanceinstitute.com/resources/valuation/what-is-wacc-formula/) (WACC), as CAPM computes the cost of equity. WACC is used extensively in [financial modeling](https://corporatefinanceinstitute.com/resources/financial-modeling/what-is-financial-modeling/).  It can be used to find the net present value (NPV) of the future cash flows of an investment and to further calculate its [enterprise value](https://corporatefinanceinstitute.com/resources/valuation/what-is-enterprise-value-ev/) and finally its equity value.")
    
    with st.container():
        st.write("----")
        st.header("CAPM Example – Calculation of Expected Return")
        st.write("Let’s calculate the expected return on a stock, using the Capital Asset Pricing Model (CAPM) formula. Suppose the following information about a stock is known:")
        st.markdown("- It trades on the NYSE and its operations are based in the United States")
        st.markdown("- Current yield on a U.S. 10-year treasury is 2.5%")
        st.markdown("- The average excess historical annual return for U.S. stocks is 7.5%")
        st.markdown("- The beta of the stock is 1.25 (meaning its average return is 1.25x as volatile as the S&P500 over the last 2 years)")
    
    with st.container():
        st.write("----")
        st.header("Video Explanation")
        img_col, text_col = st.columns((1,2))
        with img_col:
            image = Image.open("cover.jpg")
            st.image(image)
        with text_col:
            st.write("To learn more about the Capital Asset Pricing Model (CAPM), check out the video :")
            st.markdown("[Watch Video....](https://www.youtube.com/watch?v=IJeYwx-cXyc&t=3s)")

        
