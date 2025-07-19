"""
测试mesh_inpaint_processor模块是否编译成功
"""
import sys
import os

def test_module_import():
    """测试模块导入"""
    try:
        import mesh_inpaint_processor
        print("✅ 模块导入成功!")
        return True
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_module_functions():
    """测试模块函数"""
    try:
        import mesh_inpaint_processor
        
        # 检查函数是否存在
        functions = ['meshVerticeInpaint', 'meshVerticeColor']
        for func_name in functions:
            if hasattr(mesh_inpaint_processor, func_name):
                print(f"✅ 函数 {func_name} 存在")
            else:
                print(f"❌ 函数 {func_name} 不存在")
                return False
        
        # 获取帮助信息
        print("\n📖 模块帮助信息:")
        help(mesh_inpaint_processor)
        
        return True
    except Exception as e:
        print(f"❌ 函数测试失败: {e}")
        return False

def main():
    print("=" * 50)
    print("mesh_inpaint_processor 模块测试")
    print("=" * 50)
    
    print(f"Python版本: {sys.version}")
    print(f"当前目录: {os.getcwd()}")
    print()
    
    # 测试导入
    if not test_module_import():
        return
    
    # 测试函数
    test_module_functions()
    
    print("\n🎉 所有测试完成!")

if __name__ == "__main__":
    main() 