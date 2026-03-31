
navigate_to_map_point = {
    "type": "function",
    "name": "navigate_to_map_point",
    "description": "Given the x and y coordinates of a point in the map coordinate frame, navigate the robot to that point in a safe manner. A low-lever planner will make sure to avoid obstacles and navigate safely and as close as possible to the target point.",
    "parameters": {
        "type": "object",
        "properties": {
            "x": {
                "type": "number",
                "description": "x coordinate in meters"},
            "y": {
                "type": "number",
                "description": "y coordinate in meters"},
            "object_name": {
                "type": "string",
                "description": "Name of the object to navigate to (e.g., apple), based on the object legends on the map. This is optional but can help guide the robot toward the target object."
            },
            "reasoning": {
                "type": "string",
                "description": "brief explanaition for executing this action, e.g. 'I need to go to the kitchen at coordinates (20,30) on the map to find a plate.'"
            }
        },
        "required": [
            "x",
            "y",
            "object_name",
            "reasoning"
        ],
        "additionalProperties": False
    }
}
navigate_to_image_point = {
    "type": "function",
    "name": "navigate_to_image_point",
    "description": "Given the x and y coordinates of a point in the image frame (front camera), navigate the robot to that point. The point should be on navigable terrain.",
    "parameters": {
        "type": "object",
        "properties": {
            "x": {
                "type": "number",
                "description": "x coordinate in pixels"},
            "y": {
                "type": "number",
                "description": "y coordinate in pixels"},
            "reasoning": {
                "type": "string",
                "description": "brief explanaition for executing this action, e.g. 'I need to reach the door at pixel coordinates (100, 200) to get to the room.'"
            }
        },
        "required": [
            "x",
            "y",
            "reasoning"
        ],
        "additionalProperties": False
    }
}
rotate_robot = {
    "type": "function",
    "name": "rotate_robot",
    "description": ("Rotates the robot to face a specific direction based on the provided angle in degrees. "
                    "It returns True if the rotation was successful, or False if it failed."
                    "It also returns the new front camera image after rotation."),
    "parameters": {
        "type": "object",
        "properties": {
            "angle": {
                "type": "number",
                "description": "Rotation angle in degrees relative to the robot's current orientation. Rotation range is 20 to 180 degrees."},
            "direction": {
                "type": "string",
                "enum": ["left", "right"],
                "description": "The direction to rotate the robot, either 'left' or 'right'."
            },
            "reasoning": {
                "type": "string",
                "description": "brief explanaition for executing this action, e.g. 'I need to turn the robot 45 degrees to the right to face the kitchen.'"
            }
        },
        "required": [
            "angle",
            "direction",
            "reasoning"
        ],
        "additionalProperties": False
    }
}
rotate_robot_and_move_forward = {
    "type": "function",
    "name": "rotate_robot_and_move_forward",
    "description": "Rotates the robot to face a specific direction based on the provided angle in degrees, and then moves forward a certain distance. ",
    "parameters": {
        "type": "object",
        "properties": {
            "angle": {
                "type": "number",
                "description": "Rotation angle in degrees relative to the robot's current orientation. Range is 0 to 180 degrees."},
            "direction": {
                "type": "string",
                "enum": ["clockwise", "counterclockwise"],
                "description": "The direction to rotate the robot, either 'clockwise' or 'counterclockwise'."
            },
            "distance": {
                "type": "number",
                "description": "Distance to move forward in meters after rotation. Range is 0.0 to 5.0 meters."
            },
            "reasoning": {
                "type": "string",
                "description": "Brief explanation for executing this action, Example 1: 'I need to turn the robot 45 degrees clockwise (since the object is southeast) and then move forward 1 meter to face and approach the kitchen.'. Example 2: 'I need to turn the robot 135 degrees counterclockwise (since the object is northwest)'"
            }
        },
        "required": [
            "angle",
            "direction",
            "distance",
            "reasoning"
        ],
        "additionalProperties": False
    }
}

