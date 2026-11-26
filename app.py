
import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

from simulations.covid import (
    create_covid_environment,
    get_covid_information,
    get_covid_defaults,
    get_covid_dataset_information,
    get_covid_transition_matrix,
    validate_covid_start
)

from simulations.algorithms import (
    compare_algorithms,
    compare_repeated_experiments
)

from simulations.weather import (
    create_weather_environment,
    get_weather_information,
    get_weather_defaults,
    get_weather_transition_matrix,
    validate_weather_start
)

from simulations.wildlife import (
    create_wildlife_environment,
    get_wildlife_information,
    get_wildlife_graph_summary
)

from simulations.network import (
    create_network_environment,
    get_network_information,
    get_network_graph_summary,
    get_network_dataset_information,
    get_network_defaults,
    validate_network_start,
    get_network_dataset_source
)


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Entropy Lab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================================
# SESSION STATE
# =====================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "covid_result" not in st.session_state:
    st.session_state.covid_result = None

if "covid_repeated_result" not in st.session_state:
    st.session_state.covid_repeated_result = None


def enter_lab():
    st.session_state.page = "introduction"


def go_home():
    st.session_state.page = "home"


def open_covid():
    st.session_state.page = "covid"

def open_weather():
    st.session_state.page = "weather"    

def open_wildlife():
    st.session_state.page = "wildlife"

def open_network():
    st.session_state.page = "network"


def reset_covid():
    defaults = get_covid_defaults()

    st.session_state.covid_start = defaults["start_state"]
    st.session_state.covid_steps = defaults["steps"]
    st.session_state.covid_rho = defaults["rho"]
    st.session_state.covid_eta = defaults["eta"]
    st.session_state.covid_temperature = defaults[
        "initial_temperature"
    ]

    st.session_state.covid_result = None
    st.session_state.covid_repeated_result = None


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 15% 20%, rgba(0,180,216,.15), transparent 40%),
        radial-gradient(ellipse at 85% 80%, rgba(99,102,241,.15), transparent 40%),
        linear-gradient(135deg,#07111f,#0b192b,#101c35);
    color:white;
    font-family:'Inter',sans-serif;
}

#MainMenu, footer {
    visibility:hidden;
}

header {
    background:transparent !important;
}

.block-container {
    max-width:1250px;
    padding-top:2rem;
    padding-bottom:2rem;
}

/* HOME PAGE */

.hero {
    min-height:570px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    text-align:center;
    padding:35px 15px;
}

.lab-label {
    color:#00d4ff;
    font-size:13px;
    letter-spacing:5px;
    font-weight:600;
    margin-bottom:30px;
}

.hero-title {
    font-family:'Orbitron',sans-serif;
    font-size:clamp(48px,8vw,90px);
    font-weight:800;
    letter-spacing:5px;
    line-height:1.2;
    margin:0;
    background:linear-gradient(90deg,#fff,#00d4ff,#8b9cff);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero-subtitle {
    color:#c1d3e8;
    font-size:19px;
    line-height:1.8;
    margin-top:25px;
    max-width:750px;
}

.hero-tagline {
    color:#00d4ff;
    font-size:13px;
    letter-spacing:4px;
    margin-top:24px;
    font-weight:600;
}

.glow-line {
    width:110px;
    height:3px;
    background:#00d4ff;
    margin:30px auto;
    border-radius:10px;
    box-shadow:0 0 15px #00d4ff;
}

/* BUTTONS */

div.stButton > button {
    background:linear-gradient(90deg,#00b4d8,#4361ee);
    color:white;
    border:none;
    border-radius:10px;
    min-height:48px;
    font-size:14px;
    font-weight:700;
    letter-spacing:1px;
    transition:all .3s ease;
    box-shadow:0 0 22px rgba(0,212,255,.25);
}

div.stButton > button:hover {
    transform:translateY(-3px);
    box-shadow:0 0 35px rgba(0,212,255,.6);
    color:white;
}

/* INTRODUCTION PAGE */

.intro-heading {
    font-family:'Orbitron',sans-serif;
    color:#00d4ff;
    font-size:clamp(26px,4vw,40px);
    font-weight:700;
    text-align:center;
    margin-top:25px;
}

.intro-subheading {
    color:#b9cce0;
    font-size:17px;
    text-align:center;
    margin-bottom:35px;
}

.section-card {
    background:linear-gradient(
        120deg,
        rgba(255,255,255,.075),
        rgba(255,255,255,.035)
    );
    border:1px solid rgba(0,212,255,.22);
    border-radius:16px;
    padding:27px;
    margin:18px 0;
    color:#e0eaf5;
    line-height:1.8;
}

.section-card h3 {
    color:#00d4ff;
    margin-top:0;
    font-size:23px;
}

.section-card p {
    font-size:16px;
}

.algorithm-card {
    min-height:220px;
    padding:25px;
    border-radius:16px;
    margin:10px 0;
    line-height:1.8;
}

.srw-card {
    background:rgba(32,113,190,.15);
    border:1px solid rgba(70,160,255,.4);
}

.ebw-card {
    background:rgba(24,160,130,.13);
    border:1px solid rgba(55,220,180,.4);
}

.srw-card h3 {
    color:#65b9ff;
}

.ebw-card h3 {
    color:#4de0c1;
}

.algorithm-formula {
    font-size:25px;
    font-weight:700;
    text-align:center;
    padding:12px;
    color:white;
}

.flow-card {
    background:rgba(0,180,216,.08);
    border:1px solid rgba(0,212,255,.2);
    border-radius:12px;
    padding:16px;
    text-align:center;
    color:white;
    font-weight:600;
}

.flow-arrow {
    text-align:center;
    color:#00d4ff;
    font-size:25px;
    padding:3px;
}

.examples-heading {
    text-align:center;
    color:#00d4ff;
    font-family:'Orbitron',sans-serif;
    font-size:30px;
    margin-top:45px;
}

.footer {
    text-align:center;
    color:#71849d;
    font-size:12px;
    letter-spacing:2px;
    padding-top:30px;
}

/* APPLICATION PAGE */

.app-heading {
    font-family:'Orbitron',sans-serif;
    color:#00d4ff;
    font-size:clamp(25px,4vw,38px);
    font-weight:700;
    text-align:center;
    margin-top:20px;
}

.app-subheading {
    color:#b9cce0;
    text-align:center;
    font-size:16px;
    margin-bottom:25px;
}

.panel {
    background:rgba(255,255,255,.055);
    border:1px solid rgba(0,212,255,.2);
    border-radius:15px;
    padding:20px;
    margin:12px 0;
}

.panel h3 {
    color:#00d4ff;
}

.small-note {
    color:#9eb3ca;
    font-size:13px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# PAGE 1 - HOME PAGE
# =====================================================

if st.session_state.page == "home":

    st.html("""
    <div class="hero">

        <div class="lab-label">
            RESEARCH • SIMULATION • ANALYSIS
        </div>

        <h1 class="hero-title">
            ENTROPY LAB
        </h1>

        <div class="glow-line"></div>

        <div class="hero-subtitle">
            An Entropy-Based Random Walk Framework
            <br>
            Exploring how intelligent probability adaptation
            changes the behaviour of random walks.
        </div>

        <div class="hero-tagline">
            EXPLORE • SIMULATE • COMPARE
        </div>

    </div>
    """)

    left, center, right = st.columns([1, 1, 1])

    with center:
        st.button(
            "ENTER LAB  →",
            use_container_width=True,
            on_click=enter_lab
        )

    st.html("""
    <div class="footer">
        ENTROPY LAB | RANDOM WALK RESEARCH PROJECT
    </div>
    """)


# =====================================================
# PAGE 2 - INTRODUCTION PAGE
# =====================================================

elif st.session_state.page == "introduction":

    st.button("← BACK TO HOME", on_click=go_home)

    st.html("""
    <div class="intro-heading">
        WELCOME TO ENTROPY LAB
    </div>

    <div class="intro-subheading">
        Understanding random walks through entropy-based adaptation
    </div>
    """)

    # WHAT ARE WE DOING?

    st.html("""
    <div class="section-card">

        <h3>01. What are we doing?</h3>

        <p>
        We are developing a simulation framework to compare two
        different random-walk approaches:
        <b>Simple Random Walk (SRW)</b> and
        <b>Entropy-Based Walk (EBW).</b>
        </p>

        <p>
        We apply these two models to four real-world
        environments and study how their exploration behaviour
        changes.
        </p>

    </div>
    """)

    # WHY ARE WE DOING THIS?

    st.html("""
    <div class="section-card">

        <h3>02. Why are we doing this?</h3>

        <p>
        Traditional random walks select the next available node
        with equal probability. They do not consider which
        locations have already been explored.
        </p>

        <p>
        Our project investigates whether entropy-based
        probability adaptation can change exploration patterns
        and reduce unnecessary repeated visits.
        </p>

    </div>
    """)

    # UNDERSTANDING ALGORITHMS

    st.html("""
    <div class="intro-heading">
        03. UNDERSTANDING OUR ALGORITHMS
    </div>

    <div class="intro-subheading">
        Two approaches. One common simulation environment.
    </div>
    """)

    col1, col2 = st.columns(2)

    with col1:

        st.html("""
        <div class="algorithm-card srw-card">

            <h3>Simple Random Walk (SRW)</h3>

            <p>
            SRW selects one of the available neighbouring
            nodes with equal probability.
            </p>

            <div class="algorithm-formula">
                P(i → j) = 1 / dᵢ
            </div>

            <p>
            Every available next node has the same chance
            of being selected.
            </p>

        </div>
        """)

    with col2:

        st.html("""
        <div class="algorithm-card ebw-card">

            <h3>Entropy-Based Walk (EBW)</h3>

            <p>
            EBW adjusts the probability of selecting the
            next node using exploration history and
            Shannon entropy.
            </p>

            <div class="algorithm-formula">
                H(X) = − Σ p(x) log p(x)
            </div>

            <p>
            The probability distribution changes as the
            simulation progresses.
            </p>

        </div>
        """)

    # WHY COMPARE?

    st.html("""
    <div class="section-card">

        <h3>04. Why compare SRW and EBW?</h3>

        <p>
        Both algorithms explore the same environment,
        but they make decisions differently.
        </p>

        <p>
        By comparing them, we can understand their differences
        in node coverage, repeated visits, edge exploration
        and transition entropy.
        </p>

        <p>
        We do not assume that EBW is always better.
        Its performance will be evaluated using actual
        simulation results.
        </p>

    </div>
    """)

    # HOW OUR MODEL WORKS

    st.html("""
    <div class="intro-heading">
        05. HOW OUR MODEL WORKS
    </div>

    <div class="intro-subheading">
        A simple overview of our simulation process
    </div>
    """)

    st.html("""
    <div class="flow-card">
        STEP 1 — Create an environment using a dataset
    </div>

    <div class="flow-arrow">↓</div>

    <div class="flow-card">
        STEP 2 — Apply SRW and EBW
    </div>

    <div class="flow-arrow">↓</div>

    <div class="flow-card">
        STEP 3 — Run both simulations
    </div>

    <div class="flow-arrow">↓</div>

    <div class="flow-card">
        STEP 4 — Collect simulation results
    </div>

    <div class="flow-arrow">↓</div>

    <div class="flow-card">
        STEP 5 — Compare graphs and performance
    </div>

    <div class="flow-arrow">↓</div>

    <div class="flow-card">
        STEP 6 — Analyse the final output
    </div>
    """)

    # REAL-LIFE EXAMPLES

    st.html("""
    <div class="examples-heading">
        REAL-LIFE EXAMPLES
    </div>

    <div class="intro-subheading">
        Explore how our two algorithms behave in four
different real-world environments.
    </div>
    """)

    
    examples = [
        "Select an example",
        "COVID-19 Spread-Pattern Simulation",
        "Weather Pattern Simulation",
        "Wildlife and Biodiversity Simulation",
        "Computer Network Simulation"
    ]


    selected = st.selectbox(
             "Choose an application",
                examples,
                key="application_dropdown"
     )

    if selected == "COVID-19 Spread-Pattern Simulation":

        st.success(
            "The real-data COVID simulation is available."
        )

        st.button(
            "OPEN COVID SIMULATION →",
            use_container_width=True,
            on_click=open_covid
        )
    elif selected == "Weather Pattern Simulation":

        st.success(
            "The real-data Bengaluru Weather simulation is available."
        )

        st.button(
            "OPEN WEATHER SIMULATION →",
            use_container_width=True,
            on_click=open_weather
        )
    elif selected == "Wildlife and Biodiversity Simulation":

        st.success(
            "The real-data Mysuru City Bird Atlas simulation is available."
        )

        st.button(
            "OPEN WILDLIFE SIMULATION →",
            use_container_width=True,
            on_click=open_wildlife
        )

    elif selected == "Computer Network Simulation":

        st.success(
            "The real-data Stanford SNAP Internet topology simulation is available."
        )

        st.button(
            "OPEN COMPUTER NETWORK SIMULATION →",
            use_container_width=True,
            on_click=open_network
        )

    elif selected != "Select an example":

        st.info(
            f"You selected: {selected}. "
            "This application is not connected yet."
        )

    st.html("""
    <div class="footer">
        ENTROPY LAB | EXPLORE • SIMULATE • COMPARE
    </div>
    """)


# =====================================================
# COVID GRAPH VISUALIZATION
# =====================================================

def create_covid_graph_figure(graph, result=None):

    positions = {
        "Low": (0, 1),
        "Moderate": (1.5, 1),
        "High": (3, 1),
        "Very High": (4.5, 1)
    }

    fig = go.Figure()

    # Draw directed edges
    for source, destination, attributes in graph.edges(data=True):

        x0, y0 = positions[source]
        x1, y1 = positions[destination]

        count = attributes["transition_count"]

        fig.add_trace(
            go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode="lines",
                line=dict(
                    width=1.5 + count / 35,
                    color="#3286a8"
                ),
                hovertemplate=(
                    f"{source} → {destination}"
                    f"<br>Observed transitions: {count}"
                    "<extra></extra>"
                ),
                showlegend=False
            )
        )

        fig.add_annotation(
            x=x1,
            y=y1,
            ax=x0,
            ay=y0,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            arrowhead=3,
            arrowsize=1,
            arrowwidth=1.5,
            arrowcolor="#00d4ff",
            standoff=22,
            startstandoff=22
        )

        # Edge labels are placed above the midpoint
        fig.add_annotation(
            x=(x0 + x1) / 2,
            y=(y0 + y1) / 2 + 0.12,
            text=str(count),
            showarrow=False,
            font=dict(color="white", size=11)
        )

    # Draw nodes
    node_colors = {
        "Low": "#2785bd",
        "Moderate": "#23a6a1",
        "High": "#d18b35",
        "Very High": "#d65363"
    }

    for node in graph.nodes():

        x, y = positions[node]

        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                marker=dict(
                    size=42,
                    color=node_colors[node],
                    line=dict(color="white", width=1)
                ),
                text=[node],
                textposition="bottom center",
                textfont=dict(
                    color="white",
                    size=12
                ),
                hovertemplate=f"{node}<extra></extra>",
                showlegend=False
            )
        )

    fig.update_layout(
        title=dict(
            text="Historical COVID Intensity Transition Graph",
            font=dict(color="white", size=19)
        ),
        height=330,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(
            visible=False,
            range=[-0.7, 5.2]
        ),
        yaxis=dict(
            visible=False,
            range=[0.4, 1.7]
        ),
        margin=dict(l=20, r=20, t=60, b=35)
    )

    return fig


