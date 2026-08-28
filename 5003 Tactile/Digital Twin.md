## 数字峦生

![[Screenshot 2026-08-26 at 4.30.53 PM.png|495]]


**Object-conditioning World Model**

Can a world model use rapidly acquired physical object assets in the same way that a physics simulator uses manually specified simulation assets?


## 触觉数据

The tactile sensor’s position is computed via forward kinematics and transformed into the camera’s 3D coordinate frame, preserving the spatial relationships between the two modalities.

- fit a Kelvin–Voigt viscoelastic model by iteratively tuning the elastic modulus kn (compliance stiffness) and viscosity coefficient kd (damping)
## 数据集组成
数据集分成两个部分，
一个部分做个体的asset，
另一个部分采少量的manipulation数据训练policy，并且可以直接组合生成剩余的部分


## 算法改造
做后训练的数据
路线一：asset encoder （mask掉一部分可以得到encoder，不需要有manipulation数据） 和 adapter
路线二：
![[Screenshot 2026-08-26 at 8.00.53 PM.png|423]]


https://events.comp.nus.edu.sg/view/26399?utm_source=chatgpt.com


## 实验
新采一个物体A的asset，和已知的物体B，直接做交互，看结果是否好过 视觉-only