Industrial Human Resource Geo-Visualization
This project is designed to provide an interactive dashboard for exploring and visualizing industrial human resource data across Indian states and districts. The dashboard integrates multiple data visualizations—including stacked bar charts, pie charts, Plotly bar charts, and geo-maps—with official boundaries overlayed on the map.

Table of Contents
Overview

Features

Technologies Used

Installation

Usage

Project Structure

Data Sources

License

Contact

Overview
This project focuses on updating and analyzing industrial human resource data to help policymakers and business analysts understand the distribution of workers across various industries in India. The dashboard provides:

State-wise and district-level insights on the number of workers.

Visualizations that display the distribution of main and marginal workers.

Geo-visualization with official Indian boundaries.

Natural Language Processing (NLP) based text analytics on NIC names.

Features
Interactive Filtering: Select state, district, and NIC name via a sidebar.

Stacked Bar Chart: Compare the distribution of workers across rural, urban, and total counts.

Pie Charts: Visualize the distribution of marginal workers in rural and urban areas.

Plotly Bar Chart: View state-wise worker distribution on a logarithmic scale.

Geo-Map Visualization: Overlay official boundaries on an interactive map with markers.

Word Cloud & Text Analytics: (Optional) Use NLP techniques to analyze textual data (e.g., NIC names).

Modular Code: Organized into multiple sections for easy maintenance and updates.

Technologies Used
Python 3.x

Streamlit for interactive dashboard development.

Pandas for data manipulation.

Matplotlib and Seaborn for plotting.

Plotly for interactive charts.

Folium and GeoPandas for geo-mapping.

NLTK for text processing.

scikit-learn for clustering and TF-IDF vectorization.
