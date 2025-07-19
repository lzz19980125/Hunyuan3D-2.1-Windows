from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir
import pybind11
from setuptools import setup, Extension
import sys
import platform

# 定义编译选项
compile_args = []
link_args = []

if platform.system() == "Windows":
    if sys.platform == "win32":
        # Windows MSVC编译器选项
        compile_args = ['/O2', '/std:c++14', '/utf-8']
    else:
        # MinGW编译器选项
        compile_args = ['-O3', '-std=c++14']
        link_args = ['-static-libgcc', '-static-libstdc++']
else:
    # Linux/macOS编译器选项
    compile_args = ['-O3', '-std=c++14']

# 定义扩展模块
ext_modules = [
    Pybind11Extension(
        "mesh_inpaint_processor",
        [
            "mesh_inpaint_processor.cpp",
        ],
        include_dirs=[
            pybind11.get_include(),
        ],
        language='c++',
        cxx_std=14,
        extra_compile_args=compile_args,
        extra_link_args=link_args,
    ),
]

setup(
    name="mesh_inpaint_processor",
    version="1.0.0",
    author="Hunyuan3D",
    description="Mesh inpainting processor for Hunyuan3D",
    long_description="A Python extension module for mesh vertex inpainting and coloring operations.",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[
        "pybind11>=2.6.0",
        "numpy",
    ],
) 