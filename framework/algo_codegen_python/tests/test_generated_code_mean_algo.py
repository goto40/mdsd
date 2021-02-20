from P1.MeanAlgo import MeanAlgo
from Items.MeanAlgoInput import MeanAlgoInput as I
from Items.MeanAlgoOutput import MeanAlgoOutput as O

def test_custom_impl_of_MeanAlgo():
    class MyMeanAlgo(MeanAlgo):
        def compute(self, inp1: I, inp2: I, oup: O):
            outp.value = (inp1.value + inp2.value)/2

    a = MyMeanAlgo()
    inp1 = I(9)
    inp2 = I(7)
    outp = O()
    a.compute(inp1, inp2, outp)
    assert outp.value == 8