set_joint_configuration = {
    "type": "function",
    "name": "set_joint_configuration",
    "description": ("Moves the manipulator to a fixed joint configuration (e.g. home_position is the safest and compact manipulator configuration. In this position, the tip camera is pointing downwards and not useful images can be obtained from it. In contrast, scanning_position sets the tip camera pointing forward, and it is necessary before starting a sequence of manipulation tasks)."
                    " It returns True if the move was successful, or False if it failed."),
    "parameters": {
        "type": "object",
        "properties": {
            "configuration_mode": {
                "type": "string",
                "enum": ["home_position", "scanning_position"],
                "description": "The joint configuration to go to, e.g. 'home_position' or 'scanning_position'."
            },
            "reasoning": {
                "type": "string",
                "description": "brief explanation for executing this action"
            }
        },
        "required": ["configuration_mode", "reasoning"],
        "additionalProperties": False
    }
}
ask_or_notify_human = {
    "type": "function",
    "name": "ask_or_notify_human",
    "description": "It asks or notifies the human about the current task or situation. It can be used to ask for confirmation, provide information, or request assistance. The response is a string with the human's answer.",
    "parameters": {
        "type": "object",
        "properties": {
            "reasoning": {
                "type": "string",
                "description": "brief explanation for executing this action"
            },
            "message": {
                "type": "string",
                "description": "The message to send to the human. It can be a question, a notification, or a request for assistance."
            }
        },
        "required": ["reasoning", "message"],
        "additionalProperties": False
    }
}


center_tip_camera_on_target_point = {
    "type": "function",
    "name": "center_tip_camera_on_target_point",
    "description": ("Centers the manipulator's tip camera on a specified target point on the image defined by (x,y) pixel coordinates."
                    "It returns True if the centering was successful, or False if it failed."
                    "It also returns the new camera image after centering the tip camera."
                    "This function should be called before moving the tip camera forward towards an object of interest, to make sure the object is in the center of the camera view."),
    "parameters": {
        "type": "object",
        "properties": {
            "x": {
                "type": "number",
                "description": "x coordinate of the target point in pixels"
            },
            "y": {
                "type": "number",
                "description": "y coordinate of the target point in pixels"
            },
            "reasoning": {
                "type": "string",
                "description": "brief explanation for executing this action (e.g. 'I will center the tip camera on the mug at pixel coordinates (150, 200) to get a better view of it.')"
            },
        },
        "required": ["x", "y", "reasoning"],
        "additionalProperties": False
    }
}
capture_tip_camera_image = {
    "type": "function",
    "name": "capture_tip_camera_image",
    "description": ("Captures an image from the manipulator's tip camera. It returns the captured image if successful, or False if it failed."),
    "parameters": {
        "type": "object",
        "properties": {
            "reasoning": {
                "type": "string",
                "description": "brief explanation for executing this action"
            },
        },
        "required": ["reasoning"],
        "additionalProperties": False
    }
}

capture_front_camera_image = {
    "type": "function",
    "name": "capture_front_camera_image",
    "description": "Captures an image from the robot's front camera. It returns the captured image if successful, or False if it failed.",
    "parameters": {
        "type": "object",
        "properties": {
            "reasoning": {
                "type": "string",
                "description": "brief explanation for executing this action"
            },
        },
        "required": ["reasoning"],
        "additionalProperties": False
    }
}
capture_front_camera_with_potential_actions = {
    "type": "function",
    "name": "capture_front_camera_with_potential_actions",
    "description": ("Captures an image from the robot's front camera with potential actions. "
    "There are green arrows superimposed onto your observation, which represent potential actions. "
    "These are labeled with a number in a white circle, which represent the location you would move to if you took that action. "
    "If no actions are shown in the image, there are probably objects or obstacles in front of the robot. In that case, the only option is to rotate the robot in place by a certain angle."),
    "parameters": {
        "type": "object",
        "properties": {
            "reasoning": {
                "type": "string",
                "description": "brief explanation for executing this action"
            },
        },
        "required": ["reasoning"],
        "additionalProperties": False
    }
}

