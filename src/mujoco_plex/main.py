import os
import time
from typing import Optional, Tuple

import mujoco
import mujoco.viewer

# ===================== 配置区（集中管理，便于修改）=====================
CONFIG = {
    "model_path": "anybotics_anymal_c/anymal_c.xml",
    "base_body_name": "base",
    "base_position": (0.0, 0.0, 0.5),
    "base_orientation": (1.0, 0.0, 0.0, 0.0),  # wxyz
    "sim_time_step": 0.002,
    "gravity": (0.0, 0.0, -9.81),
    "target_fps": 60,
}

# ===================== 工具函数 =====================
def load_mujoco_model(model_path: str) -> Optional[Tuple[mujoco.MjModel, mujoco.MjData]]:
    """加载 MuJoCo 模型并返回 model + data，带完整路径与异常校验"""
    if not isinstance(model_path, str):
        print(f"❌ 模型路径必须是字符串，当前类型：{type(model_path)}")
        return None

    abs_path = os.path.abspath(model_path)
    if not os.path.isfile(abs_path):
        print(f"❌ 模型文件不存在：{abs_path}")
        return None

    try:
        model = mujoco.MjModel.from_xml_path(abs_path)
        data = mujoco.MjData(model)
        print(f"✅ 模型加载成功：{abs_path}")
        return model, data
    except Exception as e:
        print(f"❌ 模型加载失败：{str(e)}")
        return None

# ===================== 机器人配置 =====================
def configure_robot(model: mujoco.MjModel, data: mujoco.MjData) -> None:
    """统一配置机器人初始位姿、仿真参数、控制量"""
    # 基座位姿（安全判断 + 配置化）
    base_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, CONFIG["base_body_name"])
    if base_id >= 0:
        model.body_pos[base_id][:3] = CONFIG["base_position"]
        model.body_quat[base_id][:4] = CONFIG["base_orientation"]

    # 仿真参数
    model.opt.timestep = CONFIG["sim_time_step"]
    model.opt.gravity[:] = CONFIG["gravity"]

    # 初始化控制量
    data.ctrl[:] = 0.0

# ===================== 仿真主循环 =====================
def run_simulation(model: mujoco.MjModel, data: mujoco.MjData) -> None:
    """启动被动查看器，稳定帧率仿真"""
    print("✅ 仿真启动成功 | 关闭窗口退出")
    frame_interval = 1.0 / CONFIG["target_fps"]

    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            step_start = time.perf_counter()

            # 一步仿真
            mujoco.mj_step(model, data)
            viewer.sync()

            # 精准帧率控制（使用 perf_counter 更精确）
            elapsed = time.perf_counter() - step_start
            if elapsed < frame_interval:
                time.sleep(frame_interval - elapsed)

# ===================== 主入口 =====================
def main() -> None:
    model_data = load_mujoco_model(CONFIG["model_path"])
    if not model_data:
        return

    model, data = model_data
    configure_robot(model, data)
    run_simulation(model, data)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n✅ 手动退出程序")
    except Exception as e:
        print(f"\n❌ 运行异常：{e}")