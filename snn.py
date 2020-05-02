# SNN that models the XOR gate
# 0 0 -> 0
# 0 1 -> 1
# 1 0 -> 1
# 1 1 -> 0

class NeuralNetwork:

    def sdtp_train(self):
        # TODO implement sdtp learning
        return

    def hebb_train(self):
        # TODO implement hebbian learning
        return

    def validate(self, inputs):
        """ Validates training by using testing data
        returns output for input values
        """

        input1 = inputs[0]
        input2 = inputs[1]

        # input layer
        encoded_input1 = self.__fr_encoded_input(input1)
        encoded_input2 = self.__fr_encoded_input(input2)

        # hidden layer
        hiddenNeuron1 = LIFNeron()
        hiddenNeuron2 = LIFNeron()
        hiddenNeuron3 = LIFNeron()
        hiddenNeuron4 = LIFNeron()

        spike_train1 = hiddenNeuron1.get_spike_train([encoded_input1, encoded_input2])
        spike_train2 = hiddenNeuron2.get_spike_train([encoded_input1, encoded_input2])
        spike_train3 = hiddenNeuron3.get_spike_train([encoded_input1, encoded_input2])
        spike_train4 = hiddenNeuron4.get_spike_train([encoded_input1, encoded_input2])

        # output layer
        outputNeuron = LIFNeron()

        final_spike_train = outputNeuron.get_spike_train([spike_train1, spike_train2, spike_train3, spike_train4])
        decoded_output_value = self.__decode_output(final_spike_train)

        return decoded_output_value

    def __fr_encoded_input(self, input):
        """ encodes input via firing rate encoding
        returns 100ms period with spiking activity (1) vs no spiking activity (0)
        """
        encoded_input = []
        spike_freq = 20 if input == 0 else 10
        for t in range(100):
            if (t + 1) % spike_freq == 0 and t != 0:
                encoded_input.append(1)
            else:
                encoded_input.append(0)
        return encoded_input

    def __decode_output(self, input):
        """ decodes spike train to output value
        returns 0 or 1
        """

        spikes = 0
        for value in input:
            if value == 1:
                spikes += 1
        # these values should be continuous rather than discrete
        # the threshold values can depend on the success of the learning process
        if spikes == 5:
            return 0
        elif spikes == 10:
            return 1
        else:
            return -1

class LIFNeron:

    def __init__(self):
        self.r = 1.0
        self.c = 10.0
        self.tau = self.r * self.c
        self.rest = -65.0
        self.thresh = -60.0
        self.current = 4.0

    def get_spike_train(self, spike_trains):
        spike_train = map(sum, zip(*spike_trains)) # sum of spike trains
        v = self.rest
        current = 0
        output_spike_train = []
        for value in spike_train:
            v += (1 / self.tau) * (-(v - self.rest) + self.r * self.current) # Membrane potential equation
            # adjust voltage based on weights and value in spike train here
            if v >= self.thresh:
                # Spike is generated
                v = self.rest
                output_spike_train.append(1)
            else:
                # Spike is not generated
                output_spike_train.append(0)
        print(output_spike_train)
        return output_spike_train

NN = NeuralNetwork()
# NN.hebb_train()
# NN.sdtp_train()
print(NN.validate([0, 1]))
