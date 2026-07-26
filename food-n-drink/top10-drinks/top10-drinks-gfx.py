# Fancy Beverage Market Visualizer (2025 Data w/ Seaborn Upgrades)
# Run: python fancy_beverage_viz.py
# Outputs: fancy_beverage_markets_2025.png, fancy_beverage_chaos_2025.png
# Deps: numpy, pandas, matplotlib, seaborn (std in your env; ties to pharmacology data viz)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

def fancy_bar_charts():
    # Data artifacts (soft & alc as Pandas DFs for Seaborn)
    soft_data = pd.DataFrame({
        'Brand': ['Coca-Cola', 'Pepsi', 'Red Bull', 'Sprite', 'Diet Coke', 'Mountain Dew', 'Fanta', 'Dr Pepper', 'Gatorade', 'Monster'],
        'Share': [22.1, 15.3, 8.2, 5.7, 4.9, 3.8, 3.5, 3.2, 2.9, 2.6],
        'Category': ['Soft'] * 10
    })
    alc_data = pd.DataFrame({
        'Brand': ['Jinro', 'Ginebra San Miguel', 'Emperador', "Officer's Choice", 'Smirnoff', "McDowell's No.1", 'Imperial Blue', 'Tanduay', 'Royal Stag', 'Bacardi'],
        'Share': [4.5, 3.8, 3.2, 2.9, 2.7, 2.5, 2.3, 2.1, 1.9, 1.7],
        'Category': ['Alc'] * 10
    })
    combined = pd.concat([soft_data, alc_data])
    
    # Seaborn fancy: darkgrid theme, coolwarm palette, annotations
    sns.set_theme(style='darkgrid', palette='coolwarm', font='sans-serif', font_scale=1.1)
    fig, axs = plt.subplots(1, 2, figsize=(16, 8), sharey=False)
    
    # Soft bars: horizontal, blue gradient, labels
    sns.barplot(data=soft_data, y='Brand', x='Share', ax=axs[0], palette='Blues_d', orient='h')
    axs[0].set_title('Top 10 Soft Drinks 2025 (Expo Decay)', fontsize=14)
    axs[0].set_xlabel('Market Share (%)', fontsize=12)
    for p in axs[0].patches:
        axs[0].annotate(f'{p.get_width():.1f}%', (p.get_width() + 0.5, p.get_y() + p.get_height()/2), ha='center', va='center', fontsize=10, color='black')
    sns.despine(ax=axs[0], left=True, bottom=True)
    
    # Alc bars: horizontal, red gradient, labels
    sns.barplot(data=alc_data, y='Brand', x='Share', ax=axs[1], palette='Reds_d', orient='h')
    axs[1].set_title('Top 10 Alcoholic Beverages 2025 (Linear Decay)', fontsize=14)
    axs[1].set_xlabel('Market Share (%)', fontsize=12)
    for p in axs[1].patches:
        axs[1].annotate(f'{p.get_width():.1f}%', (p.get_width() + 0.2, p.get_y() + p.get_height()/2), ha='center', va='center', fontsize=10, color='black')
    sns.despine(ax=axs[1], left=True, bottom=True)
    
    plt.tight_layout()
    plt.savefig('fancy_beverage_markets_2025.png', dpi=300, bbox_inches='tight')  # High-res for your Medium articles
    plt.show()  # Interactive view

def fancy_lorenz_attractor():
    # Chaos sim params (Lorenz equations)
    def lorenz(x, y, z, sigma=10, rho=28, beta=8/3):
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        return dx, dy, dz
    
    dt = 0.01
    num_steps = 10000
    xs = np.empty(num_steps + 1)
    ys = np.empty(num_steps + 1)
    zs = np.empty(num_steps + 1)
    xs[0], ys[0], zs[0] = (22.1/5, 4.5/5, (22.1 + 4.5)/10)  # Scaled top shares
    
    for i in range(num_steps):
        dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
        xs[i + 1] = xs[i] + (dx * dt)
        ys[i + 1] = ys[i] + (dy * dt)
        zs[i + 1] = zs[i] + (dz * dt)
    
    # Seaborn fancy: ticks theme, viridis cmap for time-gradient
    sns.set_theme(style='ticks', palette='viridis', font='serif', font_scale=1.2)
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Gradient-colored line (fades by time, fractal depth)
    points = np.array([xs, ys, zs]).T.reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    norm = plt.Normalize(0, num_steps)
    lc = ax.add_collection3d(plt.mlines.Line3DCollection(segments, cmap='viridis', norm=norm, linewidth=0.8))
    lc.set_array(np.arange(len(xs)))
    
    ax.set_title('Fancy Beverage Market Chaos Sim (Lorenz Attractor)', fontsize=16)
    ax.set_xlabel('Soft Drinks Leader Factor', fontsize=12)
    ax.set_ylabel('Alcoholic Leader Factor', fontsize=12)
    ax.set_zlabel('Combined Share Factor', fontsize=12)
    ax.view_init(elev=20, azim=30)  # Rotated view for depth
    sns.despine(fig=fig, ax=ax)
    
    plt.colorbar(lc, ax=ax, label='Time Step', shrink=0.5)  # Colorbar for temporal flow
    plt.savefig('fancy_beverage_chaos_2025.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    fancy_bar_charts()
    fancy_lorenz_attractor()