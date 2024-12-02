import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
details = pd.read_csv("Stats/games_details.csv")

# Calculate performance metrics for a specific position
position_mapping = {
    'G': 'Guard',
    'C': 'Center',
    'F': 'Forward'
}

# Reverse the mapping for easy access in the sidebar (full name to abbreviation)
reverse_position_mapping = {v: k for k, v in position_mapping.items()}


def calculate_metrics(data, position):
    filtered_data = data[data['START_POSITION'] == position]
    return filtered_data.describe()


def main():
    st.title("Position-Based Performance Comparison")
    st.write("Analyze and compare basketball player performance metrics by position.")

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

    # Map positions for the selectbox with full names
    positions = list(position_mapping.values())
    selected_position_full = st.sidebar.selectbox(
        "Select Position", options=positions)

    # Get the corresponding abbreviation for the selected position
    selected_position = reverse_position_mapping[selected_position_full]

    teams = details['TEAM_ABBREVIATION'].dropna().unique()
    selected_team = st.sidebar.multiselect(
        "Select Team(s)", options=teams, default=teams)

    # games = details['GAME_ID'].dropna().unique()
    # selected_game = st.sidebar.multiselect(
    #     "Select Game(s)", options=games, default=games)

    # Filter data based on sidebar inputs
    filtered_data = details[
        (details['START_POSITION'] == selected_position) &
        (details['TEAM_ABBREVIATION'].isin(selected_team))  # &
        # (details['GAME_ID'].isin(selected_game))
    ]

    # st.write(f"### Players in Position: {selected_position}")
    # st.dataframe(filtered_data)

    # Show summary statistics for the selected position
    st.write("### Performance Metrics")
    metrics = calculate_metrics(filtered_data, selected_position)
    st.write(metrics)

    # Plotting performance data
    st.write("### Performance Visualization")
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot selected stats: Points, Assists, Rebounds, etc.
    sns.boxplot(data=filtered_data[['PTS', 'AST', 'REB', 'STL', 'BLK']], ax=ax)
    ax.set_title(f"Performance Distribution for {selected_position} Players")
    st.pyplot(fig)

    # Optional: Additional visualizations, e.g., correlation heatmap
    st.write("### Correlation Heatmap")
    corr_matrix = filtered_data[['PTS', 'AST', 'REB', 'STL', 'BLK']].corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
    ax.set_title(f"Correlation Matrix for {selected_position} Players")
    st.pyplot(fig)


if __name__ == "__main__":
    main()
