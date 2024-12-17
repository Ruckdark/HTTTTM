import streamlit as st
from db_connection import get_engine
from db_queries import get_trees, add_tree, update_tree, delete_tree, get_species
import pandas as pd
import plotly.express as px
from datetime import datetime
from decision_tree_model import train_decision_tree  # Nhập mô hình cây quyết định

# Kết nối đến cơ sở dữ liệu
engine = get_engine()

# Tạo menu bên trái với các nút bấm
st.sidebar.title("Menu")

if 'menu' not in st.session_state:
    st.session_state.menu = 'Danh Sách Cây Xanh'

if st.sidebar.button("Danh Sách Cây Xanh"):
    st.session_state.menu = 'Danh Sách Cây Xanh'
if st.sidebar.button("Biểu Đồ Theo Dõi"):
    st.session_state.menu = 'Biểu Đồ Theo Dõi'

menu = st.session_state.menu

# Khởi tạo biến trạng thái
if 'confirm_add_tree' not in st.session_state:
    st.session_state.confirm_add_tree = False
if 'confirm_update_tree' not in st.session_state:
    st.session_state.confirm_update_tree = False
if 'confirm_delete_tree' not in st.session_state:
    st.session_state.confirm_delete_tree = False

# Lấy dữ liệu loài cây từ bảng Species
species_data = get_species(engine)
species_options = {species['SpeciesName']: species['SpeciesId'] for species in species_data.to_dict('records')}

# Tình trạng sức khỏe dưới dạng combobox
health_status_options = ["Khỏe mạnh", "Yếu", "Bệnh", "Cần tỉa"]

