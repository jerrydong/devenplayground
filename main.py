import logging
from environment import setup_environment, calculate_metrics
from algorithms.neural_ahpp import NeuralAHPP
from algorithms.uav_dppa_dwa import UAV_DPPA_DWA
from algorithms.masac import MASAC
from utils import plot_results, plot_composite_results, plot_3d, calculate_metrics  # 导入新函数
from config import ENV_SIZE, NUM_OBSTACLES, SCENARIOS
import time
import os
from datetime import datetime  # 用于生成时间戳
import matplotlib.pyplot as plt  # 确保这里导入了 pyplot

def setup_logging():
    # 创建 logs 文件夹（如果不存在）
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # 生成日志文件名
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"log_{timestamp}.txt")

    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # 同时打印到控制台
        ]
    )

    logging.info(f"日志记录到文件: {log_file}")

def write_and_print(content, file):
    """同时打印到控制台和写入文件."""
    print(content)
    file.write(content + '\n')

def print_and_save_results(results, summary_metrics, result_file_path):
    """打印和保存算法运行结果及统计信息."""
    with open(result_file_path, 'w', encoding='utf-8') as f:
        # 打印和保存每个场景的结果
        for i, result in enumerate(results, 1):
            write_and_print(f"\n场景 {i} 结果:", f)
            for r in result:
                write_and_print(f"算法: {r['算法']}", f)
                write_and_print(f"执行时间: {r['执行时间']:.2f} 秒", f)
                for metric, value in r['指标'].items():
                    write_and_print(f"    {metric}: {value:.2f}", f)

        # 打印和保存总体统计信息
        write_and_print("\n总体统计信息:", f)
        for alg, summary in summary_metrics.items():
            avg_time = summary['total_time'] / summary['count']
            avg_metrics = {metric: value / summary['count'] for metric, value in summary['metrics_sum'].items()}
            write_and_print(f"\n算法: {alg}", f)
            write_and_print(f"平均执行时间: {avg_time:.2f} 秒", f)
            for metric, value in avg_metrics.items():
                write_and_print(f"    平均 {metric}: {value:.2f}", f)

# 初始化所有算法
def initialize_algorithms(env):
    algorithms = [
        NeuralAHPP(env),
        UAV_DPPA_DWA(env),
        MASAC(env)
    ]
    logging.info("算法已初始化")
    return algorithms

# 运行所有算法并收集结果
def run_algorithms(algorithms, env, start, goal):
    results = []
    paths = []  # 用于保存每个算法的路径
    for alg in algorithms:
        logging.info(f"开始 {alg.__class__.__name__} 路径规划")
        start_time = time.time()
        path = alg.plan_path(start, goal)
        execution_time = time.time() - start_time
        metrics = calculate_metrics(path, env)
        results.append({
            '算法': alg.__class__.__name__,
            '路径': path,
            '指标': metrics,
            '执行时间': execution_time
        })
        paths.append(path)  # 保存当前算法的路径
        logging.info(f"{alg.__class__.__name__} 路径规划完成")

    return results, paths  # 返回路径集合


# 打印结果
def print_results(results):
    for result in results:
        print(f"\n算法: {result['算法']}")
        print(f"执行时间: {result['执行时间']:.2f} 秒")
        for metric, value in result['指标'].items():
            print(f"    {metric}: {value:.2f}")


