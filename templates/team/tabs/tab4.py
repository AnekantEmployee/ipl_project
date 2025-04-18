import streamlit as st
import plotly.express as px
import pandas as pd

def apply_custom_css():
    """Apply custom CSS styles to the Streamlit app"""
    st.markdown(
        """
        <style>
            .header {
                color: #ff4b4b;
                font-size: 40px;
                font-weight: bold;
                text-align: center;
                margin-bottom: 20px;
            }
            .subheader {
                color: #1c83e1;
                font-size: 24px;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            .metric-card {
                background-color: #f0f2f6;
                border-radius: 10px;
                padding: 15px;
                text-align: center;
            }
            .metric-value {
                font-size: 36px;
                font-weight: bold;
                color: #1c83e1;
            }
            .metric-name {
                font-size: 16px;
                color: #555;
            }
            .match-card {
                background-color: #ffffff;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border-left: 5px solid #1c83e1;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def create_metric_card(value, name, highlight=None):
    """Create a metric card with optional highlight"""
    if highlight:
        name = f"{name} - {highlight}"
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-name">{name}</div>
    </div>
    """

def create_match_card(match, team):
    """Create a styled card for a super over match"""
    winner = match['winner']
    is_win = winner == team
    opponent = match['team2'] if match['team1'] == team else match['team1']
    
    return f"""
    <div class="match-card">
        <div style="font-weight:bold; font-size:18px; margin-bottom:8px; color: #333333;">
            {match['season']} - {team} vs {opponent}
        </div>
        <div style="margin-bottom:5px; color: #555555;">
            <span style="font-weight:bold; color: #333333;">Venue:</span> {match['venue']}, {match['city']}
        </div>
        <div style="margin-bottom:5px; color: #555555;">
            <span style="font-weight:bold; color: #333333;">Result:</span> 
            <span style="color: {'#4CAF50' if is_win else '#e63946'}; font-weight:bold;">
                {'Won' if is_win else 'Lost'} the super over
            </span>
        </div>
    </div>
    """

def super_over_analysis(response, team):
    """Main function to display super over analysis dashboard"""
    try:
        apply_custom_css()
        
        if "total_super_over" not in response or response["total_super_over"].shape[0] == 0:
            st.error("No Super Over Data Available")
            return
            
        total_super_overs = response["total_super_over"].shape[0]
        super_overs_won = response["total_super_over_won"].shape[0]
        super_overs_lost = total_super_overs - super_overs_won
        win_percentage = (super_overs_won / total_super_overs) * 100 if total_super_overs > 0 else 0
        
        st.subheader(f"Super Over Performance of {team}")
        
        # Create tabs
        tab1, tab2 = st.tabs(["Overview", "Match Details"])
        
        with tab1:
            # Overview metrics
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(
                    create_metric_card(total_super_overs, "Total Super Overs"),
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown(
                    create_metric_card(f"{win_percentage:.1f}%", "Win Percentage"),
                    unsafe_allow_html=True
                )
            
            st.markdown("---")
            
            # Win/Loss distribution
            st.markdown(
                '<div class="subheader">Super Over Win/Loss Distribution</div>',
                unsafe_allow_html=True
            )
            
            so_data = {
                "Result": ["Won", "Lost"],
                "Count": [super_overs_won, super_overs_lost],
                "Color": ["#4CAF50", "#e63946"]
            }
            
            fig = px.pie(
                so_data,
                values="Count",
                names="Result",
                color="Result",
                color_discrete_map={
                    "Won": "#4CAF50",
                    "Lost": "#e63946"
                },
                title=f"Super Over Outcomes ({total_super_overs} matches)",
                hole=0.4,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Match details
            st.markdown(
                '<div class="subheader">Super Over Match Details</div>',
                unsafe_allow_html=True
            )
            
            # Show won matches first
            if super_overs_won > 0:
                st.markdown("### Won Matches")
                for _, match in response["total_super_over_won"].iterrows():
                    st.markdown(
                        create_match_card(match, team),
                        unsafe_allow_html=True
                    )
            
            # Show lost matches
            if super_overs_lost > 0:
                st.markdown("### Lost Matches")
                lost_matches = response["total_super_over"][
                    ~response["total_super_over"].index.isin(response["total_super_over_won"].index)
                ]
                for _, match in lost_matches.iterrows():
                    st.markdown(
                        create_match_card(match, team),
                        unsafe_allow_html=True
                    )
            
            # Raw data table
            st.markdown(
                '<div class="subheader">Raw Data</div>',
                unsafe_allow_html=True
            )
            st.dataframe(
                response["total_super_over"][
                    ["season", "city", "venue", "team1", "team2", "winner"]
                ].sort_values("winner"),
                use_container_width=True
            )
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your data format and try again.")