import boundarysolver

import math
from dataclasses import dataclass, field
import streamlit as st
import plotly.graph_objects as graph

# Test case

def test_k1 (x : float):
    return 0.0

def test_k2 (x : float):
    return 0.0

def test_q1 (x : float):
    return 0.0

def test_q2 (x : float):
    return 0.0

def test_f1 (x : float):
    return 0.0

def test_f2 (x : float):
    return 0.0


# Main case

def main_k1 (x : float) -> float:
    return (x + 1) * (x + 1)

def main_k2 (x : float) -> float:
    return x * x

def main_q1 (x : float) -> float:
    return math.exp(-x) * math.sqrt(math.exp(1.0))

def main_q2 (x : float) -> float:
    return math.exp(x) / math.sqrt(math.exp(1.0))

def main_f1 (x : float) -> float:
    return math.cos(x * math.pi)

def main_f2 (x : float) -> float:
    return 1


# STREAM LIT

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None


st.set_page_config(layout="wide")
st.title('Краевая Задача')

# Sidebar
with st.sidebar:
    st.header("Параметры")
    
    # Input parameters
    problem_select = st.selectbox(
    "Выберите задачу",
    ("Тестовая", "Основная")
    )
    
    n = st.number_input("Кол-во узлов (n)", value=5, min_value=2, step=1, key="n")
    
    # Build button
    build_button = st.button("Решить", type="primary", width='stretch')


# Build button press event
if build_button:
    with st.spinner("Вычисляем..."):
        # try:
            if problem_select == "Тестовая":
                k1 = test_k1
                k2 = test_k2
                q1 = test_q1
                q2 = test_q2
                f1 = test_f1
                f2 = test_f2
            
            elif problem_select == "Основная":
                k1 = main_k1
                k2 = main_k2
                q1 = main_q1
                q2 = main_q2
                f1 = main_f1
                f2 = main_f2
                
            v_vector = boundarysolver.solve_bvp(k1, k2, q1, q2, f1, f2, int(n))
            # error = error_eval(function, function_der, function_der_der, spline_data.coefs, spline_data.sample_x, num_control_nodes)
            
            # Store in session state
            st.session_state.data = {
                'n' : n,
                'v_vector' : v_vector
            }
            
        # except Exception as e:
        #     st.error(f"Ошибка: {str(e)}")
        #     st.session_state.data = None

