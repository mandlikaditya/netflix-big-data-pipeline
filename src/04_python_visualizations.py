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
    'font.size': 10
})

def load_cleaned_dataset(csv_path):
    print(f"Loading cleaned dataset with custom CSV parser from: {csv_path}")
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for row in reader:
            if len(row) > 20:
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
    # Figure 1: Top 12 Genre Categories on Netflix
    top_genres = df['genre_primary'].value_counts().head(12).sort_values(ascending=True)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Alternating colors from bottom to top:
    # Dramas (top/last bar) is Red. Other bars alternate between Dark Blue and Cyan.
    colors = []
    for i in range(12):
        if i == 11:
            colors.append('#E50914')  # Red for Dramas
        elif i % 2 == 0:
            colors.append('#005B7C')  # Dark Blue
        else:
            colors.append('#00B4D8')  # Cyan
            
    bars = ax.barh(top_genres.index, top_genres.values, color=colors, height=0.7)
    
    # Add values on the right of the bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 15, bar.get_y() + bar.get_height()/2, f'{int(width):,}',
                va='center', ha='left', color='white', fontweight='bold', fontsize=9.5)
                
    ax.set_title('Top 12 Genre Categories on Netflix', fontsize=15, fontweight='bold', pad=25, color='white')
    ax.text(1.0, 1.02, "Source: Netflix Dataset (M3 Cleaned)", transform=ax.transAxes, ha='right', va='bottom', fontsize=8, color='#888888')
    
    ax.set_xlabel('Number of Titles', fontsize=11, labelpad=10)
    ax.set_xlim(0, max(top_genres.values) * 1.1)
    ax.grid(axis='x', linestyle='--', alpha=0.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'genre_distribution.png'), dpi=300, facecolor=netflix_black, edgecolor='none')
    plt.close()
    print("Saved genre_distribution.png")

def plot_content_growth(df, output_dir):
    # Figure 2: Year-over-Year Content Growth on Netflix (2015–2021)
    growth_df = df[(df['year_added'] >= 2015) & (df['year_added'] <= 2021)]
    
    # Group by year_added and type
    pivot_df = growth_df.groupby(['year_added', 'type']).size().unstack(fill_value=0)
    pivot_df['Total'] = pivot_df['Movie'] + pivot_df['TV Show']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot Total (gold), Movies (red), TV Shows (cyan)
    ax.plot(pivot_df.index, pivot_df['Total'], color='#F5A623', marker='o', linewidth=2.5, label='Total')
    ax.plot(pivot_df.index, pivot_df['Movie'], color='#E50914', marker='s', linewidth=2.5, label='Movies')
    ax.plot(pivot_df.index, pivot_df['TV Show'], color='#00B4D8', marker='^', linewidth=2.5, label='TV Shows')
    
    # Fills under/between the curves
    ax.fill_between(pivot_df.index, 0, pivot_df['TV Show'], color='#00B4D8', alpha=0.12)
    ax.fill_between(pivot_df.index, pivot_df['TV Show'], pivot_df['Movie'], color='#E50914', alpha=0.12)
    ax.fill_between(pivot_df.index, pivot_df['Movie'], pivot_df['Total'], color='#0E3D48', alpha=0.18)
    
    # Annotate peak year 2019
    peak_year = 2019
    if peak_year in pivot_df.index:
        peak_val = pivot_df.loc[peak_year, 'Total']
        ax.annotate("Peak: 2,126",
                    xy=(peak_year, peak_val),
                    xytext=(peak_year - 1.1, peak_val + 100),
                    color='#F5A623', fontweight='bold', fontsize=10,
                    arrowprops=dict(arrowstyle="->", color='#F5A623', lw=1.5))
                    
    ax.set_title('Year-over-Year Content Growth on Netflix (2015–2021)', fontsize=15, fontweight='bold', pad=25, color='white')
    ax.set_xlabel('Year Added to Netflix', fontsize=11, labelpad=10)
    ax.set_ylabel('Number of Titles Added', fontsize=11, labelpad=10)
    ax.set_xticks(pivot_df.index)
    ax.set_xlim(2014.7, 2021.3)
    ax.set_ylim(-50, max(pivot_df['Total']) * 1.1)
    ax.grid(axis='both', linestyle='--', alpha=0.15)
    ax.legend(facecolor=netflix_black, edgecolor=netflix_grey, loc='upper left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'content_growth.png'), dpi=300, facecolor=netflix_black, edgecolor='none')
    plt.close()
    print("Saved content_growth.png")

def plot_geographic_breakdown(df, output_dir):
    # Figure 3: Top 12 Countries by Netflix Content Production (Excluding Unknown Entries)
    geo_df = df[df['country_primary'] != 'Unknown']
    top_countries = geo_df['country_primary'].value_counts().head(12)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Smooth color gradient from Red (#E50914) to Cyan (#00B4D8)
    start_rgb = np.array([229, 9, 20])
    end_rgb = np.array([0, 180, 216])
    colors = []
    for i in range(12):
        ratio = i / 11
        rgb = start_rgb + (end_rgb - start_rgb) * ratio
        hex_color = f"#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}"
        colors.append(hex_color)
        
    bars = ax.bar(top_countries.index, top_countries.values, color=colors, width=0.6)
    
    # Values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 40, f'{int(height):,}',
                va='bottom', ha='center', color='white', fontweight='bold', fontsize=8.5)
                
    ax.set_title('Top 12 Countries by Netflix Content Production', fontsize=15, fontweight='bold', pad=25, color='white')
    ax.text(1.0, 1.02, "Excluding \"Unknown\" country entries", transform=ax.transAxes, ha='right', va='bottom', fontsize=8, color='#888888')
    
    ax.set_ylabel('Number of Titles', fontsize=11, labelpad=10)
    plt.xticks(rotation=35, ha='right')
    ax.set_ylim(0, max(top_countries.values) * 1.1)
    ax.grid(axis='y', linestyle='--', alpha=0.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'geographic_breakdown.png'), dpi=300, facecolor=netflix_black, edgecolor='none')
    plt.close()
    print("Saved geographic_breakdown.png")

