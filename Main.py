import streamlit as st

from streamlit_option_menu import option_menu
import Home_Page, Return_analysis, Importance, Calculate_returns

st.set_page_config(
    page_title="CAPM Web Application", layout="wide"
)

# adding background image 

# st.markdown(
#     """
#     <style>
#         body {
#             background-image: url('capm.jpg');
#             background-size: cover;
#             background-repeat: no-repeat;
#             background-position: center;
#         }

#         .stApp {
#             background-color: rgba(255, 255, 255, 0); /* Set the background color to transparent */
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )


st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        .st-emotion-cache-1wbqy5l.e17vllj40 {visibility : hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
css = """
    <style>
        body {
            background-color: #EA7056;
            font-family: 'Arial', sans-serif;
            background-image: url('stocks2.jfif');
            background-size: cover;
            margin-top : 0px ;
        }
        .stApp {
            max-width: 1500px;
            margin: 0 auto;
            margin-top : 0px;
        }
        .st-h1 {
            color: #333333;
            text-align: center;
        }
        .btn-primary {
                color: #fff;
                background-color: #007bff;
                border-color: #007bff;
        }
    </style>
"""
st.markdown(css, unsafe_allow_html=True)
marquee_html = """
    <style>
        .marquee {
            width: 100%;
            white-space: nowrap;
            overflow: hidden;
            box-sizing: border-box;
            animation: marquee 7s ease-in-out 1s infinite alternate forwards;
        }

        @keyframes marquee {
            0%   { transform: translate(100%, 0); }
            25%  { transform: translate(50%, 0); }
            50%  { transform: translate(0, 0); }
            75%  { transform: translate(-50%, 0); }
            100% { transform: translate(-100%, 0); }
            /* Add easing for a smoother animation */
            animation-timing-function: cubic-bezier(0.1, 0.7, 1.0, 0.1);

        }
    </style>
    <div class="marquee">
        <h2>A Stock Analysis Project By Kanika & Himanshu </h2>
    </div>
"""

st.markdown(marquee_html , unsafe_allow_html = True)


class MultiApp:
    def __init__(self):
        self.apps=[]

    def add_app(self,title,function):
        self.apps.append({
            "title":title,
            "function":function
        })
    

    def run(self):
        app = option_menu(
            menu_title="",
            options=["About","Importance","Return_Analysis","Calculate_Return"],
            icons=["house-fill","book-fill","stack-overflow","building-up"],
            default_index=0,
            orientation="horizontal"
            )

        if app=="About":
            Home_Page.app()
            
        if app=="Importance":
            Importance.app()
        if app=="Return_Analysis":
            Return_analysis.app()
        if app=="Calculate_Return":
            Calculate_returns.app()

    
if __name__ == '__main__':
    app = MultiApp()
    def main_page():
        st.title("CAPM Web Application - Home Page")
        st.write("Welcome to the Home Page!")

        # Add a button to navigate to the new page
        if st.button("Go to New Page"):
            # Use st.experimental_set_query_params to modify the URL
            st.experimental_set_query_params(nav="Home_Page.py")

    # Add the main page as the first app
    app.add_app("Home", main_page)
    app.run()

