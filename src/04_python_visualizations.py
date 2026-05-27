# 04_python_visualizations.py
# Milestone 5: Python Visualization (Matplotlib & Seaborn)
# Author: Saadullah Mohammed

import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Apply Netflix UI Dark Theme
netflix_black = '#141414'
netflix_red = '#E50914'
netflix_teal = '#00B4D8'
netflix_gold = '#F5A623'
netflix_grey = '#333333'

plt.rcParams.update({
    'axes.facecolor': netflix_black,
    'figure.facecolor': netflix_black,
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'axes.edgecolor': netflix_grey,
    'grid.color': '#222222',
    'font.size': 11
})

def load_cleaned_dataset(csv_path):
    print(f"Loading cleaned dataset with custom CSV parser from: {csv_path}")
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            if len(row) > 20:
                # Reconstruct description by merging split parts
                desc = ','.join(row[11:len(row)-8])
                row = row[:11] + [desc] + row[-8:]
            rows.append(row)
    
    df = pd.DataFrame(rows, columns=header)
    
    # Clean data types
    df['year_added'] = pd.to_numeric(df['year_added'], errors='coerce')
    df['month_added'] = pd.to_numeric(df['month_added'], errors='coerce')
    df['genre_count'] = pd.to_numeric(df['genre_count'], errors='coerce')
    df['duration_int'] = pd.to_numeric(df['duration_int'], errors='coerce')
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
    
    # Drop rows where year_added is null
    df = df.dropna(subset=['year_added'])
    df['year_added'] = df['year_added'].astype(int)
    
    return df

def plot_genre_distribution(df, output_dir):
    # Figure 1: Top 12 Genre Categories on Netflix by Number of Titles
    top_genres = df['genre_primary'].value_counts().head(12).sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    # Highlight top genre (Dramas) in red, rest in teal
    colors = [netflix_teal if i < len(top_genres)-1 else netflix_red for i in range(len(top_genres))]
    
    bars = ax.barh(top_genres.index, top_genres.values, color=colors, height=0.7)
    
    # Add values on the bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 15, bar.get_y() + bar.get_height()/2, f'{int(width):,}',
                va='center', ha='left', color='white', fontweight='bold')
                
    ax.set_title('Top 12 Genre Categories on Netflix by Number of Titles', fontsize=16, fontweight='bold', pad=25, color=netflix_red)
    ax.set_xlabel('Number of Titles', fontsize=12, labelpad=10)
    ax.set_xlim(0, max(top_genres.values) * 1.1)
    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'genre_distribution.png'), dpi=300, facecolor=netflix_black, edgecolor='none')
    plt.close()
    print("Saved genre_distribution.png")

def plot_content_growth(df, output_dir):
    # Figure 2: Year-over-Year Content Growth on Netflix (2015–2021)
    growth_df = df[(df['year_added'] >= 2015) & (df['year_added'] <= 2021)]
    
    # Group by year_added and type
    pivot_df = growth_df.groupby(['year_added', 'type']).size().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot Movie and TV Show lines
    ax.plot(pivot_df.index, pivot_df['Movie'], color=netflix_red, marker='o', linewidth=3, label='Movies')
    ax.plot(pivot_df.index, pivot_df['TV Show'], color=netflix_teal, marker='s', linewidth=3, label='TV Shows')
    
    # Fills under the curves
    ax.fill_between(pivot_df.index, pivot_df['Movie'], color=netflix_red, alpha=0.1)
    ax.fill_between(pivot_df.index, pivot_df['TV Show'], color=netflix_teal, alpha=0.1)
    
    # Annotate peak year 2019
    peak_year = 2019
    if peak_year in pivot_df.index:
        peak_movies = pivot_df.loc[peak_year, 'Movie']
        peak_tv = pivot_df.loc[peak_year, 'TV Show']
        total_peak = peak_movies + peak_tv
        ax.annotate(f'Peak in 2019\nTotal: {total_peak:,} added',
                    xy=(peak_year, peak_movies),
                    xytext=(peak_year - 0.8, peak_movies + 200),
                    arrowprops=dict(facecolor='white', shrink=0.08, width=1.5, headwidth=8),
                    color='white', fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', fc=netflix_black, ec=netflix_grey, alpha=0.8))
                    
    ax.set_title('Year-over-Year Content Growth on Netflix (2015–2021)', fontsize=16, fontweight='bold', pad=25, color=netflix_red)
    ax.set_xlabel('Year Added', fontsize=12, labelpad=10)
    ax.set_ylabel('Number of Titles Added', fontsize=12, labelpad=10)
    ax.set_xticks(pivot_df.index)
    ax.grid(axis='both', linestyle='--', alpha=0.3)
    ax.legend(facecolor=netflix_black, edgecolor=netflix_grey, loc='upper left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'content_growth.png'), dpi=300, facecolor=netflix_black, edgecolor='none')
    plt.close()
    print("Saved content_growth.png")

def plot_geographic_breakdown(df, output_dir):
    # Figure 3: Top 12 Countries by Netflix Content Production (Excluding Unknown Entries)
    geo_df = df[df['country_primary'] != 'Unknown']
    top_countries = geo_df['country_primary'].value_counts().head(12)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Accent colors: USA in red, India in gold, rest in teal
    colors = [netflix_red] + [netflix_gold] + [netflix_teal] * 10
    
    bars = ax.bar(top_countries.index, top_countries.values, color=colors, width=0.6)
    
    # Values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 50, f'{int(height):,}',
                va='bottom', ha='center', color='white', fontweight='bold', fontsize=10)
                
    ax.set_title('Top 12 Countries by Netflix Content Production\n(Excluding Unknown Entries)', fontsize=16, fontweight='bold', pad=25, color=netflix_red)
    ax.set_ylabel('Number of Titles', fontsize=12, labelpad=10)
    ax.set_xlabel('Country of Origin', fontsize=12, labelpad=10)
    plt.xticks(rotation=45, ha='right')
    ax.set_ylim(0, max(top_countries.values) * 1.1)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'geographic_breakdown.png'), dpi=300, facecolor=netflix_black, edgecolor='none')
    plt.close()
    print("Saved geographic_breakdown.png")