# =====================================================
# PATH VISUALIZATION
# =====================================================

def create_path_figure(path, title):

    state_order = [
        "Low",
        "Moderate",
        "High",
        "Very High"
    ]

    state_numbers = {
        state: index
        for index, state in enumerate(state_order)
    }

    values = [
        state_numbers[state]
        for state in path
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=list(range(len(path))),
            y=values,
            mode="lines+markers",
            line=dict(
                color="#00d4ff",
                width=2
            ),
            marker=dict(size=5),
            text=path,
            hovertemplate=(
                "Step: %{x}"
                "<br>State: %{text}"
                "<extra></extra>"
            ),
            showlegend=False
        )
    )

    fig.update_layout(
        title=title,
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(color="white"),
        xaxis_title="Simulation Step",
        yaxis=dict(
            tickmode="array",
            tickvals=[0, 1, 2, 3],
            ticktext=state_order,
            gridcolor="rgba(255,255,255,0.1)"
        ),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.1)"
        ),
        margin=dict(l=20, r=20, t=55, b=40)
    )

    return fig


# =====================================================
# ENTROPY COMPARISON CHART
# =====================================================

def create_entropy_figure(result):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=result["SRW"]["entropy"],
            mode="lines",
            name="SRW",
            line=dict(
                color="#65b9ff",
                width=2
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            y=result["EBW"]["entropy"],
            mode="lines",
            name="EBW",
            line=dict(
                color="#4de0c1",
                width=2
            )
        )
    )

    fig.update_layout(
        title="Transition Entropy Comparison",
        xaxis_title="Simulation Step",
        yaxis_title="Shannon Entropy",
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(color="white"),
        legend=dict(
            orientation="h",
            y=1.12
        ),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.1)"
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.1)"
        )
    )

    return fig


# =====================================================
# TEMPERATURE CHART
# =====================================================

def create_temperature_figure(result):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            y=result["EBW"]["temperature"],
            mode="lines",
            name="EBW Temperature",
            line=dict(
                color="#ffbd59",
                width=2
            )
        )
    )

    fig.update_layout(
        title="EBW Adaptive Temperature",
        xaxis_title="Simulation Step",
        yaxis_title="Temperature",
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(color="white"),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.1)"
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.1)"
        )
    )

    return fig


# =====================================================
# PAGE 3 - COVID SIMULATION
# =====================================================

