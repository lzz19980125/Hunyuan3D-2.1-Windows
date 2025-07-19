# Hunyuan3D 2.1 - Windows Compatible Version

> <img width="14" height="14" alt="image" src="https://github.com/user-attachments/assets/341fc624-e03b-4934-b3a0-f96fa4f0deb6" />  **This is a Windows-optimized version of Hunyuan3D 2.1** that addresses common compatibility issues on Windows systems, including fixes for DeepSpeed compatibility issues with the Windows environment, **custom_rasterizer** installation errors, **DifferentiableRenderer** installation errors, and environment-specific bugs.

## 🛠️ Windows Installation Guide

We test our model on one 4080 GPU with Python 3.10 and PyTorch 2.5.1+cu124.

### Prerequisites

- **OS**: Windows 11
- **GPU**: NVIDIA GPU with 10GB+ VRAM (recommended)
- **Python**: 3.10 
- **CUDA**: 12.1   (Although the host system is running CUDA 12.1, the Miniconda virtual environment uses the PyTorch build for CUDA 12.4 (cu124). Testing in this specific configuration has been completed with no errors found.)

### Environment Setup

```bash
conda create -n hunyuan3D python=3.10 -y
conda activate hunyuan3D

pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124

pip install deepspeed==0.11.2

pip install -r requirements.txt

cd hy3dpaint/custom_rasterizer
pip install -e .
cd ../..

cd hy3dpaint/DifferentiableRenderer
pip install -e .
cd ../..

wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P hy3dpaint/ckpt

# Main models cache (auto-created):
mkdir "C:\Users\%USERNAME%\.cache\hy3dgen\tencent\Hunyuan3D-2.1\hunyuan3d-dit-v2-1"
wget  https://huggingface.co/tencent/Hunyuan3D-2.1/resolve/main/hunyuan3d-dit-v2-1/config.yaml -P C:\Users\%USERNAME%\.cache\hy3dgen\tencent\Hunyuan3D-2.1
wget https://huggingface.co/tencent/Hunyuan3D-2.1/resolve/main/hunyuan3d-dit-v2-1/model.fp16.ckpt -P C:\Users\%USERNAME%\.cache\hy3dgen\tencent\Hunyuan3D-2.1
```

> **⚠️ Important**: The installation order is critical. PyTorch must be installed first, then deepspeed 0.11.2, then the remaining requirements. This prevents version conflicts that can occur on Windows.

**Then Manual Model Download**

```bash
# Create directory for background removal model
mkdir "C:\Users\%USERNAME%\.u2net"

# Download u2net.onnx manually from:
# https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx
# Place it in: C:\Users\%USERNAME%\.u2net\u2net.onnx
```

### Step 2: Launch Application

```bash
# Set environment variables for SSL bypass
set HF_HUB_DISABLE_SSL_VERIFY=1
set CURL_CA_BUNDLE=

# Run with texture generation disabled
python gradio_app.py --model_path tencent/Hunyuan3D-2.1 --subfolder hunyuan3d-dit-v2-1 --low_vram_mode --disable_tex
```

> **🔧 Windows Compilation Notes:**
> - **Visual Studio Build Tools required (Successfully tested with Visual Studio 2022)**: Download from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
> - **Custom fixes included**: Modified setup.py with Windows-specific compiler flags
> - **C++ compatibility**: Added required headers (`<array>`, `<utility>`, `<iostream>`) for Windows compilation

## 🐛 Windows-Specific Fixes Included

### 1. Deep Learning Dependencies Fix

**Problem**: Version conflicts between PyTorch, DeepSpeed, and other dependencies

**Solution**: Specific installation order with compatible versions

```bash
# Critical installation sequence:
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124
pip install deepspeed==0.11.2  # Must be this version for Windows
pip install -r requirements.txt
```

### 2. C++ Compilation Fixes

**Problem**: CUDA extensions fail to compile on Windows due to compiler compatibility issues

**Solutions Applied**:

#### A. Custom Rasterizer Fixes (`hy3dpaint/custom_rasterizer/setup.py`)
```python
# Added Windows-specific compiler flags
if os.name == 'nt':  # Windows
    extra_compile_args = {
        'cxx': ['/wd4838', '/D_ALLOW_COMPILER_AND_STL_VERSION_MISMATCH'], 
        'nvcc': ['-allow-unsupported-compiler', '-D_ALLOW_COMPILER_AND_STL_VERSION_MISMATCH']
    }
    # Disable ninja for stability
    cmdclass={"build_ext": BuildExtension.with_options(use_ninja=False)}
```