# Display plot if data is available
if st.session_state.data is not None:
    data = st.session_state.data
    n = data['n']
    v_vector = data['v_vector']
    
    # PLOT
    st.subheader("Графики")
    fig = graph.Figure()
    
    # Spline
    fig.add_trace(graph.Scatter(
        x=[0 + i * (1 / n) for i in range(n)], y=v_vector, 
        mode='lines', 
        name='S'
    ))
    
    fig.update_layout(
        xaxis_title="X",
        yaxis_title="Y",
        hovermode='closest',
        legend=dict(
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            bordercolor="black",
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig, width='stretch')
    
    fig = graph.Figure()
    
    # st.subheader("Справка")
    
    # st.info(f"Сетка сплайна: {len(spline_data.sample_x)}")
    # st.info(f"Контрольная сетка: {len(error_data.x)}")
    
    # st.info(f"Погрешность сплайна на контрольной сетке: \
    #         { max([abs(error_data.spline_y[i] - error_data.sample_y[i]) for i in range(len(error_data.x))])} \
    #         ")
    # st.info(f"Погрешность производной на контрольной сетке: \
    #     { max([abs(error_data.spline_der_y[i] - error_data.sample_der_y[i]) for i in range(len(error_data.x))])} \
    #         ")
    # st.info(f"Погрешность второй производной на контрольной сетке: \
    #     { max([abs(error_data.spline_der_der_y[i] - error_data.sample_der_der_y[i]) for i in range(len(error_data.x))])} \
    #         ")
    
    # # DATA
    # st.subheader("Таблица")
    
    # # Display coefficients
    # coef_data = []
    # for i, (a, b, c, d) in enumerate(spline_data.coefs):
    #     coef_data.append({
    #         "i": i + 1,
    #         "X i-1": spline_data.sample_x[i],
    #         "X i": spline_data.sample_x[i + 1],
    #         "a": f"{a:.4f}",
    #         "b": f"{b:.4f}",
    #         "c": f"{c:.4f}",
    #         "d": f"{d:.4f}"
    #     })
        
    # column_config = {
    #     "i": st.column_config.NumberColumn(
    #         "i"
    #     ),
    #     "X i-1": st.column_config.NumberColumn(
    #         "X i-1",
    #         format="%.5f"
    #     ),
    #     "X i": st.column_config.NumberColumn(
    #         "X i",
    #         format="%.5f"
    #     )
    # }
    
    # for i in ["a", "b", "c", "d"]:
    #     column_config[i] = st.column_config.NumberColumn(
    #         i,
    #         format="%.15f"
    #     )
    
    # st.dataframe(coef_data, width='stretch')
    
    # st.subheader("Погрешность")
    
    # fig = graph.Figure()
    
    # # Spline der der
    # fig.add_trace(graph.Scatter(
    #     x=error_data.x, y=[error_data.spline_y[i] - error_data.sample_y[i] for i in range(len(error_data.x))], 
    #     mode='lines', 
    #     name="F - S"
    # ))
    
    # fig.add_trace(graph.Scatter(
    #     x=error_data.x, y=[error_data.spline_der_y[i] - error_data.sample_der_y[i] for i in range(len(error_data.x))], 
    #     mode='lines', 
    #     name="F' - S'"
    # ))
        
    # fig.add_trace(graph.Scatter(
    #     x=error_data.x, y=[error_data.spline_der_der_y[i] - error_data.sample_der_der_y[i] for i in range(len(error_data.x))], 
    #     mode='lines', 
    #     name="F'' - S''"
    # ))
    
    # fig.update_layout(
    #     xaxis_title="X",
    #     yaxis_title="Y",
    #     hovermode='closest',
    #     legend=dict(
    #         yanchor="top",
    #         y=1,
    #         xanchor="left",
    #         x=1.02,
    #         bordercolor="black",
    #         borderwidth=1
    #     )
    # )
    
    # st.plotly_chart(fig, width='stretch')
    
    # # Display coefficients
    # error_eval_data = []
    # for i, x in enumerate(error_data.x):
    #     error_eval_data.append({
    #         "j": i,
    #         "X j": x,
    #         "F(Xj)": error_data.sample_y[i],
    #         "S(Xj)": error_data.spline_y[i],
    #         "F(Xj) - S(Xj)": error_data.sample_y[i] - error_data.spline_y[i],
            
    #         "F'(Xj)": error_data.sample_der_y[i],
    #         "S'(Xj)": error_data.spline_der_y[i],
    #         "F'(Xj) - S'(Xj)": error_data.sample_der_y[i] - error_data.spline_der_y[i],
            
    #         "F''(Xj)": error_data.sample_der_der_y[i],
    #         "S''(Xj)": error_data.spline_der_der_y[i],
    #         "F''(Xj) - S''(Xj)": error_data.sample_der_der_y[i] - error_data.spline_der_der_y[i],
    #     })
        
    # column_config = {
    #     "j": st.column_config.NumberColumn(
    #         "j"
    #     ),
    #     "X j": st.column_config.NumberColumn(
    #         "X j",
    #         format="%.5f"
    #     )
    # }
    
    # for i in ["F(Xj)", "S(Xj)", "F(Xj) - S(Xj)", "F'(Xj)", "S'(Xj)", "F'(Xj) - S'(Xj)", "F''(Xj)", "S''(Xj)", "F''(Xj) - S''(Xj)"]:
    #     column_config[i] = st.column_config.NumberColumn(
    #         i,
    #         format="%.15f"
    #     )
    
    # st.dataframe(error_eval_data, width='stretch', column_config=column_config)