if st.session_state.page == "covid":

    st.button(
        "← BACK TO APPLICATIONS",
        on_click=lambda: setattr(
            st.session_state,
            "page",
            "introduction"
        )
    )

    st.html("""
    <div class="app-heading">
        COVID-19 SPREAD-PATTERN SIMULATION
    </div>

    <div class="app-subheading">
        Comparing SRW and EBW using historical Bengaluru Urban COVID data
    </div>
    """)

    # Load actual dataset and graph
    try:

        graph = create_covid_environment()

        dataset_info = get_covid_dataset_information(
            graph
        )

    except Exception as error:

        st.error(
            f"Could not load the COVID dataset: {error}"
        )

        st.info(
            "Check that datasets/covid/covid_districts.csv "
            "exists in your project."
        )

        st.stop()

    # -------------------------------------------------
    # ABOUT THE APPLICATION
    # -------------------------------------------------

    st.markdown("### 01. About the topic")

    st.markdown("""
    This application studies historical COVID-19 case-intensity
    changes in Bengaluru Urban.

    Daily new cases are classified into four intensity states.
    Transitions between consecutive historical observations
    create a directed graph.

    SRW and EBW explore this same graph so that their
    exploration behaviour can be compared.
    """)

    # -------------------------------------------------
    # DATASET INFORMATION
    # -------------------------------------------------

    st.markdown("### 02. Dataset information")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Historical observations",
        dataset_info["Observations"]
    )

    c2.metric(
        "Observed transitions",
        dataset_info["Transitions"]
    )

    c3.metric(
        "Graph nodes",
        graph.number_of_nodes()
    )

    c4.metric(
        "Directed edges",
        graph.number_of_edges()
    )

    st.caption(
        f"District: {dataset_info['District']}, "
        f"{dataset_info['State']} | "
        f"Period: {dataset_info['Start Date']} to "
        f"{dataset_info['End Date']}"
    )

    st.markdown(
        "**Source file:** "
        "`datasets/covid/covid_districts.csv`"
    )

    # -------------------------------------------------
    # PROBLEM STATEMENT
    # -------------------------------------------------

    st.markdown("### 03. Problem statement")

    st.markdown("""
    A random walk may repeatedly explore the same states.
    We investigate how uniform random selection compares
    with entropy-based adaptive selection when exploring
    historical COVID intensity transitions.
    """)

    # -------------------------------------------------
    # GRAPH
    # -------------------------------------------------

    st.markdown("### 04. Historical transition graph")

    st.plotly_chart(
        create_covid_graph_figure(graph),
        use_container_width=True
    )

    st.caption(
        "Numbers on edges represent observed historical "
        "transition counts. Edge thickness represents "
        "the relative number of observations."
    )

    # -------------------------------------------------
    # INTENSITY THRESHOLDS
    # -------------------------------------------------

    thresholds = dataset_info["Thresholds"]

    threshold_df = pd.DataFrame({
        "Intensity State": [
            "Low",
            "Moderate",
            "High",
            "Very High"
        ],
        "Daily new cases": [
            f"0 – {thresholds['Q1']:g}",
            f"{thresholds['Q1']:g} – {thresholds['Median']:g}",
            f"{thresholds['Median']:g} – {thresholds['Q3']:g}",
            f"Above {thresholds['Q3']:g}"
        ]
    })

    st.markdown("#### Dataset-derived intensity thresholds")

    st.dataframe(
        threshold_df,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Thresholds are calculated from the first, second "
        "and third quartiles of the observed daily new cases."
    )

    # -------------------------------------------------
    # SIMULATION SETTINGS
    # -------------------------------------------------

    st.markdown("### 05. Simulation settings")

    defaults = get_covid_defaults()

    st.markdown(
        "Change the settings below and run both algorithms "
        "on the same historical transition graph."
    )

    if "covid_start" not in st.session_state:
        st.session_state.covid_start = defaults["start_state"]

    if "covid_steps" not in st.session_state:
        st.session_state.covid_steps = defaults["steps"]

    if "covid_rho" not in st.session_state:
        st.session_state.covid_rho = defaults["rho"]

    if "covid_eta" not in st.session_state:
        st.session_state.covid_eta = defaults["eta"]

    if "covid_temperature" not in st.session_state:
        st.session_state.covid_temperature = defaults[
            "initial_temperature"
        ]

    col1, col2 = st.columns(2)

    with col1:

        st.selectbox(
            "Starting intensity state",
            ["Low", "Moderate", "High", "Very High"],
            key="covid_start"
        )

        st.slider(
            "Number of simulation steps",
            min_value=10,
            max_value=1000,
            step=10,
            key="covid_steps"
        )

        st.slider(
            "Initial EBW temperature",
            min_value=0.1,
            max_value=5.0,
            step=0.1,
            key="covid_temperature"
        )

    with col2:

        st.slider(
            "Entropy target factor (rho)",
            min_value=0.0,
            max_value=1.0,
            step=0.05,
            key="covid_rho"
        )

        st.slider(
            "Temperature adaptation rate (eta)",
            min_value=0.0,
            max_value=1.0,
            step=0.05,
            key="covid_eta"
        )

        st.markdown("""
        <div class="panel">
        <b>SRW:</b> Uniform probability selection.<br><br>
        <b>EBW:</b> Adaptive probability selection
        using entropy and exploration history.
        </div>
        """, unsafe_allow_html=True)

    run_col, reset_col = st.columns(2)

    with run_col:

        run_simulation = st.button(
            "▶ RUN SIMULATION",
            use_container_width=True
        )

    with reset_col:

        st.button(
            "↺ RESET TO DEFAULT",
            use_container_width=True,
            on_click=reset_covid
        )

    # -------------------------------------------------
    # RUN BOTH ALGORITHMS
    # -------------------------------------------------

    if run_simulation:
        try:

            validate_covid_start(
                graph,
                st.session_state.covid_start
            )

            with st.spinner(
                "Running SRW and EBW simulations..."
            ):

                result = compare_algorithms(
                    graph=graph,
                    start_node=st.session_state.covid_start,
                    steps=st.session_state.covid_steps,
                    rho=st.session_state.covid_rho,
                    eta=st.session_state.covid_eta,
                    initial_temperature=(
                        st.session_state.covid_temperature
                    ),
                    seed=42
                )
                st.session_state.covid_result = result
            
                # Run 100 repeated experiments for statistical comparison
                repeated_result = compare_repeated_experiments(
                    graph=graph,
                    start_node=st.session_state.covid_start,
                    steps=st.session_state.covid_steps,
                    experiments=100,
                    rho=st.session_state.covid_rho,
                    eta=st.session_state.covid_eta,
                    initial_temperature=st.session_state.covid_temperature,
                    base_seed=42
                )

                # Store repeated experiment results separately
                st.session_state.covid_repeated_result = repeated_result


        except Exception as error:
            st.error(
                f"Simulation error: {error}"
            )
    # -------------------------------------------------
    # DISPLAY RESULTS
    # -------------------------------------------------

    result = st.session_state.covid_result

    if result is not None:

        st.divider()

        st.markdown("## 06. Simulation results")

        st.success(
            "Both algorithms completed their simulations."
        )

        # METRICS TABLE

        srw_metrics = result["SRW"]["metrics"]
        ebw_metrics = result["EBW"]["metrics"]

        comparison_df = pd.DataFrame({
            "Metric": list(srw_metrics.keys()),
            "SRW": list(srw_metrics.values()),
            "EBW": [
                ebw_metrics[key]
                for key in srw_metrics.keys()
            ]
        })

        st.markdown("### SRW vs EBW performance")

        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True
        )

        # REPEATED-EXPERIMENT STATISTICAL DASHBOARD
        repeated = st.session_state.covid_repeated_result

        if repeated is not None:
            st.divider()
            st.markdown("### 100-experiment statistical analysis")
            st.caption(
                "Each experiment uses the same graph, start state and step "
                "count for SRW and EBW, with paired seeds."
            )

            summary = repeated["Summary"]
            summary_rows = []

            for metric in summary["SRW"]:
                summary_rows.append({
                    "Metric": metric,
                    "SRW Mean": summary["SRW"][metric]["Mean"],
                    "SRW Std. Dev.": summary["SRW"][metric]["Standard Deviation"],
                    "EBW Mean": summary["EBW"][metric]["Mean"],
                    "EBW Std. Dev.": summary["EBW"][metric]["Standard Deviation"]
                })

            summary_df = pd.DataFrame(summary_rows)
            st.markdown("#### Average performance and variability")
            st.dataframe(
                summary_df,
                use_container_width=True,
                hide_index=True
            )

            coverage_col1, coverage_col2 = st.columns(2)
            coverage_col1.metric(
                "SRW average node coverage",
                f"{summary['SRW']['Node Coverage (%)']['Mean']:.2f}%"
            )
            coverage_col2.metric(
                "EBW average node coverage",
                f"{summary['EBW']['Node Coverage (%)']['Mean']:.2f}%"
            )

            revisit_col1, revisit_col2 = st.columns(2)
            revisit_col1.metric(
                "SRW average revisit rate",
                f"{summary['SRW']['Revisit Rate (%)']['Mean']:.2f}%"
            )
            revisit_col2.metric(
                "EBW average revisit rate",
                f"{summary['EBW']['Revisit Rate (%)']['Mean']:.2f}%"
            )

            st.markdown("#### Experiment variability")
            variability_df = pd.DataFrame([
                {
                    "Algorithm": algorithm,
                    "Node coverage SD (%)": summary[algorithm]["Node Coverage (%)"]["Standard Deviation"],
                    "Revisit rate SD (%)": summary[algorithm]["Revisit Rate (%)"]["Standard Deviation"],
                    "Mean entropy SD": summary[algorithm]["Mean Transition Entropy"]["Standard Deviation"]
                }
                for algorithm in ("SRW", "EBW")
            ])
            st.dataframe(
                variability_df,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "Download 100-experiment summary CSV",
                data=summary_df.to_csv(index=False).encode("utf-8"),
                file_name="entropy_lab_100_experiment_summary.csv",
                mime="text/csv"
            )

            individual_rows = []
            for run in repeated["Individual Results"]:
                for algorithm in ("SRW", "EBW"):
                    row = {
                        "Experiment": run["Experiment"],
                        "Seed": run["Seed"],
                        "Algorithm": algorithm
                    }
                    row.update(run[algorithm])
                    individual_rows.append(row)

            individual_df = pd.DataFrame(individual_rows)
            st.download_button(
                "Download individual experiment results CSV",
                data=individual_df.to_csv(index=False).encode("utf-8"),
                file_name="entropy_lab_individual_experiments.csv",
                mime="text/csv"
            )

            st.info(
                "Mean values summarize average performance. Standard "
                "deviation shows variation across runs. No algorithm is "
                "declared the winner automatically; interpret metrics "
                "according to the exploration objective."
            )

        # COVERAGE

        st.markdown("### Exploration coverage")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "SRW node coverage",
            f"{srw_metrics['Node Coverage (%)']}%"
        )

        c2.metric(
            "EBW node coverage",
            f"{ebw_metrics['Node Coverage (%)']}%"
        )

        c3.metric(
            "SRW edge coverage",
            f"{srw_metrics['Edge Coverage (%)']}%"
        )

        c4.metric(
            "EBW edge coverage",
            f"{ebw_metrics['Edge Coverage (%)']}%"
        )

        # PATHS

        st.markdown("### 07. Exploration paths")

        path_col1, path_col2 = st.columns(2)

        with path_col1:

            st.markdown("#### SRW path")

            st.plotly_chart(
                create_path_figure(
                    result["SRW"]["path"],
                    "Simple Random Walk"
                ),
                use_container_width=True
            )

        with path_col2:

            st.markdown("#### EBW path")

            st.plotly_chart(
                create_path_figure(
                    result["EBW"]["path"],
                    "Entropy-Based Walk"
                ),
                use_container_width=True
            )

        # ENTROPY

        st.markdown("### 08. Entropy comparison")

        st.plotly_chart(
            create_entropy_figure(result),
            use_container_width=True
        )

        # TEMPERATURE

        st.markdown("### EBW temperature adaptation")

        st.plotly_chart(
            create_temperature_figure(result),
            use_container_width=True
        )

        # PATH DETAILS

        with st.expander("View complete SRW and EBW paths"):

            st.write("**SRW path:**")

            st.write(
                " → ".join(result["SRW"]["path"])
            )

            st.write("**EBW path:**")

            st.write(
                " → ".join(result["EBW"]["path"])
            )

        # PROBABILITY DETAILS

        with st.expander("View transition probabilities"):

            st.write("**SRW probabilities**")

            st.dataframe(
                pd.DataFrame(
                    result["SRW"]["probabilities"]
                ),
                use_container_width=True
            )

            st.write("**EBW probabilities**")

            st.dataframe(
                pd.DataFrame(
                    result["EBW"]["probabilities"]
                ),
                use_container_width=True
            )

        # TRANSITION MATRIX

        st.markdown("### 09. Historical transition matrix")

        st.dataframe(
            get_covid_transition_matrix(graph),
            use_container_width=True
        )

        # INTERPRETATION

        st.markdown("### 10. Result interpretation")

        st.markdown("""
        The comparison measures how the two algorithms explore
        the same directed historical transition graph.

        Higher node or edge coverage means more of the graph
        was explored. Revisit rate measures how often the walk
        returned to already visited nodes.

        Mean transition entropy measures uncertainty in the
        probability distributions used during the walk.

        A lower or higher entropy value is not automatically
        better. Its interpretation depends on the exploration
        objective and the other performance metrics.
        """)

        st.info(
            "These are graph exploration experiments using "
            "historical COVID observations. They are not "
            "predictions of future infections or actual "
            "geographical transmission routes."
        )

    else:

        st.info(
            "Change your settings and click RUN SIMULATION "
            "to see the SRW and EBW comparison."
        )

    # -------------------------------------------------
    # PROCESS
    # -------------------------------------------------

    st.markdown("### 11. Process")

    st.markdown("""
    1. Load the historical Bengaluru Urban COVID dataset.
    2. Calculate daily new cases from cumulative confirmed cases.
    3. Classify daily observations using dataset quartiles.
    4. Count transitions between consecutive intensity states.
    5. Construct a directed graph using those observations.
    6. Run SRW and EBW using the same graph and settings.
    7. Compare coverage, revisit rate, entropy and execution time.
    """)

    st.markdown("### 12. Dataset source")

    st.markdown("""
    **Dataset used:** COVID19-India district-level historical data.

    **Local dataset file:**  
    `datasets/covid/covid_districts.csv`

    **Selected records:** Karnataka → Bengaluru Urban.

    The dataset contains district-level observations, not
    Bengaluru ward-level or neighbourhood-level records.
    """)

    st.html("""
    <div class="footer">
        ENTROPY LAB | COVID-19 HISTORICAL DATA SIMULATION
    </div>
    """)

