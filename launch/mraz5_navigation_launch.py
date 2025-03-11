import os.path
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from nav2_common.launch import RewrittenYaml

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    mr5_localization_dir = get_package_share_directory('mraz5_navigation')
    
    config_param_nav2 = os.path.join(mr5_localization_dir,'config', 'nav2_params.yaml')
    
    param_substitutions = {
        'global_frame': LaunchConfiguration('global_frame', default='odom')}
    configured_params = RewrittenYaml(
            source_file=config_param_nav2,
            root_key='',
            param_rewrites=param_substitutions,
            convert_types=True)
    

    pkg_nav2_bringup = get_package_share_directory('nav2_bringup')
    nav2_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2_bringup,
            'launch/navigation_launch.py')),
        launch_arguments={'use_sim_time': 'False', 'params_file': configured_params}.items(),
    )
    
    ld = LaunchDescription()
    ld.add_action(nav2_bringup_launch)

    return ld
