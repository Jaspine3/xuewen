import streamlit as st
import pandas as pd
import plotly.express as px

# --- 页面配置 ---
st.set_page_config(page_title="学生成绩趋势分析系统", layout="wide")
st.title("📊 学生成绩与排名追踪系统")

# --- 侧边栏：数据导入 ---
st.sidebar.header("1. 数据来源")
upload_file = st.sidebar.file_uploader("上传成绩单 (Excel/CSV)", type=["xlsx", "csv"])

# --- 示例数据生成函数 (如果没有上传文件时显示) ---
def get_sample_data():
    data = {
        '姓名': ['张三', '张三', '张三', '李四', '李四', '李四'],
        '考试名称': ['月考1', '期中考', '月考2', '月考1', '期中考', '月考2'],
        '科目': ['数学', '数学', '数学', '数学', '数学', '数学'],
        '成绩': [85, 92, 88, 78, 85, 95],
        '排名': [5, 2, 4, 10, 5, 1]
    }
    return pd.DataFrame(data)

# --- 数据处理逻辑 ---
if upload_file:
    try:
        if upload_file.name.endswith('.csv'):
            df = pd.read_csv(upload_file)
        else:
            df = pd.read_excel(upload_file)
        st.sidebar.success("✅ 数据导入成功！")
    except Exception as e:
        st.error(f"文件读取失败: {e}")
        st.stop()
else:
    st.info("👋 尚未上传文件，正在使用示例数据演示。请在侧边栏上传您的 Excel 表格。")
    df = get_sample_data()

# --- 数据预览与编辑 (支持自定义录入) ---
with st.expander("📝 数据预览与编辑 (点击此处展开)", expanded=False):
    st.caption("您可以在下方表格中直接修改数据，或者添加新行。")
    edited_df = st.data_editor(df, num_rows="dynamic") # 允许添加新行

# --- 数据分析区 ---
st.divider()
st.header("2. 趋势分析面板")

# 获取所有学生和科目列表
student_list = edited_df['姓名'].unique().tolist()
subject_list = edited_df['科目'].unique().tolist()

# 筛选控件
col1, col2 = st.columns(2)
with col1:
    selected_student = st.selectbox("选择学生:", student_list)
with col2:
    selected_subject = st.multiselect("选择科目 (可多选):", subject_list, default=subject_list[0])

# 数据过滤
filtered_df = edited_df[
    (edited_df['姓名'] == selected_student) & 
    (edited_df['科目'].isin(selected_subject))
]

if not filtered_df.empty:
    # --- 图表 1: 成绩变化趋势 ---
    st.subheader(f"📈 {selected_student} - 成绩变化趋势")
    fig_score = px.line(filtered_df, x='考试名称', y='成绩', color='科目', markers=True,
                        title=f"{selected_student} 各科成绩走势")
    fig_score.update_layout(yaxis_title="分数", hovermode="x unified")
    st.plotly_chart(fig_score, use_container_width=True)

    # --- 图表 2: 排名变化趋势 ---
    st.subheader(f"🏆 {selected_student} - 排名变化趋势")
    # 注意：排名是越小越好，所以我们需要反转 Y 轴
    if '排名' in filtered_df.columns:
        fig_rank = px.line(filtered_df, x='考试名称', y='排名', color='科目', markers=True,
                           title=f"{selected_student} 各科排名走势 (越高越好)")
        fig_rank.update_yaxes(autorange="reversed") # 反转Y轴，让第1名在最上面
        fig_rank.update_layout(yaxis_title="名次", hovermode="x unified")
        st.plotly_chart(fig_rank, use_container_width=True)
    else:
        st.warning("⚠️ 数据表中未检测到‘排名’列，无法生成排名趋势图。")
        
    # --- 详细数据表格 ---
    st.subheader("📋 详细数据记录")
    st.dataframe(filtered_df)

else:
    st.warning("未找到该学生的考试数据。")
