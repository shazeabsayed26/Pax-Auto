<div align="center">
  <h1 style="font-size: 36px;">Feature: User can experience a seamless and smooth driving journey between requested location</h1>
</div>


## Feature Owner: Shazeab Sayed
## 📚 Contents
- [Feature Overview](#feature-overview)
- [Test Strategy](#test-strategy)
- [Evaluation](#evaluation)

## Feature Overview
- Smooth and Seamless Autonomous Navigation is a system-level feature designed to enable the autonomous shuttle to travel continuously and reliably between requested locations within the Model City environment. (Smooth refers to the generation of smooth path for Motion execution and Seamless refers to the execution of trajectory control without interruptions) .From the user’s perspective, the shuttle navigates between locations in a predictable and uninterrupted manner while safely executing straight paths and turning maneuvers. The navigation behavior remains continuous without unnecessary stops, ensuring a reliable and comfortable travel experience.<br>
- Internally, this feature combines path planning and trajectory control. Path planning generates a feasible and continuous navigation path between the requested start and destination locations, while lateral and longitudinal control ensures that the shuttle follows this path safely through appropriate steering and speed commands. When a turning maneuver cannot be completed using forward-only motion due to vehicle kinematic constraints, the system performs a controlled reverse maneuver to safely complete the navigation task. The feature ensures predictable and collision-free navigation within the
defined operational scope of the Model City environment.<br>


**Key Performance Indicators (KPIs)**
1. Planning success rate: A valid and continuous navigation path is generated for the requested destination.

  - KPI 1: Planning Success Rate
  - Total navigation requests executed: n
  - Successful path generations: n
  - Planning success rate: (expected 100%)

2. Successful route completion: The shuttle reaches the destination without collision or unintended interruption.
  - KPI 2: Successful Route Completion
  - Total route executions: n
  - Successful destination arrivals: n
  - Route completion success rate: (expected 100%)

3. Maneuver completion success: Turning maneuvers are completed safely within vehicle constraints.
  - KPI 3: Maneuver Completion Success
  - Reverse maneuver success: n
  - Steering constraint violations (>30°):  Expected 0
  - Maneuver completion success rate: ( Expected 100%)


**Feature Functionality / Properties**

-	Generates feasible navigation paths between requested locations.
-	Produces continuous paths consisting of straight and turning segments.
-	Executes the planned path using lateral and longitudinal control.
-	Tracks navigation paths continuously using steering and speed commands.
-	Executes forward-only motion when turning constraints allow.
-	Executes controlled reverse maneuvers when forward-only motion is infeasible.
-	Ensures continuous navigation behavior within the Model City layout.


## Test Strategy
Detailed Test Strategy document can be found [here](https://git.hs-coburg.de/pax_auto/pax_auto_main/src/branch/main/test/scenario_based_testing/feature_4/Test_Stratgy_Document_Shazeab.pdf).

## Evaluation
Detailed evaluation is documented [here](https://git.hs-coburg.de/pax_auto/pax_auto_main/src/branch/main/test/scenario_based_testing/feature_4/Feature_Testing_Paxauto_Shazeab.xlsx).