# ============================================================
# WEATHER PATTERN SIMULATION
# ============================================================

if st.session_state.page == "weather":

    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    st.button(
        "← BACK TO APPLICATIONS",
        on_click=lambda: setattr(
            st.session_state, "page", "introduction"
        )
    )

    st.markdown("""
    <div class="app-heading">
        WEATHER PATTERN SIMULATION
    </div>
    <div class="app-subheading">
        Comparing SRW and EBW using historical Bengaluru
        temperature observations
    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # LOAD WEATHER ENVIRONMENT
    # --------------------------------------------------------

    try:
        weather_graph, weather_df = create_weather_environment()
        weather_info = get_weather_information()
        weather_matrix = get_weather_transition_matrix()

    except Exception as error:
        st.error(f"Unable to load weather dataset: {error}")
        st.stop()

    # --------------------------------------------------------
    # DATASET INFORMATION
    # --------------------------------------------------------

    st.markdown("## 01. Historical weather dataset")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Valid observations",
        f"{weather_info['observations']:,}"
    )

    col2.metric(
        "Weather states",
        len(weather_info["states"])
    )

    col3.metric(
        "Historical transitions",
        f"{weather_info['transition_count']:,}"
    )

    st.info(
        "Dataset: Bengaluru Daily Temperature Data, "
        f"{weather_info['start_date']} to "
        f"{weather_info['end_date']}. "
        "The four states are classified using daily mean temperature."
    )

    # --------------------------------------------------------
    # WEATHER STATE EXPLANATION
    # --------------------------------------------------------

    st.markdown("## 02. Weather state classification")

    state_table = pd.DataFrame({
        "Weather State": [
            "Cool", "Moderate", "Warm", "Hot"
        ],
        "Mean Temperature Range": [
            "Below 20°C",
            "20°C to below 25°C",
            "25°C to below 30°C",
            "30°C and above"
        ]
    })

    st.dataframe(
        state_table,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Daily mean temperature = (Temperature Maximum + "
        "Temperature Minimum) / 2."
    )

    # --------------------------------------------------------
    # WEATHER GRAPH
    # --------------------------------------------------------

    st.markdown("## 03. Historical weather transition graph")

    positions = nx.spring_layout(
        weather_graph,
        seed=42,
        k=1.5
    )

    edge_x = []
    edge_y = []

    for source, target in weather_graph.edges():
        x0, y0 = positions[source]
        x1, y1 = positions[target]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    fig_graph = go.Figure()

    fig_graph.add_trace(go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=1.5, color="#36D6E7"),
        hoverinfo="none"
    ))

    node_x = [positions[node][0] for node in weather_graph.nodes()]
    node_y = [positions[node][1] for node in weather_graph.nodes()]

    fig_graph.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=list(weather_graph.nodes()),
        textposition="bottom center",
        marker=dict(
            size=35,
            color="#13BFD0",
            line=dict(width=2, color="white")
        ),
        hovertemplate="%{text}<extra></extra>"
    ))

    fig_graph.update_layout(
        height=430,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_graph,
        use_container_width=True
    )

    # --------------------------------------------------------
    # TRANSITION MATRIX
    # --------------------------------------------------------

    st.markdown("## 04. Historical transition matrix")

    st.dataframe(
        weather_matrix,
        use_container_width=True
    )

    # --------------------------------------------------------
    # SIMULATION SETTINGS
    # --------------------------------------------------------

    st.markdown("## 05. Simulation settings")

    defaults = get_weather_defaults()

    col1, col2 = st.columns(2)

    with col1:
        weather_start = st.selectbox(
            "Starting weather state",
            options=list(weather_graph.nodes()),
            index=list(weather_graph.nodes()).index(
                defaults["start_state"]
            ),
            key="weather_start"
        )

        weather_steps = st.slider(
            "Simulation steps",
            min_value=10,
            max_value=500,
            value=defaults["steps"],
            step=10,
            key="weather_steps"
        )

        weather_rho = st.slider(
            "Entropy target (rho)",
            min_value=0.10,
            max_value=1.00,
            value=float(defaults["rho"]),
            step=0.05,
            key="weather_rho"
        )

    with col2:
        weather_eta = st.slider(
            "Adaptation rate (eta)",
            min_value=0.01,
            max_value=0.50,
            value=float(defaults["eta"]),
            step=0.01,
            key="weather_eta"
        )

        weather_temperature = st.slider(
            "Initial EBW temperature",
            min_value=0.10,
            max_value=5.00,
            value=float(defaults["initial_temperature"]),
            step=0.10,
            key="weather_temperature"
        )

        weather_experiments = st.selectbox(
            "Repeated experiments",
            options=[10, 25, 50, 100],
            index=3,
            key="weather_experiments"
        )

    # --------------------------------------------------------
    # SESSION STATE
    # --------------------------------------------------------

    if "weather_result" not in st.session_state:
        st.session_state.weather_result = None

    if "weather_repeated_result" not in st.session_state:
        st.session_state.weather_repeated_result = None

    # --------------------------------------------------------
    # RUN AND RESET BUTTONS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        run_weather = st.button(
            "RUN WEATHER SIMULATION",
            use_container_width=True,
            type="primary"
        )

    with col2:
        reset_weather = st.button(
            "RESET SIMULATION",
            use_container_width=True
        )

    if reset_weather:
        st.session_state.weather_result = None
        st.session_state.weather_repeated_result = None
        st.rerun()

    if run_weather:

        if not validate_weather_start(
            weather_graph, weather_start
        ):
            st.error(
                "The selected starting state has no outgoing transitions."
            )

        else:
            try:
                with st.spinner(
                    "Running SRW, EBW and repeated experiments..."
                ):

                    result = compare_algorithms(
                        weather_graph,
                        weather_start,
                        weather_steps,
                        rho=weather_rho,
                        eta=weather_eta,
                        initial_temperature=weather_temperature
                    )

                    repeated = compare_repeated_experiments(
                        weather_graph,
                        weather_start,
                        weather_steps,
                        experiments=weather_experiments,
                        rho=weather_rho,
                        eta=weather_eta,
                        initial_temperature=weather_temperature
                    )

                    st.session_state.weather_result = result
                    st.session_state.weather_repeated_result = repeated

                st.success(
                    "Both algorithms completed their simulations."
                )

            except Exception as error:
                st.error(f"Simulation failed: {error}")

    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    result = st.session_state.weather_result
    repeated = st.session_state.weather_repeated_result

    if result is not None:

        st.markdown("## 06. Simulation results")

        srw = result["SRW"]
        ebw = result["EBW"]

        srw_metrics = srw["metrics"]
        ebw_metrics = ebw["metrics"]

        performance = pd.DataFrame({
            "Metric": list(srw_metrics.keys()),
            "SRW": list(srw_metrics.values()),
            "EBW": list(ebw_metrics.values())
        })

        st.markdown("### SRW vs EBW performance")

        st.dataframe(
            performance,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # COVERAGE
        # ----------------------------------------------------

        st.markdown("## 07. Exploration coverage")

        c1, c2 = st.columns(2)

        c1.metric(
            "SRW node coverage",
            f"{srw_metrics['Node Coverage (%)']:.2f}%"
        )

        c2.metric(
            "EBW node coverage",
            f"{ebw_metrics['Node Coverage (%)']:.2f}%"
        )

        # ----------------------------------------------------
        # PATHS
        # ----------------------------------------------------

        st.markdown("## 08. Exploration paths")

        c1, c2 = st.columns(2)

        c1.markdown("**Simple Random Walk (SRW)**")
        c1.write(" → ".join(map(str, srw["path"])))

        c2.markdown("**Entropy-Based Walk (EBW)**")
        c2.write(" → ".join(map(str, ebw["path"])))

        # ----------------------------------------------------
        # ENTROPY COMPARISON
        # ----------------------------------------------------

        st.markdown("## 09. Entropy comparison")

        entropy_fig = go.Figure()

        entropy_fig.add_trace(go.Scatter(
            y=srw["entropy"],
            mode="lines",
            name="SRW"
        ))

        entropy_fig.add_trace(go.Scatter(
            y=ebw["entropy"],
            mode="lines",
            name="EBW"
        ))

        entropy_fig.update_layout(
            title="Transition Entropy Comparison",
            xaxis_title="Simulation Step",
            yaxis_title="Shannon Entropy",
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(
            entropy_fig,
            use_container_width=True
        )

        # ----------------------------------------------------
        # EBW TEMPERATURE
        # ----------------------------------------------------

        st.markdown("### EBW temperature adaptation")

        temperature_fig = go.Figure()

        temperature_fig.add_trace(go.Scatter(
            y=ebw["temperature"],
            mode="lines",
            name="EBW Temperature",
            line=dict(color="#F5A623")
        ))

        temperature_fig.update_layout(
            title="Adaptive Temperature",
            xaxis_title="Simulation Step",
            yaxis_title="Temperature",
            template="plotly_dark",
            height=350
        )

        st.plotly_chart(
            temperature_fig,
            use_container_width=True
        )

        # ----------------------------------------------------
        # REPEATED EXPERIMENTS
        # ----------------------------------------------------

        if repeated is not None:

            st.markdown(
                f"## 10. {weather_experiments}-experiment statistical analysis"
            )

            summary = repeated["Summary"]
            summary_rows = []

            for metric in summary["SRW"]:
                summary_rows.append({
                    "Metric": metric,
                    "SRW Mean": summary["SRW"][metric]["Mean"],
                    "SRW Std. Dev.": summary["SRW"][metric]["Standard Deviation"],
                    "EBW Mean": summary["EBW"][metric]["Mean"],
                    "EBW Std. Dev.": summary["EBW"][metric]["Standard Deviation"]
                })

            summary_df = pd.DataFrame(summary_rows)
            st.dataframe(
                            summary_df,
                            use_container_width=True,
                            hide_index=True
                        )

            st.download_button(
                "DOWNLOAD WEATHER STATISTICAL SUMMARY CSV",
                data=summary_df.to_csv(index=False),
                file_name="weather_statistical_summary.csv",
                mime="text/csv"
            )

            # ------------------------------------------------
            # EXPERIMENT INTERPRETATION
            # ------------------------------------------------

            st.info(
                "The statistical results summarize repeated "
                "experiments on the same historical weather graph. "
                "Neither algorithm is automatically declared the winner. "
                "Interpret coverage, revisits, entropy and execution time "
                "together."
            )

    # --------------------------------------------------------
    # METHODOLOGY
    # --------------------------------------------------------

    st.markdown("## 11. Process")

    st.markdown("""
    1. Load the historical Bengaluru temperature dataset.
    2. Clean missing and invalid temperature observations.
    3. Calculate daily mean temperature.
    4. Classify observations into four temperature states.
    5. Count consecutive historical state transitions.
    6. Construct a directed weather transition graph.
    7. Run SRW and EBW using the same graph and settings.
    8. Compare exploration and statistical performance.
    """)

    # --------------------------------------------------------
    # DATASET SOURCE
    # --------------------------------------------------------

    st.markdown("## 12. Dataset source")

    st.markdown("""
    **Dataset:** Bengaluru Daily Temperature Data 1951–2024

    **Source:** India Meteorological Department dataset hosted on OpenCity.

    **Local file:** `datasets/weather/bengaluru_weather.csv`

    **Variables:** Date, Rain, Temp Max and Temp Min.

    **Important limitation:** This experiment studies transitions
    between temperature-based states. It does not predict future
    weather or model geographical weather movement.
    """)

    st.markdown("""
    <div class="footer">
        ENTROPY LAB | BENGALURU WEATHER PATTERN SIMULATION
    </div>
    """, unsafe_allow_html=True)



# ============================================================
# WILDLIFE AND BIODIVERSITY SIMULATION
# ============================================================

if st.session_state.page == "wildlife":

    st.button(
        "← BACK TO APPLICATIONS",
        on_click=lambda: setattr(st.session_state, "page", "introduction")
    )

    st.markdown("""
    <div class="app-heading">WILDLIFE AND BIODIVERSITY SIMULATION</div>
    <div class="app-subheading">
        Comparing SRW and EBW using real bird observations from the
        Mysuru City Bird Atlas
    </div>
    """, unsafe_allow_html=True)

    try:
        wildlife_graph = create_wildlife_environment()
        wildlife_info = get_wildlife_information(wildlife_graph)
        wildlife_graph_summary = get_wildlife_graph_summary(wildlife_graph)
    except Exception as error:
        st.error(f"Unable to load the wildlife dataset or graph: {error}")
        st.info(
            "Check that datasets/wildlife/MBA+final+dataset.csv exists "
            "and that simulations/wildlife.py is present."
        )
        st.stop()

    # Dataset overview
    st.markdown("## 01. About the dataset")
    st.markdown(
        "This application uses the Mysuru City Bird Atlas dataset. "
        "Survey observations are associated with atlas grid cells. "
        "The graph represents grid cells as nodes and observed spatial "
        "connections between grids as edges."
    )

    info_cols = st.columns(4)
    info_cols[0].metric(
        "Observation records",
        f"{wildlife_info.get('observation_records', 0):,}"
    )
    info_cols[1].metric(
        "Unique bird species",
        f"{wildlife_info.get('unique_species', 0):,}"
    )
    info_cols[2].metric(
        "Birds observed",
        f"{wildlife_info.get('total_birds', 0):,.0f}"
    )
    info_cols[3].metric(
        "Atlas grids",
        f"{wildlife_info.get('total_grids', wildlife_graph.number_of_nodes()):,}"
    )

    st.caption(
        f"Dataset: {wildlife_info.get('dataset', 'Mysuru City Bird Atlas')} | "
        f"Survey years: {', '.join(map(str, wildlife_info.get('years', [])))} | "
        f"Months: {', '.join(map(str, wildlife_info.get('months', [])))}"
    )
    st.caption(
        "Local file: datasets/wildlife/MBA+final+dataset.csv"
    )

    st.markdown("## 02. Problem statement")
    st.markdown("""
    Bird surveys are collected across multiple atlas grid cells. We use
    the dataset-derived grid graph to compare how two random-walk methods
    explore connected survey locations.

    SRW selects uniformly among available neighbouring grids. EBW adapts
    its selection probabilities using exploration history and entropy.
    This is a graph-exploration experiment, not a prediction of bird
    migration, abundance, or real-time animal movement.
    """)

    st.markdown("## 03. Wildlife grid graph")
    graph_nodes = list(wildlife_graph.nodes())
    graph_edges = wildlife_graph.number_of_edges()
    graph_summary_cols = st.columns(3)
    graph_summary_cols[0].metric("Graph nodes", wildlife_graph.number_of_nodes())
    graph_summary_cols[1].metric("Graph edges", graph_edges)
    graph_summary_cols[2].metric(
        "Connected components",
        wildlife_graph_summary.get(
            "components",
            nx.number_connected_components(wildlife_graph)
            if not wildlife_graph.is_directed()
            else nx.number_weakly_connected_components(wildlife_graph)
        )
    )

    # Display a readable spatial graph
    positions = nx.spring_layout(wildlife_graph, seed=42, k=0.8)
    edge_x, edge_y = [], []
    for source, target in wildlife_graph.edges():
        x0, y0 = positions[source]
        x1, y1 = positions[target]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    node_x = [positions[node][0] for node in graph_nodes]
    node_y = [positions[node][1] for node in graph_nodes]
    graph_fig = go.Figure()
    graph_fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y, mode="lines",
        line=dict(width=1.2, color="#36D6E7"),
        hoverinfo="none", showlegend=False
    ))
    graph_fig.add_trace(go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=[str(node) for node in graph_nodes],
        textposition="top center",
        marker=dict(size=17, color="#13BFD0",
                    line=dict(width=1, color="white")),
        hovertemplate="Atlas grid: %{text}<extra></extra>",
        showlegend=False
    ))
    graph_fig.update_layout(
        title="Mysuru City Bird Atlas grid connectivity",
        height=520, template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        margin=dict(l=20, r=20, t=55, b=20)
    )
    st.plotly_chart(graph_fig, use_container_width=True)
    st.caption(
        "This force-directed layout visualizes graph connectivity; "
        "it is not a geographic map. Grid IDs represent atlas survey grids."
    )

    # Optional grid summary table, if the module provides it
    if isinstance(wildlife_graph_summary, dict):
        with st.expander("View graph summary"):
            st.json(wildlife_graph_summary)

    st.markdown("## 04. Simulation settings")
    default_start = graph_nodes[0]
    wildlife_start = st.selectbox(
        "Starting atlas grid",
        options=graph_nodes,
        index=0,
        format_func=lambda value: f"Grid {value}",
        key="wildlife_start"
    )
    wildlife_steps = st.slider(
        "Simulation steps", 10, 500, 100, 10,
        key="wildlife_steps"
    )
    wildlife_rho = st.slider(
        "Entropy target (rho)", 0.10, 1.00, 0.75, 0.05,
        key="wildlife_rho"
    )
    wildlife_eta = st.slider(
        "Temperature adaptation rate (eta)", 0.01, 0.50, 0.15, 0.01,
        key="wildlife_eta"
    )
    wildlife_temperature = st.slider(
        "Initial EBW temperature", 0.10, 5.00, 1.00, 0.10,
        key="wildlife_temperature"
    )
    wildlife_experiments = st.selectbox(
        "Repeated experiments",
        options=[10, 25, 50, 100],
        index=3,
        key="wildlife_experiments"
    )

    if "wildlife_result" not in st.session_state:
        st.session_state.wildlife_result = None
    if "wildlife_repeated_result" not in st.session_state:
        st.session_state.wildlife_repeated_result = None

    run_col, reset_col = st.columns(2)
    with run_col:
        run_wildlife = st.button(
            "▶ RUN WILDLIFE SIMULATION",
            use_container_width=True,
            type="primary"
        )
    with reset_col:
        reset_wildlife = st.button(
            "↺ RESET SIMULATION",
            use_container_width=True
        )

    if reset_wildlife:
        st.session_state.wildlife_result = None
        st.session_state.wildlife_repeated_result = None
        st.rerun()

    if run_wildlife:
        if wildlife_graph.out_degree(wildlife_start) == 0 if wildlife_graph.is_directed() else wildlife_graph.degree(wildlife_start) == 0:
            st.error("The selected grid has no available neighbouring grid.")
        else:
            try:
                with st.spinner("Running SRW, EBW and repeated experiments..."):
                    result = compare_algorithms(
                        wildlife_graph,
                        wildlife_start,
                        wildlife_steps,
                        rho=wildlife_rho,
                        eta=wildlife_eta,
                        initial_temperature=wildlife_temperature,
                        seed=42
                    )
                    repeated = compare_repeated_experiments(
                        wildlife_graph,
                        wildlife_start,
                        wildlife_steps,
                        experiments=wildlife_experiments,
                        rho=wildlife_rho,
                        eta=wildlife_eta,
                        initial_temperature=wildlife_temperature,
                        base_seed=42
                    )
                    st.session_state.wildlife_result = result
                    st.session_state.wildlife_repeated_result = repeated
                st.success("Both algorithms completed their simulations.")
            except Exception as error:
                st.error(f"Wildlife simulation failed: {error}")

    result = st.session_state.wildlife_result
    repeated = st.session_state.wildlife_repeated_result

    if result is not None:
        st.markdown("## 05. Single-run results")
        srw = result["SRW"]
        ebw = result["EBW"]
        srw_metrics = srw["metrics"]
        ebw_metrics = ebw["metrics"]

        performance_df = pd.DataFrame({
            "Metric": list(srw_metrics.keys()),
            "SRW": [srw_metrics[key] for key in srw_metrics],
            "EBW": [ebw_metrics[key] for key in srw_metrics]
        })
        st.dataframe(performance_df, use_container_width=True, hide_index=True)

        coverage_cols = st.columns(4)
        coverage_cols[0].metric(
            "SRW node coverage", f"{srw_metrics['Node Coverage (%)']:.2f}%"
        )
        coverage_cols[1].metric(
            "EBW node coverage", f"{ebw_metrics['Node Coverage (%)']:.2f}%"
        )
        coverage_cols[2].metric(
            "SRW edge coverage", f"{srw_metrics['Edge Coverage (%)']:.2f}%"
        )
        coverage_cols[3].metric(
            "EBW edge coverage", f"{ebw_metrics['Edge Coverage (%)']:.2f}%"
        )

        st.markdown("## 06. Exploration paths")
        path_cols = st.columns(2)
        path_cols[0].markdown("**SRW path**")
        path_cols[0].write(" → ".join(map(str, srw["path"])))
        path_cols[1].markdown("**EBW path**")
        path_cols[1].write(" → ".join(map(str, ebw["path"])))

        st.markdown("## 07. Entropy comparison")
        entropy_fig = go.Figure()
        entropy_fig.add_trace(go.Scatter(
            y=srw["entropy"], mode="lines", name="SRW",
            line=dict(color="#65b9ff", width=2)
        ))
        entropy_fig.add_trace(go.Scatter(
            y=ebw["entropy"], mode="lines", name="EBW",
            line=dict(color="#4de0c1", width=2)
        ))
        entropy_fig.update_layout(
            title="Transition Entropy Comparison",
            xaxis_title="Simulation step", yaxis_title="Shannon entropy",
            template="plotly_dark", height=370
        )
        st.plotly_chart(entropy_fig, use_container_width=True)

        st.markdown("## 08. EBW temperature adaptation")
        temp_fig = go.Figure()
        temp_fig.add_trace(go.Scatter(
            y=ebw["temperature"], mode="lines", name="EBW temperature",
            line=dict(color="#ffbd59", width=2)
        ))
        temp_fig.update_layout(
            title="Adaptive Temperature",
            xaxis_title="Simulation step", yaxis_title="Temperature",
            template="plotly_dark", height=330
        )
        st.plotly_chart(temp_fig, use_container_width=True)

        if repeated is not None:
            st.markdown(
                f"## 09. {wildlife_experiments}-experiment statistical analysis"
            )
            summary = repeated["Summary"]
            rows = []
            for metric in summary["SRW"]:
                rows.append({
                    "Metric": metric,
                    "SRW Mean": summary["SRW"][metric]["Mean"],
                    "SRW Std. Dev.": summary["SRW"][metric]["Standard Deviation"],
                    "EBW Mean": summary["EBW"][metric]["Mean"],
                    "EBW Std. Dev.": summary["EBW"][metric]["Standard Deviation"]
                })
            summary_df = pd.DataFrame(rows)
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
            st.download_button(
                "DOWNLOAD WILDLIFE SUMMARY CSV",
                data=summary_df.to_csv(index=False).encode("utf-8"),
                file_name="wildlife_statistical_summary.csv",
                mime="text/csv"
            )

            individual_rows = []
            for experiment in repeated["Individual Results"]:
                for algorithm in ("SRW", "EBW"):
                    row = {
                        "Experiment": experiment["Experiment"],
                        "Seed": experiment["Seed"],
                        "Algorithm": algorithm
                    }
                    row.update(experiment[algorithm])
                    individual_rows.append(row)
            individual_df = pd.DataFrame(individual_rows)
            st.download_button(
                "DOWNLOAD INDIVIDUAL EXPERIMENTS CSV",
                data=individual_df.to_csv(index=False).encode("utf-8"),
                file_name="wildlife_individual_experiments.csv",
                mime="text/csv"
            )
            st.info(
                "Mean values summarize average performance; standard "
                "deviation measures variation across runs. Neither method "
                "is assumed to be the winner."
            )

        st.markdown("## 10. Result interpretation")
        st.markdown("""
        Node coverage measures how many atlas grid nodes were visited.
        Edge coverage measures how many graph connections were traversed.
        Revisit rate measures repeated visits to previously visited nodes.
        Transition entropy describes uncertainty in the probability
        distribution used at each step.

        Higher coverage may indicate broader graph exploration, but it does
        not prove higher bird abundance or better biodiversity. These are
        algorithmic exploration results on a graph constructed from the
        atlas dataset.
        """)

    else:
        st.info("Choose the settings and click RUN WILDLIFE SIMULATION.")

    st.markdown("## 11. Process")
    st.markdown("""
    1. Load the Mysuru City Bird Atlas observation CSV.
    2. Associate survey observations with atlas grid cells.
    3. Construct the dataset-derived grid connectivity graph.
    4. Select a starting grid and simulation settings.
    5. Run SRW and EBW on the same graph.
    6. Repeat paired experiments and summarize the metrics.
    7. Compare node coverage, edge coverage, revisits and entropy.
    """)

    st.markdown("## 12. Dataset source")
    st.markdown("""
    **Dataset:** Mysuru City Bird Atlas, based on bird survey observations
    from 2014–2016.

    **Local file:** `datasets/wildlife/MBA+final+dataset.csv`

    **Dataset documentation:** `datasets/wildlife/README_for_MBA+final+dataset.TXT`

    The graph is a representation of atlas grid connectivity. The walk
    explores this graph; it does not model actual bird movement.
    """)

    st.markdown("""
    <div class="footer">
        ENTROPY LAB | MYSURU CITY BIRD ATLAS SIMULATION
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# COMPUTER NETWORK SIMULATION
# ============================================================

if st.session_state.page == "network":

    st.button(
        "← BACK TO APPLICATIONS",
        on_click=lambda: setattr(st.session_state, "page", "introduction")
    )

    st.markdown("""
    <div class="app-heading">COMPUTER NETWORK SIMULATION</div>
    <div class="app-subheading">
        Comparing SRW and EBW using the Stanford SNAP AS-733 Internet topology
    </div>
    """, unsafe_allow_html=True)

    try:
        network_graph = create_network_environment()
        network_info = get_network_information(network_graph)
        network_summary = get_network_graph_summary(network_graph)
        network_dataset_info = get_network_dataset_information()
    except Exception as error:
        st.error(f"Unable to load the network dataset: {error}")
        st.info(
            "Check that datasets/network/as20000102.txt exists "
            "and simulations/network.py is present."
        )
        st.stop()

    # 01. Dataset overview
    st.markdown("## 01. About the dataset")
    st.markdown("""
    This application uses the Stanford SNAP AS-733 Internet autonomous-system
    topology snapshot. Each node represents an Autonomous System (AS), and
    each undirected edge represents a recorded connection between two systems.

    SRW and EBW explore the same real network graph. This experiment evaluates
    graph exploration; it does not simulate live internet traffic, packet
    routing, outages, or current network conditions.
    """)

    info_cols = st.columns(4)
    info_cols[0].metric("Autonomous systems (nodes)", f"{network_info['nodes']:,}")
    info_cols[1].metric("Connections (edges)", f"{network_info['edges']:,}")
    info_cols[2].metric("Average degree", f"{network_info['average_degree']:.2f}")
    info_cols[3].metric("Connected components", f"{network_info['components']:,}")

    st.caption(
        f"Dataset: {network_info['dataset']} | "
        f"File: datasets/network/{network_info['filename']} | "
        f"Largest component: {network_info['largest_component_nodes']:,} "
        f"nodes ({network_info['largest_component_percentage']:.2f}%)"
    )

    st.markdown("## 02. Problem statement")
    st.markdown("""
    Large communication networks contain thousands of interconnected systems.
    A random walk can repeatedly visit already explored systems. We compare
    uniform neighbour selection (SRW) with entropy-based adaptive selection
    (EBW) to measure how effectively each method explores nodes and links
    in the observed topology.
    """)

    # 03. Network statistics
    st.markdown("## 03. Network topology statistics")
    stat_cols = st.columns(4)
    stat_cols[0].metric("Network density", f"{network_info['density']:.6f}")
    stat_cols[1].metric("Maximum degree", f"{network_summary['maximum_degree']:,}")
    stat_cols[2].metric("Minimum degree", f"{network_summary['minimum_degree']:,}")
    stat_cols[3].metric(
        "Highest-degree AS",
        str(network_summary["highest_degree_node"])
    )

    with st.expander("View detailed network summary"):
        st.json({
            **network_summary,
            "highest_degree_node": str(network_summary["highest_degree_node"]),
            "lowest_degree_node": str(network_summary["lowest_degree_node"])
        })

    # 04. Visualize a manageable local subgraph around the selected hub
    st.markdown("## 04. Network connectivity view")
    st.caption(
        "The full dataset contains thousands of nodes. For readability, "
        "the graph below shows a local view around the selected starting AS."
    )

    degree_order = sorted(
        network_graph.degree,
        key=lambda item: item[1],
        reverse=True
    )
    top_start_nodes = [node for node, degree in degree_order[:50]]
    defaults = get_network_defaults(network_graph)
    default_start = defaults["start_node"]
    if default_start not in top_start_nodes:
        top_start_nodes.insert(0, default_start)

    # Initialise state once, so reruns preserve the selected node.
    if "network_start" not in st.session_state:
        st.session_state.network_start = default_start

    selected_start = st.selectbox(
        "Starting Autonomous System (AS)",
        options=top_start_nodes,
        index=top_start_nodes.index(st.session_state.network_start)
        if st.session_state.network_start in top_start_nodes else 0,
        format_func=lambda node: (
            f"AS {node} — degree {network_graph.degree(node)}"
        ),
        key="network_start"
    )

    neighbours = sorted(
        network_graph.neighbors(selected_start),
        key=lambda node: network_graph.degree(node),
        reverse=True
    )
    visible_nodes = [selected_start] + neighbours[:59]
    local_graph = network_graph.subgraph(visible_nodes).copy()
    local_positions = nx.spring_layout(local_graph, seed=42, k=0.7)

    edge_x, edge_y = [], []
    for source, target in local_graph.edges():
        x0, y0 = local_positions[source]
        x1, y1 = local_positions[target]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    node_x = [local_positions[node][0] for node in local_graph.nodes()]
    node_y = [local_positions[node][1] for node in local_graph.nodes()]
    node_text = [str(node) for node in local_graph.nodes()]
    node_colors = [
        "#ffbd59" if node == selected_start else "#13BFD0"
        for node in local_graph.nodes()
    ]

    network_fig = go.Figure()
    network_fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y, mode="lines",
        line=dict(width=1, color="rgba(90,180,210,0.55)"),
        hoverinfo="none", showlegend=False
    ))
    network_fig.add_trace(go.Scatter(
        x=node_x, y=node_y, mode="markers",
        text=node_text,
        marker=dict(
            size=[17 if node == selected_start else 10 for node in local_graph.nodes()],
            color=node_colors,
            line=dict(width=1, color="white")
        ),
        hovertemplate="Autonomous System: %{text}<extra></extra>",
        showlegend=False
    ))
    network_fig.update_layout(
        title=f"Local topology around AS {selected_start}",
        height=470,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=15, r=15, t=55, b=15)
    )
    st.plotly_chart(network_fig, use_container_width=True)
    st.caption(
        f"Displayed local view: {local_graph.number_of_nodes()} nodes and "
        f"{local_graph.number_of_edges()} connections. The simulation itself "
        f"uses the complete graph of {network_graph.number_of_nodes():,} nodes."
    )

    # 05. Simulation settings
    st.markdown("## 05. Simulation settings")
    settings_col1, settings_col2 = st.columns(2)

    with settings_col1:
        network_steps = st.slider(
            "Simulation steps", 10, 1000, defaults["steps"], 10,
            key="network_steps"
        )
        network_rho = st.slider(
            "Entropy target (rho)", 0.10, 1.00, float(defaults["rho"]), 0.05,
            key="network_rho"
        )

    with settings_col2:
        network_eta = st.slider(
            "Temperature adaptation rate (eta)", 0.01, 0.50,
            float(defaults["eta"]), 0.01, key="network_eta"
        )
        network_temperature = st.slider(
            "Initial EBW temperature", 0.10, 5.00,
            float(defaults["initial_temperature"]), 0.10,
            key="network_temperature"
        )
        network_experiments = st.selectbox(
            "Repeated experiments", [10, 25, 50, 100],
            index=3, key="network_experiments"
        )

    if "network_result" not in st.session_state:
        st.session_state.network_result = None
    if "network_repeated_result" not in st.session_state:
        st.session_state.network_repeated_result = None

    run_col, reset_col = st.columns(2)
    with run_col:
        run_network = st.button(
            "▶ RUN NETWORK SIMULATION",
            use_container_width=True,
            type="primary"
        )
    with reset_col:
        reset_network = st.button(
            "↺ RESET SIMULATION",
            use_container_width=True
        )

    if reset_network:
        st.session_state.network_result = None
        st.session_state.network_repeated_result = None
        st.rerun()

    if run_network:
        if not validate_network_start(network_graph, selected_start):
            st.error("The selected Autonomous System has no neighbours.")
        else:
            try:
                with st.spinner(
                    "Running SRW, EBW and repeated experiments on the full network..."
                ):
                    network_result = compare_algorithms(
                        network_graph,
                        selected_start,
                        network_steps,
                        rho=network_rho,
                        eta=network_eta,
                        initial_temperature=network_temperature,
                        seed=42
                    )
                    network_repeated = compare_repeated_experiments(
                        network_graph,
                        selected_start,
                        network_steps,
                        experiments=network_experiments,
                        rho=network_rho,
                        eta=network_eta,
                        initial_temperature=network_temperature,
                        base_seed=42
                    )
                    st.session_state.network_result = network_result
                    st.session_state.network_repeated_result = network_repeated
                st.success("Both network exploration algorithms completed.")
            except Exception as error:
                st.error(f"Network simulation failed: {error}")

    # 06. Results
    network_result = st.session_state.network_result
    network_repeated = st.session_state.network_repeated_result

    if network_result is not None:
        st.markdown("## 06. Single-run results")
        srw = network_result["SRW"]
        ebw = network_result["EBW"]
        srw_metrics = srw["metrics"]
        ebw_metrics = ebw["metrics"]

        performance_df = pd.DataFrame({
            "Metric": list(srw_metrics.keys()),
            "SRW": [srw_metrics[key] for key in srw_metrics],
            "EBW": [ebw_metrics[key] for key in srw_metrics]
        })
        st.dataframe(performance_df, use_container_width=True, hide_index=True)

        coverage_cols = st.columns(4)
        coverage_cols[0].metric(
            "SRW node coverage", f"{srw_metrics['Node Coverage (%)']:.2f}%"
        )
        coverage_cols[1].metric(
            "EBW node coverage", f"{ebw_metrics['Node Coverage (%)']:.2f}%"
        )
        coverage_cols[2].metric(
            "SRW edge coverage", f"{srw_metrics['Edge Coverage (%)']:.2f}%"
        )
        coverage_cols[3].metric(
            "EBW edge coverage", f"{ebw_metrics['Edge Coverage (%)']:.2f}%"
        )

        st.markdown("## 07. Exploration paths")
        path_cols = st.columns(2)
        path_cols[0].markdown("**SRW path**")
        path_cols[0].write(" → ".join(map(str, srw["path"])))
        path_cols[1].markdown("**EBW path**")
        path_cols[1].write(" → ".join(map(str, ebw["path"])))

        st.markdown("## 08. Entropy comparison")
        entropy_fig = go.Figure()
        entropy_fig.add_trace(go.Scatter(
            y=srw["entropy"], mode="lines", name="SRW",
            line=dict(color="#65b9ff", width=2)
        ))
        entropy_fig.add_trace(go.Scatter(
            y=ebw["entropy"], mode="lines", name="EBW",
            line=dict(color="#4de0c1", width=2)
        ))
        entropy_fig.update_layout(
            title="Transition Entropy Comparison",
            xaxis_title="Simulation step",
            yaxis_title="Shannon entropy",
            template="plotly_dark", height=370
        )
        st.plotly_chart(entropy_fig, use_container_width=True)

        st.markdown("## 09. EBW temperature adaptation")
        temperature_fig = go.Figure()
        temperature_fig.add_trace(go.Scatter(
            y=ebw["temperature"], mode="lines", name="EBW temperature",
            line=dict(color="#ffbd59", width=2)
        ))
        temperature_fig.update_layout(
            title="Adaptive Temperature",
            xaxis_title="Simulation step",
            yaxis_title="Temperature",
            template="plotly_dark", height=330
        )
        st.plotly_chart(temperature_fig, use_container_width=True)

        if network_repeated is not None:
            st.markdown(
                f"## 10. {network_experiments}-experiment statistical analysis"
            )
            summary = network_repeated["Summary"]
            summary_rows = []
            for metric in summary["SRW"]:
                summary_rows.append({
                    "Metric": metric,
                    "SRW Mean": summary["SRW"][metric]["Mean"],
                    "SRW Std. Dev.": summary["SRW"][metric]["Standard Deviation"],
                    "EBW Mean": summary["EBW"][metric]["Mean"],
                    "EBW Std. Dev.": summary["EBW"][metric]["Standard Deviation"]
                })
            summary_df = pd.DataFrame(summary_rows)
            st.dataframe(summary_df, use_container_width=True, hide_index=True)

            st.download_button(
                "DOWNLOAD NETWORK STATISTICAL SUMMARY CSV",
                data=summary_df.to_csv(index=False).encode("utf-8"),
                file_name="network_statistical_summary.csv",
                mime="text/csv"
            )

            individual_rows = []
            for experiment in network_repeated["Individual Results"]:
                for algorithm in ("SRW", "EBW"):
                    row = {
                        "Experiment": experiment["Experiment"],
                        "Seed": experiment["Seed"],
                        "Algorithm": algorithm
                    }
                    row.update(experiment[algorithm])
                    individual_rows.append(row)
            individual_df = pd.DataFrame(individual_rows)
            st.download_button(
                "DOWNLOAD INDIVIDUAL NETWORK EXPERIMENTS CSV",
                data=individual_df.to_csv(index=False).encode("utf-8"),
                file_name="network_individual_experiments.csv",
                mime="text/csv"
            )
            st.info(
                "Mean values summarize average performance; standard deviation "
                "measures variation across runs. Neither method is assumed to "
                "be the winner."
            )

        st.markdown("## 11. Result interpretation")
        st.markdown("""
        Node coverage measures the percentage of Autonomous Systems visited.
        Edge coverage measures the percentage of recorded connections traversed.
        Revisit rate measures how often the walk returns to previously visited
        systems. Mean transition entropy measures uncertainty in the transition
        probabilities used by each algorithm.

        A higher coverage value indicates broader exploration of this graph,
        but it does not mean that internet traffic is faster or that routing
        quality is better. The dataset is a historical topology snapshot.
        """)

    else:
        st.info("Choose the settings and click RUN NETWORK SIMULATION.")

    # 12. Methodology
    st.markdown("## 12. Process")
    st.markdown("""
    1. Load the Stanford SNAP AS-733 edge-list dataset.
    2. Remove duplicate links and self-connections.
    3. Construct an undirected graph of Autonomous Systems.
    4. Select a starting AS and simulation parameters.
    5. Run SRW and EBW on the same complete graph.
    6. Repeat paired experiments and calculate summary statistics.
    7. Compare node coverage, edge coverage, revisits, entropy and runtime.
    """)

    # 13. Dataset source
    st.markdown("## 13. Dataset source")
    st.markdown(f"""
    **Dataset:** Stanford SNAP AS-733 Autonomous Systems topology.

    **Local file:** `datasets/network/as20000102.txt`

    **Source:** [Stanford SNAP AS-733 dataset]({get_network_dataset_source()})

    **Dataset records:** {network_dataset_info['records']:,} unique edge records.

    **Interpretation:** Nodes represent Autonomous Systems and edges represent
    recorded connections. This application performs graph exploration on the
    dataset and does not simulate live packet transmission.
    """)

    st.markdown("""
    <div class="footer">
        ENTROPY LAB | COMPUTER NETWORK TOPOLOGY SIMULATION
    </div>
    """, unsafe_allow_html=True)

