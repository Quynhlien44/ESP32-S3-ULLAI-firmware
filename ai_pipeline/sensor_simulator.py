import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-display backend
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
import os

# =============================================================================
# 1. ADVANCED SIMULATION CONFIGURATION FOR EACH SENSOR
# =============================================================================

class SensorProfiler:
    """Class for creating sensor profiles based on real datasheets"""
    
    # Technical specifications from datasheet
    NSL_19M51 = {
        'min_v': 0.18,      # Minimum voltage (0 lux)
        'max_v': 2.7,       # Maximum voltage (1000 lux)
        'response_time': 0.015,  # 15ms
        'dark_current': 0.18,
        'noise_profile': lambda: random.gauss(0, 0.03)
    }
    
    DHT22 = {
        'temp_range': (-40, 80),
        'humidity_range': (0, 100),
        'temp_accuracy': 0.5,
        'humidity_accuracy': 2.0,
        'response_time': 2.0    # 2 seconds
    }
    
    SGP30 = {
        'tvoc_range': (0, 60000),
        'co2eq_range': (400, 60000),
        'baseline_drift': 0.1,  # 10%/hour
        'noise_factor': 0.05
    }

# =============================================================================
# 2. DATA MODELING BY SCENARIO
# =============================================================================

def generate_scenario_data(scenario, duration_sec=300, sample_rate=10):
    """
    Generate sensor data for each scenario
    - duration_sec: Sample duration (seconds) - SHORTENED TO 5 MINUTES FOR TESTING
    - sample_rate: Samples per second (Hz)
    """
    n_samples = duration_sec * sample_rate
    timestamps = [datetime.now() + timedelta(seconds=i/sample_rate) 
                 for i in range(n_samples)]
    
    # Initialize data structure with float type
    data = {
        'timestamp': timestamps,
        'scenario': [scenario] * n_samples,
        'light_v': np.zeros(n_samples, dtype=np.float64),
        'temp_c': np.zeros(n_samples, dtype=np.float64),
        'humidity_pct': np.zeros(n_samples, dtype=np.float64),
        'tvoc_ppb': np.zeros(n_samples, dtype=np.float64),
        'co2eq_ppm': np.zeros(n_samples, dtype=np.float64),
        'anomaly_flag': np.zeros(n_samples, dtype=np.int32)
    }
    
    # Generate base data
    base_values = {
        'normal': {'light': 1.2, 'temp': 25.0, 'humidity': 45.0, 'tvoc': 60.0, 'co2': 450.0},
        'high_temp': {'light': 1.5, 'temp': 38.0, 'humidity': 25.0, 'tvoc': 70.0, 'co2': 500.0},
        'high_humidity': {'light': 0.9, 'temp': 28.0, 'humidity': 85.0, 'tvoc': 120.0, 'co2': 600.0},
        'poor_air': {'light': 1.0, 'temp': 26.0, 'humidity': 50.0, 'tvoc': 300.0, 'co2': 1200.0},
        'rapid_change': {'light': 1.2, 'temp': 25.0, 'humidity': 45.0, 'tvoc': 60.0, 'co2': 450.0}
    }[scenario]
    
    # Apply sensor profile
    data['light_v'] = simulate_nsl19m51(base_values['light'], n_samples, sample_rate)
    data['temp_c'], data['humidity_pct'] = simulate_dht22(
        base_values['temp'], base_values['humidity'], n_samples, sample_rate
    )
    data['tvoc_ppb'], data['co2eq_ppm'] = simulate_sgp30(
        base_values['tvoc'], base_values['co2'], n_samples, sample_rate
    )
    
    # Add special events and noise
    apply_scenario_effects(data, scenario, sample_rate)
    inject_anomalies(data, scenario)
    
    return pd.DataFrame(data)

# =============================================================================
# 3. ADVANCED SENSOR SIMULATION - BUG FIXED
# =============================================================================

def simulate_nsl19m51(base_voltage, n_samples, sample_rate):
    """Simulate NSL 19M51 with real physical characteristics"""
    p = SensorProfiler.NSL_19M51
    data = np.full(n_samples, base_voltage, dtype=np.float64)
    
    # Add measurement noise
    noise = np.array([p['noise_profile']() for _ in range(n_samples)], dtype=np.float64)
    data += noise
    
    # Simulate response time
    response_filter = np.exp(-np.arange(0, 5) / (p['response_time'] * sample_rate))
    response_filter /= response_filter.sum()
    data = np.convolve(data, response_filter, mode='same')
    
    return np.clip(data, p['min_v'], p['max_v'])

