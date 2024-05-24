from unidecode import unidecode
import streamlit as st
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')
sochudao = {
    "filename": None,
    "content": None
}

sosumenh = {
    "filename": None,
    "content": None
}

solinhhon = {
    "filename": None,
    "content": None
}
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

# Hàm để đọc nội dung từ tệp văn bản
def read_file_content(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def so_chu_dao(ngay_thang_nam_sinh):
    """Hàm tính số chủ đạo từ ngày tháng năm sinh."""
    # Tách ngày, tháng và năm từ chuỗi ngày tháng năm sinh
    day, month, year = map(int, ngay_thang_nam_sinh.split('/'))

    # Hàm tính tổng các chữ số của một số
    def tong_chu_so(number):
        total = 0
        while number > 0:
            total += number % 10
            number //= 10
        return total

    # Tính tổng các chữ số của ngày, tháng, năm sinh
    tong_chu_so_ngay = tong_chu_so(day)
    tong_chu_so_thang = tong_chu_so(month)
    tong_chu_so_nam = tong_chu_so(year)

    # Tính tổng tổng các chữ số
    tong = tong_chu_so_ngay + tong_chu_so_thang + tong_chu_so_nam

    # Tính số chủ đạo từ tổng
    while tong > 10:
        if tong == 11 or tong == 22 or tong == 33:
            return tong
        tong = tong_chu_so(tong)

    return tong


def tinh_chi_so_linh_hon(ten):
    chi_so = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
        'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
    }
    nguyen_am = ["A", 'O', 'E', 'I', 'U']

    def tinh_tong_chu_so(so):
        tong = 0
        while so > 0:
            tong += so % 10
            so //= 10
        return tong

    ten = unidecode(ten.upper())

    def check_Y(words, place):
        if words[place] != 'Y':
            return False
        else:
            if place == len(words) - 1:
                if words[place - 1] not in nguyen_am:

                    return True
                else:
                    return False
            else:
                if words[place - 1] not in nguyen_am:
                    if words[place + 1] not in nguyen_am:
                        return True
                else:
                    return False

    words = word_tokenize(ten)
    temp = []
    chi_so_linh_hon = 0
    for word in words:
        chus = list(word)

        for i in range(len(chus)):
            if check_Y(chus, i) or (chus[i] in nguyen_am):
                temp.append(chus[i])
                chi_so_linh_hon += chi_so[chus[i]]

    while chi_so_linh_hon >= 10:
        if chi_so_linh_hon == 11 or chi_so_linh_hon == 22:
            return chi_so_linh_hon
        chi_so_linh_hon = tinh_tong_chu_so(chi_so_linh_hon)

    return chi_so_linh_hon


def tinh_chi_so_su_menh(ten):
    chi_so = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
        'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
    }
    nguyen_am = ["A", 'O', 'E', 'I', 'U']

    def tinh_tong_chu_so(so):
        tong = 0
        while so > 0:
            tong += so % 10
            so //= 10
        return tong

    ten = unidecode(ten.upper())
    words = word_tokenize(ten)
    temp = []
    chi_so_su_menh = 0
    for word in words:
        hold = 0
        chus = list(word)
        for chu in chus:
            hold += chi_so[chu]
        while hold >= 10:
            hold = tinh_tong_chu_so(hold)
        chi_so_su_menh += hold
    while chi_so_su_menh >= 10:
        if chi_so_su_menh == 11 or chi_so_su_menh == 22:
            return chi_so_su_menh
        chi_so_su_menh = tinh_tong_chu_so(chi_so_su_menh)

    return chi_so_su_menh


def format_date(day, month, year):
    formatted_day = str(day).zfill(2)
    formatted_month = str(month).zfill(2)
    formatted_year = str(year)
    return f"{formatted_day}/{formatted_month}/{formatted_year}"


def main():
    hide_streamlit_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                    </style>
                    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    set_background_image()
    st.title("Ứng dụng Tính Thần Số Học")

    # Hàng nhập ngày tháng năm
    col_ngay, col_thang, col_nam = st.columns(3)
    with col_ngay:
        ngay = st.number_input("Ngày", min_value=1, max_value=31)
    with col_thang:
        thang = st.number_input("Tháng", min_value=1, max_value=12)
    with col_nam:
        nam = st.number_input("Năm", min_value=1900, max_value=2100)

    # Ô nhập họ tên
    ten = st.text_input("Họ và tên")

    if st.button("Start"):
        if not (ngay and thang and nam and ten):
            st.error("Vui lòng nhập đầy đủ thông tin")
        else:
            so_chu_dao_result = so_chu_dao(format_date(ngay, thang, nam))
            so_linh_hon_result = tinh_chi_so_linh_hon(ten)
            so_su_menh_result = tinh_chi_so_su_menh(ten)
            sochudao["filename"] = f"Label_than_so/So_chu_dao/{so_chu_dao_result}.txt"
            sochudao["content"] = read_file_content(sochudao["filename"])

            solinhhon["filename"] = f"Label_than_so/So_linh_hon/{so_linh_hon_result}.txt"
            solinhhon["content"] = read_file_content(solinhhon["filename"])

            sosumenh["filename"] = f"Label_than_so/So_su_menh/{so_su_menh_result}.txt"
            sosumenh["content"] = read_file_content(sosumenh["filename"])

            st.write("Kết quả:")
            st.subheader("Số chủ đạo")
            st.markdown(
                f"<p style='text-align:center; font-size:80px; color:blue'><strong>{so_chu_dao_result}</strong></p>",
                unsafe_allow_html=True)
            # st.markdown(f"**Giá trị:** {so_chu_dao_result}")
            st.markdown("**Thông tin chi tiết:**")
            st.text_area(" ", sochudao["content"], height=300)


            st.subheader("Số linh hồn")
            st.markdown(
                f"<p style='text-align:center; font-size:80px; color:blue'><strong>{so_linh_hon_result}</strong></p>",
                unsafe_allow_html=True)
            st.markdown("**Thông tin chi tiết:**")
            st.text_area(" ", solinhhon["content"], height=300)


            st.subheader("Số sứ mệnh")
            st.markdown(
                f"<p style='text-align:center; font-size:80px; color:blue'><strong>{so_su_menh_result}</strong></p>",
                unsafe_allow_html=True)

            st.markdown("**Thông tin chi tiết:**")
            st.text_area(" ", sosumenh["content"], height=300)




if __name__ == "__main__":
    main()
