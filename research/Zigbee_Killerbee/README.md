# Introduction

Two tools stand out in the security analysis of Zigbee networks: Killerbee, a professional penetration test framework known for the range of features and for its wide use, and the CC2531,a popular hardware device well known for its low price .

Some solutions that allow compatibility between KillerBee and CC2531 are currently available but they only support sniffing features. 

# Goal

The aim of this research is to create a solution based on KilleBee and CC2531 that allows to extend the currently supported functionalities by providing the ability to actively transmit packets within the Zigbee network using the CC2531.

To achieve this goal, the open source firmware provided by ZBOSS has been used and modified in order to implement the desired data transmission feature. The new firmware (ZBOSS\_extended), which was not supported by the KillerBee framework, has been adapted for the purpose. Consequently, the Killerbee drivers have been implemented to provide compatibility with the CC2531 mounting the new firmware.

## Content

Content of the research:
- General introduction to Zigbee
- General introduction to KillerBee and compatible devices
- Implementation of the proposed solution

The research is entirely written in Italian :) 
Working on a English translation soon.
