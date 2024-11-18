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
    send_base = 0
    next_seq_num = 0
    timeouts = {}
    unacked_segments = {}
    rcv_base = 0
    received_data = ''
    buffered_data = {}
    window_size = FLOW_CONTROL_WIN_SIZE // DATA_LENGTH
    expected_seq_num = 0
    # Add items as needed

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
        self.send_base = 0
        self.next_seq_num = 0
        self.timeouts = {}
        self.unacked_segments = {}
        self.rcv_base = 0
        self.received_data = ''
        self.buffered_data = {}
        self.window_size = self.FLOW_CONTROL_WIN_SIZE // self.DATA_LENGTH
        self.expected_seq_num = 0
        # self.timeout_threshold = 5
        # Add items as needed

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

        # print('getDataReceived(): Complete this...')

        # ############################################################################################################ #
        return self.received_data

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

        # first check if we can send new segments
        while self.next_seq_num < self.send_base + self.window_size and self.next_seq_num * self.DATA_LENGTH < len(self.dataToSend):
            data_start = self.next_seq_num * self.DATA_LENGTH
            data_end = data_start + self.DATA_LENGTH
            segment_data = self.dataToSend[data_start:data_end]
            # create a new segment
            segmentSend = Segment()
            segmentSend.setData(self.next_seq_num, segment_data)

            self.unacked_segments[self.next_seq_num] = segmentSend
            self.timeouts[self.next_seq_num] = self.currentIteration

            print("Sending segment: ", segmentSend.to_string())
            self.sendChannel.send(segmentSend)
            self.next_seq_num += 1
        
        # check for a timeout and retransmit if necessary
        for seq, start_time in list(self.timeouts.items()):
            if self.currentIteration - start_time > 3: # arbitrary timeout val (may change)
                print("Timeout: Resending segment ", seq)
                self.sendChannel.send(self.unacked_segments[seq])
                self.timeouts[seq] = self.currentIteration

    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):
        segmentAck = Segment()
        listIncomingSegments = self.receiveChannel.receive()

        for segment in listIncomingSegments:
            if segment.checkChecksum() and segment.seqnum >= 0:
                print(f"Received segment: {segment.to_string()}")
                # debug
                print(f"Expected seqnum: {self.rcv_base}, Received seqnum: {segment.seqnum}")
                print(f"Received data: {segment.payload}")

                
                # store the segment if within the receive window
                if self.rcv_base <= segment.seqnum < self.rcv_base + self.window_size:
                    self.buffered_data[segment.seqnum] = segment.payload

                    # process contiguous segs
                    while self.rcv_base in self.buffered_data:
                        self.received_data += self.buffered_data.pop(self.rcv_base)
                        self.rcv_base += 1

                # send ack
                segmentAck.setAck(self.rcv_base)
                print(f"Sending ack: {segmentAck.to_string()}")
                self.sendChannel.send(segmentAck)
            else:
                print("Checksum error or invalid segment. Ignoring.")

        if not listIncomingSegments:
            print("No segments received.")


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
