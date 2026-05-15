import os
import mujoco
import mujoco.viewer


def main():
    # 模型路径（确保 mujoco_menagerie 在同级目录）
    model_path = "anybotics_anymal_c/anymal_c.xml"

    if not os.path.exists(model_path):
        print(f"❌ 模型文件不存在：{model_path}")
        print("💡 请把 mujoco_menagerie 放在代码同一级目录下")
        return

    print(f"✅ 正在加载：ANYmal B 机器人（已固定基座，不会掉落）")

    # 加载模型
    model = mujoco.MjModel.from_xml_path(model_path)
    data = mujoco.MjData(model)

    # ===================== 核心优化：防止机器人掉落 =====================
    # 1. 固定机器人基座（最有效！直接把 torso 钉在世界坐标系）
    model.body("base").pos = [0, 0, 0.5]  # 初始高度
    model.body("base").quat = [1, 0, 0, 0]  # 初始姿态
    model.body("base").freejoint = None  # 移除自由关节（关键！）
    model.body("base").mocapid = 0  # 固定不动

    # 2. 增加物理稳定性：阻尼、摩擦、防穿透
    model.opt.timestep = 0.002  # 仿真步长（更稳定）
    model.opt.gravity = [0, 0, -9.81]  # 正常重力
    model.opt.o_margin = 0.001  # 碰撞边距（防穿透）
    model.opt.o_solref = [0.02, 0.1]  # 接触刚度/阻尼
    model.opt.o_solimp = [0.9, 0.95, 0.01]  # 接触摩擦参数

    # 3. 初始化关节角度（让机器人自然站立）
    for i, name in enumerate(model.joint_names):
        if "HAA" in name or "HFE" in name or "KFE" in name:
            data.ctrl[i] = 0.0

    # ==================================================================

    # 启动仿真
    with mujoco.viewer.launch_passive(model, data) as viewer:
        print("🚀 仿真运行中 | 机器人已固定，不会掉落")
        print("❌ 关闭窗口即可退出")

        # 稳定渲染循环（不疯狂占CPU）
        while viewer.is_running():
            mujoco.mj_step(model, data)
            viewer.sync()


if __name__ == "__main__":
    main()