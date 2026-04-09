import yaml
import os
# output_dir = "../output"  # /path/to/vlm_interface/output
output_dir = "/mnt/ssd2T/vlm_interface_output_2025/Experimental_Results"
if not os.path.exists(output_dir):
    raise ValueError(f"Output directory {output_dir} does not exist.")
# looking for all 'metadata.yaml' files in the output directory
human_tasks_summary = []
for root, dirs, files in os.walk(output_dir):
    for file in files:
        if file == 'metadata.yaml':
            metadata_path = os.path.join(root, file)
            with open(metadata_path, 'r') as f:
                metadata = yaml.safe_load(f)
                try:
                    if metadata[0]['vlm_model'] == 'human': # and metadata[-1]['completeness_score']==100:
                        main_data = {}
                        main_data['environment_name'] = metadata[0]['environment_name']
                        main_data['agent_mode'] = metadata[0]['agent_mode']
                        main_data['user_name'] = metadata[0]['user_name']
                        main_data['task_id'] = metadata[0]['task_id']
                        main_data['task_prompt'] = metadata[0]['task_prompt']
                        main_data['task_category'] = metadata[0]['task_category']
                        main_data['load_gt_objects'] = metadata[0]['load_gt_objects']
                        main_data['use_demonstrations'] = metadata[0]['use_demonstrations']
                        main_data['robot_position'] = metadata[1]['robot_position']
                        main_data['robot_orientation'] = metadata[1]['robot_orientation']
                        main_data['traveled_distance'] = metadata[-2]['traveled_distance']
                        main_data['tool_calls_count'] = metadata[-2]['tool_calls_count']
                        main_data['reset_cause'] = metadata[-1]['reset_cause']
                        main_data['completeness_score'] = metadata[-1]['completeness_score']
                        
                        # computing token usage
                        total_tokens = 0
                        for entry in metadata:
                            if 'total_tokens' in entry:
                                total_tokens += entry['total_tokens']
                                
                        main_data['total_tokens'] = total_tokens
                        human_tasks_summary.append(main_data)
                        print(f"Found task_id: {main_data['task_id']} in {metadata_path}")
                except Exception as e:
                    print(f"Error retrieving task_id: {e}")


# Save the task IDs to a YAML file
# raise Exception("Stopping here to avoid overwriting existing files. Remove this line to proceed.")
vlm_tasks_summary = []
for root, dirs, files in os.walk(output_dir):
    for file in files:
        if file == 'metadata.yaml':
            metadata_path = os.path.join(root, file)
            with open(metadata_path, 'r') as f:
                metadata = yaml.safe_load(f)
                try:
                    if metadata[0]['vlm_model'] == 'gpt-4.1': #and metadata[-1]['completeness_score']==100:
                        main_data = {}
                        main_data['environment_name'] = metadata[0]['environment_name']
                        main_data['agent_mode'] = metadata[0]['agent_mode']
                        main_data['user_name'] = metadata[0]['user_name']
                        main_data['task_id'] = metadata[0]['task_id']
                        main_data['task_prompt'] = metadata[0]['task_prompt']
                        main_data['task_category'] = metadata[0]['task_category']
                        main_data['load_gt_objects'] = metadata[0]['load_gt_objects']
                        main_data['use_demonstrations'] = metadata[0]['use_demonstrations']
                        main_data['robot_position'] = metadata[1]['robot_position']
                        main_data['robot_orientation'] = metadata[1]['robot_orientation']
                        main_data['traveled_distance'] = metadata[-2]['traveled_distance']
                        main_data['tool_calls_count'] = metadata[-2]['tool_calls_count']
                        main_data['reset_cause'] = metadata[-1]['reset_cause']
                        main_data['completeness_score'] = metadata[-1]['completeness_score']
                        # computing token usage
                        total_tokens = 0
                        for entry in metadata:
                            if 'total_tokens' in entry:
                                total_tokens += entry['total_tokens']
                                
                        main_data['total_tokens'] = total_tokens
                        
                        vlm_tasks_summary.append(main_data)
                        print(f"Found task_id: {main_data['task_id']} in {metadata_path}")
                except Exception as e:
                    print(f"Error retrieving task_id: {e}")

print(f"Total human task_ids found: {len(human_tasks_summary)}")

print(f"Total VLM task_ids found: {len(vlm_tasks_summary)}")
# sorting tasks in human_tasks_summary by task_id
human_tasks = sorted(human_tasks_summary, key=lambda x: x['task_id'])
vlm_tasks = sorted(vlm_tasks_summary, key=lambda x: x['task_id'])

if human_tasks:
    tasks_summary_path = os.path.join(output_dir, 'human_tasks_summary.yaml')
    with open(tasks_summary_path, 'w') as f:
        yaml.dump(human_tasks, f, default_flow_style=False)
    print(f"Saved task summary to {tasks_summary_path}")
else:
    print("No task IDs found to save.")

if vlm_tasks:
    vlm_tasks_summary_path = os.path.join(output_dir, 'vlm_tasks_summary.yaml')
    with open(vlm_tasks_summary_path, 'w') as f:
        yaml.dump(vlm_tasks, f, default_flow_style=False)
    print(f"Saved VLM task summary to {vlm_tasks_summary_path}")
else:
    print("No VLM task IDs found to save.")