def plot_rating_distribution(df, output_dir):
    # Figure 4: Rating Distribution — Movies vs TV Shows Stacked by Content Type
    rating_counts = df.groupby(['rating', 'type']).size().unstack(fill_value=0)
    rating_counts['total'] = rating_counts['Movie'] + rating_counts['TV Show']
    rating_counts = rating_counts.sort_values(by='total', ascending=False).head(10)
    rating_counts = rating_counts.drop(columns=['total'])
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot stacked bar chart
    rating_counts.plot(kind='bar', stacked=True, color=[netflix_red, netflix_teal], ax=ax, width=0.6)
    
    # Add counts inside and on top of bars
    for i, (idx, row) in enumerate(rating_counts.iterrows()):
        movie_val = row['Movie']
        tv_val = row['TV Show']
        total = movie_val + tv_val
        
        # Labels for Movies
        if movie_val > 50:
            ax.text(i, movie_val / 2, f'{int(movie_val):,}', va='center', ha='center', color='white', fontsize=9, fontweight='bold')
        # Labels for TV Shows
        if tv_val > 50:
            ax.text(i, movie_val + (tv_val / 2), f'{int(tv_val):,}', va='center', ha='center', color='white', fontsize=9, fontweight='bold')
        # Total on top
        ax.text(i, total + 40, f'{int(total):,}', va='bottom', ha='center', color='white', fontsize=10, fontweight='bold')

    ax.set_title('Rating Distribution — Movies vs TV Shows Stacked by Content Type', fontsize=16, fontweight='bold', pad=25, color=netflix_red)
    ax.set_xlabel('Content Rating', fontsize=12, labelpad=10)
    ax.set_ylabel('Number of Titles', fontsize=12, labelpad=10)
    plt.xticks(rotation=0)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.legend(['Movies', 'TV Shows'], facecolor=netflix_black, edgecolor=netflix_grey)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rating_distribution.png'), dpi=300, facecolor=netflix_black, edgecolor='none')
    plt.close()
    print("Saved rating_distribution.png")