# 主函数
def main():
    log_file = setup_logging()
    logging.info("开始执行主函数")
    env = setup_environment(size=ENV_SIZE, num_obstacles=NUM_OBSTACLES)
    algorithms = initialize_algorithms(env)
    all_results = []
    result_dir = "results"
    os.makedirs(result_dir, exist_ok=True)

    # 存储所有场景的所有路径以用于后续绘制综合图，并关联场景编号
    all_paths_with_scenarios = []

    # 定义算法名称列表，确保顺序与algorithms一致
    algorithm_names = [alg.__class__.__name__ for alg in algorithms]

    # 使用matplotlib的默认颜色循环获取颜色
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # 创建算法名称到颜色的映射
    algorithm_color_map = {name: colors[i % len(colors)] for i, name in enumerate(algorithm_names)}

    for i, (start, goal) in enumerate(SCENARIOS, 1):
        logging.info(f"开始场景 {i}")
        results, paths = run_algorithms(algorithms, env, start, goal)  # 收集每种算法的路径
        all_results.append(results)
        all_paths_with_scenarios.extend(zip([i] * len(paths), paths))  # 将场景编号和路径配对保存

        # 绘制并保存当前场景的路径图
        plot_file = os.path.join(result_dir, f"path_planning_results_{i}.png")  # 修改文件名
        plot_results(env, [r['路径'] for r in results], [r['算法'] for r in results], start, goal, i)
        logging.info(f"场景 {i} 的路径图保存至 {plot_file}")

        # 调用plot_3d来绘制3D图形（障碍物和路径）
        plot_3d(env, paths, i)  # 这里调用plot_3d，传入环境和路径信息
        logging.info(f"场景 {i} 的3D路径图已绘制")

        # 在所有场景完成后，绘制综合轨迹图
    composite_plot_file = os.path.join(result_dir, "composite_path_planning_results.png")
    plot_composite_results(env, all_paths_with_scenarios, algorithm_names, algorithm_color_map)
    logging.info(f"综合结果图已保存为 '{composite_plot_file}'")

    metrics_summary = {}
    for result_set in all_results:
        for result in result_set:
            algorithm_name = result['算法']
            if algorithm_name not in metrics_summary:
                metrics_summary[algorithm_name] = {'count': 0, 'total_time': 0, 'metrics_sum': {}}
            metrics_summary[algorithm_name]['count'] += 1
            metrics_summary[algorithm_name]['total_time'] += result['执行时间']
            for metric, value in result['指标'].items():
                metrics_summary[algorithm_name]['metrics_sum'][metric] = (
                        metrics_summary[algorithm_name]['metrics_sum'].get(metric, 0) + value
                )

    result_file_path = os.path.join(result_dir, f"result_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
    print_and_save_results(all_results, metrics_summary, result_file_path)
    logging.info("所有场景已完成。结果保存至: %s", result_file_path)
# def main():
#     log_file = setup_logging()
#     logging.info("开始执行主函数")
#     env = setup_environment(size=ENV_SIZE, num_obstacles=NUM_OBSTACLES)
#     algorithms = initialize_algorithms(env)
#     all_results = []
#     result_dir = "results"
#     os.makedirs(result_dir, exist_ok=True)
#
#     # 存储所有场景的所有路径以用于后续绘制综合图，并关联场景编号
#     all_paths_with_scenarios = []
#
#     # 定义算法名称列表，确保顺序与algorithms一致
#     algorithm_names = [alg.__class__.__name__ for alg in algorithms]
#
#     # 使用matplotlib的默认颜色循环获取颜色
#     colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
#
#     # 创建算法名称到颜色的映射
#     algorithm_color_map = {name: colors[i % len(colors)] for i, name in enumerate(algorithm_names)}
#
#     for i, (start, goal) in enumerate(SCENARIOS, 1):
#         logging.info(f"开始场景 {i}")
#         results, paths = run_algorithms(algorithms, env, start, goal)  # 收集每种算法的路径
#         all_results.append(results)
#         all_paths_with_scenarios.extend(zip([i] * len(paths), paths))  # 将场景编号和路径配对保存
#
#         # 绘制并保存当前场景的路径图
#         plot_file = os.path.join(result_dir, f"path_planning_results_{i}.png")  # 修改文件名
#         plot_results(env, [r['路径'] for r in results], [r['算法'] for r in results], start, goal, i)
#         logging.info(f"场景 {i} 的路径图保存至 {plot_file}")
#
#         # 调用plot_3d来绘制3D图形（障碍物和路径）
#         plot_3d(env, paths, i)  # 这里只调用一次plot_3d，并传入所有路径
#         logging.info(f"场景 {i} 的3D路径图已绘制")
#
#         # 在所有场景完成后，绘制综合轨迹图
#     composite_plot_file = os.path.join(result_dir, "composite_path_planning_results.png")
#     plot_composite_results(env, all_paths_with_scenarios, algorithm_names, algorithm_color_map)
#     logging.info(f"综合结果图已保存为 '{composite_plot_file}'")
#
#     metrics_summary = {}
#     for result_set in all_results:
#         for result in result_set:
#             algorithm_name = result['算法']
#             if algorithm_name not in metrics_summary:
#                 metrics_summary[algorithm_name] = {'count': 0, 'total_time': 0, 'metrics_sum': {}}
#             metrics_summary[algorithm_name]['count'] += 1
#             metrics_summary[algorithm_name]['total_time'] += result['执行时间']
#             for metric, value in result['指标'].items():
#                 metrics_summary[algorithm_name]['metrics_sum'][metric] = (
#                         metrics_summary[algorithm_name]['metrics_sum'].get(metric, 0) + value
#                 )
#
#     result_file_path = os.path.join(result_dir, f"result_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
#     print_and_save_results(all_results, metrics_summary, result_file_path)
#     logging.info("所有场景已完成。结果保存至: %s", result_file_path)



if __name__ == "__main__":
    main()

