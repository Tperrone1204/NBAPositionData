import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# details = pd.read_csv("Stats/games_details.csv")

url = "https://drive.google.com/file/d/1B4jdJDW-5Z45RsoSMCh1ji-qCW6FO1_z/view?usp=drive_link"
details = pd.read_csv(url)

position_mapping = {
    'G': 'Guard',
    'C': 'Center',
    'F': 'Forward'
}

reverse_position_mapping = {v: k for k, v in position_mapping.items()}


def calculate_metrics(data, position):
    filtered_data = data[data['START_POSITION'] == position]
    return filtered_data.describe()


def main():
    st.title("Position-Based Performance Comparison")

    # Display basic data info
    # st.write("### Dataset Overview")
    # st.dataframe(details.head())

    # Sidebar filters
    st.sidebar.header("Filters")

    # for row in positions:
    #    for element in row:
    #        if element == "F":
    #            element = "Forward"
    #       elif element == "G":
    #            element = "Guard"
    #       elif element == "C":
    #           element = "Center"

    positions = list(position_mapping.values())
    selected_position_full = st.sidebar.selectbox(
        "Select Position", options=positions)
    selected_position = reverse_position_mapping[selected_position_full]

    teams = details['TEAM_ABBREVIATION'].dropna().unique()
    selected_team = st.sidebar.multiselect(
        "Select Team(s)", options=teams, default=teams)

    # games = details['GAME_ID'].dropna().unique()
    # selected_game = st.sidebar.multiselect(
    #     "Select Game(s)", options=games, default=games)

    filtered_data = details[
        (details['START_POSITION'] == selected_position) &
        (details['TEAM_ABBREVIATION'].isin(selected_team))  # &
        # (details['GAME_ID'].isin(selected_game))
    ]

    # st.write(f"### Players in Position: {selected_position}")
    # st.dataframe(filtered_data)

    st.write("Performance Metrics")
    metrics = calculate_metrics(filtered_data, selected_position)
    st.write(metrics)

    st.write("Performance Visualization")
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.boxplot(data=filtered_data[['PTS', 'AST', 'REB', 'STL', 'BLK']], ax=ax)
    ax.set_title(f"Performance Distribution for {selected_position} Players")
    st.pyplot(fig)

    st.write("Heatmap")
    corr_matrix = filtered_data[['PTS', 'AST', 'REB', 'STL', 'BLK']].corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
    ax.set_title(f"Correlation Matrix for {selected_position} Players")
    st.pyplot(fig)


if __name__ == "__main__":
    main()
