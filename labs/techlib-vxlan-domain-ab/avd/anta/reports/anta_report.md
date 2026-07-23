# 📊 ANTA Report <a id="anta-report"></a>

**Table of Contents:**

- [ANTA Report](#anta-report)
  - [Test Results Summary](#test-results-summary)
    - [Summary Totals](#summary-totals)
    - [Summary Totals Device Under Test](#summary-totals-device-under-test)
    - [Summary Totals Per Category](#summary-totals-per-category)
  - [Test Results](#test-results)

## 📉 Test Results Summary <a id="test-results-summary"></a>

### 🔢 Summary Totals <a id="summary-totals"></a>

| Total Tests | ✅&nbsp;Success | ⏭️&nbsp;Skipped | ❌&nbsp;Failure | ❗&nbsp;Error |
| :- | :- | :- | :- | :- |
| 39 | 0 | 0 | 0 | 0 |

### 🔌 Summary Totals Device Under Test <a id="summary-totals-device-under-test"></a>

| Device | Total Tests | ✅&nbsp;Success | ⏭️&nbsp;Skipped | ❌&nbsp;Failure | ❗&nbsp;Error | Categories Skipped | Categories Failed |
| :- | :- | :- | :- | :- | :- | :- | :- |
| **A-SPINE1** | 39 | 0 | 0 | 0 | 0 | - | - |

### 🗂️ Summary Totals Per Category <a id="summary-totals-per-category"></a>

| Test Category | Total Tests | ✅&nbsp;Success | ⏭️&nbsp;Skipped | ❌&nbsp;Failure | ❗&nbsp;Error |
| :- | :- | :- | :- | :- | :- |
| **BGP** | 1 | 0 | 0 | 0 | 0 |
| **Configuration** | 4 | 0 | 0 | 0 | 0 |
| **Hardware** | 7 | 0 | 0 | 0 | 0 |
| **Interfaces** | 9 | 0 | 0 | 0 | 0 |
| **Logging** | 1 | 0 | 0 | 0 | 0 |
| **Routing** | 2 | 0 | 0 | 0 | 0 |
| **STP** | 1 | 0 | 0 | 0 | 0 |
| **System** | 14 | 0 | 0 | 0 | 0 |

## 🧪 Test Results <a id="test-results"></a>

| Device | Categories | Test | Description | Result | Messages |
| :- | :- | :- | :- | :- | :- |
| A-SPINE1 | BGP | VerifyBGPPeersHealth | Verifies the health of BGP peers for given address families. | Unset | - |
| A-SPINE1 | Configuration | VerifyRunningConfigDiffs | Verifies there is no difference between the running-config and the startup-config. | Unset | - |
| A-SPINE1 | Configuration | VerifyRunningConfigDiffs | Verifies there is no difference between the running-config and the startup-config. | Unset | - |
| A-SPINE1 | Configuration | VerifyZeroTouch | Verifies ZeroTouch is disabled. | Unset | - |
| A-SPINE1 | Configuration | VerifyZeroTouch | Verifies ZeroTouch is disabled. | Unset | - |
| A-SPINE1 | Hardware | VerifyEnvironmentCooling | Verifies the status of power supply fans and all fan trays. | Unset | - |
| A-SPINE1 | Hardware | VerifyEnvironmentPower | Verifies the power supplies state and input voltage. | Unset | - |
| A-SPINE1 | Hardware | VerifyEnvironmentSystemCooling | Verifies the device's system cooling status. | Unset | - |
| A-SPINE1 | Hardware | VerifyInventory | Verifies the physical hardware inventory of the device. | Unset | - |
| A-SPINE1 | Hardware | VerifyTemperature | Verifies if the device temperature is within acceptable limits. | Unset | - |
| A-SPINE1 | Hardware | VerifyTransceiversManufacturers | Verifies if all the transceivers come from approved manufacturers. | Unset | - |
| A-SPINE1 | Hardware | VerifyTransceiversTemperature | Verifies if all the transceivers are operating at an acceptable temperature. | Unset | - |
| A-SPINE1 | Interfaces | VerifyInterfaceDiscards | Verifies that the interfaces packet discard counters are equal to zero. | Unset | - |
| A-SPINE1 | Interfaces | VerifyInterfaceDiscards | Verifies that the interfaces packet discard counters are equal to zero. | Unset | - |
| A-SPINE1 | Interfaces | VerifyInterfaceErrDisabled | Verifies there are no interfaces in the errdisabled state. | Unset | - |
| A-SPINE1 | Interfaces | VerifyInterfaceErrDisabled | Verifies there are no interfaces in the errdisabled state. | Unset | - |
| A-SPINE1 | Interfaces | VerifyInterfaceErrors | Verifies that the interfaces error counters are equal to zero. | Unset | - |
| A-SPINE1 | Interfaces | VerifyInterfaceErrors | Verifies that the interfaces error counters are equal to zero. | Unset | - |
| A-SPINE1 | Interfaces | VerifyInterfaceUtilization | Verifies that the utilization of interfaces is below a certain threshold. | Unset | - |
| A-SPINE1 | Interfaces | VerifyInterfacesStatus | Verifies the operational states of specified interfaces to ensure they match expected configurations. | Unset | - |
| A-SPINE1 | Interfaces | VerifyL3MTU | Verifies the L3 MTU of routed interfaces. | Unset | - |
| A-SPINE1 | Logging | VerifyLoggingErrors | Verifies there are no syslog messages with a severity of ERRORS or higher. | Unset | - |
| A-SPINE1 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Unset | - |
| A-SPINE1 | Routing | VerifyRoutingProtocolModel | Verifies the configured routing protocol model. | Unset | - |
| A-SPINE1 | STP | VerifySTPCounters | Verifies there is no errors in STP BPDU packets. | Unset | - |
| A-SPINE1 | System | VerifyAgentLogs | Verifies there are no agent crash reports. | Unset | - |
| A-SPINE1 | System | VerifyAgentLogs | Verifies there are no agent crash reports. | Unset | - |
| A-SPINE1 | System | VerifyCPUUtilization | Verifies that the CPU utilization of the device is within the configured threshold. | Unset | - |
| A-SPINE1 | System | VerifyCoredump | Verifies there are no core dump files. | Unset | - |
| A-SPINE1 | System | VerifyCoredump | Verifies there are no core dump files. | Unset | - |
| A-SPINE1 | System | VerifyFileSystemUtilization | Verifies that no partition is utilizing more than 75% of its disk space. | Unset | - |
| A-SPINE1 | System | VerifyFileSystemUtilization | Verifies that no partition is utilizing more than 75% of its disk space. | Unset | - |
| A-SPINE1 | System | VerifyMaintenance | Verifies that the device is not currently under or entering maintenance. | Unset | - |
| A-SPINE1 | System | VerifyMemoryUtilization | Verifies whether the memory utilization is below 75%. | Unset | - |
| A-SPINE1 | System | VerifyMemoryUtilization | Verifies whether the memory utilization is below 75%. | Unset | - |
| A-SPINE1 | System | VerifyNTP | Verifies if NTP is synchronised. | Unset | - |
| A-SPINE1 | System | VerifyNTP | Verifies if NTP is synchronised. | Unset | - |
| A-SPINE1 | System | VerifyReloadCause | Verifies the last reload cause of the device. | Unset | - |
| A-SPINE1 | System | VerifyReloadCause | Verifies the last reload cause of the device. | Unset | - |