def plot_rating_distribution(df, output_dir):
    # Figure 4: Rating Distribution — Movies vs TV Shows Stacked by Content Type
    rating_counts = df.groupby(['rating', 'type']).size().unstack(fill_value=0)
    
    # Standard rating order matching the screenshot
    rating_order = ['G', 'TV-G', 'PG', 'TV-Y', 'TV-Y7', 'TV-Y7-FV', 'PG-13', 'TV-PG', 'TV-14', 'TV-MA', 'R', 'NR', 'UR', 'NC-17']
    rating_counts = rating_counts.reindex(rating_order, fill_value=0)
    rating_counts['Total'] = rating_counts['Movie'] + rating_counts['TV Show']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot stacked bar chart
    ax.bar(rating_counts.index, rating_counts['Movie'], color='#E50914', label='Movie', width=0.55)
    ax.bar(rating_counts.index, rating_counts['TV Show'], bottom=rating_counts['Movie'], color='#00B4D8', label='TV Show', width=0.55)
    
    # Shading bands for target audiences
    # Kids / Family: indices 0 to 5 (G to TV-Y7-FV)
    ax.axvspan(-0.5, 5.5, color='#00B4D8', alpha=0.06)
    # Teen: indices 6 to 7 (PG-13 to TV-PG)
    ax.axvspan(5.5, 7.5, color='#F5A623', alpha=0.06)
    # Mature: indices 8 to 13 (TV-14 to NC-17)
    ax.axvspan(7.5, 13.5, color='#E50914', alpha=0.06)
    
    # Labels for Shading bands
    ax.text(2.5, 2700, "Kids / Family", color='#00B4D8', ha='center', va='center', fontweight='bold', fontsize=8.5, alpha=0.7)
    ax.text(6.5, 2700, "Teen", color='#F5A623', ha='center', va='center', fontweight='bold', fontsize=8.5, alpha=0.7)
    ax.text(10.5, 2700, "Mature", color='#E50914', ha='center', va='center', fontweight='bold', fontsize=8.5, alpha=0.7)
    
    # Values on top of bars for total > 10
    for i, rating in enumerate(rating_counts.index):
        total = rating_counts.loc[rating, 'Total']
        if total > 10:
            ax.text(i, total + 30, f'{int(total):,}', va='bottom', ha='center', color='white', fontweight='bold', fontsize=8)
            
    ax.set_title('Rating Distribution - Movies vs TV Shows', fontsize=15, fontweight='bold', pad=25, color='white')
    ax.set_ylabel('Number of Titles', fontsize=11, labelpad=10)
    ax.set_ylim(0, 3000)
    ax.grid(axis='y', linestyle='--', alpha=0.15)
    ax.legend(facecolor=netflix_black, edgecolor=netflix_grey, loc='upper right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rating_distribution.png'), dpi=300, facecolor=netflix_black, edgecolor='none')
    plt.close()
    print("Saved rating_distribution.png")