if menu == "Danh Sách Cây Xanh":
    st.header("Danh Sách Cây Xanh")
    data = get_trees(engine)

    # Thêm mục tìm kiếm
    with st.expander("Tìm kiếm cây xanh", expanded=True):
        search_species = st.selectbox("Chọn loại cây", ["Tất cả"] + list(species_options.keys()))

        if search_species != "Tất cả":
            data = data[data['Species'] == search_species]
        
        st.write(f"Hiển thị {len(data)} cây")

    st.dataframe(data)
    
    # Huấn luyện mô hình cây quyết định
    clf, y_labels = train_decision_tree(data)

    with st.expander("Thêm Cây Mới"):
        species_name = st.selectbox("Loại cây", list(species_options.keys()))
        species_id = species_options[species_name]
        age = st.number_input("Tuổi cây", min_value=0, step=1)
        height = st.number_input("Chiều cao cây (m)", min_value=0.0, step=0.01)
        diameter = st.number_input("Đường kính cây (m)", min_value=0.0, step=0.01)
        note = st.text_area("Ghi chú")
        location = st.text_input("Vị trí")
        reminder_date = st.date_input("Ngày nhắc nhở")

        if st.session_state.confirm_add_tree:
            st.warning("Bạn có chắc chắn muốn thêm cây này không?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Xác nhận Thêm Cây"):
                    if clf:
                        # Dự đoán tình trạng sức khỏe của cây mới
                        new_data = [[height * 100, diameter * 100, age]]
                        predicted_health = clf.predict(pd.DataFrame(new_data, columns=['Height', 'Diameter', 'Age']))
                        health_status = y_labels[predicted_health.iloc[0]]
                    else:
                        health_status = "Khỏe mạnh"
                    add_tree(engine, species_id, age, height * 100, diameter * 100, health_status, note, location, reminder_date)
                    st.success("Đã thêm cây thành công!")
                    st.session_state.confirm_add_tree = False
                    data = get_trees(engine)
            with col2:
                if st.button("Hủy"):
                    st.session_state.confirm_add_tree = False
        else:
            if st.button("Thêm Cây"):
                st.session_state.confirm_add_tree = True

    with st.expander("Chọn Cây để Chỉnh Sửa/Xóa"):
        selected_tree = st.selectbox("Chọn Cây", data['TreeId'].values, key="select_tree")
        
        if selected_tree:
            tree_data = data[data['TreeId'] == selected_tree]
            new_species_name = st.selectbox("Loại cây mới", list(species_options.keys()), index=list(species_options.values()).index(tree_data['SpeciesId'].values[0]), key="edit_species")
            new_species_id = species_options[new_species_name]
            new_age = st.number_input("Tuổi cây mới", value=int(tree_data['Age'].values[0]), min_value=0, step=1, key="edit_age")
            new_height = st.number_input("Chiều cao cây mới (m)", value=float(tree_data['Height'].values[0]), min_value=0.0, step=0.01, key="edit_height")
            new_diameter = st.number_input("Đường kính cây mới (m)", value=float(tree_data['Diameter'].values[0]), min_value=0.0, step=0.01, key="edit_diameter")
            new_health_status = st.selectbox("Tình trạng sức khỏe mới", health_status_options, index=health_status_options.index(tree_data['HealthStatus'].values[0]), key="edit_health_status")
            new_note = st.text_area("Ghi chú mới", tree_data['Note'].values[0], key="edit_note")
            new_location = st.text_input("Vị trí mới", tree_data['Location'].values[0], key="edit_location")
            new_reminder_date = st.date_input("Ngày nhắc nhở mới", datetime.strptime(tree_data['ReminderDate'].values[0], "%Y-%m-%d").date(), key="edit_reminder_date")

            if st.session_state.confirm_update_tree:
                st.warning("Bạn có chắc chắn muốn cập nhật cây này không?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Xác nhận Cập Nhật Cây"):
                        update_tree(engine, selected_tree, new_species_id, new_age, new_height * 100, new_diameter * 100, new_health_status, new_note, new_location, new_reminder_date)
                        st.success("Đã cập nhật cây thành công!")
                        st.session_state.confirm_update_tree = False
                        data = get_trees(engine)
                with col2:
                    if st.button("Hủy"):
                        st.session_state.confirm_update_tree = False
            else:
                if st.button("Cập Nhật Cây"):
                    st.session_state.confirm_update_tree = True

            if st.session_state.confirm_delete_tree:
                st.warning("Bạn có chắc chắn muốn xóa cây này không?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Xác nhận Xóa Cây"):
                        delete_tree(engine, selected_tree)
                        st.success("Đã xóa cây thành công!")
                        st.session_state.confirm_delete_tree = False
                        data = get_trees(engine)
                with col2:
                    if st.button("Hủy"):
                        st.session_state.confirm_delete_tree = False
            else:
                if st.button("Xóa Cây"):
                    st.session_state.confirm_delete_tree = True

elif menu == "Biểu Đồ Theo Dõi":
    st.header("Biểu Đồ Theo Dõi")
    data = get_trees(engine)
    
    # Biểu đồ số lượng cây theo tình trạng sức khỏe
    chart_data = data.groupby("HealthStatus").size().reset_index(name="Counts")
    fig = px.bar(chart_data, x="HealthStatus", y="Counts", title="Số lượng cây theo tình trạng sức khỏe")
    fig.update_layout(xaxis_title="Tình trạng sức khoẻ", yaxis_title="Số lượng")
    st.plotly_chart(fig)
    
    # Biểu đồ phân bố chiều cao và đường kính cây
    fig = px.scatter(data, x="Diameter", y="Height", color="HealthStatus", size="Age", hover_data=["Species", "Location"], title="Phân bố Chiều cao và Đường kính cây")
    fig.update_layout(xaxis_title="Đường kính (m)", yaxis_title="Chiều cao (m)")
    st.plotly_chart(fig)
    
    # Biểu đồ tỷ lệ loài cây
    species_distribution = data['Species'].value_counts().reset_index()
    species_distribution.columns = ['Species', 'Counts']
    fig = px.pie(species_distribution, names='Species', values='Counts', title="Tỷ lệ Loài cây")
    st.plotly_chart(fig)
