import yaml
import os
import numpy as np
import json
# output_dir = "../output"  # /path/to/vlm_interface/output
output_dir = "/mnt/ssd2T/vlm_interface_output_2025/Experimental_Results"


if not os.path.exists(output_dir):
    raise ValueError(f"Output directory {output_dir} does not exist.")


human_tasks_path = os.path.join(output_dir, 'human_tasks_summary.yaml')
vlm_tasks_path = os.path.join(output_dir, 'vlm_tasks_summary.yaml')
if not os.path.exists(human_tasks_path):
    raise ValueError(f"Human tasks summary file {human_tasks_path} does not exist.")
if not os.path.exists(vlm_tasks_path):
    raise ValueError(f"VLM tasks summary file {vlm_tasks_path} does not exist.")
with open(human_tasks_path, 'r') as f:
    human_tasks_all = yaml.safe_load(f)
with open(vlm_tasks_path, 'r') as f:
    vlm_tasks_all = yaml.safe_load(f)

environment = 'all'  # 'all' or 'greenhouse10' or 'greenhouse11' or 'greenhouse12'
if environment not in ['greenhouse10', 'greenhouse11', 'greenhouse12']:
    vlm_tasks = vlm_tasks_all
    human_tasks = human_tasks_all
else:
    vlm_tasks = [task for task in vlm_tasks_all if task['environment_name'] == environment]
    human_tasks = [task for task in human_tasks_all if task['environment_name'] == environment]



human_zero_shot_tasks_no_noise = []
for task in human_tasks:
    if task['load_gt_objects'] == True and (task['agent_mode']=='navigation_manipulation_mode_v3' or task['agent_mode']=='navigation_manipulation_mode_v1'):
        human_zero_shot_tasks_no_noise.append(task)

vlm_zero_shot_tasks_no_noise = []
for task in vlm_tasks:
    if task['load_gt_objects'] == True and task['use_demonstrations'] == False and (task['agent_mode']=='navigation_manipulation_mode_v3' or task['agent_mode']=='navigation_manipulation_mode_v1'):
        vlm_zero_shot_tasks_no_noise.append(task)

# ablations vlm tasks - mode v2

human_tasks_noisy_map_mode_v2 = []
for task in human_tasks:
    if task['load_gt_objects'] == False and task['agent_mode']=='navigation_manipulation_mode_v2':
        human_tasks_noisy_map_mode_v2.append(task)

vlm_zero_shot_tasks_noisy_map_mode_v2 = []
for task in vlm_tasks:
    if task['load_gt_objects'] == False and task['use_demonstrations'] == False and task['agent_mode']=='navigation_manipulation_mode_v2':
        vlm_zero_shot_tasks_noisy_map_mode_v2.append(task)

vlm_few_shot_tasks_noisy_map_mode_v2 = []
for task in vlm_tasks:
    if task['load_gt_objects'] == False and task['use_demonstrations'] == True and task['agent_mode']=='navigation_manipulation_mode_v2':
        vlm_few_shot_tasks_noisy_map_mode_v2.append(task)

# ablations vlm tasks - mode v3
human_tasks_noisy_map_mode_v3 = []
for task in human_tasks:
    if task['load_gt_objects'] == False and task['agent_mode']=='navigation_manipulation_mode_v3':
        human_tasks_noisy_map_mode_v3.append(task)

vlm_zero_shot_tasks_noisy_map_mode_v3 = []
for task in vlm_tasks:
    if task['load_gt_objects'] == False and task['use_demonstrations'] == False and task['agent_mode']=='navigation_manipulation_mode_v3':
        vlm_zero_shot_tasks_noisy_map_mode_v3.append(task)

vlm_few_shot_tasks_noisy_map_mode_v3 = []
for task in vlm_tasks:
    if task['load_gt_objects'] == False and task['use_demonstrations'] == True and task['agent_mode']=='navigation_manipulation_mode_v3':
        vlm_few_shot_tasks_noisy_map_mode_v3.append(task)


