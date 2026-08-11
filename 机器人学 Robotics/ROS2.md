# ROS 2 教程与重点

ROS 2 是机器人开发的中间件——处理通信、硬件抽象、包管理。和 ROS1 相比，核心变化是**去中心化**（干掉 roscore）和**实时性**。

---

## 一、ROS1 vs ROS2：为什么换？

| | ROS1 | ROS2 |
|------|------|------|
| **通信层** | 自研 TCP/UDP (TCPROS/UDPROS) | DDS 标准协议 |
| **中心节点** | 必须 roscore，单点故障 | 无 roscore；通过 DDS discovery 自动发现节点 |
| **实时性** | 不保证 | 支持实时（RT） |
| **多机器人** | 需额外配置 | 原生支持 |
| **跨平台** | Ubuntu only | Linux / macOS / Windows |
| **构建工具** | catkin_make | **colcon** |
| **启动** | XML launch | **Python launch**（也支持 XML/YAML） |
| **Python** | 2.7 → 3 | 3 only |
| **消息格式** | `.msg` | `.msg` + `.idl`（DDS 兼容） |

**一句话**：ROS2 把协议层全换成了工业级 DDS，核心功能下沉到中间件，ROS 只做上层封装。

---

## 二、核心概念

### 2.1 通信模型全景

```
┌─────────┐  Topic (pub/sub)  ┌─────────┐
│  Node A │ ←───────────────→ │  Node B │
└─────────┘                   └─────────┘
     │                              │
     │    Service (req/rep)        │
     │ ←─────────────────────────→ │
     │                              │
     │    Action (goal/feedback)   │
     │ ←─────────────────────────→ │
     └──────────────────────────────┘
```

### 2.2 Topic（话题）— 数据流

异步、多对多，最常用的通信方式。传感器数据、关节状态全是 topic。

```python
# Publisher
self.publisher = self.create_publisher(String, 'chatter', 10)
self.publisher.publish(msg)

# Subscriber  
self.subscription = self.create_subscription(String, 'chatter', self.callback, 10)
```

**QoS（Quality of Service）** — ROS2 新增，控制传输策略：

| QoS 参数 | 含义 | 选择 |
|---------|------|------|
| **Reliability** | 可靠（RELIABLE）vs 尽力（BEST_EFFORT） | 传感器数据用 BEST_EFFORT，指令用 RELIABLE |
| **Durability** | 新 subscriber 是否收到历史消息 | TRANSIENT_LOCAL（发最后一条）vs VOLATILE |
| **History** | 缓存多少条消息 | KEEP_LAST(N) 或 KEEP_ALL |
| **Depth** | KEEP_LAST 时的队列深度 | 传感器 1-5，关键数据 10+ |

**为什么要关心 QoS**：激光雷达 30Hz 发包，如果你用 RELIABLE + KEEP_ALL，网络一卡它给你补发 200 条历史激光帧，把后面 pipeline 全堵死。

### 2.3 Service（服务）— 请求/应答

同步，一问一答。适合配置参数、触发动作。

```python
# Server
self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.callback)

# Client  
self.client = self.create_client(AddTwoInts, 'add_two_ints')
future = self.client.call_async(request)
```

**什么时候用 Service 而不是 Topic**：需要返回值 + 低频调用时。连续高频数据流通常用 Topic；如果任务持续时间长、需要反馈/取消，用 Action。

### 2.4 Action（动作）— 长任务

异步 + 有反馈 + 可取消。导航、抓取、所有"需要一段时间"的任务。

```python
# Server
self.action_server = ActionServer(self, Fibonacci, 'fibonacci', self.execute)

# Client
self.client = ActionClient(self, Fibonacci, 'fibonacci')
goal_handle = await self.client.send_goal_async(goal_msg)
result = await goal_handle.get_result_async()
```

**Action 的内部机制**：底层用了 5 个 topic（goal, cancel, status, feedback, result），你不需要关心，ActionClient/Server 封装好了。

### 2.5 对比总结

| | Topic | Service | Action |
|------|:------:|:------:|:------:|
| **模式** | pub/sub | req/rep | goal/feedback/result |
| **同步/异步** | 异步 | 同步 | 异步 |
| **可取消** | — | — | ✓ |
| **反馈** | — | — | ✓ |
| **典型场景** | 激光、图像、状态 | 参数配置、标定触发 | 导航、抓取 |

---

## 三、工作空间与构建

### 3.1 标准目录结构

```
ros2_ws/
├── src/                    # 源码（你写的）
│   └── my_pkg/
│       ├── CMakeLists.txt  # C++ 构建
│       ├── package.xml     # 包信息（必须）
│       ├── my_pkg/
│       │   └── __init__.py
│       │   └── node.py     # Python 节点
│       ├── src/            # C++ 源码
│       ├── launch/         # launch 文件
│       ├── msg/            # 自定义消息
│       ├── srv/            # 自定义服务
│       └── action/         # 自定义动作
├── build/                  # 构建中间文件（colcon 生成）
├── install/                # 安装目录（colcon 生成）
└── log/                    # 构建日志
```

### 3.2 常用命令

```bash
# 创建工作空间
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws

# 构建（colcon = catkin 的 ROS2 版）
colcon build --symlink-install   # symlink 让 Python 改了代码不用重新 build

# 只构建一个包
colcon build --packages-select my_pkg

# source 环境
source install/setup.bash        # 或 .zsh

# 运行节点
ros2 run my_pkg my_node

# launch
ros2 launch my_pkg my_launch.py
```

