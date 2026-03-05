// Beverage Market Distribution Simulator (2025 Data)
// Compile/Run: rustc market_sim.rs && ./market_sim
// Outputs fits and sims to stdout; lightweight on your 64GB/6-core.

use std::f64::consts::E;

fn main() {
    // Soft shares (power-law sim)
    let soft_ranks: Vec<f64> = (1..=10).map(|x| x as f64).collect();
    let soft_shares: Vec<f64> = vec![22.1, 15.3, 8.2, 5.7, 4.9, 3.8, 3.5, 3.2, 2.9, 2.6];
    
    // Alc shares (linear-ish sim)
    let alc_shares: Vec<f64> = vec![4.5, 3.8, 3.2, 2.9, 2.7, 2.5, 2.3, 2.1, 1.9, 1.7];
    
    // Power-law fit params (from SciPy equiv: a * rank^(-b))
    let soft_a = 30.0; // Approx from data
    let soft_b = 1.2;
    let alc_a = 5.0;
    let alc_b = 0.3; // Shallower for linear approx
    
    println!("Simulated Soft Power-Law Shares:");
    for rank in 1..=10 {
        let share = soft_a * (rank as f64).powf(-soft_b);
        println!("Rank {}: {:.2}%", rank, share);
    }
    
    println!("\nSimulated Alc Near-Linear Shares:");
    for rank in 1..=10 {
        let share = alc_a * (rank as f64).powf(-alc_b); // Low b ≈ linear
        println!("Rank {}: {:.2}%", rank, share);
    }
    
    // Exponential decay sim (alternative fit)
    println!("\nExp Decay Sim for Soft:");
    let exp_a = 25.0;
    let exp_b = 0.3;
    for rank in 1..=10 {
        let share = exp_a * E.powf(-exp_b * rank as f64);
        println!("Rank {}: {:.2}%", rank, share);
    }
    
    // R² calc (manual impl for self-contained)
    fn r_squared(y: &Vec<f64>, y_fit: &Vec<f64>) -> f64 {
        let mean_y = y.iter().sum::<f64>() / y.len() as f64;
        let ss_res: f64 = y.iter().zip(y_fit).map(|(&yi, &yfi)| (yi - yfi).powi(2)).sum();
        let ss_tot: f64 = y.iter().map(|&yi| (yi - mean_y).powi(2)).sum();
        1.0 - (ss_res / ss_tot)
    }
    
    // Compute for soft power fit
    let soft_fit: Vec<f64> = soft_ranks.iter().map(|&r| soft_a * r.powf(-soft_b)).collect();
    let soft_r2 = r_squared(&soft_shares, &soft_fit);
    println!("\nSoft Power R²: {:.3}", soft_r2);
    
    // Alc
    let alc_fit: Vec<f64> = soft_ranks.iter().map(|&r| alc_a * r.powf(-alc_b)).collect();
    let alc_r2 = r_squared(&alc_shares, &alc_fit);
    println!("Alc Near-Lin R²: {:.3}", alc_r2);
}