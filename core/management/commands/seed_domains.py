from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Domain, ProblemStatement, RubricCriterion


DOMAINS = [
    {
        "name": "Edge AI, Embedded Systems & IoT",
        "icon": "🤖",
        "tagline": "Real-time intelligence that runs on the metal, not the cloud.",
        "budget": "₹2000 / team",
        "order": 1,
        "problem_statements": [
            {
                "number": 1,
                "title": "EdgeShield — Wireless Threat Detection",
                "description": "Build a real-time wireless intrusion detection system that runs entirely on a microcontroller. The device must sniff 802.11 management frames and flag anomalies without cloud connectivity.",
                "context": "Industrial environments often lack reliable internet. Security must happen at the edge — latency budgets are measured in milliseconds, not seconds.",
                "minimum_requirements": [
                    "Detect at least 3 types of wireless anomalies (deauth floods, rogue APs, probe storms)",
                    "Alert latency < 500 ms",
                    "No cloud dependency — fully offline operation",
                    "Visual or serial output for alerts",
                ],
                "dependencies": [
                    "Arduino UNO R4 WiFi or ESP32 with monitor-mode support",
                    "802.11 packet capture library (e.g. ESP32 promiscuous mode)",
                    "Budget: ₹2000 (hardware must be sourced within this)",
                ],
                "rubric": [
                    ("Threat detection accuracy", "30%", "False positive rate penalised"),
                    ("Latency under load", "25%", "Tested with 50 concurrent devices"),
                    ("Code quality & documentation", "20%", "Inline comments + README"),
                    ("Demo & explainability", "15%", "Live demo mandatory"),
                    ("Innovation", "10%", "Novel detection heuristics"),
                ],
            },
            {
                "number": 2,
                "title": "TinyML Gesture Controller",
                "description": "Train and deploy a gesture recognition model on a microcontroller using IMU sensor data. The system must classify at least 6 distinct gestures in real-time and trigger corresponding device actions.",
                "context": "Touchless control interfaces are increasingly critical in sterile, industrial, and accessibility-focused environments. TinyML brings this capability to ₹500 hardware.",
                "minimum_requirements": [
                    "≥ 6 gesture classes with ≥ 85% accuracy on a held-out test set",
                    "Inference on-device (no streaming to PC)",
                    "Model size ≤ 256 KB flash",
                    "Real-time output: LED, buzzer, or serial trigger",
                ],
                "dependencies": [
                    "Arduino Nano 33 BLE Sense or Seeed XIAO nRF52840",
                    "Edge Impulse SDK or TensorFlow Lite Micro",
                    "IMU (MPU-6050 or on-board)",
                ],
                "rubric": [
                    ("Classification accuracy", "35%", "Judges will test live"),
                    ("Model efficiency (size/speed)", "25%", "Smaller + faster = better"),
                    ("Dataset quality & collection method", "20%", "Diversity of subjects"),
                    ("Demo clarity", "20%", "Can a non-expert use it?"),
                ],
            },
            {
                "number": 3,
                "title": "Predictive Maintenance Sentinel",
                "description": "Build an embedded system that monitors vibration and temperature of a rotating machine and predicts failure before it occurs using anomaly detection running on the microcontroller.",
                "context": "Unplanned downtime in manufacturing costs billions. A ₹500 edge sensor that predicts failures 10 minutes in advance changes the economics of maintenance entirely.",
                "minimum_requirements": [
                    "Continuous acquisition of vibration (accelerometer) + temperature",
                    "On-device anomaly scoring (no cloud)",
                    "Alert triggered ≥ 2 minutes before simulated failure",
                    "OLED or serial dashboard showing current health score",
                ],
                "dependencies": [
                    "ESP32 or STM32",
                    "ADXL345 or MPU-6050 accelerometer",
                    "DS18B20 or NTC thermistor",
                ],
                "rubric": [
                    ("Detection lead time", "30%", "Earlier warning = higher score"),
                    ("False alarm rate", "25%", "Must stay below 10%"),
                    ("System robustness", "25%", "Runs for 24 hours unattended"),
                    ("Presentation of insights", "20%", "Dashboard clarity"),
                ],
            },
            {
                "number": 4,
                "title": "Autonomous Rover Navigation",
                "description": "Design a rover that navigates an obstacle course autonomously using only onboard sensors — no camera, no GPS. The rover must complete a mapped path and return to start.",
                "context": "GPS-denied environments (underground, warehouses, disaster zones) require robust dead-reckoning and sensor-fusion navigation. This PS tests those fundamentals at low cost.",
                "minimum_requirements": [
                    "Complete a 2m × 2m obstacle course without human intervention",
                    "Return to origin within ±15 cm",
                    "No camera or external positioning system",
                    "Onboard obstacle avoidance (ultrasonic or IR)",
                ],
                "dependencies": [
                    "Arduino Mega or ESP32",
                    "HC-SR04 ultrasonic sensors (×3 minimum)",
                    "Encoder-equipped DC motors",
                    "L298N or L293D motor driver",
                ],
                "rubric": [
                    ("Course completion", "35%", "Timed; fewer collisions = bonus"),
                    ("Return accuracy", "25%", "Euclidean distance from origin"),
                    ("Algorithm design", "25%", "Elegance & extensibility"),
                    ("Build quality", "15%", "Mechanical reliability"),
                ],
            },
            {
                "number": 5,
                "title": "Smart Energy Harvesting Node",
                "description": "Build a battery-less IoT sensor node that harvests energy from ambient sources (solar, RF, or vibration) and transmits periodic sensor readings over a low-power wireless protocol.",
                "context": "Deploying thousands of sensors in the field is impractical when each needs a battery change every 6 months. Zero-power sensing enables truly pervasive IoT at scale.",
                "minimum_requirements": [
                    "No primary battery — must operate on harvested or supercapacitor energy",
                    "At least one sensor reading (temp, humidity, or light) transmitted every 5 minutes",
                    "Wireless range ≥ 5 m (BLE, LoRa, or Zigbee)",
                    "Demonstrate cold-start from zero charge",
                ],
                "dependencies": [
                    "Ambiq Apollo or nRF52 ultra-low-power MCU",
                    "Solar cell or RF energy harvester (e.g. P2110B)",
                    "Supercapacitor (1F–10F)",
                    "BLE or LoRa module",
                ],
                "rubric": [
                    ("Energy autonomy", "35%", "Longest gap without harvest wins"),
                    ("Transmission reliability", "25%", "Packet loss rate under test"),
                    ("Hardware design", "25%", "PCB or neat breadboard"),
                    ("Scalability argument", "15%", "Cost-per-node if mass produced"),
                ],
            },
        ],
    },
    {
        "name": "Aviation & Space Technology",
        "icon": "🚀",
        "tagline": "Altitude, orbit, and everything that has to fly right the first time.",
        "budget": "₹2000 / team",
        "order": 2,
        "problem_statements": [
            {
                "number": 1,
                "title": "Altitude-Hold Drone Controller",
                "description": "Implement a PID-based altitude-hold controller on a microcontroller that keeps a quad-rotor at a target height using only a barometric pressure sensor and IMU.",
                "context": "GPS-independent altitude hold is critical for indoor drones, micro-UAVs, and low-altitude inspection platforms where satellite signals are unavailable.",
                "minimum_requirements": [
                    "Altitude hold accuracy ±20 cm for 30 seconds",
                    "Response to manual setpoint change within 2 seconds",
                    "No GPS — baro + IMU only",
                    "Safety cutoff if tilt exceeds 45°",
                ],
                "dependencies": [
                    "STM32 or ESP32",
                    "BMP280 barometric sensor",
                    "MPU-6050 IMU",
                    "ESC + brushless motors (within budget)",
                ],
                "rubric": [
                    ("Altitude precision", "35%", "RMS error over 30 s"),
                    ("Disturbance rejection", "25%", "Judge applies gentle push"),
                    ("PID tuning methodology", "25%", "Documented tuning process"),
                    ("Safety features", "15%", "Failsafe demonstrated"),
                ],
            },
            {
                "number": 2,
                "title": "CubeSat Attitude Estimator",
                "description": "Implement a Madgwick or Mahony filter on a microcontroller to estimate the 3D orientation of a simulated CubeSat using magnetometer, accelerometer, and gyroscope data.",
                "context": "Attitude determination is one of the most fundamental problems in small satellite design. Doing it accurately on a microcontroller is a core embedded skill for space teams.",
                "minimum_requirements": [
                    "Quaternion output at ≥ 100 Hz",
                    "Yaw, pitch, roll error < 3° under slow rotation",
                    "Magnetic distortion compensation",
                    "Real-time 3D visualisation (serial or BLE to PC)",
                ],
                "dependencies": [
                    "Arduino Nano 33 BLE or equivalent 9-DOF IMU board",
                    "Python visualiser (PySerial + matplotlib or Processing)",
                ],
                "rubric": [
                    ("Angular accuracy", "35%", "Compared to reference"),
                    ("Update rate", "20%", "Measured with oscilloscope or timer"),
                    ("Disturbance handling", "25%", "Magnet placed near sensor"),
                    ("Visualisation quality", "20%", "Smooth, lag-free rendering"),
                ],
            },
            {
                "number": 3,
                "title": "Ground Station Telemetry Decoder",
                "description": "Build a real-time telemetry receiver that decodes LoRa packets from a simulated satellite transmitter, displays flight data on a dashboard, and flags anomalies automatically.",
                "context": "CubeSat ground stations require reliable, low-latency telemetry with built-in health monitoring. This PS simulates that pipeline end-to-end.",
                "minimum_requirements": [
                    "Decode at least 10 telemetry fields (altitude, temp, battery, RSSI…)",
                    "Live dashboard on PC (web or desktop)",
                    "Auto-alert on any field crossing threshold",
                    "Packet loss recovery / retransmit request",
                ],
                "dependencies": [
                    "2× LoRa modules (SX1278 or Ra-02)",
                    "ESP32 or Raspberry Pi Pico W for ground station",
                    "Dashboard: any language/framework",
                ],
                "rubric": [
                    ("Decoding accuracy", "30%", "All fields correct under noise"),
                    ("Dashboard usability", "25%", "Non-engineer must understand it"),
                    ("Anomaly detection", "25%", "True positives tested by judges"),
                    ("Packet loss handling", "20%", "Graceful degradation"),
                ],
            },
            {
                "number": 4,
                "title": "Parachute Deployment Timer",
                "description": "Design a flight computer that detects apogee and triggers a parachute deployment mechanism at the correct moment using barometric and accelerometric data fusion.",
                "context": "Model rocketry flight computers must reliably detect apogee within milliseconds. Premature or missed deployment means loss of vehicle. This PS demands safety-critical embedded thinking.",
                "minimum_requirements": [
                    "Apogee detection within ±100 ms on simulated flight profile",
                    "Arm/safe switch with LED indicators",
                    "Black-box logging to SD card",
                    "Servo or relay actuator trigger",
                ],
                "dependencies": [
                    "Arduino Nano or STM32 Blue Pill",
                    "BMP388 (high-resolution baro)",
                    "MicroSD breakout",
                    "SG90 servo for deployment sim",
                ],
                "rubric": [
                    ("Apogee detection timing", "40%", "Tested on 3 profiles"),
                    ("Black-box log integrity", "25%", "Readable after power cut"),
                    ("Safety switch implementation", "20%", "No accidental deployment"),
                    ("Code reliability", "15%", "No crashes over 24 h"),
                ],
            },
            {
                "number": 5,
                "title": "Wind-Aware Fixed-Wing Autopilot",
                "description": "Implement a heading-hold autopilot for a fixed-wing UAV that compensates for crosswind using an airspeed sensor and IMU, maintaining the desired ground track.",
                "context": "Wind compensation is the difference between a UAV that can fly a survey grid and one that drifts off-track. This PS targets that core control challenge at low hardware cost.",
                "minimum_requirements": [
                    "Hold heading ±5° under simulated crosswind (fan)",
                    "Airspeed-based throttle control",
                    "Waypoint sequencing (min 3 waypoints)",
                    "Manual override with smooth handoff",
                ],
                "dependencies": [
                    "STM32F4 or Pixhawk-compatible board",
                    "PITOT tube + differential pressure sensor (MPXV7002)",
                    "Servo outputs for aileron/elevator sim",
                ],
                "rubric": [
                    ("Heading hold accuracy", "35%", "Tested at 3 wind speeds"),
                    ("Waypoint tracking", "25%", "Cross-track error measured"),
                    ("Override smoothness", "20%", "No actuator jerk on handoff"),
                    ("Code architecture", "20%", "State machine clarity"),
                ],
            },
        ],
    },
    {
        "name": "Security & Privacy",
        "icon": "🔐",
        "tagline": "Break it, then build the version that can't be broken.",
        "budget": "₹2000 / team",
        "order": 3,
        "problem_statements": [
            {
                "number": 1,
                "title": "Hardware Security Key (FIDO2 Lite)",
                "description": "Build a USB HID security key on a microcontroller that performs challenge-response authentication using ECDSA, mimicking the FIDO2 protocol flow.",
                "context": "Hardware tokens are the strongest form of two-factor authentication. Understanding their internals — and building one from scratch — reveals the full trust chain.",
                "minimum_requirements": [
                    "USB HID enumeration on any OS without drivers",
                    "ECDSA P-256 sign/verify on-device",
                    "User presence button (physical touch required)",
                    "Demonstrate working login to a test app",
                ],
                "dependencies": [
                    "STM32 with USB FS or Raspberry Pi Pico",
                    "micro-ecc or MbedTLS library",
                    "USB HID descriptors (HID keyboard or custom)",
                ],
                "rubric": [
                    ("Cryptographic correctness", "40%", "Verified with known test vectors"),
                    ("USB compatibility", "25%", "Tested on Win/Mac/Linux"),
                    ("User presence enforcement", "20%", "Must fail without button press"),
                    ("Code documentation", "15%", "Security assumptions stated"),
                ],
            },
            {
                "number": 2,
                "title": "Encrypted LoRa Messaging Device",
                "description": "Build a pair of handheld devices that exchange end-to-end encrypted text messages over LoRa with no internet dependency, using AES-256 and a shared key exchange protocol.",
                "context": "Off-grid secure communication is essential for disaster relief, activism, and military edge operations. This PS builds the minimum viable secure messenger.",
                "minimum_requirements": [
                    "End-to-end AES-256 encryption",
                    "Key exchange without pre-shared secret (DH or ECDH)",
                    "OLED display + keypad or serial input",
                    "Range ≥ 100 m line-of-sight",
                ],
                "dependencies": [
                    "2× ESP32 + RA-02 LoRa modules",
                    "2× SSD1306 OLED displays",
                    "AES library (mbedTLS or Arduino Cryptography)",
                ],
                "rubric": [
                    ("Encryption correctness", "35%", "Intercept + decrypt attempt by judges"),
                    ("Key exchange security", "25%", "MITM resistance explained"),
                    ("Range & reliability", "25%", "Packet loss < 5% at 100 m"),
                    ("UX", "15%", "Usable without manual"),
                ],
            },
            {
                "number": 3,
                "title": "Side-Channel Attack Demonstrator",
                "description": "Demonstrate a power analysis attack on an unprotected AES implementation running on a microcontroller. Then harden it and show the attack fails.",
                "context": "Side-channel attacks break cryptography without touching the math. Understanding them is essential for anyone shipping secure hardware — and this PS teaches both the attack and the defence.",
                "minimum_requirements": [
                    "Capture power traces using current-sense resistor + ADC",
                    "Recover at least 1 byte of AES key via SPA or DPA",
                    "Implement masking countermeasure",
                    "Show attack failure rate before vs after hardening",
                ],
                "dependencies": [
                    "STM32 or Arduino running AES",
                    "Current-sense resistor (1 Ω)",
                    "Oscilloscope or high-speed ADC (ADS1115 or ESP32 ADC)",
                ],
                "rubric": [
                    ("Attack success", "35%", "Key byte recovered live"),
                    ("Countermeasure effectiveness", "30%", "Attack fails on hardened version"),
                    ("Explanation quality", "20%", "Can explain to a non-expert"),
                    ("Trace visualisation", "15%", "Clear, annotated plots"),
                ],
            },
            {
                "number": 4,
                "title": "Intrusion Detection via CAN Bus Anomaly",
                "description": "Monitor a simulated CAN bus network (automotive) for injected anomalous frames and trigger real-time alerts using a microcontroller-based IDS.",
                "context": "Modern vehicles are networks on wheels. CAN bus attacks are real — demonstrated on Jeep Cherokee in 2015. This PS builds the embedded IDS that should have been there.",
                "minimum_requirements": [
                    "Passively sniff CAN frames (no disruption to bus)",
                    "Detect replay, flooding, and spoofing attacks",
                    "Alert within 50 ms of attack start",
                    "Whitelist-based and frequency-based detection modes",
                ],
                "dependencies": [
                    "Arduino Uno or STM32 + MCP2515 CAN controller",
                    "CAN bus simulator (second MCU injecting frames)",
                    "CAN transceiver MCP2551",
                ],
                "rubric": [
                    ("Detection coverage", "35%", "All 3 attack types tested"),
                    ("Alert latency", "25%", "Measured with logic analyser"),
                    ("False positive rate", "25%", "Must be < 1% on clean traffic"),
                    ("Documentation", "15%", "Attack taxonomy explained"),
                ],
            },
            {
                "number": 5,
                "title": "Biometric Vault — Fingerprint-Gated Storage",
                "description": "Build a hardware-encrypted file vault that unlocks only after fingerprint verification, stores data on an SD card using AES-256, and wipes on repeated failed attempts.",
                "context": "Physical data security requires both \"something you are\" and \"something you have.\" This PS combines biometric auth with hardware-level encryption — the basis of every secure enclave.",
                "minimum_requirements": [
                    "Fingerprint enrolment + verification (FAR < 0.1%)",
                    "AES-256 file encryption on SD",
                    "Auto-wipe after 5 failed attempts",
                    "Re-enrolment after wipe (secure reset flow)",
                ],
                "dependencies": [
                    "Arduino Mega or ESP32",
                    "AS608 or R307 fingerprint sensor",
                    "MicroSD module",
                    "AES library",
                ],
                "rubric": [
                    ("Auth accuracy", "30%", "FAR and FRR measured"),
                    ("Encryption integrity", "30%", "File unreadable on raw SD read"),
                    ("Wipe mechanism", "25%", "Verified by judges — no bypass"),
                    ("Reset flow UX", "15%", "Clean re-enrol without residual data"),
                ],
            },
        ],
    },
    {
        "name": "Communications & Signal Processing",
        "icon": "🌊",
        "tagline": "Modulate, decode, denoise — make the signal survive the channel.",
        "budget": "₹2000 / team",
        "order": 4,
        "problem_statements": [
            {
                "number": 1,
                "title": "Software-Defined Radio APRS Decoder",
                "description": "Build an SDR-based APRS (Automatic Packet Reporting System) decoder that receives 144.800 MHz transmissions and displays real-time GPS position data on a map.",
                "context": "APRS is used by amateur radio operators, weather balloons, and emergency services. Decoding it from raw RF teaches the full communication stack — modulation, framing, error correction.",
                "minimum_requirements": [
                    "Decode AFSK 1200 baud AX.25 frames",
                    "Extract callsign, lat/lon, timestamp",
                    "Display on live map (Folium, Leaflet, or similar)",
                    "Decode ≥ 5 unique packets during demo",
                ],
                "dependencies": [
                    "RTL-SDR dongle (₹800–1200)",
                    "Python: pyrtlsdr, NumPy, SciPy",
                    "APRS replay file provided by organisers if live signal unavailable",
                ],
                "rubric": [
                    ("Decode accuracy", "35%", "Compared to reference decoder"),
                    ("Map visualisation", "25%", "Live update, clean UI"),
                    ("Pipeline architecture", "25%", "DSP stages documented"),
                    ("Edge cases handled", "15%", "Corrupt frames, overlapping TX"),
                ],
            },
            {
                "number": 2,
                "title": "Real-Time Speech Noise Canceller",
                "description": "Implement a real-time adaptive noise cancellation algorithm on a microcontroller that processes microphone input at 16 kHz and outputs clean audio via a speaker or DAC.",
                "context": "Industrial comms, hearing aids, and voice interfaces all require robust noise cancellation with sub-10 ms latency. This PS builds it from scratch in firmware.",
                "minimum_requirements": [
                    "16 kHz sample rate, real-time (no offline batch)",
                    "SNR improvement ≥ 10 dB on white noise test",
                    "Latency < 10 ms end-to-end",
                    "Adaptive to changing noise floor",
                ],
                "dependencies": [
                    "STM32F4 (FPU required) or ESP32-S3",
                    "I2S microphone (INMP441)",
                    "I2S DAC (MAX98357A) or PWM output",
                ],
                "rubric": [
                    ("SNR improvement", "35%", "Measured with calibrated noise"),
                    ("Latency", "25%", "Oscilloscope measured"),
                    ("Adaptability", "25%", "Noise type changed mid-demo"),
                    ("Code efficiency", "15%", "CPU% reported"),
                ],
            },
            {
                "number": 3,
                "title": "OFDM Modem on FPGA/MCU",
                "description": "Implement a simplified OFDM transmitter and receiver over an audio channel (3.5 mm jack) that achieves reliable data transfer at ≥ 1 kbps with audible carrier.",
                "context": "OFDM underlies 4G, 5G, Wi-Fi, and DSL. Building one from scratch — even at audio frequencies — makes the modulation concept concrete and deeply understood.",
                "minimum_requirements": [
                    "≥ 4 subcarriers",
                    "BER < 1% on a clean cable connection",
                    "Synchronisation handled (pilot tones or correlation)",
                    "Bit error rate displayed live",
                ],
                "dependencies": [
                    "STM32F4 with DAC/ADC or audio codec",
                    "Alternatively: Python TX + MCU RX (or vice versa)",
                    "3.5 mm TRS cable for loopback test",
                ],
                "rubric": [
                    ("BER performance", "35%", "Tested at 3 SNR levels"),
                    ("Throughput", "25%", "Bits/sec over 60 s"),
                    ("Sync robustness", "25%", "Cold start < 500 ms"),
                    ("Architecture explanation", "15%", "FFT stages clearly described"),
                ],
            },
            {
                "number": 4,
                "title": "Driver Drowsiness Detection System",
                "description": "Build an embedded system that detects driver drowsiness using EEG-like signals or eye-blink frequency from a sensor, and triggers a haptic or audio alert before microsleep onset.",
                "context": "Drowsy driving causes 1 in 5 fatal accidents. A low-cost embedded detector that works without a camera addresses the problem in markets where camera-based ADAS is unaffordable.",
                "minimum_requirements": [
                    "Detect drowsiness indicator (EEG delta-wave proxy, blink rate, or head-nod via IMU)",
                    "Alert within 2 seconds of drowsiness onset",
                    "False alert rate < 5% during 10-minute alert test",
                    "Haptic or buzzer alert, not just LED",
                ],
                "dependencies": [
                    "ESP32 or Arduino Mega",
                    "MPU-6050 (head-nod) OR AD8232 ECG (repurposed for bio-signal) OR IR eye sensor",
                    "Vibration motor or piezo buzzer",
                ],
                "rubric": [
                    ("Detection sensitivity", "35%", "Judges simulate drowsy behaviour"),
                    ("False alarm rate", "30%", "Alert on normal driving sim"),
                    ("Alert effectiveness", "20%", "Haptic must be perceptible"),
                    ("System robustness", "15%", "Works with glasses, head movement"),
                ],
            },
            {
                "number": 5,
                "title": "Acoustic Leak Detector",
                "description": "Use an array of MEMS microphones and cross-correlation to locate the source of an acoustic leak in a pipe, displaying distance-to-leak on an OLED without GPS or vision.",
                "context": "Water utilities lose 20–30% of supply to leaks. Acoustic localization is the gold standard detection method — and it can run on a ₹500 microcontroller.",
                "minimum_requirements": [
                    "≥ 2 microphone array with ≥ 1 m separation",
                    "Locate simulated leak to within ±20 cm on a 3 m pipe",
                    "Real-time cross-correlation processing on MCU",
                    "OLED display of distance estimate",
                ],
                "dependencies": [
                    "STM32F4 or ESP32-S3 (I2S microphones)",
                    "2× INMP441 microphones",
                    "PVC pipe segment for demo (provided by organisers)",
                ],
                "rubric": [
                    ("Localisation accuracy", "40%", "3 test positions, mean error scored"),
                    ("Processing speed", "25%", "Result in < 1 s of signal capture"),
                    ("Signal processing depth", "20%", "Filtering, windowing explained"),
                    ("Hardware robustness", "15%", "Survives handling during demo"),
                ],
            },
        ],
    },
    {
        "name": "Open Innovation (Wildcard)",
        "icon": "⚡",
        "tagline": "No brief. Full freedom. Bring the idea only you would build.",
        "budget": "₹2000 / team",
        "order": 5,
        "problem_statements": [
            {
                "number": 1,
                "title": "Smart Grid Micro-Inverter Controller",
                "description": "Design an embedded MPPT (Maximum Power Point Tracking) controller for a small solar panel that maximises energy harvest and feeds into a simulated load with efficiency monitoring.",
                "context": "Rooftop solar is the fastest growing energy source globally. The micro-inverter is its brain — and building one from a microcontroller up teaches power electronics fundamentals.",
                "minimum_requirements": [
                    "Perturb-and-Observe or Incremental Conductance MPPT",
                    "Efficiency ≥ 85% at rated load",
                    "Real-time power curve display (OLED or serial)",
                    "Over-voltage and reverse polarity protection",
                ],
                "dependencies": [
                    "STM32 or ESP32 with PWM output",
                    "5W–10W solar panel",
                    "Buck converter (synchronous preferred)",
                    "INA219 current/voltage sensor",
                ],
                "rubric": [
                    ("MPPT efficiency", "35%", "Vs. fixed-duty reference"),
                    ("Tracking speed", "25%", "Response to shade transition"),
                    ("Protection circuits", "25%", "Must not fry on judge test"),
                    ("Data logging", "15%", "Energy harvested over 1 hour"),
                ],
            },
            {
                "number": 2,
                "title": "Haptic Braille Display Controller",
                "description": "Build a refreshable Braille cell driver using solenoids or piezo actuators, controlled by a microcontroller that receives text via BLE and renders it as tactile Braille output.",
                "context": "Commercial Braille displays cost ₹50,000–2,00,000. A single-cell proof-of-concept using hobby actuators demonstrates the accessibility gap that embedded engineers can close.",
                "minimum_requirements": [
                    "At least 1 full Braille cell (6 dots) with tactile pin height ≥ 0.5 mm",
                    "BLE text input from a phone app or serial terminal",
                    "Correct Grade 1 Braille mapping for A–Z and 0–9",
                    "Auto-advance on timeout or button press",
                ],
                "dependencies": [
                    "Arduino Nano 33 BLE or ESP32 with BLE",
                    "6× mini solenoids or servo-driven cams",
                    "ULN2003 driver array",
                ],
                "rubric": [
                    ("Braille accuracy", "35%", "Blind evaluator or reference chart"),
                    ("Tactile feel", "25%", "Pin height and force measured"),
                    ("BLE reliability", "25%", "50 characters without drop"),
                    ("Accessibility impact statement", "15%", "Bill of materials vs. commercial cost"),
                ],
            },
            {
                "number": 3,
                "title": "Flood Early-Warning Sensor Node",
                "description": "Build a solar-powered water level sensor node that transmits alerts over LoRa when river levels exceed configurable thresholds, with local LED and siren output.",
                "context": "Flash floods kill thousands annually, often because warning systems are expensive or absent. A ₹1500 node that transmits 10 km without internet changes what's deployable.",
                "minimum_requirements": [
                    "Ultrasonic or pressure-based water level sensing",
                    "LoRa alert to base station ≥ 500 m away",
                    "Solar charging with battery backup (supercap or LiPo)",
                    "Configurable threshold via base station command",
                ],
                "dependencies": [
                    "ESP32 + LoRa (Ra-02)",
                    "JSN-SR04T waterproof ultrasonic sensor",
                    "6V solar panel + TP4056 charger + 18650 cell",
                ],
                "rubric": [
                    ("Sensing accuracy", "30%", "±2 cm at test depths"),
                    ("LoRa range & reliability", "25%", "Tested at 100 m minimum"),
                    ("Power autonomy", "30%", "Runtime without sun calculated"),
                    ("Remote configurability", "15%", "Threshold changed from base station"),
                ],
            },
            {
                "number": 4,
                "title": "Embedded Spectrum Analyser",
                "description": "Build a real-time audio spectrum analyser on a microcontroller with a live LED matrix or OLED waterfall display, using FFT computed entirely on-chip.",
                "context": "Spectrum analysis is fundamental to debugging RF, audio, and vibration signals. Building one from scratch — FFT to pixels — solidifies DSP intuition like nothing else.",
                "minimum_requirements": [
                    "256-point FFT at ≥ 30 frames/second",
                    "Frequency resolution ≤ 100 Hz / bin",
                    "Visual display: LED matrix, OLED, or serial plotter",
                    "Peak frequency label shown numerically",
                ],
                "dependencies": [
                    "STM32F4 or ESP32 (hardware FPU preferred)",
                    "INMP441 microphone or 3.5 mm ADC input",
                    "WS2812B LED matrix or SSD1306 OLED",
                ],
                "rubric": [
                    ("FFT accuracy", "30%", "Known tones verified"),
                    ("Frame rate", "25%", "Measured with oscilloscope trigger"),
                    ("Display quality", "25%", "Resolution, brightness, clarity"),
                    ("Feature depth", "20%", "Peak hold, windowing, log scale"),
                ],
            },
            {
                "number": 5,
                "title": "Open Problem — Team's Choice",
                "description": "Propose and build your own embedded systems solution to a real-world problem of your choice. The problem statement must be submitted and approved within the first 2 hours of the hackathon.",
                "context": "The best problems are ones teams actually care about. This slot exists so that genuinely novel ideas don't get shoehorned into the wrong domain. Full creative freedom — with full accountability.",
                "minimum_requirements": [
                    "Problem statement approved by a judge within the first 2 hours",
                    "Hardware + firmware component mandatory (not pure software)",
                    "Real-world use case with named beneficiary",
                    "Working demo at judging time — no PowerPoint-only submissions",
                ],
                "dependencies": [
                    "Team's own hardware selection (within ₹2000 budget)",
                    "PS approval form submitted to organisers by Hour 2",
                ],
                "rubric": [
                    ("Problem significance", "25%", "Real need, real beneficiary"),
                    ("Technical depth", "30%", "Not a tutorial project"),
                    ("Demo quality", "25%", "Works live, judge can operate it"),
                    ("Innovation", "20%", "Would this be novel at a conference?"),
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed Domain, ProblemStatement, and RubricCriterion data for the Tracks pages.'

    def handle(self, *args, **options):
        for d_index, d in enumerate(DOMAINS, start=1):
            domain, created = Domain.objects.update_or_create(
                slug=slugify(d['name']),
                defaults={
                    'icon': d['icon'],
                    'name': d['name'],
                    'tagline': d['tagline'],
                    'budget': d['budget'],
                    'order': d['order'],
                    'is_active': True,
                }
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f"{action} domain: {domain.name}")

            for ps_index, ps in enumerate(d['problem_statements'], start=1):
                problem_statement, ps_created = ProblemStatement.objects.update_or_create(
                    domain=domain,
                    number=ps['number'],
                    defaults={
                        'title': ps['title'],
                        'description': ps['description'],
                        'context': ps['context'],
                        'minimum_requirements': '\n'.join(ps['minimum_requirements']),
                        'dependencies': '\n'.join(ps['dependencies']),
                        'order': ps_index,
                    }
                )
                # Reset rubric rows each time to keep them in sync with the seed data
                problem_statement.rubric_criteria.all().delete()
                for r_index, (criterion, weight, notes) in enumerate(ps['rubric'], start=1):
                    RubricCriterion.objects.create(
                        problem_statement=problem_statement,
                        criterion=criterion,
                        weight=weight,
                        notes=notes,
                        order=r_index,
                    )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(DOMAINS)} domains with problem statements and rubrics."
        ))
