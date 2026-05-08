import os
import mujoco
import mujoco.viewer


def main():
    # 你的绝对路径（已直接写好）
    model_path = r"D:\nn\mujoco_menagerie\anybotics_anymal_b\anymal_b.xml"

    if not os.path.exists(model_path):
        print(f"❌ 模型文件不存在：{model_path}")
        return

    print(f"✅ 正在加载：ANYmal B 机器人")

    # 加载模型
    model = mujoco.MjModel.from_xml_path(model_path)
    data = mujoco.MjData(model)

    # 启动仿真窗口
    with mujoco.viewer.launch_passive(model, data) as viewer:
        print("🚀 仿真运行中，关闭窗口退出")
        while viewer.is_running():
            mujoco.mj_step(model, data)
            viewer.sync()


if __name__ == "__main__":
    main()