tasks_sets = {}
tasks_sets['vlm_zero_shot_tasks_no_noise'] = vlm_zero_shot_tasks_no_noise
tasks_sets['human_zero_shot_tasks_no_noise'] = human_zero_shot_tasks_no_noise
tasks_sets['vlm_zero_shot_tasks_noisy_map_mode_v2'] = vlm_zero_shot_tasks_noisy_map_mode_v2
tasks_sets['vlm_few_shot_tasks_noisy_map_mode_v2'] = vlm_few_shot_tasks_noisy_map_mode_v2
tasks_sets['vlm_zero_shot_tasks_noisy_map_mode_v3'] = vlm_zero_shot_tasks_noisy_map_mode_v3
tasks_sets['vlm_few_shot_tasks_noisy_map_mode_v3'] = vlm_few_shot_tasks_noisy_map_mode_v3
tasks_sets['human_tasks_noisy_map_mode_v2'] = human_tasks_noisy_map_mode_v2
tasks_sets['human_tasks_noisy_map_mode_v3'] = human_tasks_noisy_map_mode_v3

human_ref_sets = {}
human_ref_sets['vlm_zero_shot_tasks_no_noise'] = human_zero_shot_tasks_no_noise
human_ref_sets['human_zero_shot_tasks_no_noise'] = human_zero_shot_tasks_no_noise
human_ref_sets['vlm_zero_shot_tasks_noisy_map_mode_v2'] = human_tasks_noisy_map_mode_v2
human_ref_sets['vlm_few_shot_tasks_noisy_map_mode_v2'] = human_tasks_noisy_map_mode_v2
human_ref_sets['vlm_zero_shot_tasks_noisy_map_mode_v3'] = human_tasks_noisy_map_mode_v3
human_ref_sets['vlm_few_shot_tasks_noisy_map_mode_v3'] = human_tasks_noisy_map_mode_v3
human_ref_sets['human_tasks_noisy_map_mode_v2'] = human_tasks_noisy_map_mode_v2
human_ref_sets['human_tasks_noisy_map_mode_v3'] = human_tasks_noisy_map_mode_v3

def get_optimal_distance_from_human_tasks(h_tasks, task_id):
    for task in h_tasks:
        if task['task_id'] == task_id and task['completeness_score'] == 100:
            return task['traveled_distance']  # Assuming human traveled_distance is the optimal distance
    return None

def compute_success_rate(tasks, task_category=0):
    successful_tasks = [task for task in tasks if task['completeness_score'] == 100 and task['task_category'] == task_category]
    total_tasks = len([task for task in tasks if task['task_category'] == task_category])
    success_rate = (len(successful_tasks) / total_tasks * 100) if total_tasks > 0 else 0
    print(f"Total tasks in category {task_category}: {total_tasks}")
    return success_rate

def compute_spl(tasks, h_tasks, task_category=0):
    # computes Success weighted by Path Length (SPL)
    total_spl = 0
    successful_tasks = 0
    for task in tasks:
        if task['task_category'] == task_category:
            optimal_distance = get_optimal_distance_from_human_tasks(h_tasks, task['task_id'])
            if optimal_distance is not None and task['completeness_score'] == 100:
                successful_tasks += 1
                path_length = task['traveled_distance']
                if path_length > 0:
                    total_spl += optimal_distance / max(path_length, optimal_distance)
    total_tasks = len([task for task in tasks if task['task_category'] == task_category])
    spl = (total_spl / total_tasks) if total_tasks > 0 else 0
    return spl * 100  # return as percentage

def compute_average_metrics(tasks, task_category=0):
    # only for successful tasks
    total_distance = sum(task['traveled_distance'] for task in tasks if task['task_category'] == task_category and task['completeness_score'] == 100)
    
    average_tool_calls = np.mean([task['tool_calls_count'] for task in tasks if task['task_category'] == task_category and task['completeness_score'] == 100])
    std_tool_calls = np.std([task['tool_calls_count'] for task in tasks if task['task_category'] == task_category and task['completeness_score'] == 100])
    successful_tasks_count = len([task for task in tasks if task['task_category'] == task_category and task['completeness_score'] == 100])
    
    average_tokens = np.mean([task['total_tokens'] for task in tasks if task['task_category'] == task_category])
    std_tokens = np.std([task['total_tokens'] for task in tasks if task['task_category'] == task_category])

    average_completeness_score = np.mean([task['completeness_score'] for task in tasks if task['task_category'] == task_category])
    std_completeness_score = np.std([task['completeness_score'] for task in tasks if task['task_category'] == task_category])
    tasks_count = len([task for task in tasks if task['task_category'] == task_category])
    
    max_tool_calls = max((task['tool_calls_count'] for task in tasks if task['task_category'] == task_category), default=1)
    return {
        'task_category': task_category,
        'tasks_count': tasks_count,
        # 'successful_tasks_count': len(successful_tasks_count),
        'success_rate': (successful_tasks_count / tasks_count * 100) if tasks_count > 0 else 0,
        # 'average_traveled_distance': total_distance / len(successful_tasks_count) if successful_tasks_count else 0,
        'average_tool_calls_count': average_tool_calls if successful_tasks_count > 0 else 0,
        '__std_tool_calls': std_tool_calls if successful_tasks_count > 0 else 0,
        'average_completeness_score': average_completeness_score if tasks_count > 0 else 0,
        '__std_completeness_score': std_completeness_score,
        'average_total_tokens': average_tokens,
        '__std_total_tokens': std_tokens,
        
        # 'max_tool_calls': max_tool_calls
    }