#### B. CUDA GPU Kernel Fixes (`rasterizer_gpu.cu`)
```cpp
// Fixed line 49-50: Changed data type casting for Windows compatibility
// Original:
z_min.data_ptr<long>()
// Fixed:
z_min.data_ptr<int64_t>()
```

#### C. Mesh Inpaint Processor Fixes (`DifferentiableRenderer/`)

**New Files Added:**
- `setup.py` - Cross-platform compilation setup

**C++ Header Fixes** (`mesh_inpaint_processor.cpp`):
```cpp
// Added missing headers for Windows compilation
#include <array>      // For std::array support
#include <utility>    // For std::pair, std::move
#include <iostream>   // For debug output support
```

### 3. Torchvision Compatibility Fix

**Problem**: `ModuleNotFoundError: No module named 'torchvision.transforms.functional_tensor'`

**Solution**: Automatic compatibility layer in `torchvision_fix.py`
```python
# Automatically applied on startup
from torchvision_fix import apply_fix
apply_fix()
```

### 2. SSL Connection Issues

**Problem**: `SSLZeroReturnError` when downloading models

**Solutions**:
- **Environment Variables**: Set `HF_HUB_DISABLE_SSL_VERIFY=1`
- **Mirror Sites**: Use `https://hf-mirror.com` instead of `huggingface.co`
- **Manual Download**: Download models manually and place in cache directories

### 3. Background Removal (rembg) Issues

**Problem**: Numba/LLVM compilation errors on Windows

**Solutions**:

- **Quick Fix**: Use `--disable_tex` parameter
- **Advanced**: Install proper C++ build tools and recompile

### 4. Network Download Issues

**Manual Download Locations**:
```bash
# Main models cache (auto-created):
C:\Users\%USERNAME%\.cache\hy3dgen\tencent\Hunyuan3D-2.1\hunyuan3d-dit-v2-1\config.yaml
C:\Users\%USERNAME%\.cache\hy3dgen\tencent\Hunyuan3D-2.1\hunyuan3d-dit-v2-1\model.fp16.ckpt

# Background removal model:
C:\Users\%USERNAME%\.u2net\u2net.onnx

# Real-ESRGAN model:
hy3dpaint\ckpt\RealESRGAN_x4plus.pth
```

## 🎯 Usage Examples

### API Usage:
```python
import sys
sys.path.insert(0, './hy3dshape')
sys.path.insert(0, './hy3dpaint')

# Apply Windows compatibility fix
from torchvision_fix import apply_fix
apply_fix()

from hy3dshape.pipelines import Hunyuan3DDiTFlowMatchingPipeline

# Generate 3D shape
shape_pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained('tencent/Hunyuan3D-2.1')
mesh_untextured = shape_pipeline(image='assets/demo.png')[0]

# If texture generation is working:
# from textureGenPipeline import Hunyuan3DPaintPipeline, Hunyuan3DPaintConfig
# paint_pipeline = Hunyuan3DPaintPipeline(Hunyuan3DPaintConfig(max_num_view=6, resolution=512))
# mesh_textured = paint_pipeline(mesh_path, image_path='assets/demo.png')
```

### Gradio App

You could also host a [Gradio](https://www.gradio.app/) App in your own computer via:

```bash
python gradio_app.py --model_path tencent/Hunyuan3D-2.1 --subfolder hunyuan3d-dit-v2-1 --low_vram_mode --disable_tex
```



## 🔧 Troubleshooting

### Common Issues:

1. **"SSLError" or "Connection refused"**:
   ```bash
   set HF_HUB_DISABLE_SSL_VERIFY=1
   set CURL_CA_BUNDLE=
   ```

2. **"functional_tensor not found"**:
   
- Already fixed automatically in this version
  
3. **"CUDA out of memory"**:
   ```bash
   python gradio_app.py --low_vram_mode --disable_tex
   ```

4. **"Build tools missing"**:
   - Install Visual Studio Build Tools
   - Or use `--disable_tex` to skip compilation

5. **Models not downloading**:
   - Check internet connection
   - Use manual download links provided above
   - Try using mirror sites

## 🔗 Community Resources

| Platform | Link | Description |
|----------|------|-------------|
| Original Repo | [Hunyuan3D-2.1](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1) | Official repository |

---

<img width="14" height="14" alt="image" src="https://github.com/user-attachments/assets/341fc624-e03b-4934-b3a0-f96fa4f0deb6" />  **Windows users**: If you encounter issues not covered here, please open an issue with your system specifications and error logs. 
