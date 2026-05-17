import boundarysolver

import math
from dataclasses import dataclass, field
import streamlit as st
import plotly.graph_objects as graph

# General
ksi = 0.5

# Test case

def test_analytical (x : float):
    return 0.0 # заглушка

def test_analytical_mixed (x : float):
    C1 = -0.176770
    C2 = 0.707598
    C3 = -0.141992
    C4 = 0.533268
    if x <= math.pi / 4:
        return C1 * math.exp( math.sqrt(math.pi) / 2 * x ) + C2 * math.exp( -math.sqrt(math.pi) / 2 * x ) + 4 / math.pi
    else:
        return C3 * math.exp( math.pi /(4 * math.sqrt(2)) * x) + C4 * math.exp( -math.pi /(4 * math.sqrt(2)) * x) + 8 * math.sqrt(2) / math.pi**2

def test_k1 (x : float):
    return 1

def test_k2 (x : float):
    return 2

def test_q1 (x : float):
    return math.pi / 4

def test_q2 (x : float):
    return math.pi ** 2 / 16

def test_f1 (x : float):
    return 1

def test_f2 (x : float):
    return math.sqrt(2) / 2


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
    (
        "первая краевая тестовая задача",
        "первая краевая основная задача",
        "смешанная краевая тестовая задача, классич. аппрокс. ГУ",
        "смешанная краевая основная задача, улучш. аппрокс. ГУ")
    )
    
    n = st.number_input("Кол-во узлов", value=5, min_value=2, step=1, key="n") - 1
    
    # Build button
    build_button = st.button("Решить", type="primary", width='stretch')


# Build button press event
if build_button:
    with st.spinner("Вычисляем..."):
        # try:
            if problem_select == "первая краевая тестовая задача":
                k1 = test_k1
                k2 = test_k2
                q1 = test_q1
                q2 = test_q2
                f1 = test_f1
                f2 = test_f2
                
                v_vector = boundarysolver.solve_bvp(k1, k2, q1, q2, f1, f2, ksi, int(n))
                control_vector = [test_analytical(0.0 + i * (1 / n)) for i in range(n + 1)]
                control_graph = control_vector
            
            elif problem_select == "первая краевая основная задача":
                k1 = main_k1
                k2 = main_k2
                q1 = main_q1
                q2 = main_q2
                f1 = main_f1
                f2 = main_f2
                
                v_vector = boundarysolver.solve_bvp(k1, k2, q1, q2, f1, f2, ksi, int(n))
                control_graph = boundarysolver.solve_bvp(k1, k2, q1, q2, f1, f2, ksi, int(n) * 2)
                control_vector = control_graph[::2]

            elif problem_select == "смешанная краевая тестовая задача, классич. аппрокс. ГУ":
                k1 = test_k1
                k2 = test_k2
                q1 = test_q1
                q2 = test_q2
                f1 = test_f1
                f2 = test_f2
                
                v_vector = boundarysolver.solve_bvp_mixed_test_function(k1, k2, q1, q2, f1, f2, ksi, int(n))
                control_vector = [test_analytical_mixed(0.0 + i * (1 / n)) for i in range(n + 1)]
                control_graph = control_vector
            
            error_eval_list = [abs(v_vector[i] - control_vector[i]) for i in range(n + 1)]
            
            error = 0.0
            max_error_x = 0.0
            for i, e in enumerate(error_eval_list):
                if e > error:
                    error = e
                    max_error_x = 0.0 + i * (1 / n)
            
            # Store in session state
            st.session_state.data = {
                'problem' : problem_select,
                'n' : n,
                'v_vector' : v_vector,
                'control_vector' : control_vector,
                'control_graph' : control_graph,
                'error' : error,
                'max_error_x' : max_error_x,
                'error_eval_list' : error_eval_list
            }
            
        # except Exception as e:
        #     st.error(f"Ошибка: {str(e)}")
        #     st.session_state.data = None