def compute_spl_over_all_categories(tasks, h_tasks):
    # computes Success weighted by Path Length (SPL)
    total_spl = 0
    successful_tasks = 0
    for task in tasks:
        optimal_distance = get_optimal_distance_from_human_tasks(h_tasks, task['task_id'])
        if optimal_distance is not None and task['completeness_score'] == 100:
            successful_tasks += 1
            path_length = task['traveled_distance']
            if path_length > 0:
                total_spl += optimal_distance / max(path_length, optimal_distance)
    total_tasks = len(tasks)
    spl = (total_spl / total_tasks) if total_tasks > 0 else 0
    return spl * 100  # return as percentage

def compute_average_metrics_over_all_categories(tasks):
    # only for successful tasks
    total_distance = sum(task['traveled_distance'] for task in tasks if task['completeness_score'] == 100)
    
    average_tool_calls = np.mean([task['tool_calls_count'] for task in tasks if task['completeness_score'] == 100])
    std_tool_calls = np.std([task['tool_calls_count'] for task in tasks if task['completeness_score'] == 100])
    successful_tasks_count = len([task for task in tasks if task['completeness_score'] == 100])
    
    average_tokens = np.mean([task['total_tokens'] for task in tasks ])
    std_tokens = np.std([task['total_tokens'] for task in tasks])

    average_completeness_score = np.mean([task['completeness_score'] for task in tasks ])
    std_completeness_score = np.std([task['completeness_score'] for task in tasks])
    tasks_count = len(tasks)
    
    max_tool_calls = max((task['tool_calls_count'] for task in tasks), default=1)
    return {
        'task_category': -1,
        'tasks_count': tasks_count,
        # 'successful_tasks_count': len(successful_tasks_count),
        'success_rate': (successful_tasks_count / tasks_count * 100) if tasks_count > 0 else 0,
        # 'average_traveled_distance': total_distance / len(successful_tasks_count) if successful_tasks_count else 0,
        'average_tool_calls_count': average_tool_calls if successful_tasks_count > 0 else 0,
        '__std_tool_calls': std_tool_calls if successful_tasks_count > 0 else 0,
        'average_completeness_score': average_completeness_score if tasks_count > 0 else 0,
        '__std_completeness_score': std_completeness_score,
        'average_total_tokens': average_tokens,
        '__std_total_tokens': std_tokens,
        
        # 'max_tool_calls': max_tool_calls
    }


for set_name, tasks in tasks_sets.items():
    for category in range(4):  # Assuming task categories are 0, 1, 2, 3

        print(f"\nEvaluating task set: {set_name} with category: {category}")
        print(f"Environment: {environment}")
        metrics = compute_average_metrics(tasks, task_category=category)
        spl = compute_spl(tasks, human_ref_sets[set_name], task_category=category)
        print(f"Average Metrics:")
        for key, value in metrics.items():
            print(f"  {key}: {value:.2f}")
        print(f"  SPL: {spl:.2f}%")

# metrics over all categories
# for set_name, tasks in tasks_sets.items():
    
#     print(f"\nEvaluating task set: {set_name} with category: All")
#     print(f"Environment: {environment}")
#     metrics = compute_average_metrics_over_all_categories(tasks)
#     spl = compute_spl_over_all_categories(tasks, human_ref_sets[set_name])
#     print(f"Average Metrics:")
#     for key, value in metrics.items():
#         print(f"  {key}: {value:.2f}")
#     print(f"  SPL: {spl:.2f}%")