def simulate_dht22(base_temp, base_humidity, n_samples, sample_rate):
    """Simulate DHT22 with characteristic delay (BUG FIXED)"""
    p = SensorProfiler.DHT22
    temp = np.full(n_samples, base_temp, dtype=np.float64)
    humidity = np.full(n_samples, base_humidity, dtype=np.float64)
    
    # Natural temperature variation
    temp_variation = 0.5 * np.sin(np.linspace(0, 20*np.pi, n_samples))
    temp += temp_variation
    
    # Temperature-humidity relationship
    humidity = humidity * (1 - 0.002 * (temp - base_temp))
    
    # Add noise
    temp += np.random.normal(0, 0.2, n_samples).astype(np.float64)
    humidity += np.random.normal(0, 0.5, n_samples).astype(np.float64)
    
    # Simulate measurement delay
    update_interval = 2 * sample_rate  # Update every 2 seconds
    for i in range(update_interval, n_samples, update_interval):
        # Hold value steady for 2 seconds
        temp[i:i+update_interval] = temp[i]
        humidity[i:i+update_interval] = humidity[i]
    
    return (
        np.clip(temp, *p['temp_range']),
        np.clip(humidity, *p['humidity_range'])
    )

def simulate_sgp30(base_tvoc, base_co2, n_samples, sample_rate):
    """Simulate SGP30 with baseline drift phenomenon"""
    p = SensorProfiler.SGP30
    tvoc = np.full(n_samples, base_tvoc, dtype=np.float64)
    co2 = np.full(n_samples, base_co2, dtype=np.float64)
    
    # Baseline drift over time
    drift = np.linspace(0, p['baseline_drift'], n_samples, dtype=np.float64)
    tvoc *= (1 + drift)
    co2 *= (1 + drift * 0.8)
    
    # TVOC-CO2 correlation
    co2 = co2 + 0.2 * (tvoc - base_tvoc)
    
    # Add noise
    noise_tvoc = np.random.normal(0, p['noise_factor'], n_samples)
    noise_co2 = np.random.normal(0, p['noise_factor'], n_samples)
    tvoc *= (1 + noise_tvoc)
    co2 *= (1 + noise_co2)
    
    return (
        np.clip(tvoc, *p['tvoc_range']),
        np.clip(co2, *p['co2eq_range'])
    )

# =============================================================================
# 4. SCENARIO EFFECTS & ANOMALIES - PERFORMANCE OPTIMIZED
# =============================================================================

