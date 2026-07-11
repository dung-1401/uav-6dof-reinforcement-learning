#!/usr/bin/env python3
"""
Script kiểm tra cài đặt toàn bộ thư viện cần thiết
"""

import sys
from packaging import version

def check_module(module_name, min_version=None):
    """Kiểm tra xem module có được cài đặt không"""
    try:
        module = __import__(module_name)
        v = getattr(module, '__version__', 'unknown')
        
        status = "✅"
        if min_version and v != 'unknown':
            if version.parse(v) < version.parse(min_version):
                status = "⚠️"
        
        print(f"{status} {module_name:20} v{v}")
        return True
    except ImportError:
        print(f"❌ {module_name:20} NOT INSTALLED")
        return False

print("\n" + "="*60)
print("   🔍 KIỂM TRA CÀI ĐẶT - 6-DoF UAV CONTROL")
print("="*60 + "\n")

# Kiểm tra Python version
py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
print(f"Python Version: {py_version}")
if sys.version_info >= (3, 8):
    print("✅ Python version OK\n")
else:
    print("❌ Cần Python 3.8+\n")

# Kiểm tra các thư viện
print("Checking installed packages:\n")

all_ok = True
all_ok &= check_module('numpy', '1.21.0')
all_ok &= check_module('matplotlib', '3.5.0')
all_ok &= check_module('torch', '1.10.0')
all_ok &= check_module('gymnasium', '0.27.0')
all_ok &= check_module('stable_baselines3', '2.0.0')

print()

# Kiểm tra PyTorch CUDA
print("="*60)
print("PyTorch Hardware Check:")
print("="*60 + "\n")

try:
    import torch
    print(f"PyTorch Version: {torch.__version__}")
    print(f"CUDA Available: {'✅ YES' if torch.cuda.is_available() else '❌ NO (CPU Only)'}")
    
    if torch.cuda.is_available():
        print(f"CUDA Version: {torch.version.cuda}")
        print(f"GPU Name: {torch.cuda.get_device_name(0)}")
        print(f"GPU Count: {torch.cuda.device_count()}")
        
        # Memory check
        device_prop = torch.cuda.get_device_properties(0)
        total_memory = device_prop.total_memory / (1024**3)  # Convert to GB
        print(f"GPU Memory: {total_memory:.2f} GB")
    else:
        print("⚠️  Will run on CPU (much slower)")
        print("   Consider installing CUDA for faster training")
        
except Exception as e:
    print(f"Error checking PyTorch: {e}")

print()

# Kiểm tra Gymnasium environment
print("="*60)
print("Gymnasium Environment Check:")
print("="*60 + "\n")

try:
    import gymnasium as gym
    
    # Test tạo environment đơn giản
    print("Testing basic Gymnasium environment...")
    env = gym.make('CartPole-v1')
    print(f"✅ Can create Gymnasium environments")
    print(f"   Action space: {env.action_space}")
    print(f"   Observation space: {env.observation_space}")
    env.close()
    
except Exception as e:
    print(f"❌ Error with Gymnasium: {e}")

print()

# Kiểm tra Stable-Baselines3
print("="*60)
print("Stable-Baselines3 Check:")
print("="*60 + "\n")

try:
    from stable_baselines3 import SAC
    print("✅ SAC algorithm available")
    
    # Test tạo model đơn giản
    env = gym.make('Pendulum-v1')
    model = SAC('MlpPolicy', env, verbose=0)
    print("✅ Can create SAC model")
    env.close()
    
except Exception as e:
    print(f"❌ Error with Stable-Baselines3: {e}")

print()

# Kiểm tra Matplotlib
print("="*60)
print("Matplotlib Check:")
print("="*60 + "\n")

try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    print("✅ Matplotlib available")
    print("✅ 3D plotting available")
    
    # Test save figure
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot([0, 1], [0, 1], [0, 1])
    fig.savefig('/tmp/test_plot.png', dpi=100)
    print("✅ Can save PNG files")
    plt.close('all')
    
except Exception as e:
    print(f"❌ Error with Matplotlib: {e}")

print()

# Tóm tắt
print("="*60)
if all_ok:
    print("✅ All packages installed correctly!")
    print("   You can now run: python advanced_6dof_uav_sac.py")
else:
    print("❌ Some packages missing!")
    print("   Run: pip install -r requirements.txt")
print("="*60 + "\n")

# Gợi ý
print("💡 Tips:")
print("  - For faster training, use NVIDIA GPU (CUDA)")
print("  - For first run, use: total_steps = 50000 (faster)")
print("  - For better results, use: total_steps = 500000 (slower)")
print()