execute_action_id = {
    "type": "function",
    "name": "execute_action_id",
    "description": "Executes a specific action after capturing an image with potential actions. It also returns the new front camera image with potential actions after execution.",
    "parameters": {
        "type": "object",
        "properties": {
            "action_id": {
                "type": "number",
                "description": "ID of the action to be performed."
            },
            "reasoning": {
                "type": "string",
                "description": "brief explanation for executing this action"
            },
        },
        "required": ["action_id", "reasoning"],
        "additionalProperties": False
    }
}
get_occupancy_map_with_objects = {
    "type": "function",
    "name": "get_occupancy_map_with_objects",
    "description": "It returns a top-down view of the occupancy map with the robot and objects in the environment, as an Image. Free space is black, occupied space is white and unknown space is gray.",
    "parameters": {
        "type": "object",
        "properties": {
            "reasoning": {
                "type": "string",
                "description": "brief explanation for executing this action"
            }
        },
        "required": ["reasoning"],
        "additionalProperties": False
    }
}
get_robot_centric_map_with_objects = {
    "type": "function",
    "name": "get_robot_centric_map_with_objects",
    "description": ("It returns a top-down view of the robot-centric occupancy map with the robot and objects in the environment, as an Image. Free space is black, occupied space is white and unknown space is gray."
                    "The map shows the robot and the objects in the environment, specified by color labels. "
                    "The red arrow indicates the robot's current orientation. "),
    
    "parameters": {
        "type": "object",
        "properties": {
            "reasoning": {
                "type": "string",
                "description": "brief explanation for executing this action"
            }
        },
        "required": ["reasoning"],
        "additionalProperties": False
    }
}


move_tip_camera = {
    "type": "function",
    "name": "move_tip_camera",
    "description": ("Moves the tip camera along six possible directions (up, down, left, right, forward or backward). It returns True if the move was successful, or False if it failed."
                    "It also returns the new camera image after moving the tip camera."
                    "Before moving the tip camera forward, make sure the object of interest is centered in the camera using the center_tip_camera_on_target_point function."),
    "parameters": {
        "type": "object",
        "properties": {
            "direction": {
                "type": "string",
                "enum": ["up", "down", "left", "right", "forward", "backward"],
                "description": "Direction to move the tip camera a fixed distance (~0.1m)."
            },
            "reasoning": {
                "type": "string",
                "description": "brief explanation for executing this action (e.g. 'The tip camera is looking over the coffee table. I need to move the camera downward to get a clearer view of the table.')"
            },
        },
        "required": ["direction", "reasoning"],
        "additionalProperties": False
    }
}
# ++++++++ NAVIGATION TOOLS ++++++++

# global map (for global navigation) and front camera with potential actions (for local navigation)
navigation_manipulation_mode_v2_tools = [get_occupancy_map_with_objects,
                                         navigate_to_map_point,
                                         capture_front_camera_with_potential_actions,
                                         execute_action_id,
                                         rotate_robot,
                                         set_joint_configuration,
                                         capture_tip_camera_image,
                                         move_tip_camera,
                                         center_tip_camera_on_target_point,
                                         ask_or_notify_human]
# global map (for global navigation) and robot-centric map (for local navigation)
navigation_manipulation_mode_v3_tools = [get_occupancy_map_with_objects,
                                         navigate_to_map_point,
                                         get_robot_centric_map_with_objects,
                                         rotate_robot_and_move_forward,
                                         capture_front_camera_image,
                                         set_joint_configuration,
                                         capture_tip_camera_image,
                                         move_tip_camera,
                                         center_tip_camera_on_target_point,
                                         ask_or_notify_human]

tools = {
    "navigation_manipulation_mode_v2": navigation_manipulation_mode_v2_tools,
    "navigation_manipulation_mode_v3": navigation_manipulation_mode_v3_tools,
}