### 3.3 package.xml 关键字段

```xml
<package format="3">
  <name>my_pkg</name>
  <version>0.0.0</version>
  <description>what this package does</description>
  <maintainer email="xx@xx.com">name</maintainer>
  <license>Apache-2.0</license>

  <!-- 构建依赖 -->
  <buildtool_depend>ament_cmake</buildtool_depend>
  <!-- 或 Python 包用 ament_cmake_python 或 ament_python -->
  
  <!-- 运行时依赖 -->
  <depend>rclcpp</depend>      <!-- ROS2 C++ client library -->
  <depend>std_msgs</depend>
  <depend>sensor_msgs</depend>
</package>
```

---

## 四、写一个节点

### 4.1 Python 最小节点

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher = self.create_publisher(String, 'topic', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello {self.count}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()
    rclpy.spin(node)  # 阻塞直到 Ctrl+C
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 4.2 C++ 最小节点

```cpp
#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class MinimalPublisher : public rclcpp::Node {
public:
  MinimalPublisher() : Node("minimal_publisher"), count_(0) {
    publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
    timer_ = this->create_wall_timer(500ms, std::bind(&MinimalPublisher::timer_callback, this));
  }

private:
  void timer_callback() {
    auto msg = std_msgs::msg::String();
    msg.data = "Hello " + std::to_string(count_++);
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", msg.data.c_str());
    publisher_->publish(msg);
  }

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  size_t count_;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalPublisher>());
  rclcpp::shutdown();
  return 0;
}
```

---

## 五、Launch 文件（Python）

ROS2 的 launch 是 Python 脚本，不是 XML（虽然也兼容 XML）。

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_pkg',
            executable='talker',
            name='my_talker',        # 运行时重命名
            parameters=[{'param1': 1.0}],
            remappings=[('/topic', '/renamed_topic')],
            output='screen',
        ),
        Node(
            package='my_pkg',
            executable='listener',
            name='my_listener',
        ),
    ])
```

**Launch 可以做的事**：启动节点、传参、命名空间隔离、条件启动、延迟启动、生命周期绑定（一个节点挂了，连带 kill 其他）。

---

## 六、常用 ros2 CLI

```bash
# 节点
ros2 node list                       # 所有运行节点
ros2 node info /node_name            # 节点订阅/发布了什么

# 话题
ros2 topic list                      # 所有 topic
ros2 topic echo /topic               # 实时打印（= rostopic echo）
ros2 topic hz /topic                 # 发布频率
ros2 topic info /topic               # topic 的 type 和 QoS

# 服务
ros2 service list
ros2 service call /service type "{data: 1}"

# 参数
ros2 param list /node
ros2 param get /node param_name
ros2 param set /node param_name value

# 包
ros2 pkg list                        # 所有已安装包
ros2 pkg executables my_pkg          # 包里有哪些可执行文件

# 调试
ros2 run rqt_reconfigure rqt_reconfigure  # 动态调参
rqt_graph                                # 可视化节点和 topic 关系图
ros2 topic pub /topic type "{data: 'hi'}" --once
```

---

## 七、DDS 基础（仅需了解）

DDS（Data Distribution Protocol）是 ROS2 的底层通信协议。**通常不需要关心，直到出问题**。

| DDS 实现 | ROS2 默认 | 特点 |
|------|:------:|------|
| Fast DDS (eProsima) | Humble 及之后 | 开箱即用，性能好 |
| Cyclone DDS | 部分发行版 | 零拷贝、低延迟 |
| RTI Connext | — | 商业级，需 license |

**ROS_DOMAIN_ID**：同一网络多台机器时，设成相同数字（0-232）才能互相发现。默认 0。

```bash
export ROS_DOMAIN_ID=42   # 隔离到 domain 42
```

**多机通信**：同一二层网络里通常不需要手动写节点 IP，ROS2 通过 DDS 自动发现同域下的节点。但跨网段、Docker、VPN、公司/校园网、防火墙或禁用 multicast 的环境，经常需要配置 DDS discovery server、静态 peer、端口或网络模式。

---

## 八、实战 workflow

从零到运行一个机器人系统的标准流程：

```
1. 写 URDF/XACRO → 定义机器人模型（关节、link、传感器安装位）
2. 写节点       → 传感器驱动、控制器、规划器
3. 写 launch     → 一键启动所有节点
4. rqt_graph     → 确认节点连接正确
5. ros2 topic echo → 逐个检查数据流
6. rviz2         → 可视化（TF、点云、图像）
```

### 常见坑

| 问题 | 解 |
|------|-----|
| colcon build 报找不到包 | `source /opt/ros/humble/setup.bash` 先 |
| 改了 Python 代码不生效 | `colcon build --symlink-install` |
| topic echo 没数据 | 检查 QoS 是否匹配（RELIABLE vs BEST_EFFORT） |
| 两个节点互相看不见 | `echo $ROS_DOMAIN_ID` 检查是否一致 |
| rviz2 看不到 TF | 检查 `use_sim_time` 参数是否一致 |

---

## 九、相关笔记

- [[空间与坐标系]] — TF 树、frame 约定
- [[感知 Perception/相机内外参]] — 相机标定与外参
- [[../CS_Note/工具/tmux]] — tmux 分割窗口跑多个 ROS 节点
- [[../CS_Note/工具/Docker]] — Docker 里跑 ROS2 避免环境污染