def plot_type_and_duration(df, output_dir):
    # Figure 5: Movies vs TV Shows Split (Donut) & Duration Distribution (Box Plot)
    fig = plt.figure(figsize=(15, 6))
    
    # 1. Donut Chart (Subplot 1)
    ax1 = plt.subplot2grid((1, 3), (0, 0))
    type_counts = df['type'].value_counts()
    colors = [netflix_red, netflix_teal]
    wedges, texts, autotexts = ax1.pie(type_counts.values, labels=type_counts.index, 
                                      autopct='%1.1f%%', startangle=90, 
                                      colors=colors, pctdistance=0.75,
                                      textprops=dict(color="white", fontweight="bold"))
                                      
    # Draw inner circle to make it a donut
    centre_circle = plt.Circle((0,0), 0.55, fc=netflix_black)
    ax1.add_artist(centre_circle)
    ax1.set_title('Content Type Split', fontsize=14, fontweight='bold', pad=15)
    
    # 2. Movie Duration Box Plot (Subplot 2)
    ax2 = plt.subplot2grid((1, 3), (0, 1))
    movie_durations = df[(df['type'] == 'Movie') & (df['duration_int'].notnull())]['duration_int']
    sns.boxplot(y=movie_durations, ax=ax2, color=netflix_red, width=0.4, 
                flierprops=dict(markerfacecolor='white', markeredgecolor='none', alpha=0.3))
    ax2.set_title('Movie Runtimes', fontsize=14, fontweight='bold', pad=15)
    ax2.set_ylabel('Duration (minutes)', fontsize=12)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    
    # 3. TV Show Duration Box Plot (Subplot 3)
    ax3 = plt.subplot2grid((1, 3), (0, 2))
    tv_durations = df[(df['type'] == 'TV Show') & (df['duration_int'].notnull())]['duration_int']
    sns.boxplot(y=tv_durations, ax=ax3, color=netflix_teal, width=0.4,
                flierprops=dict(markerfacecolor='white', markeredgecolor='none', alpha=0.3))
    ax3.set_title('TV Show Seasons', fontsize=14, fontweight='bold', pad=15)
    ax3.set_ylabel('Duration (seasons)', fontsize=12)
    ax3.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.suptitle('Movies vs TV Shows Split (Donut) & Duration Distribution by Content Type (Box Plots)', 
                 fontsize=16, fontweight='bold', y=1.02, color=netflix_red)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'type_and_duration.png'), dpi=300, facecolor=netflix_black, edgecolor='none', bbox_inches='tight')
    plt.close()
    print("Saved type_and_duration.png")

def plot_genre_year_heatmap(df, output_dir):
    # Figure 6: Top 10 Genres by Year Added (Heatmap, 2016–2021)
    top_10_genres = df['genre_primary'].value_counts().head(10).index.tolist()
    
    heatmap_data = df[
        (df['genre_primary'].isin(top_10_genres)) & 
        (df['year_added'] >= 2016) & 
        (df['year_added'] <= 2021)
    ]
    
    pivot_df = heatmap_data.groupby(['genre_primary', 'year_added']).size().unstack(fill_value=0)
    pivot_df = pivot_df.reindex(top_10_genres)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    cmap = sns.dark_palette(netflix_red, as_cmap=True)
    
    sns.heatmap(pivot_df, annot=True, fmt='d', cmap=cmap, linewidths=.5, cbar_kws={'label': 'Titles Added'}, ax=ax,
                annot_kws={'fontsize': 10, 'fontweight': 'bold', 'color': 'white'})
                
    ax.set_title('Top 10 Genres by Year Added (Heatmap, 2016–2021)', fontsize=16, fontweight='bold', pad=25, color=netflix_red)
    ax.set_ylabel('Primary Genre', fontsize=12, labelpad=10)
    ax.set_xlabel('Year Added', fontsize=12, labelpad=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'genre_year_heatmap.png'), dpi=300, facecolor=netflix_black, edgecolor='none')
    plt.close()
    print("Saved genre_year_heatmap.png")

def main():
    # Detect the path of the cleaned data
    data_paths = [
        'data/processed/netflix_cleaned.csv',
        'netflix_cleaned.csv',
        '../data/processed/netflix_cleaned.csv'
    ]
    
    csv_path = None
    for path in data_paths:
        if os.path.exists(path):
            csv_path = path
            break
            
    if csv_path is None:
        raise FileNotFoundError("Could not find netflix_cleaned.csv in any of the search paths.")
        
    df = load_cleaned_dataset(csv_path)
    
    # Establish output directory
    output_dir = 'reports/figures'
    os.makedirs(output_dir, exist_ok=True)
    print(f"Saving output visualizations to: {output_dir}/")
    
    # Generate all visualizations
    plot_genre_distribution(df, output_dir)
    plot_content_growth(df, output_dir)
    plot_geographic_breakdown(df, output_dir)
    plot_rating_distribution(df, output_dir)
    plot_type_and_duration(df, output_dir)
    plot_genre_year_heatmap(df, output_dir)
    
    print("\nVisualizations saved successfully in reports/figures/ folder.")

if __name__ == "__main__":
    main()
