# 2025 Beverage Market Simulator (Soft Drinks & Alcoholic)
# Run with: python beverage_sim.py
# Dependencies: numpy, matplotlib (pip install if needed; your env has them)
import numpy as np
import matplotlib.pyplot as plt

def simulate_beverage_markets():
    # Soft Drinks Data Artifact (2025)
    soft_brands = ['Coca-Cola', 'Pepsi', 'Red Bull', 'Sprite', 'Diet Coke', 'Mountain Dew', 'Fanta', 'Dr Pepper', 'Gatorade', 'Monster']
    soft_shares = np.array([22.1, 15.3, 8.2, 5.7, 4.9, 3.8, 3.5, 3.2, 2.9, 2.6])
    soft_sales = np.array([35.8, 28.4, 13.2, 9.2, 7.9, 6.1, 5.6, 5.1, 4.7, 4.2])
    
    # Alcoholic Data Artifact (2025)
    alc_brands = ['Jinro', 'Ginebra San Miguel', 'Emperador', "Officer's Choice", 'Smirnoff', "McDowell's No.1", 'Imperial Blue', 'Tanduay', 'Royal Stag', 'Bacardi']
    alc_shares = np.array([4.5, 3.8, 3.2, 2.9, 2.7, 2.5, 2.3, 2.1, 1.9, 1.7])
    alc_sales = np.array([12.5, 10.6, 8.9, 8.1, 7.5, 7.0, 6.4, 5.8, 5.3, 4.7])
    
    # Print Tables
    print("2025 Top 10 Soft Drinks:")
    for rank, (brand, share, sale) in enumerate(zip(soft_brands, soft_shares, soft_sales), 1):
        print(f"{rank}. {brand}: {share}% share, ${sale}B sales")
    
    print("\n2025 Top 10 Alcoholic Beverages:")
    for rank, (brand, share, sale) in enumerate(zip(alc_brands, alc_shares, alc_sales), 1):
        print(f"{rank}. {brand}: {share}% share, ${sale}B sales")
    
    # Visualize Bar Charts
    fig, axs = plt.subplots(1, 2, figsize=(16, 6))
    
    axs[0].barh(soft_brands[::-1], soft_shares[::-1], color='blue')
    axs[0].set_xlabel('Market Share (%)')
    axs[0].set_title('Top 10 Soft Drinks 2025')
    axs[0].grid(axis='x')
    
    axs[1].barh(alc_brands[::-1], alc_shares[::-1], color='red')
    axs[1].set_xlabel('Market Share (%)')
    axs[1].set_title('Top 10 Alcoholic Beverages 2025')
    axs[1].grid(axis='x')
    
    plt.tight_layout()
    plt.savefig('beverage_markets_2025.png')
    plt.show()
    
    # Bonus: Chaos Sim for Market Volatility (Lorenz, tuned for beverage dynamics)
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
    xs[0], ys[0], zs[0] = (soft_shares[0]/5, alc_shares[0]/5, (soft_shares[0] + alc_shares[0])/10)  # Init with top shares scaled
    for i in range(num_steps):
        dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
        xs[i + 1] = xs[i] + (dx * dt)
        ys[i + 1] = ys[i] + (dy * dt)
        zs[i + 1] = zs[i] + (dz * dt)
    
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(xs, ys, zs, lw=0.5, color='green')
    ax.set_title('Beverage Market Chaos Sim (Lorenz Attractor)')
    ax.set_xlabel('Soft Drinks Leader Factor')
    ax.set_ylabel('Alcoholic Leader Factor')
    ax.set_zlabel('Combined Share Factor')
    plt.savefig('beverage_chaos_2025.png')
    plt.show()

if __name__ == "__main__":
    simulate_beverage_markets()