def plot_type_and_duration(df, output_dir):
    # Figure 5: Movies vs TV Shows Split (Donut) & Duration Distribution (Box Plot)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    
    # 1. Donut Chart (Left Subplot)
    type_counts = df['type'].value_counts()
    colors = ['#E50914', '#00B4D8'] # Movies (Red), TV Shows (Cyan)
    
    # Outer pie wedges with thick dark border
    wedges, texts, autotexts = ax1.pie(
        [type_counts['Movie'], type_counts['TV Show']], 
        labels=['Movie', 'TV Show'], 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=colors, 
        pctdistance=0.75,
        textprops=dict(color="white", fontweight="bold", fontsize=11),
        wedgeprops=dict(width=0.45, edgecolor='#141414', linewidth=3.5)
    )
    
    for autotext in autotexts:
        autotext.set_fontsize(11)
        
    centre_circle = plt.Circle((0,0), 0.55, fc=netflix_black)
    ax1.add_artist(centre_circle)
    ax1.text(0, 0, f"{len(df):,}\nTitles", ha='center', va='center', color='white', fontweight='bold', fontsize=14)
    ax1.set_title('Movies vs TV Shows Split', fontsize=14, fontweight='bold', pad=15)
    
    # 2. Box Plot (Right Subplot)
    df_box = df.copy()
    df_box['box_group'] = df_box['type'].map({
        'Movie': 'Movies\n(minutes)',
        'TV Show': 'TV Shows\n(seasons)'
    })
    
    # Plot side-by-side boxplots on the same axis
    palette = {
        'Movies\n(minutes)': '#B30710',
        'TV Shows\n(seasons)': '#F5A623'
    }
    
    sns.boxplot(
        data=df_box, 
        x='box_group', 
        y='duration_int', 
        ax=ax2, 
        hue='box_group',
        palette=palette, 
        legend=False,
        width=0.45, 
        medianprops=dict(color='#F5A623', linewidth=2.5),
        flierprops=dict(marker='o', markerfacecolor='#444444', markeredgecolor='none', markersize=2, alpha=0.4)
    )
    
    ax2.set_title('Duration Distribution by Content Type', fontsize=14, fontweight='bold', pad=15)
    ax2.set_ylabel('Duration', fontsize=12)
    ax2.set_xlabel(None)
    ax2.grid(axis='y', linestyle='--', alpha=0.15)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'type_and_duration.png'), dpi=300, facecolor=netflix_black, edgecolor='none')
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
    
    fig, ax = plt.subplots(figsize=(12, 7))
    cmap = sns.dark_palette(netflix_red, as_cmap=True)
    
    sns.heatmap(pivot_df, annot=True, fmt='d', cmap=cmap, linewidths=.5, cbar_kws={'label': 'Titles Added'}, ax=ax,
                annot_kws={'fontsize': 10, 'fontweight': 'bold', 'color': 'white'})
                
    ax.set_title('Top 10 Genres by Year Added (Heatmap, 2016–2021)', fontsize=15, fontweight='bold', pad=25, color='white')
    ax.set_ylabel('Primary Genre', fontsize=11, labelpad=10)
    ax.set_xlabel('Year Added', fontsize=11, labelpad=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'genre_year_heatmap.png'), dpi=300, facecolor=netflix_black, edgecolor='none')
    plt.close()
    print("Saved genre_year_heatmap.png")

def main():
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
    
    output_dir = 'reports/figures'
    os.makedirs(output_dir, exist_ok=True)
    print(f"Saving output visualizations to: {output_dir}/")
    
    plot_genre_distribution(df, output_dir)
    plot_content_growth(df, output_dir)
    plot_geographic_breakdown(df, output_dir)
    plot_rating_distribution(df, output_dir)
    plot_type_and_duration(df, output_dir)
    plot_genre_year_heatmap(df, output_dir)
    
    print("\nVisualizations saved successfully in reports/figures/ folder.")

if __name__ == "__main__":
    main()
