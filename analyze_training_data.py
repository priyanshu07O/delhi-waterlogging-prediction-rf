"""
Analyze training data to understand the model's behavior
"""
import pandas as pd
import numpy as np

print('='*70)
print('TRAINING DATA ANALYSIS')
print('='*70)

df = pd.read_csv('data/processed/training_data.csv')

print(f'\nTotal samples: {len(df)}')
print(f'Waterlogged: {df["waterlogged"].sum()} ({df["waterlogged"].mean()*100:.1f}%)')
print(f'Non-waterlogged: {(df["waterlogged"]==0).sum()} ({(df["waterlogged"]==0).mean()*100:.1f}%)')

print('\n' + '='*70)
print('RAINFALL DISTRIBUTION')
print('='*70)
print('\nWaterlogged samples rainfall stats:')
print(df[df['waterlogged']==1]['rainfall_current'].describe())

print('\nNon-waterlogged samples rainfall stats:')
print(df[df['waterlogged']==0]['rainfall_current'].describe())

print('\n' + '='*70)
print('LOCATION FEATURE ANALYSIS')
print('='*70)
print('\nNear known location distribution:')
print(f"Waterlogged samples near known locations: {(df[df['waterlogged']==1]['near_known_location']==1).sum()}/{len(df[df['waterlogged']==1])}")
print(f"Non-waterlogged samples near known locations: {(df[df['waterlogged']==0]['near_known_location']==1).sum()}/{len(df[df['waterlogged']==0])}")

print('\n' + '='*70)
print('PROBLEM DIAGNOSIS')
print('='*70)

# Check if all waterlogged samples are near known locations
waterlogged = df[df['waterlogged']==1]
all_near = (waterlogged['near_known_location'] == 1).all()
print(f"\nALL waterlogged samples near known locations? {all_near}")

if all_near:
    print("\n⚠️  ISSUE FOUND: Model learned 'near_known_location' = waterlogged")
    print("   This creates a perfect correlation, ignoring rainfall!")
    
print('\nSample waterlogged records:')
print(df[df['waterlogged']==1][['rainfall_current', 'near_known_location', 'distance_to_known_location']].head(10))
