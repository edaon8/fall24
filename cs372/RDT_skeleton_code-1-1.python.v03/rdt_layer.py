# rdt_layer.py
# by Ethan Daon
from segment import Segment


# #################################################################################################################### #
# RDTLayer                                                                                                             #
#                                                                                                                      #
# Description:                                                                                                         #
# The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable         #
# channel.                                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is meant to be changed.                                                                                    #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class RDTLayer(object):
    # ################################################################################################################ #
    # Class Scope Variables                                                                                            #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    DATA_LENGTH = 4 # in characters                     # The length of the string data that will be sent per packet...
    FLOW_CONTROL_WIN_SIZE = 15 # in characters          # Receive window size for flow-control
    sendChannel = None
    receiveChannel = None
    dataToSend = ''
    currentIteration = 0                                # Use this for segment 'timeouts'
    countSegmentTimeouts = 0
    currentWindow = [0, 4]
    currentSeqNum = 0
    nextSeqNum = 0
    serverData = []
    nextAck = 4
    numIters =  0
    

    # ################################################################################################################ #
    # __init__()                                                                                                       #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.currentIteration = 0
        self.countSegmentTimeouts = 0
        self.currentWindow = [0, 4]
        self.currentSeqNum = 0
        self.nextSeqNum = 0
        self.serverData = []
        self.nextAck = 4
        self.numIters =  0
        self.numTimeouts = 0

    # ################################################################################################################ #
    # setSendChannel()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable sending lower-layer channel                                                 #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # ################################################################################################################ #
    # setReceiveChannel()                                                                                              #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable receiving lower-layer channel                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # ################################################################################################################ #
    # setDataToSend()                                                                                                  #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the string data to send                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setDataToSend(self,data):
        self.dataToSend = data

    # ################################################################################################################ #
    # getDataReceived()                                                                                                #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to get the currently received and buffered string data, in order                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def getDataReceived(self):
        # ############################################################################################################ #
        # Identify the data that has been received...

        orderedData = []
        for i in range(self.nextAck):
            if i < len(self.serverData) and self.serverData[i] is not None:
                orderedData.append(self.serverData[i])

        dataString = ''.join(orderedData)

        # ############################################################################################################ #
        return dataString

    # ################################################################################################################ #
    # processData()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # "timeslice". Called by main once per iteration                                                                   #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processData(self):
        self.currentIteration += 1
        self.processSend()
        self.processReceiveAndSendRespond()

    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def checkReceivedAck(self, acks):
        for ack in acks:
            if ack.isAck():
                ackNum = int(ack.getAck())
                print(f"Received ACK for segment {ackNum}")
                if ackNum >= self.currentWindow[0]:
                    # Slide the window forward
                    self.currentWindow[0] = ackNum + 1
                    self.currentWindow[1] = min(self.currentWindow[0] + self.FLOW_CONTROL_WIN_SIZE, len(self.dataToSend))

    def processSend(self):
        # ############################################################################################################ #
        # print('processSend(): Complete this...')

        # You should pipeline segments to fit the flow-control window
        # The flow-control window is the constant RDTLayer.FLOW_CONTROL_WIN_SIZE
        # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH
        # These constants are given in # characters

        # Somewhere in here you will be creating data segments to send.
        # The data is just part of the entire string that you are trying to send.
        # The seqnum is the sequence number for the segment (in character number, not bytes)

        if not self.dataToSend:
            return

        splitData = []
        for i in range(0, len(self.dataToSend), self.DATA_LENGTH):
            chunk = self.dataToSend[i:i + self.DATA_LENGTH]
            splitData.append(chunk)

        # check for timeouts
        ackSegments = self.receiveChannel.receive()
        if self.currentIteration > 1 and len(ackSegments) == 0:
            if (self.numIters == 1): # timeout reached, resend window
                self.numTimeouts += 1
                print(f"Timeout reached. Resending window: {self.currentWindow}")
                self.currentSeqNum = self.currentWindow[0]
                self.numIters = 0
            else:
                self.numIters += 1
                return
        
        # handle acks
        for ackSeg in ackSegments:
            if ackSeg.acknum != -1:
                print(f"Received ACK for sequence number {ackSeg.acknum}")
                if ackSeg.acknum > self.currentWindow[0]:
                    self.currentWindow[0] = ackSeg.acknum
                    self.currentWindow[1] = ackSeg.acknum + self.DATA_LENGTH

        # now send new segs w/n the current window
        while self.currentSeqNum < self.currentWindow[1] and self.currentSeqNum < len(splitData) * self.DATA_LENGTH:
            segmentSend = Segment()
            seqnum = self.currentSeqNum
            data = splitData[seqnum // self.DATA_LENGTH]

            # prepare the segment
            segmentSend.setData(seqnum, data)
            print(f"Sending segment: {segmentSend.to_string()}")

            self.sendChannel.send(segmentSend)
            self.currentSeqNum += self.DATA_LENGTH


    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):
        segmentAck = Segment()                  # Segment acknowledging packet(s) received

        # This call returns a list of incoming segments (see Segment class)...
        listIncomingSegments = self.receiveChannel.receive()

        # ############################################################################################################ #
        # What segments have been received?
        # How will you get them back in order?
        # This is where a majority of your logic will be implemented
        # print('processReceive(): Complete this...')

        for segment in listIncomingSegments:
            if segment.acknum != -1:
                # handle ack
                print(f"Received ACK for sequence number {segment.acknum}")
            elif segment.seqnum != -1:
                # handle data seg
                print(f"Received data segment with seqnum {segment.seqnum} and data: {segment.payload}")
                self.serverData.append(segment.payload)
                self.nextAck += len(segment.payload)
                segmentAck.setAck(self.nextAck)
                self.sendChannel.send(segmentAck)


        # ############################################################################################################ #
        # How do you respond to what you have received?
        # How can you tell data segments apart from ack segemnts?
        # print('processReceive(): Complete this...')

        # Somewhere in here you will be setting the contents of the ack segments to send.
        # The goal is to employ cumulative ack, just like TCP does...
        # acknum = "0"


        # ############################################################################################################ #
        # Display response segment
        # segmentAck.setAck(acknum)
        # print("Sending ack: ", segmentAck.to_string())

        # Use the unreliable sendChannel to send the ack packet
        self.sendChannel.send(segmentAck)
