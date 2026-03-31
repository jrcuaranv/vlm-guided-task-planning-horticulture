# vlm-guided-task-planning-horticulture
This repository contains supplementary material for our paper entitled [“Visual-Language-Guided Task Planning for Horticultural Robots.”](https://kendallkoe.com/Visual-Language-Guided-Task-Planning-for-Horticultural-Robots/)

## Prompts
We provide the main prompts for the two navigation-manipulation modes used in our evaluation:
- Mode v2: uses the front camera image with polar actions for local navigation.
- Mode v3: leverages a robot-centric semantic occupancy map for local navigation.

## Demonstrations
The demonstrations are textual-only reasoning examples designed to help the VLM handle common issues when using a noisy semantic map (for example, detecting a false positive instead of the actual target).
These demonstrations serve as additional information for the few-shot VLM in our evaluation.


## Tools description
We provide the perception and action tool descriptions in JSON schema format, compatible with the OpenAI API.

## Gazebo Environments
We provide the .world files for the three Gazebo simulation environments used in our evaluation:
- greenhouse10.world: complex polyculture environment
- greenhouse11.world: monoculture environment
- greenhouse12.world: simple polyculture environment

These models were tested on ROS1 Gazebo. ROS2 Gazebo may require some adjustments.

## 3D plant models
The original 3D plant models cannot be redistributed due to licensing restrictions. To access them, please download the models from the links below and send us an email (jrcuaranv@gmail.com) with your purchase receipts. After verification, we can provide the post-processed 3D plant models ready to use in the Gazebo environments.


[Orange bell-peppers](https://www.turbosquid.com/3d-models/xfrogplants-chili-pepper-plant-3d-obj/545597), [Lettuces](https://www.turbosquid.com/3d-models/lettuce-set-36-lactuca-1455522), [Red and Yellow Capsicum plants](https://3dexport.com/3d-model-realistic-3d-capsicum-plant-537768), [Tomatoes](https://3dexport.com/3d-model-tomato-plantation-405015), [Strawberries](https://3dexport.com/3d-model-3d-strawberry-plant-collection-547320),  [Eggplants](https://www.vfxgrace.com/product/blender-3d-plant-eggplant-pack/)