# Display plot if data is available
if st.session_state.data is not None:
    data = st.session_state.data
    problem = data['problem']
    n = data['n']
    v_vector = data['v_vector']
    control_vector = data['control_vector']
    control_graph = data['control_graph']
    error = data['error']
    max_error_x = data['max_error_x']
    error_eval_list = data['error_eval_list']
    
    # PLOT
    st.subheader("Графики")
    fig = graph.Figure()
    
    fig.add_trace(graph.Scatter(
        x=[0 + i * (1 / (len(control_graph) - 1)) for i in range(len(control_graph))], y=control_graph, 
        mode='lines', 
        name= 'V2' if problem == "первая краевая основная задача" else 'U',
        line=dict(color='rgb(75, 75, 255)')
    ))
    
    fig.add_trace(graph.Scatter(
        x=[0 + i * (1 / n) for i in range(n + 1)], y=v_vector, 
        mode='lines', 
        name='V',
        line=dict(color='rgb(255, 255, 255)')
    ))
    
    fig.update_layout(
        title="Решение",
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
    
    fig.add_trace(graph.Scatter(
        x=[0 + i * (1 / n) for i in range(n + 1)], y=[control_vector[i] - v_vector[i] for i in range(n + 1)], 
        mode='lines', 
        name='Error'
    ))
    
    fig.update_layout(
        title="Погрешность",
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
        ),
        yaxis=dict(
            exponentformat='power', # Options: 'none', 'e', 'E', 'power', 'SI', 'B'
            showexponent='all'      # Options: 'none', 'all', 'first', 'last'
        )
    )
    
    st.plotly_chart(fig, width='stretch')
    
    # INFO
    st.subheader("Справка")
    
    if problem == "первая краевая тестовая задача":
        st.info(f"""Для решения задачи использована равномерная сетка с числом разбиений n = {n}; \n
Задача должна быть решена с погрешностью не более ε = 0.5⋅10 –6; \n
Задача решена с погрешностью ε1 = {error}; \n
Максимальное отклонение аналитического и численного решений наблюдается в точке x = {max_error_x}.
""")
        
    elif problem == "первая краевая основная задача":
        st.info(f"""Для решения задачи использована равномерная сетка с числом разбиений n = {n}; \n
Задача должна быть решена с погрешностью не более ε = 0.5⋅10 –6; \n
Задача решена с погрешностью ε2 = {error}; \n
Максимальное отклонение аналитического и численного решений наблюдается в точке x = {max_error_x}.
""")
    
    # DATA
    st.subheader("Таблица")
    
    # Table data
    if problem == "первая краевая тестовая задача":
        table_data = []
        for i in range(n + 1):
            table_data.append({
                "N": i,
                "X_i": 0.0 + i * (1 / n),
                "U_i": control_vector[i],
                "V_i": v_vector[i],
                "U_i - V_i": control_vector[i] - v_vector[i],
            })
            
        column_config = {
            "N": st.column_config.NumberColumn(
                "N"
            ),
            "X_i": st.column_config.NumberColumn(
                "X_i",
                format="%.5f"
            ),
            "U_i": st.column_config.NumberColumn(
                "U_i",
                format="%.5f"
            ),
            "V_i": st.column_config.NumberColumn(
                "V_i",
                format="%.5f"
            ),
            "U_i - V_i": st.column_config.NumberColumn(
                "U_i - V_i",
                format="%.15f"
            )
        }
        
        st.dataframe(table_data, width='stretch', column_config=column_config)
        
        
    elif problem == "первая краевая основная задача":
        table_data = []
        for i in range(n + 1):
            table_data.append({
                "N": i,
                "X_i": 0.0 + i * (1 / n),
                "V_i": v_vector[i],
                "V2_i": control_vector[i],
                "V2_i - V_i": control_vector[i] - v_vector[i],
            })
            
        column_config = {
            "N": st.column_config.NumberColumn(
                "N"
            ),
            "X_i": st.column_config.NumberColumn(
                "X_i",
                format="%.15f"
            ),
            "V_i": st.column_config.NumberColumn(
                "V_i",
                format="%.15f"
            ),
            "V2_i": st.column_config.NumberColumn(
                "V2_i",
                format="%.15f"
            ),
            "V2_i - V_i": st.column_config.NumberColumn(
                "V2_i - V_i",
                format="%.15f"
            )
        }
        
        st.dataframe(table_data, width='stretch', column_config=column_config)