# # Extracting the task IDs for category 1 tasks for each environment in vlm_tasks
# g10_tasks_ids = []
# g11_tasks_ids = []
# g12_tasks_ids = []
# for task in vlm_tasks:
#     if task['environment_name'] == 'greenhouse10' and task['task_category']==1:
#         g10_tasks_ids.append(task['task_id'])
#     if task['environment_name'] == 'greenhouse11' and task['task_category']==1:
#         g11_tasks_ids.append(task['task_id'])
#     if task['environment_name'] == 'greenhouse12' and task['task_category']==1:
#         g12_tasks_ids.append(task['task_id'])
# print(f"\nGreenhouse10 Number of tasks: {len(g10_tasks_ids)} tasks IDs (category 1): {g10_tasks_ids}")
# print(f"\nGreenhouse11 Number of tasks: {len(g11_tasks_ids)} tasks IDs (category 1): {g11_tasks_ids}")
# print(f"\nGreenhouse12 Number of tasks: {len(g12_tasks_ids)} tasks IDs (category 1): {g12_tasks_ids}")

# Extracting unique tasks from human_zero_shot_tasks_no_noise, keeping only the task_id, the environment_name, the task_category and the task_prompt. 

unique_human_zero_shot_tasks_no_noise = []
seen_task_ids = set()
for task in human_zero_shot_tasks_no_noise:
    if task['task_id'] not in seen_task_ids:
        unique_human_zero_shot_tasks_no_noise.append({
            'task_id': task['task_id'],
            'environment_name': task['environment_name'],
            'task_category': task['task_category'],
            'task_prompt': task['task_prompt']
        })
        seen_task_ids.add(task['task_id'])
print(f"\nNumber of unique human zero-shot tasks with no noise: {len(unique_human_zero_shot_tasks_no_noise)}")

# creatig a json file with the unique human zero-shot tasks with no noise for future reference
env10_id0_tasks = [task for task in unique_human_zero_shot_tasks_no_noise if task['environment_name'] == 'greenhouse10' and task['task_category']==0]
env10_id1_tasks = [task for task in unique_human_zero_shot_tasks_no_noise if task['environment_name'] == 'greenhouse10' and task['task_category']==1]
env10_id2_tasks = [task for task in unique_human_zero_shot_tasks_no_noise if task['environment_name'] == 'greenhouse10' and task['task_category']==2]
env11_id0_tasks = [task for task in unique_human_zero_shot_tasks_no_noise if task['environment_name'] == 'greenhouse11' and task['task_category']==0]
env11_id1_tasks = [task for task in unique_human_zero_shot_tasks_no_noise if task['environment_name'] == 'greenhouse11' and task['task_category']==1]
env11_id2_tasks = [task for task in unique_human_zero_shot_tasks_no_noise if task['environment_name'] == 'greenhouse11' and task['task_category']==2]
env12_id0_tasks = [task for task in unique_human_zero_shot_tasks_no_noise if task['environment_name'] == 'greenhouse12' and task['task_category']==0]
env12_id1_tasks = [task for task in unique_human_zero_shot_tasks_no_noise if task['environment_name'] == 'greenhouse12' and task['task_category']==1]
env12_id2_tasks = [task for task in unique_human_zero_shot_tasks_no_noise if task['environment_name'] == 'greenhouse12' and task['task_category']==2]
unique_tasks_dict = {
    'greenhouse10': {
        'category_0': env10_id0_tasks,
        'category_1': env10_id1_tasks,
        'category_2': env10_id2_tasks
    },
    'greenhouse11': {
        'category_0': env11_id0_tasks,
        'category_1': env11_id1_tasks,
        'category_2': env11_id2_tasks
    },
    'greenhouse12': {
        'category_0': env12_id0_tasks,
        'category_1': env12_id1_tasks,
        'category_2': env12_id2_tasks
    }
}
output_unique_human_zero_shot_tasks_no_noise_json_path = os.path.join(output_dir, 'unique_tasks_prompts.json')
with open(output_unique_human_zero_shot_tasks_no_noise_json_path, 'w') as f:
    json.dump(unique_tasks_dict, f, indent=4)