def apply_scenario_effects(data, scenario, sample_rate):
    """Apply characteristic effects for each scenario"""
    n_samples = len(data['temp_c'])
    
    if scenario == 'high_temp':
        # Linear temperature increase + oscillation
        linear_increase = np.linspace(0, 10, n_samples, dtype=np.float64)
        oscillation = 2 * np.sin(np.linspace(0, 8*np.pi, n_samples))
        data['temp_c'] += linear_increase + oscillation
        
    elif scenario == 'high_humidity':
        # Exponential increase in humidity
        ramp = np.geomspace(1, 3, n_samples//2, dtype=np.float64)
        reversed_ramp = ramp[::-1]
        data['humidity_pct'] = np.concatenate((
            data['humidity_pct'][:n_samples//2] * ramp,
            data['humidity_pct'][n_samples//2:] * reversed_ramp
        ))
        
    elif scenario == 'poor_air':
        # Periodic TVOC/CO2 spikes
        for start in range(200, n_samples, 300):
            end = min(start + 20, n_samples)
            data['tvoc_ppb'][start:end] *= 3.0
            data['co2eq_ppm'][start:end] *= 1.8
            
    elif scenario == 'rapid_change':
        # Sudden changes in all three parameters
        transitions = [
            (100, {'light': 2.5, 'temp': -5, 'humidity': -30}),
            (300, {'light': 0.3, 'temp': +15, 'humidity': +40}),
            (500, {'light': 1.8, 'temp': -8, 'humidity': -20})
        ]
        
        for frame, changes in transitions:
            idx = frame * sample_rate
            if idx < n_samples:
                data['light_v'][idx:] += changes['light']
                data['temp_c'][idx:] += changes['temp']
                data['humidity_pct'][idx:] += changes['humidity']

def inject_anomalies(data, scenario):
    """Inject real-world anomalies into the data"""
    n_samples = len(data['temp_c'])
    anomaly_prob = 0.002  # 0.2% chance of anomaly
    
    # Short anomaly - Noise spike
    short_anomalies = max(1, int(n_samples * anomaly_prob))
    for _ in range(short_anomalies):
        idx = random.randint(10, n_samples-10)
        sensor = random.choice(['light_v', 'temp_c', 'humidity_pct'])
        
        # Create noise spike
        anomaly_factor = random.choice([0.1, 2.0, 5.0])
        data[sensor][idx] *= anomaly_factor
        data['anomaly_flag'][idx] = 1
        
        # Decay effect
        decay_length = random.randint(3, 5)
        decay = np.linspace(1.0, 0.1, decay_length)
        for i in range(1, decay_length):
            if idx+i < n_samples:
                data[sensor][idx+i] = data[sensor][idx] * decay[i]
                data['anomaly_flag'][idx+i] = 2

    # Long anomaly - Sensor failure
    if scenario != 'rapid_change':
        long_duration = random.randint(50, 200)  # 5-20 seconds
        start_idx = random.randint(100, n_samples-long_duration)
        affected_sensor = random.choice(['tvoc_ppb', 'co2eq_ppm'])
        
        # Static value error
        static_value = np.mean(data[affected_sensor]) * random.choice([0.2, 0.5, 1.5])
        data[affected_sensor][start_idx:start_idx+long_duration] = static_value
        data['anomaly_flag'][start_idx:start_idx+long_duration] = 3

# =============================================================================
# 5. DATA PROCESSING & VISUALIZATION - OPTIMIZED
# =============================================================================

def visualize_scenario(df, scenario):
    """Visualize sensor data for the scenario"""
    try:
        fig, axs = plt.subplots(5, 1, figsize=(15, 20), sharex=True)
        fig.suptitle(f'Sensor Data Simulation: {scenario} Scenario', fontsize=16)
        
        # Light Sensor
        axs[0].plot(df['timestamp'], df['light_v'], 'b-')
        axs[0].set_ylabel('Light (V)')
        axs[0].grid(True)
        
        # Temperature
        axs[1].plot(df['timestamp'], df['temp_c'], 'r-')
        axs[1].set_ylabel('Temp (°C)')
        axs[1].grid(True)
        
        # Humidity
        axs[2].plot(df['timestamp'], df['humidity_pct'], 'g-')
        axs[2].set_ylabel('Humidity (%)')
        axs[2].grid(True)
        
        # Air Quality
        axs[3].plot(df['timestamp'], df['tvoc_ppb'], 'm-', label='TVOC')
        axs[3].set_ylabel('TVOC (ppb)')
        axs[3].grid(True)
        
        axs[4].plot(df['timestamp'], df['co2eq_ppm'], 'c-', label='CO2eq')
        axs[4].set_ylabel('CO2eq (ppm)')
        axs[4].set_xlabel('Timestamp')
        axs[4].grid(True)
        
        # Mark anomaly points
        anomalies = df[df['anomaly_flag'] > 0]
        for _, row in anomalies.iterrows():
            color = {1: 'red', 2: 'orange', 3: 'purple'}.get(row['anomaly_flag'], 'gray')
            for ax in axs:
                ax.axvline(x=row['timestamp'], color=color, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{scenario}_sensor_data.png', dpi=150)
        plt.close()
    except Exception as e:
        print(f"Visualization error for {scenario}: {str(e)}")

# =============================================================================
# 6. MAIN EXECUTION & DATA EXPORT - STABLE VERSION
# =============================================================================

def main():
    scenarios = [
        'normal', 
        'high_temp', 
        'high_humidity', 
        'poor_air', 
        'rapid_change'
    ]
    
    full_dataset = pd.DataFrame()
    
    # Create output directory if it does not exist
    os.makedirs('simulation_output', exist_ok=True)
    
    for scenario in scenarios:
        print(f"Generating {scenario} scenario data...")
        try:
            scenario_df = generate_scenario_data(scenario, duration_sec=300)  # Only 5 minutes/scenario
            visualize_scenario(scenario_df, scenario)
            
            # Save image to output directory
            if os.path.exists(f'{scenario}_sensor_data.png'):
                os.rename(f'{scenario}_sensor_data.png', f'simulation_output/{scenario}_sensor_data.png')
            
            full_dataset = pd.concat([full_dataset, scenario_df])
        except Exception as e:
            print(f"Error generating {scenario} data: {str(e)}")
    
    # Export data
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"simulation_output/ullai_sensor_data_{timestamp_str}.csv"
    full_dataset.to_csv(filename, index=False)
    
    print("\n" + "="*50)
    print(f"Dataset generated successfully: {filename}")
    print(f"Total samples: {len(full_dataset)}")
    print(f"Scenarios: {', '.join(scenarios)}")
    print("="*50)
    
    # Statistical report
    try:
        report = full_dataset.groupby('scenario').agg({
            'light_v': ['min', 'max', 'mean'],
            'temp_c': ['min', 'max', 'mean'],
            'humidity_pct': ['min', 'max', 'mean'],
            'tvoc_ppb': ['min', 'max', 'mean'],
            'co2eq_ppm': ['min', 'max', 'mean'],
            'anomaly_flag': lambda x: (x > 0).sum()
        })
        print("\nStatistical Summary:")
        print(report)
        
        # Save report
        report.to_csv(f'simulation_output/summary_report_{timestamp_str}.csv')
    except Exception as e:
        print(f"Error generating report: {str(e)}")

if __name__ == "__main__":
    main()
