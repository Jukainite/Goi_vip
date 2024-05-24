import pandas as pd
import streamlit as st
from st_login_form import login_form
from supabase import create_client, Client


# Đường link đến trang Thần số học, Sinh trắc học, Nhân tướng học
thanosohoc_link = "https://directionalpathway-thansohoc-free.streamlit.app/"
sinhtrachoc_link = "https://directionalpathway-sinhtrachoc-free.streamlit.app/"
nhantuonghoc_link = "https://directionalpathway-nhantuonghoc-free.streamlit.app/"
login_link = "https://directionalpathway-dangnhap.streamlit.app/"
thanosohoc_link_vip = "https://directionalpathway-thansohoc-vip.streamlit.app/"
sinhtrachoc_link_vip = "https://directionalpathway-sinhtrachoc-vip.streamlit.app/"
nhantuonghoc_link_vip = "https://directionalpathway-nhantuonghoc-vip.streamlit.app/"

status = False


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()



def set_background_image():
    page_bg_img = f"""
    <style>
    .stApp {{
        background: url("https://img.upanh.tv/2024/05/24/4-wxLLDdDYg-transformed.png");
        background-size: cover
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# set_background_image()
col1, col2, col3 = st.columns([3, 1, 1])  # Chia layout thành 3 cột
name=None
with col2:
    if not status:
        if st.button("Sign In"):
            st.session_state["show_login"] = True
    else:
        st.success(f"Welcome {st.session_state['username']}")
# Nút "Sign Out" và chức năng
with col3:
    if st.button("Sign Out"):
        status = False
        st.session_state["authenticated"]=False
        name=None
        st.session_state["username"]=False
        st.write("You've been signed out!") 
# Nếu người dùng nhấn nút đăng nhập, hiển thị form đăng nhập
if "show_login" in st.session_state and st.session_state["show_login"]:
    login_form()
    if st.session_state["authenticated"]:
        if st.session_state["username"]:
            st.success(f"Welcome {st.session_state['username']}")
            status = True
            name=st.session_state['username']
        else:
            st.success("Welcome guest")
            
            status = True
            name=None

    else:
        st.error("Not authenticated")
        status = False
        name=None


# Tiêu đề của trang
st.title("Chào mừng đến với Direction-Pathway")
st.write(
    "Chúng ta hãy khám phá những khía cạnh thú vị về vận mệnh và tính cách của bạn thông qua thần số học, sinh trắc học và nhân tướng học")




# Tiêu đề "Thần số học" sẽ là một hyperlink
st.title("Chào mừng đến với Trang chủ Thần số học, Sinh trắc học vân tay và Nhân tướng học")
st.write("Chúng ta hãy khám phá những khía cạnh thú vị về vận mệnh, tính cách và vân tay của bạn!")
# Hàm để kiểm tra trạng thái đăng nhập và chuyển hướng
def create_link_or_warning(link, name):
    if status:
        st.markdown(f'<a href="{link}" target="_blank" style="text-decoration: none;"><button style="background-color: #DD83E0; border: none; border-radius: 5px; padding: 10px 20px; cursor: pointer;">{name}</button></a>', unsafe_allow_html=True)
    else:
        st.warning(f"Bạn chưa đăng nhập. Vui lòng đăng nhập để truy cập chức năng {name} này.")


# Chuyển trang tới đường link "Thần số học" khi tiêu đề được nhấp
if name is None:
    # Nút bấm cho Thần số học
    create_link_or_warning(thanosohoc_link, "Thần số học")
    st.write("Thần số học là nghệ thuật dựa trên việc phân tích các số liên quan đến ngày, tháng và năm sinh của bạn để hiểu về vận mệnh và tính cách.")
    
    # Nút bấm cho Sinh trắc học
    create_link_or_warning(sinhtrachoc_link, "Sinh trắc học")
    st.write("Sinh trắc học vân tay là nghiên cứu về các đặc điểm vân tay để xác định tính cách và tương lai của một người.")
    
    # Nút bấm cho Nhân tướng học
    create_link_or_warning(nhantuonghoc_link, "Nhân tướng học")
    st.write("Nhân tướng học là nghiên cứu về các đặc điểm gương mặt để xác định tính cách và tương lai của một người.")
else:
    # Perform query.
    # Uses st.cache_data to only rerun when the query changes or after 10 min.
    # @st.cache_data
    @st.cache_resource
    def run_query():
        return supabase.table("feature").select("*").eq("username", name).execute()

    rows = run_query()
    for row in rows.data:
        data = {
        'Cột 1': ['thansohoc', 'nhantuonghoc', 'sinhtrachoc'],
        'Cột 2': [row['thansohoc'],row['nhantuonghoc'], row['nhantuonghoc']]
    }
    # Tạo dữ liệu cho bảng
    
    
    # # Chuyển đổi dữ liệu thành DataFrame
    df = pd.DataFrame(data)
    st.table(df)

    
    
    # Nút bấm cho Thần số học
    create_link_or_warning(thanosohoc_link_vip, "Thần số học")
    st.write("Thần số học là nghệ thuật dựa trên việc phân tích các số liên quan đến ngày, tháng và năm sinh của bạn để hiểu về vận mệnh và tính cách.")
    
    # Nút bấm cho Sinh trắc học
    create_link_or_warning(thanosohoc_link_vip, "Sinh trắc học")
    st.write("Sinh trắc học vân tay là nghiên cứu về các đặc điểm vân tay để xác định tính cách và tương lai của một người.")
    
    # Nút bấm cho Nhân tướng học
    create_link_or_warning(thanosohoc_link_vip, "Nhân tướng học")
    st.write("Nhân tướng học là nghiên cứu về các đặc điểm gương mặt để xác định tính cách và tương lai của một người.")
