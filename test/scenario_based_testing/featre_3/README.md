<div align="center">
  <h1 style="font-size: 36px;">Feature: User can take the shuttle when external positioning system (OptiTrack) is temporarily  unavailable</h1>
</div>

## Feature Owner: Yashashwi Raja Gowda


## 📚 Contents
- [Feature Overview](#feature-overview)
- [Evaluation](#evaluation)

## Feature Overview
The shuttle is designed to remain operational even when external positioning is temporarily unavailable. During such situations, the system automatically switches to dead-reckoning based on wheel odometry and the last known position to estimate the shuttle’s movement, allowing it to continue driving through areas such as tunnels without user intervention. While a small, expected drift may occur over time, motion remains stable and controlled. When external positioning is available, the system uses a linear Kalman filter to continuously correct and stabilize the shuttle’s position, and once external positioning becomes available again after a dropout, the shuttle’s position is seamlessly realigned without noticeable jumps or interruptions, ensuring a smooth and reliable user experience.

**Key Performance Indicators (KPIs)**
The following KPIs define the system-level quality measures used to evaluate this feature:
1. Position stability: Estimated position remains continuous without sudden jumps
2. Velocity consistency: Velocity estimates remain smooth, especially during stops and restarts
3. Acceleration behaviour: Acceleration changes are smooth and physically realistic
4. Orientation continuity: Vehicle orientation remains consistent across localization mode transitions


**Feature Functionality / Properties**

This feature provides the following functionality:

- Uses vehicle speed information from Ackermann drive feedback for motion propogation
- Uses pose information from Model Cars for state estimation
-	Publishes continuous odometry output when OptiTrack is unavailable
-	Derives vehicle velocity from Ackermann drive feedback
-	Maintains stable estimates of position, velocity, acceleration, and orientation
-	Handles smooth transitions between external positioning and dead reckoning
-	Supports intentional vehicle stops and restarts at pickup and drop-off points inside tunnel regions
-	Prevents discontinuities in odometry during planned stops and motion resumption


Feature images can be found [here.](https://git.hs-coburg.de/pax_auto/localization#feature)

## Evaluation

The localization system was evaluated using three scenario-based tests: traversal through a tunnel without external positioning (OptiTrack) (happy flow), a planned stop and restart inside the tunnel without external positioning (alternate flow), and vehicle start inside a tunnel region without sufficient localization initialization (edge case). In the first two scenarios, localization output remained continuous without pose dropouts, relying on dead-reckoning based on wheel odometry with stable behavior and controlled, expected drift. When external positioning was available, localization utilized a linear Kalman filter to fuse external pose updates with odometry, providing stable and corrected state estimates. In the edge case scenario, where external positioning was unavailable before a valid localization state could be established and dead-reckoning could not be initialized, the system prevented the vehicle from moving forward. Once external positioning became available, localization was initialized and normal localization behavior resumed without discontinuities. All Key Performance Indicators defined in the test strategy were met. 

Detailed evaluation is documented in [Test Specification](https://hscoburgde-my.sharepoint.com/:x:/g/personal/yas8416s_hs-coburg_de/IQDgUIbgDOXgQ5HyVwBNeGG4AS1H-nwF8YS-619K1EB0QiU?e=9OEKde) document.

Test Strategy document can be found [here.](https://drive.google.com/file/d/1v9XIzPNozHYK4WEYhit5cvRkzdPosFxb/view?usp=drivesdk)