import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from pathlib import Path

# ==========================================
# 1. DATA LOADING (Or Mock Data Generation)
# ==========================================
def load_or_create_data():
    """
    Attempts to load your actual data. 
    If not found, generates mock data so you can see the graph logic work immediately.
    """
    data_path = Path('data/processed/training_data.csv')
    
    if data_path.exists():
        print(f"Loading actual data from {data_path}...")
        df = pd.read_csv(data_path)
        # Drop non-numeric columns for simplicity in this utility
        # Assuming 'waterlogged' is target based on your analyze_training_data.py
        X = df.drop('waterlogged', axis=1).select_dtypes(include=[np.number])
        y = df['waterlogged']
    else:
        print("Data file not found. Generating MOCK data for demonstration...")
        # creating synthetic waterlogging data
        np.random.seed(42)
        n_samples = 1000
        data = {
            'rainfall_current': np.random.uniform(0, 100, n_samples),
            'rainfall_3h': np.random.uniform(0, 150, n_samples),
            'elevation': np.random.uniform(190, 250, n_samples),
            'dist_drain': np.random.uniform(0, 5000, n_samples),
            'humidity': np.random.uniform(30, 90, n_samples)
        }
        X = pd.DataFrame(data)
        # Generate target: higher rain + lower elevation = waterlogged
        prob = (X['rainfall_current']/100 + (250-X['elevation'])/60) / 2
        y = (prob > 0.6).astype(int)
        
    return train_test_split(X, y, test_size=0.2, random_state=42)

# ==========================================
# 2. RANDOM FOREST ANALYSIS
# ==========================================
def analyze_random_forest(X_train, X_test, y_train, y_test):
    print("\nRunning Random Forest Analysis...")
    
    # Parameter to test: n_estimators (Number of trees)
    # Random Forest doesn't use 'learning_rate', it uses 'n_estimators' or 'max_depth'
    param_values = [10, 20, 50, 100, 200, 300, 500]
    accuracies = []
    
    for val in param_values:
        clf = RandomForestClassifier(n_estimators=val, random_state=42, n_jobs=-1)
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)
        acc = accuracy_score(y_test, preds)
        accuracies.append(acc)
        print(f"  n_estimators={val}: Accuracy={acc:.4f}")
        
    return param_values, accuracies

# ==========================================
# 3. GRADIENT BOOSTING ANALYSIS (For Alpha/Learning Rate)
# ==========================================
def analyze_gradient_boosting(X_train, X_test, y_train, y_test):
    print("\nRunning Gradient Boosting Analysis (Learning Rate)...")
    
    # Parameter to test: learning_rate (often called alpha)
    param_values = [0.001, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0]
    accuracies = []
    
    for val in param_values:
        clf = GradientBoostingClassifier(learning_rate=val, n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)
        acc = accuracy_score(y_test, preds)
        accuracies.append(acc)
        print(f"  learning_rate={val}: Accuracy={acc:.4f}")
        
    return param_values, accuracies

# ==========================================
# 4. PLOTTING FUNCTION
# ==========================================
def plot_results(rf_data, gb_data):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Random Forest
    rf_params, rf_acc = rf_data
    ax1.plot(rf_params, rf_acc, marker='o', color='green', linewidth=2)
    ax1.set_title('Random Forest: Accuracy vs n_estimators')
    ax1.set_xlabel('Number of Trees (n_estimators)')
    ax1.set_ylabel('Accuracy')
    ax1.grid(True)
    
    # Annotate max point
    max_acc_rf = max(rf_acc)
    best_param_rf = rf_params[rf_acc.index(max_acc_rf)]
    ax1.annotate(f'Optimal: {best_param_rf}\nAcc: {max_acc_rf:.4f}', 
                 xy=(best_param_rf, max_acc_rf), 
                 xytext=(best_param_rf, max_acc_rf - 0.02),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    # Plot 2: Gradient Boosting (Learning Rate)
    gb_params, gb_acc = gb_data
    ax2.plot(gb_params, gb_acc, marker='o', color='blue', linewidth=2)
    ax2.set_title('Gradient Boosting: Accuracy vs Learning Rate (Alpha)')
    ax2.set_xlabel('Learning Rate')
    ax2.set_ylabel('Accuracy')
    ax2.set_xscale('log') # Log scale is better for learning rate
    ax2.grid(True)
    
    # Annotate max point
    max_acc_gb = max(gb_acc)
    best_param_gb = gb_params[gb_acc.index(max_acc_gb)]
    ax2.annotate(f'Optimal: {best_param_gb}\nAcc: {max_acc_gb:.4f}', 
                 xy=(best_param_gb, max_acc_gb), 
                 xytext=(best_param_gb, max_acc_gb - 0.05),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    plt.tight_layout()
    
    # Save plot
    plt.savefig('hyperparameter_optimization.png')
    print("\nGraph saved as 'hyperparameter_optimization.png'")
    plt.show()

# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    # 1. Load Data
    X_train, X_test, y_train, y_test = load_or_create_data()
    
    # 2. Analyze Random Forest
    rf_results = analyze_random_forest(X_train, X_test, y_train, y_test)
    
    # 3. Analyze Gradient Boosting (for learning rate)
    gb_results = analyze_gradient_boosting(X_train, X_test, y_train, y_test)
    
    # 4. Draw Graphs
    plot_results(rf_results, gb_results)