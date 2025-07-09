import streamlit as st

# 結構定義
components_dict = {
    "Fresh Oocyte ICSI": {
        "<7# HTF": {"HTF": 2.5},
        ">8# HTF": {"HTF": 3.1},
        "≧12 HTF": {"HTF": 3.75},
        "≧20 HTF": {"HTF": 6.36},
        "other HTF": {"HTF": 0},
        "<5# GL": {"GL": 0.25},
        "6-20# GL": {"GL": 0.35},
        ">21 GL": {"GL": 0.7},
    },
    "Frest Oocyte IVF": {"HTF": 1.0, "GL": 0.35},
    "Frest Oocyte ICSI+IVF": {
        ">8# HTF": {"HTF": 4.1},
        "≦20# HTF": {"HTF": 6.7},
        "# GL": {"GL": 0.7},
    },
    "Thaw Oocyte ICSI": {
        "D-1 HTF": {"HTF": 0.5},
        "≦20 GL": {"GL": 0.35},
        "≧21 GL": {"GL": 0.7},
    },
    "Cryo Oocyte": {
        "<7# HTF": {"HTF": 2.3},
        ">8# HTF": {"HTF": 2.9},
        "≧12 HTF": {"HTF": 3.55},
        "≧20 HTF": {"HTF": 6.15},
        "other HTF": {"HTF": 0},
    },
    "FET": {
        "D-2 GL": {"GL": 0.2},
    },
    "Change Dish": {
        "<5 GL": {"GL": 0.25},
        "≧6 GL": {"GL": 0.35},
    },
    "Biopsy": {"GL": 0.2}
}

# 記錄加總
total_components = {}

st.title("🧪 實驗室培養液計算器")

# 遍歷每個項目
for item, themes in components_dict.items():
    st.subheader(f"📦 {item}")

    if isinstance(themes, dict) and all(isinstance(v, dict) for v in themes.values()):
        for theme, ingredients in themes.items():
            with st.expander(f"🔸 {theme}", expanded=False):
                people = st.number_input(f"{item} - {theme} 人數", min_value=0, step=1, key=f"{item}_{theme}")
                for name, dose in ingredients.items():
                    # 若劑量為 0，開放輸入劑量
                    if dose == 0:
                        dose = st.number_input(f"{item} - {theme} - {name} 劑量", min_value=0.0, step=0.1,
                                               key=f"{item}_{theme}_{name}_dose")

                    subtotal = people * dose
                    st.markdown(f"- {name}：{dose} × {people} = **{subtotal:.2f} ml**")

                    if name in total_components:
                        total_components[name] += subtotal
                    else:
                        total_components[name] = subtotal

    else:
        # 沒有主題的平坦結構
        with st.expander(f"{item}", expanded=False):
            people = st.number_input(f"{item} 人數", min_value=0, step=1, key=f"{item}_flat")
            for name, dose in themes.items():
                subtotal = people * dose
                st.markdown(f"- {name}：{dose} × {people} = **{subtotal:.2f} ml**")
                if name in total_components:
                    total_components[name] += subtotal
                else:
                    total_components[name] = subtotal

st.markdown("---")
st.header("📊 成分加總用量")
for name, total in total_components.items():
    st.write(f"🔹 {name}：{total:.2f} ml")
